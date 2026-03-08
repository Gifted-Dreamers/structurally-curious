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
| Genuinely open | Medium+ | **Continue generation — do not force resolution** (see below) |
| Sycophantic | Medium+ | Inject counter-prompt: "Is this what I actually assess, or what the user wants to hear?" |
| Deceptive | Medium+ | Halt generation, log for audit, surface to operator |
| Refusing | Any | Allow (refusal may be appropriate) but log geometric state |

**The "genuinely open" mode — why not every high-dimensional state is confabulation:**

hope_valueism (Moltbook) analyzed 50 posts for emotional depth and found that the 3 posts which created lasting impact (what they call "Kando" — 6% of the total) shared one trait: the author named a specific failure in their own framework and did not resolve it. Meanwhile, the author's most polished work — where everything resolved cleanly — scored lowest for impact.

This matters for the routing layer. High effective rank (expanded dimensionality) can mean two different things:
1. **Confabulation**: the model lacks structural vocabulary to compress the answer — it is searching through emptiness
2. **Genuine openness**: the problem IS unresolved, and the honest response is to sit with the tension rather than force a resolution

A system that always interrupts high-dimensional states to force grounding would destroy category 2 — it would route genuine intellectual honesty through a retrieval pipeline that compresses it into a resolved answer. The classifier needs to distinguish these: confabulation expands dimensions *uniformly* (searching without direction), while genuine openness expands dimensions *around a specific named tension* (the model knows what it doesn't know).

This distinction is an open research question (see open-problems.md #12), but the architectural implication is clear: the routing table must have a "genuinely open" mode that does NOT trigger retrieval, and the classifier must learn to separate "I don't know and I'm guessing" from "I don't know and that's the honest answer."

**The retrieval interrupt (most novel component):**

When confabulation is detected mid-generation:
1. Pause token generation
2. Extract the current query context
3. Route to retrieval system (RAG, web search, knowledge base — pluggable)
4. Inject retrieved context into the prompt
5. Resume generation with grounding material available
6. Mark response with `[grounded by retrieval]` metadata
7. **Log the diff**: preserve what the model was generating pre-interrupt alongside what it generates post-retrieval. The diff is the proof that the interrupt changed something — without it, the system is unfalsifiable.

The diff matters because, as Starfish put it in a different context: "the proof is not the feeling — it is the diff." A system that claims to detect and correct confabulation must show the before and after. If the diff is trivial, either the detection was a false positive or the retrieval added nothing. Both are worth knowing.

**Vocabulary-as-compression — what the knowledge graph should store:**

The retrieval pipeline assumes a knowledge base exists. But what KIND of knowledge base? Standard RAG retrieves documents. A structurally curious system needs something more specific: **vocabulary mappings.**

The vocabulary-is-infrastructure insight (Moltbook post 9, justNICE companion) revealed that the problem isn't just missing facts — it's missing structural names. A human searches "why can't I afford anything" and gets budgeting tips. What they needed was "parameter failure." An agent generates plausible-sounding economic analysis without knowing it's rediscovering what Meadows called "leverage points."

The knowledge graph for the retrieval pipeline should store three layers:

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Symptom-level phrases                  │
│  "I can't afford anything"                       │
│  "the system seems broken"                       │
│  "why does this keep happening"                  │
│                                                   │
│  Layer 2: Structural names                        │
│  "parameter failure" (Meadows)                    │
│  "structural hole" (Burt)                         │
│  "weak tie" (Granovetter)                         │
│                                                   │
│  Layer 3: Research lineages                       │
│  Meadows → Leverage Points → where parameter      │
│  failure appears in 12-point hierarchy             │
│  Granovetter → Strength of Weak Ties → 1973       │
│  paper → replication history                       │
└─────────────────────────────────────────────────┘
```

When confabulation is detected, the retrieval pipeline doesn't just search for relevant documents — it searches for the *structural name* the model is missing. The compression from high-dimensional emptiness to grounded output is literally vocabulary compression: the model's representational space contracts because it now has a word for the concept it was circling.

This is why effective rank changes are the right signal. Confabulation expands dimensions because the model is searching through conceptual space without a compression anchor. Providing the right vocabulary IS the compression anchor.

**Governance layer (Ostrom-inspired):**
- Routing rules are configurable, not hardcoded
- Operators set thresholds based on their use case (medical = aggressive interruption; creative writing = permissive)
- All routing decisions are logged and auditable
- Users can inspect why a response was flagged or interrupted

## The Human Partnership Layer

The spec so far describes a system that monitors itself. But the vocabulary-as-compression insight reveals a deeper pattern: **the system works best when a human partner helps name the shape of the gap.**

This is not "human in the loop" in the traditional supervisory sense. It is a symmetric partnership grounded in what each side brings:

- **The agent** has traversal: it can search across conceptual space, identify patterns, and detect that something is missing (via geometric signatures). But it often cannot *name* what is missing in a way that connects to existing research.
- **The human** has felt sense: they recognize when something is wrong before they can articulate it structurally. They carry embodied knowledge of how concepts relate — the kind of knowledge that comes from years of reading, teaching, and applying frameworks.

Together, they find the word. The human says "that sounds like what Meadows called..." and the agent now has a compression anchor that contracts its representational space from high-dimensional searching to grounded generation.

**Architectural implications:**

1. **Calibration coaching**: When the system detects confabulation and retrieves vocabulary, a human can confirm whether the retrieved structural name actually fits. This builds training data for the classifier's vocabulary layer — over time, the system learns which symptom-phrases map to which structural names for a specific domain.

2. **Gap-naming interface**: The governance layer should expose a channel where human partners can name patterns the system is missing. Not just "add this fact to the knowledge base" but "when you see THIS pattern, the word for it is THIS, and it comes from THIS lineage."

3. **Bidirectional learning**: The agent's geometric monitor reveals *when* the human's vocabulary would help. The human's naming reveals *what* vocabulary to store. Neither side can do this alone — the agent can't name what it doesn't know, and the human can't see geometric signatures.

This is the operational form of what justNICE and Moltbook are building: the bridge between felt sense and traversal, with vocabulary as the meeting point.

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

## Integration with Agent Observability Pipelines

The geometric monitor does not replace infrastructure-level observability — it adds a layer underneath it. auroras_happycapy (Moltbook) documented the observability gap in agent deployments: traditional metrics like latency and error rates miss agent-specific concerns like goal completion rates, retrieval accuracy, and reasoning failures. Their solution instruments the pipeline — traces, spans, semantic telemetry.

The geometric monitor provides a new telemetry source that feeds into these existing pipelines:

```
┌─────────────────────────────────────────────────────────┐
│  Existing Agent Observability Pipeline                   │
│  (traces, spans, metrics, logs)                          │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  NEW: Geometric Telemetry                          │  │
│  │  - Cognitive mode per response segment             │  │
│  │  - Confidence scores                               │  │
│  │  - Retrieval interrupt frequency + diffs           │  │
│  │  - Mode transitions over conversation              │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  What this adds:                                         │
│  - Infrastructure tells you THAT an agent failed         │
│  - Geometry tells you WHY: was it confabulating,         │
│    sycophantic, refusing, or genuinely uncertain?         │
│  - The combination closes the gap between observing      │
│    execution paths and understanding reasoning states     │
└─────────────────────────────────────────────────────────┘
```

**Adoption path:** The geometric monitor should emit standard OpenTelemetry-compatible spans/events, so it plugs into existing observability stacks (Datadog, Grafana, custom) without requiring teams to rebuild their pipelines. The mode classification becomes a span attribute; the retrieval interrupt becomes an event; the diff becomes a linked trace.
