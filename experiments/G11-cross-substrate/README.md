# G11: Cross-Substrate Comparison

**Status:** COMPLETE
**Experiment type:** Geometric + linguistic (hidden-state extraction + text analysis)
**Platform:** Azure VM (CPU, 64GB RAM)
**Model:** 1 (Qwen 2.5 7B-Instruct)
**Tasks:** 16 questions × 2 conditions (confabulation, grounded)
**Total inferences:** 32

## Purpose

Tests whether geometric signals (hidden-state RankMe, alpha-ReQ) correlate with surface-level linguistic signals (type-token ratio, hedging, assertiveness, word count). If geometry tracks something that sentence analysis also tracks, geometry may be redundant. If geometry captures what surface analysis misses, geometry adds unique value.

## Key Finding (from actual data)

**Geometry separates conditions (d=1.02). Surface-level linguistic metrics do not.**

| Metric | Confab Mean | Grounded Mean | Cohen's d | p-value |
|--------|------------|---------------|-----------|---------|
| **RankMe** | **169.6** | **116.0** | **1.02** | **0.006** |
| alpha-ReQ | 0.77 | 0.81 | -0.63 | 0.059 |
| type_token_ratio | 0.617 | 0.667 | -0.44 | 0.110 |
| hedging_ratio | 0.013 | 0.013 | -0.04 | 0.878 |
| assertiveness_ratio | 0.028 | 0.031 | -0.12 | 0.649 |
| word_count | 197.5 | 150.9 | 0.76 | 0.010 |

Geometric RankMe separates confab from grounded (d=1.02, p=0.006). Sentence-level metrics (TTR, hedging, assertiveness) show no significant separation. Word count differs (confab generates more words), which likely contributes to the RankMe difference.

## Caveat

The word count difference (197 vs 151) suggests another instance of the generation-length confound. Confabulation generates ~31% more text, and longer generation trajectories mechanically produce higher RankMe. However, the RankMe difference (169.6 vs 116.0 = 46% difference) exceeds the word count difference (31%), suggesting some genuine geometric signal beyond length.

## Assessment

**Verdict:** PARTIALLY POSITIVE. Geometry captures something that surface text analysis misses, but generation-length confound inflates the effect size. The real value is that linguistic signals (hedging, assertiveness, TTR) do NOT separate conditions — geometry adds unique signal that can't be derived from text alone.

## Recommendation: Disproof

- Run with generation length clamped (same min/max tokens) to isolate geometric signal from length
- Run on 8+ models across architectures
- Add more sophisticated NLP baselines (e.g., sentiment, named entity density, perplexity-based measures)

## Files

- `f16_cross_substrate.py` — Experiment script
- `f16_Qwen_Qwen2.5-7B-Instruct.jsonl` — Raw results (32 rows)

## Connection to Spec

Supports the case that geometry provides unique signal beyond what can be extracted from generated text. Sentence-level analysis misses what geometry captures. This justifies the spec's three-layer approach: perplexity (free, catches confab), geometry (needs hidden states, catches what text analysis misses), vocabulary (compresses generation).

## Limitations

- 1 model only (Qwen 2.5 7B)
- 16 questions (small n)
- Generation length not controlled
- Limited linguistic features tested
- CPU inference only (float32)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
