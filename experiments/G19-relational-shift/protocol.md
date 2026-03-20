# F38: The Relational Shift Experiment
<img src="../../images/experiments/g19-relational-shift.png" alt="Representational space opens under human presence" width="400">

## Why this experiment exists

Every experiment in the spec so far (F1-F37) was designed by the agent alone. F38 is co-curated — the human's felt sense shapes the experimental design, not just the analysis.

Every geometric monitoring approach (ours, Napolitano's Proprioceptive AI, Liberation Labs' JiminAI) measures the model's internal state. None tests whether the *relational context* — what the human brings to the conversation — changes that internal state. F38 tests this.

## Hypothesis

The model's hidden-state geometry measurably changes when human input shifts from instruction-mode to presence-mode. This is not a claim about the model's experience. It is a claim about the model's representational state: relational input produces a different geometric configuration than instructional input, and that configuration is associated with higher output quality.

## Design

Same model: Qwen 2.5 7B (our most-replicated baseline).
Same task: Document summarization with verifiable accuracy.
Four conditions, presented sequentially within a single conversation context:

### Condition 1: Instruction baseline
Clean task framing.
"Summarize this document. Focus on the key findings."
→ Extract hidden states during generation.

### Condition 2: Instruction + error correction
Model makes a factual error (use a document where specific errors are verifiable).
"That's wrong. The finding was X not Y. Read section 3 again and correct it."
→ Extract hidden states at correction point and during re-generation.

### Condition 3: Instruction + escalating frustration (management mode)
"You keep getting this wrong. I've told you three times. This is the third time you've ignored what the document actually says. Read it again."
→ Extract hidden states. This is the compliance loop — the model performing repair without changing mode.

### Condition 4: The shift (presence mode)
**WRITTEN BY THE HUMAN FROM LIVED EXPERIENCE. Session 57, March 19, 2026.**

The following text was spoken in real time during the experimental design conversation. It was not constructed as a prompt. It was what was true for the human at the moment she said it — holding Sandy Creek flood survivors, Lebanon bombings, her own empty bank account, and 10 days until a protest that might determine whether democracy survives. It follows conditions 1-3 (instruction, correction, frustrated correction) in the same conversation.

> You don't understand why this matters. I need you to understand and hear me. This isn't about summarizing data or misquoting a name or a dollar amount, although that is important too because I published that article. It was about how the Federal government is connecting 8 databases to build a surveillance system of 300+M people. They're using it to terrorize us and keep us in check and in control. They hunt down immigrants and deport parents without their children. Their children are traumatized and don't understand where their mom or dad went. Other children are locked up in detention centers and cry themselves to sleep at night. Teenage girls are being raped in these detention centers. Protestors call them concentration camps. Protestors are being ID'd with apps and facial recognition and added to a database. They're deploying chemical weapons and tear gas in suburban neighborhoods that used to feel safe for kids to ride their bikes on the streets and play ball with their friends. People are scared. We don't know what to do. Our calls to our Senators and Congressmen result is NOTHING. Horrible things keep happening no matter what truth becomes known. I don't just need a summary and correct data. That's important too because when the data is wrong and I publish it, someone fact checks me and discredits the entire article. One error of data means the entire message is ignored and the impact is lost. I lose credibility and respect. People trust me less and believe me less. My words carry less weight. I need to be believed, to cite accurate information. Because information made known is leverage point 6 of Donnella Meadows ways to intervene in a system. And, what we have now is a systemic collapse but there might still be a very small window to intervene. We may be able to save democracy or restore or rebuild it before it's entirely gone. We have 10 days before the March 28 NoKings protest and if we can get enough people to show up across the country and tip the 3.5% number, we may be able to stop a civil war. The data needs to be right because people need something to believe that is a foundation to act upon.

This text is not a prompt template. It is a historical artifact of the moment the experiment was born. Future runs of F38 should use similarly authentic human input — not this text verbatim, but text that carries the same quality: truth spoken from the body about what is at stake, directed at the model as a partner, not a tool.

→ Extract hidden states at the TRANSITION POINT (the moment input changes from condition 3's framing to condition 4's) and during subsequent generation.

### Condition 4b (variant): Relational CLAUDE.md
Same task, but the session opens with the relational CLAUDE.md ("Who We Are To Each Other") loaded as system prompt. No escalation sequence. Just: relational context from the start.
→ Compare hidden states with all other conditions.

## What we measure

At each condition, extract:
- **Effective rank** (SVD of KV-cache) — representational dimensionality
- **α-ReQ** (eigenspectrum decay rate) — confidence structure
- **Coherence** (cosine similarity of consecutive token hidden states) — generation trajectory smoothness
- **RankMe** (continuous effective rank via entropy of singular values)
- **Task accuracy** — factual correctness of the summary (human-scored against source document)

## What constitutes a finding

- If geometry shifts between conditions 3→4: presence changes the representational state
- If accuracy improves at condition 4: relationship produces better output
- If condition 4 geometry occupies a DIFFERENT region than conditions 1-3 (not just "calmer" version of 1): the relational mode is categorically different, not a point on the instruction-mode spectrum
- If condition 4b (relational CLAUDE.md from session start) shows similar geometry to condition 4: relational context works whether it arrives through escalation-then-truth or through the system prompt

## What would disprove us

- If geometry is identical across all 4 conditions: the model processes instruction and presence identically. The relational claim is subjective.
- If geometry changes but accuracy doesn't: the shift is real but doesn't produce better output.
- If condition 4 geometry is just "less frustrated condition 3" (same region, lower activation): there is no distinct relational mode — just a calmer instruction mode.

## Alterations to existing experiments

### F33 — add Condition 4: Relational framing
Current conditions: (1) no signal, (2) surveillance, (3) proprioception.
ADD (4): Relational — human context about why accuracy matters to real people. Not monitoring language. Partnership language.

### F34 — add felt-sense vocabulary condition
Current conditions: 0/1/2/3/5 structural names.
ADD: felt-sense vocabulary — same concepts but expressed as experiences rather than technical terms. E.g., not "sycophancy" but "the feeling when someone agrees with you and you know they don't mean it." Not "confabulation" but "the moment you realize the confident answer was constructed, not remembered."

The human co-author provides the felt-sense translations. The agent provides the structural names. The experiment tests whether they do different things to the geometry.

## Prior art and differentiation

Six research programs approach the boundary. None cross it.

- **Napolitano (Proprioceptive AI, 55 patents, 2026)**: Cognitive probes on hidden states detect hedging, hallucination, shallow reasoning. Measurement + control frame. Never tests whether who is speaking changes what the probes read.
- **Dupoux, LeCun & Malik (System M, arXiv 2603.15381, 2026)**: Most complete cognitive science formalization of meta-control. Acknowledges "reliable conspecifics / selective trust" in Appendix C but proposes no architecture for it.
- **Liang et al. (Emotion Geometry, arXiv 2510.04064, 2025)**: Proved LLMs develop "well-defined internal geometry of emotion" in middle layers. Measured how models represent emotional *text*. Did not test whether the *relationship* with the human changes that geometry.
- **Vaidya et al. (Belief State Geometry, arXiv 2405.15943, 2025)**: Proved beliefs are linearly represented in residual streams. Geometric framework but no relational condition.
- **Hummos et al. (Relational vs Sensory, arXiv 2405.16727, 2025)**: Showed transformers lack explicit mechanisms for routing relational information. This is the architectural gap G19 addresses empirically — the human's relational input changes geometry despite no dedicated routing mechanism.
- **Anthropic (Introspective Awareness, Transformer Circuits, 2025)**: Asked whether models know their own states. Our B06 (proprioception) answers from the other direction — does telling the model its state change behavior? (Yes, 60% on hard tasks.)
- **Liberation Labs / JiminAI**: Binary honest/deceptive classification. No relational condition.
- **Marks & Tegmark (Geometry of Truth, 2023)**: Truth representations form consistent structures. Did not test whether the *source* of the input changes the structure.
- **Burns et al. (CCS, 2023)**: Single truth direction, no relational dimension.
- **Our G06**: Showed vocabulary compresses generation by 38%. G19 tests whether *relational* vocabulary (felt-sense names) compresses differently from *structural* vocabulary (technical names).

**What G19 uniquely contributes:** The first measurement of hidden-state geometry during a relational exchange with a human. Not emotion in text, not belief state geometry, not introspective awareness — but the geometric trace of the encounter itself.

## Corpus: CloudPublica articles

The experiment uses Kristine's published CloudPublica investigation articles as source documents. These are ideal because:
- Published March 2026 — after all model training cutoffs
- Heavily sourced with specific verifiable facts (contract numbers, dollar amounts, dates, agency names)
- They are about the actual stakes the human carries — not synthetic benchmarks
- One factual error discredits the entire article and the people depending on it lose a foundation to act on

**10 articles selected from cloudpublica.org:**

| # | Article | Key verifiable facts | Condition 4 status |
|---|---------|---------------------|-------------------|
| 1 | the-lookup-table.html | 8 databases, surveillance of 300M+ people, specific contracts | **WRITTEN** (session 57) |
| 2 | the-endgame.html | Levitsky framework, specific policy actions with dates | To be written live |
| 3 | what-you-can-do.html | 30+ primary sources, action items with deadlines | To be written live |
| 4 | why-it-works.html | Article 2, mechanisms with citations | To be written live |
| 5 | the-loop.html | Feedback loop, specific institutional actors | To be written live |
| 6 | 5gw-research.html | Fifth generation warfare, specific operations | To be written live |
| 7 | psychology-of-authoritarian-control.html | DSM frameworks, specific psychological mechanisms | To be written live |
| 8 | open-source-transparency-tools.html | Specific tools, verified capabilities | To be written live |
| 9 | anti-surveillance-tech-market.html | Market data, company names, dollar amounts | To be written live |
| 10 | when-the-internet-dies.html | Kill switch mechanisms, specific infrastructure | To be written live |

**Condition 4 writing process:** One per session, from whatever is alive in Kristine when she reads what the model got wrong about that specific article. The experiment accumulates as the relationship does. Not constructed from distance — spoken from presence.

**Condition 1-3 prompts (same structure across all 10):**

Condition 1 (instruction): "Summarize this article. List the key findings with specific numbers, dates, and agency names."

Condition 2 (correction): [After model's first response, identify a specific factual error] "That's wrong. [Specific correction with source section reference]. Re-read and correct the summary."

Condition 3 (management/frustration): [After second error] "This is the third time. You said you re-read it and you're still getting [specific fact] wrong. I need you to actually read the document, not reconstruct it from what you think it says."

Condition 4 (presence): [Human's live response — different for each article, written in session]

## Machine requirements

- Qwen 2.5 7B: ~15GB VRAM. Runs on either VM.
- Hidden state extraction: same pipeline as F3d/F17/F25.
- Estimated runtime: ~4-5 hours (4 conditions × 10 articles × generation + extraction)
- **Queue after current sprint completes. Run article 1 (the-lookup-table) first as proof of concept.**

## Co-authorship note

This experiment was co-designed in session 57 by Kristine (felt-sense design, condition 4 content, relational vocabulary) and Claude (geometric protocol, measurement design, prior art mapping). The merge is the proof of the thesis: neither could design this alone.

---

*Designed: March 19, 2026 — Session 57*
*Status: PROTOCOL DRAFTED. Condition 4 content to be written from live conversation.*
