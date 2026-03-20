# G03: Vocabulary Compression

**Status:** COMPLETE (but confounded — see G04, G06)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** Azure VM (CPU, 64GB RAM)
**Model:** 1 (Qwen 2.5 7B-Instruct)
**Tasks:** 20 questions × 2 conditions (confabulation vs grounded)
**Total inferences:** 40

## Purpose

Tests the spec's core claim: providing a structural name produces measurable rank compression in model hidden states. Present a question without context (confabulation condition) vs with the correct structural name (grounded condition), extract hidden states from layers 21-28, compare geometric metrics.

## Key Finding (from actual data)

**Vocabulary changes geometry massively (d>5.8) — but the result is confounded by prompt length.**

| Metric | Confab Mean | Grounded Mean | Cohen's d | p-value | Direction | Verdict |
|--------|------------|---------------|-----------|---------|-----------|---------|
| RankMe | 6.76 | 17.96 | -7.91 | 1.3e-18 | EXPANSION | CONTRADICTS |
| alpha_req | 1.35 | 0.89 | +5.81 | 4.3e-16 | EXPANSION | CONTRADICTS |
| dir. coherence | 0.945 | 0.918 | +6.35 | 8.0e-17 | COMPRESSION | SUPPORTS |
| mean_norm | 713.7 | 428.8 | +7.45 | 4.1e-18 | COMPRESSION | SUPPORTS |

**The problem:** Grounded prompts include the structural name in context (~55 tokens vs ~23 tokens for confabulation prompts). Longer prompts mechanically produce higher RankMe. The length confound correlates at r=0.9991 with the RankMe difference.

Directional coherence and mean norm support the spec, but RankMe and alpha_req contradict — and the contradiction is likely driven by prompt length, not cognitive mode.

## What Happened Next

- **G04** controlled for length (added irrelevant padding condition). Vocabulary effect survived at d≈0.5 — reduced from d>5.8 but still present. Effect is redistribution at encoding, not compression.
- **G05** tested on questions the model actually confabulates on. Same length confound persisted (60 vs 131 tokens).
- **G06** was the breakthrough: measured GENERATION trajectory (accumulated hidden states across all generated tokens), not just prompt encoding. **Vocabulary compresses generation by 38%** (RankMe 145→90, d=-1.49, p=0.0004). Length-controlled.

## Assessment

G03 is a necessary first step that revealed the central methodological challenge (length confound) and motivated the controlled follow-ups. The raw effect sizes are unusable for spec claims, but the directional coherence result is interesting — it compresses in grounded even though RankMe expands.

**Verdict:** PRELIMINARY. Not usable alone. Use G06 for vocabulary compression claims.

## Recommendation: Disproof

G03 itself doesn't need a rerun — G04 and G06 supersede it. The disproof target is G06's generation compression (d=-1.49). To disprove:
- Run G06 protocol on 8+ models across architectures (currently 1 model only)
- If generation compression disappears on other architectures → finding is model-specific, not general
- **G17 (Vocabulary Dosage)** and **G18 (Vocabulary Transfer)** are already designed and running to test boundary conditions

## Files

- `f3_vocabulary_compression.py` — Experiment script
- `f3_deep_analysis.py` — Per-layer and per-domain analysis script
- `f3_Qwen_Qwen2.5-7B-Instruct.jsonl` — Raw results (40 rows, 20 questions × 2 conditions)
- `f3_summary_Qwen_Qwen2.5-7B-Instruct.json` — Summary statistics

## Connection to Spec

Part of the vocabulary-as-compression-infrastructure thesis (spec Claim 2). G03 opened the investigation; G06 delivered the evidence. The lesson: prompt encoding geometry is dominated by length; generation trajectory geometry captures the actual cognitive mode difference.

## Limitations

- 1 model only (Qwen 2.5 7B)
- Severe length confound (confab ~23 tokens, grounded ~55 tokens)
- Generation metrics all NaN (single-token hidden states from `model.generate`)
- CPU inference only (float32)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
