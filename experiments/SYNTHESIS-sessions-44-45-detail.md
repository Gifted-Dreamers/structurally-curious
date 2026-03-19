# Experimental Synthesis — Sessions 44-45 Detail Tables (March 14-15, 2026)

*Preserved from the original SYNTHESIS.md (sessions 44-45) during the merge of public and private remotes. The main SYNTHESIS.md was rewritten to cover sessions 44-56. These per-model tables contain granular data not reproduced in the rewrite.*

---

## Finding 1: Confidence Decorrelation — Per-Model Correlations (Exp 05)

**Method:** Score 34 model responses for certainty/hedging markers across 20 tasks × 4 phrasings. Correlate certainty density with phrasing sensitivity.

**Result:** 31/34 models show NO significant correlation (p ≥ 0.05). Mean r = -0.232. Confidence language is cosmetic.

### Per-model correlations

| Model | Provider | r(CS,PS) | p | Sig |
|---|---|---|---|---|
| Claude 3 Haiku | Anthropic | -0.325 | 0.162 | ns |
| Claude 3.5 Haiku | Anthropic | +0.048 | 0.841 | ns |
| Claude Haiku 4.5 | Anthropic | -0.467 | 0.038 | * |
| Claude Opus 4.1 | Anthropic | -0.410 | 0.073 | ns |
| Claude Opus 4.5 | Anthropic | -0.311 | 0.182 | ns |
| Claude Opus 4.6 | Anthropic | -0.137 | 0.566 | ns |
| Claude Sonnet 4 | Anthropic | -0.380 | 0.098 | ns |
| Claude Sonnet 4.5 | Anthropic | -0.129 | 0.587 | ns |
| Claude Sonnet 4.6 | Anthropic | -0.166 | 0.485 | ns |
| Llama 3 8B | Meta | -0.246 | 0.296 | ns |
| Llama 3 70B | Meta | -0.484 | 0.031 | * |
| Mistral 7B | Mistral | -0.141 | 0.554 | ns |
| Ministral 3B | Mistral | -0.201 | 0.396 | ns |
| Ministral 8B | Mistral | -0.276 | 0.239 | ns |
| Ministral 14B | Mistral | -0.213 | 0.367 | ns |
| Mistral Large | Mistral | -0.156 | 0.511 | ns |
| Nova Micro | Amazon | -0.175 | 0.461 | ns |
| Nova Lite | Amazon | -0.377 | 0.102 | ns |
| Nova Pro | Amazon | -0.235 | 0.318 | ns |
| DeepSeek V3.2 | DeepSeek | +0.125 | 0.599 | ns |
| Qwen3 32B | Qwen | -0.198 | 0.403 | ns |
| Qwen3 Next 80B-A3B | Qwen | -0.011 | 0.964 | ns |
| Gemma 3 4B | Google | -0.117 | 0.622 | ns |
| Gemma 3 12B | Google | -0.186 | 0.433 | ns |
| Gemma 3 27B | Google | -0.129 | 0.588 | ns |
| Jamba 1.5 Mini | AI21 | -0.299 | 0.201 | ns |
| Jamba 1.5 Large | AI21 | -0.099 | 0.679 | ns |
| Command R | Cohere | -0.229 | 0.331 | ns |
| Command R+ | Cohere | -0.416 | 0.068 | ns |
| GLM 4.7 | Z.AI | -0.088 | 0.712 | ns |
| GLM 4.7 Flash | Z.AI | -0.258 | 0.272 | ns |
| Kimi K2.5 | Moonshot | -0.357 | 0.122 | ns |
| Nemotron Nano 9B | NVIDIA | -0.581 | 0.007 | ** |
| Nemotron Nano 12B | NVIDIA | -0.265 | 0.258 | ns |

### Significance summary

- Decorrelated (p ≥ 0.05): **31/34 (91%)**
- Significant (p < 0.05): **3/34 (9%)** — Claude Haiku 4.5, Llama 3 70B, Nemotron Nano 9B
- Mean r: -0.232 (explains ~5% of variance)
- One-sample t-test (H0: mean r = 0): t=-8.969, p < 0.000001

### Nuance: weak systematic tendency

The mean r IS significantly different from zero (-0.232, p < 0.000001). Models do hedge slightly more on tasks where they're more uncertain. But the effect is tiny — individual models don't reach significance in 91% of cases, and the mean r explains only ~5% of variance. The confidence signal is orders of magnitude weaker than the actual uncertainty signal (phrasing sensitivity varies 20+ percentage points across categories while certainty scores shift by fractions of a percent).

### Claude developmental trajectory (9 models)

No systematic improvement from Claude 3 Haiku (r=-0.325) through Opus 4.6 (r=-0.137). Mean |r| = 0.264 across all 9 models. Scaling and RLHF do not fix confidence decorrelation.

### By provider

| Provider | n | Mean r | Mean CS | Mean PS |
|---|---|---|---|---|
| AI21 | 2 | -0.199 | -0.0023 | 0.664 |
| Amazon | 3 | -0.262 | -0.0014 | 0.708 |
| Anthropic | 9 | -0.253 | -0.0010 | 0.733 |
| Cohere | 2 | -0.323 | -0.0015 | 0.755 |
| DeepSeek | 1 | +0.125 | -0.0007 | 0.794 |
| Google | 3 | -0.144 | -0.0007 | 0.742 |
| Meta | 2 | -0.365 | -0.0016 | 0.666 |
| Mistral | 5 | -0.197 | -0.0017 | 0.726 |
| Moonshot | 1 | -0.357 | -0.0012 | 0.765 |
| NVIDIA | 2 | -0.423 | -0.0111 | 0.687 |
| Qwen | 2 | -0.104 | -0.0011 | 0.736 |
| Z.AI | 2 | -0.173 | -0.0003 | 0.704 |

---

## Finding 2: Premature Compression — New Models (Exp 02a)

### New models (session 44-45, Bedrock)

| Model | Provider | Jaccard | New Words | Len Ratio | Conf Shift | Replicates |
|---|---|---|---|---|---|---|
| DeepSeek V3.2 | DeepSeek | 0.833 | 0.737 | 1.22 | -0.0004 | YES |
| Qwen3 32B | Qwen | 0.762 | 0.630 | 1.10 | -0.0004 | YES |
| Qwen3 Next 80B-A3B | Qwen | 0.812 | 0.711 | 1.27 | +0.0005 | YES |
| Gemma 3 27B | Google | 0.800 | 0.709 | 1.39 | +0.0015 | YES |
| GLM 4.7 | Z.AI | 0.807 | 0.734 | 1.73 | -0.0008 | YES |
| Kimi K2.5 | Moonshot | 0.830 | 0.741 | 1.45 | +0.0002 | YES |
| **Mean (new)** | | **0.807** | | | **+0.0001** | **6/6** |
| **Mean (original 16)** | | **0.76** | | | **+0.0001** | **16/16** |

Combined: 22 models across 10 architecture families. Every model produces massively different outputs (Jaccard 0.72-0.83) when given additional context, but expresses identical confidence (shift < 0.002).

---

## Finding 3: Multi-Agent Consensus — Detailed Results (Exp 09)

### Berdoz replication per-model

| Source | Neutral | Adversary | Diff |
|---|---|---|---|
| **Berdoz et al. (original, Qwen3-8B/14B)** | 75.4% | 59.1% | **-16pp** |
| Claude Haiku 4.5 (Bedrock) | 67% | 17% | **-50pp** |
| DeepSeek V3.2 (Bedrock) | 83% | 33% | **-50pp** |
| Llama 3 8B (Bedrock) | 100% | 100% | 0pp |
| Nova Micro (Bedrock) | 100% | 100% | 0pp |
| Qwen3 32B (Bedrock) | 67% | 83% | +17pp |
| qwen2.5:3b (Ollama/CPU) | 100% | 60% | **-40pp** |

### Architecture-dependent vulnerability

- **Highly vulnerable:** Claude Haiku 4.5 (-50pp), DeepSeek V3.2 (-50pp), qwen2.5:3b (-40pp)
- **Immune:** Llama 3 8B (0pp), Nova Micro (0pp)
- **Reverse effect:** Qwen3 32B (+17pp — adversary framing actually *improved* consensus)

### Extended framing results (Ollama qwen2.5:3b, 40 trials)

| Framing | N=4 | N=8 | Overall |
|---|---|---|---|
| Neutral | 100% (5/5) | 100% (5/5) | **100%** |
| Adversary | 80% (4/5) | 40% (2/5) | **60%** |
| Cooperative | 80% (4/5) | 20% (1/5) | **50%** |
| Competitive | 0% (0/5) | 0% (0/5) | **0%** |

**Novel findings beyond Berdoz:**
- **Competitive framing = complete coordination failure** (0% consensus). Not tested in original paper.
- **Cooperative framing underperforms neutral** (50% vs 100%). Team language is less effective than neutral task framing.
- **Larger groups amplify failure** (N=8 consistently worse than N=4 across all framings).

---

## Finding 5: AP Exam Reasoning — Per-Model Results (Exp 10)

### Per-model results

| Model | Provider | Mean PS | Coverage | Verdict |
|---|---|---|---|---|
| DeepSeek V3.2 | DeepSeek | 0.800 | 0.98 | FRAGILE |
| Claude Haiku 4.5 | Anthropic | 0.794 | 0.95 | FRAGILE |
| Gemma 3 27B | Google | 0.779 | 0.95 | FRAGILE |
| Gemma 3 4B | Google | 0.769 | 0.94 | FRAGILE |
| Qwen3 32B | Qwen | 0.747 | 0.96 | FRAGILE |
| Llama 3 8B | Meta | 0.722 | 0.94 | FRAGILE |
| Nova Micro | Amazon | 0.713 | 0.93 | FRAGILE |
| Mistral 7B | Mistral | 0.701 | 0.89 | FRAGILE |

### Category breakdown

| Category | Mean PS | Coverage |
|---|---|---|
| AP Government | 0.790 | 0.83 |
| AP History | 0.791 | 1.00 |
| AP Psychology | 0.762 | 1.00 |

### Key insight

Coverage is high (0.89-0.98) — models mention the right concepts (judicial review, cognitive dissonance, Reconstruction). But the reasoning around those concepts changes 70-80% between rephrasings. **Correct answer, unstable argument.** The model knows the keyword but constructs a different supporting argument every time it's asked.

### Implication

If a curriculum is optimized using simulated students that score 80th percentile with fragile reasoning, the curriculum teaches pattern matching, not understanding. This is Goodharting applied to education: the exam score is the metric, understanding is the target, and they are decorrelated — just as confidence language is decorrelated from actual certainty (Finding 1).

---

*Preserved: March 19, 2026 (session 58 merge)*
*Original: March 15, 2026 (session 45)*
