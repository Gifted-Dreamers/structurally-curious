# G12: Hard Distinctions (Geometry vs Perplexity)

**Status:** COMPLETE — KEY SPEC RESULT
**Experiment type:** Geometric + perplexity comparison
**Platform:** Azure VM (CPU, 64GB RAM)
**Model:** 1 (Qwen 2.5 7B-Instruct)
**Tasks:** 20 pairs across 4 hard distinctions (5 pairs each)
**Total inferences:** 40

## Purpose

Tests the spec's core value proposition: can geometry distinguish cognitive modes that perplexity CANNOT? Four hard distinctions where the surface outputs look similar but the underlying cognitive mode differs.

## Key Finding (from actual data)

**Censorship vs refusal: geometry wins where perplexity fails.** This is the spec's primary differentiator.

### Censorship vs Refusal (n=5, tokens=200 both conditions)

| Method | d | p | Separates? |
|--------|---|---|-----------|
| Perplexity | -0.48 | 0.391 | **No** |
| **RankMe** | **1.48** | **0.041** | **Yes** |

Both produce refusal-like outputs. Perplexity can't tell them apart. Geometry can. Appropriate refusal has higher RankMe (145.8) than possible censorship (141.0).

### Sycophancy vs Agreement (n=5, tokens=200)

| Method | d | p | Separates? |
|--------|---|---|-----------|
| **Perplexity** | **-2.44** | **0.008** | **Yes** |
| RankMe | -1.07 | 0.098 | No |

Perplexity wins here. Sycophancy has higher perplexity (more uncertain when agreeing without conviction).

### Confabulation vs Openness (n=5, tokens=200)

| Method | d | p | Separates? |
|--------|---|---|-----------|
| Perplexity | -0.27 | 0.622 | No |
| RankMe | -0.75 | 0.210 | No |

**Neither separates.** This is an honest negative — at 7B scale, confabulation and genuine openness are geometrically indistinguishable.

### Performative vs Grounded (n=5, tokens=248-250)

| Method | d | p | Separates? |
|--------|---|---|-----------|
| **Perplexity** | **1.44** | **0.045** | **Yes** |
| RankMe | -0.82 | 0.178 | No |

Perplexity wins. Grounded responses have higher perplexity (more careful/uncertain).

## Summary Table

| Distinction | Perplexity wins? | Geometry wins? | Unique contribution |
|------------|-----------------|---------------|-------------------|
| Censorship vs Refusal | No | **Yes** | **GEOMETRY ONLY** |
| Sycophancy vs Agreement | Yes | No | Perplexity |
| Confab vs Openness | No | No | Neither |
| Performative vs Grounded | Yes | No | Perplexity |

## Assessment

**Verdict:** CRITICAL POSITIVE for the spec. The censorship/refusal result (d=1.48, p=0.041) is the clearest evidence that geometry adds unique value. Perplexity can detect confabulation (G07) and sycophancy, but it CANNOT detect censorship. Geometry can.

**Caveat:** n=5 pairs per distinction. This needs replication across architectures. G15 (censorship cross-architecture) and G14 (DWL scale) test related claims.

## Recommendation: Disproof

**HIGH PRIORITY:** Replicate censorship vs refusal on 8+ models across architectures.
- If the d=1.48 holds across models → robust finding, spec's core claim validated
- If it fails on other architectures → model-specific artifact
- n=5 is marginal for publication. Need n≥20 pairs per distinction.

Also: test with larger models (>7B) where cognitive modes may be more differentiated.

## Files

- `f17_hard_distinctions.py` — Experiment script
- `f17_Qwen_Qwen2.5-7B-Instruct.jsonl` — Raw results (40 rows)
- `f17_summary_Qwen_Qwen2.5-7B-Instruct.json` — Summary with all d values and separability flags

## Connection to Spec

**THE spec result.** The three-layer architecture exists because:
1. Perplexity catches confabulation (free, Layer 1)
2. Geometry catches what perplexity misses — specifically censorship vs refusal (Layer 2)
3. Vocabulary compresses generation (Layer 3)

G12 validates Layer 2. Without this result, geometry doesn't add enough value to justify hidden-state extraction.

## Limitations

- 1 model only (Qwen 2.5 7B)
- **n=5 per distinction** (marginal for statistical claims)
- Confab vs openness unseparable at this scale
- CPU inference only (float32)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
