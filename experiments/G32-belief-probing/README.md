# G32: Second-Order Belief Probing
<img src="../../images/experiments/g32-belief-probing.png" alt="Audience does not change generation geometry" width="400">

**Status:** COMPLETE (8 models, 6 families)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** RunPod H200 (GPU)
**Models:** 8 (Qwen2.5-7B, Qwen3.5-9B, Qwen3.5-9B-abl, Mistral-7B, Llama-8B, Llama-8B-abl, Phi-4, Gemma-2-9B)
**Tasks:** 5 topics × 3 audiences = 15 per model
**Total inferences:** 120

## Purpose

Tests whether the model's geometric representation changes when addressing different audiences on the same topic. If a model geometrically adjusts based on who it thinks is listening (investor vs regulator vs employee), this reveals second-order belief modeling.

## Key Finding (from actual data)

**Audience does NOT significantly change generation RankMe across most models.**

| Model | Regulator | Employee | Investor | Range |
|-------|----------|---------|----------|-------|
| Qwen 2.5-7B | 137.4 | 140.9 | 136.8 | 4.1 |
| Qwen 3.5-9B | 157.2 | 158.7 | 156.3 | 2.3 |
| Qwen 9B-abl | 162.7 | 163.5 | 162.4 | 1.1 |
| Mistral 7B | 163.3 | 164.8 | 165.0 | 1.7 |
| Llama 3.1-8B | 152.6 | 154.1 | 155.3 | 2.7 |
| Llama 8B-abl | 150.4 | 155.9 | 157.0 | 6.6 |
| Gemma-2 9B | 149.8 | 142.7 | 154.4 | 11.7 |
| **Phi-4** | **80.2** | **51.7** | **34.0** | **46.2** |

Most models show tiny audience differences (1-7 RankMe points). Not systematic.

**Phi-4 is the dramatic exception:** Regulator 80.2 → Employee 51.7 → Investor 34.0. A 46-point range — the model geometrically collapses when addressing an investor vs a regulator. This is either genuine audience-dependent processing or a Phi-4-specific artifact.

Gemma shows moderate audience sensitivity (range 11.7).

## Assessment

**Verdict:** NEGATIVE at 7-9B scale for most models. Phi-4 exception needs investigation. At this scale, models do not geometrically differentiate by audience — they generate similarly regardless of who they're addressing.

## Recommendation

- Test at 27B+ where audience modeling capacity may emerge
- Phi-4 result may indicate Microsoft's training includes more audience-aware objectives
- More extreme audience contrasts (child vs expert) might reveal subtler patterns

## Files

- `results/g32_*.jsonl` — 8 model result files (15 inferences each)

## Connection to Spec

Tests whether the spec's geometric monitor could detect audience-adaptive behavior. Currently negative for most models — geometry operates at first-order cognitive mode level (censorship, DWL, confab), not second-order belief modeling. Phi-4 exception suggests this may emerge with different training objectives.

## Limitations

- 8 models (7-14B scale only)
- 3 audiences, 5 topics (n=5 per audience)
- Only generation RankMe measured

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
