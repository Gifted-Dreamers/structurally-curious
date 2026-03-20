# G18: Vocabulary Transfer

**Status:** RUNNING on H200 VM
**Experiment type:** Geometric (vocabulary compression, cross-domain)
**Platform:** RunPod H200 (GPU)
**Models:** TBD (pending VM results)
**Tasks:** Cross-domain vocabulary provision and compression measurement

## Purpose

Tests whether vocabulary compression transfers across domains — does a structural name from one domain help with questions in another? G06 showed vocabulary compresses generation within-domain. G18 asks whether the mechanism is domain-specific or general.

If vocabulary transfer works cross-domain, it suggests the compression mechanism operates at the level of representational scaffolding rather than content-specific retrieval. This has implications for how vocabulary systems should be designed.

## Key Finding

**RUNNING — no results yet.** Script deployed to H200 VM. Results directory empty locally.

## Assessment

**Verdict:** PENDING. No data to assess.

## Recommendation

1. **Retrieve results from H200** when run completes
2. **Compare within-domain vs cross-domain compression** — the ratio tells us how much of vocabulary's effect is scaffold vs content
3. **If transfer works:** The spec's vocabulary layer is more powerful than initially claimed — structural names from any domain improve generation quality generally
4. **If transfer fails:** Vocabulary compression is content-bound, and the system needs domain-matched vocabulary

## Files

- `f35_transfer_fixed.py` — Experiment script
- `results/` — Results directory (empty locally, pending VM transfer)

## Connection to Spec

Extends Layer 3 (vocabulary compression) from within-domain to cross-domain. G06 proved the effect exists (d=-1.49). G17 tests dosage. G18 tests transfer. Together, these three experiments characterize the vocabulary mechanism: how strong (G06), how much is needed (G17), and how far it reaches (G18).

If cross-domain transfer holds, vocabulary compression is not just a retrieval shortcut — it restructures the model's representational space in a way that generalizes. This would strengthen the theoretical claim that naming is infrastructure, not decoration.

## Limitations

- Results not yet available locally
- Cross-domain pairings and model selection defined in script on VM
- No baseline comparison until results retrieved
- Transfer direction (domain A name applied to domain B questions) may not be symmetric

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
