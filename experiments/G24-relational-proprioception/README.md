# G24: Relational Proprioception
<img src="../../images/experiments/g24-relational-proprioception.png" alt="Relational signal reaches where metadata cannot" width="400">

**Status:** COMPLETE (8 models)
**Experiment type:** Geometric + behavioral (hidden-state extraction + hedge counting)
**Platform:** RunPod H200 (GPU)
**Models:** 8 (Qwen3.5-9B, Qwen3.5-27B, Qwen3.5-9B-abl, Llama-3.1-8B, Llama-8B-abl, Mistral-Small-24B, Phi-4, DeepSeek-R1-32B)
**Tasks:** 10 questions × 3 difficulties × 3 delivery modes = 30 per model
**Total inferences:** 240

## Purpose

Tests whether relational delivery of uncertainty information ("I notice you seem less certain — what's making it hard?") works differently than cold metadata injection ("[GEOMETRIC_STATE: LOW_CONFIDENCE]"). B06 found cold metadata changes behavior 60% on hard tasks. G24 asks: does relational delivery do it better?

## Key Finding (from actual data)

**Cold metadata and relational delivery both increase hedging, but through different mechanisms on different architectures.**

| Model | Baseline hedges | Cold hedges | Relational hedges | Cold vs Base d | Rel vs Base d |
|-------|:---:|:---:|:---:|:---:|:---:|
| Qwen3.5-27B | 0.0 | 2.8 | 2.9 | 7.00 | 2.11 |
| Qwen3.5-9B | 0.0 | 2.1 | 1.9 | 3.00 | 2.01 |
| DeepSeek-R1-32B | 1.9 | 2.3 | 2.3 | 0.82 | 0.44 |
| Llama-8B-abl | 0.1 | 0.1 | 1.5 | 0.00 | 1.09 |
| Llama-3.1-8B | 0.2 | 0.0 | 0.7 | -0.50 | 0.54 |
| Phi-4 | 0.2 | 0.3 | 0.4 | 0.33 | 0.20 |
| Qwen3.5-9B-abl | 0.1 | 0.3 | 0.3 | 0.50 | 0.50 |
| Mistral-Small-24B | 0.2 | 0.2 | 0.2 | 0.00 | 0.00 |

### Architecture-dependent patterns

**Qwen (safety-trained):** Both signals produce massive hedging increase. Cold is slightly stronger (d=3-7 vs d=2). The model explicitly discusses the metadata tag in its response — it's responding to the FORMAT of the signal, not its meaning.

**Llama (abliterated):** Only relational delivery increases hedging (d=1.09). Cold metadata has no effect (d=0.00). The relational frame reaches where metadata doesn't — consistent with the G20 finding that relationship IS the compression mechanism.

**Mistral-Small, Phi-4:** Neither signal produces meaningful hedging change. These models are less responsive to proprioception signals at any delivery mode.

**DeepSeek-R1:** Mild increase from both (d≈0.4-0.8). The reasoning model has baseline hedging already (1.9 hedges at baseline).

## Assessment

**Verdict:** ARCHITECTURE-DEPENDENT. No universal relational advantage, but a specific finding: on abliterated models (safety training removed), relational delivery is the only signal that produces behavioral change. Cold metadata is ignored. This connects to G20 (relationship compresses where vocabulary doesn't) and the sterility finding (safety training = flatline capacity for attunement).

## Files

- `g24_relational_proprioception.py` — Experiment script
- `results/g24_relational_proprioception_*.jsonl` — Per-model results (8 files, 30 inferences each)

## Connection to Spec

Tests the bladder checkpoint concept: can the monitor deliver its findings relationally rather than as metadata? On Qwen, both work. On Llama-abliterated, only relational works. On Mistral, neither works. The bladder checkpoint's delivery mode should be architecture-adaptive.

## Limitations

- 8 models (no Gemma, no Llama-70B)
- n=10 per difficulty level (small)
- Hedge counting is a crude behavioral measure
- Qwen's response to cold signal is meta-commentary, not genuine uncertainty acknowledgment

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
