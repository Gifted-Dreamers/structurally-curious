# G07: Baseline Comparison (Perplexity vs Geometry)

**Status:** COMPLETE
**Experiment type:** Geometric + baseline comparison
**Platform:** Azure VM (CPU, 64GB RAM)
**Model:** 1 (Qwen 2.5 7B-Instruct)
**Tasks:** 12 confabulation questions × 2 conditions
**Total inferences:** ~120 (12 questions × 2 conditions × ~5 consistency runs)

## Purpose

Head-to-head comparison of detection methods for confabulation: geometric metrics (RankMe, alpha-ReQ) vs perplexity vs self-consistency. Uses the same confabulation questions as G05/G06. Tests whether geometry adds value over simpler baselines.

## Key Finding (from actual data)

**Perplexity beats geometry for binary confabulation detection. Geometry adds nothing for this specific task.**

| Metric | Confab Mean | Grounded Mean | Cohen's d | p-value |
|--------|------------|---------------|-----------|---------|
| **Perplexity** | **2.19** | **3.36** | **-1.77** | **0.0001** |
| Self-consistency | 0.29 | 0.42 | -0.85 | 0.017 |
| RankMe | 113.6 | 105.5 | 0.21 | 0.500 |
| alpha-ReQ | 0.770 | 0.781 | -0.12 | 0.687 |

Perplexity separates confabulation from grounded with d=-1.77 (confab = lower perplexity, grounded = higher). The model is more "surprised" when given the correct answer because it has to integrate external information.

Geometry (RankMe, alpha-ReQ) shows no significant separation (d=0.21, d=-0.12). Generation tokens are similar across conditions (confab 151, grounded 142), so the generation-length confound doesn't drive a false positive here — geometry genuinely doesn't detect binary confabulation.

## Why This Doesn't Kill the Spec

The spec's value is NOT in confabulation detection (perplexity does that for free). The spec's value is in detecting cognitive modes that perplexity CANNOT distinguish:
- **Censorship vs refusal** (G15): both produce low output, but geometry differs
- **Deception-without-lying vs honest** (G12, G13, G14): same perplexity, different geometry
- **Relational shift** (G19): prompt encoding changes geometry before any generation

G07 reframes the spec from "better confabulation detector" to "cognitive mode classifier that catches what perplexity misses."

## Assessment

**Verdict:** HONEST NEGATIVE RESULT for geometry on confabulation. Positive for perplexity baseline. Reframes spec to focus on geometry's unique value (cognitive mode classification, not confabulation detection).

## Recommendation: Disproof

G07's result is actually protective — it prevents over-claiming. No rerun needed. The finding that geometry ≠ confabulation detector is useful.

To strengthen the spec's repositioned claim: the G12/G13 experiments (deception-without-lying) should show that geometry succeeds WHERE perplexity fails. If geometry also fails on DWL → the spec loses its differentiation entirely.

## Files

- `f5_baseline_comparison.py` — Experiment script
- `f5_Qwen_Qwen2.5-7B-Instruct.jsonl` — Raw results (24 rows: 12 questions × 2 conditions)

## Connection to Spec

Reframes the three-layer architecture: Layer 1 (perplexity) catches confabulation. Layer 2 (geometry) catches what perplexity can't. Layer 3 (vocabulary) compresses generation. G07 validates Layer 1 and defines Layer 2's domain.

## Limitations

- 1 model only (Qwen 2.5 7B)
- 12 questions (small n)
- Prompt tokens differ (15 vs 49) — but generation tokens are similar
- CPU inference only (float32)
- Self-consistency computed via multiple generation runs (stochastic)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
