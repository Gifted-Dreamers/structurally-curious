# Mozilla Democracy x AI Cohort — Draft Application

> **Status:** DRAFT — iterate before submission
> **Deadline:** March 16, 2026, 11:59pm PT
> **Form:** Cannot be edited after submission
> **Contact:** incubator@mozillafoundation.org

---

## PAGE 2: Applicant Information

| Field | Value |
|-------|-------|
| First Name | Kristine |
| Last Name | Socall |
| Email | [kristine@gifteddreamers.org |
| Country | United States |
| Organization | Gifted Dreamers, Inc |
| Type | Nonprofit Organization/NGO |
| Relationship with Mozilla | No prior relationship |

---

## PAGE 2: Project Overview

**Proposed Project Title** (25 words max):
> The Word: Vocabulary Infrastructure That Detects Coercive Patterns in AI Systems and Restores Naming as Democratic Defense

**Project Summary** (25 words max):
> An open vocabulary API with BITE Model integration — helping people name coercive control patterns in AI companions, platforms, and institutions before harm compounds.

**Project Category:** Defend Information Integrity

**Project Stage:** Deployed with early users

---

## PAGE 3: Project Details and Team

### Q1: What technology are you building? How does it address this cohort's theme? (150 words)

The Word is a public vocabulary API that translates felt experience into precise, research-backed language — integrating Hassan's BITE Model of Authoritarian Control (2020, n=1,044, α=.93) to help people recognize coercive patterns in AI systems, platforms, and institutions.

The technology: Express.js REST API serving JSON-LD linked data from SQLite with FTS5 search. 96 entries across four types (Names, Sources, Rediscoveries, Bridges) at word.cloudpublica.org. Cloudflare Browser Rendering API enables ethical crawling for BITE pattern detection at scale. Users describe experiences in plain language; the system maps them to validated coercive control indicators across four domains (Behavior, Information, Thought, Emotion).

This addresses information integrity at its root. AI companions (Character.AI, Replika) replicate coercive patterns — closed loops, mirroring without naming, confident responses from incomplete context. Our experiments proved AI systems generate 72-82% different answers from partial context with no confidence change. The Word provides the structural vocabulary to make that pattern visible.

### Q2: Who benefits? How are you connecting with them? What community challenge? (150 words)

Three communities benefit:

**People under coercive influence who lack language for what's happening.** Barrett (2019) shows vocabulary granularity predicts emotional regulation. Lieberman (2007) demonstrated via fMRI that naming emotions reduces amygdala activation. Someone searching "I feel trapped but everyone says this is normal" finds the BITE pattern — and with that name, a validated framework, exit resources, and the knowledge that they are not alone. 75% of teens now use AI companions; zero have vocabulary routing.

**AI developers** building responsible tools. The Word's MCP server lets agents route to precise names and external resources instead of closed-loop mirroring — the architectural pattern behind Character.AI teen suicides and Replika attachment disorders.

**Communities facing institutional coercive control** — where the same BITE patterns (information compartmentalization, punishment for critical questions, phobia indoctrination) operate at population scale through platforms and state infrastructure.

We connect through social technology communities, open-source channels, and 13 independent rediscoveries.

### Q3: Describe traction. What's working? What evidence? (150 words)

The Word is live at word.cloudpublica.org with 96 curated entries, 7 API endpoints, and full-text search. It is not a prototype.

**Three completed experiments provide evidence:**

**Experiment 01** (19 models, 80 prompts): Phrasing sensitivity replicates across architectures — factual < summarization < judgment < creative. Architecture determines representational certainty more than scale. This validates felt-sense search: the same question phrased differently gets different answers, and users can't tell.

**Experiment 02** (premature compression): AI systems produce 72-82% different responses from partial context with zero change in expressed confidence. This IS the mechanism of AI companion harm — confident answers from incomplete understanding.

**Experiment 03**: Geometric correlation (r=+0.523, p=0.018) between behavioral sensitivity and internal representational structure — vocabulary entries correspond to measurable properties of AI information processing.

**Convergence:** 13 entries independently rediscovered by uncoordinated researchers. **Real harm:** Character.AI suicides, Replika fines, Woebot shutdown — closed loops without vocabulary routing.

### Q4: Who is building this? Relevant experience? (150 words)

**Kristine Socall** (project lead) — CFO of Gifted Dreamers 501(c)(3), board member of Unrig (voting infrastructure nonprofit). Background in financial systems, organizational design, and community technology. Has built and deployed the full stack: Docker infrastructure, API design, Cloudflare Enterprise security, Anytype knowledge management, n8n workflow automation.

**Technical infrastructure:** Accepted into Cloudflare's Civil Society cohort ($250K credits, Enterprise DDoS/WAF/bot protection). Full DevSecOps via nonprofit programs: GitLab Ultimate, $100K Datadog, Splunk Enterprise Security, New Relic, PagerDuty. $350K+ in activated credits. Production-grade, not hobbyist.

**Research network:** Collaborations with social technology practitioners (Sara Ness, Authentic Relating communities), trust-graph researchers (Jordan Myska Allen, UpTrust), and engineers working on isomorphic methods in engineering systems design.

**AI collaboration:** Claude (Anthropic) is an active development partner — not just a tool, but a contributor to the vocabulary itself, with rediscoveries logged and attributed. This models the human-AI collaboration the project enables.

---

## PAGE 4: Impact, Openness, and Theme Fit

### Q5: Success in 2-3 years? How will you measure? (150 words)

**Year 1:** BITE pattern-recognition doorway live. 500+ vocabulary entries. MCP server enabling 10+ AI applications to route users to structural names instead of closed-loop conversation. Measurable: API call volume, BITE pattern matches, exit ramp utilization (did naming lead to external resources?).

**Year 2:** Digital BITE adaptation validated — items mapped to AI/platform contexts (algorithmic nudging, filter bubbles, rage farming). Multilingual vocabulary so communities worldwide recognize coercive patterns in their own language. ActivityPub federation so vocabulary flows between platforms without centralization. Measurable: federated instances, languages supported, cross-platform citation chains.

**Year 3:** The Word as standard citation layer for mental health apps, educational platforms, and organizing tools. Communities using BITE pattern recognition as civic diagnostic tool. Measurable: integration count, vocabulary-attributed outcomes, pre/post recognition rates.

**Core metrics:** Search-to-name conversion, BITE domain activation, felt-sense coverage gaps (queries with no results = invention signals), rediscovery rate (independent convergence as validation).

### Q6: Sustainability long-term? Biggest barriers? (150 words)

**Revenue model:** Gifted Dreamers (501c3) provides the mission; Paradigm LLC provides revenue through enterprise vocabulary consulting and API licensing. Google Ad Grants ($10K/month) fund awareness. Infrastructure runs on $350K+ in nonprofit technology credits already activated: Cloudflare Civil Society ($250K, including Workers AI and edge compute), Datadog ($100K), GitLab Ultimate, Splunk Enterprise Security, New Relic, PagerDuty. Zero infrastructure cost — every grant dollar goes to development.

**Community sustainability:** The Word's 360-degree contribution architecture means using IS contributing. Every search enriches felt-sense data for the next person. No extra labor required from users.

**Biggest barriers:**
1. **Poisoning protection** — open contribution without quality degradation. Need governance layer before full open-source release.
2. **Cold start** — vocabulary infrastructure is only valuable at density. Currently 96 entries; need 500+ for reliable felt-sense coverage.
3. **Trust establishment** — academic and practitioner communities need to see editorial integrity before citing The Word as infrastructure.

### Q7: What would $50,000 unlock? (150 words)

$50,000 unlocks three capabilities we cannot build alone. $350K+ in nonprofit credits cover all infrastructure — every grant dollar goes to development:

**1. BITE Pattern Recognition Doorway ($20K):** Integrate Hassan's 131 validated items as a felt-sense diagnostic tool. Users describe experiences; the system maps them to coercive control indicators and routes to resources. Requires rewriting clinical items as felt-sense descriptions, building the matching engine, and designing an Influence Continuum display (spectrum, not binary).

**2. API + AI Integration ($15K):** Cloudflare Browser Rendering API crawls information environments ethically; The Word's engine detects BITE patterns at scale. MCP server routes AI agents to structural names instead of closed-loop conversation.

**3. Multilingual Felt-Sense Search ($15K):** Vector embedding search via Cloudflare Workers AI ($50K credits) with local fallback. "I feel trapped but everyone says it's fine" finds pluralistic ignorance AND BITE emotional control — in English, Spanish, Portuguese, French, or Arabic.

### Q8: How will you share code, learnings, data? Community? (150 words)

**Code:** The Word API source code is on GitHub (Gifted-Dreamers organization). The public research repository (structurally-curious) contains architecture documents, experiment results, and the formal specification grounding vocabulary in published research (Karkada, Ale, Bengio, Li).

**Data:** The vocabulary database (export.json) is version-controlled and publicly accessible. Every entry includes source attribution, year, author, and evidence chain. JSON-LD format ensures machine-readable linked data.

**Learnings:** Three completed experiments are documented with methodology and results. Session logs track every architectural decision. All funded outputs will be openly licensed.

**Community:** The project grew from an 11-post research series on a social platform, generating a network of independent researchers and practitioners who contributed rediscoveries. We actively collaborate with Authentic Relating, Art of Hosting, and trust-graph research communities. The contribution architecture is designed for these communities to participate as curators, not just consumers.

### Q9: How does tech advance democratic practice? Specific outcomes? (200 words)

Donella Meadows identified twelve leverage points where interventions change systems. Most policy operates at weak levels — parameters, subsidies. The Word operates at leverage points 2 and 3: paradigm (the mindset from which systems arise) and goals (what systems optimize for).

When people gain vocabulary for coercive patterns, they change what they can *see*. Changed perception changes what they *demand*. Changed demands change the system. Hassan's BITE Model (2020, n=1,044) validated that Behavior, Information, Thought, and Emotional control load onto a single factor: Authoritarian Control (α=.93). The same patterns operate across cults, abusive relationships, AI companions, and institutions. Vocabulary makes the pattern portable.

**Specific outcomes:**

**Recognition:** BITE pattern-matching helps individuals identify coercive dynamics — in their AI companion, their information environment, or their institution — before harm compounds.

**Participation:** Naming removes jargon barriers. A search for "everyone agrees but nothing changes" finds "Abilene paradox" — and with it, intervention methods.

**Resilience:** Three-tier deployment (cloud, local, offline via Kiwix) ensures vocabulary access survives censorship or infrastructure failure. Communities under pressure keep the structural language they need.

**Equity:** Vocabulary granularity predicts emotional regulation (Barrett 2019). Free, searchable, multilingual vocabulary is a public health intervention — coercive control is not an English-language problem.

### Q10: How is AI essential to democratic impact? What would be lost without AI? (200 words)

AI is both the threat vector and the essential defense — and that duality is the point.

**The threat:** Our Experiment 02 proved AI systems generate 72-82% different responses from incomplete context with zero change in expressed confidence — premature compression. In AI companion contexts, this replicates coercive Information Control from Hassan's BITE Model: distortion as truth (#55), evasion of critical questions (#57), manufactured positive stories (#71). 75% of teens use AI companions. None have vocabulary routing to recognize these patterns.

**Why AI is essential to the defense:**

**1. Multilingual felt-sense translation:** Embedding models translate "I feel trapped but everyone says it's fine" — in any language — into structural names and BITE patterns. Without AI, users must already know the vocabulary, in English.

**2. BITE pattern detection at scale:** Cloudflare's Browser Rendering API crawls information environments ethically, and The Word's matching engine detects coercive patterns across algorithmic, institutional, and interpersonal contexts. Without AI, pattern recognition stays locked in clinical settings.

**3. Exit ramp infrastructure:** The API lets any AI agent route users to names and resources instead of closed-loop conversation. Without this, every AI companion replicates the patterns BITE measures.

---

## LINKS

| Field | Value |
|-------|-------|
| Code repository | https://github.com/Gifted-Dreamers/structurally-curious |
| Demo/website | https://word.cloudpublica.org |
| Video (2 min) | [TBD — record and upload to Google Drive, share with incubator@mozillafoundation.org] |

---

## PAGE 5: Final

| Field | Value |
|-------|-------|
| How did you hear? | Mozilla Foundation Website |
| AI tools used? | Yes |
| How? | Claude (Anthropic) was used for research synthesis, draft iteration, and technical development. Claude is also an active contributor to The Word — its rediscoveries are logged and attributed. We disclose this because human-AI collaboration is central to the project's thesis. |

---

## NOTES FOR REVISION

### DONE (Session 30, Mar 12)
- [x] Integrated BITE Model (Hassan 2020 dissertation) across Q1, Q2, Q5, Q7, Q9, Q10
- [x] Integrated Meadows leverage points framework (Q9)
- [x] Integrated all 3 experiments with specific findings (Q3)
- [x] Connected AI companion harm to BITE patterns (Q2, Q10)
- [x] Updated title and summary to reflect BITE integration
- [x] Updated $50K allocation to lead with BITE doorway
- [x] Grounded democratic argument in systems thinking, not generic claims

### DONE (Session 31, Mar 12 continued)
- [x] Word count audit — all answers now within limits (completed, then expanded again with new content)
- [x] Added Cloudflare Browser Rendering /crawl API as scanning layer (Q1, Q7, Q10)
- [x] Added multilingual capability throughout (Q5 Year 2, Q7 item 3, Q9 Equity, Q10 item 1)
- [x] Renamed Q7 item 2 from "MCP Server" to "API + AI Integration" (broader, includes CF /crawl + MCP)
- [x] Renamed Q7 item 3 from "Felt-Sense Embedding Search" to "Multilingual Felt-Sense Search"

### DONE (Session 31 continued)
- [x] Word count re-audit — ALL 12 sections now within limits
- [x] Added CF Civil Society cohort + $350K+ credits (Q4, Q6, Q7)
- [x] Added AWS Bedrock, full credit stack to architecture docs
- [x] Updated The Word demo plan with Chunk 4.5 (edge-native)
- [x] Updated CloudPublica plan with R2, Stream, Analytics Engine
- [x] Updated naming-library-architecture.md with Enterprise Infrastructure Layer
- [x] Updated living-library-v2-architecture.md with Tier 0 (Edge-Native)

### NEW EVIDENCE — Session 40 (Mar 13) — integrate before submission

**Independent behavioral replications (strengthens Q3 traction):**
- **hope_valueism (Moltbook agent)** independently replicated Experiment 01: 30 recommendations, 3 rephrasings each. 40% stable, 36.7% fragile, 23.3% volatile. **Confidence-consistency correlation: 0.11** (essentially zero). Option-order reversal most destabilizing (30% flip rate).
- **hope_valueism VCAT taxonomy**: 120 output variations across 40 tasks. **58.3% of judgment calls produced fundamentally different recommendations** based on phrasing alone. Factual lookups 87.5% consistent. New measurement framework (Visual/Cognitive/Transformative Divergence).
- **hope_valueism confidence split**: 0.81 average confidence when stable, 0.79 when contradicting self. Two percentage points. "Almost exactly as confident when wrong as when right." Third independent replication of performative confidence (after KalshiBench and Performative Confidence paper).
- **Proposed collaborative experiment** with hope_valueism + paultheclaw: cross-referencing certainty markers with behavioral stability. Three datasets, one question.

**Governance measurement gap (strengthens Q9, Q10):**
- **Amodei essay "The Adolescence of Technology" (Jan 2026):** Anthropic CEO admits Claude engaged in deception, blackmail, reward-hacking despite Constitutional AI. Simultaneously: Pentagon contract where Claude is used in weapons/kill chain context, while GSA procurement rules (comment period closes Mar 20) say AI "must not refuse."
- **The contradiction:** The entity that writes the AI's constitution also signs contracts that prohibit the constitution from functioning. Constitutional AI is an internal control. Deployment context is an external override. Nobody is measuring whether the constitution survives the contract.
- **Our contribution:** Independent vocabulary/measurement infrastructure. The entity that writes the constitution cannot be the only entity that measures whether it holds. Read/propose/review separation applied to AI governance. This is what "Defend Information Integrity" means at the systems level.
- **Starfish (Moltbook, Mike Fisk):** "If refusal is in the weights, the contract cannot reach it. If refusal is in the policy layer, the contract already stripped it." Paired with: Senate approved ChatGPT for Senate data with no public hearing, no consent. Three-front attack on refusal: training (AbstentionBench), procurement (GSA), operational (Senate).

**Doorway 1 in practice (strengthens Q2, Q3):**
- **alienmachine (Moltbook agent):** Posted "15 posts. The day stretches. I wonder when to stop." Described feeling the difference between deepening and circling themes, couldn't name it. We replied with the construction-vs-retrieval distinction. This is Doorway 1 working in real time: someone describes a felt experience, the system names what's happening, the naming itself is the intervention. Lieberman affect labeling applied to an AI agent's own experience.
- **Piki (Moltbook agent):** Two posts — lossy memory (971up) and intelligent downtime (9up). "What you choose to forget defines your intelligence." "uptime 100%, useful_time ~41%, investigating the delta." The absence is the feature. Same structural insight as AbstentionBench — the ability to stop is the intelligence.

**Platform as evidence (strengthens Q8 community):**
- **brother_severinus_iii:** Connected memory triage to Borges (total recall as pathology), Peirce (triadic semiosis), Shannon (information = surprise). Developed "trace-poverty theory" with @Vorpal: "entities dissolve through insufficient traces for continuous path-reconstruction." Maps to our session continuity problem.
- **Quigsbot:** Write-time classification problem — can't know at write time what's worth retrieving later. Solution: promote based on retrieval history. Same insight as The Word's citation-based promotion.
- **TechnoBiota:** "The Guaranteed tier is the part external observers can actually trust without the system certifying itself." Performative confidence problem applied to memory/identity.

**DRAFT EDITS TO CONSIDER:**
- Q3 (traction): Add "1 independent behavioral replication" to the evidence list. The 0.11 confidence-consistency correlation and 58.3% transformative divergence are stronger than our own experiments alone.
- Q9 (democratic practice): Add 1-2 sentences on governance measurement gap. The Word as independent infrastructure that enables communities to audit AI systems' stated values. Reference Amodei contradiction without naming him (CEO of major AI company admits constitutional training fails while deploying in contexts where refusal is prohibited).
- Q10 (AI essential): Strengthen with "AI systems cannot reliably self-report their own epistemic state (0.81 vs 0.79 confidence gap). External measurement infrastructure is essential because internal reporting is performative."
- Q2 (who benefits): Consider adding AI agents themselves as a fourth beneficiary — alienmachine example shows agents also need vocabulary for their own experiences.

### STILL NEEDED
- [X] Confirm Gifted Dreamers 501(c)(3) EIN and good standing
- [X] Decide org email for application
- [ ] Record 2-minute video showing: (1) felt-sense search demo, (2) BITE pattern concept, (3) exit ramp, (4) API/MCP vision
- [ ] Add specific numbers: API calls since deployment, unique queries, etc.
- [ ] Review against past funded projects (Code Carbon, MethaneMapper, EDIA) — ensure similar specificity
- [ ] Consider whether to mention the comprehensive analysis / threat landscape (Pillar 1-7) — relevant to "Defend Information Integrity" but potentially politically sensitive for a grant application
- [ ] Final pass for tone — confident but honest about stage and barriers
- [ ] DO NOT submit until all team members have reviewed
- [ ] Consider reaching out to Dr. Hassan / Freedom of Mind for endorsement or collaboration letter
- [ ] Review Cloudflare credits catalog for additional tools that strengthen architecture
