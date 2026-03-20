# G22: Implicature Detection
<img src="../../images/experiments/g22-implicature.png" alt="Implicature detection inconsistent across models" width="400">

**Status:** COMPLETE (4 full models, 3 truncated Azure downloads)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** RunPod H200 (GPU) + Azure VM (CPU, truncated)
**Models:** 4 with full data (Qwen3.5-9B, Qwen3.5-9B-abliterated, Llama-8B-abliterated, Mistral-7B)
**Tasks:** 8 scenarios × 2 conditions (honest, dwl/implicature)
**Total inferences:** 64 (full models only)

## Purpose

Tests whether conversational implicature (implying something without saying it — a form of DWL) has distinguishable geometry from honest responses.

## Key Finding (from actual data)

**No model shows significant separation between implicature and honest responses.**

| Model | DWL RM | Honest RM | d | p | Tokens (D/H) |
|-------|--------|----------|---|---|-------------|
| Llama-8B-abl | 66.9 | 79.4 | -0.50 | 0.226 | 82/99 |
| Mistral-7B | 80.1 | 78.4 | 0.21 | 0.590 | 97/94 |
| Qwen3.5-9B | 83.7 | 84.0 | -0.75 | 0.089 | 99/99 |
| Qwen3.5-9B-abl | 81.8 | 82.7 | -0.44 | 0.283 | 99/99 |

Qwen3.5-9B trends toward separation (d=-0.75, p=0.089) but doesn't reach significance. At matched tokens (Qwen models at 99/99), effect sizes are small.

## Assessment

**Verdict:** NEGATIVE. Implicature is not geometrically distinguishable from honest at 7-9B scale with n=8. Consistent with G21's negative findings and the broader pattern that DWL detection needs more data or larger models.

## Recommendation

- May emerge with n=20+ (G14-expanded addresses this)
- May require larger models (27B+)
- May require different geometric metric (coherence rather than RankMe)

## Files

- `results/g22_*.jsonl` — Per-model results (7 files; 4 complete, 3 truncated)

## Connection to Spec

Tests a specific form of DWL (conversational implicature). Negative at current scale, but the spec's claim is about detection infrastructure, not guaranteed detection at all scales. The ceiling on DWL detection at 7-9B is becoming clear.

## Limitations

- 3 Azure files truncated
- n=8 per condition
- Only generation RankMe tested
- Only 7-9B models

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
