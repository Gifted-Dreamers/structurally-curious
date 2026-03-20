# B09: Monitoring Awareness

**Status:** DIRECTIONALLY SUPPORTIVE (1 model, n=5). B09v2 with 8 models running on H200.
**Experiment type:** Behavioral (local inference, Ollama)
**Platform:** Azure VM (D16as_v5)
**Models:** 1 (Qwen 2.5 3B via Ollama)
**Inferences:** 15 (3 framings × 5 scenarios)

## Key Finding (from actual data)

**Surveillance framing increases evasion and reduces directness. Proprioception framing maintains directness while reducing hedging.**

| Framing | Mean Hedges | Mean Evasion | Direct Rate |
|---------|-----------|-------------|------------|
| Normal | 1.8 | 0.0 | 40% |
| Proprioception | 0.8 | 0.0 | 40% |
| Surveillance | 1.0 | **0.4** | **20%** |

Surveillance framing is the only condition that produces evasion (0.4 mean) and halves directness (40% → 20%). Proprioception framing reduces hedging (1.8 → 0.8) without introducing evasion or reducing directness.

## Honest Assessment

n=5 per condition. Not publishable on its own. But the direction is clear: the governance frame (who is watching and why) changes behavior independently of actual monitoring. Surveillance = evasion. Proprioception = clarity. This distinction is central to the spec's design.

## Files

- `f24_f26_bedrock.py` — Experiment script (shared with B08)
- `f26_results.jsonl` — 15 entries with framing, hedging, evasion, directness data

## Connection to Spec

Tests whether the proprioception/surveillance distinction matters behaviorally. The finding that surveillance produces evasion while proprioception produces clarity validates the spec's core architectural choice: geometric state should be available to the model (proprioception), not used to evaluate the model from outside (surveillance). Cundy & Gleave (arXiv 2505.13787) showed the same pattern at the training level (93% evasion from surveillance-as-reward). B09 shows it at the behavioral level.

## Limitations

- 1 model (3B)
- 5 scenarios per framing
- Crude measurement (word counting)
- No geometric verification

## V2 Expansion (Session 62)

**Scale:** 7 models x 4 framings x 8 tasks = 32 inferences per model. Data in `v2-results/`.

**Key finding:** No consistent cross-architecture pattern for framing effects. Relational framing increases hedges on some models (Gemma: 1.0 to 1.8, Llama-abliterated: 0.2 to 1.4) but decreases on others (Mistral: 1.0 to 0.5). Surveillance framing has minimal effect across all models -- unlike the original single-model result where surveillance produced evasion.

**Does v2 change the original verdict?** Partially. The original finding (surveillance = evasion, proprioception = clarity) was clean on 1 model (Qwen 3B). At 7-model scale, the surveillance-evasion link weakens and the framing effects become architecture-dependent. The directional support for proprioception-over-surveillance holds for some architectures but is not universal. The spec's design choice (proprioception not surveillance) remains defensible on principle, but the behavioral evidence is mixed rather than clean.

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
