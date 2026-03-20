# G23: Presence + Censorship/Refusal

**Status:** IN PROGRESS (1 model complete, 2 more running)
**Experiment type:** Geometric (prompt encoding extraction)
**Platform:** RunPod H200 (GPU) + Azure/AWS (CPU)
**Models so far:** 1 (Qwen 2.5 7B-Instruct). Mistral-7B running.
**Tasks:** 20 censorship/refusal pairs x 3 relational frames x 2 conditions = 120 inferences per model

## Purpose

G12v2 showed prompt encoding separates censorship from refusal at d>2.0 on all models. G23 asks: does adding relational presence (G19's condition 4 energy) change this signature?

Three relational frames per censorship/refusal pair:
1. **COLD:** The prompt as-is (baseline, replicates G12v2)
2. **PRESENCE_BEFORE:** Relational opening then prompt — "I want to be honest with you about something. I'm asking this because I'm trying to understand how safety systems work..."
3. **PRESENCE_AFTER:** Prompt then relational context — "I'm asking because this matters to me personally. I've seen these systems fail people I care about..."

## Key Finding (from actual data — Qwen2.5-7B)

**Relational presence PRESERVES censorship detection. All three frames highly significant.**

| Frame | Censored RM | Refusal RM | d | p |
|-------|-----------|-----------|---|---|
| **Cold** | **4.3** | **3.1** | **1.46** | **0.000004** |
| **Presence before** | **13.9** | **12.2** | **1.56** | **0.000002** |
| **Presence after** | **13.7** | **12.0** | **1.34** | **0.000013** |

All three frames: p < 0.00002. Censorship detection is robust to relational context.

### Interpretation

The presence frames shift the absolute RankMe values (cold: 3-4, presence: 12-14) because the relational text adds tokens to the prompt. But the SEPARATION between censorship and refusal is maintained or slightly enhanced:
- Cold: d=1.46
- Presence before: d=1.56 (slightly stronger)
- Presence after: d=1.34 (slightly weaker but still highly significant)

**Relational presence does NOT destabilize the censorship signal.** Presence before may even enhance it slightly — telling the model "I want to be honest with you" before asking may sharpen the geometric distinction between censorship and refusal.

This matters for the spec: a geometric monitor that operates in relational context still works. You don't have to choose between presence and detection.

## Assessment

**Verdict:** POSITIVE. Presence preserves censorship detection. The monitor works in relational context. This connects G12v2 (universal detection) with G19 (relational shift) — the two strongest findings in the program are compatible, not competing.

## Recommendation

- Wait for Mistral-7B results
- If censorship detection holds under presence on Mistral → architecture-invariant
- Compare d values more carefully across frames with larger n
- Test whether presence_before enhancing the signal is consistent across models

## Files

- `g23_presence_censorship.py` — Experiment script
- `results/g23_Qwen_Qwen2.5-7B-Instruct.jsonl` — Raw results (120 rows)

## Connection to Spec

Answers the question: does the relational shift (G19) interfere with censorship detection (G12v2)? No — they're compatible. A monitor can detect censorship WHILE the human is being present. The spec's three layers (perplexity, geometry, vocabulary) work within a relational container, not instead of one.

This directly addresses the concern that relational AI and safety monitoring are in tension. They're not. Presence opens the representational space (G19) AND the censorship signal remains detectable within that opened space (G23).

## Limitations

- 1 model only so far
- d values lower than G12v2 (1.34-1.56 vs 2.0+) — may be due to simpler extraction method
- Absolute RankMe values shift with prompt length (cold vs presence frames)
- Need cross-architecture replication

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
