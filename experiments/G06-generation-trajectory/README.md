# G06: Generation Trajectory Compression (The "Breakthrough")

**Status:** COMPLETE — but generation-length confound needs resolution (see below)
**Experiment type:** Geometric (hidden-state extraction + generation trajectory)
**Platform:** Azure VM (CPU, 64GB RAM)
**Model:** 1 (Qwen 2.5 7B-Instruct)
**Tasks:** 12 confabulation questions × 3 conditions (padded, grounded, irrelevant)
**Total inferences:** 36

## Purpose

Fixes all known issues from G03/G04/G05:
1. Uses questions the model actually confabulates on
2. Three conditions with matched PROMPT token lengths (~70 tokens each)
3. Extracts generation trajectory — hidden states accumulated across ALL generated tokens, not just prompt encoding

The key innovation: instead of measuring prompt encoding geometry (which is dominated by prompt length), measures how the representational space evolves during generation.

## Key Finding (from actual data)

**Vocabulary compresses generation trajectory by 38% (RankMe 145→90, d=-1.49, p=0.0004).**

| Condition | n | Gen RankMe (mean±sd) | Avg Gen Tokens |
|-----------|---|---------------------|----------------|
| Padded | 12 | 143.5 ± 2.3 | 200 |
| Grounded | 12 | 89.7 ± 36.4 | 120 |
| Irrelevant | 12 | 145.5 ± 3.9 | 199 |

| Comparison | Cohen's d | t | p |
|-----------|----------|---|---|
| **Grounded vs Irrelevant** | **-1.49** | **-4.93** | **0.000449** |
| Grounded vs Padded | -1.43 | -4.75 | 0.000599 |
| Padded vs Irrelevant | ~0 | — | n.s. |

Padded and irrelevant produce nearly identical trajectories (~145 RankMe). Grounded compresses to ~90. This separation (d=-1.49) is content-specific — it's the structural name, not the extra context, that changes the geometry.

## CRITICAL: Generation-Length Confound

**RankMe correlates with generation token count at r=0.996 (p<1e-6) across all conditions and r=0.997 within grounded alone.**

The grounded condition generates shorter, more focused responses (avg 120 tokens vs 199-200 for padded/irrelevant). Shorter generation trajectories mechanically produce lower RankMe because the SVD operates on a matrix with fewer rows (token positions).

There are two interpretations:

1. **The compression IS the finding:** The model generates fewer tokens because the structural name constrains the generation space. The shorter, more focused response IS the compression. RankMe measures the trajectory's effective dimensionality, and a focused trajectory naturally has lower dimensionality.

2. **The compression is an artifact:** Any content that causes shorter generation would produce lower RankMe. The structural name might just be stopping generation earlier rather than changing the representational geometry.

**To resolve:** Re-run with generation length clamped (force all conditions to generate exactly N tokens). If RankMe compression persists → interpretation 1 (genuine geometric compression). If RankMe equalizes → interpretation 2 (length artifact).

## SYNTHESIS Accuracy Check

SYNTHESIS says: "d=-1.49, p=0.0004, length-controlled."
- The d and p values are correct ✓
- "Length-controlled" refers to PROMPT length only. Generation length is NOT controlled. ⚠️
- The SYNTHESIS should specify: "prompt-length-controlled" to avoid implying generation length was also controlled

## Assessment

**Verdict:** STRONGEST vocabulary experiment — but the generation-length confound means the headline claim needs qualification. The separation between grounded and irrelevant (d=-1.49) is real and reproducible. Whether it reflects genuine representational compression or a generation-length artifact is unresolved.

## Recommendation: Disproof / Next Steps

**HIGH PRIORITY:** G06v2 — clamp generation length across all conditions:
- Force `max_new_tokens=200, min_new_tokens=200` for all conditions
- If grounded still shows lower RankMe → genuine compression (spec validated)
- If RankMe equalizes → finding was generation-length artifact (spec must be revised)

Also:
- Run on 8+ models across architectures (currently 1 model only)
- G17 (Vocabulary Dosage) and G18 (Vocabulary Transfer) test boundary conditions but don't resolve the length confound

## Files

- `f3d_true_confab_controlled.py` — Experiment script (3-condition, generation trajectory)
- `find_confabulation_questions.py` — Confabulation question finder
- `f3d_Qwen_Qwen2.5-7B-Instruct.jsonl` — Raw results (36 rows, 12 questions × 3 conditions)

## Connection to Spec

Central to Claim 2 (vocabulary-as-compression-infrastructure). G06 is cited as "THE BREAKTHROUGH" in SYNTHESIS and bridge-document. The d=-1.49 effect is real, but the generation-length confound means we need G06v2 with clamped generation before using this as a primary publication claim.

## Limitations

- 1 model only (Qwen 2.5 7B)
- 12 questions (small n)
- Generation length not controlled (grounded avg 120 vs padded/irrelevant avg 200 tokens)
- RankMe vs gen_tokens r=0.996 — generation length confound
- CPU inference only (float32)
- High variance in grounded condition (sd=36.4 vs sd=2.3-3.9 for other conditions)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
