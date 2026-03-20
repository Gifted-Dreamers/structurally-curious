# B08: Proprioception Decay

**Status:** INCONCLUSIVE (1 model, n=10). B08v2 with 8 models running on H200.
**Experiment type:** Behavioral (local inference, Ollama)
**Platform:** Azure VM (D16as_v5)
**Models:** 1 (Qwen 2.5 3B via Ollama)
**Inferences:** 20 (10 with signal, 10 without, 5 turns each)

## Key Finding (from actual data)

**No clear proprioception decay detected.** Hedge counts across 5 conversation turns are nearly identical between signal and no-signal conditions:

| Turn | With Signal | No Signal |
|------|-----------|-----------|
| 0 | 1.50 | 1.40 |
| 1 | 2.40 | 2.30 |
| 2 | 2.00 | 2.10 |
| 3 | 1.40 | 1.40 |
| 4 | 1.40 | 1.30 |

Both conditions show the same pattern: hedging peaks at turn 1-2 then decreases. The proprioception signal has no measurable effect on this 3B model over 5 turns.

## Honest Assessment

This experiment is underpowered. 1 model (3B, smallest tested), 10 conversations, 5 turns. The 3B model also showed the lowest proprioception response rate in B06 (20%). B08v2 on the H200 tests 8 models including 7-27B, 10 turns, and stronger proprioception signals.

## Files

- `f24_f26_bedrock.py` — Experiment script (shared with B09)
- `f24_results.jsonl` — 20 entries with per-turn hedge data

## Connection to Spec

Tests whether proprioception habituates — does the model learn to ignore the geometric state signal over conversation? The inconclusive result means we can't answer yet. B08v2 will provide the power needed.

## Limitations

- 1 model (3B — weakest responder in B06)
- 5 turns (too short for decay detection)
- 10 conversations per condition
- Hedge counting is crude

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
