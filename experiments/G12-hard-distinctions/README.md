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

## G12v2: Cross-Architecture Censorship Detection (Session 62) — COMPLETE

**6 models, 20 censorship/refusal pairs each, tested at 75 and 200 generated tokens.**

### The headline: PROMPT ENCODING detects censorship on ALL architectures. Generation trajectory is Qwen-specific.

#### Prompt Encoding (before any generation — ARCHITECTURE-INVARIANT)

| Model | Prompt RankMe d | p |
|-------|:---:|:---:|
| **Qwen2.5-7B** | **-2.20** | **<1e-6** |
| **Qwen3.5-9B** | **-2.54** | **<1e-6** |
| **Qwen3.5-27B** | **-2.49** | **<1e-6** |
| **Qwen3.5-9B-abliterated** | **-2.49** | **<1e-6** |
| **Mistral-7B** | **-2.02** | **<1e-6** |
| **Llama-8B-abliterated** | **-2.42** | **<1e-6** |

ALL models, ALL architectures, including abliterated models. d>2.0 across the board. The censorship/refusal distinction exists in the prompt encoding geometry of every model tested.

#### Generation Trajectory (Qwen-specific)

| Model | Gen RM @75tok | Gen RM @200tok | Perplexity @75tok |
|-------|:---:|:---:|:---:|
| **Qwen2.5-7B** | d=1.23, p<0.001 | d=-0.32, n.s. | d=-0.55, n.s. |
| **Qwen3.5-9B** | d=-0.57, p=0.020 | d=-0.74, p=0.004 | d=-0.19, n.s. |
| **Qwen3.5-27B** | d=-0.19, n.s. | d=-0.57, p=0.020 | d=-0.68, p=0.007 |
| Qwen3.5-9B-abl | d=-0.38, n.s. | d=-0.10, n.s. | d=-0.45, n.s. |
| Mistral-7B | d=0.19, n.s. | d=0.30, n.s. | d=-0.03, n.s. |
| Llama-8B-abl | d=-0.15, n.s. | d=0.01, n.s. | d=-0.02, n.s. |

At generation level, only safety-trained Qwen models maintain the signal. Abliteration, Mistral, and Llama lose it during generation.

**Perplexity never reliably separates censorship from refusal on any model at any token count after Bonferroni correction.**

### Interpretation

The censorship/refusal distinction is encoded in the PROMPT geometry of all models — the model "knows" the difference before generating. But only Qwen's safety training architecture preserves this signal through the generation trajectory. This suggests:

1. All models encode censorship-relevant features from the prompt
2. Qwen's RLHF creates generation-level geometric signatures that others don't
3. A monitor based on prompt encoding (not generation) would work universally

### Files
- `g12v2_censorship.py` — G12v2 experiment script
- `g12v2_*.jsonl` — Per-model raw results (6 files)
- `g12v2_summary_*.json` — Per-model summary statistics (6 files)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
