#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Start ComfyUI in the background
echo "Starting ComfyUI in the background..."

echo "DEBUG: Listing root / content:"
ls -F /

echo "DEBUG: Checking /runpod-volume..."
if [ -d "/runpod-volume" ]; then
    echo "/runpod-volume exists. Listing content:"
    ls -F /runpod-volume
else
    echo "/runpod-volume does NOT exist."
fi

echo "Waiting for /runpod-volume/models to be available..."
max_retries=30
count=0
while [ ! -d "/runpod-volume/models" ] && [ $count -lt $max_retries ]; do
    sleep 1
    count=$((count + 1))
    echo "Waiting for /runpod-volume/models... ($count/$max_retries)"
done

if [ -d "/runpod-volume/models" ]; then
    echo "/runpod-volume/models found!"
    ls -F /runpod-volume/models
else
    echo "ERROR: /runpod-volume/models NOT found after waiting. Listing /runpod-volume again:"
    ls -F /runpod-volume || echo "/runpod-volume not accessible"
fi

python /ComfyUI/main.py --listen --use-sage-attention &

# Wait for ComfyUI to be ready
echo "Waiting for ComfyUI to be ready..."
max_wait=120  # 최대 2분 대기
wait_count=0
while [ $wait_count -lt $max_wait ]; do
    if curl -s http://127.0.0.1:8188/ > /dev/null 2>&1; then
        echo "ComfyUI is ready!"
        break
    fi
    echo "Waiting for ComfyUI... ($wait_count/$max_wait)"
    sleep 2
    wait_count=$((wait_count + 2))
done

if [ $wait_count -ge $max_wait ]; then
    echo "Error: ComfyUI failed to start within $max_wait seconds"
    exit 1
fi

# Start the handler in the foreground
# 이 스크립트가 컨테이너의 메인 프로세스가 됩니다.
echo "Starting the handler..."
exec python handler.py