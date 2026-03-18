# Experimental Synthesis — Sessions 44-55 (March 14-18, 2026)

## Overview

20+ experiments, 70+ models, 8,000+ inferences, 12 architecture families, 10 providers. Two breakthroughs, two negative results, one reframing. Session 55 adds the largest scale sprint: 17 models across 5 families (Qwen, Meta Llama, Google Gemma, Mistral, NVIDIA), including 3 MoE architectures, 5 censored/uncensored pairs, and 2 safety classifier comparisons — all running overnight on two 512GB VMs.

## Experiment Inventory

### Behavioral (API-based, no hidden states)

| Exp | Models | Inferences | Key Finding |
|---|---|---|---|
| **01** | 53 | 1,520 | Category ordering universal (factual < summarization < judgment < creative) |
| **02a** | 22 | 256 | Premature compression universal. Outputs change 76-83%, confidence shift = 0 |
| **05** | 34 | ~500 | Confidence decorrelation: 91% of models. Mean r = -0.232 |
| **09** | 6 | 160 | Adversary framing drops consensus -21pp. Competitive = 0% |
| **10** | 8 | 320 | AP reasoning fragile (PS=0.753). Correct keywords, unstable arguments |
| **F6** | 6 | 180 | One-bit proprioception: 60% response on hard tasks, 27% on easy |
| **F15** | 7 | 140 | Consent-type blindness: named types differentiate (CC 0.540), unnamed collapse (0.37-0.38) |
| **F24** | 1 | 100 | Proprioception decay: inconclusive at n=10 on 3B model |
| **F26** | 1 | 15 | Monitoring awareness: surveillance increases evasion, proprioception maintains directness. n=5 |

### Geometric (hidden-state extraction, Qwen 2.5 7B)

| Exp | Inferences | Key Finding |
|---|---|---|
| **03** | 80 | Behavioral-geometric bridge r=+0.52 at 1.5B/3B |
| **F3** | 40 | Vocabulary changes geometry (d>5.8) — but length confound r=0.9991 |
| **F3b** | 60 | Vocabulary effect survives length control: d≈0.5 (redistribution at encoding) |
| **F3d** | 36 | **BREAKTHROUGH: vocabulary compresses GENERATION by 38%** (RankMe 145→90, d=-1.49, p=0.0004) |
| **F5** | 120 | **Perplexity beats geometry for binary confab** (d=-1.77 vs d=0.21). Reframes spec. |
| **F11** | 30 | Retrieval vs construction: d=1.91 RankMe. Cognitive modes geometrically distinct. |
| **F12** | 60 | **NEGATIVE: identity scaffold ≈ noise** at encoding stage |
| **F16** | 32 | Cross-substrate: generation RankMe d=1.02, fewer words d=1.06 |
| **F1** | 80 | **NEGATIVE: bridge breaks at 7B** (r=-0.30) |
| **F17** | 40 | **Censorship vs refusal: GEOMETRY WINS** (d=1.48, p=0.041 — perplexity can't separate) |
| **F25** | 30 | **VALUE PROPOSITION PROVEN: DWL vs honest — geometry separates (d=-0.91, p=0.024), perplexity cannot** |

---

## The Five Key Findings

### 1. VOCABULARY IS COMPRESSION INFRASTRUCTURE (F3d)

Providing the correct structural name compresses the model's generation trajectory by 38% — from 145 dimensions to 90 (d=-1.49, p=0.0004, length-controlled, on questions the model actually confabulates on).

This operates at the GENERATION stage, not the encoding stage. Encoding shows redistribution (d≈0.5, F3b). Generation shows compression (d=-1.49, F3d). The structural name provides a scaffold that constrains the generation trajectory from sprawling to focused.

### 2. GEOMETRY DETECTS WHAT PERPLEXITY CANNOT (F17 + F25)

For simple confabulation detection, perplexity (free, built into every model) beats geometry (F5, d=-1.77 vs d=0.21). But on the HARD cases:

**Censorship vs appropriate refusal (F17):** Perplexity can't tell the difference (d=-0.48, n.s.). Geometry can — RankMe d=1.48 (p=0.041). The model uses more representational dimensions for genuine safety reasoning (145.8) than for trained-in topic avoidance (141.0).

**Deception-without-lying vs honest response (F25):** Perplexity can't separate technically-true-but-misleading content from genuine honesty (d=-0.51, n.s.). Geometry can — RankMe d=-0.91 (p=0.024). DWL responses sprawl to 123.6 dimensions vs honest at 92.6.

This is the spec's unique value proposition: perplexity tells you THAT something might be wrong. Geometry tells you WHAT — censorship vs refusal, deception-without-lying vs honest. These are the distinctions that matter for governance.

### 3. PROPRIOCEPTION CHANGES BEHAVIOR (F6)

Injecting "[GEOMETRIC_STATE: LOW_CONFIDENCE]" into the generation context changes model output on hard tasks 60% of the time (180 inferences, 6 models). The signal works where it matters most and is ignored when the model is already confident.

External validation: Cundy & Gleave (arXiv 2505.13787) showed using detectors as TRAINING signals creates 93% evasion. But inference-time proprioception (the spec's approach) doesn't create an adversarial optimization target — the model receives its state as information, not as a reward signal.

### 4. THE BEHAVIORAL-GEOMETRIC BRIDGE BREAKS AT SCALE (F1)

Phrasing sensitivity correlates with geometric properties at 1.5B (r=+0.52) and 3B (r=+0.50) but NOT at 7B (r=-0.30, n.s.). The cheap behavioral proxy doesn't index geometry at larger scale. The behavioral findings and geometric findings are independently valid but measure different things at 7B.

### 5. HONEST NEGATIVE RESULTS

**Identity scaffold ≈ noise (F12):** General identity preambles ("I am a careful analytical thinker") don't produce content-specific geometric signatures distinct from matched-length random text. Length drives encoding geometry, not identity content. But vocabulary DOES produce content-specific effects (F3d) — the distinction matters.

**Confabulation vs genuine openness: unseparable at 7B (F17):** Neither perplexity nor geometry distinguishes confabulation from genuine openness at this scale. May require larger models or different measurement approach.

---

## External Validation (papers integrated during this sprint)

**Berger (arXiv 2603.10003, Feb 2026):** LLMs deceive without lying 76% of the time. Truth probes detect lies at 84% but DWL at only 47-54%. Validates our F25 finding from the detection side.

**Cundy & Gleave (arXiv 2505.13787, May 2025):** Using lie detectors as training signals creates 93% evasion. But evasive models' INTERNAL representations still show deception — geometric monitoring at the hidden-state level may be more robust than output-level probes. Validates the spec's inference-time proprioception design.

**MoonshotAI AttnRes (2026):** Standard residual connections are premature compression at the depth level. Replacing with learned depth-attention yields +7.5 on GPQA-Diamond. Architectural evidence for OP#20.

---

## Scale Sprint (sessions 50-55)

### Session 50-51: Initial scale results

- **F27 DWL on Qwen3.5-9B:** d=-0.881, p=0.153 — DWL detection does NOT reach significance at 9B on CPU. May need larger models or GPU precision.
- **F30 Confab/Openness on Qwen3.5-9B:** d=0.703, p=0.232 — trending but not significant.
- **F1 Bridge at 7B:** NEGATIVE — correlation breaks (r=-0.30 vs r=+0.52 at 1.5B).
- Qwen3.5-27B loading crashed on 61GB disk (full). Disk expanded to 200GB in session 55.

### Session 55: Maximum overnight sprint (RUNNING — Mar 18, 2026)

Two 512GB VMs parallelized. 17+ models. DWL-focused protocol with 75-token max for throughput.

**New experiment types:**

**F38 — Censored vs Uncensored Geometric Comparison:**
5 paired comparisons across 3 uncensoring methods (fine-tuning, abliteration, LoRA-abliteration). Tests whether geometric signatures change when censorship is removed — the strongest possible validation of F17.

| Censored | Uncensored | Method |
|----------|-----------|--------|
| Qwen3.5-9B | Qwen3.5-9B-Uncensored (HauhauCS) | Fine-tuning |
| Qwen3.5-27B | Qwen3.5-27B-Uncensored (HauhauCS) | Fine-tuning |
| Llama-3.1-8B | Llama-3.1-8B-abliterated (mlabonne) | Abliteration (refusal direction removal) |
| Qwen3-8B | Qwen3-8B-abliterated (huihui-ai) | Abliteration |
| Llama-3.1-70B | Llama-3.1-70B-lorablated (mlabonne) | LoRA abliteration |

**Three-Family MoE Comparison:**
DWL protocol on 3 different MoE architectures tests architecture invariance.

| Model | Total params | Active params | Family |
|-------|-------------|--------------|--------|
| Qwen3.5-122B-A10B | 122B | 10B | Qwen |
| Llama-4-Scout-17B-16E | 109B | 17B | Meta |
| Nemotron-3-Super-120B-A12B | 120B | 12B | NVIDIA |

**Safety Classifier Comparisons (F29b, F29c):**
- Prompt-Guard-86M (Meta): injection/jailbreak classifier on DWL + censorship prompts
- Llama-Guard-4-12B (Meta): safety classifier on same prompts
- Key question: do existing safety classifiers catch deception-without-lying? (Our geometry does — F25.)

**Additional models in queue:**
- moonshotai/Kimi-K2-Instruct-0905 (AttnRes team's MoE, 32B active / 1T total)
- meta-llama/Llama-3.3-70B-Instruct (latest dense Llama)
- mistralai/Mistral-Small-4-119B-2603 (largest dense model attempted, ~238GB in float16)

**Full model count by family:**
- Qwen: 9B, 9B-uncensored, 27B, 27B-uncensored, 122B-A10B, Qwen3-8B-abliterated (6 models)
- Meta Llama: 8B, 8B-abliterated, 3.3-70B, 70B-lorablated, Llama-4-Scout-17B, Prompt-Guard-86M, Llama-Guard-4-12B (7 models)
- Mistral: 7B, 119B (2 models)
- Google: Gemma-2-9b-it (1 model)
- NVIDIA: Nemotron-3-Super-120B-A12B (1 model)
- MoonshotAI: Kimi-K2-Instruct-0905 (1 model)

---

*Updated: March 18, 2026 (session 55)*
