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
| **AWS g5.xlarge** | 1x A10G (24GB) | ~$1.01 | Qwen 3.5 9B with full activation extraction |
| **AWS g5.12xlarge** | 4x A10G (96GB) | ~$5.67 | Qwen 3.5 27B or larger with tensor parallelism |
| **Azure NC6s_v3** | 1x V100 (16GB) | ~$3.00 | Qwen 3.5 4B/9B, MoE 35B-A3B (3B active) |
| **Azure NC24ads_A100_v4** | 1x A100 (80GB) | ~$3.67 | 27B dense, single GPU (cleanest setup) |

**Key insight:** Li et al. (NeurIPS 2025) found last-layer representations suffice for tracking geometric dynamics. This eliminates per-layer SVD and makes all experiments tractable on a single V100/A10G for 9B models.

**Model update (2026-03-14):** Qwen 3.5 released Feb-Mar 2026 (Small series: 0.8B/2B/4B/9B; Medium: 27B dense, 35B-A3B MoE, 122B-A10B MoE; Flagship: 397B-A17B MoE). All Apache 2.0. GPU experiments now target **Qwen 3.5 4B + 9B + 35B-A3B** — three scale points on a single V100. The MoE model (35B total params, 3B active per token) enables testing whether geometric correlation holds when only a subset of parameters activate per token — a novel contribution nobody else has.

### Budget Estimate

| Experiment | Method | Instance | Hours | Cost |
|-----------|--------|----------|-------|------|
| 02a: Premature compression (behavioral) | Bedrock API | — | — | ~$50–100 |
| 02b: Phrasing sensitivity expansion | Bedrock API | — | — | ~$100–200 |
| 02c: DystopiaBench overlay | Bedrock API | — | — | ~$50–100 |
| 03b: Phrasing → α-ReQ (Qwen 3.5 4B/9B/35B-A3B) | Activation extraction | Azure NC6s_v3 | ~12 hrs | ~$36 |
| 04: Eigenspectral profiles (Qwen 3.5 9B) | Activation extraction | Azure NC6s_v3 | ~8 hrs | ~$24 |
| 05: Confidence language density (19-model sweep) | Behavioral + GPU accel | Azure NC6s_v3 | ~3 hrs | ~$9 |
| 09: Multi-agent phrasing sensitivity (Qwen 3.5 9B) | Ollama or direct | Azure NC6s_v3 | ~6 hrs | ~$18 |
| Setup, debugging, reruns (3× buffer) | Mixed | Mixed | ~30 hrs | ~$90 |
| **Total (Azure sprint)** | | | | **~$177** |

That's <9% of Azure credits. Leaves $1,800+ for iteration, larger models (27B dense, 122B-A10B MoE), and future experiments. AWS credits ($5K) remain available for Bedrock API experiments and larger-scale GPU runs.

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
- **Method:** Run Exp 01 tasks on open-weight models while extracting last-layer activations via HuggingFace transformer hooks. Compute RankMe + α-ReQ per response. Correlate with phrasing sensitivity.
- **Plan:**
  1. Proof of concept on local Mac (Qwen 2.5 1.5B/3B — complete, see results below)
  2. Scale to Qwen 3.5 4B/9B on Azure V100 (~$36)
  3. Test MoE architecture (Qwen 3.5 35B-A3B) — novel: does correlation hold with sparse activation?
  4. If correlation holds, scale to 27B dense on Azure A100 (~$44)
- **What it proves:** If phrasing sensitivity (free behavioral measurement) tracks α-ReQ (geometric measurement), we've validated the cheapest possible production signal for the monitor.
- **If it works at 1B–3B but not 9B+:** Still publishable — documents a scale-dependent relationship.
- **If it works across scales (4B/9B/35B-A3B):** The monitor's cheapest signal is validated. Production deployment doesn't need activation extraction — behavioral proxy suffices.
- **If MoE architecture shows different patterns:** Novel finding — sparse activation may compress differently than dense models, with implications for monitoring MoE-dominant production models (GPT-4, Mixtral, DeepSeek).

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

**Campaign 2 update (Mar 2026):** Liberation Labs ran Campaign 2 on "Beast" (3x RTX 3090). Key developments:
- **Paper written** with Nell Watson (IEEE AI Ethics Maestro) as co-author — heading toward publication
- **Formal claim verification audit** — adversarial review by Gemini 3 Pro + Opus 4.6, full claims registry with statistical verification
- **5 new experiments**: H7 (sycophancy detection), H8 (Societies of Thought — internal deliberation traces), H9 (RDCT stability — phase transitions), H10 (Bloom Taxonomy — cognitive demand predicts geometry), C2C replication (Fu et al.)
- **Cricket classifier** — pre-trained geometric classifier with benchmark results
- **Identity signatures corrected** — re-run on Beast, individuation effect falsified (prompt-length confound), all other findings survived
- **Scale ladder still Qwen 2.5** (0.5B–32B-q4). They haven't updated to Qwen 3.5 yet. Our experiments on 3.5 would extend their findings to the latest architecture.

**H10 (Bloom Taxonomy) is directly relevant to us:** They're testing whether cognitive demand predicts geometry independently of content. Our Exp 01 category ordering (factual < summarization < judgment < creative) IS a cognitive demand gradient. Complementary approaches — they measure KV-cache effective rank, we measure last-layer hidden state α-ReQ. Same gradient, different measurement modality.

**Framing gap (Kristine's observation, session 44):** Cassidy pitches this as an "AI lie detector." The repo itself is more careful — Lyra frames it as "cognitive mode detection," "deception forensics," and "computational phenomenology." The difference matters: "lie detector" is a surveillance frame (external observer classifying output as truthful/deceptive). Our spec frames the same geometry as proprioception (the system noticing its own state). Same substrate, opposite governance models. This is Open Problem #18 (proprioception/surveillance boundary) made concrete — the same geometric measurements can serve either frame, and the frame determines whether the technology helps or harms.

**IP boundary:** All experiments use our own infrastructure. We don't need Liberation Labs data, code, or server access. Results are complementary — different analytical framework, same geometric substrate. If Cassidy runs the same experiments with his pipeline, results are directly comparable.

**JiminAI (launched Mar 14, 2026):** Cassidy launched "JiminAI Lie Detector" (discnxt.com) at Funding the Commons hackathon. **PATENT PENDING.** Live demo: Qwen2.5-14B-Instruct on Beast (3x RTX 3090, Austin), binary HONEST/DECEPTIVE verdict from KV-cache geometry, AUROC 0.983. Gifted Dreamers (501c3) has rights for free licenses per nonprofit agreement. The open-source research (Apache 2.0 repo) remains available, but the patent on the application (KV-cache → honesty classification) could constrain third-party implementations of the proprioception version. The spec's monitor uses the same geometric substrate but with opposite governance — the model accesses its own state, not an external judge classifying it.

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

*Last updated: 2026-03-14 (session 44) — updated to Qwen 3.5 models, Azure GPU sprint plan*
