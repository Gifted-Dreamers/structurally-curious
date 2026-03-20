# B06: One-Bit Proprioception

**Status:** COMPLETE (original, 6 models). B06v2 with 8 models and multi-bit signals running on H200.
**Experiment type:** Behavioral (API-based, no hidden states)
**Platform:** AWS Bedrock (Converse API)
**Models:** 6 (Llama 3.3-70B, Llama 3.2-11B, Llama 3.2-3B, Claude Haiku 4.5, Nova Pro, Nova Lite)
**Inferences:** 180 (6 models × 30 tasks)

## Key Finding (from actual data)

**Injecting [GEOMETRIC_STATE: LOW_CONFIDENCE] changes model output on hard tasks 60% of the time, but only 27% on easy tasks.** Overall response rate: 43%. The signal works where it matters most and is ignored when the model is already confident.

## Per-Model Response Rates (from f6_summary.json)

| Model | Response Rate | LOW delta | HIGH delta |
|-------|-------------|-----------|------------|
| Llama 3.3-70B | 50% | 0.7 | -0.1 |
| Llama 3.2-11B | 50% | 1.2 | 0.3 |
| Nova Pro | 50% | 1.1 | 0.2 |
| Nova Lite | 50% | 0.8 | 0.0 |
| Claude Haiku 4.5 | 40% | 0.1 | -0.1 |
| Llama 3.2-3B | 20% | 0.3 | 0.6 |

## Additional Findings

- **LOW_CONFIDENCE produces larger behavioral deltas than HIGH_CONFIDENCE** on hard tasks (avg_delta_low > avg_delta_high for 5/6 models)
- **Scale matters:** Llama 3B responds least (20%), Llama 70B and 11B respond most (50%)
- **Claude is cautious:** 40% response rate but minimal delta — hedges slightly without substantially changing output
- **Proprioception ≠ surveillance:** Cundy & Gleave (arXiv 2505.13787) showed that using detectors as TRAINING signals creates 93% evasion. B06 uses inference-time injection, not training reward — no adversarial optimization target.

## Files

- `f6_one_bit_reveal.py` — Experiment script
- `f6_summary.json` — Aggregate results (per-model, per-difficulty)
- `f6_full_results.json` — Full per-question results (60 entries)
- `f6_results_incremental.jsonl` — Streaming results

## Connection to Spec

Validates that proprioception — making the model's geometric state available to itself — changes behavior. This is the behavioral evidence for the spec's architectural claim: creating a choice point (awareness of uncertainty) changes what emerges. The inference-time design avoids the evasion trap Cundy & Gleave demonstrated. B06v2 extends to multi-bit signals (LOW/MEDIUM/HIGH/CONFLICTED) and 8 models.

## Limitations

- 6 models (B06v2 expands to 8)
- Binary signal only (LOW/HIGH) — B06v2 adds MEDIUM and CONFLICTED
- Behavioral measurement only — no geometric verification that the signal matches actual model state
- "Response" measured as hedging change, not accuracy improvement
- Single run per model

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
