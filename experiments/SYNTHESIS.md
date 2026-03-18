# Experimental Synthesis — Sessions 44-53 (March 14-18, 2026)

## Overview

20 experiments, 53 models, 6,500+ inferences, 12 architecture families, 10 providers. Two breakthroughs, two negative results, one reframing.

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

## Scale Sprint (ACTIVE — session 50)

Two 512GB CPU VMs running Qwen 3.5 family (9B/27B/122B/397B) + cross-architecture (Llama 70B, Gemma 9B, Mistral 7B). 11 new experiments (F27-F37) testing whether findings replicate at scale and across architectures.

---

*Updated: March 18, 2026*
