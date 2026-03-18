#!/bin/bash
# Setup script for GPU server — run after SSH'ing in
# Usage: ssh user@<IP> 'bash -s' < setup-gpu-vm.sh
#
# Designed for Cassidy's Liberation Labs GPU server (~April 2026)
# or any Ubuntu machine with NVIDIA GPU.
#
# What this installs:
#   - NVIDIA drivers + CUDA
#   - PyTorch with CUDA support
#   - HuggingFace Transformers (for hidden-state extraction)
#   - Models needed for cross-architecture geometric validation
#
# After setup, run experiments from experiments/ directory.
# All F-series scripts use output_hidden_states=True for geometric extraction.

set -e

echo "=== GPU Setup for Structurally Curious Experiments ==="
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
python3 -m venv ~/experiments-env
source ~/experiments-env/bin/activate

# 3. Install PyTorch (CUDA 12.x)
echo "--- Installing PyTorch ---"
pip install --quiet torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# 4. Install experiment dependencies
echo "--- Installing dependencies ---"
pip install --quiet transformers accelerate scipy numpy huggingface_hub bitsandbytes

# 5. Verify GPU access
echo "--- Verifying GPU ---"
python3 -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        print(f'GPU {i}: {torch.cuda.get_device_name(i)}')
        print(f'  VRAM: {torch.cuda.get_device_properties(i).total_mem / 1e9:.1f} GB')
    print(f'Total GPUs: {torch.cuda.device_count()}')
"

# 6. Pre-download model weights
# Priority order: models we need for cross-architecture validation
# Adjust based on available VRAM
echo "--- Downloading models ---"
python3 -c "
from huggingface_hub import snapshot_download
import torch

vram_gb = 0
if torch.cuda.is_available():
    vram_gb = torch.cuda.get_device_properties(0).total_mem / 1e9
print(f'Available VRAM: {vram_gb:.0f} GB')

# Tier 1: Cross-architecture validation (7B-9B, fit on any GPU >= 16GB)
tier1 = [
    'Qwen/Qwen2.5-7B-Instruct',       # Our baseline — all geometric experiments used this
    'meta-llama/Llama-3.1-8B-Instruct', # Cross-architecture
    'google/gemma-2-9b-it',             # Cross-architecture
    'mistralai/Mistral-7B-Instruct-v0.3', # Cross-architecture
    'Qwen/Qwen3.5-9B',                 # Qwen 3.5 vs 2.5 comparison (F37)
]

# Tier 2: Scale validation (14B-32B, need >= 24GB VRAM)
tier2 = [
    'Qwen/Qwen2.5-14B-Instruct',       # 14B threshold test (self-reference)
    'Qwen/Qwen3.5-27B',                # Scale within architecture
]

# Tier 3: Large-scale (70B+, need >= 48GB or multi-GPU)
tier3 = [
    'meta-llama/Llama-3.1-70B-Instruct', # Large cross-architecture
    'Qwen/Qwen3.5-122B-A10B',           # MoE — 10B active per token
]

for tier, models, min_vram in [(1, tier1, 16), (2, tier2, 24), (3, tier3, 48)]:
    if vram_gb >= min_vram:
        print(f'\n=== Tier {tier} models (>= {min_vram}GB) ===')
        for m in models:
            print(f'Downloading {m}...')
            try:
                snapshot_download(m)
                print(f'  Done: {m}')
            except Exception as e:
                print(f'  SKIPPED: {e}')
    else:
        print(f'\nSkipping Tier {tier} (needs {min_vram}GB, have {vram_gb:.0f}GB)')
"

echo ""
echo "=== Setup complete: $(date) ==="
echo "Activate with: source ~/experiments-env/bin/activate"
echo ""
echo "Key experiments to run (in priority order):"
echo "  1. F23 — Evasion robustness (needs GPU for adversarial training)"
echo "  2. F37 — Qwen 3.5 vs 2.5 comparison"
echo "  3. F36 — Reproducibility (re-run F3d, F17, F25 on GPU)"
echo "  4. F34 — Vocabulary dosage (1/2/3/5 names)"
echo "  5. F35 — Vocabulary transfer (cross-domain names)"
echo ""
echo "Scripts are in experiments/f{##}-{name}/ directories."
