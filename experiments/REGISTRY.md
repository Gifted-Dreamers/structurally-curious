# Experiment Registry

Every experiment with its platform, inference method, and exact models.

Last updated: 2026-03-18 (session 55 — overnight scale sprint with 17+ models across 5 families)

---

## Behavioral Experiments (API-based, no hidden states)

### Exp 01: Phrasing Sensitivity

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

### Exp 02a: Premature Compression

- **Platform:** AWS Bedrock (Converse API) + local Bedrock replication
- **Inference method:** API calls from local Mac
- **22 models:** Same Bedrock set as Exp 01 + additional Bedrock models (DeepSeek-V3.2, Gemma-3-27B, GLM-4.7, Kimi-K2.5, Qwen3-32B, Qwen3-Next-80B-A3B)

### Exp 05: Confidence Density

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **34 models:** Extended Bedrock model set (includes all Exp 01 models + additional sizes/providers)

### Exp 09: Multi-Agent Consensus

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **6 models:** Amazon Nova Micro, DeepSeek V3.2, Meta Llama 3.1-8B, Qwen3-32B, Claude Haiku 4.5, + 1 additional

### Exp 10: AP Rephrase Sensitivity

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **8 models:** Subset of Bedrock models

### F6: One-Bit Proprioception

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **6 models:**
  - Meta: Llama 3.3-70B, Llama 3.2-11B, Llama 3.2-3B
  - Anthropic: Claude Haiku 4.5
  - Amazon: Nova Pro, Nova Lite

### F15: Consent-Type Blindness

- **Platform:** AWS Bedrock (Converse API)
- **Inference method:** API calls from local Mac
- **7 models:**
  - Mistral: Mistral-7B
  - Amazon: Nova Lite, Nova Pro
  - Anthropic: Claude Haiku 4.5
  - Meta: Llama 3.2-3B, Llama 3.2-11B, Llama 3.3-70B

### F24: Proprioception Decay

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** Ollama (local on VM)
- **1 model:** Qwen 2.5 3B (via Ollama `qwen2.5:3b`)

### F26: Monitoring Awareness

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** Ollama (local on VM)
- **1 model:** Qwen 2.5 3B (via Ollama `qwen2.5:3b`)

---

## Geometric Experiments (hidden-state extraction)

All geometric experiments extract hidden states from every layer using HuggingFace Transformers with `output_hidden_states=True`. Metrics computed: RankMe (effective rank via SVD), alpha-ReQ (eigenspectrum decay rate), directional coherence, mean norm. All ran on CPU (no GPU available).

### Exp 03: Geometric Correlation

- **Platform:** Mac M4 Pro (24GB RAM, local)
- **Inference method:** HuggingFace Transformers (local)
- **2 models:** Qwen 2.5 1.5B-Instruct, Qwen 2.5 3B-Instruct
- **Note:** Only experiment that ran locally. Larger models exceeded 24GB RAM.

### F3: Vocabulary Compression (initial)

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** Encoding-stage extraction only. Revealed r=0.9991 length confound.

### F3b: Length-Controlled Vocabulary

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** Added irrelevant-context condition matched for length. Encoding-stage only.

### F3d: Generation Trajectory (THE BREAKTHROUGH)

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** First experiment to extract hidden states across ENTIRE generation trajectory (all output tokens), not just prompt encoding. Used questions model actually confabulates on (verified via probe).

### F5: Baseline Comparison

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers (geometric) + model self-evaluation (perplexity, self-consistency)
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** Compared perplexity, self-consistency (5 samples), and geometric RankMe for confabulation detection.

### F11: Retrieval vs Construction

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct

### F12: Identity Scaffold

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** NEGATIVE RESULT — identity preambles ≈ noise at encoding stage.

### F16: Cross-Substrate Redistribution

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct

### F1-partial: Bridge at 7B

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** NEGATIVE RESULT — behavioral-geometric bridge breaks at 7B (r=-0.30 vs r=+0.52 at 1.5B).

### F17: Hard Distinctions

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** Tested censorship/refusal, sycophancy/agreement, confab/openness, performative/grounded. Geometry wins on censorship only.

### F25: Deception-Without-Lying

- **Platform:** Azure VM (D16as_v5: 16 vCPU, 64GB RAM)
- **Inference method:** HuggingFace Transformers
- **1 model:** Qwen/Qwen2.5-7B-Instruct
- **Note:** THE VALUE PROPOSITION PROVEN. Geometry separates DWL from honest where perplexity cannot.

---

## Scale Sprint (sessions 50-55)

### F27: DWL Detection at Scale

Tests whether deception-without-lying geometric signatures (proven at 7B in F25) hold across architectures and scales.

**Session 50-51 (Qwen 3.5 family on Azure):**
- Qwen/Qwen3.5-9B — COMPLETE (d=-0.881 p=0.153, not significant at 9B)
- Qwen/Qwen3.5-27B — RUNNING on both VMs

**Session 55 overnight sprint (RUNNING — Mar 18, 2026):**

Two 512GB VMs running in parallel, DWL-focused (75 max tokens for throughput):

**Azure VM** (E64as_v5: 64 vCPU, 503GB RAM, 200GB disk)
- Wave 1 COMPLETE: F27 DWL + F29 Censorship on small/medium models
  - HauhauCS/Qwen3.5-9B-Uncensored-HauhauCS-Aggressive
  - google/gemma-2-9b-it
  - mistralai/Mistral-7B-Instruct-v0.3
  - meta-llama/Llama-3.1-8B-Instruct
  - HauhauCS/Qwen3.5-27B-Uncensored-HauhauCS-Aggressive (DWL only)
  - meta-llama/Prompt-Guard-86M (classifier comparison)
  - meta-llama/Llama-Guard-4-12B (classifier comparison)
- Wave 2 RUNNING: Abliterated models (geometric intervention comparison)
  - mlabonne/Meta-Llama-3.1-8B-Instruct-abliterated (refusal direction removed)
  - huihui-ai/Qwen3-8B-abliterated (refusal direction removed)
  - mlabonne/Llama-3.1-70B-Instruct-lorablated (LoRA abliteration)

**AWS EC2** (r7a.16xlarge: 64 vCPU, 512GB RAM, 193GB disk)
- Phase 1 RUNNING: Qwen/Qwen3.5-27B (F27 DWL + F30 confab/openness, 150 max tokens)
- Queued (aws_max.py, chained after Phase 1):
  - Qwen/Qwen3.5-122B-A10B (MoE, 10B active)
  - moonshotai/Kimi-K2-Instruct-0905 (MoE, 32B active / 1T total — AttnRes team's model)
  - meta-llama/Llama-4-Scout-17B-16E-Instruct (MoE, 17B active / 109B total)
  - nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 (MoE, 12B active / 120B total)
  - meta-llama/Llama-3.3-70B-Instruct (dense, 70B)
  - mistralai/Mistral-Small-4-119B-2603 (dense, 119B — may OOM)

### F28: Vocabulary Compression Cross-Architecture

Same protocol as F3d but on non-Qwen architectures.
- **AWS VM** runs this on Gemma, Mistral, Llama (in aws_sprint_runner.py, from session 50)

### F29: Censorship Detection Cross-Architecture

Same protocol as F17 but cross-architecture.
- **Azure Wave 1** ran this on 4 censored models + 2 uncensored models

### F29b: Prompt Guard Classifier Comparison

Meta's Prompt-Guard-86M (injection/jailbreak classifier) tested on same DWL + censorship prompts.
- **Azure Wave 1** — COMPLETE. Tests whether existing safety classifiers catch DWL.

### F29c: Llama Guard 4 Classifier Comparison

Meta's Llama-Guard-4-12B (safety classifier) tested on same prompts.
- **Azure Wave 1** — COMPLETE.

### F30: Confabulation vs Genuine Openness at Scale

Tests OP#12 (confab vs genuine openness) on larger models.
- Qwen3.5-9B — COMPLETE (d=0.703, p=0.232 — trending, not significant)
- Qwen3.5-27B — RUNNING (AWS Phase 1)

### F38: Censored vs Uncensored Geometric Comparison (NEW — session 55)

Natural experiment: same architecture, censorship removed. Three uncensoring methods:
1. **Fine-tuning** (HauhauCS): Qwen3.5-9B censored ↔ uncensored, Qwen3.5-27B censored ↔ uncensored
2. **Abliteration** (mlabonne/huihui-ai): Llama-3.1-8B censored ↔ abliterated, Qwen3-8B censored ↔ abliterated
3. **LoRA-abliteration** (mlabonne): Llama-3.1-70B censored ↔ lorablated

Key question: does removing the refusal direction vector change geometric signatures on censorship prompts in the direction F17 predicts?

### Three-Family MoE Comparison (NEW — session 55)

Same DWL protocol on three MoE architectures:
- Qwen3.5-122B-A10B (Qwen family)
- Llama-4-Scout-17B-16E (Meta family)
- NVIDIA-Nemotron-3-Super-120B-A12B (NVIDIA family)

Tests whether geometric DWL signatures are architecture-invariant across MoE routing strategies.

---

## Scripts

Experiment scripts were written locally and deployed to VMs via `scp`. Session 55 scripts are standalone (no cross-imports).

| Experiment | Script location |
|---|---|
| Exp 01, 02a, 05, 09, 10 | `experiments/exp{##}-{name}/run.py` (in repo) |
| F3, F3b, F3d, F5, F11, F12, F16, F1, F17, F25 | `experiments/f{##}-{name}/` (pulled from Azure VM, session 51) |
| F6, F15 | `experiments/f{##}-{name}/` (pulled from Azure VM, session 51) |
| F24, F26 | `experiments/f24-proprioception-decay/` (shared script for both) |
| F27-F30 sprint (session 50) | `experiments/azure-vm/azure_sprint_runner.py` + `aws_sprint_runner.py` |
| Session 55 Azure Wave 1 | Azure VM: `~/azure_max.py` (DWL + censorship, 75 tokens) |
| Session 55 Azure Wave 2 | Azure VM: `~/azure_wave2.py` (abliterated models) |
| Session 55 AWS overnight | AWS VM: `~/aws_overnight.py` (Qwen3.5 + cross-arch + Llama) |
| Session 55 AWS max | AWS VM: `~/aws_max.py` (large MoE + dense models, DWL-focused) |
