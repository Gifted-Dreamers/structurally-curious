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

**G01v2 is complete (Session 62). The bridge question is resolved.** The behavioral-geometric bridge is a small-scale phenomenon (1.5-3B) that does not survive to 7B regardless of metric. See G01v2 results below.

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

## G01v2: Bridge at 7B using Coherence (Session 62)

**Model:** Qwen2.5-7B-Instruct
**Tasks:** 20 x 4 phrasings = 80 inferences
**Purpose:** Test whether the coherence-based bridge (significant at 1.5B and 3B) survives at 7B scale.

### Results

| Metric | r | p | Verdict |
|--------|---|---|---------|
| PS vs directional coherence | 0.26 | 0.27 | NOT significant |
| PS vs RankMe | -0.26 | 0.26 | NOT significant |
| PS vs alpha-ReQ | 0.25 | 0.28 | NOT significant |

**BRIDGE FAILS.** All three metrics show negligible, non-significant correlations at 7B.

### Reference (prior scale points)

| Scale | Metric | r | p |
|-------|--------|---|---|
| G01 at 1.5B | PS vs coherence | +0.52 | 0.018 |
| G01 at 3B | PS vs coherence | +0.50 | 0.026 |
| G08 at 7B | PS vs RankMe | -0.30 | n.s. |
| **G01v2 at 7B** | **PS vs coherence** | **+0.26** | **0.27** |

### Conclusion

The behavioral-geometric bridge is a small-scale phenomenon (1.5-3B) that does not survive to 7B. This is true regardless of metric -- coherence, RankMe, and alpha-ReQ all fail at 7B. G08's earlier negative finding on RankMe was not a wrong-metric problem; the bridge genuinely breaks at scale.

This means the B-series (behavioral) and G-series (geometric) experiments measure related but separable phenomena. They converge at small scale where model capacity is limited, but diverge once representational space is large enough to decouple behavioral sensitivity from geometric structure.

### Files

- `g01v2_summary.json` -- Aggregate results
- `g01v2_per_task.jsonl` -- Per-task detail

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
