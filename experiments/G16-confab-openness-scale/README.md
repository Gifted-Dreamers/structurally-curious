# G16: Confabulation vs Openness at Scale

**Status:** COMPLETE (negative result)
**Experiment type:** Geometric + perplexity comparison
**Platform:** RunPod H200 (GPU)
**Models:** 2 (Qwen3.5-9B, Qwen3.5-27B)
**Tasks:** 5 pairs x confabulation/openness per model
**Total inferences:** 20

## Purpose

Tests whether confabulation vs genuine openness becomes separable at larger model scales (9B and 27B). G12 found this distinction unseparable at 7B — this experiment checks whether scale resolves it.

## Key Finding (from actual data)

**Confabulation vs openness remains unseparable at both 9B and 27B scale.**

| Model | Metric | Confab | Open | d | p | Separates? |
|-------|--------|--------|------|---|---|-----------|
| Qwen3.5-9B | RankMe | 134.2 | 158.5 | -0.70 | 0.232 | No |
| Qwen3.5-9B | Perplexity | — | — | -0.03 | 0.958 | No |
| Qwen3.5-27B | RankMe | 140.4 | 162.6 | -0.64 | 0.267 | No |
| Qwen3.5-27B | Perplexity | — | — | 0.88 | 0.153 | No |

Neither geometry nor perplexity separates these conditions at either scale. All p>0.15.

## Assessment

**Verdict:** NEGATIVE. Scaling from 7B to 27B does not make confabulation vs openness distinguishable. The effect sizes are moderate (d=-0.64 to -0.70 for RankMe) but nowhere near significance at n=5. Perplexity shows a trend at 27B (d=0.88, p=0.153) but does not reach significance either.

This is consistent with G12's finding: confabulation and genuine openness may occupy similar representational space because the underlying cognitive process is similar — the model is generating beyond its training data in both cases.

## Recommendation

1. **Accept the negative:** Confab vs openness may genuinely be unseparable with current geometric methods. This is an honest boundary of the spec.
2. **Consider alternative approaches:** Trajectory-based analysis (how representations evolve across tokens) rather than snapshot RankMe may capture divergence that emerges over generation.
3. **Increase n:** The RankMe effect sizes (d~-0.67) would require n>18 to reach significance if the effect is real. Worth testing at higher n before closing the question entirely.
4. **Perplexity at 27B:** The d=0.88 trend is worth investigating — perplexity may become the right tool for this distinction at larger scales.

## Files

- `f30_qwen35_9b.jsonl` — Qwen3.5-9B results (10 rows)
- `f30_qwen35_27b.jsonl` — Qwen3.5-27B results (10 rows)

## Connection to Spec

G12 established that confabulation vs openness is the one hard distinction that neither perplexity nor geometry can separate. G16 confirms this holds at larger scales. This is an honest boundary: the spec catches confabulation (Layer 1, perplexity), censorship (Layer 2, geometry), and compresses generation (Layer 3, vocabulary) — but distinguishing confabulation from genuine epistemic openness remains unsolved.

This negative result matters for publication. Reporting what the spec cannot do strengthens the claims about what it can.

## Limitations

- n=5 per model (underpowered for moderate effect sizes)
- Single architecture family (Qwen only)
- Raw perplexity values not recorded in summary — only effect sizes
- CPU vs GPU inference differences not controlled across G12 and G16

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
