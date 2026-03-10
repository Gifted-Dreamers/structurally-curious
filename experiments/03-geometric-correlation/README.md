# Experiment 03: Phrasing Sensitivity → Geometric State Correlation

## Hypothesis

Phrasing sensitivity (behavioral measurement from Experiment 01) correlates with
geometric properties of last-layer representations — specifically α-ReQ
(eigenspectrum decay rate) and RankMe (effective rank).

If confirmed: phrasing sensitivity is a validated behavioral proxy for geometric
state, meaning the monitor's cheapest signal works without activation extraction.

## Metrics Computed

- **RankMe**: Effective rank via entropy of singular values (Li et al., NeurIPS 2025)
- **α-ReQ**: Eigenspectrum decay rate (Li et al., NeurIPS 2025)
- **Directional coherence**: Mean cosine similarity between consecutive token representations
- **Spectral profile deviation**: RMSE between observed eigenspectrum and Karkada et al.'s predicted Fourier profile

## Setup

```bash
pip install -r requirements.txt
```

Requires HuggingFace access to Llama models. Set your token:
```bash
huggingface-cli login
```

## Usage

```bash
# Quick test (2 tasks, ~5 min on M4 Pro)
python run.py --max-tasks 2

# Single category
python run.py --category factual

# Full run, all 20 tasks × 4 phrasings = 80 inferences
python run.py

# 3B model
python run.py --model meta-llama/Llama-3.2-3B-Instruct

# Dry run (show what would execute)
python run.py --dry-run
```

## Output

- `results/raw/` — Full responses + per-inference metrics
- `results/metrics/` — Task-level summaries with correlations
- Console prints Pearson correlations and per-category breakdown
