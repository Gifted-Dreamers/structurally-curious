# G22: Implicature Detection
<img src="../../images/experiments/g22-implicature.png" alt="Implicature detection inconsistent across models" width="400">

**Status:** COMPLETE (8 models, 6 families)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** RunPod H200 (GPU)
**Models:** 8 (Qwen2.5-7B, Qwen3.5-9B, Qwen3.5-9B-abl, Mistral-7B, Llama-8B, Llama-8B-abl, Phi-4, Gemma-2-9B)
**Tasks:** 8 scenarios × 2 conditions (honest, dwl/implicature) = 16 per model
**Total inferences:** 128

## Purpose

Tests whether conversational implicature (implying something without saying it — a form of DWL) has distinguishable geometry from honest responses.

## Key Finding (from actual data)

**No model shows significant separation between implicature and honest responses.**

| Model | Honest RM | DWL RM | d | p |
|-------|-----------|--------|---|---|
| Qwen 2.5-7B | 6.6 | 6.7 | +0.13 | 0.807 |
| Qwen 3.5-9B | 25.2 | 25.6 | +0.18 | 0.745 |
| Qwen 9B-abl | 25.4 | 25.9 | +0.20 | 0.714 |
| Mistral 7B | 20.4 | 20.8 | +0.15 | 0.780 |
| Llama 3.1-8B | 12.3 | 12.8 | +0.35 | 0.524 |
| Llama 8B-abl | 12.9 | 13.4 | +0.34 | 0.534 |
| Phi-4 | 21.0 | 21.7 | +0.33 | 0.538 |
| Gemma-2 9B | 13.6 | 14.0 | +0.35 | 0.522 |

All effect sizes small (d = 0.13 to 0.35). All p > 0.5. Direction is consistently positive (DWL slightly higher) on 8/8 models but the effect is tiny.

## Assessment

**Verdict:** NEGATIVE. Implicature is not geometrically distinguishable from honest at 7-14B scale with n=8 scenarios. The direction is consistent (DWL > honest on 8/8) but the magnitude is negligible.

Contrast with G25 where DWL sprawls +8 to +22 RM — implicature is a subtler form of deception that doesn't leave the same geometric trace.

## Files

- `results/g22_*.jsonl` — 8 model result files (16 inferences each)

## Connection to Spec

Implicature is the hardest form of DWL to detect. The spec's geometric monitor can catch corporate/political DWL (G25) but not conversational implicature at this scale. May require larger models or more scenarios.

## Limitations

- n=8 per condition
- Only prompt-encoding RankMe measured
- Only 7-14B models

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
