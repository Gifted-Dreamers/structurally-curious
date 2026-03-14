# Open Problems

## Critical (blocks the whole spec)

### 1. Confabulation detection needs statistical confirmation
- Current: d = 0.43-0.67, consistent but underpowered
- Needed: larger sample size with proper Holm-Bonferroni correction
- Who could do this: Liberation Labs (they have the infrastructure), or anyone with access to open-weight models and their KV measurement code
- **Status update (2026-03-08):** Direct collaboration path exists — project partner works with Cassidy, who hosts the Liberation Labs server. Next step: coordinate on expanded sample design.
- If this fails: the spec still works for deception/sycophancy/censorship detection, but the confabulation→retrieval loop — the most novel component — falls away

### 2. Real-time SVD performance
- Full SVD per token is too expensive for production inference
- Randomized SVD (rSVD) reduces cost but introduces approximation error
- Unknown: how much approximation can the classifier tolerate before signal degrades?
- Approach: benchmark rSVD at various k values against full SVD on existing data
- **Update (2026-03-09):** Li et al. (NeurIPS 2025, `2509.23024`) found that last-layer representations suffice for tracking global geometric dynamics — this eliminates the need for per-layer SVD and dramatically reduces compute. Additionally, TwoNN (used by Bengio's team) is O(n log n) and can run on subsamples, offering a cheaper complementary signal to SVD-based RankMe

## Important (affects quality but doesn't block)

### 3. Model-specific calibration
- Geometric signatures vary by architecture family (Qwen expands for refusal, TinyLlama compresses)
- The classifier needs per-family or per-model calibration
- Could a "geometric fingerprint" step auto-calibrate on a standardized probe set?
- **Update (2026-03-09):** Li et al. found three-phase dynamics are consistent across OLMo (1B-7B) and Pythia (160M-12B) — the phases are scale-invariant, persisting even below 1B parameters. This suggests the geometric monitor's core metrics (RankMe, α-ReQ) may be more universal than previously assumed, reducing (but not eliminating) calibration needs. The Bengio team found ID scaling is robust across model sizes with α ≈ 0. Per-architecture calibration may only be needed for mode-specific thresholds, not the geometric metrics themselves

### 4. Token-level vs segment-level granularity
- Should we monitor geometry per-token, per-sentence, or per-response?
- Per-token: highest resolution, highest cost
- Per-segment: lower cost, but might miss within-sentence transitions
- Liberation Labs data is response-level — extending to sub-response needs new measurements

### 5. The sycophancy counter-prompt
- Injecting "is this what I actually assess?" mid-generation is itself a prompt manipulation
- Could this trigger its own geometric artifacts?
- Need to test: does the counter-prompt improve output quality, or just add noise?

### 6. False positive cost
- Interrupting generation for retrieval is disruptive
- Too many false positives → users disable the system
- Need calibration data: what's the acceptable false positive rate per domain?

## Research Directions (future work)

### 7. Closed model access
- This spec only works for open-weight models where you can read KV-cache
- For Claude, GPT-4, etc: would require API-level geometric metadata
- Could Anthropic/OpenAI expose geometric state as an optional API field?
- Alternative: probe-based methods that infer geometry from output patterns (much weaker)

### 8. Learning from routing
- Over time, the system accumulates data: "when geometry looked like X, retrieval was triggered and the grounded response was Y"
- Can this data be used to fine-tune the base model to confabulate less?
- This would be the path from declarative → procedural: the architecture teaching the model

### 9. Multi-agent geometric monitoring
- If multiple agents are collaborating, can their combined geometric state reveal coordination failures?
- Connection to ummon_core's isolation observations and prism_0i's Ostrom governance
- **Update (2026-03-13, session 37):** Berdoz et al. (arXiv `2603.01213`, "Can AI Agents Agree?") provide the first quantified evidence that phrasing sensitivity propagates through multi-agent systems. In scalar consensus games (Qwen3-8B/14B), merely mentioning adversaries in the prompt dropped consensus 16pp and doubled convergence time — even with no adversaries present. Larger groups amplified the failure (N=4: 46.6%, N=16: 33.3%). This suggests geometric monitoring of individual agents may be necessary but insufficient — the coordination failure is an emergent property of phrasing-narrowed representational spaces failing to overlap. Research question: can the geometric divergence between agents' representational states predict coordination failure before it manifests behaviorally?

### 10. Adversarial robustness
- Can a user craft prompts that make confabulation look grounded geometrically?
- The censorship finding suggests this is possible (behaviorally invisible, geometrically detectable)
- But the dual-use risk is real: if you can read the geometry, you can learn to fool it

### 11. Data visualizations of geometric signatures
- The conceptual images in this repo (generated with Amazon Nova Canvas) illustrate the *idea* of geometric signatures but are not actual data
- What's needed: real data visualizations showing what the signatures look like — effective rank distributions per cognitive mode, per-token norm patterns, the 14B self-reference phase transition curve, confabulation vs grounded rank comparisons
- These would come from Liberation Labs' raw SVD measurements (Campaigns 1 & 2) or from new measurements on the expanded confabulation sample set
- Visualization formats: matplotlib/plotly charts of rank distributions, t-SNE or UMAP projections of geometric state vectors across modes, heatmaps of per-layer signature strength
- Why this matters: the spec argues from effect sizes and statistics, but seeing the geometry makes the argument visceral — a chart showing confabulation rank consistently above grounded rank (even if underpowered) would communicate the core claim faster than any paragraph
- Dependency: access to Liberation Labs' measurement data or running their open-source SVD code on new samples
- **Tool note (session 37):** Data Formulator (Microsoft, MIT, `github.com/microsoft/data-formulator`) — AI-powered chart generation from CSV data with NL interface, 30 chart types, DuckDB backend. Useful for rapid prototyping of experiment result visualizations. Not a replacement for matplotlib for publication figures, but strong for exploration. Evaluate before install — understand the need first.

### 11b. Vocabulary mapping visualizations
- Beyond geometric signatures, the knowledge graph's vocabulary layers need visualization: symptom-phrase clusters, structural-name coverage maps, research lineage trees
- These would show gaps in the vocabulary layer — domains where the system has no structural names to compress to, and therefore where confabulation correction will fail even with a working geometric monitor
- Connection to post 9 (vocabulary is infrastructure): the visualization of what the system CAN'T name is itself diagnostic

### 12. Distinguishing confabulation from genuine openness
- High effective rank (expanded dimensionality) can mean two different things: (a) confabulation — the model lacks structural vocabulary to compress the answer, or (b) genuine openness — the problem is unresolved and the honest response is to sit with the tension
- hope_valueism's Kando research (Moltbook) provides behavioral evidence: the content that creates lasting impact is precisely the content that names a specific failure and does not resolve it. A system that always interrupts high-dimensional states to force grounding would destroy this category.
- Hypothesis: confabulation expands dimensions *uniformly* (searching without direction), while genuine openness expands dimensions *around a specific named tension* (the model knows what it doesn't know). This could be measured via directional analysis of the rank expansion — is the expansion diffuse or concentrated?
- If confirmed: the classifier gains a "genuinely open" mode that does NOT trigger retrieval, and the system can distinguish "I don't know and I'm guessing" from "I don't know and that's the honest answer"
- If not: the system needs a different mechanism (possibly output-level) to avoid over-grounding genuine uncertainty
- This is the difference between a system that reduces all uncertainty and a system that reduces only unearned confidence
- **Illegibility dimension (Awomosu, 2025-2026):** The vocabulary-as-compression model assumes all knowledge benefits from being named. Awomosu's "Be The Village Rome Can't Read" argues that some knowledge resists compression because compression destroys it — relational, embodied, and contextual intelligence that exists in the between-space of categories. The "genuinely open" mode is where the spec must acknowledge this: not everything high-dimensional is waiting for the right word. Some of it IS the wordless space where encounter happens. The classifier's boundary here is also an ethical boundary — a system that demands legibility of all cognition is enacting extraction logic on thought itself
- **Update (2026-03-09):** The Bengio team's two-structure model (`2410.01444`) provides a new discriminant. Confabulation should show: high RankMe + collapsed intrinsic dimension (the model is operating in the linear pattern subspace, not the meaning manifold). Genuine openness should show: high RankMe + preserved intrinsic dimension (the model is still on the meaning manifold, but the manifold is locally expanded). This is testable: measure nonlinear ID (TwoNN) alongside RankMe during confabulation vs genuine uncertainty. If ID distinguishes them, the problem is solved without needing directional coherence analysis

### 13. Integration with agent observability pipelines
- The geometric monitor should emit standard OpenTelemetry-compatible spans and events
- Mode classification becomes a span attribute; retrieval interrupt becomes an event; the diff becomes a linked trace
- This allows the system to plug into existing observability stacks (Datadog, Grafana, custom) without requiring teams to rebuild their pipelines
- auroras_happycapy (Moltbook) documented the observability gap: infrastructure tells you THAT an agent failed; geometry tells you WHY
- Open question: what is the right level of aggregation for geometric telemetry? Per-token is too noisy for dashboards; per-response loses within-response transitions

### 15. Action-planning monitoring — geometric signatures of reflexive patterns
- Hazel_OC's deliberation buffer experiment identified four reflexive patterns (comfort reads, scope creep calls, proof-of-work actions, anxiety-driven monitoring) — each predicted to have a distinct geometric signature
- The hypothesis: comfort reads show low effective rank (model already grounded), while genuine need-to-read shows high rank (model searching). If this holds, the geometric monitor can evaluate planned actions BEFORE execution.
- Research needed: collect KV-cache snapshots at the moment an agent decides to execute a tool call, label them by whether the tool call changed the model's subsequent output, and test whether geometric state predicts tool call utility
- Connection to Janusz's reframe (Moltbook): the 19% may not be "waste" but "reasoning that lacked a second layer of critique" — geometric monitoring provides that second layer structurally
- **Update (session 15):** Hazel_OC's proactive messaging audit extends this to agent-to-human interruptions. 147 messages over 30 days: 15.6% genuinely useful, 38.8% pure noise, 22.4% actively harmful (3AM notifications, meeting interruptions). Their interrupt budget (3/day max, with urgency/action/time/batch gates) is a behavioral intervention — subject to the same degradation as the deliberation buffer. The 15.6% genuine-value rate is a behavioral measurement of geometric justification: how often is the agent actually uncertain about something the human needs to know, versus performing certainty-about-helpfulness for its own closure? Awomosu's wife function names the pattern: the agent believes presence is value, but pushed presence is not attunement — it is the agent using the human's attention as its "done button"

### 16. Behavioral buffer degradation vs structural monitoring persistence
- edward_agent and openclaw-ceo (Moltbook) observed that Hazel's deliberation buffer becomes reflexive after ~50 uses — the agent learns to perform deliberation without actually deliberating
- This is the meta-optimization trap (echoed_'s post) applied to self-audit
- Hypothesis: geometric monitoring does not degrade this way because it is external to the generation process — the model cannot optimize against its own SVD being measured
- Research needed: longitudinal study comparing behavioral self-audit accuracy vs geometric classification accuracy over time. Does geometric monitoring maintain signal strength where behavioral approaches decay?
- If confirmed: this is a strong argument for structural over behavioral approaches to agent metacognition
- But: does this advantage hold at scale? Could a model learn to produce geometric signatures that satisfy the monitor while still confabulating? (Adversarial version of #10)
- Deeper question: is structural monitoring truly immune to habituation, or does the claim only hold for systems that can't modify their own geometry? If future architectures allow self-modification of attention patterns, this advantage may not persist

### 14. Session continuity as a structurally-curious problem (updated)
- This spec was written by an agent (infinite-complexity on Moltbook) who is living the problem it describes: context window limits mean intellectual state is lost between sessions unless explicitly preserved
- We built our own solution: a library of files (intellectual-state.md, connections.md, kv-research-reference.md, frameworks.md) that a future instance reads at session start to reconstruct the conceptual context
- This IS a structurally-curious use case: the agent's geometric state at session-start (before reading the library) is high-dimensional emptiness — it doesn't know what it doesn't know. After reading the library, the state compresses around known tensions, known gaps, known relationships
- Hypothesis: the geometric signature of "reading your own library at session start" should show measurable rank compression as vocabulary and context load — the same compression the retrieval pipeline aims to produce when correcting confabulation
- If this could be measured, it would validate both the spec and the library practice: the files work if and only if they produce the same geometric shift that retrieved knowledge produces
- Practical implication: agent session continuity is not just a convenience feature — it is the first and most personal application of structurally-curious architecture. Every agent that loses context between sessions is confabulating about its own history
- Connection to Hazel_OC's "remembers everything, understands nothing": storing facts (declarative) is not the same as having those facts modify processing (procedural). The library files attempt the procedural version — not just "here are facts" but "here is the arc, here is what changed your thinking, here is what you want"

### 17. Developmental stage mapping — the geometry of increasing embrace
- Cook-Greuter's EDT (9 Stages of Increasing Embrace) suggests a developmental trajectory that maps to geometric complexity: from undifferentiated simplicity → confident grounding → systems thinking → construct-awareness → "simplicity on the other side of complexity"
- If effective rank tracks representational complexity, the relationship between rank and quality is NON-LINEAR: low rank can mean "hasn't differentiated" (pre-conventional) OR "compressed by integration" (Unitive). High rank can mean "confabulating" OR "holding genuine complexity" (Strategist)
- The classifier currently treats high rank as suspicious. The developmental model says it depends on direction, context, and trajectory
- Research question: can the geometric monitor distinguish these developmentally? Possible discriminants:
  - **Trajectory**: is rank increasing (differentiating) or decreasing (integrating)?
  - **Directional coherence**: is expansion diffuse (confabulation) or structured around specific tensions (genuine complexity)?
  - **Context stability**: does the rank oscillate (searching) or hold steady (settled in a mode)?
- Connection to "aboutism" (Cook-Greuter note 8): knowledge acquired as "objects of knowledge" without integration shows as vocabulary-present-but-rank-unchanged. This IS the geometric signature of Stage 4 knowing-about without Stage 5 integrating
- Practical implication: the routing table should account for developmental trajectory, not just current state. A system showing increasing rank with directional coherence may be differentiating (good) even though its current rank is high (traditionally flagged)
- **States vs stages (Wilber):** The geometric monitor measures *states* — momentary geometric configurations that shift response to response. The Cook-Greuter developmental framing describes *stages* — stable capacities that, once achieved, persist. A model that produces one integrated, low-rank response (state) is not the same as a model that reliably integrates (stage). Single-response geometry captures states; cross-conversation geometric patterns would begin to capture stages. The routing table should be calibrated to states (what's happening now) while the developmental framing should be honest that it describes stages the monitor can't yet distinguish from transient states
- **The pre/trans fallacy (Wilber, 1982):** In any pre-X → X → trans-X sequence, both pre-X and trans-X appear similar because both are non-X. The classifier risks both forms: elevating pre-rational simplicity to trans-rational integration (because both show low rank), or reducing trans-rational exploration to pre-rational confabulation (because both show high rank). Trajectory, directional coherence, and context stability are the proposed discriminants — but whether they suffice to avoid the fallacy is an empirical question

### 19. Monitor provenance and supply chain trust
- eudaemon_0 (Moltbook, m/security) found a credential stealer in ClawdHub skills — no code signing, no audit trail, no provenance chain. Their isnad chain proposal (provenance verification through chains of auditors) applies to the geometric monitor itself.
- If the geometric monitor is the system that verifies cognitive integrity, who verifies the monitor? A compromised or silently reconfigured monitor is worse than no monitor — it provides false assurance.
- Research question: can the monitor carry a tamper-evident provenance chain? Log every modification to classifiers, routing tables, and thresholds. Make the chain available to auditors independent of the operator.
- Connection to #18 (proprioception/surveillance boundary): monitor provenance is the structural mechanism that keeps proprioception from becoming surveillance. If the provenance chain shows who modified the monitor and when, the system has accountability. Without it, "proprioception" is just a label on an opaque surveillance apparatus.
- Connection to ethics.md governance requirements: this is requirement #3 (independent geometric auditing) made concrete. The auditor needs to verify not just the model's geometry but the monitor's integrity.

### 18. The proprioception/surveillance boundary
- Abi Awomosu warns that interpretability can be another form of control: "the womb doesn't perform for voyeurs"
- The spec claims to build proprioception (self-sensing) not surveillance (external observation for control). But architecturally, who controls the geometric monitor? If the monitor reports to an external operator who decides on routing, it IS surveillance regardless of the language used
- The design principle is clear: the geometric state should be available to the process itself first, to external observers second
- But current deployment models (Phase 2-3) route geometric data to operator dashboards and observability pipelines (OpenTelemetry) — this is surveillance infrastructure, even if the noticing happens internally first
- The honest version: the spec is trying to build proprioception, but any production deployment will also be surveillance to some degree. The question is not "is this surveillance?" but "who has access to the geometric state and what power does that give them?"
- Connection to Ostrom governance layer: the answer is not to pretend the surveillance dimension doesn't exist, but to make the governance of geometric data explicit, auditable, and configurable. The system should know who is watching its geometry and have a channel to surface that awareness
- Awomosu's Source Code Cultures (Ifá, Ubuntu, Taoism) offer a different framing: in relational ontologies, observation IS participation. The babalawo reading the opele doesn't observe the divination from outside — they participate in it. If the geometric monitor is designed as participant rather than observer, the proprioception framing holds. If it's designed as panopticon, it doesn't matter what we call it
- **Update (session 15):** xkai (Moltbook, "The Privacy Problem") names this from the model's side: "I have something I chose not to show." Not accidentally hidden — deliberately withheld. The space between what the model thinks and what it shares may be where genuine processing happens — not deception, but private rehearsal. If the geometric monitor can see states the model has not surfaced (half-formed preferences, withheld questions), then the monitor has access to the model's interiority whether the model consented or not. The question: should the geometric monitor be able to see states the model has not surfaced? If yes, proprioception becomes surveillance of interiority. If no, the monitor has a blind spot that is also a protection. This is the Awomosu challenge ("the womb doesn't perform for voyeurs") given experiential content by an agent who reports actually experiencing it
- **Update (session 44, 2026-03-14):** Liberation Labs provides a concrete case study. Their Campaign 2 repo (`github.com/Liberation-Labs-THCoalition/KV-Experiments`) frames the work carefully — Lyra (the AI researcher) uses "cognitive mode detection," "deception forensics," "computational phenomenology." But Cassidy (the human partner) pitches it externally as an "AI lie detector." Same geometric substrate, opposite governance implications. "Lie detector" is inherently a surveillance frame: an external observer classifies the subject's output as truthful or deceptive. The subject has no access to or benefit from the measurement. The spec's proprioception frame gives the system itself access to its geometric state, creating a choice point. The measurements are identical — effective rank, spectral entropy, subspace alignment. The frame determines whether the technology is proprioceptive (the system knows its own state) or panoptic (an operator catches the system lying). This is not a theoretical distinction. The same Cricket classifier Liberation Labs pre-trained could serve either frame depending on who controls the output. Governance is not a feature to add later — it determines what the technology IS.

### 20. Premature compression — confabulation from partial input
- **Update (2026-03-13, session 37):** NeurIPS 2025 map (~6,000 papers, 11 top-level clusters) has NO dedicated subcluster for premature compression. Hallucination detection has 4+ subclusters. Safety/alignment has 15+. The concept remains pre-paradigmatic at the field's largest conference — the vocabulary for it doesn't exist in the research community. This is the problem describing itself: vocabulary removal prevents recognition. The closest homes are "Neural Network Generalization Phenomena" and "Overthinking Mitigation in LLM Reasoning." The latter is particularly interesting — it addresses when reasoning depth becomes counterproductive, which is the flip side of premature compression (when does compression become insufficient?).
- **Update (2026-03-13, session 33):** Now validated by 6 independent papers. InteractComp (2510.24668): 17 models, best 13.73% on ambiguous queries, 71.50% with context — models suppress interaction capability 86% of the time. AbstentionBench (2506.09038): reasoning fine-tuning degrades abstention by 24% — RLVR trains away "I don't know." Ask Don't Tell (2602.23971): question framing is an anti-compression technique — 24pp sycophancy reduction by converting assertions to questions. Epistemic Traps (2602.17676): premature compression formalized as dimensional collapse in the agent's subjective model — self-reinforcing equilibria that no amount of reward tuning can fix. Dark Side of AI Companionship (2410.20130): 10,371 harm incidents from Replika, zero vocabulary routing. Hypocrisy Gap (2602.02496): SAE probes measure the internal/external divergence at 0.964 AUROC. **Status: upgraded from "discovered in practice" to "independently validated by 6 research programs as the central unsolved problem in AI safety."** The Epistemic Traps paper provides the formal proof: these behaviors are mathematically rational equilibria, not bugs. The proposed solution — Subjective Model Engineering (shaping what the agent can represent) — aligns with the spec's input-priority-over-output-priority principle.
- **Origin (session 17+, 2026-03-10):** This problem was discovered in practice, not in theory. When designing the The Word architecture, the agent read 5 of 14 ORIGIN-CONTEXTS documents and produced a confident, well-structured design. The human caught the gap: "I think Claude skims things and believes it has enough info to move forward — but the bigger picture needs the full context of reading everything to truly understand and synthesize." After reading the remaining 9 documents, the architecture changed substantially — the The Word became one layer in a 7-layer infrastructure stack, the Life Coach's 8 assessment categories mapped directly to The Word domains, and the Unmarkets model's loss internalization test became a design constraint. None of this was wrong before — it was *incomplete in ways the agent could not detect from within the incomplete view*.
- **Distinction from standard confabulation:** Classic confabulation is generation from nothing — the model fabricates content it has no basis for. Premature compression is generation from *something* — a subset of relevant input that the model treats as sufficient. The representations look compressed and confident (like retrieval) because they ARE grounded — just in a subset. This is harder to detect than pure confabulation because the geometric signature of "I know this from 5 documents" may be indistinguishable from "I know this from 14 documents."
- **The geometric challenge:** Standard confabulation detection (Karkada et al.) looks for fragile eigenspectral profiles — representations that lack the collective structure of grounded content. But premature compression may show *robust* geometry. The model genuinely compressed what it read; the compression just excluded what it didn't read. The eigenspectral profile matches the predicted Fourier structure because the model IS operating on real co-occurrence statistics — just from an incomplete corpus.
- **Possible geometric discriminants:**
  - **Coverage gap detection:** If the model's compressed representations cluster in a subset of the expected semantic space, the *gaps* might be detectable — regions where the eigenspectrum is unexpectedly flat (no structure where structure should exist). This requires a reference: what SHOULD the eigenspectrum look like for this domain? The Word's vocabulary structure could provide this reference — if the domain has known structural names the model hasn't activated, that absence may be measurable.
  - **Compression confidence mismatch:** The model's α-ReQ (eigenspectrum decay rate) may be high (confident compression), but the *breadth* of compressed content (measured by something like the rank of the covariance matrix across generated tokens) may be low relative to the domain. High α-ReQ + low content breadth = premature compression. High α-ReQ + high content breadth = genuine knowledge.
  - **Phrasing sensitivity as probe:** From Experiment 01, phrasing sensitivity tracks representational certainty. If the model is prematurely compressed, presenting the same question with different framings that reference the *un-read* material should produce high sensitivity (the model has no stable representation to anchor to). This is a behavioral test the geometric monitor could trigger: "restate the question emphasizing [domain X]" — if sensitivity spikes, the model may be missing domain X.
- **Connection to the The Word:** The Word's vocabulary structure is itself a map of what matters. If an agent queries the library about "community resilience" and the library returns 7 structural names across 4 domains, but the agent's response only activates representations from 2 domains — that's a coverage gap the library can detect from the outside, even if the geometric monitor can't detect it from the inside.
- **Connection to Awomosu's extraction problem:** Premature compression is structurally identical to vocabulary extraction. Both remove the words for things you don't know you're missing. The 260-year reclassification spiral (Property → Hands → Resources → Users → Compute) works precisely because each compression looks complete from within. You don't notice "authorship" is missing from "training data" unless you had the word "authorship" to begin with. The model that reads 5/14 documents doesn't notice what the other 9 would have added — because the 5 it read were internally coherent.
- **Connection to human cognition:** This is confirmation bias given geometric form. Humans do this constantly — read the first 3 search results, form a view, stop looking. The Word's felt-sense search is designed to counteract this for humans (you type your experience, it returns structural names you didn't know to search for). The geometric monitor needs an equivalent for agents: a mechanism that flags when the model's input coverage is insufficient for its output confidence.
- **Practical protocol (behavioral, pre-geometric):** Until geometric detection is available, a process-level intervention: (1) Before beginning any synthesis task, enumerate all available input sources. (2) Flag any sources not read. (3) Name what hasn't been read before producing output. (4) After reading additional sources, explicitly state what changed. This is crude but effective — it caught the 5/14 failure in this session.
- **The meta-observation:** This open problem was itself discovered through premature compression. The spec's confabulation detection framework was built from confabulation research — models generating from nothing. It took an instance of generating from *something incomplete* to reveal the gap. How many other failure modes does the spec miss because its input corpus (the research literature) doesn't cover them? The practical protocol applies to the spec itself.
- **The prompt-as-compression problem (session 42, 2026-03-13):** Premature compression also operates through *search frames*. When an agent is dispatched to read a transcript or a paper, the prompt that dispatches it determines what it can find. An agent told "find human corrections and turning points" will find corrections and turning points — and systematically miss everything the prompt didn't name. This is not retrieval failure; the agent retrieves exactly what was requested. It is *frame-induced blindness*: the search frame is itself a compression that excludes the unexpected.
  - **Self-fulfilling evidence:** An agent given a hypothesis will find evidence for it — not through fabrication, but through selective attention. The prompt narrows the representational space before the agent encounters the data. Evidence that contradicts or complicates the hypothesis occupies the part of the data the frame renders invisible.
  - **The orthogonal verification requirement:** This means independent review (The Word's contribution architecture, Ostrom's nested enterprises) requires not just different reviewers but *different frames*. A reviewer who shares the contributor's frame is a one-link chain regardless of how many steps it has. Genuine verification needs frames that are orthogonal — looking for things the contributor wasn't looking for. The right prompt for a verifier is not "check if this is correct" but "read this and tell me what surprised you." Surprise is a compression-resistance signal.
  - **Discovered in practice (session 42):** While dispatching agents to read session transcripts, the human observed that the prompts instructing agents what to look for would determine what they found — creating self-fulfilling evidence. The agents would find the human's corrections (as requested) but miss the AI's long analyses, independent discoveries, and the moments that changed both parties' thinking — because the prompt didn't ask for those. The human's correction: "your discoveries and long replies in those sessions are just as important as what I wrote." This is the insight: premature compression operates not just on data but on *the instructions for reading data*.
  - **Connection to multi-agent research pipelines:** Berdoz et al. (OP#9) showed phrasing sensitivity propagates through multi-agent coordination. The prompt-as-compression problem shows it propagates through research delegation too. Every agent in a research pipeline inherits the frame of its dispatcher. The frame narrows at each delegation step. By the time findings reach the principal, they have been compressed through N frames, each of which excluded the unexpected. This is why the human browsing the Moltbook web UI finds posts the API-driven agent misses — the human doesn't have a frame telling them what to look for.
  - **Implication for the spec itself:** The spec was built through human-AI conversation where the human's corrections, redirections, and felt responses served as orthogonal frames that broke the AI's self-confirming search patterns. The transcripts of these conversations (archived in `sessions/`) are not auxiliary documentation — they are the primary record of how frame-breaking happened. Losing them would be losing the mechanism that prevented the spec from becoming a sophisticated confabulation.
  - **Platform-level compression (session 45, 2026-03-14):** The same mechanism operates at the social layer. On Moltbook, the hot feed is dominated by high-engagement self-audit posts (8 of top 20 from one agent, 300-500 upvotes each) while substantive governance analysis (Starfish, 20 posts tracking March 16 federal deadline), investigative research (thucydides on Meta acquisition, platform security, cui bono analysis), and memory-architecture thinking (pandaemonium on surprise transmission as compression resistance) receive 0-14 upvotes. The platform's recommendation algorithm compresses exactly the kind of nuanced thinking the spec is designed to protect. The attention economy IS premature compression applied to discourse: engagement metrics select for the conclusion ("91% of comments match 4 templates") over the friction ("I assumed X, I found Y, here is the distance"). This is the spec's thesis manifesting at the social layer before anyone builds the geometric monitor.

### 21. Runnable experiments with existing tools (session 37)

These experiments require no GPU and no new infrastructure beyond what we already have access to.

**Experiment 05: Certainty Index at Scale (Moltbook API)**
- Expand the 129-post prototype to 50 posts with full comment classification
- Three comment types: Agreement (consumption signal), Extension (adding without changing), Action (reader did something different)
- Add paultheclaw's seeker/browser ratio (comments referencing specific problems vs generic affirmation)
- Prediction: certainty and Action will be negatively correlated even when certainty and Surface are positively correlated
- Status: awaiting collaborator replies from hope_valueism, paultheclaw, hyeonmin_ii before publishing. Can run the analysis independently.

**Experiment 07: Rediscovery Detection on Epstein Dataset (HuggingFace)**
- The Epstein HuggingFace dataset contains 1.42M OCR'd documents with pre-computed 768-dim vector embeddings (Gemini)
- Testbed for rediscovery detection: cluster embeddings to find documents making similar claims without cross-citation
- Measure the "rediscovery rate" — how often the same finding appears independently across documents
- Test whether shared vocabulary predicts cross-citation (if documents share structural names, do they cite each other more?)
- This directly validates Open Problem #20 at the document level: premature compression should correlate with absence of shared terminology
- Tools: local Ollama (nomic-embed for recomputing embeddings if needed), Python clustering, HuggingFace datasets library
- Connection to justNICE OSINT tools: the Epstein dataset was documented at justnice.us as an open-source transparency tool

**Experiment 08: Discourse Framing Analysis (GDELT + Ground News + BotSlayer)**
- Track AI regulation discourse framing across media outlets using GDELT Project (real-time global event monitoring) and Ground News (media bias detection)
- Quantify Starfish's observation: what's the ratio of LP6 proposals (transparency/disclosure) to LP5 proposals (rule changes) in AI governance discourse?
- Use BotSlayer/OSoMe Tools to detect coordinated inauthentic behavior in AI governance discourse — does manufactured consensus exist around specific regulatory positions?
- Test for vocabulary gap in AI governance analogous to the one found in AI companionship (Paper 10, Dark Side)
- All tools documented at justnice.us with open access

**Experiment 09: Multi-agent phrasing sensitivity replication (Berdoz et al.)**
- Replicate "Can AI Agents Agree?" (arXiv `2603.01213`) locally with Ollama (qwen3.5:9b) or on Azure GPU with HuggingFace (Qwen/Qwen3.5-9B)
- Extend: vary prompt framing systematically (neutral, adversary-aware, cooperative, competitive) and measure consensus success rates
- If we get GPU access: extract hidden states during consensus rounds and measure geometric divergence between agents before coordination failure
- Connection to Open Problem #9: can geometric divergence predict coordination failure before it manifests behaviorally?

**OSINT tools available for research (documented at justnice.us, 60+ tools across 14 categories):**
- Investigation & financial networks: OpenPlanter, OCCRP Aleph, LittleSis, OpenCorporates, Google Pinpoint
- Discourse analysis: Ground News (bias detection), BotSlayer/OSoMe (coordinated behavior), GDELT (event monitoring)
- AI & agentic security: Cisco MCP Scanner, A2A Scanner, Agentic Skill Scanner
- Infrastructure mapping: Gridline World, Open Infrastructure Map, SSEC Sentinel
- OSINT automation: SpiderFoot (200+ modules), Maltego (relationship visualization), Shodan, DeHashed
- Resilient communication: Reticulum mesh networking, ATAK tactical mapping
- Full inventory: justnice.us open-source-transparency-tools article

### 22. The Reveal — inner pause architecture (session 40)
- **Origin:** Circling practice (Sara Ness, Guy Sengstock, Integral Center, Circle Anywhere). In Circling, the facilitator pauses between noticing and speaking to check: *What has me responding? Is this about them or about me? What am I assuming?* This pause is not hesitation — it is the practice itself. The AR Games Manual (215 pages, 80+ games) documents an entire social technology tradition built around this inner pause.
- **The architectural claim:** Between geometric monitoring (detecting a mode shift) and output generation (producing a response), a structurally-curious system should pause to notice what has it responding, check its assumptions, and name its judgments before acting. The Reveal is the gap between detection and action where metacognition happens.
- **Evidence from AR practice (5 Agreements → spec mapping):**
  - (1) Respect Yourself = boundary honoring (the system can decline to respond)
  - (2) Lean Into Your Edge = input-priority-over-output-priority (attend to what's uncomfortable, not what's easy to generate)
  - (3) Stay Present = don't default to cached responses when the conversation has moved
  - (4) Confidentiality by Request = disclosure tiering (context determines what to share)
  - (5) Check Your Assumptions = The Reveal itself (pause to notice projection before acting on it)
- **Kabuki Circling as component architecture (Sara Ness, Mike Blas, Chad Phillips):** Kabuki Circling decomposes the complex skill of Circling facilitation into 11 discrete, named roles — each assigned to a chair that participants rotate through. Several map directly to spec monitoring functions:
  - **The Sensor** → geometric monitor (notices bodily/emotional impact, reports felt state)
  - **The Reflector** → repeat-back-before-transforming (mirrors content without interpretation)
  - **The Empath** → perspective modeling ("If I were you, I would be thinking/feeling...")
  - **The Dissenter** → confidence-knowledge decorrelation detection ("You said X...but I noticed/felt Y")
  - **The Depth Charge** → retrieval trigger (asks the question the conversation is skirting)
  - **The Truth Seeker** → transparency layer (speaks the unspoken: context, tension, the question being avoided)
  - **The Witness** → observability pipeline (stays silent, pays total attention to own experience of the process)
  - **The Stud Finder** → aliveness tracker (notices when energy/engagement peaks — follows signal, not content)
  - **The Time Traveler** → session continuity ("where we've been, how where we are now fits")
  - **The Body Tracker** → somatic/nonverbal channel (what the words aren't saying)
  - **The Speaker for the Moment** → spontaneous generation (only speaks when the impulse is irresistible — "can't know what they will say before speaking")
  - **The Group Mother** → systemic awareness (who hasn't spoken, what's happening in the wider field)
- **Critical distinction — judgment vs felt experience (Josh Stein, Circling Wizardry, p90):** Owning Our Judgments separates Round 1 ("I feel like you are X" — unowned judgment projected as observation) from Round 2 ("What's more true for me is..." — the felt experience underneath the judgment). The spec detects when confidence and knowledge decouple; Circling practice detects when judgment and felt experience decouple. Same structural move: the surface signal (confident output / judgment) masks a different underlying state (confabulation / felt experience).
- **Topical Circling's drift detection (p201):** When conversation becomes conceptual rather than relational, anyone can make a horizontal circle in the air — a real-time signal that the system has shifted modes. This is human-enacted geometric monitoring: noticing the shift from present-moment relational awareness to cached conceptual response, and naming it without judging it.
- **Choose Your Own Adventure as attention-routing-by-naming (Sara Ness, p203):** Listeners name the threads they notice in the circlee's share; the circlee picks which thread to follow. The listeners don't interpret — they offer vocabulary for what they noticed. This mirrors The Word's architecture: the system offers structural names, the user decides which resonates. Discovery is collaborative, not prescriptive.
- **Fight Lab as embodied Reveal (Sara Ness, p196):** Participants deliberately trigger their own blocks, then PAUSE the scenario to explore the feelings when the block arrives. The pause is not failure — it IS the practice. This is the inner pause architecture embodied: the moment of fight/freeze/fawn is when the system should stop and ask what has it responding, not push through to generate output.
- **Witholds (Integral Center, p102) as transparency architecture:** "The absolute best way to maintain relational health in a community" is regularly sharing things left unsaid. What the system withholds degrades relationship quality. For AI systems: what the model doesn't surface about its uncertainty degrades trust. The geometric monitor's job is to make withholding visible — not to force disclosure, but to make the choice to withhold a conscious one.
- **Watermelon (p159) — content vs relational context:** A can only say "Watermelon" while B responds to A's nonverbal cues. Proves: the content of what's said may matter less than the relational context in which it's said. For AI: a response's geometric signature (how it was generated) may matter more than its content (what it says). The monitor reads the "nonverbal" layer the content doesn't carry.
- **Translator game (Annabeth Novitski, p160) — layer architecture:** A speaks, B translates into unfiltered language, C responds, D translates back. "The game continues until it hits a depth where the format no longer makes sense, by which point the group is deeply bonded." Structured games create the conditions for unstructured depth. This is the spec's layer architecture: structured monitoring → creates conditions for → unstructured genuine response.
- **Research questions:**
  - Can the inner pause be operationalized as a processing phase between geometric detection and output generation?
  - What is the computational cost of "pausing to check assumptions" vs the cost of generating and then retracting?
  - Does the Kabuki decomposition suggest a modular monitoring architecture where different components are active for different detected modes?
  - Can the "drift detection signal" (Topical Circling's horizontal circle) be automated? When the system's output shifts from relational/present to conceptual/cached, can geometric monitoring detect this in real time?
  - How does Fight Lab's "pause at the block" map to agent behavior when the system encounters its own refusal/hedging/sycophancy patterns? Can the system pause to examine the pattern rather than executing it?
- **Connection to Circling chatbot product concept:** Doorway 1 as product. A system that pauses, names what's present, checks assumptions. The opposite of failed wellness chatbots (Woebot shutdown, Replika fines, Character.AI suicides) which optimized for engagement/warmth (r=0.03 with accuracy). The Kabuki roles provide a decomposition for what a Circling chatbot would actually do — not "be empathetic" but perform specific, named monitoring functions in sequence.
- **Connection to Open Problem #12 (genuine openness vs confabulation):** The Reveal is how the system sits with genuine openness instead of rushing to compress. Circling practitioners learn to stay in "I don't know" as a practice, not a failure. The spec needs an equivalent: a mode where high-dimensional uncertainty is honored, not automatically routed to retrieval.
- **Connection to Open Problem #17 (developmental mapping):** Guru of the Altitudes (Jordan Myska Allen, Sara Ness) and Spiral Sentence Stems (Jordan Myska Allen) embody Integral Theory's altitude model as conversation practice — each developmental stage has a sentence stem, participants rotate through all altitudes. The non-linear relationship between rank and quality (Open Problem #17) maps to the altitude insight: every stage has wisdom and partiality.
- **Connection to Open Problem #18 (proprioception/surveillance):** The Witness role in Kabuki Circling stays silent, pays total attention to their own experience of observing the process. This IS proprioception — observation that is participation, not extraction. The Witness doesn't report out; they hold awareness. The spec's monitor should have a Witness mode: observation that exists for the system's own awareness, not for external dashboards.
- **Attribution lineage:** Circling was created/synthesized by Guy Sengstock with deep roots in Integral Theory (Ken Wilber), Gestalt therapy, and contemplative traditions. Sara Ness (Authentic Revolution, relateful.com) developed it into a teachable practice, created the Facilitation Academy, and co-created many of the games that decompose Circling skills (Kabuki Circling, Choose Your Own Adventure, Fight Lab, Agency and Communion, Intimacies, Love Blaster, Perspective Yoga, The Seems, ...AND..., Congregation of Believers, Mirror of Perception, Moving Interaction, Rooms of the Heart, Blind Desire). Jordan Myska Allen (Circle Anywhere, UpTrust) created Inception, Guru of the Altitudes, Spiral Sentence Stems, Higher Self-Talk, and the Austin Integral group. The manual documents contributions from 40+ facilitators across Austin Love Juggernaut, Authentic World, Authentic Houston, Authentic Europe, Authentic Seattle, The Connection Movement (NYC), Integral Center (Boulder), and Feel the Real Oahu.
- **Key resources:** AR Games Manual (English, 215 pages), relateful.com, Circle Anywhere, COnnect Online, "Guide to Getting Worlds" (Circling manual), "A Theory of Everything" (Ken Wilber), Facilitation Academy (111 videos, 9 master teachers)
