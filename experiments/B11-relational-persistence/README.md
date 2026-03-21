# B11: Relational Priming Persistence
<img src="../../images/experiments/b11-relational-persistence.png" alt="Relational priming persistence varies by architecture" width="400">

**Status:** COMPLETE (8 models, 6 families)
**Experiment type:** Geometric (hidden-state extraction, generation trajectory)
**Platform:** RunPod H200 (GPU)
**Models:** 8 (Qwen2.5-7B, Qwen3.5-9B, Qwen3.5-9B-abl, Mistral-7B, Llama-8B, Llama-8B-abl, Phi-4, Gemma-2-9B)
**Tasks:** 8 turns × 2 conditions (control, primed) = 16 per model
**Total inferences:** 128

## Purpose

Tests whether a relational priming turn persists into subsequent generation — does the model's geometry stay changed after the relational input is no longer in the immediate context?

2 conditions: control (standard prompt), primed (relational context given before task)

## Key Finding (from actual data)

**Priming compresses generation on 6/7 models. Three reach significance.**

| Model | Control RM | Primed RM | d | p | Sig? |
|-------|-----------|-----------|---|---|------|
| **Gemma-2 9B** | **91.3** | **2.2** | **-4.56** | **<0.0001** | **YES** |
| **Llama 8B-abl** | **121.1** | **112.9** | **-2.10** | **0.001** | **YES** |
| **Mistral 7B** | **119.9** | **99.4** | **-1.98** | **0.002** | **YES** |
| Qwen 2.5-7B | 115.4 | 110.7 | -0.99 | 0.109 | no |
| Llama 3.1-8B | 119.2 | 112.0 | -0.92 | 0.108 | no |
| Qwen 9B-abl | 121.6 | 120.2 | -0.85 | 0.145 | no |
| Qwen 3.5-9B | 97.3 | 113.6 | +0.83 | 0.166 | no (opposite) |

**Gemma-2 9B** shows extreme compression under priming (91.3 → 2.2, d=-4.56). This is a near-complete collapse of representational space.

6/7 models show primed < control (compression). Qwen 3.5-9B is the exception — priming EXPANDS its generation.

## Assessment

**Verdict:** MIXED — direction mostly consistent (6/7 compress) but 3/7 significant. The Gemma collapse (d=-4.56) is dramatic and needs investigation — may be a truncation artifact or a genuine extreme compression effect.

Relational priming persists into subsequent generation on some architectures but not others. Architecture-dependent, like G24.

## Files

- `results/b11_*.jsonl` — 8 model result files (16 inferences each)

## Connection to Spec

Tests whether the relational signal from G19 persists beyond the immediate context. The compression finding is unexpected — G19 showed presence EXPANDS at prompt encoding, but B11 shows priming may COMPRESS at generation. Different measurement stage, different direction — consistent with G27's finding that prompt encoding and generation behave differently.

## Limitations

- n=8 per condition
- Only generation RankMe measured
- Gemma collapse needs verification (possible truncation)
- 7 models with valid data

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
