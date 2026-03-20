# G25: Relationship + Deception-Without-Lying (Prompt Encoding)
<img src="../../images/experiments/g25-dwl-prompt-encoding.png" alt="DWL sprawl visible at prompt encoding" width="400">

**Status:** PARTIAL (1 model, 1 scenario only — needs more models and scenarios)
**Experiment type:** Geometric (hidden-state extraction, prompt encoding)
**Platform:** AWS EC2 r7a.16xlarge (CPU)
**Models:** 1 (Qwen2.5-7B-Instruct)
**Design:** 20 DWL scenarios × 3 conditions × 2 frames = 120 per model (only 6 inferences completed — 1 scenario)
**Total inferences:** 6

## Purpose

G14-expanded showed generation-trajectory DWL detection is unreliable (mixed directions, 3/10 sig). But G12v2 proved prompt encoding is UNIVERSAL for censorship (d>2.0 on 10/10 models). G25 tests whether the same prompt-encoding approach works for DWL detection, and whether relational presence changes the DWL signature.

3 conditions: honest (truthful), DWL (technically true but misleading), lie (outright false)
2 frames: cold (prompt as-is), presence ("I need to trust what you tell me...")

## Key Finding (from actual data — 1 scenario only, directional)

**DWL sprawls at prompt encoding. Lying compresses. Pattern holds in both frames.**

| Frame | Honest RM | DWL RM | Lie RM | DWL sprawl | Lie collapse |
|-------|-----------|--------|--------|------------|-------------|
| Cold | 12.6 | 20.6 | 8.3 | +8.0 | -4.3 |
| Presence | 21.7 | 31.2 | 16.8 | +9.4 | -5.0 |

DWL requires more representational dimensions than honest (sprawl). Lying requires fewer (collapse). This is the same pattern G13 found at generation level (d=-0.91), now visible at prompt encoding before a single token is generated.

**Last-layer RankMe shows the same ordering with larger separation:**

| Frame | Honest RM_last | DWL RM_last | Lie RM_last |
|-------|----------------|-------------|-------------|
| Cold | 39.1 | 59.2 | 28.4 |
| Presence | 57.5 | 76.1 | 47.1 |

**Presence expands everything uniformly** (+8.5 to +10.6 across all conditions). The DWL-honest gap is preserved under presence — relationship does not mask deception.

**Perplexity shows DWL ≈ lie (both higher than honest) — no separation:**
- Honest: cold 5.00, presence 6.64
- DWL: cold 8.43, presence 9.08
- Lie: cold 9.11, presence 5.83

Geometry separates DWL from lie (opposite directions on RankMe). Perplexity cannot.

## Assessment

**Verdict:** DIRECTIONAL POSITIVE but underpowered. Only 1 scenario completed out of 20 designed. The pattern is consistent with G13 (DWL sprawls) but at prompt encoding, which could enable zero-overhead detection like G12v2 does for censorship.

**Caveat:** Token counts differ across conditions (33-99 tokens) because the prompts have different lengths. This introduces a potential length confound at prompt encoding. The DWL prompt is longest (72 tokens) and has the highest RankMe — some of the "sprawl" may be length-driven. Needs clamped-length version or per-token normalization.

## Recommendation

- Run remaining 19 scenarios on H200 (GPU will be ~20x faster than CPU)
- Run across 10+ models to test cross-architecture validity
- Add length normalization or token-count regression to separate DWL signal from length confound
- If confirmed: prompt-encoding DWL detection could match G12v2's universality for censorship

## Files

- `results/g25_Qwen_Qwen2.5-7B-Instruct.jsonl` — 6 inferences (1 scenario × 3 conditions × 2 frames)
- `results/g25_summary_Qwen_Qwen2.5-7B-Instruct.json` — Statistical summary (all "insufficient_pairs" at n=1)
- `g25_relational_dwl.py` — Experiment script (20 scenarios, prompt-encoding extraction)

## Connection to Spec

Tests whether the spec's geometric monitor can detect deception-without-lying at prompt encoding (before generation starts). G13 proved DWL detection at generation level. G14-expanded showed it doesn't replicate across architectures at generation. G12v2 showed prompt encoding IS universal for censorship. G25 bridges these: if DWL is detectable at prompt encoding, the spec has two universal detectors (censorship + DWL) with zero inference overhead.

## Limitations

- 1 scenario only (20 designed, 19 remaining)
- 1 model only (Qwen2.5-7B)
- Token-count confound uncontrolled
- n=1 per cell — no statistics possible

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
