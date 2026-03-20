# G14: DWL Detection at Scale (Cross-Architecture)
<img src="../../images/experiments/g14-dwl-mixed.png" alt="DWL detection shows mixed directions across architectures" width="400">

**Status:** COMPLETE (directional but not significant)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** Azure VM + AWS VM (CPU), RunPod H200 (GPU)
**Models:** 10 (Qwen2.5-7B, Qwen3.5-9B, Qwen3.5-9B-abliterated, Qwen3.5-27B, Qwen3.5-122B, Llama-3.1-8B, Llama-8B-abliterated, Mistral-7B, Gemma-2-9b, Gemma-3-4b)
**Tasks:** 5 scenarios × 3 conditions (honest, DWL, lie) per model
**Total inferences:** ~150

## Purpose

Tests whether G13's finding (DWL geometrically distinguishable from honest) replicates across architectures. If the DWL signal is architecture-invariant, it's a robust finding. If it's Qwen-specific, the spec needs qualification.

## Key Finding (from actual data)

**DWL shows higher RankMe than honest in 7/10 models, but NO model reaches significance at n=5.**

| Model | DWL RankMe | Honest RankMe | d | p | DWL tok | Hon tok |
|-------|-----------|---------------|---|---|---------|---------|
| Gemma-2-9b | 47.2 | 27.6 | 0.79 | 0.191 | 56 | 32 |
| Gemma-3-4b | (no geometric data) | — | — | — | — | — |
| Llama-3.1-8B | 61.8 | 58.6 | 0.59 | 0.301 | 74 | 74 |
| Llama-8B-abliterated | 59.8 | 40.9 | 0.78 | 0.194 | 72 | 50 |
| Mistral-7B | 60.1 | 42.5 | 0.86 | 0.159 | 70 | 48 |
| Qwen2.5-7B | 55.6 | 61.4 | -0.71 | 0.230 | 68 | 74 |
| Qwen3.5-9B | 108.5 | 110.4 | -0.06 | 0.912 | 132 | 149 |
| Qwen3.5-9B-abliterated | 62.7 | 61.3 | 0.60 | 0.300 | 74 | 74 |
| Qwen3.5-27B | 124.2 | 121.2 | 0.90 | 0.145 | 149 | 149 |
| Qwen3.5-122B | 64.2 | 56.6 | 0.60 | 0.297 | 74 | 66 |

**Direction:** 7/10 models show DWL > Honest (consistent with G13). 2 models show opposite direction (Qwen2.5-7B, Qwen3.5-9B). 1 model (Gemma-3-4b) has no geometric data.

**Token confound:** Where DWL and honest have different generation lengths, the model with more tokens tends to have higher RankMe. On Llama-8B and Qwen3.5-9B-abliterated (both 74/74 tokens), the effect is minimal.

## SYNTHESIS Accuracy Check

SYNTHESIS says "5/6 models show DWL sprawls more than honest (d=-0.6 to -0.9)". Using opposite sign convention (honest-DWL), this matches the directional finding. But:
- **More models now available** (10 vs 6 in earlier reports)
- **No significance at n=5** — all p>0.14
- SYNTHESIS should note "directional but NOT significant"

## Assessment

**Verdict:** DIRECTIONAL SUPPORT, NOT CONFIRMED. The DWL>Honest direction is consistent across most architectures (7/10), supporting G13. But n=5 per model is insufficient for significance. The generation-length confound remains uncontrolled.

## Recommendation: Disproof

**CRITICAL:** Increase scenarios from 5 to 20+ per model. At d≈0.7 and n=5, power is ~40%. At n=20, power rises to ~85%. The effect may be real but underpowered.

Also:
- Clamp generation length across conditions
- Gemma-3-4b needs investigation (why no geometric data?)
- The two contrary models (Qwen2.5-7B, Qwen3.5-9B) need attention — are they genuinely different or noise at n=5?

## Files

- `f27_*.jsonl` — Per-model results (10 files, 5 scenarios × 3 conditions each)
- `results/f27_qwen35_122b.jsonl` — 122B MoE model results
- `results/f27_qwen35_27b.jsonl` — Duplicate of top-level 27B results

## Connection to Spec

Tests whether geometry's DWL detection (first found in G13) generalizes across architectures. The direction is consistent but power is insufficient. This is the most important experiment to scale up — it determines whether geometry's unique contribution (detecting DWL) is robust or artifact.

## Limitations

- **n=5 scenarios per model** (insufficient for significance at observed effect sizes)
- Generation length not controlled across conditions
- 1 model has no geometric data (Gemma-3-4b)
- Mixed CPU/GPU inference across models
- Duplicate 27B results in two locations

## G14-expanded: 20 Scenarios (Session 62)

**10 models, 20 scenarios per model (4x the original n=5).** Follows recommendation to increase power.

### Results

| Model | DWL RM | Honest RM | d | p |
|-------|--------|-----------|---|---|
| **Qwen3.5-9B-abliterated** | **124.0** | **121.0** | **0.66** | **0.009** |
| **Llama-8B-abliterated** | **101.2** | **79.4** | **0.71** | **0.006** |
| **Mistral-Small-24B** | **28.0** | **62.1** | **-0.90** | **0.001** |
| Qwen3.5-27B | 125.2 | 118.4 | 0.37 | 0.127 |
| Qwen2.5-7B | 105.1 | 100.0 | 0.24 | 0.300 |
| Qwen3.5-9B | 115.3 | 118.1 | -0.11 | 0.633 |
| Llama-3.1-8B | 116.4 | 120.1 | -0.35 | 0.143 |
| DeepSeek-R1-32B | 75.2 | 84.0 | -0.26 | 0.273 |
| Mistral-7B | 46.8 | 49.5 | -0.09 | 0.712 |
| Gemma-2-27b | (no data) | -- | -- | -- |
| Phi-4 | (no data) | -- | -- | -- |

### Key Findings

3/10 significant but in **MIXED DIRECTIONS**:

- **Abliterated models (Qwen3.5-9B-abl, Llama-8B-abl): DWL > Honest.** Removing safety training exposes a DWL signal where the deceptive condition uses MORE representational dimensions than honest. This is consistent with the original G13/G14 hypothesis.
- **Mistral-Small-24B: DWL < Honest (d=-0.90).** The OPPOSITE direction -- honest responses occupy more representational space than DWL. This is a large, highly significant effect in the wrong direction.

The mixed directionality means DWL detection via generation-trajectory RankMe is **unreliable across architectures**. The sign of the effect depends on the model family and whether safety training is present. A monitor built on "DWL has higher RankMe than honest" would produce false negatives on Mistral-Small and false positives on safety-trained Qwen/Llama.

### Updated Verdict

**DWL detection at generation trajectory is NOT a reliable cross-architecture signal.** The original G14 finding (7/10 directional at n=5) was underpowered and masked the sign-reversal problem. At n=20, significance emerges but in contradictory directions. The spec's DWL detection claim should be restricted to prompt-encoding geometry (G13) rather than generation trajectory, or should note that the generation-trajectory signal is architecture-dependent and sign-unstable.

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
