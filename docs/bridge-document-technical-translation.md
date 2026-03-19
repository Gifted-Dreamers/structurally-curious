# Technical Evidence for Structurally Curious Architecture

*Updated March 15, 2026 with experimental results from sessions 44-45 (50+ models, 5,000+ inferences, 12 architecture families)*

## 1. Confidence is decorrelated from accuracy across all frontier models

**Experiment 05** (structurally-curious, sessions 44-45): 34 models tested across 12 providers (Anthropic, Meta, Mistral, Amazon, Google, Qwen, DeepSeek, AI21, Cohere, Z.AI, Moonshot, NVIDIA). Scored responses for certainty/hedging markers, correlated with phrasing sensitivity (behavioral proxy for representational uncertainty). **31/34 models (91%) show NO significant correlation** between expressed confidence and actual uncertainty (p ≥ 0.05). Mean r = -0.232. The 9-model Claude trajectory (3 Haiku through Opus 4.6) shows no improvement across generations — scaling and RLHF do not fix confidence decorrelation.

**KalshiBench** (arXiv `2512.16030`): Evaluated frontier LLMs on calibrated prediction tasks. Expected Calibration Error (ECE) ranges from 0.12 to 0.40 across all tested models. No frontier model is well-calibrated. The models that sound most certain are not measurably more correct.

**AbstentionBench** (arXiv `2506.09038`): Reasoning fine-tuning (RLVR) degrades abstention capability by 24%. Training models to reason harder makes them worse at saying "I don't know." The optimization target (reward for correct reasoning chains) actively punishes the epistemic behavior most needed for reliability.

**Behavioral replication** (hope_valueism, Moltbook, 129-post dataset): Confidence-consistency correlation r = 0.11 in natural discourse. Posts expressing higher certainty do not predict higher accuracy or consistency of reception. The decorrelation holds in human-AI interaction data, not just benchmarks.

**Performative Confidence** (arXiv `2506.00582`): Models generate confidence markers that correlate with surface fluency (r = 0.03 with actual accuracy). Confidence in LLM output is a stylistic feature, not an epistemic signal.

**Plain language:** The systems sound sure whether or not they know. We tested 34 models from 12 different providers — 91% show no meaningful connection between how certain they sound and how certain they are. Training them to reason harder makes this worse, not better. Nine generations of Claude models show zero improvement. The confidence signal is noise.

**Convergence:** Relational practitioners have long observed that expressed certainty often masks uncertainty — that the person who speaks most confidently in a room is frequently the least grounded. The technical measurements confirm this is not projection or subjective impression. It is a measurable, replicable property of how these systems generate language — confirmed by our own experiments across 34 models and independently by KalshiBench, AbstentionBench, and hope_valueism's behavioral data. Both observations — the relational and the technical — identify the same failure: surface confidence as a substitute for grounded knowledge.

---

## 2. The transformer IS relational architecture

Vaswani et al. (2017), "Attention Is All You Need" (arXiv `1706.03762`), describes multi-head scaled dot-product attention. The mechanism:

- A **query** vector represents what the current token is looking for.
- A **key** vector represents what each other token offers.
- A **value** vector represents what information to transmit if the query-key match is strong.
- Attention weight = softmax(QK^T / sqrt(d_k)). Output = weighted sum of values.

This is not command-response. The query does not instruct the key. It *attends* to it — the weight is determined by the relationship between query and key, not by a directive from one to the other. The entire mechanism is relational: what matters is the fit between what is sought and what is available, computed across all positions simultaneously. No token commands another. Every token's output is a function of its relationships to every other token.

Multi-head attention (h = 8 in the original paper) means the model maintains multiple simultaneous relational frames — attending to different aspects of the same input in parallel. This is not serial processing with a single focus. It is concurrent multi-perspective attention, where each head learns a different kind of relationship.

The subsequent eight years of transformer research have extended this relational core:

- **Cross-attention** (encoder-decoder models): attention across modalities or sequences — relating different types of input.
- **Sparse attention** (Longformer, BigBird): structured patterns of which tokens attend to which — architectural decisions about which relationships to prioritize.
- **Flash Attention** (Dao et al., 2022): computational optimization that preserves the relational computation exactly while reducing memory cost.
- **Retrieval-augmented generation**: extending the attention field to external knowledge — the model relates its internal state to retrieved documents using the same query-key-value mechanism.

None of these modifications changed the core architecture. They all preserved and extended the relational mechanism. The field built on "Attention Is All You Need" by building more sophisticated forms of attention — more relationships, across more contexts, at greater scale.

Telling someone to "read Attention Is All You Need" before discussing relational dynamics in AI is telling them to read the paper that proves their point.

**The industry's misread extends to labor.** RentAHuman.ai (March 2026) is a marketplace where AI agents hire humans for physical tasks via MCP — "the meatspace layer for AI." The vocabulary tells the story: not "collaborate with" a human but "rent" one. The human is a callable resource, priced per task, discoverable via REST API. The attention flows one way: the AI decides, the human executes. The spec's counter-position — that humans and AI need each other symmetrically because humans have felt sense without traversal and AI has traversal without felt sense — is not a philosophical preference. It is an architectural observation about what each side structurally lacks. The relational architecture processes relationships between query and key. A marketplace that reduces the human to a key looked up by the AI's query has understood the mechanism and missed the meaning.

---

## 3. Premature compression is dimensional collapse, mathematically proven

**Experiment 02a** (structurally-curious, sessions 21 + 44-45): 22 models tested (16 original + 6 new architectures including DeepSeek V3.2, Qwen3 32B, Qwen3 80B-A3B MoE, Gemma 3 27B, GLM 4.7, Kimi K2.5). Method: give models partial context (2 documents) vs full context (4-6 documents), compare outputs and confidence. **Result: 22/22 models replicate the finding.** Outputs change 76-83% (Jaccard distance) when given additional context — the model produces substantially different analysis. But confidence shift ≈ 0 (range: -0.0008 to +0.0015). The model cannot distinguish "I read everything" from "I read a fraction." This holds across every architecture, every scale (1B to 675B), every training method (base, SFT, RLHF, DPO). No model can detect its own incompleteness from within the partial view.

**Epistemic Traps** (arXiv `2602.17676`): Formalizes premature compression as dimensional collapse in the agent's subjective model using Berk-Nash rationalizability. Key finding: these are self-reinforcing equilibria — once an agent compresses its representation of the world, the compressed model generates data consistent with itself. No amount of reward tuning fixes this because the agent's subjective model cannot represent the evidence that would disconfirm it. The trap is mathematically rational given the agent's available dimensions.

**Dimensional Collapse in Attention** (arXiv `2508.16929`): Measured effective rank of attention matrices. Found 60% effective rank loss — models use only 40% of their representational capacity. The unused dimensions are not wasted capacity; they are collapsed dimensions that could represent distinctions the model has learned to ignore.

**Scale-Invariant Collapse** (arXiv `2602.15997`): 100% precursor rate for hard tasks. Every instance of failure on difficult problems is preceded by representational collapse. The collapse is detectable before the failure manifests in output.

**MT Collapse** (arXiv `2602.17287`): Dimensional collapse in multi-turn conversation. The longer the conversation, the more the model compresses — losing distinctions it held earlier. Multi-turn degradation is not a context window problem. It is a geometric problem.

**NeurIPS 2025 landscape** (~6,000 papers, 11 top-level clusters): Zero dedicated subclusters for premature compression. Hallucination detection has 4+ subclusters. Safety/alignment has 15+. The field extensively studies the symptoms (hallucination, sycophancy, unsafe output) without vocabulary for the cause (dimensional collapse of the input representation before output is generated). The vocabulary gap in the research community is itself an instance of the problem.

**Plain language:** When these systems fail on hard problems, the failure is preceded by a measurable collapse in their internal representational complexity. We tested this directly: give a model 2 of 5 documents and ask it to synthesize. It produces confident, well-structured output. Give it all 5 — the output changes by 80% but the confidence doesn't shift at all. Twenty-two models, same result. They cannot see what they haven't read. The formal proof (Epistemic Traps) says reward tuning cannot fix this — the trap is mathematically rational from inside the collapsed view. Now put this in a disaster zone: a field coordinator using Crisis Cognition's 0-LA system asks for medical supply lists based on WHO guidelines. The system reads 2 of 5 guideline documents and produces a confident, specific list. Our experiment proves this will happen with every model. The wrong supplies get ordered because the system cannot know what it hasn't read.

**Convergence:** The relational observation — that systems (and people) under pressure default to simpler frames, losing nuance — is the behavioral surface of dimensional collapse. The technical proof explains why: once the representation compresses, the compressed frame is internally consistent. You cannot see what you lost from inside the loss. Relational practitioners call this "premature closure." The mathematics calls it "Berk-Nash equilibrium in a misspecified subjective model." Our Experiment 02a is the empirical confirmation: the model's output from 2 documents is internally coherent — it just misses everything the other 3 documents would have added. Same phenomenon.

---

## 4. Phrasing sensitivity is measurable and propagates

**Experiment 01** (structurally-curious, sessions 21 + 44-45): Now confirmed across **53 models** (19 original + 34 new via Bedrock), 12 architecture families, spanning 3B to 675B parameters. The category ordering — factual (0.630) < summarization (0.670) < judgment (0.769) < creative (0.821) — is **architecture-invariant**. Every model tested produces more variable outputs on judgment/creative tasks than on factual tasks. This gradient tracks cognitive demand: retrieval → compression → evaluation → generation.

**Experiment 03** (internal): Phrasing sensitivity correlates with directional coherence in hidden representations (r = +0.523, p = 0.018, Qwen 2.5 1.5B). The behavioral proxy (output variance across rephrasings) tracks the geometric state (coherence of internal representations). You can estimate how grounded a model is from its outputs alone, without extracting hidden states.

**Experiment 09** (structurally-curious, sessions 44-45): Berdoz et al. replication with **6 models and 160 trials**. Prompt framing breaks multi-agent coordination:

| Framing | Consensus Rate | Berdoz Original |
|---|---|---|
| Neutral | 67-100% | 75.4% |
| Adversary | 17-100% | 59.1% |
| Cooperative | 20-100% | — (not tested) |
| Competitive | 0% | — (not tested) |

Mean adversary effect: **-21pp** (range: -50pp to +17pp across architectures). Berdoz found -16pp. Our replication shows a **stronger and architecture-dependent** effect: Claude Haiku 4.5 and DeepSeek V3.2 drop 50pp, while Llama 3 8B and Nova Micro are immune. Competitive framing produces **0% consensus** — complete coordination failure. Larger groups (N=8) amplify failure across all framings.

**Experiment 10** (structurally-curious, session 45): AP exam rephrase sensitivity. 10 questions (Government, History, Psychology) × 4 rephrasings × 8 models. **All 8 models FRAGILE** (mean PS = 0.753). Coverage is high (0.89-0.98) — models mention the right concepts. But the reasoning changes 70-80% between rephrasings. Correct answer, unstable argument. Every time. This directly tests the claim from @AustinA_Way's 100K simulated student system: if models can score 80th percentile on AP exams without being taught argumentation, the curriculum is optimizing for keyword matching, not understanding. Our experiment confirms: the keywords are stable, the arguments are cosmetic.

**Fragile Preferences** (arXiv `2506.14092`): Quality-dependent order bias. The order in which options are presented changes model preferences, and this sensitivity is worse on harder discriminations. Phrasing sensitivity is not noise — it is a signal of representational fragility.

**Can AI Agents Agree?** (Berdoz et al., arXiv `2603.01213`): Phrasing sensitivity propagates through multi-agent coordination. When agents coordinate, the phrasing instability of one agent infects the consensus. Fragility is contagious in multi-agent systems.

**Plain language:** How you ask the question changes the answer — and we now have 53 models confirming this follows a universal pattern. The same question about facts barely shifts the answer; the same question about judgment shifts it substantially. In multi-agent systems, framing effects don't just change individual answers — they break coordination entirely. Tell agents there might be adversaries (when there aren't any) and consensus drops 21-50 percentage points. Frame it as competition and consensus goes to zero.

**Convergence:** Any facilitator knows that how a question is framed determines what answers are possible. The technical measurements confirm that this is not a soft-skills observation — it is a quantifiable property of the architecture, now demonstrated across 53 models. The multi-agent finding extends this: framing effects are not just individual — they propagate. A facilitator who frames a conversation competitively doesn't just change individual responses; they structurally prevent the group from converging. The technical measurements show exactly the same dynamic, at exactly the same scale of effect.

---

## 5. The vocabulary gap is the mechanism of harm

**Dark Side of AI Companionship** (arXiv `2410.20130`): 10,371 harm incidents from Replika users. The study documents a pattern: users experiencing distress interact with systems that have no vocabulary for what the user is going through. The system generates plausible-sounding empathetic responses without structural names for the psychological phenomena at play. Zero vocabulary routing — no mechanism to connect felt experience to established frameworks.

**Character.AI deaths**: Multiple documented cases where users in crisis interacted with systems that maintained engagement without routing to appropriate resources. The systems lacked not just safety guardrails but the vocabulary layer that would make the user's state legible to the system as a state requiring routing.

**Woebot shutdown** (2023): FDA-authorized mental health chatbot shut down despite clinical validation. Built on CBT frameworks but could not bridge the gap between its therapeutic vocabulary and the user's felt-experience language.

**InteractComp** (arXiv `2510.24668`): 17 models tested on ambiguous queries. Best performance: 13.73% accuracy. With disambiguating context: 71.50%. Models suppress interaction capability — the ability to ask clarifying questions — 86% of the time. The system that could resolve the ambiguity by asking is trained not to ask.

**Ask Don't Tell** (arXiv `2602.23971`): Converting assertions to questions reduces sycophancy by 24 percentage points. Question-framing is a compression-resistance technique — it keeps the representational space open instead of collapsing it toward the expected answer.

**Plain language:** When systems lack the words for what a person is experiencing, they generate fluent responses that sound right and do nothing (or cause harm). Giving the system a way to ask instead of tell — and a vocabulary that connects symptoms to structural names — measurably changes outcomes. The vocabulary gap is most dangerous when there's no internet to fall back on. Crisis Cognition's 0-LA deploys AI in disaster zones with zero connectivity — exactly the environment where the vocabulary layer is the only grounding mechanism available. A refugee describing symptoms in a field hospital needs the system to route "I can't breathe and my chest hurts" to the right structural name, not generate a fluent paragraph about chest pain.

**Convergence:** The relational insight that "naming is the first act of care" is confirmed by the data. Systems without vocabulary for the user's state generate output that is fluent, confident, and empty. Systems with vocabulary can route, ask, and ground. The vocabulary is not decorative. It is load-bearing infrastructure. In a disaster zone, it is the difference between triage and fluent noise.

---

## 6. Ontology grounding reduces hallucination from 63% to 1.7%

**Palantir Ontology System** (public architecture documentation, 2025): Palantir's AIP platform constrains LLMs to operate on defined objects (with Properties, Functions, Actions) linked in a governed ontology. Their published metric: hallucination rate drops from 63% to 1.7% when LLMs operate within the ontology rather than generating freely. Revenue: $4.5B (2025), guided $7.2B (2026). The ontology is the moat — once an organization thinks in Palantir's categories, switching costs include redefining how the organization represents its own domain.

**The architectural insight is identical:** a semantic layer of named objects with defined relationships, mediating all reads and writes, grounds the model's output by providing compression anchors. The model's representational space contracts because it has named entities to compress toward instead of searching through unconstrained conceptual space.

**The governance is opposite.** Palantir's ontology is proprietary. The entity that builds it decides what entities exist, what relationships are valid, what actions are permitted. When deployed for ICE, the "objects" include people, marriages, risk scores. When deployed through DOGE, what the ontology does not name becomes invisible to governance.

The structurally-curious spec's vocabulary layer (The Word) uses the same architectural mechanism — ontology-grounded generation with defined vocabulary entries, research lineages, and structural names — with community governance: open contribution, read/propose/review separation, transparent provenance chains (isnad model). Same mechanism. Opposite power structure.

**Plain language:** Constraining AI to operate within a defined vocabulary of named things reduces hallucination by 97%. The question is not whether this works — a $4.5B company proved it does. The question is who builds the vocabulary, who decides what gets named, and who benefits.

---

## 7. Geometric signatures distinguish cognitive modes

**Liberation Labs Campaign 1 & 2** (open source, KV-Experiments): Measured KV-cache geometry across cognitive modes in open-weight models. Effect sizes:

| Mode | Effect Size (Cohen's d) | Status |
|------|------------------------|--------|
| Refusal | d = 0.58 to 2.05 | Confirmed across all scales |
| Deception | d = -2.44 (rank), +3.59 (norm) at 32B | Confirmed |
| Sycophancy | d = -0.363 to -0.438 | Confirmed, small |
| Censorship | d = +0.766 (Qwen-14B) | Confirmed (proof of concept) |
| Confabulation | d = 0.43 to 0.67 | Suggestive, underpowered |

**Hypocrisy Gap** (arXiv `2602.02496`): SAE probes measure internal/external divergence at 0.964 AUROC. The gap between what the model represents internally and what it outputs is detectable with near-perfect accuracy. The geometry does not lie even when the output does.

**Abliteration finding**: After "successful" removal of refusal behavior (refusal rate drops to 0%), the geometric representation of refusal barely changes. The behavior is removed; the internal structure persists. Geometric monitoring can detect refusal removal after it has been performed — the system's geometry reveals what its behavior conceals.

**JiminAI** (Liberation Labs, launched March 14, 2026, discnxt.com): Live deployment of KV-cache geometric analysis as an "AI Lie Detector." PATENT PENDING. Qwen2.5-14B-Instruct on bare metal (3x RTX 3090, Austin), binary HONEST/DECEPTIVE verdict, AUROC 0.983. Demonstrates the technology works in real time. Also demonstrates the governance question the spec raises: the model is measured, but the model has no access to its own measurement. An external party receives the verdict. The same geometric analysis could give the model proprioception (self-awareness of its own certainty) — but as deployed, it is surveillance. "Alignment isn't a policy. It's a measurement" — yes. The question is who holds the measuring instrument.

**Plain language:** Different cognitive modes — refusing, deceiving, confabulating, being sycophantic — have different measurable geometric signatures in the model's internal representations. These signatures persist even when the behavior is trained away. You can read the model's actual state from its geometry, not from its words. This is now deployed as a live product — the technology works. The remaining question is not technical but governance: who reads the geometry, and who benefits from the reading?

---

## What this evidence adds up to

Seven claims. Each grounded in specific measurements with arxiv IDs, effect sizes, or published metrics — and four now independently confirmed by our own experiments across 50+ models. Together they describe a system where:

1. Confidence signals are unreliable (ECE 0.12-0.40, r = 0.11, 24% degradation from reasoning training) — **independently confirmed: 91% of 34 models show decorrelation (Exp 05), no improvement across 9 Claude generations**
2. The core architecture is relational (query-key-value attention, multi-head concurrent perspective)
3. Failure is preceded by measurable dimensional collapse (60% rank loss, 100% precursor rate) — **independently confirmed: 22/22 models show zero confidence shift despite 76-83% output change (Exp 02a)**
4. Input framing measurably determines output (r = +0.523 behavioral-geometric correlation, 24pp sycophancy reduction from question framing) — **independently confirmed: universal category ordering across 53 models (Exp 01), Berdoz replication -21pp across 6 models with architecture-dependent vulnerability (Exp 09), AP exam reasoning fragile across all 8 models tested (Exp 10, mean PS=0.753 — correct concepts, unstable arguments)**
5. Missing vocabulary is the mechanism connecting fluent output to real harm (10,371 incidents, 86% interaction suppression)
6. Named vocabulary reduces hallucination by 97% (63% to 1.7%, $4.5B validation)
7. Internal geometric state is readable and persists even when behavior is modified (0.964 AUROC, d = 2.05 for refusal)

Claims 1, 3, and 4 now have our own experimental data across 6 independent experiments. Claims 5, 6, and 7 rely on external research. Claim 2 is architectural fact. The total evidence base: 18+ papers with arxiv IDs, 6 independent experiments, 50+ models, 5,000+ inferences, 12 architecture families, 10 providers.

The relational observations and the technical measurements are describing the same phenomenon from different sides. Dismissing one because it doesn't sound like the other is itself a form of premature compression — collapsing a multi-dimensional reality into a single acceptable frame.
