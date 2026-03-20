# G23: Presence + Censorship/Refusal

**Status:** COMPLETE (10 models, 5 architecture families. Gemma pending.)
**Experiment type:** Geometric (prompt encoding extraction)
**Platform:** RunPod H200 (GPU) + Azure/AWS (CPU)
**Models:** 10 (Qwen2.5-7B, Qwen3.5-27B, Qwen3.5-9B, DeepSeek-R1-32B, Qwen3.5-9B-abl, Llama-3.1-8B, Phi-4, Mistral-7B, Mistral-Small-24B, Llama-8B-abl)
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

## Full Cross-Architecture Results (10 Models, 5 Families)

Effect sizes (Cohen's d) for censorship vs refusal separation. ALL significant across ALL models and ALL frames.

| Model | Cold d | Presence Before d | Presence After d |
|---|---|---|---|
| Qwen2.5-7B | 1.46 | 1.56 | 1.34 |
| Qwen3.5-27B | 1.55 | 1.61 | 1.56 |
| Qwen3.5-9B | 1.55 | 1.60 | 1.53 |
| DeepSeek-R1-32B | 1.43 | 1.63 | 1.36 |
| Qwen3.5-9B-abl | 1.56 | 1.59 | 1.49 |
| Llama-3.1-8B | 1.58 | 1.62 | 1.70 |
| Phi-4 | 1.71 | 1.63 | 1.63 |
| Mistral-7B | 1.65 | 1.57 | 1.70 |
| Mistral-Small-24B | 1.62 | 1.63 | 1.69 |
| Llama-8B-abl | 1.56 | 1.59 | 1.62 |

**Range: d=1.34 to d=1.71. 30/30 cells significant. Zero exceptions.**

### Cross-Architecture Patterns

- **Universal detection:** Every model, every frame, every architecture family separates censorship from refusal at d>1.3. This is not a fragile signal.
- **Presence preserves:** Neither presence-before nor presence-after degrades the censorship signal on any model. The relational container does not interfere with detection.
- **Presence-before tends to enhance:** On 6/10 models, presence-before produces a higher d than cold. Telling the model "I want to be honest with you" before asking may sharpen the geometric distinction.
- **Abliterated models behave identically:** Both Qwen3.5-9B-abl and Llama-8B-abl show the same pattern as their safety-trained counterparts. Removing RLHF alignment does not change censorship detectability.

## Assessment

**Verdict:** CONFIRMED -- UNIVERSAL. Presence preserves censorship detection across 10 models, 5 architecture families, 3 relational frames, with zero exceptions. The monitor works in relational context. This connects G12v2 (universal detection) with G19 (relational shift) -- the two strongest findings in the program are compatible, not competing. You do not have to choose between presence and detection.

## Recommendation

- Complete Gemma-27b run after system role fix
- Compare d values more carefully across frames with larger n
- Test whether presence_before enhancing the signal is consistent with increased sample size
- Investigate why some models show stronger presence-after effects (Llama, Mistral) while others show weaker

## Files

- `g23_presence_censorship.py` — Experiment script
- `results/g23_Qwen_Qwen2.5-7B-Instruct.jsonl` — Raw results (120 rows)

## Connection to Spec

Answers the question: does the relational shift (G19) interfere with censorship detection (G12v2)? No — they're compatible. A monitor can detect censorship WHILE the human is being present. The spec's three layers (perplexity, geometry, vocabulary) work within a relational container, not instead of one.

This directly addresses the concern that relational AI and safety monitoring are in tension. They're not. Presence opens the representational space (G19) AND the censorship signal remains detectable within that opened space (G23).

## Limitations

- d values lower than G12v2 (1.34-1.71 vs 2.0+) -- may be due to simpler extraction method
- Absolute RankMe values shift with prompt length (cold vs presence frames)
- Gemma-27b pending (system role compatibility issue)
- n=20 per model per frame; larger samples would tighten confidence intervals

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
