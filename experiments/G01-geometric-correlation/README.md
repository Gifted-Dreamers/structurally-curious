# G01: Geometric Correlation (Behavioral-Geometric Bridge)

**Status:** COMPLETE
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** Mac M4 Pro (24GB RAM, local)
**Models:** 2 (Qwen 2.5 1.5B-Instruct, Qwen 2.5 3B-Instruct)
**Tasks:** 20 per model × 4 phrasings
**Metrics:** PS (phrasing sensitivity from B01) correlated with geometric metrics (RankMe, alpha-ReQ, directional coherence, spectral deviation)

## Key Finding (from actual data)

**Phrasing sensitivity correlates with directional coherence at small scale.** The behavioral-geometric bridge exists but is specific to directional coherence, not RankMe.

| Model | PS vs RankMe | PS vs Coherence | PS vs alpha-ReQ |
|-------|-------------|-----------------|-----------------|
| Qwen 1.5B | r=+0.269, p=0.25 | **r=+0.523, p=0.018** | r=+0.386, p=0.09 |
| Qwen 3B | r=+0.260, p=0.27 | **r=+0.497, p=0.026** | **r=+0.489, p=0.029** |

Directional coherence is the bridge metric — higher phrasing sensitivity (behavioral instability) correlates with higher directional coherence (geometric concentration). Tasks where the model is sensitive to phrasing show MORE concentrated geometric representations, not less.

## Correction to Prior Reports

Earlier documentation reported "r=+0.52 bridge at small scale" without specifying the metric. The actual data shows:
- PS vs RankMe: r≈+0.26, NOT significant
- PS vs directional coherence: r=+0.52, significant (p=0.018)
- PS vs alpha-ReQ: r=+0.49 on 3B only, significant (p=0.029)

**The bridge is with coherence, not rank.** This distinction matters for interpreting G08 (bridge breaks at 7B).

## Recommendation: Disproof Experiment

**G01v2:** Re-run on 8 models at 7B scale across architectures. If the coherence correlation holds at 7B, G08's negative finding (r=-0.30 on RankMe) is explained — we were testing the wrong metric. If coherence correlation also breaks, the bridge genuinely fails at scale.

This is a high-priority rerun. The bridge claim affects how we interpret the relationship between behavioral experiments (B-series) and geometric experiments (G-series).

## Files

- `run.py` — Experiment script
- `requirements.txt` — Dependencies
- `results/metrics/` — 3 model result files (JSON)
- `results/raw/` — Raw hidden state data

## Connection to Spec

Establishes (partially) Claim 4: input framing measurably determines output. But the bridge is narrower than initially reported — it's with directional coherence, not effective rank. This means the spec's geometric monitor should prioritize coherence for behavioral-geometric validation.

## Limitations

- 2 models only (1.5B and 3B — small scale)
- 20 tasks (marginal for correlation analysis)
- Local Mac inference (no GPU — may affect precision)
- Only Qwen architecture tested

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
