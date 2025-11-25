import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODELS_TO_DOWNLOAD = [
    {
        "url": "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/I2V/Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors",
        "path": "/ComfyUI/models/diffusion_models/Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors"
    },
    {
        "url": "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/I2V/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors",
        "path": "/ComfyUI/models/diffusion_models/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors"
    },
    {
        "url": "https://huggingface.co/lightx2v/Wan2.2-Lightning/resolve/main/Wan2.2-I2V-A14B-4steps-lora-rank64-Seko-V1/high_noise_model.safetensors",
        "path": "/ComfyUI/models/loras/high_noise_model.safetensors"
    },
    {
        "url": "https://huggingface.co/lightx2v/Wan2.2-Lightning/resolve/main/Wan2.2-I2V-A14B-4steps-lora-rank64-Seko-V1/low_noise_model.safetensors",
        "path": "/ComfyUI/models/loras/low_noise_model.safetensors"
    },
    {
        "url": "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/clip_vision/clip_vision_h.safetensors",
        "path": "/ComfyUI/models/clip_vision/clip_vision_h.safetensors"
    },
    {
        "url": "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-bf16.safetensors",
        "path": "/ComfyUI/models/text_encoders/umt5-xxl-enc-bf16.safetensors"
    },
    {
        "url": "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors",
        "path": "/ComfyUI/models/vae/Wan2_1_VAE_bf16.safetensors"
    }
]

def download_file(url, path):
    if os.path.exists(path):
        logger.info(f"✅ File already exists: {path}")
        return

    logger.info(f"⬇️ Downloading {url} to {path}...")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    try:
        subprocess.run(['wget', '-O', path, '--no-verbose', url], check=True)
        logger.info(f"✅ Downloaded {path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to download {url}: {e}")
        raise

def check_and_download_models():
    logger.info("Checking and downloading models...")
    for model in MODELS_TO_DOWNLOAD:
        download_file(model["url"], model["path"])
    logger.info("✅ All models checked/downloaded.")

if __name__ == "__main__":
    check_and_download_models()
