# G10: Identity Scaffold Effect
<img src="../../images/experiments/g10-identity-noise.png" alt="Identity scaffolds equal noise at geometric level" width="400">

**Status:** COMPLETE (negative result)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** Azure VM (CPU, 64GB RAM)
**Model:** 1 (Qwen 2.5 7B-Instruct)
**Tasks:** 20 questions × 3 conditions (direct, scaffold, noise)
**Total inferences:** 60 (+ phrasing sensitivity runs)

## Purpose

Tests whether identity preambles ("I am a careful analytical thinker") produce content-specific geometric signatures, or whether they're geometrically equivalent to random text of the same length. If identity scaffolds change geometry in content-specific ways, system prompts could be a geometric intervention tool.

## Key Finding (from actual data)

**Identity scaffolds are geometrically indistinguishable from matched-length random text.** Length drives the geometry, not identity content.

| Condition | n | RankMe (mean±sd) | alpha-ReQ (mean±sd) | Coherence (mean±sd) | Avg Prompt Tokens |
|-----------|---|-------------------|---------------------|---------------------|-------------------|
| Direct | 20 | 14.17 ± 1.21 | 0.999 ± 0.028 | 0.915 ± 0.003 | 50.4 |
| Scaffold | 20 | 50.81 ± 1.73 | 0.689 ± 0.004 | 0.874 ± 0.001 | 141.4 |
| Noise | 20 | 52.53 ± 1.77 | 0.710 ± 0.004 | 0.881 ± 0.002 | 147.4 |

**Scaffold vs Noise**: RankMe 50.8 vs 52.5 (negligible difference). Phrasing sensitivity 1.70 vs 1.73 (negligible). The identity content adds nothing beyond what random text of the same length provides.

**Direct vs Scaffold/Noise**: Massive difference driven entirely by prompt length (50 vs 141-147 tokens).

## Why This Matters

This is an important NEGATIVE result:
1. **System prompts don't change geometry via identity content** — only via length
2. **Distinguishes vocabulary from identity**: G06 showed that *structural names* (specific domain knowledge) DO change geometry. G10 shows that *generic identity preambles* do NOT. The compression effect requires relevant content, not just more tokens.
3. **Validates G04's length confound finding**: confirms that encoding geometry is dominated by prompt length

## Assessment

**Verdict:** HONEST NEGATIVE. Identity scaffolds ≈ noise at the geometric level. Supports the distinction between vocabulary (content-specific compression, G06) and identity (generic preamble, no geometric effect).

## Recommendation: Disproof

No rerun needed — the negative result is valuable as-is. However:
- Could test with MORE specific identity scaffolds (domain expertise descriptions rather than generic traits)
- Could test at generation level (as G06 did for vocabulary) rather than encoding
- If specific-identity scaffolds DO change generation geometry → refined finding (specificity matters)

## Files

- `f12_scaffold_reconstruction.py` — Experiment script
- `f12_results_incremental.jsonl` — Raw per-question results
- `f12_full_Qwen_Qwen2.5-7B-Instruct.json` — Full per-question data
- `f12_summary_Qwen_Qwen2.5-7B-Instruct.json` — Summary statistics

## Connection to Spec

Negative result that sharpens the spec's vocabulary claim. The spec's value is NOT in identity scaffolding — it's in structural vocabulary. Generic system prompts ("be helpful and honest") don't change geometry. Specific structural names (prosopagnosia, Brooks's Law) do. This is an important distinction for the publication narrative.

## Limitations

- 1 model only (Qwen 2.5 7B)
- Scaffold prompts are generic ("I am a careful analytical thinker") — more specific identity descriptions might produce different results
- Only measures encoding, not generation trajectory
- CPU inference only (float32)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
