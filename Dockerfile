FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install Python 3.12
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common git curl && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3.12-dev && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    ln -sf /usr/bin/python3.12 /usr/bin/python && \
    ln -sf /usr/bin/python3.12 /usr/bin/python3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone the Orpheus-TTS-FastAPI repo and install deps
RUN git clone https://github.com/prakharsr/Orpheus-TTS-FastAPI.git . && \
    pip install --no-cache-dir -r requirements.txt runpod

# Copy serverless handler
COPY handler.py .

CMD ["python", "handler.py"]
