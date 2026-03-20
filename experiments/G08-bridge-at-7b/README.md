# G08: Bridge at 7B Scale
<img src="../../images/experiments/g08-bridge-at-7b.png" alt="Bridge crumbles at 7B scale" width="400">

**Status:** COMPLETE (negative result) — but tested wrong metric. NEEDS RETEST.
**Experiment type:** Geometric (hidden-state extraction + behavioral correlation)
**Platform:** Azure VM (CPU, 64GB RAM)
**Model:** 1 (Qwen 2.5 7B-Instruct)
**Tasks:** 20 tasks × 4 phrasings
**Total inferences:** 80

## Purpose

Tests whether the behavioral-geometric bridge (PS vs geometric metrics) discovered in G01 at 1.5B and 3B holds at 7B scale. If the bridge breaks at scale, behavioral experiments (B-series) cannot predict geometric states for larger models.

## Key Finding (from SYNTHESIS — no result files in folder)

**Bridge breaks at 7B: r=-0.30 (PS vs RankMe).**

However, per the G01 audit correction: the actual bridge metric is directional COHERENCE (r=+0.52 at 1.5B), not RankMe (r=+0.27, n.s. at 1.5B). G08 tested RankMe at 7B and found it negative — but RankMe wasn't the bridge metric at any scale.

**The coherence bridge was never tested at 7B.**

## Data Status

**No result files in this folder.** Only the experiment script (`f1_partial_bridge.py`). The r=-0.30 finding is reported in SYNTHESIS but the raw data is not preserved locally. May still exist on the Azure VM at `~/experiments/`.

## Assessment

**Verdict:** NEEDS RETEST (G01v2). The negative result is for the wrong metric. Cannot claim the bridge breaks at 7B until PS vs directional coherence is tested at 7B across architectures.

## Recommendation: G01v2 (HIGH PRIORITY)

- Run PS vs directional coherence on 8 models at 7B+ scale
- If coherence bridge holds at 7B → G08's negative is metric-specific, not scale-specific
- If coherence bridge also breaks → bridge genuinely fails at scale, and behavioral experiments lose their predictive connection to geometry

## Files

- `f1_partial_bridge.py` — Experiment script (tests PS vs RankMe, alpha-ReQ, coherence)

## Connection to Spec

The bridge connects B-series (behavioral, API-only) to G-series (geometric, hidden-state). If the bridge breaks, behavioral experiments become indirect evidence only. G01v2 is needed to determine whether the bridge holds on the correct metric (coherence) at production scale.

## Limitations

- Result data not preserved in repo
- 1 model only (Qwen 2.5 7B)
- Tested RankMe as bridge metric, but G01 showed bridge is with coherence
- CPU inference only

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
