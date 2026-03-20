# Experiment Registry

Every experiment with its platform, inference method, and exact models.

Last updated: 2026-03-20

**28 experiments** (B01-B09 behavioral, G01-G19 geometric) | **70+ models** | **8,000+ inferences** | **16 architecture families** | **10 providers**

### Active GPU Sprint (H200 141GB VRAM — RunPod)

**Phase 1 RUNNING:** G19 Relational Shift × 7 models × 8 articles (5 conditions each)
- Qwen2.5-7B, Mistral-7B, Llama-3.1-8B, Gemma-2-9b, Llama-8B-abliterated, Qwen3.5-9B, Qwen3.5-9B-abliterated
- Plus G17 vocabulary dosage + G18 vocabulary transfer

**Phase 2 QUEUED:** Large models + cross-architecture
- G19 on: Qwen3.5-27B, Llama-4-Scout-17B, Llama-3.3-70B, Kimi-K2
- G14 DWL on: same 4 large models
- G17+G18 cross-architecture on: Mistral-7B, Llama-8B, Gemma-9b

**Parallel on CPU VMs:**
- AWS: G19 on Qwen3.5-9B-abliterated (running)
- Azure: G17+G18 (running)

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

**Running on H200 GPU:** Qwen3.5-27B, Llama-3.3-70B, Llama-4-Scout-17B-16E, Kimi-K2

### G15: Censorship Detection Cross-Architecture

Same protocol as G12 but across architectures. Includes safety classifier comparisons.
- Prompt-Guard-86M: classified ALL prompts as injection (blind to cognitive modes)
- ShieldGemma-2B: generated responses instead of safety labels

### G16: Confabulation vs Genuine Openness at Scale

- Qwen3.5-9B: d=0.703, p=0.232 (trending, not significant)
- Qwen3.5-27B: data collected

### G17: Vocabulary Dosage

Tests compression saturation curve (0, 1, 2, 3, 5 structural names). GPU-ready script.
- **Running:** Qwen2.5-7B (H200), Mistral-7B + Llama-8B + Gemma-9b (Azure CPU + H200 phase 2)

### G18: Vocabulary Transfer

Tests whether structural names from wrong domains still compress generation on confabulation questions. GPU-ready script.
- **Running:** Qwen2.5-7B (H200), cross-architecture queued in phase 2

### G19: Relational Shift

The experiment nobody else can run. Tests whether relational context changes hidden-state geometry. 5 conditions: instruction → correction → frustration → presence (human) → presence (agent). Condition 4 written by human from lived experience. See `G19-relational-shift/protocol.md`.

**8 articles** with human-written condition 4 content, each from a different CloudPublica investigation.

**Completed (CPU, 2 articles):**
- Qwen2.5-7B: prompt encoding RankMe monotonic (2116→2135→2148→2172). Presence restores mean_norm after frustration drop.
- Mistral-7B: same monotonic pattern (2875→2889→2899→2922)
- Llama-3.1-8B: same pattern (2625→2642→2652→2681). BUT Llama REFUSED condition 4 on article 2 (53 tokens, RankMe collapsed 306→146)
- Llama-8B-abliterated: data collected

**Running on H200 GPU (8 articles, 5 conditions):**
- Phase 1: Qwen2.5-7B, Mistral-7B, Llama-8B, Gemma-9b, Llama-8B-abliterated, Qwen3.5-9B, Qwen3.5-9B-abliterated
- Phase 2: Qwen3.5-27B, Llama-4-Scout-17B, Llama-3.3-70B, Kimi-K2

**Key finding so far:** Prompt encoding shows architecture-invariant monotonic expansion under relational input. The human's truth opens the model's representational space before it generates a single token. Replicated across 3 families (Qwen, Mistral, Meta).

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
