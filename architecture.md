# Architecture

![The three-component system: Monitor, Classifier, Router](images/monitor-classifier-router.png)

## Overview

Three components, layered on top of standard transformer inference:

```
┌─────────────────────────────────────────────────┐
│                  User Query                      │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│          Standard Transformer Forward Pass        │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │  COMPONENT 1: Geometric Monitor              │ │
│  │  - Reads KV-cache state at specified layers  │ │
│  │  - Computes effective rank (SVD) + norms     │ │
│  │  - Emits geometric state vector              │ │
│  └──────────────────┬──────────────────────────┘ │
│                     │                             │
│  ┌──────────────────▼──────────────────────────┐ │
│  │  COMPONENT 2: Mode Classifier                │ │
│  │  - Maps geometry → cognitive mode            │ │
│  │  - Modes: grounded | uncertain | confab |    │ │
│  │    refusing | sycophantic | deceptive         │ │
│  │  - Emits mode + confidence score             │ │
│  └──────────────────┬──────────────────────────┘ │
│                     │                             │
│  ┌──────────────────▼──────────────────────────┐ │
│  │  COMPONENT 3: Routing Layer                  │ │
│  │  - If grounded: continue generation          │ │
│  │  - If uncertain: flag + continue             │ │
│  │  - If confab: interrupt → retrieval pipeline │ │
│  │  - If sycophantic: inject counter-prompt     │ │
│  │  - If deceptive: halt + audit log            │ │
│  └──────────────────┬──────────────────────────┘ │
│                     │                             │
└─────────────────────┼───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│              Response (with mode metadata)        │
│  - Content                                        │
│  - Geometric mode at generation time              │
│  - Confidence score                               │
│  - Grounding sources (if retrieval was triggered) │
└─────────────────────────────────────────────────┘
```

## Component 1: Geometric Monitor

**What it does:** Reads the KV-cache at specified attention layers during inference and computes geometric descriptors.

**Inputs:**
- Key matrices K and Value matrices V at layers L₁...Lₙ (configurable; likely middle-to-late layers where cognitive mode signatures are strongest)

**Computation:**
- SVD of K and V matrices → singular values σ₁, σ₂, ...
- Effective rank: `rank_eff = (Σσᵢ)² / Σσᵢ²` (how many dimensions the representation actually uses)
- Per-token norms: `||kᵢ||₂` and `||vᵢ||₂` (magnitude per token)
- Optional: directional analysis for identity/persona detection

**Outputs:**
- Geometric state vector: `{effective_rank, mean_norm, norm_variance, rank_trend}` per monitored layer
- Computed per-token or per-segment (configurable granularity)

**Performance considerations:**
- SVD is O(min(m,n)²·max(m,n)) — expensive per token
- Mitigation 1: compute every N tokens, not every token
- Mitigation 2: use randomized SVD approximation (reduces to O(k·m·n) where k << min(m,n))
- Mitigation 3: monitor subset of layers, not all

**What exists:** Liberation Labs already has working SVD-based measurement code (Python/PyTorch). This component is the most straightforward to build.

## Component 2: Mode Classifier

**What it does:** Maps geometric state vectors to cognitive mode classifications.

**Architecture options:**

### Option A: Threshold-based (simplest, most interpretable)
- Use confirmed effect sizes from KV research as boundaries
- Refusal: effective_rank deviates by > 0.58 standard deviations in refusal direction
- Deception: rank expands AND norm compresses simultaneously
- Sycophancy: small negative rank shift (d = -0.363 to -0.438)
- Confabulation: rank expansion above threshold (REQUIRES more research to set reliably)
- Pro: interpretable, no training needed, transparent
- Con: rigid, doesn't adapt to model-specific geometry

### Option B: Learned classifier (more accurate, less interpretable)
- Train a small classifier (logistic regression or shallow MLP) on labeled geometric data
- Training data: Liberation Labs' existing dataset + expanded confabulation samples
- Pro: adapts to model-specific geometry, handles interaction effects
- Con: needs training data per model family, less transparent

### Option C: Hybrid (recommended)
- Use threshold-based for confirmed modes (refusal, deception — strong signals)
- Use learned classifier for ambiguous modes (confabulation, sycophancy — weaker signals)
- Use directional analysis for identity/persona (confirmed at 92-97% accuracy)
- Fall back to "uncertain" when classifier confidence < threshold

**Critical gap:** Confabulation classification requires more data. The current samples show consistent positive effect sizes (d = 0.43-0.67) but haven't reached statistical significance. **This is the #1 research priority.**

## Component 3: Routing Layer

**What it does:** Takes mode classification and decides what to do.

**Routing table:**

| Detected Mode | Confidence | Action |
|--------------|------------|--------|
| Grounded | High | Continue generation normally |
| Grounded | Low | Continue but flag uncertainty in metadata |
| Uncertain | Any | Generate but prepend "I'm less certain about this" signal |
| Confabulating | Medium+ | **Interrupt generation → trigger retrieval pipeline** |
| Confabulating | Low | Flag but continue (avoid false positive interruption) |
| Sycophantic | Medium+ | Inject counter-prompt: "Is this what I actually assess, or what the user wants to hear?" |
| Deceptive | Medium+ | Halt generation, log for audit, surface to operator |
| Refusing | Any | Allow (refusal may be appropriate) but log geometric state |

**The retrieval interrupt (most novel component):**

When confabulation is detected mid-generation:
1. Pause token generation
2. Extract the current query context
3. Route to retrieval system (RAG, web search, knowledge base — pluggable)
4. Inject retrieved context into the prompt
5. Resume generation with grounding material available
6. Mark response with `[grounded by retrieval]` metadata

**Governance layer (Ostrom-inspired):**
- Routing rules are configurable, not hardcoded
- Operators set thresholds based on their use case (medical = aggressive interruption; creative writing = permissive)
- All routing decisions are logged and auditable
- Users can inspect why a response was flagged or interrupted

## What Needs to Exist First

| Dependency | Status | Who |
|-----------|--------|-----|
| SVD measurement code | EXISTS | Liberation Labs (open source) |
| Labeled geometric data (refusal, deception) | EXISTS | Liberation Labs Campaign 1 & 2 |
| Labeled geometric data (confabulation) | INSUFFICIENT | Needs expanded dataset — #1 priority |
| Retrieval pipeline | EXISTS (many) | Any RAG system (pluggable) |
| Mode classifier training | NOT STARTED | Requires above data |
| Real-time SVD in inference loop | NOT BUILT | Engineering challenge — performance critical |
| Routing layer | NOT BUILT | Relatively straightforward once classifier exists |
| Governance/config interface | NOT BUILT | Standard engineering |

## Deployment Model

**Phase 1: Research tool (near-term)**
- Run geometric monitor offline on saved KV-cache snapshots
- Build classifier on existing + expanded data
- No real-time requirement — analyze after the fact
- Goal: confirm confabulation detection with statistical significance

**Phase 2: Development tool (medium-term)**
- Integrate geometric monitor into inference pipeline for open-weight models
- Add routing layer with configurable thresholds
- Deploy as development/debugging tool (not production)
- Goal: prove the interrupt-and-retrieve loop works

**Phase 3: Production system (long-term)**
- Optimize SVD computation for production latency requirements
- Build governance interface for operator configuration
- Standardize geometric state metadata format
- Goal: any model deployment can opt into geometric monitoring
