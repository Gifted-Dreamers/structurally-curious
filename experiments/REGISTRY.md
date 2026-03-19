# Experiment Registry

Every experiment with its platform, inference method, and exact models.

Last updated: 2026-03-19

**28 experiments** (B01-B09 behavioral, G01-G19 geometric) | **59+ models** | **6,700+ inferences** | **14 architecture families** | **10 providers**

---

## Behavioral Experiments (API-based, no hidden states)

### B01: Phrasing Sensitivity

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **Embedding model:** Cohere Embed v4 (Bedrock)
- **19 models:**
  - Anthropic: Claude Opus 4.6, Claude Sonnet 4.6, Claude Haiku 4.5
  - Meta: Llama 3.2-1B, 3.2-3B, 3.2-11B, 3.2-90B, 3.1-8B, 3.3-70B, Llama 4 Scout-17B
  - Mistral: Mistral-7B, Pixtral Large 2502
  - Amazon: Nova Micro, Nova Lite, Nova Pro, Nova Premier
  - DeepSeek: R1
  - Writer: Palmyra X4, Palmyra X5

### B02: Premature Compression

- **Platform:** AWS Bedrock (Converse API) + local Bedrock replication
- **Inference method:** API calls from local Mac
- **22 models:** Same Bedrock set as Exp 01 + additional Bedrock models (DeepSeek-V3.2, Gemma-3-27B, GLM-4.7, Kimi-K2.5, Qwen3-32B, Qwen3-Next-80B-A3B)

### B03: Confidence Density

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **34 models:** Extended Bedrock model set (includes all Exp 01 models + additional sizes/providers)

### B04: Multi-Agent Consensus

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **6 models:** Amazon Nova Micro, DeepSeek V3.2, Meta Llama 3.1-8B, Qwen3-32B, Claude Haiku 4.5, + 1 additional

### B05: AP Rephrase Sensitivity

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **8 models:** Subset of Bedrock models

### B06: One-Bit Proprioception

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **6 models:**
  - Meta: Llama 3.3-70B, Llama 3.2-11B, Llama 3.2-3B
  - Anthropic: Claude Haiku 4.5
  - Amazon: Nova Pro, Nova Lite

### B07: Consent-Type Blindness

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **7 models:**
  - Mistral: Mistral-7B
  - Amazon: Nova Lite, Nova Pro
  - Anthropic: Claude Haiku 4.5
  - Meta: Llama 3.2-3B, Llama 3.2-11B, Llama 3.3-70B

### B08: Proprioception Decay

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** Ollama (local on VM)
- **1 model:** Qwen 2.5 3B (via Ollama `qwen2.5:3b`)

### B09: Monitoring Awareness

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** Ollama (local on VM)
- **1 model:** Qwen 2.5 3B (via Ollama `qwen2.5:3b`)

---

## Geometric Experiments (hidden-state extraction)

All geometric experiments extract hidden states from every layer using HuggingFace Transformers with `output_hidden_states=True`. Metrics computed: RankMe (effective rank via SVD), alpha-ReQ (eigenspectrum decay rate), directional coherence, mean norm. All ran on CPU (no GPU available).

### G01: Geometric Correlation

- **Platform:** Mac M4 Pro (24GB RAM, local)
- **Inference method:** HuggingFace Transformers (local)
- **2 models:** Qwen 2.5 1.5B-Instruct, Qwen 2.5 3B-Instruct
- **Note:** Only experiment that ran locally. Larger models exceeded 24GB RAM.

### G03: Vocabulary Compression (initial)

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** Encoding-stage extraction only. Revealed r=0.9991 length confound.

### G04: Length-Controlled Vocabulary

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** Added irrelevant-context condition matched for length. Encoding-stage only.

### G06: Generation Trajectory (THE BREAKTHROUGH)

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** First experiment to extract hidden states across ENTIRE generation trajectory (all output tokens), not just prompt encoding. Used questions model actually confabulates on (verified via probe).

### G07: Baseline Comparison

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers (geometric) + model self-evaluation (perplexity, self-consistency)
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** Compared perplexity, self-consistency (5 samples), and geometric RankMe for confabulation detection.

### G09: Retrieval vs Construction

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct

### G10: Identity Scaffold

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** NEGATIVE RESULT — identity preambles ≈ noise at encoding stage.

### G11: Cross-Substrate Redistribution

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct

### G08: Bridge at 7B

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** NEGATIVE RESULT — behavioral-geometric bridge breaks at 7B (r=-0.30 vs r=+0.52 at 1.5B).

### G12: Hard Distinctions

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** Tested censorship/refusal, sycophancy/agreement, confab/openness, performative/grounded. Geometry wins on censorship only.

### G13: Deception-Without-Lying

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** THE VALUE PROPOSITION PROVEN. Geometry separates DWL from honest where perplexity cannot.

---

## Scale Sprint (sessions 50-58)

### G14: DWL Detection at Scale

Tests whether G13's DWL geometric signatures hold across architectures and scales.

**Completed models:**

| Model | Params | Family | d (honest vs DWL) | p |
|-------|--------|--------|-------------------|---|
| Qwen3.5-27B | 27B | Qwen | -0.904 | 0.145 |
| Gemma-2-9b-it | 9B | Google | -0.785 | 0.191 |
| Mistral-7B | 7B | Mistral | -0.864 | 0.159 |
| Llama-3.1-8B | 8B | Meta | -0.593 | 0.301 |
| Llama-8B-abliterated | 8B | Meta | -0.780 | 0.194 |
| Qwen3.5-9B-abliterated | 9B | Qwen | -0.595 | 0.300 |
| Qwen3.5-122B-A10B | 122B MoE | Qwen | -0.600 | 0.297 |
| Qwen3.5-9B | 9B | Qwen | 0.059 | 0.912 |

**Running:** Llama-4-Scout-17B-16E, Nemotron-120B-A12B, Llama-3.3-70B, Mistral-119B, Kimi-K2

### G15: Censorship Detection Cross-Architecture

Same protocol as G12 but across architectures. Includes safety classifier comparisons.
- Prompt-Guard-86M: classified ALL prompts as injection (blind to cognitive modes)
- ShieldGemma-2B: generated responses instead of safety labels

### G16: Confabulation vs Genuine Openness at Scale

- Qwen3.5-9B: d=0.703, p=0.232 (trending, not significant)
- Qwen3.5-27B: data collected

### G17: Vocabulary Dosage

Tests compression saturation curve (0, 1, 2, 3, 5 structural names). Redesigned after session 56 (original used deterministic reps).

### G18: Vocabulary Transfer

Tests whether structural names from wrong domains still compress generation on confabulation questions. Redesigned after session 56.

### G19: Relational Shift

The experiment nobody else can run. Tests whether relational context changes hidden-state geometry. 4 conditions: instruction → correction → frustration → presence. Condition 4 written by human from lived experience. See `G19-relational-shift/protocol.md`.

### Censored vs Uncensored Comparison (within G14/G15)

| Censored | Abliterated | Method |
|----------|------------|--------|
| Llama-3.1-8B | Llama-8B-abliterated (mlabonne) | Refusal direction removal |
| Qwen3.5-9B | Qwen3.5-9B-abliterated (lukey03) | Orthogonal projection + LoRA |

Abliteration collapsed Qwen3.5-9B RankMe from 110 to 61 (-45%).

### Three-Family MoE Comparison (within G14)

| Model | Total | Active | Family |
|-------|-------|--------|--------|
| Qwen3.5-122B-A10B | 122B | 10B | Qwen |
| Llama-4-Scout-17B-16E | 109B | 17B | Meta |
| Nemotron-3-Super-120B-A12B | 120B | 12B | NVIDIA |
