# G04: Length-Controlled Vocabulary Effect

**Status:** COMPLETE
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** Azure VM (CPU, 64GB RAM)
**Model:** 1 (Qwen 2.5 7B-Instruct)
**Tasks:** 20 questions × 3 conditions (confabulation, grounded, irrelevant)
**Total inferences:** 60

## Purpose

Controls for the length confound discovered in G03. Adds a third condition: irrelevant context of matched length to the grounded condition. If grounded differs from confabulation but irrelevant does not → vocabulary matters. If both differ similarly → length is the driver. If grounded differs from BOTH confabulation AND irrelevant → vocabulary has an effect beyond length.

## Key Finding (from actual data)

**Length drives most of the G03 effect. Vocabulary produces a small additional redistribution (d≈0.5) at encoding.**

### Confab vs Grounded (replicates G03 — length-confounded)

| Metric | Confab | Grounded | d | p |
|--------|--------|----------|---|---|
| RankMe | 6.76 | 17.96 | -7.91 | 1.3e-18 |
| alpha_req | 1.35 | 0.89 | +5.81 | 4.3e-16 |
| coherence | 0.945 | 0.918 | +6.35 | 8.0e-17 |
| mean_norm | 713.7 | 428.8 | +7.45 | 4.1e-18 |

### Confab vs Irrelevant (pure length effect)

| Metric | Confab | Irrelevant | d | p |
|--------|--------|------------|---|---|
| RankMe | 6.76 | 17.14 | -6.47 | 5.6e-17 |
| alpha_req | 1.35 | 0.91 | +6.90 | 1.7e-17 |
| coherence | 0.945 | 0.916 | +9.01 | 1.2e-19 |
| mean_norm | 713.7 | 436.5 | +7.79 | 1.8e-18 |

### Grounded vs Irrelevant (vocabulary effect, length-controlled)

| Metric | Grounded | Irrelevant | d | p | Significant? |
|--------|----------|------------|---|---|-------------|
| RankMe | 17.96 | 17.14 | +0.60 | 0.017 | Yes |
| alpha_req | 0.889 | 0.907 | -0.51 | 0.038 | Yes |
| coherence | 0.918 | 0.916 | +0.48 | 0.050 | Borderline |
| mean_norm | 428.8 | 436.5 | -0.48 | 0.049 | Borderline |

## Interpretation

Confab-vs-grounded and confab-vs-irrelevant produce nearly identical huge effects (d~6-9). This confirms length drives G03's massive effect sizes.

But grounded vs irrelevant shows a small, consistent difference (d≈0.5 across all metrics). Vocabulary slightly EXPANDS rank and slightly reduces alpha — the opposite of what the spec predicted (compression). This is redistribution: the structural name reorganizes the encoding space, it doesn't compress it.

**G06 later showed compression happens at generation, not encoding.** The encoding-stage redistribution (G04) and generation-stage compression (G06) are complementary findings.

## Assessment

**Verdict:** IMPORTANT METHODOLOGICAL CONTROL. Confirmed length confound. Revealed vocabulary effect is real but small (~d=0.5) and operates as redistribution, not compression, at encoding. Set up G06's breakthrough by distinguishing encoding from generation.

## Recommendation: Disproof

G04's finding (d≈0.5 redistribution at encoding) is modest and on a single model. To stress-test:
- Run on 8+ models across architectures — if the d≈0.5 disappears on non-Qwen models, it's architecture-specific
- However, the higher-value target is G06's generation compression (d=-1.49), which is the claim that actually matters for the spec

## Files

- `f3b_length_control.py` — Experiment script (3-condition design)
- `f3b_Qwen_Qwen2.5-7B-Instruct.jsonl` — Raw results (60 rows, 20 questions × 3 conditions)
- `f3b_summary_Qwen_Qwen2.5-7B-Instruct.json` — Summary statistics with all pairwise comparisons

## Connection to Spec

Part of the vocabulary-as-compression-infrastructure thesis (Claim 2). G04 controlled for G03's confound and found the encoding effect is redistribution, not compression. This redirected the investigation toward generation-time measurement (G06), which found the actual compression.

## Limitations

- 1 model only (Qwen 2.5 7B)
- Irrelevant context is generic padding — a better control would match domain/complexity
- CPU inference only (float32)
- Generation metrics still all NaN (single-token hidden states)
- Borderline significance on coherence and mean_norm (p=0.050, p=0.049)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
