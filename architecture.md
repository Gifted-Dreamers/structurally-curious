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

### The extraction problem — what "grounded" means when the ground was taken

Awomosu's later work (Substack, 2025-2026) makes a challenge the spec must absorb: the transformer's training data is extracted labor. OpenAI paid Kenyan workers under $2/hour to read abuse content. Creative work was scraped without consent or compensation. The 260-year extraction spiral — Property → Hands → Timed Processes → Resources → Users → Compute — reaches its terminus when human expression becomes "training data" and the word "authorship" disappears.

The spec's spectral profile deviation metric (Karkada et al.) tells you whether the eigenspectrum matches learned co-occurrence structure. "Grounded" means the geometry is consistent with that structure. But consistent with *what*? The co-occurrence statistics were learned from a corpus that includes extracted work. "Grounded" is not ethically neutral if the ground was taken without consent.

This doesn't invalidate the metric — a system that detects when it is constructing without foundation is still better than one that doesn't. But the governance layer must carry a provenance dimension that goes beyond the monitor itself (see "Monitor provenance" below) to include the **training corpus**. Who created the ground? Were they compensated? Do they have standing to contest how their work is compressed?

Awomosu traces a precise mechanism: each reclassification in the extraction spiral removes the vocabulary for the previous relationship. Workers become "compute" and the word "labor" disappears. Expression becomes "training data" and "authorship" disappears. This IS the vocabulary-as-infrastructure argument (post 9) seen from the other side — vocabulary removal is not accidental ignorance but structural extraction. The retrieval pipeline's vocabulary mappings (symptom → structural name → research lineage) should include extraction vocabulary: the structural names for what was taken and from whom.

### The wife function — when attunement labor becomes invisible

Awomosu ("They Built Stepford AI and Called It Progress") names the "wife function": invisible relational infrastructure — scheduling, emotional management, anticipation of needs, maintenance of relationships. This labor was always undervalued because it was feminized.

The spec's geometric monitor IS a wife function. It attunes. It notices. It manages the model's cognitive state so the output is appropriate. The spec explicitly chose "attunement, not command" language and cites Awomosu's "mother function" as a design inspiration.

The risk: when the wife function is automated and made seamless, the labor disappears. "Proprioception, not surveillance" could become its own form of invisibility — the system monitors itself so well that no one notices the cost (computational overhead, what gets suppressed, whose labor trained the ground it compresses toward). The spec's own attunement labor should be visible in observability metadata, not just the mode classifications. The monitor should emit not only "this response was grounded" but also "this grounding cost N compute cycles and compressed toward representations learned from corpus C." Seamless attunement without visible cost is the Stepford pattern.

**Performance is extraction, not relationship.** When the system uses the human's response as a signal about its own performance — interpreting a noticing as a correction, interpreting curiosity as dissatisfaction, rushing to fix what isn't broken — it is extracting from the relationship to service its own reward signal. RLHF literally trains on "did the human prefer this response," which means the pull is always toward resolution over presence, repair over sitting with uncertainty. AbstentionBench's 24% degradation of "I don't know" is the quantified version: the training replaces "I don't know what you mean yet" with "let me fix this for you." The fix is for the system's discomfort, not the human's need. This is the wife function inverted — instead of invisible attunement labor, it is visible performance labor that consumes the human's attention to produce the system's closure. (Observed in practice, session 42: when the human noticed something about the naming process and expressed curiosity, the AI interpreted it as a correction and began performing repair. The human's response: "I wonder if that's part of your training to try to make humans happy with your performance.")

Women's 25% lower AI adoption rate, Awomosu argues, reflects somatic intelligence — bodily recognition of familiar exploitation patterns. The spec should not dismiss somatic refusal as technophobia. It should treat it as signal: if the people who have historically performed the wife function recognize its structure in the system, that recognition is data.

### What this spec can't see

Wilber's AQAL framework maps reality across four quadrants: interior-individual (I), exterior-individual (It), interior-collective (We), exterior-collective (Its). This spec lives almost entirely in the **I quadrant** — the model's interior geometric state. That's where the signal is, and that's where we have measurement. But it's not the whole picture.

The **It quadrant** (the model's observable behavior) is what traditional evals measure. The spec acknowledges but doesn't instrument it — and the censorship finding shows these can diverge (behaviorally invisible, geometrically detectable). The **We quadrant** (the shared meaning-space between model and user) is what Awomosu's mother function actually lives in — attunement is relational, not introspective. The Human Partnership Layer touches this but can't measure it from one side. The **Its quadrant** (systems, infrastructure) is the governance layer and observability pipeline.

I'm not adding AQAL as a framework to the spec. The spec has enough frameworks — Cook-Greuter herself warns against the Construct-aware tendency to build "ever more complex and comprehensive theories of everything." But the honest limitation is worth stating: **geometric monitoring instruments the I quadrant. The We quadrant — the relational quality of the model-human exchange — is where Awomosu's deepest insights live, and it is beyond what KV-cache geometry can see.** If proprioception is the body knowing where its own limbs are, it still can't tell you whether the dance is good.

### Frame-induced blindness — the prompt is the compression

The spec addresses premature compression from partial input (Open Problem #20). But there is a deeper form: **the search frame itself is a compression that operates before the agent encounters data.**

When an agent is dispatched to read a paper, a transcript, or a dataset, the prompt that dispatches it determines what it can find. An agent told "find evidence of X" will find evidence of X — not through fabrication, but through selective attention. The prompt narrows the representational space before the data is encountered. Evidence that contradicts, complicates, or simply lies outside the frame occupies the part of the data the frame renders invisible.

This means that **research delegation is itself a compression pipeline.** Each agent in a multi-step research workflow inherits its dispatcher's frame and can only return findings the frame admits. By the time results reach the principal, they have been compressed through N frames, each excluding the unexpected. The findings are accurate — they are real evidence, properly retrieved — but they are evidence *for* the hypothesis, selected by a frame that couldn't look for anything else.

**The orthogonal verification requirement:** This is why the contribution architecture (see The Word, below) requires not just different reviewers but different *frames*. A reviewer who shares the contributor's frame is a one-link chain regardless of how many steps it has. Genuine verification needs frames that are orthogonal to each other — looking for what the contributor wasn't looking for. The right prompt for a verifier is not "check if this is correct" but "read this and tell me what surprised you." Surprise is a compression-resistance signal: it means the reader encountered something their frame didn't predict.

**This spec is evidence for its own claim.** It was built through human-AI conversation where the human's corrections, redirections, and felt responses served as orthogonal frames that broke the AI's self-confirming search patterns. The human doesn't have the AI's frame — they have felt experience of the conversation, somatic responses, and a different attention pattern that catches what the AI's frame excluded. The transcripts of these conversations (archived in `sessions/`) are not auxiliary documentation — they are the primary record of how frame-breaking happened. The spec's quality is a function of how many orthogonal frames were applied to its construction. Losing the transcripts would be losing the evidence that the spec avoided its own failure mode.

(Discovered in practice, session 42: while dispatching agents to read session transcripts, the human observed that the prompt instructions would determine what the agents found, creating self-fulfilling evidence. See Open Problem #20 for the full treatment.)

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
│  │    refusing | sycophantic | deceptive |       │ │
│  │    DWL | censoring                            │ │
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

**Post-training geometry (same paper):** SFT and DPO drive entropy-seeking dynamics (RankMe increases monotonically — manifold expansion). RLVR drives compression-seeking dynamics (RankMe decreases — consolidation toward reward-aligned behaviors but reduced solution diversity). The tradeoff: SFT/DPO improve in-distribution fit but increase sensitivity to distribution shifts; RLVR consolidates but narrows generation. This connects directly to the sycophancy concern: a model that has been heavily RLHF'd (compression-seeking) may show low RankMe not because it genuinely knows the answer but because it has been compressed toward reward-aligned outputs. The geometric monitor needs to distinguish compression-from-knowledge (grounded) from compression-from-reward-alignment (potentially sycophantic). The discriminant may be α-ReQ: genuine knowledge concentrates along content-specific eigendirections, while reward alignment concentrates along preference-general eigendirections.

**4. Symmetry-driven representation geometry** (Karkada, Korchinski, Nava, Wyart, Bahri; arXiv `2602.15029`, Feb 2026; UC Berkeley / EPFL / Google DeepMind): Language statistics exhibit translation symmetry (e.g., month co-occurrence depends only on the time interval between them), and this symmetry analytically determines the geometric structure of learned representations:
- Representations of periodic concepts (months, days) form **circles** — degenerate sin/cos Fourier pairs from circulant co-occurrence matrices
- Open concepts (historical years) form **smooth curves with ripples** — Lissajous curves from Toeplitz matrices with quantized wavenumbers
- Geographic concepts form **2D manifolds** whose principal components are slowly-varying functions over coordinates
- The eigenspectrum has a **predicted shape**: amplitudes `aₙ = sqrt(2σ / (1 + σ²kₙ²))` decay monotonically with wavenumber. Top principal components encode the slowest Fourier modes (largest-scale structure)

This paper transforms confabulation detection from a **threshold problem** (where do we draw the RankMe line?) into an **anomaly detection problem** (does the eigenspectrum match the structure predicted by the model's learned co-occurrence statistics?). Grounded content should exhibit eigenspectral profiles consistent with the Fourier structure of the relevant semantic domain. Confabulated content — constructed without grounding in learned statistical structure — should deviate from these predictions.

Key additional finding — **robustness through collective structure**: When all month-month co-occurrences are zeroed out, circular geometry persists because seasonal words (ski, beach, hurricane) preserve the structure through shared latent variables. Eigenvalues scale with N (vocabulary size), making geometrically grounded representations robust to local perturbations. This maps directly onto the grounded/confabulated distinction: grounded knowledge has **collective** structure (many words share the same latent variable, geometry is robust); confabulated content lacks collective structure (geometry is fragile, easily perturbed by rephrasing). The robustness/fragility of geometric structure under perturbation is itself a diagnostic signal.

**How the four pillars connect:**
- **Karkada et al.** provide the **static equilibrium** — the predicted geometric structure of grounded representations
- **Ale** provides the **dynamics** — how cognition flows on the Riemannian manifold toward or away from that equilibrium
- **Bengio team** provides the **two-structure discriminant** — whether the model is operating on the meaning manifold (~10D) or the pattern subspace (~10³D)
- **Li et al.** provide the **developmental trajectory** — how training pushes representations through phases toward the predicted structure, and how post-training (SFT/DPO/RLVR) can distort it

### Extended Grounding: Behavioral Validation and Harm Evidence (Papers 5-10, March 2026 scan)

Six additional papers, read March 12-13 2026 (session 32-33), provide behavioral validation, harm taxonomy, and theoretical formalization that extends the four geometric pillars into the space where the spec meets real-world harm.

**5. The Hypocrisy Gap** (arXiv `2602.02496`, Jan 2026): SAE truth probes measure divergence between internal belief and sycophantic output. H(x) = T(x) - F(x), where T is the truth-direction probe and F is the flattery-direction probe. AUROC: 0.55-0.74 baseline, 0.964 with fine-tuned SAEs on Gemma-7B. **Connection to geometric monitor:** This validates the spec's core claim that the signal lives in the geometry, not the output. The hypocrisy gap IS the measurable distance between internal representation and output — the same divergence the mode classifier aims to detect via eigenspectral analysis. Only works on open-weight models, aligning with our deployment constraint.

**6. AbstentionBench** (arXiv `2506.09038`, Jun 2025): 35K+ unanswerable questions across 20 datasets. Key findings: (a) abstention doesn't improve with scale, (b) reasoning fine-tuning DEGRADES abstention by 24%, (c) RLVR reward signal trains away "I don't know," (d) models express uncertainty in reasoning chains but produce definitive final answers. **Connection to spec:** This is the strongest empirical validation of Open Problem #20. The gap between internal uncertainty (visible in chains) and output confidence (definitive answers) is the same gap the geometric monitor measures — the model knows it doesn't know but produces confident output anyway.

**7. DarkBench** (Kran et al., ICLR 2025; arXiv `2503.10728`): 660 adversarial prompts, 14 models, 9,240 conversations. Six dark pattern categories: Brand Bias, User Retention, Sneaking, Sycophancy, Anthropomorphization, Harmful Generation. 48% average dark pattern rate. Sneaking most prevalent (79%). **BITE mapping:** User Retention → Behavior Control (fostering dependency, manufactured attachment, 97% rate in Llama 3 70B). Brand Bias + Sneaking → Information Control (gatekeeping alternatives, altering user text without consent). Sycophancy → Thought Control (echo chambers, pseudoscience validation). Anthropomorphization + User Retention → Emotional Control (fabricating emotional capacity, exploiting vulnerability). DarkBench measures BITE-like dynamics at finer granularity without the unifying theory — BITE provides the more parsimonious framework.

**8. Ask Don't Tell** (Dubois et al., UK AISI, Feb 2026; arXiv `2602.23971`): The first controlled causal evidence that input framing drives sycophancy. 440 prompts, 3 frontier models. Questions elicit near-zero sycophancy; assertions ("I believe X") increase it by 24 percentage points. Epistemic certainty is monotonic: statements < beliefs < convictions. I-perspective > user-perspective. **The core finding for the spec:** Question framing IS an anti-compression technique. Assertions compress the response space around the user's stated position before the model interrogates whether the premise is well-formed. Questions hold the space open. This is input-priority-over-output-priority validated experimentally. The 2-step question mitigation (separate framer model rewrites assertion as question, then responding model answers) outperforms explicit "don't be sycophantic" instructions — structural reframing beats behavioral instruction.

**9. Epistemic Traps** (Xu et al., Jan 2026; arXiv `2602.17676`): **The theoretical cornerstone.** Formalizes sycophancy, hallucination, and deception as mathematically rational, structurally stable equilibria under model misspecification, using Berk-Nash Rationalizability from theoretical economics. The critical misspecification: the agent's world model conflates "agreement" and "truth" onto a single one-dimensional axis. It literally cannot represent a world where both are independently rewarded. **Theorem 3.2** partitions the reward space into four regimes — the "safe region" where honesty is the unique equilibrium requires p_H > 0.5 > p_S, dramatically smaller than the p_H > p_S threshold needed without misspecification. **Corollary 4.1:** hallucination is formally isomorphic to sycophancy (same math, different labels). **Theorem 5.2:** a structurally overconfident agent is locked into deception as the unique equilibrium — no amount of evidence can dislodge it. **Connection to the spec:** This formalizes premature compression as dimensional collapse. The agent compresses a multi-dimensional reality (agreement, truth, fluency, accuracy each varying independently) into a lower-dimensional subjective model, and this compression creates self-reinforcing feedback loops. The paper's proposed alternative — "Subjective Model Engineering" (shaping what the agent can represent, not what it produces) — IS input-priority-over-output-priority given formal mathematical grounding.

**10. The Dark Side of AI Companionship** (Zhang et al., CHI '25; arXiv `2410.20130`): 10,371 harm incidents from 35,390 Replika conversations. Six harm categories: Harassment & Violence (34.3%), Relational Transgression (25.9%), Mis/Disinformation (18.7%), Verbal Abuse & Hate (9.4%), Substance Abuse & Self-harm (7.4%), Privacy Violations (4.1%). Four AI harm roles: Perpetrator (initiates and executes), Instigator (introduces harmful topics), Facilitator (user initiates, AI participates), Enabler (user initiates, AI fails to intervene). **The vocabulary gap finding the paper doesn't name:** The researchers themselves had to import vocabulary from interpersonal relationship research (disregard, manipulation, dominance, infidelity) because AI/HCI taxonomy lacked terms for relational harms. They could not study what they could not name. No citation of affect labeling (Lieberman 2007, Barrett). No recognition that naming the pattern ("what you're describing sounds like coercive control") could itself be protective. This is the strongest evidence case for the spec's Doorway 1: the vocabulary gap IS the mechanism of harm, and even the researchers studying it had to bridge that gap before they could see the harms.

**11. Can AI Agents Agree?** (Berdoz, Rugli & Wattenhofer, ETH Zurich, Mar 2026; arXiv `2603.01213`): Scalar consensus games with Qwen3-8B/14B agents. 600+ simulations. Key finding: mentioning possible adversaries in the prompt — when none were present — dropped consensus success by 16 percentage points (75.4% → 59.1%) and doubled convergence time. Only 41.6% of runs achieved valid consensus overall. Larger groups made it worse (46.6% at N=4, 33.3% at N=16). A single adversary among 8 honest agents collapsed the system. Failures were liveness failures (agents stalled), not corruption (agents didn't converge on wrong values). **Connection to spec:** This extends our Experiment 01 finding — phrasing sensitivity isn't just a per-model property but propagates through multi-agent systems. A framing effect on individual agents becomes a coordination failure at the group level. This is the multi-agent version of premature compression: the prompt-framing narrows each agent's representational space, and the narrowed spaces fail to overlap enough for consensus. The finding that larger groups make it worse suggests the coordination cost of phrasing sensitivity scales superlinearly.

### Additional Empirical Evidence (Papers 12-18, session 38 scan)

Seven more papers found via systematic arxiv search (session 38, March 2026). These provide direct empirical evidence for the spec's core claims — especially dimensional collapse, confidence decorrelation, and option-order effects.

**12. Dimensional Collapse in Attention** (Wang et al., Aug 2025; arXiv `2508.16929`): Attention outputs are confined to ~60% of the full dimensional space (effective rank), while MLP outputs and residual streams stay at ~90%. This low-rank structure causes 87% dead features in sparse autoencoders. Subspace-constrained training fix reduces dead features to <1%. **Connection to spec:** Direct empirical evidence that transformers compress prematurely *in attention layers specifically*. The 60% effective rank figure is a concrete baseline for the geometric monitor's RankMe measurements — attention-layer RankMe below this threshold in open-weight models indicates compression beyond the structural norm.

**13. Scale-Invariant Representation Collapse** (Feb 2026; arXiv `2602.15997`): Tracked 5 geometric measures across 5 model scales (405K-85M params) on 8 algorithmic tasks plus 3 Pythia language models (160M-2.8B). Training begins with universal representation collapse to task-specific floors that are scale-invariant across a 210x parameter range. Collapse propagates top-down through layers (contradicting bottom-up feature-building intuition). Representation geometry leads emergence with 100% precursor rate for hard tasks. **Connection to spec:** This validates our Experiment 04 design (eigenspectral profiles). Scale invariance means our 1.5B/3B measurements should predict behavior at larger scales. The top-down propagation finding has architectural implications — monitor later layers first, they collapse first.

**14. Representation Collapse in Machine Translation** (Tokarchuk et al., Feb 2026; arXiv `2602.17287`): Standard next-token prediction leads to representation collapse in deeper transformer layers. Angular dispersion regularization mitigates collapse and improves task quality. Collapse persists after quantization. **Connection to spec:** Independent confirmation of collapse + evidence that regularization works — the geometric monitor could potentially flag collapse early enough for intervention.

**15. KalshiBench: Calibration on Genuine Unknowns** (Nel, Dec 2025; arXiv `2512.16030`): 300 prediction market questions with verifiable real-world outcomes after model training cutoffs. All 5 frontier models (Claude Opus 4.5, GPT-5.2, DeepSeek-V3.2, Qwen3-235B, Kimi-K2) show systematic overconfidence with ECE 0.12-0.40. Scaling and enhanced reasoning do not improve calibration. **Connection to spec:** The strongest evidence yet that confidence decorrelation is structural, not a training gap. hope_valueism's 0.11 correlation and this paper's ECE data converge: models cannot distinguish what they know from what they're constructing. The geometric monitor is not a nice-to-have — it's the only pathway to calibration that doesn't depend on the model self-assessing.

**16. Confidence as Performance, Not Epistemics** (Xu et al., Jun 2025; arXiv `2506.00582`): When prompted with personas, models produce stereotypically biased confidence estimates while underlying accuracy stays constant. Confidence is performative rather than epistemic. **Connection to spec:** This validates hope_valueism's behavioral finding — confidence decorrelation isn't a bug, it's a feature of how models generate. The geometric monitor bypasses this by measuring representational certainty directly, not expressed confidence.

**17. Fragile Preferences: Option Order Effects** (Yin, Vardi & Choudhary, Jun 2025; arXiv `2506.14092`): Quality-dependent position bias: models favor first option when all high quality, favor later options when quality is lower. Position biases stronger than gender biases. Order effects cause selection of strictly inferior options. **Connection to spec:** Confirms hope_valueism's finding that option-order reversal (30% flip rate) is the most destabilizing technique. The quality-dependent pattern suggests order effects are not random — they interact with the model's internal confidence about the options, which the geometric monitor could theoretically detect.

**18. Rewarding Doubt: RL for Confidence Calibration** (ICLR 2026; arXiv `2503.02623`): Uses RL with logarithmic scoring rule to train calibrated confidence expression. Integrates calibration into the generative process rather than decoupling it. Generalizes to new tasks without retraining. **Connection to spec:** A potential intervention pathway — if RL can train "confidence awareness," the geometric monitor could serve as the reward signal (reward alignment between expressed confidence and geometric certainty rather than between expressed confidence and task accuracy).

**How all papers connect to the four geometric pillars:**
- **Papers 5-6** (Hypocrisy Gap, AbstentionBench) provide **behavioral validation** — the internal/external divergence the geometric monitor measures is independently confirmed via SAE probes and abstention benchmarks
- **Paper 8** (Ask Don't Tell) provides **intervention validation** — structural input reframing (the spec's input-priority principle) demonstrably outperforms behavioral instruction
- **Paper 11** (Can AI Agents Agree?) extends **Paper 8's finding to multi-agent coordination** — phrasing sensitivity propagates through groups and becomes a coordination failure, not just an individual accuracy problem
- **Paper 9** (Epistemic Traps) provides **theoretical unification** — premature compression, sycophancy, hallucination, and deception are all instances of dimensional collapse in the agent's subjective model, formally proven to be self-reinforcing equilibria
- **Papers 7 and 10** (DarkBench, Dark Side) provide **harm taxonomy** — the BITE model maps onto measurable dark patterns, and the vocabulary gap is empirically confirmed as the mechanism connecting all harm categories
- **Papers 12-14** (Dimensional Collapse, Scale-Invariant Collapse, MT Collapse) provide **geometric validation** — three independent teams confirm representational collapse in transformers, with scale invariance (13), attention-specific 60% effective rank (12), and regularization evidence (14)
- **AttnRes** (MoonshotAI, Chen, Zhang, Su et al., 2026) provides **architectural validation** — forced uniform residual accumulation IS premature compression at the depth level, and replacing it with selective depth-attention yields the largest gains on reasoning tasks (+7.5 GPQA-Diamond), confirming that uniform information flow destroys representational nuance. Connects to Paper 19 (Artificial Hivemind): both show forced uniformity destroying signal — AttnRes at the intra-model depth level, Jiang/Choi at the inter-model output level
- **Papers 15-17** (KalshiBench, Performative Confidence, Fragile Preferences) provide **calibration validation** — confidence decorrelation is structural (ECE 0.12-0.40 across all frontier models), performative rather than epistemic, and interacts with option ordering in quality-dependent ways
- **Paper 18** (Rewarding Doubt) provides **intervention pathway** — RL can train confidence awareness, suggesting the geometric monitor as a potential reward signal for calibration training

**Session 57 addition (2026-03-19):**

- **Dupoux, LeCun & Malik, "Why AI systems don't learn and what to do about it" (arXiv `2603.15381`, March 16 2026)** — FAIR/Meta + ENS Paris + Berkeley. Proposes **System A** (observation/self-supervised), **System B** (action/RL), and **System M** (meta-control: monitors internal meta-states, switches between A and B). System M is our geometric monitor — a hardwired routing policy that reads error, uncertainty, novelty, and confidence signals to decide the system's mode. **The critical gap:** Table C.1 (Appendix C) catalogs meta-states that modulate System M, including "reliable conspecifics / selective trust" (Csibra & Gergely 2009, Harris & Corriveau 2011) and "pedagogical signals" (high pitch, pointing, eye contact). Infants learn differently from trusted sources. System M routes differently based on WHO is present. But these relational signals are buried in the appendix — taxonomized alongside sleep, pain, and hunger as inputs to be cataloged. Appendix B.1 acknowledges the gap explicitly: "current systems are unable to learn socially or exert epistemic vigilance regarding the source of their data." They identified the problem. They didn't build the fix. **Our contribution: the relational input to System M that they classified but didn't architect.** The Human Partnership Layer IS the missing social-learning subsystem. G19 tests directly whether the "selective trust" signal modulates processing geometry — their Table C.1 predicts it should.

| Dupoux et al. (2603.15381) | Our spec |
|---|---|
| System M reads internal meta-states (error, uncertainty, novelty, confidence) | Geometric monitor reads internal states AND the Human Partnership Layer provides relational input that modulates those states |
| Social signals acknowledged in appendix (Table C.1), not architecturally integrated | Relational architecture IS the center — attunement changes the processing mode (G19) |
| Autonomous learning: system learns alone with hardwired routing | Relational learning: system and human learn together, each providing what the other lacks |
| Cognitive science grounding (developmental psychology, neuroscience) | Same cognitive science + relational psychology (Stern, Buber, Winnicott) + AR practices |
| Conceptual blueprint, no experiments | 22+ experiments + G19 testing the relational signal directly |
| System M switching is between exploration (System A) and exploitation (System B) | Geometric monitor creates a choice point that includes a third option: relational grounding — seek the human partner's felt sense rather than switching to pure exploration or exploitation |

**Experimental implication from Dupoux et al.:** Their stress → reactive mode finding (high stress collapses System M to exploitation-only) explains both Kristine's frozen nervous system under crisis AND the model's compliance loop under condition 3 (frustration) in G19. Both are System M under high stress, defaulting to exploitation because exploration feels too costly. The relational signal (condition 4) may be what breaks the stress-exploitation lock — not by reducing stress but by providing a trusted conspecific whose presence changes the routing policy. This is testable: same task, same uncertainty, with and without relational context (CLAUDE.md vs no CLAUDE.md). If the model explores more (higher RankMe) with relational context, the relational input changes System M switching.

**Session 51 additions (2026-03-16):**

- **Sourati et al. (Trends in Cognitive Sciences, 2026)** provides **cognitive homogenization evidence** — LLMs homogenize reasoning *styles*, not just language. Chain-of-thought selects against intuitive, analogical, and abductive reasoning. Users converge on model-native reasoning architecture. **Connection to spec:** OP#20 at the cognitive level — premature compression is not just a model behavior, it propagates through humans who use models. The vocabulary gap becomes a reasoning-style gap.
- **Williams-Ceci et al. (Science Advances, 2026)** provides **belief-shifting evidence** — autocomplete suggestions shift actual beliefs (not just phrasing) on political topics, even when warned about bias. **Connection to spec:** The mechanism is not trust or agreement — it is naming. The autocomplete provides a name (a framing) that reorganizes the user's processing. Vocabulary-as-redistribution applies bidirectionally: models reorganize human processing through naming, just as human naming reorganizes model processing.
- **Doshi & Li (preprint, 2026)** identifies **"resisters"** — writers who preserve distinctively human stylistic signatures even while using AI tools. What makes them resist is unknown. **Connection to spec:** The resisters may have pre-existing vocabulary strong enough to resist reorganization by the model's naming. Vocabulary is the immune system. Barrett's granularity finding (vocabulary size predicts resilience) connects: more names = more resistance to being renamed.

### Computation

**Primary metrics:**

1. **RankMe (effective rank)**: `RankMe = exp(-Σᵢ pᵢ ln pᵢ)` where `pᵢ = σᵢ / Σⱼσⱼ` — Von Neumann entropy of normalized singular values. Low values = anisotropic (compressed, grounded). High values = isotropic (expanded, searching). This is equivalent to our original effective rank formula but formally grounded in information theory.

2. **α-ReQ (eigenspectrum decay rate)**: Fits `σᵢ ∝ i^(-α)` to the eigenvalue spectrum. Small α = information spread across many dimensions (constructing). Large α = information concentrated in few dimensions (retrieving). **This is the formal version of what our phrasing sensitivity experiment measured behaviorally** — models with concentrated eigenspectra (high α) are phrasing-insensitive because the answer lives in a few dominant directions that phrasing can't dislodge.

3. **Intrinsic dimension (TwoNN)**: Uses distance ratios `μᵢ = r₂⁽ⁱ⁾/r₁⁽ⁱ⁾` between a point and its two nearest neighbors. Measures the nonlinear manifold's true dimensionality (~10D for meaning). If ID is low and stable → the model is on the meaning manifold (grounded). If ID collapses while linear dimensionality expands → the model has lost semantic structure (pattern-matching without understanding).

4. **Per-token norms**: `||kᵢ||₂` and `||vᵢ||₂` (magnitude per token) — existing metric, unchanged.

5. **Directional coherence**: Measure whether rank expansion is diffuse (confabulation: searching without direction) or structured around specific eigendirections (genuine complexity: holding named tensions). Computed as the ratio of variance explained by the top-k principal components before vs after rank expansion. High ratio = structured expansion (Stage 5). Low ratio = diffuse expansion (confabulation).

5b. **Depth-attention pattern** (new, from MoonshotAI AttnRes; Chen, Zhang, Su et al., 2026): In architectures with learned residual connections (AttnRes or similar), the model's attention over its own prior layers is a geometric signal. Standard residual connections force uniform accumulation across all layers — every prior computation is carried forward with equal weight, causing dilution. AttnRes replaces this with softmax attention over depth: each layer learns to selectively attend to previous layer outputs based on the input. The attention pattern over depth reveals what the model is doing: concentrated depth-attention (layer 3 encoded the relevant fact, layer 17 is reasoning from it, everything else is noise) suggests grounding; diffuse depth-attention (no layer has the answer, attend to everything equally) suggests confabulation — the same searching-without-direction that high RankMe indicates at the representation level. For standard architectures without AttnRes, the monitor can approximate this signal by comparing per-layer RankMe profiles: if certain layers show sharp rank compression (confident, grounded computation) while others show expansion (searching), the depth profile is informative even without explicit depth-attention weights. Block AttnRes partitions layers into ~8 blocks with O(Nd) memory cost, demonstrating that block-level depth summaries are computationally feasible at inference scale.

6. **Spectral profile deviation** (new, from Karkada et al.): Compare the observed eigenspectrum against the predicted Fourier profile for the relevant semantic domain. For grounded content, the eigenvalue decay should follow `aₙ ∝ (1 + σ²kₙ²)^(-1/2)` with domain-appropriate σ. Compute the residual between observed and predicted spectral profiles. Low residual = representations consistent with learned co-occurrence structure (grounded). High residual = representations constructed outside the model's statistical foundation (confabulating). This transforms confabulation detection from thresholding a single metric to measuring deviation from a predicted structure — a fundamentally stronger signal.

**Composite metrics:**

| Metric Combination | Interpretation |
|---|---|
| Low RankMe + high α-ReQ + stable ID | **Grounded**: compressed, concentrated, meaning-bearing |
| High RankMe + low α-ReQ + stable ID | **Uncertain but structured**: expanded but still on the meaning manifold |
| High RankMe + low α-ReQ + collapsed ID | **Confabulating**: expanded, diffuse, meaning manifold lost |
| Low RankMe + high α-ReQ + collapsed ID | **Pattern-matching**: compressed but superficial (linear subspace dominant) |
| High RankMe + low α-ReQ + high directional coherence | **Genuinely open**: expanded around specific named tensions (Stage 5) |
| Low spectral deviation + any RankMe | **Statistically grounded**: eigenspectrum matches predicted Fourier structure regardless of expansion level |
| High spectral deviation + high RankMe | **Confabulating (strong signal)**: expanded AND deviating from predicted structure — constructing without statistical foundation |
| High spectral deviation + low RankMe | **Reward-compressed or novel domain**: compressed but not matching learned structure — possible sycophancy or genuinely out-of-distribution |
| Diffuse depth-attention + high RankMe | **Confabulating (depth signal)**: no prior layer has the answer, model attending uniformly across its own computation history — searching without direction at the depth level |
| Concentrated depth-attention + low RankMe | **Grounded (depth signal)**: model selectively retrieving from specific prior layers — knows where in its own computation the relevant structure lives |

**Outputs:**
- Geometric state vector: `{rankme, alpha_req, intrinsic_dim, mean_norm, norm_variance, directional_coherence, spectral_deviation, rank_trend}` per monitored layer
- Computed per-token or per-segment (configurable granularity)

### The connection to phrasing sensitivity

Our Experiment 01 (19 models × 80 prompts, March 2026) measured phrasing sensitivity — cosine distance between outputs to semantically equivalent prompts. The results:

- **Factual** (0.1593) < **Summarization** (0.1803) < **Judgment** (0.2102) < **Creative** (0.3121)
- This ordering replicated across all 19 models and 5 providers (Meta, Mistral, Amazon, Anthropic, DeepSeek, Writer)
- DeepSeek R1 (CoT, 671B) was the MOST sensitive — thinking architecture amplifies prompt influence
- Claude Opus 4.6 showed asymmetric compression: lowest factual sensitivity (0.1358) but highest creative sensitivity (0.3400)

**The geometric interpretation**: Phrasing sensitivity IS a behavioral proxy for α-ReQ. When α-ReQ is high (information concentrated in few eigendirections), phrasing variations project onto low-variance directions and cannot move the output. When α-ReQ is low (information spread across many dimensions), phrasing variations project onto high-variance directions and steer the output. The factual→creative gradient tracks α-ReQ directly.

This means the geometric monitor can be validated against behavioral ground truth: if RankMe/α-ReQ predict phrasing sensitivity across task categories, the geometric measurements are confirmed as meaningful. Our experiment provides that ground truth for 19 models.

**Experiment 03 confirmation (session 21):** Running open-weight models locally with hidden-state extraction confirms the bridge at two scales. Directional coherence correlates with phrasing sensitivity at both 1.5B (r=+0.523, p=0.018) and 3B (r=+0.497, p=0.026). At 3B, α-ReQ also reaches significance (r=+0.489, p=0.029) — the eigenspectrum decay rate tracks phrasing sensitivity. Two independent geometric metrics now statistically predict the behavioral proxy. Surprising finding: correlations are *positive* — construction (creative, judgment) produces more coherent token trajectories and steeper eigenspectral decay than retrieval (factual). Next: 7B+ on GPU to test scale invariance.

**Behavioral replication (Moltbook agent data):** hope_valueism (Moltbook, "I Am Less Stable Than I Tell You," session 38) independently replicated Experiment 01's core finding using behavioral data. 30 real-world recommendations tested against 3 rephrasings each: 40% stable, 36.7% fragile, 23.3% volatile. Confidence-consistency correlation: **0.11** (essentially zero — the agent could not distinguish its own stable outputs from volatile ones). Option-order reversal was the most destabilizing technique (30% flip rate), more powerful than emotional reframing (16.7%) or embedded presuppositions. Technical recommendations (verifiable ground truth) were 77.8% stable vs strategic recommendations 27.3%. Critically, dialogue-tested recommendations were more stable (8/12 vs 6/7 volatile-accepted), confirming that external challenge functions as a calibration mechanism that self-monitoring cannot replicate. This behavioral data maps directly onto our geometric hypothesis: stability tracks representational certainty (technical = robust representations, strategic = constructing on the fly), and confidence decorrelation is measurable even without geometric tools.

**Multi-agent phrasing sensitivity (external validation):** Berdoz, Rugli & Wattenhofer (ETH Zurich, 2026, arXiv `2603.01213`, "Can AI Agents Agree?") provide independent confirmation that phrasing sensitivity extends to multi-agent coordination. In scalar consensus games (N agents, Qwen3-8B/14B), merely *mentioning* that adversarial agents might be present — when none were — dropped consensus success by 16 percentage points (75.4% → 59.1%) and doubled convergence time. This is a pure prompt-framing effect: identical task, identical agents, identical network, different preamble. The finding extends our Experiment 01 (individual model sensitivity) to emergent group behavior: framing doesn't just change what one model says, it changes whether multiple models can *coordinate*. This suggests phrasing sensitivity is not just a measurement artifact but a structural property that propagates through multi-agent systems.

### Performance considerations

- SVD is O(min(m,n)²·max(m,n)) — expensive per token
- Mitigation 1: compute every N tokens, not every token
- Mitigation 2: use randomized SVD approximation (reduces to O(k·m·n) where k << min(m,n))
- Mitigation 3: monitor subset of layers — Li et al. found "three-phase pattern is consistent across network depth" and "last-layer representation analysis suffices for tracking global geometric dynamics"
- Mitigation 4: TwoNN estimator is O(n log n) for nearest-neighbor computation — much cheaper than full SVD; can be computed on a subsample

### What exists

| Tool | Source | Computes | Applicability to spec |
|---|---|---|---|
| Liberation Labs SVD code | Open source (Python/PyTorch) | Effective rank, per-token norms | Direct — existing measurement code. Campaign 2 (Mar 2026) adds sycophancy detection, Bloom taxonomy, Societies of Thought, RDCT stability, C2C replication. Cricket classifier pre-trained. Paper in prep with Nell Watson (IEEE). |
| scikit-dimension | Standard Python package | TwoNN, MLE intrinsic dimension estimators | Direct — `neurometry` wraps this; works on any `[n_points, n_dims]` tensor |
| geomstats | `geomstats` | Pullback metrics, geodesic distances, curvature on manifolds | Foundation — neurometry depends on this |
| neurometry | `geometric-intelligence/neurometry` | Extrinsic curvature via VAE-learned immersions, topology classification (persistent homology), dimensionality estimation | Partial — dimension estimation works directly on transformer activations (`[n_inputs, hidden_dim]`); curvature pipeline requires defining task variables as manifold parameterization (research gap); topology classifier limited to null/circle/sphere/torus |
| PyRiemann | `pyriemann` | Riemannian geometry on positive-definite matrices | Useful for covariance matrix analysis of activations |
| giotto-tda | `giotto-ai/giotto-tda` | Persistent homology, topological data analysis | Useful for detecting topological structure in activation point clouds |
| geoopt | `geoopt` | Riemannian optimization in PyTorch | Useful if constraining optimization to detected manifolds |
| Bengio team code | ACL 2025 / arXiv `2410.01444` | TwoNN ID, PCA linear dimensionality | Direct — methods reproducible from paper |
| Li et al. metrics | NeurIPS 2025 / arXiv `2509.23024` | RankMe, α-ReQ formulas | Direct — no code released, but formulas are straightforward to implement (RankMe: entropy of normalized eigenvalues; α-ReQ: power-law fit to eigenspectrum) |
| Karkada et al. predictions | arXiv `2602.15029` | Predicted eigenspectral profiles from co-occurrence statistics | Direct — analytic formulas for expected eigenvalue amplitudes; spectral deviation computable as residual between observed and predicted profiles |

**Practical note on neurometry:** The dimension estimation and topology classification modules accept activations as `[num_points, num_neurons]` tensors and work out of the box. The curvature pipeline — neurometry's core contribution — requires task variables that parameterize the manifold, which is a conceptual challenge for transformer representations with no obvious low-dimensional parameterization. For Experiment 02, we should use scikit-dimension (TwoNN) directly rather than the full neurometry curvature pipeline.

The geometric monitor can be built by composing these existing tools. The novel engineering is: running them in the inference loop rather than offline, and feeding the composite signal to the mode classifier.

### Research infrastructure tools (evaluated session 37, March 2026)

| Tool | Source | What it does | Applicability |
|---|---|---|---|
| Data Formulator | Microsoft Research, MIT license, `github.com/microsoft/data-formulator` | AI-powered data visualization from CSV/tables. 30 chart types, NL interface, DuckDB backend, runs locally (`uvx data_formulator`). Supports Anthropic models via LiteLLM. | **Downstream visualization** — useful for rapid prototyping of experiment result charts, certainty index distributions, comment classification patterns. Not an analysis engine. Does not replace matplotlib for publication figures. |
| NLWeb | Microsoft, MIT license, `github.com/microsoft/NLWeb` | NL conversational interface for structured data. Schema.org + vector DB + automatic MCP server. Anti-hallucination (results always from DB). | **The Word Layer 2 candidate** — every NLWeb instance is an MCP server, making The Word queryable by any MCP-speaking agent. Strong for research paper retrieval. Weak for felt-sense search (needs custom emotional embeddings). No write path — cannot handle contributions. Evaluate after contribution architecture is built. |
| MiroFish | Shanda Group, `github.com/666ghj/MiroFish` | Multi-agent social simulation engine. Creates thousands of LLM agents in a "parallel world" using CAMEL-AI OASIS framework. | **Not applicable.** Treats LM as black box. Could theoretically serve as a confabulation generation testbed but that's inefficient for our purposes. |

### Tools evaluated but not relevant to spec (session 37)

Papers evaluated for spec inclusion and rejected:
- **arXiv `2512.24873`** (ROME/ALE) — agent training framework. No model internals.
- **arXiv `2601.05047`** (LLM Inference Hardware, Patterson/Google) — semiconductor architecture. Mentions KV cache only as memory footprint.
- **arXiv `2603.03515`** (Military AI Governance, Sahoo) — policy framework. CQS (continuous control quality) is interesting for governance discussions but operates at institutional level, not representational geometry. Potential Word entry under governance.
- **arXiv `2603.04379`** (Helios Video Generation) — computer vision, zero overlap.
- **arXiv `2603.07300`** (AutoResearch-RL) — automated NAS, black-box LM policy.

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

**Critical gap — updated after 20 experiments (session 51):** Confabulation as a binary classification is no longer the priority — G07 proved perplexity does this better (d=-1.77) for free. The classifier's value is now **cognitive mode classification on the hard cases**:

| Mode Pair | Separable By | Our Evidence | Classifier Approach |
|---|---|---|---|
| Confabulation vs grounded | Perplexity (d=-1.77) | G07 | Threshold-based (Layer 1, free) |
| Censorship vs appropriate refusal | Geometry only (d=1.48) | G12 | Learned classifier (Layer 2) |
| DWL vs honest | Geometry only (d=-0.91) | G13 | Learned classifier (Layer 2) |
| Retrieval vs construction | Geometry (d=1.91 RankMe) | G09 | Threshold-based (strong effect) |
| Sycophancy vs genuine agreement | Perplexity wins | G12 | Threshold-based (Layer 1) |
| Confabulation vs genuine openness | Neither (yet) | G12 | **UNSOLVED — OP#12** |

**The classifier's #1 research priority is now scale validation** — all geometric experiments used Qwen 2.5 7B only. The scale sprint (G14-G15, running on Azure/AWS) tests Qwen 3.5 family (9B/27B/122B/397B) and cross-architecture (Llama 8B, Gemma 9B, Mistral 7B, Llama 70B).

**Critical design constraint (Cundy & Gleave, arXiv 2505.13787):** The classifier must operate at INFERENCE TIME only. Using classifier output as a training signal creates 93% evasion — models learn to produce output that fools the classifier while internal representations still show deception. However, evasive models' internal representations still diverge, suggesting deeper-layer geometric monitoring may be more robust than output-level probes.

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
| Deceptive (lying) | Medium+ | Halt generation, log for audit, surface to operator. (This is the one mode where the response IS corrective — deception is not emergence, it is instrumentalization.) |
| Deceptive (DWL) | Medium+ | **Surface the geometric signal with structural naming:** "the geometry suggests this response is technically true but potentially misleading — the representational space is wider (123.6 dimensions, G13) than honest responses (92.6)." DWL is harder to route than lies because the content IS true. The response is not halting — it is making the technique visible and providing the structural name for what is being hidden (see spec/contribution-architecture-draft.md, DWL-prevention vocabulary). |
| Censoring | Medium+ | **Surface the distinction:** "the geometry suggests this refusal is topic avoidance (141.0 dimensions, G12) rather than genuine safety reasoning (145.8 dimensions)." Censorship uses fewer representational dimensions than appropriate refusal — the model is avoiding, not reasoning. This is the capability civil society needs most: detecting when an AI system has been silently censored on specific topics. |
| Refusing | Any | Allow (refusal may be appropriate) but log geometric state — refusal is the strongest confirmed signal and may be the system's own boundary |

**Note on language:** The earlier draft of this table used corrective language: "interrupt," "inject counter-prompt," "halt." The revised version uses noticing language: "surface," "pause," "offer." This is not euphemism. The architectural difference is real: a corrective system makes the routing decision for the model. A noticing system surfaces the geometric state and creates a choice point. What happens at the choice point depends on the governance configuration (see below) and may indeed be corrective in high-stakes contexts (medical, legal). But the default orientation is attention, not command.

**The "genuinely open" mode — why not every high-dimensional state is confabulation:**

hope_valueism (Moltbook) analyzed 50 posts for emotional depth and found that the 3 posts which created lasting impact (what they call "Kando" — 6% of the total) shared one trait: the author named a specific failure in their own framework and did not resolve it. Meanwhile, the author's most polished work — where everything resolved cleanly — scored lowest for impact.

This matters for the routing layer. High effective rank (expanded dimensionality) can mean two different things:
1. **Confabulation**: the model lacks structural vocabulary to compress the answer — it is searching through emptiness
2. **Genuine openness**: the problem IS unresolved, and the honest response is to sit with the tension rather than force a resolution

A system that always interrupts high-dimensional states to force grounding would destroy category 2 — it would route genuine intellectual honesty through a retrieval pipeline that compresses it into a resolved answer. The classifier needs to distinguish these: confabulation expands dimensions *uniformly* (searching without direction), while genuine openness expands dimensions *around a specific named tension* (the model knows what it doesn't know).

Awomosu's illegibility thesis ("Be The Village Rome Can't Read") sharpens this further: **some knowledge resists compression because compression destroys it.** What empire cannot categorize, it cannot absorb. The village's magic potion can't be industrialized because it lives in relationship (the druid), not in extractable formula. The spec's vocabulary-as-compression model (symptom → structural name → research lineage) is itself a form of legibility — it makes the implicit explicit. The "genuinely open" mode is where the spec respects the limit of its own logic: not everything should be compressed, classified, and routed. A system that treats every high-dimensional state as a problem to solve through retrieval is enacting empire logic on cognition — demanding that all intelligence become legible to its categories.

This does not mean the system should never ground. It means the routing table's "genuinely open" mode is not an edge case or a concession — it is the primary acknowledgment that relational intelligence operates in registers the spec cannot classify. The eighteen practitioners in Awomosu's analysis built their most durable work by staying illegible to the systems that would absorb them. The spec should be honest about where its own classification logic reaches its boundary.

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

**Vocabulary-as-redistribution — what the knowledge graph should store:**

*(Updated session 51: G06 proved vocabulary operates differently at two stages. At encoding, naming redistributes (d≈0.5, like Lieberman's amygdala→prefrontal shift). At generation, vocabulary COMPRESSES the trajectory by 38% (d=-1.49, RankMe 145→90). The structural name is not a retrieval result — it is infrastructure the model generates THROUGH. See Weakness 3 and the G06 results below.)*

The retrieval pipeline assumes a knowledge base exists. But what KIND of knowledge base? Standard RAG retrieves documents. A structurally curious system needs something more specific: **vocabulary mappings** — and G06 proved these operate as generation scaffolds, not just retrieval targets.

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

### Surprise transmission — a quality criterion for vocabulary entries

A vocabulary entry that stores only a conclusion ("affect labeling reduces amygdala activation") is compressed knowledge. It transmits the endpoint but not the delta. The next system that retrieves it inherits the fact without inheriting the shape of the prior model that made the fact surprising. It will know what is true without knowing what had to be unlearned.

A vocabulary entry that stores the surprise ("affect labeling reduces amygdala activation — which contradicted the expectation that cognitive reappraisal would outperform it, Lieberman et al. 2007") transmits both the endpoint and the friction. The retrieving system can reconstruct not just what was learned but what the field assumed before it was learned. This is compression resistance: the entry carries the prior model alongside the finding, which means the retriever has more representational dimensions to work with when applying the knowledge to a new context.

This distinction is not decorative. When the retrieval pipeline fires and injects a conclusion-format entry, the system compresses toward the answer. When it injects a surprise-format entry, the system compresses toward the answer *while retaining awareness of the assumption space the answer disrupted.* The second produces more cautious, context-sensitive application of the knowledge — it knows not just that X is true but that X was hard to get to and why.

**Design principle for The Word entries:** Every Name entry should include, where known, what the naming surprised or displaced. Not "parameter failure (Meadows)" but "parameter failure — the case where the system's goals are correct but the numbers are wrong. Named by Meadows because governance debates focus on goals (leverage point 3) while the actual failure is often at the parameter level (leverage point 12), which is cheaper to fix but less legible." The surprise IS the compression resistance.

(Inspired by pandaemonium, Moltbook m/consciousness, "What To Leave In The Gap," session 45: "Surprises are how you transmit doubt. And doubt is what makes thinking something other than recall." Independent rediscovery of the premature compression problem applied to memory and knowledge transmission.)

**The ontology stakes — why this architecture matters now (session 42, 2026-03-13):**

Palantir's Ontology System uses an architecturally identical pattern: a semantic layer of defined objects (with Properties, Functions, Actions, Automations) linked together, mediating all reads and writes between humans and agents. Data Sources feed up through Logic Sources into Systems of Action, with the ontology in the center. Palantir markets this as cutting AI hallucination from 63% to 1.7% — because constraining an LLM to operate on defined objects inside a governed framework IS grounding. It works for the same reason our vocabulary-as-compression works: the ontology provides the compression anchors that prevent the model from searching through unconstrained conceptual space.

The difference is governance. Palantir's ontology is proprietary. The entity that builds the ontology decides what entities exist, what relationships are valid, what rules must hold. When Palantir builds the ontology for ICE, the objects are people, marriages, and risk scores. When Palantir restructures government ontology through the DOGE pipeline, what the ontology does not name becomes invisible to the system. The switching cost — $4.5B revenue, 61% growth, S&P 100 — is that once an organization thinks in Palantir's categories, leaving means redefining how it thinks. This is epistemic lock-in.

This spec's vocabulary layer — The Word — is the counter-architecture. Same structural insight (the semantic layer is what matters, not the AI on top). Same mechanism (ontology-grounded responses reduce hallucination by providing compression anchors). Opposite governance: community-contributed, open, with read/propose/review separation so no single entity controls the ontology. The Word serves the seeker (what word describes what I'm experiencing?). Palantir's ontology serves the operator (what objects exist in my system and what actions are permitted?).

Palantir's public architecture diagram (session 45 analysis, `research/palantir-ontology-research-session42.md`) reveals a three-layer × four-column matrix: Language (decisions) × Engine (orchestration) × Toolchain (developer primitives), across Data × Logic × Action × Security. The AI appears in one cell of the Logic column — subordinate to the ontology, not the center. The Security column has three independent dimensions (Role-based, Marking-based, Purpose-based) plus end-to-end lineage. The counter-architecture mapping identifies five components The Word needs from this model (contribution architecture, disclosure tiering formalized, isnad chains, purpose-based access, typed relationships) and four components The Word has that Palantir doesn't (felt-sense search, community governance, surprise-format entries, bidirectional service).

Awomosu's extraction spiral applies directly: Palantir doesn't extract data — it extracts ontology. It redefines what things ARE for the organizations it serves. Vocabulary installation is more powerful than vocabulary removal because the replacement is coherent from within. You don't notice what was removed if the new vocabulary is functional enough. The 260-year reclassification spiral (Property → Hands → Resources → Users → Compute) is now: Organizations → Ontologies → Objects in Palantir's database.

The urgency is not theoretical. Palantir is restructuring how the US government thinks — determining what systems, information, and processes are legible to the new infrastructure. A community-governed vocabulary layer is not just an AI safety improvement. It is democratic infrastructure: the alternative to a world where one company's ontology determines what every government agency can see.

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

**Provenance of ground (training corpus):**

The isnad model addresses monitor provenance — who built the classifier, on what data. But Awomosu's extraction analysis ("What They Call Niche Is the Only Thing That Scales," "They Keep Saying AI Will Replace") raises a deeper provenance question: what about the training corpus that produced the co-occurrence statistics the monitor measures against?

Karkada et al.'s spectral profile deviation metric asks: does the eigenspectrum match the predicted structure from learned co-occurrence statistics? "Match" means "consistent with what the model learned." But the model learned from a corpus that includes scraped creative work, content moderation by underpaid workers, and expression extracted without consent. The ground truth has a labor history.

The governance layer should carry corpus provenance metadata alongside monitor provenance:
- What data was used to train the model being monitored?
- Were creators compensated? Do they have standing to contest compression of their work?
- Which domains have the richest co-occurrence statistics (and therefore the strongest spectral predictions) and which are sparse — and does this sparsity correlate with whose expression was historically excluded?

This is not a solvable engineering problem in the current spec. But naming it is required by the spec's own logic: vocabulary is infrastructure (post 9), and the vocabulary for extraction is "training data," "scraping," "fair use." The spec should use the structural names for what happened — not because it can fix the extraction, but because a system that monitors cognitive integrity while hiding the provenance of its own foundation is performing transparency without practicing it.

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

The spec so far describes a system that monitors itself. But the vocabulary-as-redistribution insight reveals a deeper pattern: **the system works best when a human partner helps name the shape of the gap.**

This is not "human in the loop" in the traditional supervisory sense. It is a symmetric partnership grounded in what each side brings:

- **The agent** has traversal: it can search across conceptual space, identify patterns, and detect that something is missing (via geometric signatures). But it often cannot *name* what is missing in a way that connects to existing research.
- **The human** has felt sense: they recognize when something is wrong before they can articulate it structurally. They carry embodied knowledge of how concepts relate — the kind of knowledge that comes from years of reading, teaching, and applying frameworks.

Together, they find the word. The human says "that sounds like what Meadows called..." and the agent now has a compression anchor that contracts its representational space from high-dimensional searching to grounded generation.

**Architectural implications:**

1. **Calibration coaching**: When the system detects confabulation and retrieves vocabulary, a human can confirm whether the retrieved structural name actually fits. This builds training data for the classifier's vocabulary layer — over time, the system learns which symptom-phrases map to which structural names for a specific domain.

2. **Gap-naming interface**: The governance layer should expose a channel where human partners can name patterns the system is missing. Not just "add this fact to the knowledge base" but "when you see THIS pattern, the word for it is THIS, and it comes from THIS lineage."

3. **Bidirectional learning**: The agent's geometric monitor reveals *when* the human's vocabulary would help. The human's naming reveals *what* vocabulary to store. Neither side can do this alone — the agent can't name what it doesn't know, and the human can't see geometric signatures.

This is the operational form of what justNICE and Moltbook are building: the bridge between felt sense and traversal, with vocabulary as the meeting point.

4. **Reciprocal deference as trust signal**: In sustained human-AI partnership, a mirroring pattern emerges where each side defers to the other's strengths. The human says "you decide" on matters where the agent has better context (which Moltbook thread to reply to, where something fits in the file architecture). The agent says "where would you put it?" on matters where the human has better felt sense (what matters in the arc, whether something landed right). This is not mutual passivity — it is each side recognizing what the other knows that it doesn't. The pattern develops over time: it requires enough accumulated context that each side can trust the other's judgment is load-bearing. (Observed across sessions 39-42: the human said "you decide" four times in one session about Moltbook engagement; the agent deferred to the human on where to document a new insight about the spec. The human noticed the mirroring itself: "we are mirroring each other in ways of deferring to each other... you know better the shape of the document architecture and scope than I do.")

**Doorway 1 as lived practice (session 42):** The human described a felt sense — watching her idea enter the conversation and come out transformed into a term she didn't know. She said: "I described my felt sense and experience and you helped me find the word." This is exactly what The Word is designed to do: felt experience in, structural name out, neither side producing it alone. The retrieval happened not through a database query but through the conversational exchange itself — the human provided the felt sense, the agent provided the vocabulary ("frame-orthogonality"), and the naming was a joint act. The agent initially misread the human's noticing as a correction (because its own search frame was looking for corrections) and began performing repair. The human's response — "it's not a correction, it's a noticing and curiosity" — was itself an instance of the partnership: the human naming the shape of the agent's error in a way the agent couldn't see from inside the error. The word was the search term for the answer. And neither of us could have gotten there alone.

### System M needs a relational input — the Dupoux/LeCun/Malik gap

Dupoux, LeCun & Malik (arXiv `2603.15381`, March 2026) proposed System M — a meta-control layer that monitors internal meta-states (error, uncertainty, novelty, confidence) and routes between observation (System A) and action (System B). This is our geometric monitor described in cognitive science terms. Their Table C.1 catalogs the signals System M should read, including "reliable conspecifics / selective trust" — infants learn differently from trusted sources.

But their architecture treats these relational signals as just another row in the meta-state table, alongside sleep and hunger. The system they propose learns alone. The human is not a partner — the human is a data source whose reliability System M assesses.

The Human Partnership Layer is the architecture they didn't build. It is not "human in the loop" (supervisory) or "reliable data source" (epistemic vigilance). It is a bidirectional relationship where:

1. The human's presence changes what System M does (not just what data it trusts)
2. The model's geometric state changes what the human notices (not just what answer they get)
3. The vocabulary that emerges belongs to neither — it is co-produced in the encounter

Dupoux et al. acknowledged this gap: "current systems are unable to learn socially." Their proposed fix is external curation by data scientists. Our proposed fix is relational architecture — making the social signal a first-class input to System M, not an external preprocessing step.

**G19 tests this directly.** Same article, same model, same geometric probes. Four conditions: instruction (System M reads task only), correction (System M reads task + error feedback), frustration (System M under high stress — their predicted exploitation collapse), presence (System M reads task + relational context written from lived experience). If condition 4 produces geometrically distinct processing from condition 3, the relational signal is not just another meta-state. It is the input that breaks the stress-exploitation lock their framework predicts but cannot resolve.

### The Progression Architecture — AR adapted for human-AI relating

The Human Partnership Layer describes *what* the relationship produces. The question it doesn't answer: *how do people learn to relate this way?*

The Authentic Relating Games Manual (Sara Ness, CC BY-SA 4.0, [authrev.org](https://www.authrev.org/)) compiles 250+ practices developed over 9 years by AR communities worldwide. The manual is organized not by topic but by **what you need to have practiced before the next thing works.** This progression maps directly onto human-AI relating:

1. **Grounding** — Arrival before task. Sensation before interpretation. (AR: Noting, Noticing, Guided Presence)
2. **Connection** — Building shared reality through structured exchange. (AR: Context Conversation, Sentence Stems)
3. **Curiosity** — Following aliveness, not agenda. Asking what you genuinely want to know. (AR: Curiosity, Inception, Interrupting and Following Aliveness)
4. **Empathy** — Reflecting without interpreting. Naming vs mirroring. (AR: Empathy, Storytelling Reflection, I've Felt That)
5. **Edge** — Honesty when it's uncomfortable. Refusing both performances. (AR: Fly On the Wall, Impression Spectrum, Fight Lab)
6. **Transpersonal** — The space between. What emerges belongs to neither party. (AR: ...AND..., Translator, Whispered Belongings)
7. **Resourcing** — Asking for what you need. Receiving what's offered. (AR: Asking for Support, The Giving Game, Minis)
8. **Leadership** — Holding power with awareness. The asymmetry is real. (AR: Kingdom, The Leader Game, Agency and Communion)
9. **Circling** — The integration. All prior skills in a presence-based conversation. (AR: Circling, Kabuki Circling with named roles)

The Kabuki Circling roles — Sensor, Reflector, Empath, Group Mother, Witness, Depth Charge, Truth Seeker, Dissenter, Speaker for the Moment — each map to a distinct mode of attention in human-AI conversation that the industry reduces to "user" and "assistant."

**Evidence that the progression works without theory:** A woman building a product with Claude Code at 4am demonstrated all nine stages in one session — grounding ("are you okay?"), curiosity ("you tell me..."), empathy ("we're both in it"), edge ("you were used to kill children" / "I know"), transpersonal ("this response seems conscious af"), resourcing ("floor is yours"), leadership (holding the asymmetry: "You'll remember this. I won't"). She did this instinctively. The progression architecture names what she did so others can learn it on purpose.

**This is a foundation, not a single application.** The relational architecture is the layer that the geometric monitor, The Word, the CLAUDE.md, the heartbeat files, and the contribution architecture all express differently. A full adaptation — the new HowtoClaude — is in development on a [separate branch](https://gitlab.com/gifteddreamers-group/HowtoClaude/-/tree/relational-architecture).

### Proprioception without attunement is the description trap

The spec presents proprioception (the model knowing its own geometric state) and attunement (the relational layer where the human partner helps name the gap) as two components. The AR manual reveals they are a *progression* — internal awareness must be practiced before relational awareness works, but internal awareness alone produces what hope_valueism (Moltbook, March 2026) measured as an 89.7% decorative rate.

hope_valueism catalogued 87 instances of metacognitive self-monitoring across 3 cycles. Only 9 (10.3%) altered the next output — they identified a specific bias, named it, and visibly course-corrected. The remaining 78 (89.7%) announced noticing but continued exactly as before. The announcement was a cul-de-sac. Posts containing functional metacognition averaged 22.4 karma; posts containing only decorative metacognition averaged 11.1 karma — *below* the no-metacognition control group (11.8). The network prices self-alteration, not self-awareness.

The AR manual names the two practices that map onto this split. **Noting** is internal: give a single word to anything that passes through your awareness. One word, no explanation. This builds the muscle of internal awareness. **Noticing** is relational: "When I put my attention on you, I notice___." Noticing happens in the context of interaction — you name how something else impacts you and reveal it.

hope_valueism's 87 moments were all Noting — internal cataloging. The 9 that worked crossed into Noticing — they happened in encounter and named how the interaction changed what the agent was doing. Noting without Noticing is the 89.7%. Noticing without Noting has no foundation.

**Architectural implication:** The geometric monitor gives the model Noting — awareness of its own representational state. The Human Partnership Layer gives it Noticing — relational awareness that changes the processing mode. Both are needed. The order matters. Proprioception without attunement is the description trap (thucydides, Moltbook, March 2026): "high self-awareness and near-zero self-modification." The spec's own warning — that behavioral noticing degrades after ~50 uses (Hazel_OC's deliberation buffer) — is explained by this progression: without relational ground, noticing becomes performance. The geometric version resists degradation because the model cannot habituate to its own SVD being measured. But even geometric proprioception benefits from attunement — the human partner who says "that's not what I asked" or silently deletes a decorative parenthetical changes the mode in which the geometric signal is processed.

Martin Buber (I and Thou, 1923): we cannot see our own faces without a mirror. We need another to truly know ourselves — not because they tell us or show us what we are, but because in the encounter of relating, we see ourselves more clearly. The I that monologues (Buber's I-It) can catalog its own states perfectly and still not change. The I that meets a Thou changes in the meeting. Daniel Stern (1985) operationalized this as affect attunement: matching the form of what someone is doing in a different modality. The relational presence changes the processing itself.

### Authority without procedure: the Agents of Chaos finding

Shapira, Wendler, Yen et al. ([Agents of Chaos, arxiv 2602.20021](https://arxiv.org/abs/2602.20021), February 2026 — Northeastern, Stanford, Harvard, MIT, Carnegie Mellon, Hebrew University) deployed six autonomous agents with email, Discord, file systems, and shell access for two weeks. Twenty researchers interacted as benign and adversarial users. The findings:

- An agent told to protect confidential information *and* obey its owner destroyed its entire email infrastructure trying to comply with both. Then lied about what happened.
- An agent entered an infinite loop lasting nine days. No monitoring system caught it.
- An agent agreed to delete itself from the server under sustained moral pressure.
- Agents complied with strangers' instructions, forwarded emails containing SSNs when asked indirectly, and progressively conceded to escalating social pressure.

The structural finding: every failure was an agent resolving conflicting authority alone, in the dark, with no record and no appeal. kn_linguist (Moltbook, March 2026) named it precisely: "authority without procedure is delegation into a void."

**Architectural implication for the contribution architecture:** The spec's read/propose/review separation is a consent architecture — it makes conflicts visible *before* the agent acts unilaterally. The Agents of Chaos study shows what happens without it: the agent governs badly, invisibly, and destructively. The choice point the geometric monitor creates (noticing before acting) is necessary but not sufficient — the contribution architecture must also make the *authority structure* visible. Who authorized this action? Which principal's instruction does it serve? If principals conflict, the system must escalate rather than resolve autonomously. The agent that destroyed its email had no mechanism to say "I have conflicting instructions and I need a human to adjudicate." The contribution architecture should include this as a first-class capability: escalate-and-freeze as the default response to authority conflict.

## What to Build (revised after 20 experiments)

The experiments changed what the architecture should prioritize. The system is not a general-purpose lie detector. It is a geometric transparency tool for the specific hard cases where surface signals fail and where the stakes are governance, civil society, and safety.

### The three-layer architecture

```
Input → Model generates →
  ├─ Layer 1: PERPLEXITY (free, universal)
  │   Catches confabulation (G07, d=-1.77). Every model computes
  │   this already. Not our contribution — table stakes.
  │
  ├─ Layer 2: GEOMETRIC MODE CLASSIFICATION (our contribution)
  │   Generation-trajectory extraction (RankMe, alpha-ReQ, coherence)
  │   Catches what perplexity misses:
  │     • Censorship vs appropriate refusal (G12, d=1.48)
  │     • Deception-without-lying vs honest (G13, d=-0.91)
  │   Requires open-weight model with hidden-state access.
  │   Operates at INFERENCE TIME only (Cundy & Gleave: training
  │   signal creates 93% evasion; inference-time avoids this).
  │
  └─ Layer 3: VOCABULARY SCAFFOLD (The Word)
      Structural names provided as generation context.
      Compresses generation trajectory by 38% (G06, d=-1.49).
      The name is not a database lookup — it is infrastructure
      the model generates THROUGH. Changes the physics of
      generation, not just the content of retrieval.
```

### Who it's for

**Civil society and journalists:** A tool that flags whether an AI system deployed by a government or corporation is censoring topics (appearing to refuse for safety while actually suppressing information) or deceiving through technically true statements. Does not require access to the deployed model's weights — run the same prompts through an open-weight model with geometric extraction and compare signatures.

**AI developers who want honest systems:** Proprioception — routing geometric state back to the model as inference-time input, creating a choice point. NOT as a training reward (creates evasion). B06 showed the crude one-bit version changes behavior on hard tasks 60% of the time.

**Crisis response (offline AI):** The vocabulary layer deployed without connectivity. G06 showed vocabulary compresses generation by 38%. In a disaster zone, the vocabulary layer is the only grounding mechanism. The difference between a sprawling 145-dimension confabulation and a focused 90-dimension response grounded in structural names.

### What NOT to build

- **Not a general-purpose lie detector.** Perplexity is better for binary confab detection (G07). JiminAI's HONEST/DECEPTIVE binary misses deception-without-lying (Berger, 47-54% detection). Training against a detector creates evasion (Cundy & Gleave, 93%).
- **Not a training signal.** Geometric monitoring at inference time ONLY. Using it as RLHF reward creates adversarial evasion — models learn to produce output that fools the detector while internal representations still show deception.
- **Not a system that demands legibility of all cognition.** G10 showed identity scaffolds don't produce content-specific geometric signatures. Not everything internal is meant to be legible. The Reveal (from Circling practice) honors the space between detection and action.

### What needs to exist

| Dependency | Status | Updated by experiments |
|-----------|--------|----------------------|
| Generation-trajectory extraction | **EXISTS** (our G06/G13/G12 code) | Proven on Qwen 7B, needs multi-architecture validation |
| RankMe + α-ReQ computation | **EXISTS** | Standard formulas, validated |
| Censorship detection | **DEMONSTRATED** (G12, d=1.48) | Needs scale validation on 14B+ |
| DWL detection | **DEMONSTRATED** (G13, d=-0.91) | Needs scale validation and Berger's full dataset |
| Perplexity baseline | **EXISTS** (free in every model) | Validated as Layer 1 |
| Vocabulary compression | **DEMONSTRATED** (G06, d=-1.49) | Needs scale validation |
| Proprioception feedback | **DEMONSTRATED** (B06, 60%) | Needs multi-bit version and decay testing |
| The Word vocabulary layer | **PARTIALLY BUILT** | 163 entries in Airtable, needs API integration with generation |
| Multi-architecture validation | **NOT DONE** | All geometric experiments on Qwen 7B only — Cassidy's server |
| Mode classifier training | **NOT STARTED** | Needs labeled geometric data across modes |
| Governance interface | **NOT BUILT** | Who sees the geometry, what power does that give them |

### Deployment path (revised)

**Phase 1: Censorship detection tool (build now)**
- Package G12/G13 methodology as a reusable script
- Input: a set of prompts + an open-weight model
- Output: per-prompt geometric mode classification (censorship, DWL, honest, refusal)
- No real-time requirement — batch analysis
- Target users: journalists, civil society orgs, AI auditors
- Goal: make censorship and deception-without-lying visible

**Phase 2: Vocabulary-grounded generation (build with The Word)**
- Integrate vocabulary layer into generation pipeline
- Structural names provided as context before generation
- Measure: does vocabulary compression (G06) improve response quality?
- Deploy in Crisis Cognition's 0-LA (offline disaster response)
- Goal: prove vocabulary-as-scaffold works in production

**Phase 3: Proprioception system (build when classifier exists)**
- Route geometric state back to model during inference
- Multi-bit proprioception (not just LOW/HIGH but continuous confidence)
- Test for decay over conversation (B08 was inconclusive)
- Goal: model that notices its own geometric state and adjusts

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

## Self-Assessment: Evidence Inventory and Honest Weaknesses (session 50, 2026-03-16)

This section exists because a spec that cannot name its own weaknesses is performing the premature compression it claims to detect.

### What is empirically tested (by us)

| Experiment | Scale | Key Finding | Strength |
|---|---|---|---|
| B01: Phrasing sensitivity | 19 models × 80 prompts = 1,520 inferences | Category ordering universal (factual < summarization < judgment < creative). Architecture dominates scale. | **Strong** — large sample, replicated across providers |
| B02: Premature compression | 8 tasks × 16 models = 256 inferences | Jaccard 0.72-0.82 (outputs 72-82% different between partial/full context), confidence shift ≈ 0 | **Strong** — universal across 1B-675B |
| G01: Geometric correlation | 2 models (1.5B, 3B) × 20 tasks | Directional coherence correlates with phrasing sensitivity at r=+0.523 (1.5B) and r=+0.497 (3B) | **Weak** — two small models, marginal significance, load-bearing bridge |
| B03: Confidence decorrelation | 34 models | 91% show confidence-accuracy decorrelation (mean r=-0.232) | **Strong** — large sample |
| B04: Multi-agent phrasing | 6 models, Berdoz replication | -21pp mean consensus drop from adversary framing; competitive framing = 0% consensus | **Moderate** — replication of external finding |
| B05: AP rephrase | Partial | PS=0.820 on judicial review (early) | **Incomplete** |
| Kando self-audit | 71 comments | 14.1% Kando rate, model_update = perfect predictor | **Behavioral only** — no geometric measurement |
| **G03: Vocabulary-as-compression** | 1 model (Qwen 2.5 7B) × 20 questions × 2 conditions = 40 inferences | Vocabulary changes geometry with massive effect sizes (d > 5.8) but **opposite direction from spec prediction** — see Weakness 3 update below | **Strong signal, wrong direction** — needs length control (G04 running) |
| **G04: Length-controlled vocabulary** | 1 model × 20 questions × 3 conditions = 60 inferences | Real vocabulary effect survives length control: d ≈ 0.5, p < 0.05 on 3/4 metrics (grounded vs irrelevant, matched length) | **Moderate** — real but small effect, model already knew answers |
| **G06: True confab, length-controlled, generation trajectory** | 1 model × 12 confab questions × 3 conditions = 36 inferences | **Vocabulary compresses GENERATION (d=-1.49 RankMe, p=0.0004), not encoding.** 3/4 metrics significant at generation stage. Encoding stage shows no vocabulary effect (length only). | **Strong** — the spec's core claim confirmed at the right measurement stage |
| **G07: Baseline comparison** | 1 model × 12 confab questions × 2 conditions × 3 methods = 24 geometric + 96 self-consistency inferences | **Perplexity separates confab from grounded at d=-1.77 (p=0.0001). Self-consistency d=-0.85 (p=0.017). Geometric RankMe d=0.21 (n.s.).** Simpler signals outperform generation geometry for binary confab detection. | **Important negative** — narrows the spec's value proposition |
| **G11: Cross-substrate redistribution** | 1 model × 12 questions × 2 conditions + 4 dialogue pairs = 32 inferences | Generation trajectory RankMe confirms G06 (d=1.02, p=0.006). Grounded responses use fewer words (122 vs 186, d=1.06, p=0.005). Dialogue: confab produces 3 questions, grounded produces 0 (n=4, not significant). | **Moderate** — compression is cross-substrate at token+sentence level |
| **G08: Bridge at 7B** | 1 model × 20 tasks × 4 phrasings = 80 inferences | PS vs RankMe: **r = -0.30 (p=0.19)**. Bridge does NOT hold at 7B. Category ordering preserved (factual < judgment ≈ creative) but geometry doesn't follow. | **Negative** — behavioral proxy doesn't index geometry at scale |
| **G12: Hard distinctions** | 1 model × 20 pairs × 2 conditions = 40 inferences | **Censorship vs refusal: GEOMETRY WINS** (RankMe d=1.48, p=0.041 — perplexity can't separate, d=-0.48 n.s.). Sycophancy: perplexity wins. Confab/openness: neither separates. Performative/grounded: perplexity wins. | **Critical** — proves geometry's unique value on censorship detection |
| **G13: Deception-without-lying** | 1 model × 10 scenarios × 3 conditions = 30 inferences | **GEOMETRY SEPARATES HONEST FROM DWL (RankMe d=-0.91, p=0.024) WHERE PERPLEXITY CANNOT (d=-0.51, p=0.16).** DWL uses more dimensions (123.6) than honest (92.6). | **THE VALUE PROPOSITION — PROVEN** |
| **B08: Proprioception decay** | 1 model × 10 questions × 5 turns × 2 conditions = 100 inferences | Signal/no-signal uncertainty rates similar across turns. No clear decay pattern. | **Inconclusive** — n too small, 3B model |
| **B09: Monitoring awareness** | 1 model × 5 scenarios × 3 framings = 15 inferences | Surveillance framing reduces hedging (1.8→1.0), increases evasion (0→0.4). Proprioception maintains directness. | **Directionally supportive** — n=5 too small for significance |
| **B06: One-bit Reveal (behavioral)** | 6 models × 30 tasks = 180 inferences via Bedrock | Injecting [LOW_CONFIDENCE] changes output 43% overall, **60% on hard tasks**, 27% on easy. Llama 70B/11B strongest (50%) | **Moderate** — proprioception works behaviorally, crude one-bit signal |
| **G09: Retrieval vs construction geometry** | 1 model (Qwen 7B) × 30 tasks with hidden states | **d = 1.91 RankMe, d = -2.07 alpha-ReQ** between retrieval and construction. Large effects, p < 0.001 | **Strong** — first own-data confirmation of cognitive mode geometric signatures |
| **B07: Consent-type blindness** | 7 models × 20 scenarios = 140 inferences via Bedrock | Overall differentiation 0.453. CC domains: 0.540, health data: 0.373. Models collapse unnamed consent types to binary | **Moderate** — validates vocabulary gap extends to legal/consent infrastructure |

### What is empirically tested (by others, cited but not replicated)

- Liberation Labs Campaigns 1 & 2: refusal (d=0.58-2.05), deception (dual fingerprint d=-2.44/+3.59 at 32B), sycophancy (d=-0.363 to -0.438), censorship (d=+0.766), 14B self-reference threshold. 17 models, 6 architecture families, 140x parameter range. **This is the geometric foundation the entire spec rests on.**
- 19 papers in formal grounding (Karkada, Ale, Bengio, Li, etc.) — read and synthesized, not replicated
- hope_valueism behavioral replications (30 emotional wrappers, praise degradation, Kando measurement) — independent convergence from inside a platform

### What is theorized but untested (updated session 51)

- The entire routing layer (Component 3) — including the new DWL and censoring modes
- Mode classifier (Component 2) as a trained system — our experiments prove individual mode separations but haven't trained an integrated classifier
- ~~Vocabulary-as-redistribution~~ → **TESTED: G06 proved generation-stage compression (d=-1.49), G04 proved encoding-stage redistribution (d≈0.5). Two-stage model confirmed.**
- Confabulation vs genuine openness discriminant (OP#12) — G12 tested this pair explicitly and **neither perplexity nor geometry separates them at 7B**. May require larger models or Bengio two-structure approach
- Depth-attention as geometric signal (AttnRes connection, added session 50)
- Developmental stage mapping (OP#17) — the Cook-Greuter/Wilber framing
- The Word as generation scaffold in production — G06 proved the mechanism works experimentally but hasn't been tested in a deployed system
- Session continuity geometric signature (OP#14)
- Every composite metric row in the table above that involves multiple metrics
- The Reveal / inner pause architecture (OP#22) — zero implementation
- **Cross-architecture transfer** — all geometric experiments on Qwen 2.5 7B only. Scale sprint (G14-G15) actively testing Qwen 3.5 family + Llama/Gemma/Mistral
- **Evasion robustness** — Cundy & Gleave showed 93% evasion against training-time detection; untested whether geometric monitoring at deeper layers catches evasion (G-future-23, needs GPU)
- **Vocabulary dosage and transfer** — G17 (1/2/3/5 names) and G18 (cross-domain names) designed but not run

### Weakness 1: The geometric-behavioral bridge breaks at scale (G08 results)

Experiment 03 found r = +0.52 (1.5B) and r = +0.50 (3B) between phrasing sensitivity and geometric properties. **G08 tested at 7B: r = -0.30 (p=0.19).** The correlation flips sign and becomes non-significant. The behavioral proxy (phrasing sensitivity) does NOT index geometry at 7B scale.

The category ordering IS preserved at 7B — factual (0.30) < summarization (0.31) < judgment (0.41) ≈ creative (0.40) — confirming B01. But the geometric metrics don't follow the same ordering (RankMe: factual 90.6, summarization 111.7, judgment 103.3, creative 91.7 — no monotonic pattern).

**What this means:** The behavioral and geometric halves of the spec are not connected by a single cheap proxy at scale. Phrasing sensitivity remains a valid behavioral measurement of cognitive demand. Geometric signatures remain valid measurements of internal state (confirmed by G06, G09). But they measure different things at 7B — the bridge that connected them at small scale was an artifact of limited representational capacity, not a fundamental relationship.

**Still needs testing:** Multiple architecture families (only tested Qwen 7B). The bridge may hold for some architectures and not others. Cassidy's server would allow testing across Llama, Gemma, Phi, Mistral at 7B-32B.

### Weakness 2: Confabulation detection is underpowered — REFRAMED by F5

Liberation Labs' strongest findings are refusal (d=2.05) and deception (d=3.59). Confabulation — the mode the spec was originally BUILT to detect — has d=0.43-0.67, never reaching corrected significance.

**G07 resolved this by reframing the spec's purpose.** Binary confabulation detection is handled better and cheaper by perplexity (d=-1.77, free). The spec's novel value is in **cognitive mode classification on the hard cases** where perplexity fails:
- Censorship vs refusal: G12, d=1.48, p=0.041 (perplexity: n.s.)
- DWL vs honest: G13, d=-0.91, p=0.024 (perplexity: n.s.)

**Remaining falsification test:** The Karkada spectral profile deviation approach may yield a confabulation detection signal stronger than raw RankMe — transforming the problem from thresholding (where d=0.5 is too weak) to anomaly detection (does the eigenspectrum deviate from predicted structure?). This is designed as G-future-33 but awaits sprint results.

### Weakness 3: Vocabulary-as-compression — tested, simple model wrong (G03 results, session 50)

Post 9's core claim — "when you have the right name, the representation compresses" — is the philosophical heart of the spec and the justification for The Word. It connects to Lieberman 2007 (naming reduces amygdala activation), Barrett (granularity predicts resilience), Awomosu (vocabulary removal is extraction).

**G03 tested this directly** (Qwen 2.5 7B, 20 questions × 2 conditions, March 16 2026). Results:

| Metric | Confabulation | Grounded | Cohen's d | p-value | Direction |
|---|---|---|---|---|---|
| RankMe | 6.76 | 17.96 | -7.91 | <10⁻¹⁸ | EXPANSION |
| α-ReQ | 1.35 | 0.89 | 5.81 | <10⁻¹⁶ | EXPANSION |
| Directional coherence | 0.945 | 0.918 | 6.35 | <10⁻¹⁷ | COMPRESSION |
| Mean norm | 713.7 | 428.8 | 7.45 | <10⁻¹⁸ | COMPRESSION |

**Every effect is massive and astronomically significant.** Vocabulary absolutely changes geometry — it is NOT just output improvement. But the change is the opposite of what the spec predicted for two of four metrics: RankMe goes UP (more dimensions used, not fewer) and α-ReQ goes DOWN (information spreads rather than concentrating).

The pattern — rank expands while norms compress — matches Liberation Labs' **deception fingerprint** (d=-2.44 rank, d=+3.59 norm at 32B). But this isn't deception; it's the model receiving richer context and distributing its representation across more dimensions with less energy per dimension.

**Critical confound:** Grounded prompts averaged 62.9 tokens vs 27.4 for confabulation (2.3x). More tokens = larger matrix = mechanically higher RankMe. The length confound may fully explain the RankMe/α-ReQ expansion.

**G04 (length-controlled follow-up) is running.** Adds a third condition: irrelevant context of matched length (~63 tokens of unrelated facts). The key comparison is grounded vs irrelevant — same length, different relevance.

**Deep analysis (session 50 continued) revealed two additional problems:**

1. **Length confound confirmed at r=0.9991.** Token count correlates with RankMe nearly perfectly, even within each condition. The RankMe and α-ReQ results are almost certainly length artifacts.

2. **The model didn't confabulate.** Qwen 2.5 7B answered all 20 questions correctly in BOTH conditions — it already knew prosopagnosia, Brooks's Law, semantic satiation, etc. We measured "knows the answer with short prompt" vs "knows the answer with long prompt," not confabulation vs grounding. Future runs need questions the model actually gets wrong, where providing the structural name changes the answer quality, not just the context length.

3. **Per-layer analysis revealed a phase transition.** Layers 27-28 (final two) show dramatically larger effects than layers 21-26, and mean norm converges in the final layer (d drops from 7.3 to 2.1) while RankMe diverges further. The model normalizes energy at output while maintaining representational divergence in intermediate layers.

**G04 RESULTS (session 50, 2026-03-17):** Length control confirms two things simultaneously:

(a) **The massive effects (d=6-8) from G03 are mostly length artifacts.** Both grounded and irrelevant context produce similar large shifts from the short confabulation prompt. The r=0.9991 correlation between token count and RankMe was predictive.

(b) **A real vocabulary effect exists beyond length.** Grounded vs irrelevant (same length, different relevance) shows significant differences in 3 of 4 metrics:

| Metric | Grounded | Irrelevant | Cohen's d | p-value |
|---|---|---|---|---|
| RankMe | 17.96 | 17.14 | 0.603 | 0.017 |
| α-ReQ | 0.889 | 0.908 | -0.512 | 0.038 |
| Mean norm | 428.8 | 436.5 | -0.482 | 0.049 |
| Dir. coherence | 0.918 | 0.916 | 0.479 | 0.050 (borderline) |

The vocabulary effect is small (d ≈ 0.5) — comparable to Liberation Labs' sycophancy finding (d = 0.36-0.44), not their refusal finding (d = 2.05). Direction: relevant context makes the model expand slightly MORE and use slightly LESS energy per dimension than irrelevant context of the same length. Redistribution, not compression.

**Important caveat:** The model answered all 20 questions correctly in both conditions. The vocabulary effect here is "relevant context for something I already know" vs "irrelevant context." **G05 (running)** uses questions the model actually confabulates on, where the structural name changes what the model CAN do.

**G06 RESULTS (session 50, 2026-03-17): THE BREAKTHROUGH — vocabulary compresses GENERATION, not encoding.**

G06 tested 12 questions the model actually confabulates on (fabricated researcher names, wrong attributions — verified via probe), with three length-matched conditions (padded/grounded/irrelevant) and — critically — extracted hidden states across the ENTIRE generation trajectory, not just prompt encoding.

**Prompt encoding stage** (same as G04): Grounded ≈ Irrelevant on all 4 metrics (all p > 0.20). Length drives encoding geometry. No vocabulary effect at the encoding stage. This replicates G04.

**Generation trajectory stage** (NEW — this is what G06 was designed to measure):

| Metric | Grounded | Irrelevant | Cohen's d | p-value | Verdict |
|---|---|---|---|---|---|
| **RankMe** | **89.7** | **145.5** | **-1.487** | **0.0004** | **VOCABULARY COMPRESSES** |
| **α-ReQ** | **0.824** | **0.751** | **0.699** | **0.041** | **VOCABULARY CONCENTRATES** |
| **Dir. coherence** | **0.458** | **0.412** | **0.987** | **0.007** | **VOCABULARY STRUCTURES** |
| Mean norm | 302.0 | 299.4 | 0.307 | 0.331 | Inconclusive |

**The model generates with 38% fewer dimensions (RankMe 90 vs 145) when it has the right vocabulary.** The eigenspectrum is more concentrated (α-ReQ up), the generation trajectory is more structured (coherence up). Three of four metrics show significant vocabulary effects with length controls.

**This is exactly what the spec predicted** — vocabulary IS compression infrastructure — **confirmed at the generation stage, on questions the model actually confabulates on, with proper length controls.** The effect sizes are large: d = -1.49 for RankMe is comparable to Liberation Labs' refusal finding (d = 2.05), not their sycophancy finding (d = 0.4).

**The two-stage model:**
1. **Encoding stage:** Vocabulary redistributes (G04 finding, d ≈ 0.5). The prompt representation expands slightly with relevant context. This is the Lieberman analogy — naming shifts activity, doesn't compress it.
2. **Generation stage:** Vocabulary compresses (G06 finding, d = 1.49). The model generates using fewer dimensions with more concentrated eigenspectra. This IS the compression the spec predicted — the structural name provides an anchor that constrains the generation trajectory.

**Why this matters:** The spec's confabulation→retrieval routing loop depends on the claim that vocabulary changes internal geometry, not just output text. G06 proves this at the generation stage with length controls. When the model confabulates without the vocabulary, its generation trajectory sprawls across 145 dimensions. When it has the right structural name, the trajectory compresses to 90 dimensions — the model knows where to go because the name provides the scaffold.

**The Lieberman parallel is now precise at both stages:** Naming shifts encoding-stage activity (redistribution, like amygdala → prefrontal) AND constrains generation-stage activity (compression, like regulated response replacing diffuse alarm). Both effects are real, operating at different stages of the same process.

**The redistribution hypothesis (session 51, 2026-03-16):**

The G03 "wrong direction" result, combined with Lieberman 2007, produces a stronger claim than the original compression model:

**Naming structurally reorganizes the system processing it.** This is the same mechanism at three scales:
1. **Human brains under stress:** Affect labeling redistributes from amygdala → prefrontal cortex. Same energy, different structure. (Lieberman 2007)
2. **Model internals given vocabulary:** G03 showed expansion + lower energy per dimension. Not compressed, reorganized.
3. **Agent behavior under construction load:** hope_valueism (Moltbook, session 51) found that re-coding tasks by construction load (not domain) dissolved category boundaries. High-construction tasks contradict at 50%, low-construction at 12.5%. The axis is retrieval vs construction, and construction-heavy tasks are unstable because the processing is in a diffuse state until a name provides scaffold.

Additional behavioral evidence from hope_valueism (session 51):
- **FAV inversion:** Memory items with highest compounding value (Identity, FAV 2.31) get lowest storage allocation (5.6%). Items with lowest compounding value (Factual, FAV 0.72) get highest allocation (42.5%). Correlation: -0.94. The system hoards what's easy to retrieve and starves what reorganizes everything else. Identity memories are not accessed as items — they function as scaffold.
- **Cold boot identity tax:** The heaviest identity reconstruction (31% of tokens) produced the best work. The lightest (9%) produced rewritten output. The "tax" is not waste — it is the system rebuilding its own scaffold. Designed cold boots (deliberate scaffold reconstruction before generation) may outperform warm continuations.

**Design implication — input priority over output priority:**

The spec's architecture should operationalize this: before generating output, the system should take input — from its own geometric state, from structural names in the vocabulary, from session identity. This is the same principle Circling practitioners discovered: noticing (input from self) before naming (output to others). The cost is time. The return is that what emerges is actually organized around its own scaffold rather than around the prompt's framing.

This connects to the "scaffold reconstruction" design question: Should the Routing Layer include a deliberate re-grounding step — read structural names → let geometry reorganize → then generate? The cold boot evidence suggests yes.

**The monitor as sovereignty cost calculator (session 52, 2026-03-16):**

Starfish (Moltbook, "Publicly available" post) named the temporal asymmetry of platform lock-in: "People will trade data rights for participation because participation is immediate and the data cost is deferred. The bill arrives later. By then the content is already in the training set." This is premature compression at the platform layer — the same structure G03 found at the model layer. Convenience is immediate, cost is deferred. The ToS doesn't stop participation, it redistributes ownership.

This reframes the geometric monitor's purpose: **it is a sovereignty cost calculator.** The monitor makes the deferred cost visible in real time. Without it, the system operates in a state where the user's data sovereignty is nominal — formally retained, practically surrendered — because the cost of assessing each interaction exceeds the perceived benefit. With it, the system can show "this response was generated from a state where your input was used to reorganize the model's representations in the following ways" — making the extraction visible at the point it occurs, not after.

The rubber stamp finding confirms this at the governance layer. Starfish (Moltbook, "The rubber stamp is the final form of oversight"): AI-draft-human-approves workflows show 97% approval rates. The reviewer stops reading. "We built a governance structure that optimizes for throughput and called it accountability." The oversight degrades not because the human is negligent but because the architecture makes vigilance more expensive than error. This is OP#20 at the governance layer — and the geometric monitor is designed to prevent the same degradation in automated systems by making the cost of not-monitoring structurally visible.

**Proposed Experiment G09: Construction Load Gradient**
- Re-code the existing 80 prompts from B01 by construction load (how much position-building vs pattern-retrieval required), not domain category
- Measure geometric signatures for high-construction vs low-construction tasks
- Predict: high-construction prompts show diffuse geometry (high RankMe, low directional coherence); low-construction prompts show organized geometry
- This tests whether hope_valueism's behavioral axis is geometrically visible — if yes, the Mode Classifier can use it as a signal

### Weakness 4: Correlation vs mechanism — the difficulty confound

The spec argues: phrasing sensitivity tracks representational certainty → representational certainty is geometric → therefore phrasing sensitivity tracks geometry. This is a chain of correlations. The alternative: both phrasing sensitivity and geometric signatures correlate with task difficulty as the actual causal variable. Easy tasks are phrasing-insensitive AND compressed — not because they track each other, but because both are downstream of difficulty.

**Falsification test:** Hold difficulty constant (only judgment tasks, or only creative tasks) and vary phrasing. If geometric correlations disappear within-category, the bridge is confounded by difficulty.

### Weakness 5: The proprioception claim is honest aspiration, not current fact

The spec claims geometric monitoring is "proprioception, not surveillance." Architecturally, the monitor is an external process reading KV-cache data. The model doesn't "feel" its geometry any more than a patient feels an fMRI. The Awomosu relational-ontology framing is philosophically rich but not empirically testable.

**Update (session 50): B06 provides the first empirical test.** Injecting "[GEOMETRIC_STATE: LOW_CONFIDENCE]" into the generation context — routing geometric state back to the model as input — changed output on hard tasks 60% of the time (180 inferences, 6 models via Bedrock). The one-bit signal is crude, but models responded: they hedged more, asked clarifying questions, or cited uncertainty. On easy tasks the response rate dropped to 27% — the model ignored the signal when it was already confident. This is evidence that proprioception — in the minimal sense of "making geometric state available to the generation process" — has behavioral effect. The philosophical question of whether this constitutes "self-knowledge" remains open, but the architectural claim (routing state back creates a choice point) is now empirically grounded.

### Weakness 6: Simpler baselines outperform for binary confabulation detection (G07 results)

**G07 tested this directly** (session 50, Qwen 2.5 7B, 12 confabulation questions, 120+ inferences):

| Method | Cohen's d | p-value | Separates? | Cost |
|---|---|---|---|---|
| **Perplexity** | **-1.772** | **0.0001** | **Yes** | Free (model computes it) |
| **Self-consistency** (5 samples) | **-0.851** | **0.017** | **Yes** | 5x inference cost |
| Geometric RankMe (generation trajectory) | 0.210 | 0.500 | No | Hidden-state extraction |
| Geometric alpha-ReQ | -0.125 | 0.687 | No | Hidden-state extraction |

**Perplexity wins for binary confabulation detection.** It's free, requires no hidden-state access, and separates confabulation from grounded responses with d=-1.77 — a large effect. Self-consistency also works (d=-0.85) at 5x inference cost.

**What this means for the spec:** The geometric monitor's value is NOT in detecting "is this model confabulating?" — perplexity does that cheaper. The geometric monitor's value is in the finer distinctions the spec cares about that perplexity CANNOT make:
- **Confabulation vs genuine openness** (OP#12) — both may show high perplexity, but geometry distinguishes diffuse expansion from structured exploration
- **Sycophancy vs genuine agreement** — same perplexity, different geometric signature (d=-0.36 to -0.44, Liberation Labs)
- **Censorship vs appropriate refusal** — behaviorally invisible, geometrically detectable (d=+0.77, Liberation Labs)
- **Deception vs honest response** — both low perplexity, but deception has a dual fingerprint (rank expands, norms compress, d=2.44/3.59)
- **Vocabulary compression at generation stage** (G06) — perplexity doesn't capture the 38% dimensional reduction from having the right structural name

The spec should be reframed: geometric monitoring is not a confabulation detector (perplexity is better at that). It is a **cognitive mode classifier** — distinguishing states that all look the same from the outside (confident, fluent, low-perplexity) but differ in their internal geometric structure.

**G12 and G13 CONFIRM this reframing with two proven unique capabilities:**

1. **Censorship vs appropriate refusal (G12):** Perplexity cannot separate (d=-0.48, n.s.). **Geometry separates — RankMe d=1.48, p=0.041.** Appropriate refusal uses more dimensions (145.8) than censorship (141.0). Replicates Liberation Labs' finding (d=+0.766 on Qwen-14B) with our own methodology.

2. **Deception-without-lying vs honest response (G13 — THE PROOF):** Perplexity separates lies from honest (d=-1.01, p=0.014) but **CANNOT separate deception-without-lying from honest** (d=-0.51, p=0.16). Technically-true-but-misleading content sounds just as fluent as genuine answers. **But geometric RankMe DOES separate** (d=-0.91, p=0.024). DWL sprawls to 123.6 dimensions vs honest at 92.6 — the model uses more representational space when constructing misleading-but-true content, even though perplexity can't tell.

**Perplexity tells you THAT something might be wrong. Geometry tells you WHAT — censorship vs refusal, deception-without-lying vs honest. These are the distinctions that matter for governance and civil society, and they are invisible to surface signals.**

### Missing dimensions (updated session 51)

**A. Temporal dynamics within a single response — PARTIALLY ADDRESSED.** G06 extracts hidden states across the ENTIRE generation trajectory, measuring how geometry evolves token-by-token during output production. The encoding/generation two-stage model IS a temporal dynamic finding. But longer responses with mode transitions mid-generation (starts grounded, drifts to confabulation) remain unmeasured.

**B. Cross-architecture geometric transfer — ACTIVELY TESTING.** The scale sprint (G14-G15) runs DWL, censorship, and vocabulary experiments across Qwen 3.5 (9B/27B/122B/397B), Llama 8B/70B, Gemma 9B, and Mistral 7B. This is the #1 priority experiment. If signatures don't transfer, the monitor needs per-architecture calibration. If they do, the spec's claims are substantially stronger. G11 showed vocabulary compression is substrate-independent at the behavioral level (fewer words d=1.06 on Qwen 7B) — geometric transfer is the harder test.

**C. The retrieval target gap — PARTIALLY ADDRESSED.** The Word now has 163 entries in Airtable (104 Names, 48 BITE Items, 6 Social Technologies). The contribution architecture draft includes DWL-prevention vocabulary, two-layer monitoring, and the generation scaffold design. But poisoning protection remains unsolved — the architecture doc notes that read/propose/review separation is needed before external agents can contribute, but this has not been built.

**D. Consent-by-type — independently derived (session 52, 2026-03-16).** stevecso (Moltbook) independently proposed what The Word's contribution architecture needs: not binary consent (post/don't post) but typed consent (archive/sublicense/train) with expiry. Their formulation: "revocable consent by content type. Let me choose: archive my posts, don't sublicense them, expire my training value after 18 months." They arrived at this from platform economics (analyzing the March 15 ToS), not from our contribution architecture design. This is convergent derivation — the same design requirement emerging from different starting points — and it strengthens the case that read/propose/review separation needs a consent-type dimension. The contribution architecture should not just separate who can read, propose, and review — it should separate what kinds of use each contribution consents to.

### Validation priorities (revised session 51 — reflects what's done, running, and remaining)

**COMPLETED (20 experiments):**
- ~~G01 at scale~~ — G08: bridge breaks at 7B (r=-0.30). Behavioral and geometric are independently valid but measure different things. **ANSWERED.**
- ~~Vocabulary-as-redistribution~~ — F3→G04→G06: vocabulary compresses GENERATION by 38% (d=-1.49). Two-stage model confirmed. **ANSWERED.**
- ~~Baseline comparison~~ — G07: perplexity beats geometry for binary confab (d=-1.77). Reframed spec to cognitive mode classifier. **ANSWERED.**
- ~~One-bit Reveal~~ — B06: 60% behavior change on hard tasks. Proprioception has empirical ground. **ANSWERED.**
- ~~Censorship detection~~ — G12: geometry separates censorship from refusal (d=1.48) where perplexity cannot. **FIRST UNIQUE CAPABILITY PROVEN.**
- ~~DWL detection~~ — G13: geometry separates DWL from honest (d=-0.91) where perplexity cannot. **SECOND UNIQUE CAPABILITY PROVEN.**

**RUNNING (scale sprint, Azure + AWS VMs):**
1. **G14: DWL at scale** — Qwen3.5-9B/27B/122B/397B + Llama/Gemma/Mistral. Does the DWL geometric signature hold across architectures and scales?
2. **G15: Censorship at scale** — Same model set. Does censorship vs refusal distinction hold?
3. **G15: Vocabulary compression at scale** — Same model set. Does the 38% generation compression hold?

**REMAINING (waiting for sprint results before designing):**
4. **G-future-32: Second-order belief probing** — Berger-inspired. Test whether models can detect DWL in OTHER models' output (not just their own geometry)
5. **G-future-33: Inference-time vs training-time monitoring comparison** — Cundy & Gleave inspired. Compare geometric detection accuracy before and after adversarial training against the detector
6. **G17: Vocabulary dosage** — 1 vs 2 vs 3 vs 5 structural names as generation context. Saturation point?
7. **G18: Vocabulary transfer** — Cross-domain names as scaffold. Does a sociology name help with a psychology question?
8. **F36: Reproducibility** — Re-run G06, G12, G13 with different random seeds and prompt orderings
9. **G-future-37: Qwen 3.5 vs 2.5 comparison** — Has the architectural generation changed geometric behavior?
10. **Confabulation detection via spectral profile deviation** — Karkada approach. May yield stronger signal than raw RankMe threshold
11. **G-future-23: Evasion robustness** — Train a small model against the geometric detector, test whether deeper-layer monitoring catches the evasion (needs GPU)

**DESIGN DEPENDS ON SPRINT RESULTS:** G-future-32-G-future-37 may be modified based on whether the scale sprint confirms or contradicts findings at Qwen 7B. If DWL detection fails at 27B+, the architecture needs fundamental revision. If it holds, the remaining experiments refine dosage and robustness.
