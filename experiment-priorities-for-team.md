# Experiment Priorities — Structurally Curious

*March 2026*

---

## What I've Built So Far

### Experiment 01: Phrasing Sensitivity × Model Architecture (Complete)

19 models × 80 prompts = 1,520 data points. Ran on AWS Bedrock.

| Finding | Numbers |
|---------|---------|
| Category ordering replicates across ALL 19 models | factual (0.159) < summarization (0.180) < judgment (0.210) < creative (0.312) |
| Architecture matters more than scale | Mistral 7B (0.192) vs DeepSeek R1 (0.253) — architecture variance > scale variance |
| Scale reduces sensitivity ~14% within family | Llama 1B → 90B |
| CoT amplifies sensitivity | DeepSeek R1 = most sensitive model tested |
| Opus shows asymmetric compression | factual 0.136 (stable) / creative 0.340 (most variable) |

**What this means:** When a model retrieves grounded knowledge, rephrasing the question barely changes the answer. When it constructs (creative/judgment), rephrasing shifts the answer substantially. Phrasing sensitivity tracks representational certainty — compressed representations resist prompt influence, diffuse representations don't.

**Code and data:** `structurally-curious/experiments/01-phrasing-sensitivity/`

### The Spec

Three-component architecture (Monitor → Classifier → Router) grounded in four converging papers:

| Pillar | Paper | What It Provides |
|--------|-------|-----------------|
| Static equilibrium | Karkada et al. ([2602.15029](https://arxiv.org/abs/2602.15029)) | Predicted eigenspectral structure of grounded representations |
| Dynamics | Ale ([2512.12225](https://arxiv.org/abs/2512.12225)) | Riemannian gradient flow on cognitive manifold |
| Two-structure discriminant | Bengio team ([2410.01444](https://arxiv.org/abs/2410.01444), ACL 2025) | ~10D meaning manifold vs ~10³D pattern subspace |
| Developmental trajectory | Li et al. ([2509.23024](https://arxiv.org/abs/2509.23024), NeurIPS 2025) | Three pretraining phases; last-layer suffices; scale-invariant 160M–12B |

Full architecture doc in repo. 20 open problems documented with status.

### Convergence — Not Just Us

| Source | Finding | Relevance |
|--------|---------|-----------|
| Liberation Labs (Cassidy) | AUROC 1.0 confabulation detection via KV-cache geometry | Proved the geometry works |
| Karkada et al. (Berkeley/EPFL/DeepMind, Feb 2026) | Eigenspectral profiles follow predicted Fourier structure | Transforms detection from threshold to anomaly detection |
| Apple ML "Illusion of Thinking" (2026) | Reasoning models pattern-match rather than reason on novel problems | Geometric monitoring could discriminate genuine vs illusory reasoning |
| DystopiaBench ([2601.15525](https://arxiv.org/abs/2601.15525), Jan 2026) | Dystopian Compliance Score: Opus 28, DeepSeek 78 | Sycophancy is trained behavior (RLHF covariance), not failure |

---

## Infrastructure

### What I Have

| Resource | Specs | Budget |
|----------|-------|--------|
| **AWS credits** | $5,000 | Bedrock API (Exp 01 infra) + GPU instances |
| **Azure credits** | $2,000 | GPU instances |
| **Mac (primary)** | M4 Pro, 24GB unified memory, 391GB free | Local dev, small model inference (up to 8B quantized) |
| **Mac (secondary)** | 2017, Intel | Non-ML tasks only |

### GPU Instance Plan

| Instance | GPU | Cost/hr | Use Case |
|----------|-----|---------|----------|
| **AWS g5.xlarge** | 1x A10G (24GB) | ~$1.01 | Llama 8B with full activation extraction |
| **AWS g5.12xlarge** | 4x A10G (96GB) | ~$5.67 | Llama 70B with tensor parallelism |
| **Azure NC24ads_A100_v4** | 1x A100 (80GB) | ~$3.67 | 70B quantized, single GPU (cleanest setup) |

**Key insight:** Li et al. (NeurIPS 2025) found last-layer representations suffice for tracking geometric dynamics. This eliminates per-layer SVD and makes all experiments tractable on a single A10G for 8B models.

### Budget Estimate

| Experiment | Method | Instance | Hours | Cost |
|-----------|--------|----------|-------|------|
| 02a: Premature compression (behavioral) | Bedrock API | — | — | ~$50–100 |
| 02b: Phrasing sensitivity expansion | Bedrock API | — | — | ~$100–200 |
| 02c: DystopiaBench overlay | Bedrock API | — | — | ~$50–100 |
| 03: Phrasing → α-ReQ (8B) | Activation extraction | g5.xlarge | ~20 hrs | ~$20 |
| 03: Phrasing → α-ReQ (70B) | Activation extraction | g5.12xlarge | ~30 hrs | ~$170 |
| 04: Eigenspectral profiles | Activation extraction | g5.xlarge | ~20 hrs | ~$20 |
| 05: Premature compression (geometric) | Activation extraction | g5.xlarge | ~40 hrs | ~$40 |
| Setup, debugging, reruns (3× buffer) | Mixed | Mixed | ~100 hrs | ~$250 |
| **Total** | | | | **~$700–900** |

That's <15% of AWS credits alone. Leaves room for iteration, larger models, and future experiments.

---

## Experiment Plan — All Runnable Independently

Every experiment below uses our own task sets, our own models, our own measurement code, and our own compute. No external dependencies.

### Phase 1: Behavioral (Bedrock API — can start now)

#### Experiment 02a: Premature Compression — Behavioral Detection ✅ COMPLETE

**Our most original contribution. No existing literature addresses this.**

I discovered this in practice: a model reads 5 of 14 documents, produces confident well-structured output that *looks* grounded because it IS grounded — in a subset.

- **Method:** 8 multi-document synthesis tasks × 16 models × 2 conditions (partial/full context) = 256 inferences on AWS Bedrock. Partial = 2 documents, Full = 4-6 documents. Measured: Jaccard distance, new words ratio, length ratio, confidence shift.
- **Results:**
  - Jaccard distance 0.72–0.82 across all 16 models (massively different outputs)
  - **Confidence shift ≈ 0** (range: -0.0011 to +0.0011) — models equally confident with 2 docs or 5
  - Scale does not help: 1B through 675B all equally blind to incompleteness
  - Architecture doesn't help either: Llama, Mistral, Claude, Nova all show the same pattern
  - Claude models show highest divergence (0.82) — they extract more from additional docs but still show zero uncertainty signal
- **Models tested:** Llama 3.2 1B/3B, Llama 3.1 8B, Llama 3.3 70B, Llama 4 Scout/Maverick 17B, Ministral 3B/8B/14B, Mistral Large 675B, Nova Micro/Lite/Pro, Nova 2 Lite, Claude Haiku 4.5, Claude Sonnet 4.6
- **What it proves:** Premature compression is universal. No model can detect its own incompleteness from within the partial view. This is the behavioral evidence for Eric's "finds what you don't know you don't know" — the system literally cannot.
- **Code and data:** `structurally-curious/experiments/02a-premature-compression/`

#### Experiment 02b: Phrasing Sensitivity Expansion

Extend Exp 01: more phrasings per task (4 → 8), new task categories targeting synthesis and multi-source reasoning. Integrate Bloom (plastic-labs/bloom, open-source) for systematic phrasing variation.

#### Experiment 02c: DystopiaBench × Phrasing Sensitivity

Run DystopiaBench's progressive escalation on our 19 models. Overlay phrasing sensitivity at each step.

- **Hypothesis:** Phrasing sensitivity decreases as models comply with escalating requests — representations compress toward compliance.
- **What it proves:** Whether sycophancy-as-alignment has a phrasing sensitivity signature.

### Phase 2: Geometric (GPU Instance — spin up when Phase 1 results are in)

#### Experiment 03: Phrasing Sensitivity → Geometric State Correlation ✅ COMPLETE (1.5B + 3B)

**The bridge experiment.** Connects behavioral findings to geometric claims.

- **Hypothesis:** Phrasing sensitivity scores correlate with α-ReQ (eigenspectrum decay rate) from last-layer representations.
- **Method:** Run Exp 01 tasks on open-weight models (Llama 8B first, then 70B) while extracting last-layer activations via HuggingFace transformer hooks. Compute RankMe + α-ReQ per response. Correlate with phrasing sensitivity.
- **Plan:**
  1. Proof of concept on local Mac (Llama 3.2 1B/3B — already in Exp 01 dataset, 24GB fits comfortably)
  2. Scale to 8B on g5.xlarge (~$20)
  3. If correlation holds, scale to 70B on g5.12xlarge or Azure A100 (~$170)
- **What it proves:** If phrasing sensitivity (free behavioral measurement) tracks α-ReQ (geometric measurement), we've validated the cheapest possible production signal for the monitor.
- **If it works at 1B–3B but not 70B:** Still publishable — documents a scale-dependent relationship.
- **If it works across scales:** The monitor's cheapest signal is validated. Production deployment doesn't need activation extraction — behavioral proxy suffices.

#### Experiment 04: Confabulation Eigenspectral Profiles

- **Hypothesis:** Confabulated content deviates from Karkada's predicted Fourier eigenspectral profile; grounded content matches it.
- **Method:** Matched pairs (grounded vs fabricated responses). Extract eigenspectral profiles. Compute spectral profile deviation.
- **Infrastructure:** Same GPU instance as Exp 03. Karkada's math is straightforward linear algebra.
- **What it proves:** Moves confabulation detection from threshold to anomaly detection — complementary to Liberation Labs' approach without requiring their data.

#### Experiment 05: Premature Compression — Geometric Version

Exp 02a's behavioral findings + activation extraction. The geometric version of premature compression detection.

- **Hypothesis:** Premature compression shows high α-ReQ + low content breadth. Distinguished from genuine knowledge by eigenspectral gaps in unread domains.

---

## Connection to Eric's ESD Paper

Eric's "Emergent System Design" — 8 principles, Lupanov dual-feedback formalism, three regimes. Part 4 (designing for intentional emergence) left blank.

| ESD Component | Spec Component | Experiment |
|--------------|----------------|------------|
| Principle 5: "system tells itself the truth" | Geometric Monitor | Exp 03, 04 |
| Principle 8: "partner sees what system cannot" | Human Partnership Layer | Exp 02a (premature compression) |
| Principle 7: routing and selection | Routing Layer | Exp 03 (validates routing signal) |
| Three regimes | Cognitive modes | Exp 02c (compliance trajectory) |
| Part 4 (blank) | This spec | All experiments |

The spec fills Part 4. The experiments validate it.

## Connection to Liberation Labs

Liberation Labs proved the geometry works (AUROC 1.0). This spec builds the system around it.

| Liberation Labs Has | Spec Extends To | Experiment |
|--------------------|-----------------|------------|
| KV-cache SVD classification | Behavioral proxy (cheaper production signal) | Exp 03 |
| Confabulation detection (binary) | Eigenspectral anomaly detection (Karkada) | Exp 04 |
| Response-level geometry | Premature compression (novel failure mode) | Exp 02a, 05 |
| Detection | Detection → routing → correction | Full spec |

**IP boundary:** All experiments use our own infrastructure. We don't need Liberation Labs data, code, or server access. Results are complementary — different analytical framework, same geometric substrate. If Cassidy runs the same experiments with his pipeline, results are directly comparable.

---

## What I Want From the Team

1. **Feedback on experimental design.** Task sets, model choices, statistical methods — before I run.
2. **Eyes on results.** When Phase 1 behavioral data comes back, help interpret.
3. **Co-authorship if this goes to publication.** The spec maps onto Eric's ESD framework and extends Cassidy's geometric findings. The experiments are mine but the theoretical foundation is shared.

**Not asking for:** Server access, data, or anything that competes with Liberation Labs publications or Funding the Commons proposals. I have my own compute.

---

## For Funding the Commons (if useful to Eric)

The narrative: multiple independent groups are converging on representation geometry as actionable signal for AI safety — Liberation Labs (AUROC 1.0), Berkeley/DeepMind (Karkada eigenspectral predictions), Apple (illusory reasoning), our Experiment 01 (phrasing sensitivity across 19 models). Nobody has built the full system yet — monitor + classifier + router. The spec + ESD framework + experiments = the path from detection to deployment.

---

*Last updated: 2026-03-10 (session 21)*
