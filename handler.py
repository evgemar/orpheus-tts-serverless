"""RunPod Serverless handler for prakharsr/Orpheus-TTS-FastAPI."""

import base64
import subprocess
import time

import requests
import runpod

INTERNAL_URL = "http://127.0.0.1:8880"

# Start FastAPI server in background
subprocess.Popen(
    ["uvicorn", "fastapi_app:app", "--host", "127.0.0.1", "--port", "8880"],
    cwd="/app",
)

# Wait for server to be ready
print("[Handler] Waiting for FastAPI server...")
for _ in range(120):  # up to 4 minutes
    try:
        r = requests.get(f"{INTERNAL_URL}/health", timeout=3)
        if r.ok:
            print("[Handler] FastAPI server is ready!")
            break
    except Exception:
        pass
    time.sleep(2)
else:
    print("[Handler] WARNING: Server did not become ready in time")


def handler(job):
    inp = job["input"]
    text = inp.get("text", "")
    if not text.strip():
        return {"error": "Input text is missing or empty"}

    voice = inp.get("voice", "tara")

    payload = {
        "model": "orpheus",
        "input": text,
        "voice": voice,
        "response_format": "wav",
    }

    # Pass through optional params if provided
    if "speed" in inp:
        payload["speed"] = inp["speed"]
    if "temperature" in inp:
        payload["temperature"] = inp["temperature"]
    if "top_p" in inp:
        payload["top_p"] = inp["top_p"]
    if "repetition_penalty" in inp:
        payload["repetition_penalty"] = inp["repetition_penalty"]
    if "max_tokens" in inp:
        payload["max_tokens"] = inp["max_tokens"]

    try:
        resp = requests.post(
            f"{INTERNAL_URL}/v1/audio/speech",
            json=payload,
            timeout=300,
        )
    except requests.Timeout:
        return {"error": "TTS generation timed out (300s)"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

    if resp.status_code != 200:
        return {"error": f"TTS error {resp.status_code}: {resp.text[:500]}"}

    audio_b64 = base64.b64encode(resp.content).decode("utf-8")
    return {"audio_base64": audio_b64, "format": "wav"}


runpod.serverless.start({"handler": handler})
