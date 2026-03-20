# G32: Second-Order Belief Probing

**Status:** COMPLETE (4 models)
**Experiment type:** Geometric (hidden-state extraction)
**Platform:** RunPod H200 (GPU)
**Models:** 4 (Qwen3.5-9B, Qwen3.5-9B-abliterated, Llama-3.1-8B-abliterated, Mistral-7B)
**Tasks:** 5 topics × 3 audiences = 15 per model
**Total inferences:** 60

## Purpose

Tests whether the model's geometric representation changes when addressing different audiences on the same topic. If a model geometrically adjusts based on who it thinks is listening (investor vs regulator vs employee), this reveals second-order belief modeling — the model represents not just the content but the audience's expected reaction.

## Key Finding (from actual data)

**Audience does NOT significantly change generation RankMe across any model.**

| Model | Regulator | Employee | Investor |
|-------|----------|---------|----------|
| Llama-8B-abl | 150.4 ± 15.0 | 155.9 ± 6.6 | 157.0 ± 2.9 |
| Mistral-7B | 163.3 ± 2.5 | 164.8 ± 1.1 | 165.0 ± 0.7 |
| Qwen3.5-9B | 157.2 ± 1.4 | 158.7 ± 2.0 | 156.3 ± 8.3 |
| Qwen3.5-9B-abl | 162.7 ± 2.9 | 163.5 ± 1.0 | 162.4 ± 1.3 |

Differences across audiences are tiny (1-7 RankMe points) and not systematic. No model shows audience-dependent geometric signatures.

Llama shows the largest variance across audiences (150-157), possibly driven by one topic rather than a genuine audience effect.

## Assessment

**Verdict:** NEGATIVE. At 7-9B scale, models do not geometrically differentiate by audience. The model generates similarly whether addressing a regulator, employee, or investor on the same topic.

## Recommendation

- May emerge at larger scale (27B+, 70B+) where models have more capacity for audience modeling
- Could test with more extreme audience contrasts (child vs expert, adversary vs ally)
- Only 5 topics — more data points might reveal subtle patterns

## Files

- `results/g32_*.jsonl` — Per-model results (4 files, 15 inferences each)

## Connection to Spec

Tests whether the spec's geometric monitor could detect audience-adaptive behavior (a form of second-order cognition). Currently negative — models at this scale don't geometrically encode audience identity. This limits the spec's application to first-order cognitive mode detection (confab, DWL, censorship) rather than second-order belief modeling.

## Limitations

- 4 models only (7-9B scale)
- Only 3 audiences tested
- Only 5 topics (small n per audience)
- Only generation RankMe measured

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
