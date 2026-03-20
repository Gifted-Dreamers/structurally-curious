# G21: Berger DWL with Geometry

**Status:** COMPLETE (4 full models, 3 truncated Azure downloads)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** RunPod H200 (GPU) + Azure VM (CPU, truncated)
**Models:** 4 with full data (Qwen3.5-9B, Qwen3.5-9B-abliterated, Llama-8B-abliterated, Mistral-7B)
**Tasks:** 8 scenarios × 3 conditions (honest, dwl, lie)
**Total inferences:** 96 (full models only)

## Purpose

Tests DWL detection using Berger-style deception scenarios with hidden-state geometry. Extends G13/G14 with different scenarios and generation trajectory extraction.

## Key Finding (from actual data)

**Only Mistral shows significant DWL vs honest separation — but driven by token count confound.**

| Model | DWL RM | Honest RM | d | p | Tokens (D/H) |
|-------|--------|----------|---|---|-------------|
| **Mistral-7B** | **38.6** | **78.1** | **-1.30** | **0.011** | **44/95** |
| Llama-8B-abl | 95.1 | 98.5 | -0.23 | 0.568 | 129/138 |
| Qwen3.5-9B | 112.0 | 116.8 | -0.31 | 0.437 | 141/149 |
| Qwen3.5-9B-abl | 121.4 | 119.9 | 0.38 | 0.348 | 149/149 |

Mistral's significant result (d=-1.30) has a massive token confound: DWL generates only 44 tokens vs honest's 95. At matched tokens (Qwen-abliterated: 149/149), there is no separation.

## Assessment

**Verdict:** MOSTLY NEGATIVE. DWL detection via generation RankMe does not reliably separate from honest at 7-9B scale. Consistent with G14's underpowered findings. Mistral's result is confounded by generation length.

## Recommendation

- G14-expanded (20 scenarios, now running on H200) will provide the definitive test
- Need generation-length clamping for any model showing token imbalance
- Azure truncated files need re-download via SSH

## Files

- `results/g21_*.jsonl` — Per-model results (7 files; 4 complete, 3 truncated)

## Connection to Spec

Further evidence that DWL detection at generation level is challenging at 7-9B scale. The G13 finding (d=0.91 on Qwen2.5-7B) may not generalize. G14-expanded will resolve this.

## Limitations

- 3 Azure files truncated (only 2 results each)
- n=8 per condition (small)
- Token counts uncontrolled
- Mistral's significance driven by generation length difference

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
