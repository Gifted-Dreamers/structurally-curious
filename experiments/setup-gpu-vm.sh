#!/bin/bash
# Setup script for Azure GPU VM — run after SSH'ing in
# Usage: ssh azureuser@<VM_IP> 'bash -s' < setup-gpu-vm.sh

set -e

echo "=== GPU VM Setup for Structurally Curious Experiments ==="
echo "Started: $(date)"

# 1. Install NVIDIA drivers + CUDA (Ubuntu 24.04)
echo "--- Installing NVIDIA drivers ---"
sudo apt-get update -qq
sudo apt-get install -y -qq ubuntu-drivers-common
sudo ubuntu-drivers install --gpgpu
sudo apt-get install -y -qq nvidia-cuda-toolkit

# 2. Install Python environment
echo "--- Setting up Python ---"
sudo apt-get install -y -qq python3-pip python3-venv
python3 -m venv ~/exp-env
source ~/exp-env/bin/activate

# 3. Install PyTorch (CUDA 12.x)
echo "--- Installing PyTorch ---"
pip install --quiet torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# 4. Install experiment dependencies
echo "--- Installing dependencies ---"
pip install --quiet transformers accelerate scipy numpy huggingface_hub

# 5. Pre-download model weights
echo "--- Downloading Qwen 3.5 models ---"
python3 -c "
from huggingface_hub import snapshot_download
import os

models = [
    'Qwen/Qwen3.5-4B',
    'Qwen/Qwen3.5-9B',
]

for m in models:
    print(f'Downloading {m}...')
    snapshot_download(m)
    print(f'  Done: {m}')

# MoE model — larger download, do last
print('Downloading Qwen/Qwen3.5-35B-A3B (MoE)...')
snapshot_download('Qwen/Qwen3.5-35B-A3B')
print('  Done: Qwen3.5-35B-A3B')
"

# 6. Verify GPU access
echo "--- Verifying GPU ---"
python3 -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB')
"

echo ""
echo "=== Setup complete: $(date) ==="
echo "Activate with: source ~/exp-env/bin/activate"
echo "Run experiments from ~/experiments/"
