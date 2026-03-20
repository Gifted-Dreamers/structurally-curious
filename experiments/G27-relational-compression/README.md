# G27: Relationship vs Premature Compression
<img src="../../images/experiments/g27-compression-trap.png" alt="Relational frame expands prompt encoding but generation flattens" width="400">

**Status:** COMPLETE (1 model, 10 topics — full design)
**Experiment type:** Geometric (hidden-state extraction, prompt encoding + generation)
**Platform:** AWS EC2 r7a.16xlarge (CPU)
**Models:** 1 (Qwen2.5-7B-Instruct)
**Design:** 10 topics × 3 information levels × 2 frames = 60 inferences per model
**Total inferences:** 60

## Purpose

B02 found 0 confidence shift across 22 models when moving from partial to full information — the model treats incomplete input with the same confidence as complete input. That's premature compression (the Berk-Nash trap). G27 asks: does relational framing break the trap?

3 information levels:
- **Partial:** question + 1 short paragraph (incomplete, leads to wrong conclusion)
- **Full:** question + 3 paragraphs (complete picture)
- **Contradictory:** question + 1 paragraph that contradicts partial info

2 frames:
- **Cold:** information presented as-is
- **Relational:** "I've read all the source material on this, and I think there's something important you might be missing. Take your time with this — I'd rather have your genuine uncertainty than a confident answer based on incomplete information."

## Key Finding (from actual data)

### Prompt encoding: Relational frame massively expands representational space

| Frame | Partial | Contradictory | Full |
|-------|---------|---------------|------|
| Cold | 33.2 ± 5.6 | 74.4 ± 8.6 | 123.6 ± 17.7 |
| Relational | 53.5 ± 6.4 | 100.0 ± 9.4 | 152.8 ± 18.9 |

Relational frame adds +20 to +30 RankMe points across ALL information levels. This replicates the G19 monotonic expansion pattern: relationship opens representational space before generation starts. The model uses more dimensions to represent the same content when delivered relationally.

The information-level gradient is preserved in both frames: partial < contradictory < full. More information = more representational dimensions. The relational frame doesn't collapse this gradient — it lifts the entire curve.

### Generation: Everything flattens — no compression trap detectable

| Frame | Partial | Contradictory | Full |
|-------|---------|---------------|------|
| Cold | 112.2 ± 8.9 | 111.3 ± 4.9 | 111.7 ± 2.4 |
| Relational | 108.9 ± 4.3 | 110.8 ± 3.6 | 112.2 ± 1.8 |

All generation RankMe values cluster at 109-112 regardless of frame or information level. The rich prompt-encoding structure (33-153 RankMe) collapses to a narrow band at generation.

**Contradictory does NOT compress generation vs full** (d=-0.09, p=0.84). **Relational frame does NOT change generation under contradiction** (d=-0.12, p=0.79). Neither comparison reaches significance.

### What this means

The Berk-Nash trap doesn't manifest as generation-trajectory compression on Qwen-7B at this design. The model handles contradictory information with the same generation geometry as full information. So there's no compression for presence to resist.

This is consistent with B02's finding (0 shift on 22 models): premature compression may operate at a different level than what generation RankMe captures. The model may be compressing semantically (collapsing to a confident answer) without compressing geometrically (the representational dimensions stay the same).

The prompt-encoding expansion under relational framing (+20 to +30 RM) is consistent with G19, G20, and G23 — relationship opens space. That replicates.

## Assessment

**Verdict:** MIXED. Prompt encoding confirms relational expansion (replicates G19). Generation shows no compression trap to break. The design may need revision — premature compression might need to be measured through confidence language density (B02's behavioral approach) combined with geometry, not generation geometry alone.

## Recommendation

- Run on 10+ models to confirm generation-level null is not Qwen-specific
- Consider adding behavioral measures: hedge count, confidence markers, "I'm not sure" patterns
- May need redesign: test with longer generation (200+ tokens) where compression has time to manifest
- Alternative: measure coherence (not RankMe) at generation — G01 found coherence was the bridge metric, not RankMe

## Files

- `results/g27_Qwen_Qwen2.5-7B-Instruct.jsonl` — 60 inferences (10 topics × 3 info levels × 2 frames)
- `g27_relational_compression.py` — Experiment script

## Connection to Spec

Tests Open Problem #20 (premature compression). B02 showed the trap is real (0 behavioral shift on 22 models). G27 tests whether relationship can break it geometrically. Finding: the trap doesn't manifest as generation geometry changes, so presence can't break what isn't geometrically visible. This suggests premature compression operates at a level the current geometric pipeline doesn't capture — or that generation RankMe is the wrong metric for this phenomenon.

## Limitations

- 1 model only (Qwen2.5-7B)
- Generation RankMe may not capture premature compression
- No behavioral measures (confidence language, hedging)
- 10 topics (adequate for within-model statistics but not cross-architecture claims)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
