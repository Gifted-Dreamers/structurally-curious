# G02: Eigenspectral Profiles

**Status:** DESIGNED, NOT RUN
**Experiment type:** Geometric (hidden-state extraction)
**Script:** `run.py` (ready), `tasks.json` (ready)

## Purpose

Test whether confabulation and grounded responses have distinguishable eigenspectral profiles — the shape of the singular value distribution, not just summary statistics (RankMe, alpha-ReQ). Uses Karkada et al.'s spectral profile deviation approach (arXiv 2602.15029).

## Recommendation

**Deprioritized.** G07 showed perplexity beats geometry for binary confabulation detection (d=-1.77 vs d=0.21). The spec's value is in cognitive mode classification (G12, G13, G19), not confabulation detection. G02's spectral profile approach might recover the confabulation signal, but the practical need is low given perplexity's performance.

If revisited, run on H200 GPU with 8 models. Estimated time: ~2 hours.

## Files

- `run.py` — Experiment script (ready to run)
- `tasks.json` — Task definitions

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
