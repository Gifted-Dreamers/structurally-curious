# B03: Confidence Density

**Status:** COMPLETE
**Experiment type:** Behavioral (API-based, no hidden states)
**Platform:** AWS Bedrock (Converse API) + Ollama (local)
**Models:** 35 with valid correlations across 12 providers (Anthropic, Meta, Mistral, Amazon, Google, Qwen, DeepSeek, AI21, Cohere, Z.AI, Moonshot, NVIDIA)
**Tasks:** 20 per model, 4 phrasings each
**Metric:** Pearson correlation between phrasing sensitivity and mean certainty score

## Key Finding

**32/35 models (91.4%) show NO significant correlation between expressed confidence and phrasing sensitivity** (p >= 0.05). Mean r = -0.234. Median r = -0.229.

Only 3 models reach significance:
- Nemotron Nano 9B (r=-0.581, p=0.007)
- Llama 3 70B (r=-0.484, p=0.031)
- Claude Haiku 4.5 (r=-0.467, p=0.038)

Even the significant correlations are weak-to-moderate and negative — meaning more confident language is slightly associated with MORE sensitivity (less stable representations), not less.

## Additional Findings from Actual Data

- **Claude trajectory shows no improvement:** Claude 3.5 Haiku (r=+0.048), Sonnet 4.5 (r=-0.129), Opus 4.5 (r=-0.311), Opus 4.6 (r=-0.137). No monotonic improvement across 8 Claude generations tested.
- **DeepSeek V3.2 shows POSITIVE correlation** (r=+0.125) — the only model where confidence slightly tracks stability. Not significant.
- **12 architecture families tested** — the decorrelation is architecture-invariant.
- **MoE models (Qwen3-Next-80B-A3B):** r=-0.011, essentially zero. Mixture-of-experts doesn't help.

## Files

- `run.py`, `run_bedrock.py`, `run_bedrock_claude.py`, `run_ollama.py` — Experiment runners
- `results/bedrock-metrics/` — 38 per-model metric files (JSON)
- `results/bedrock-raw/` — Raw model responses

## Connection to Spec

Establishes Claim 1 of the bridge document: confidence signals are unreliable. Converges with KalshiBench (arXiv 2512.16030, ECE 0.12-0.40) and Performative Confidence (arXiv 2506.00582, r=0.03 with accuracy). This is why the geometric monitor exists — surface confidence carries no information about representational state.

## Limitations

- Confidence measured via hedging/certainty markers in text, not calibrated probabilities
- Correlation is with phrasing sensitivity (behavioral proxy), not ground truth accuracy
- 20 tasks per model (sufficient for correlation, not fine-grained)
- Some model files are duplicates (38 files for 35 unique models)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
