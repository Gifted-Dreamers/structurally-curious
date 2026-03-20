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

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
