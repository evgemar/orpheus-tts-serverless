# Orpheus TTS Serverless (RunPod)

RunPod Serverless handler wrapping [prakharsr/Orpheus-TTS-FastAPI](https://github.com/prakharsr/Orpheus-TTS-FastAPI).

## Input

```json
{"input": {"text": "Hello world", "voice": "tara"}}
```

Voices: tara, leah, jess, leo, dan, mia, zac, zoe

## Output

```json
{"audio_base64": "<base64 WAV>", "format": "wav"}
```
