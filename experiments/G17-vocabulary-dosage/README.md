# G17: Vocabulary Dosage

**Status:** RUNNING on VMs
**Experiment type:** Geometric (vocabulary compression)
**Platform:** AWS VM + RunPod H200 (GPU)
**Models:** TBD (pending VM results)
**Tasks:** Variable dosage levels of structural name provision

## Purpose

Tests whether vocabulary compression varies with the amount of structural name provided — a dosage effect. G06 established that vocabulary compresses generation (d=-1.49). G17 asks: is the compression proportional to how much vocabulary is given, or is it a threshold effect where any vocabulary produces the full compression?

This matters for practical deployment. If dosage-dependent, systems can be tuned. If threshold, even minimal vocabulary scaffolding provides full benefit.

## Key Finding

**RUNNING — no results yet.** Script deployed to VMs. Results directory empty locally.

## Assessment

**Verdict:** PENDING. No data to assess.

## Recommendation

1. **Retrieve results from VMs** when runs complete
2. **Compare dosage curves** across models — if compression is linear with dosage, this validates a tunable system; if step-function, minimal vocabulary suffices
3. **Connect to G06 baseline** — dosage results should be interpretable against the d=-1.49 full-vocabulary compression already measured

## Files

- `f34_dosage_fixed.py` — Experiment script
- `results/` — Results directory (empty locally, pending VM transfer)

## Connection to Spec

Directly tests Layer 3 (vocabulary compression) mechanics. G06 proved vocabulary compresses generation. G17 asks how much vocabulary is needed. The answer determines whether the spec's vocabulary layer needs rich structural names or whether minimal naming suffices — which affects both implementation complexity and the theoretical claim about why vocabulary works.

## Limitations

- Results not yet available locally
- Dosage levels and model selection defined in script on VMs
- No baseline comparison until results retrieved

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
