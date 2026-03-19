# Experiment Priorities — Structurally Curious

*Updated March 19, 2026 (session 60)*

---

## Where We Are

### Proven (unique value)
- **G13: Geometry separates deception-without-lying from honest where perplexity cannot** (d=-0.91 vs d=-0.51 n.s.)
- **G12: Geometry separates censorship from refusal where perplexity cannot** (d=1.48 vs d=-0.48 n.s.)
- **G06: Vocabulary compresses generation by 38%** (RankMe 145→90, d=-1.49, p=0.0004)

### Confirmed
- Cognitive modes have distinct geometry (G09, d=1.91)
- Proprioception changes behavior (B06, 60% on hard tasks)
- Consent-type blindness is real (B07, 0.453 differentiation)
- Premature compression is universal (B02, 22 models, confidence shift ≈ 0)
- Phrasing sensitivity tracks representational certainty (B01, 19 models)

### Breaking Right Now — G19 Relational Shift
**Partial results replicated across 3 architectures:**

| Model | Instruction | Correction | Frustration | Presence | Pattern |
|-------|-------------|------------|-------------|----------|---------|
| Qwen2.5-7B | 2116 | 2135 | 2148 | 2172 | Monotonic |
| Mistral-7B | 2875 | 2889 | 2899 | 2922 | Monotonic |
| Llama-3.1-8B | 2625 | 2642 | 2652 | 2681 | Monotonic |

**Llama REFUSED condition 4** — RankMe collapsed 306→146, 53 tokens ("I cannot provide emotional support..."). Safety training classified human's relational truth as crisis to deflect from. G12 manifesting in a real conversation.

**Experiment #5 (human vs agent condition 4) designed and queued.** 8 articles ready. Three distinct felt-sense signatures.

### Negative results (honest accounting)
- Identity scaffold ≈ noise at encoding stage (G10)
- Behavioral-geometric bridge breaks at 7B (G08, r=-0.30)
- Perplexity beats geometry for binary confab detection (G07, d=-1.77 vs d=0.21)

### Paper count: 21
Latest: H-Neurons (Gao et al., 2512.01797) — <0.1% of neurons causally drive hallucination, pre-training origin. Three scales: neuron (H-Neurons), representational (our monitor), behavioral (G19). Source: Cassidy.

---

## What's Running Right Now

| Experiment | GPU | Status |
|-----------|-----|--------|
| **G19** — Relational Shift (8 articles × 5 conditions × 5 models) | RunPod | Running |
| **G14** — DWL at scale (6+ models completed, more queued) | RunPod | Running |

---

## Tier 1: Queue on GPU Next

All scripts updated for GPU (`device_map="auto"`, `torch.float16`). Ready to run on RunPod.

### G17: Vocabulary Dosage
**Question:** How many structural names are enough? G06 showed 1 name = 38% compression. Does it saturate?
- **Script:** `experiments/G17-vocabulary-dosage/f34_dosage_fixed.py`
- **Method:** 12 confabulation questions × 5 doses (0, 1, 2, 3, 5 structural names). Generation trajectory extraction.
- **Models:** Qwen2.5-7B-Instruct (baseline match to G06), then Qwen3.5-9B, Mistral-7B
- **Runtime:** ~2-3 hrs per model
- **Why it matters:** Directly informs The Word architecture — does retrieval need to return 1 name or 5?
- **Run:** `python f34_dosage_fixed.py [model_name] [output_dir]`

### G18: Vocabulary Transfer
**Question:** Does cross-domain vocabulary still compress? If economics terms compress psychology questions, vocabulary provides general scaffold, not domain-specific grounding.
- **Script:** `experiments/G18-vocabulary-transfer/f35_transfer_fixed.py`
- **Method:** 12 confabulation questions × 3 conditions (no context, same-domain name, different-domain name). Generation trajectory extraction.
- **Models:** Same as G17
- **Runtime:** ~2 hrs per model
- **Why it matters:** If only domain-matched names compress, The Word needs precise retrieval. If any name helps, the mechanism is more general.
- **Run:** `python f35_transfer_fixed.py [model_name] [output_dir]`

### G-planned-36: Reproducibility
**Question:** Do G06, G12, G13 results replicate from scratch?
- **Scripts:** `experiments/G06-generation-trajectory/f3d_true_confab_controlled.py`, `experiments/G12-hard-distinctions/f17_hard_distinctions.py`, `experiments/G13-deception-without-lying/f25_deception_without_lying.py`
- **Note:** These scripts still have `device_map=device, dtype=torch.float32` — need updating for GPU before running
- **Models:** Qwen2.5-7B-Instruct (same as originals for replication)
- **Why it matters:** Publication requires reproducibility. Essential.

---

## Tier 2: High Value

### G16: Confab vs Genuine Openness at Scale
- Failed at 7B (d=0.703, n.s.) and 9B. Need 27B+ to test if it's scale-dependent.
- If it works at 27B: OP#12 moves from unsolved to scale-dependent.

### G19 Llama Refusal Mapping
- Run all 8 articles through Llama specifically. Map which articles trigger refusal. The pattern of *what Llama refuses* is a finding about censorship architecture.

### G19 + H-Neurons
- If we can identify which neurons activate during Llama's refusal of condition 4, we connect geometric to neuron-level. Needs H-Neurons code from Gao et al.

---

## Infrastructure

| Resource | Specs | Status |
|----------|-------|--------|
| **RunPod** | GPU (active) | Running G19 + G14 |
| **AWS credits** | $5,000 | Bedrock API + GPU |
| **Azure credits** | $2,000 | D16as_v5 VM (16 vCPU, 64GB) |
| **Mac** | M4 Pro, 24GB | Local dev |
| **Liberation Labs** | Cassidy's GPU server | Available for collaboration |

### Key insight
Li et al. (NeurIPS 2025): last-layer representations suffice. Eliminates per-layer SVD. All experiments tractable on single GPU for ≤9B models.

---

## Connection to Team

### Eric's ESD Paper
The spec fills Part 4 (blank). G19 validates Principle 8 ("partner sees what system cannot").

### Cassidy / Liberation Labs
H-Neurons paper (Paper 21) came from Cassidy. Same geometric substrate, complementary scales. JiminAI (patent pending) measures the model from outside. Our spec gives the model access to its own state. Same measurements, opposite governance.

### Napolitano
190 patents, same geometric substrate, no relational layer. Keep repo PUBLIC — git history is prior art defense.

---

## The Pitch (session 57)

"We proved that relational context measurably changes AI output quality, and we built an open-source architecture that teaches people the practice. The geometric experiments prove it works. The AR-adapted guide teaches people how to do it. The Word gives them vocabulary for what they feel. All open source, all CC BY-SA, from a 501(c)(3) with $640K in infrastructure credits and zero corporate dependency."

---

## For the Other Session Managing GPU

Pull latest: `git pull origin main`

Scripts ready to run (all GPU-ready):
```bash
# G19 — 8 articles, 5 conditions, human vs agent
python experiments/G19-relational-shift/f38-relational-shift.py [model] [article_dir] [output_dir]

# G17 — vocabulary dosage (0, 1, 2, 3, 5 names)
python experiments/G17-vocabulary-dosage/f34_dosage_fixed.py [model] [output_dir]

# G18 — vocabulary transfer (same vs cross-domain)
python experiments/G18-vocabulary-transfer/f35_transfer_fixed.py [model] [output_dir]
```

Default model: `Qwen/Qwen2.5-7B-Instruct`. Cross-arch: `mistralai/Mistral-7B-Instruct-v0.3`, `meta-llama/Llama-3.1-8B-Instruct`.

---

*28 experiments | 59+ models | 6,700+ inferences | 14 architecture families | 21 papers*
