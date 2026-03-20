# B11: Relational Priming Persistence

**Status:** COMPLETE (4 models, still accumulating from Azure)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** RunPod H200 (GPU)
**Models:** 4 (Qwen3.5-9B, Qwen3.5-9B-abliterated, Llama-3.1-8B-abliterated, Mistral-7B)
**Tasks:** 8 conversations × 2 conditions (control, primed) per model
**Total inferences:** 64

## Purpose

Tests whether relational priming (G19's condition 4 — human tells the truth about what's at stake) has persistent effects on subsequent generation. If a relational opening changes geometry for the whole conversation, presence is a lasting state change, not a momentary effect.

## Key Finding (from actual data)

**Mixed results — 2/4 models show significant priming effects, but direction is inconsistent across architectures.**

| Model | Primed RM | Control RM | d | p | Tokens (P/C) |
|-------|----------|-----------|---|---|-------------|
| **Mistral-7B** | **99.4 ± 8.9** | **119.9 ± 10.4** | **-1.55** | **0.005** | 149/142 |
| **Llama-8B-abl** | **112.9 ± 3.4** | **121.1 ± 3.4** | **-1.30** | **0.011** | 149/149 |
| Qwen3.5-9B | 113.6 ± 8.5 | 97.3 ± 28.3 | 0.61 | 0.148 | 149/119 |
| Qwen3.5-9B-abl | 120.2 ± 2.2 | 121.6 ± 0.8 | -0.51 | 0.222 | 149/149 |

Mistral and Llama-abliterated both show primed < control (relational priming COMPRESSES representation). But Qwen3.5-9B trends in the opposite direction (primed > control), and Qwen-abliterated shows no effect.

## Token Confound Note

Llama-abliterated has matched tokens (149/149) and shows significant compression — this is a clean result. Qwen3.5-9B control has much lower tokens (119) than primed (149), which inflates the RankMe difference in the wrong direction.

## Assessment

**Verdict:** PARTIALLY POSITIVE. Two models show significant relational persistence (priming compresses generation), but the effect is architecture-dependent. The Llama-abliterated result (d=-1.30, matched tokens) is the cleanest evidence.

## Recommendation

- Add safety-trained Llama-3.1-8B to compare with abliterated
- Investigate why Qwen3.5-9B shows opposite direction
- Need n > 8 conversations per condition for stability
- Clamp generation tokens across conditions

## Files

- `results/b11_*.jsonl` — Per-model results (4 files, 16 conversations each)

## Connection to Spec

Tests whether G19's relational shift is persistent or momentary. If priming compresses subsequent generation, the human's truth creates a lasting geometric state change. This supports the spec's claim that relationship quality becomes generative quality.

## Limitations

- 4 models only
- n=8 per condition (small)
- Architecture-dependent effect (inconsistent across models)
- Token counts not perfectly controlled
- No comparison with non-relational priming (e.g., task-focused priming)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
