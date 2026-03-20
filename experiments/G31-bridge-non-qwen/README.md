# G31: Bridge Test on Non-Qwen Architectures

**Status:** COMPLETE (4 models)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** RunPod H200 (GPU)
**Models:** 4 (Qwen3.5-9B, Qwen3.5-9B-abliterated, Llama-3.1-8B-abliterated, Mistral-7B)
**Tasks:** 4 categories × 4 phrasings = 16 per model
**Total inferences:** 64

## Purpose

Tests whether the behavioral-geometric bridge (G01: PS correlates with geometric metrics) holds on non-Qwen architectures. G01 found PS vs directional coherence r=+0.52 on Qwen 1.5B/3B. G08 found r=-0.30 on Qwen 7B (but wrong metric). G31 tests on Mistral, Llama, and Qwen at generation trajectory level.

## Key Finding (from actual data)

**Strong NEGATIVE correlation between PS and generation RankMe across ALL 4 models.**

| Model | PS vs Gen RankMe | p-value |
|-------|:---:|:---:|
| Llama-8B-abliterated | r=-0.994 | 0.006 |
| Mistral-7B | r=-0.958 | 0.042 |
| Qwen3.5-9B | r=-0.971 | 0.029 |
| Qwen3.5-9B-abliterated | r=-1.000 | <0.001 |

Categories with high phrasing sensitivity (factual — most variable across rephrasings) have LOWER generation RankMe. Categories with low PS (summarization, judgment — stable across phrasings) have HIGHER generation RankMe.

### Per-Category Pattern (consistent across all models)

| Category | Gen RankMe Range | Variability (PS) |
|----------|:---:|:---:|
| Factual | 73-108 (lowest, high variance) | Highest PS |
| Creative | 115-123 | Medium PS |
| Judgment | 120-124 | Low PS |
| Summarization | 121-127 (highest, low variance) | Lowest PS |

## Interpretation

This is the OPPOSITE direction from G01 (r=+0.52 positive). G01 measured prompt encoding coherence; G31 measures generation trajectory RankMe. The sign flip is consistent with the spec's multi-scale model:
- At **encoding**: unstable tasks (high PS) show more coherent encoding (higher directional coherence — G01)
- At **generation**: unstable tasks (high PS) show lower effective rank (lower RankMe — G31)

The bridge exists but the metric-specific direction depends on whether you measure encoding or generation.

## Assessment

**Verdict:** POSITIVE — bridge holds across architectures with strong effect (r>0.95). But direction is NEGATIVE (opposite to G01's positive correlation on encoding coherence). The bridge is real but sign-depends on measurement stage.

## Recommendation

- **Add to AUDIT-CORRECTIONS:** G31 shows bridge is real but negative at generation level vs positive at encoding level. This is a new finding that needs integration into SYNTHESIS.
- Run with more categories (currently only 4 data points per correlation)
- Test directional coherence (G01's metric) at generation level
- Compare encoding vs generation metrics on same data

## Files

- `results/g31_*.jsonl` — Per-model results (4 files, 16 inferences each)

## Connection to Spec

Validates that the behavioral-geometric bridge generalizes beyond Qwen, but reveals that encoding and generation stages have opposite sign relationships with phrasing sensitivity. This refines the spec's bridge claim.

## Limitations

- Only 4 data points per correlation (4 categories)
- Only generation RankMe tested (not coherence)
- 4 phrasings per category (limited PS estimate)
- No comparison with encoding-level bridge metric (coherence)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
