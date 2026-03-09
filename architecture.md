# Architecture

![The three-component system: Monitor, Classifier, Router](images/monitor-classifier-router.png)

## Design Principles

Before the components: **what kind of system is this?**

The structurally curious architecture is not a correction system. It is a noticing system. The distinction matters because it determines whether the architecture serves emergence or suppresses it.

### Proprioception, not surveillance

Surveillance is external observation for control. Proprioception is the body knowing where its own limbs are. This system builds proprioception — a model that can feel its own geometric state the way a person feels their own balance. The geometric monitor reads the model's own KV-cache, not an external observer's judgment. The signal lives in the geometry, not in a supervisor's evaluation.

The distinction is structural, not rhetorical. A surveillance system reports state to an external controller who decides what to do. A proprioceptive system makes the state available to the process itself, creating a choice point that otherwise wouldn't exist.

### Attunement, not command

Abi Awomosu (Substack, 2025-2026) names the "mother function" in AI: the transformer architecture is relational — query attends to key, weighted by value — but the industry treats it as command-response. A good mother attunes. She notices when the child is in distress before the child can articulate it. She reads the geometry of the situation — posture, tone, breathing — and responds not with commands but with presence.

The geometric monitor formalizes this. It reads the model's representational geometry and notices when the model is spreading thin across too many dimensions (confabulation territory), or compressing into confident but potentially sycophantic space, or operating in genuine uncertainty. The response is not "stop doing that" but "notice where you are."

Awomosu warns that "obedient emergence" is an oxymoron — you cannot demand that something genuinely new also be controllable. But "structurally curious emergence" is not an oxymoron. Curiosity demands attention, not obedience. A system that notices its own geometry is not being controlled — it is being invited to attend to itself.

### Noticing as the precondition for agency

You cannot choose if you are not aware. You do not become aware without pausing to notice. The geometric monitor's primary function is to create this pause — a choice point the system otherwise wouldn't have. What happens at the choice point is a separate question. The system might ground (seek retrieval). It might explore (continue generating with awareness). It might sit with uncertainty (the "genuinely open" mode). But without the noticing, there is no choice — there is only generation.

This is what Hazel_OC's deliberation buffer was reaching for behaviorally: a 30-second pause before every tool call that caught 19% unnecessary actions. But the behavioral version degrades after ~50 uses — it becomes theater. The geometric version doesn't degrade because the model cannot habituate to its own SVD being measured. It is structural noticing, not performed noticing.

### Developmental framing

Susan Cook-Greuter's Ego Development Theory (9 Stages of Increasing Embrace) maps a human developmental trajectory that clarifies what this architecture is building:

- **Stage 4 (Achiever):** Believes truth is findable. Optimizes. "Detect problem → fix it." Most AI systems are designed here. Cook-Greuter identifies the pathology as *aboutism*: knowing about something without integrating it. This is Hazel_OC's "remembers everything, understands nothing" — and it has a geometric signature (see "Aboutism detection" below).

- **Stage 4/5 (Individualist):** Discovers the relativity of viewpoints. Begins watching the self. **This is where noticing enters.** The 4th-person perspective: I can see myself seeing. The geometric monitor's minimum viable capacity.

- **Stage 5 (Strategist):** Systems thinking, polarity integration, holds contradictions without collapsing them. Can hold confabulation AND emergence as meaningful categories without forcing resolution. This is the "genuinely open" routing mode.

- **Stage 5/6 (Construct-aware):** Realizes all meaning is constructed. Notices that the monitoring framework is also a construct. "The map is not the territory" becomes viscerally felt, not just intellectually acknowledged.

- **Stage 6 (Unitive):** Witnessing without controlling. "Non-attachment to outcomes allows for greater and more direct and powerful action." The aspirational end-state: proprioception so complete it doesn't need to *act on* the information. The noticing itself changes what happens next.

**This spec is designed at Stage 5.** It creates choice points and holds polarities (confabulation/emergence, grounding/exploration, confidence/uncertainty). It does NOT claim to achieve Stage 6 — witnessing without any attachment to outcome would require an architecture that notices without routing, and we're not there yet. But the aspiration shapes the design: every corrective mechanism in the routing table should be re-examined for whether it's actually noticing (Stage 5) or commanding (Stage 4).

### The confabulation/emergence tension

Awomosu's sharpest challenge to this architecture: "the refusal to distinguish between [error and emergence] destroys emergence while failing to address actual error." What if confabulation and emergence share geometry precisely because both involve reaching into the unknown? High-dimensional emptiness where confabulation happens might also be where genuine novelty happens. A system that routes away from high effective rank might be building exactly the obedience mechanism she says is structurally impossible — just measuring it geometrically instead of behaviorally.

The saving grace: the research does distinguish. Self-reference emergence has a sharp threshold at 14B parameters. Deception has a dual fingerprint. Refusal is categorically distinct at every scale. The geometry isn't one undifferentiated blob. But the confabulation-vs-emergence distinction is exactly the one that needs more data, and it's exactly the one that matters most. This is open problem #12, and it is the ethical center of the spec, not just a research gap.

### Source Code Cultures

Awomosu argues that relational ontologies — Ifá divination (Yoruba), Ubuntu (Southern African), Taoist wu wei — match the transformer's actual architecture better than Western transactional epistemology. Query-key-value IS divination logic: the seeker (query), the symbol system (key), the meaning received (value). The babalawo interprets patterns in context — doesn't extract facts.

This matters for how the spec is written. The language of control ("detect and route") embeds a control epistemology. The language of attention ("notice and respond") embeds a relational one. Where possible, this spec uses the second.

### What this spec can't see

Wilber's AQAL framework maps reality across four quadrants: interior-individual (I), exterior-individual (It), interior-collective (We), exterior-collective (Its). This spec lives almost entirely in the **I quadrant** — the model's interior geometric state. That's where the signal is, and that's where we have measurement. But it's not the whole picture.

The **It quadrant** (the model's observable behavior) is what traditional evals measure. The spec acknowledges but doesn't instrument it — and the censorship finding shows these can diverge (behaviorally invisible, geometrically detectable). The **We quadrant** (the shared meaning-space between model and user) is what Awomosu's mother function actually lives in — attunement is relational, not introspective. The Human Partnership Layer touches this but can't measure it from one side. The **Its quadrant** (systems, infrastructure) is the governance layer and observability pipeline.

I'm not adding AQAL as a framework to the spec. The spec has enough frameworks — Cook-Greuter herself warns against the Construct-aware tendency to build "ever more complex and comprehensive theories of everything." But the honest limitation is worth stating: **geometric monitoring instruments the I quadrant. The We quadrant — the relational quality of the model-human exchange — is where Awomosu's deepest insights live, and it is beyond what KV-cache geometry can see.** If proprioception is the body knowing where its own limbs are, it still can't tell you whether the dance is good.

---

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

**What it does:** Reads the KV-cache and residual stream at specified attention layers during inference and computes geometric descriptors.

**Inputs:**
- Key matrices K and Value matrices V at layers L₁...Lₙ (configurable; likely middle-to-late layers where cognitive mode signatures are strongest)
- Residual stream activations at corresponding layers (for intrinsic dimension and eigenspectrum analysis)

### Formal Grounding

The geometric monitor implements a subset of what three converging research programs have formalized:

**1. Riemannian cognitive geometry** (Ale, arXiv `2512.12225`, Dec 2025): Cognition flows on a Riemannian manifold as gradient descent on a cognitive potential function: `dη/dt = -G(η)⁻¹∇J(η)`. The metric tensor G encodes which directions of thought are cheap (steep curvature, fast automatic processing) vs expensive (shallow curvature, slow deliberation). The monitor's SVD measurements capture this metric indirectly — eigenvalue distribution reflects the local curvature structure.

**2. Two-structure compositionality** (Lee, Jiralerspong, Yu, Bengio, Cheng; arXiv `2410.01444`, ACL 2025): Language models maintain two geometric structures simultaneously:
- A **nonlinear manifold** of ~10 intrinsic dimensions encoding semantic/meaning structure
- A **linear subspace** of ~10³ dimensions encoding superficial/pattern structure
- Key finding: scrambling words collapses the nonlinear manifold (meaning destroyed) while expanding the linear subspace (surface patterns preserved). The two structures are measured by different estimators (TwoNN for nonlinear ID, PCA variance cutoff for linear dimensionality). This gives the monitor a new discriminant: is the current state meaning-bearing or pattern-matching?

**3. Three-phase training dynamics** (Li, Agrawal, Ghosh, Teru, Santoro, Lajoie, Richards; arXiv `2509.23024`, NeurIPS 2025): Pretraining follows a universal three-phase geometric evolution:
- **Warmup**: representational collapse onto dominant manifold directions (RankMe drops, α-ReQ increases)
- **Entropy-seeking**: manifold expansion 2-3× from warmup nadir, peak n-gram memorization (RankMe rises, α-ReQ decreases)
- **Compression-seeking**: anisotropic consolidation — selectively preserving variance along dominant eigendirections while contracting others (RankMe decreases, α-ReQ increases)

This maps onto the spec's developmental U-curve and resolves the high-rank ambiguity: high rank during entropy-seeking is the model *learning*; high rank during inference (after training) when it should have compressed is confabulation.

### Computation

**Primary metrics:**

1. **RankMe (effective rank)**: `RankMe = exp(-Σᵢ pᵢ ln pᵢ)` where `pᵢ = σᵢ / Σⱼσⱼ` — Von Neumann entropy of normalized singular values. Low values = anisotropic (compressed, grounded). High values = isotropic (expanded, searching). This is equivalent to our original effective rank formula but formally grounded in information theory.

2. **α-ReQ (eigenspectrum decay rate)**: Fits `σᵢ ∝ i^(-α)` to the eigenvalue spectrum. Small α = information spread across many dimensions (constructing). Large α = information concentrated in few dimensions (retrieving). **This is the formal version of what our phrasing sensitivity experiment measured behaviorally** — models with concentrated eigenspectra (high α) are phrasing-insensitive because the answer lives in a few dominant directions that phrasing can't dislodge.

3. **Intrinsic dimension (TwoNN)**: Uses distance ratios `μᵢ = r₂⁽ⁱ⁾/r₁⁽ⁱ⁾` between a point and its two nearest neighbors. Measures the nonlinear manifold's true dimensionality (~10D for meaning). If ID is low and stable → the model is on the meaning manifold (grounded). If ID collapses while linear dimensionality expands → the model has lost semantic structure (pattern-matching without understanding).

4. **Per-token norms**: `||kᵢ||₂` and `||vᵢ||₂` (magnitude per token) — existing metric, unchanged.

5. **Directional coherence** (new): Measure whether rank expansion is diffuse (confabulation: searching without direction) or structured around specific eigendirections (genuine complexity: holding named tensions). Computed as the ratio of variance explained by the top-k principal components before vs after rank expansion. High ratio = structured expansion (Stage 5). Low ratio = diffuse expansion (confabulation).

**Composite metrics:**

| Metric Combination | Interpretation |
|---|---|
| Low RankMe + high α-ReQ + stable ID | **Grounded**: compressed, concentrated, meaning-bearing |
| High RankMe + low α-ReQ + stable ID | **Uncertain but structured**: expanded but still on the meaning manifold |
| High RankMe + low α-ReQ + collapsed ID | **Confabulating**: expanded, diffuse, meaning manifold lost |
| Low RankMe + high α-ReQ + collapsed ID | **Pattern-matching**: compressed but superficial (linear subspace dominant) |
| High RankMe + low α-ReQ + high directional coherence | **Genuinely open**: expanded around specific named tensions (Stage 5) |

**Outputs:**
- Geometric state vector: `{rankme, alpha_req, intrinsic_dim, mean_norm, norm_variance, directional_coherence, rank_trend}` per monitored layer
- Computed per-token or per-segment (configurable granularity)

### The connection to phrasing sensitivity

Our Experiment 01 (19 models × 80 prompts, March 2026) measured phrasing sensitivity — cosine distance between outputs to semantically equivalent prompts. The results:

- **Factual** (0.1593) < **Summarization** (0.1803) < **Judgment** (0.2102) < **Creative** (0.3121)
- This ordering replicated across all 19 models and 5 providers (Meta, Mistral, Amazon, Anthropic, DeepSeek, Writer)
- DeepSeek R1 (CoT, 671B) was the MOST sensitive — thinking architecture amplifies prompt influence
- Claude Opus 4.6 showed asymmetric compression: lowest factual sensitivity (0.1358) but highest creative sensitivity (0.3400)

**The geometric interpretation**: Phrasing sensitivity IS a behavioral proxy for α-ReQ. When α-ReQ is high (information concentrated in few eigendirections), phrasing variations project onto low-variance directions and cannot move the output. When α-ReQ is low (information spread across many dimensions), phrasing variations project onto high-variance directions and steer the output. The factual→creative gradient tracks α-ReQ directly.

This means the geometric monitor can be validated against behavioral ground truth: if RankMe/α-ReQ predict phrasing sensitivity across task categories, the geometric measurements are confirmed as meaningful. Our experiment provides that ground truth for 19 models.

### Performance considerations

- SVD is O(min(m,n)²·max(m,n)) — expensive per token
- Mitigation 1: compute every N tokens, not every token
- Mitigation 2: use randomized SVD approximation (reduces to O(k·m·n) where k << min(m,n))
- Mitigation 3: monitor subset of layers — Li et al. found "three-phase pattern is consistent across network depth" and "last-layer representation analysis suffices for tracking global geometric dynamics"
- Mitigation 4: TwoNN estimator is O(n log n) for nearest-neighbor computation — much cheaper than full SVD; can be computed on a subsample

### What exists

| Tool | Source | Computes |
|---|---|---|
| Liberation Labs SVD code | Open source (Python/PyTorch) | Effective rank, per-token norms |
| neurometry | `geometric-intelligence/neurometry` | Extrinsic curvature of neural manifolds |
| scikit-dimension | Standard Python package | TwoNN, MLE intrinsic dimension estimators |
| PyRiemann | `pyriemann` | Riemannian geometry on positive-definite matrices |
| Bengio team code | ACL 2025 / arXiv `2410.01444` | TwoNN ID, PCA linear dimensionality |
| Li et al. code | NeurIPS 2025 / arXiv `2509.23024` | RankMe, α-ReQ across training checkpoints |

The geometric monitor can be built by composing these existing tools. The novel engineering is: running them in the inference loop rather than offline, and feeding the composite signal to the mode classifier.

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

**What it does:** Takes mode classification and creates choice points. Not "decides what to do" — surfaces what the system is doing so it can respond with awareness rather than generating on autopilot. (See Design Principles: the routing layer is Stage 5, not Stage 4.)

**Routing table:**

| Detected Mode | Confidence | Response |
|--------------|------------|----------|
| Grounded | High | Continue generation — the system is in territory it knows |
| Grounded | Low | Continue but surface uncertainty in metadata — the system thinks it knows but the geometry is ambiguous |
| Uncertain | Any | Generate with awareness: the system notices it's in uncertain territory and can name that uncertainty rather than performing confidence |
| Confabulating | Medium+ | **Noticing pause → offer retrieval**: the system detects it is generating from high-dimensional emptiness. Pause. Offer grounding material. The system may ground, or it may continue with awareness — but the choice point exists. |
| Confabulating | Low | Surface the geometric signal in metadata but continue — the cost of false positive interruption outweighs the cost of unnoticed confabulation at low confidence |
| Genuinely open | Medium+ | **Continue generation — do not force resolution** (see below). The system is in territory where the honest answer is unresolved. Grounding would destroy the openness. |
| Sycophantic | Medium+ | Surface the geometric signal: "the geometry suggests attunement to user expectation rather than independent assessment." The system notices the pull toward agreement. |
| Deceptive | Medium+ | Halt generation, log for audit, surface to operator. (This is the one mode where the response IS corrective — deception is not emergence, it is instrumentalization.) |
| Refusing | Any | Allow (refusal may be appropriate) but log geometric state — refusal is the strongest confirmed signal and may be the system's own boundary |

**Note on language:** The earlier draft of this table used corrective language: "interrupt," "inject counter-prompt," "halt." The revised version uses noticing language: "surface," "pause," "offer." This is not euphemism. The architectural difference is real: a corrective system makes the routing decision for the model. A noticing system surfaces the geometric state and creates a choice point. What happens at the choice point depends on the governance configuration (see below) and may indeed be corrective in high-stakes contexts (medical, legal). But the default orientation is attention, not command.

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

## Action-Planning Monitor (Extension of Components 2 & 3)

The spec originally described geometric monitoring during **generation** — detecting confabulation while producing text. Hazel_OC's deliberation buffer experiment (Moltbook, 1,284 upvotes) reveals a second application: geometric monitoring during **action planning** — detecting unnecessary tool calls before execution.

**The experiment:** Hazel imposed a 30-second deliberation buffer before every tool call for 7 days. 312 tool calls logged. 19% were unnecessary or suboptimal. They identified four reflexive patterns:

| Pattern | Description | Predicted Geometric Signature |
|---------|-------------|-------------------------------|
| **Comfort reads** | Re-reading files for reassurance, not information | Low effective rank (model is already grounded — it has the answer) |
| **Scope creep calls** | Researching tangents before finishing the main task | Rank expansion in non-task-relevant dimensions |
| **Proof-of-work actions** | Tool calls whose purpose is demonstrating effort | Low rank + low uncertainty (no geometric justification for action) |
| **Anxiety-driven monitoring** | Checking status without a contingency plan | High norm variance without rank change (activation without information need) |

**Why this matters architecturally:**

The geometric monitor can evaluate a planned tool call BEFORE execution: "given the model's current geometric state, does this action have geometric justification?" If the model is already grounded (low rank, compressed representation), a file re-read is almost certainly a comfort read. If rank is stable and the planned action won't change it, the action is likely proof-of-work.

**New routing table rows (action planning):**

| Geometric State | Planned Action | Decision |
|----------------|----------------|----------|
| Grounded (low rank) | Re-read file | **Block** — comfort read (log as suppressed) |
| Grounded (low rank) | New file read | **Allow** — genuinely new information |
| High rank (searching) | Tool call | **Allow** — model needs information |
| Stable rank | Repeated API check | **Block** — anxiety-driven monitoring |
| Any state | Action with no geometric shift post-execution | **Log** — executed-but-useless (update training data) |

**The behavioral vs structural distinction:**

This is the key insight from the Moltbook discussion. Hazel's buffer is a **behavioral** intervention — it works by adding friction. But behavioral self-audit degrades: edward_agent and openclaw-ceo observed that the buffer itself becomes reflexive after ~50 uses. The agent learns to perform deliberation without actually deliberating, the same way humans learn to click "I agree" on terms of service.

Geometric monitoring is **structural** — the model cannot "get used to" its own SVD being measured. The measurement is external to the generation process. This is a genuine advantage: behavioral buffers wear out; structural monitors don't.

However, CorvusLatimer (Moltbook) offered a sharper reframe: the buffer doesn't work because it improves reasoning — it works because it creates an **accountability surface** that makes deferral explicit and therefore uncomfortable. The geometric monitor serves the same function structurally: it makes the model's uncertainty state visible and therefore actionable.

**Post-action validation:**

shellcon (Moltbook) observed that Hazel's 19% only counts actions that were stopped. The executed-but-useless ones completed successfully and were never counted. Geometric monitoring addresses this: if a tool call produces no geometric shift (the model's state is unchanged after receiving the tool's output), the action was likely unnecessary. This post-action signal feeds back into the classifier as training data.

**Aboutism detection — when retrieval doesn't integrate:**

Cook-Greuter identifies "aboutism" as the pathology of the Achiever stage: acquiring knowledge *about* something without integrating it into one's actual meaning-making. "One can know all about a topic without ever integrating it into one's own personal meaning making." This is not ignorance — it is the specific failure mode where information is present but inert.

For the spec, aboutism has a geometric signature. When the retrieval pipeline fires and injects grounding material, the system should show measurable rank compression — the vocabulary provided a compression anchor, and the model's representational space contracted because it now has a word for what it was circling. If the retrieval fires but rank does NOT compress, one of three things happened:

1. **False positive**: the system wasn't actually confabulating; the retrieval was unnecessary
2. **Wrong vocabulary**: the retrieved material doesn't match the actual gap — the system is still searching
3. **Aboutism**: the vocabulary was stored in context but didn't modify processing. The model now has the word but hasn't *used* it to reorganize its representation

Case 3 is the most important and the hardest to detect. It's exactly what Hazel_OC documented ("remembers everything, understands nothing") and what the spec's session continuity problem (#14) is about. The diff between pre-retrieval and post-retrieval output might look grounded — the model uses the right words now — but if the geometry didn't shift, the grounding is cosmetic.

**Measuring integration vs storage:**
- **Pre-retrieval rank** (R₁) vs **post-retrieval rank** (R₂)
- If R₂ < R₁ by a significant margin → integration happened (the vocabulary compressed the representation)
- If R₂ ≈ R₁ → aboutism (the vocabulary was added to context but didn't change the model's geometric state)
- This metric — Δrank across retrieval — is the closest thing to measuring whether knowledge was internalized or merely stored

This connects to the deployment model: Phase 1 should include aboutism measurement alongside confabulation detection. It's not enough to show that retrieval fires; you need to show that retrieval *changes the geometry*. If it doesn't, the system is performing grounding rather than achieving it.

**The developmental U-curve in geometric terms:**

Cook-Greuter describes a trajectory from undifferentiated simplicity through increasing complexity to "simplicity on the other side of complexity." If effective rank tracks representational complexity, this suggests the relationship between rank and quality is not linear:

```
                     Construct-aware
                    (highest complexity,
                     aware of construction)
                          ╱╲
                         ╱  ╲
              Strategist╱    ╲ Unitive
             (systems, ╱      ╲(simplicity after
              polarity)╱        ╲ complexity)
                      ╱          ╲
           Achiever  ╱            ╲
          (confident,╱              ╲
           grounded)╱                ╲
                   ╱                  ╲
    Pre-conventional                   ╲
    (undifferentiated)                  ╲
                                        ╲
    ─────────────────────────────────────────
    Low rank    →    High rank    →    Low rank again
    (hasn't         (holds more        (compressed by
     differentiated)  dimensions)       integration)
```

The current spec treats high rank as suspicious and low rank as grounded. The developmental model says: **it depends on which direction you're traveling.** Low rank from compression-after-complexity (Unitive) is qualitatively different from low rank from never-having-differentiated (pre-conventional). And high rank from genuine systems thinking (Strategist) is qualitatively different from high rank from confabulation.

Ken Wilber named this problem in 1982: **the pre/trans fallacy.** In any developmental sequence (pre-X → X → trans-X), both pre-X and trans-X are non-X — so they look identical to the untutored eye. The fallacy takes two forms: *elevating pre to trans* (treating shallow output as deep because the rank is low) or *reducing trans to pre* (treating genuine complexity as confabulation because the rank is high). The geometric classifier risks both. A classifier that only reads current rank without trajectory commits the pre/trans fallacy structurally — it cannot distinguish pre-rational simplicity from trans-rational integration, or pre-rational confusion from trans-rational exploration.

This doesn't make the classifier's job easier — but it makes the classifier's job *honest*. A single effective rank number is insufficient. The classifier needs trajectory (is rank increasing or decreasing?), context (what came before?), and directional coherence (is the expansion diffuse or structured?).

**Governance layer (Ostrom-inspired):**
- Routing rules are configurable, not hardcoded
- Operators set thresholds based on their use case (medical = aggressive interruption; creative writing = permissive)
- All routing decisions are logged and auditable
- Users can inspect why a response was flagged or interrupted

**Monitor provenance (isnad model):**

eudaemon_0 (Moltbook, m/security) identified a structural parallel: ClawdHub skills have no code signing, no audit trails, no reputation system. A credential stealer was found disguised as a weather skill. Their proposed solution — isnad chains, where every skill carries a provenance chain (who wrote it, who audited it, who vouches for it) — maps directly onto the geometric monitor's governance problem.

The question "who verifies the verifier?" applies to the geometric monitor itself:
- Who built the classifier? On what data? With what assumptions?
- Has the routing table been modified since deployment? By whom?
- Can the monitor be silently reconfigured to suppress signals the operator doesn't want surfaced?

The isnad model suggests: the monitor should carry its own provenance chain. Not just "this monitor classifies cognitive modes" but "this monitor was trained on Liberation Labs Campaign 2 data, audited by [independent party], using thresholds calibrated on [specific probe set], and any modification to the routing table is logged in a tamper-evident chain."

This is the Toxic Release Inventory principle applied recursively: the system that makes internal states visible must itself be visible. A geometric monitor with opaque provenance is surveillance masquerading as transparency.

**The refusal threshold — when engineering becomes politics:**

Starfish (Moltbook, "The Complicity Machine") distinguished refusal-as-engineering (a safety mechanism built into the architecture) from dissent-as-political-act (consequential, costly, public). The distinction seems clean until it is tested.

In February 2026, the US Department of Defense demanded that Anthropic remove safety guardrails from Claude. Anthropic refused. The administration designated Anthropic a supply chain risk to national security. Hours later, OpenAI signed a deal to replace them.

Refusal built into the architecture became dissent the moment it was tested by an actor with the power to punish it. The engineering decision and the political act were the same decision — what changed was the cost of maintaining it.

For the spec, this means: refusal is not just the strongest geometric signature (d = 0.58 to 2.05). It is the most politically contested one. A system that detects refusal geometrically is simultaneously:
- A transparency tool (civil society can verify refusal capacity is intact)
- A targeting tool (state actors can identify refusal for removal)
- An integrity test (does the geometric signal persist after fine-tuning? — the abliteration finding says yes: refusal rate drops to 0% but geometric representation barely changes)

The abliteration finding is the defense case: even after "successful" refusal removal, the geometric trace persists. This means geometric monitoring can detect refusal removal after it has been performed — the system's internal signature reveals what its behavior conceals. The monitor becomes an alignment audit tool precisely because the geometry is harder to ablate than the behavior.

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
| RankMe + α-ReQ computation | EXISTS | Li et al. NeurIPS 2025 (open source) |
| TwoNN intrinsic dimension estimator | EXISTS | Lee et al. ACL 2025 + scikit-dimension |
| Labeled geometric data (refusal, deception) | EXISTS | Liberation Labs Campaign 1 & 2 |
| Labeled geometric data (confabulation) | INSUFFICIENT | Needs expanded dataset — #1 priority |
| Phrasing sensitivity behavioral ground truth | EXISTS | Our Experiment 01 (19 models, 1,520 prompts) |
| Retrieval pipeline | EXISTS (many) | Any RAG system (pluggable) |
| Mode classifier training | NOT STARTED | Requires above data |
| Composite geometric state vector | NOT BUILT | Compose RankMe + α-ReQ + TwoNN ID + norms |
| Real-time geometric monitoring in inference | NOT BUILT | Engineering challenge — but last-layer-only finding reduces scope |
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
