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
| Email | [TBD — use org email] |
| Country | United States |
| Organization | Gifted Dreamers |
| Type | Nonprofit Organization/NGO |
| Relationship with Mozilla | No prior relationship |

---

## PAGE 2: Project Overview

**Proposed Project Title** (25 words max):
> The Word: Open Vocabulary Infrastructure That Breaks AI Closed Loops Through Naming, Citation, and Democratic Knowledge Sharing

**Project Summary** (25 words max):
> A searchable vocabulary API where describing what you feel finds the research-backed name for it — breaking AI companion dependency through exit ramps.

**Project Category:** Defend Information Integrity

**Project Stage:** Deployed with early users

---

## PAGE 3: Project Details and Team

### Q1: What technology are you building? How does it address this cohort's theme? (150 words)

The Word is a public vocabulary API that translates felt experience into precise, research-backed language. Users describe what they're going through in plain language; full-text search returns the established name, its research lineage, and outward links to communities, papers, and practitioners.

The technology stack: Express.js REST API serving JSON-LD linked data from SQLite with FTS5 search. Currently 96 curated entries across four types — Names (concepts with felt-sense descriptions), Sources (academic origins), Rediscoveries (independent convergence as validation), and Bridges (connections between concepts). Deployed at word.cloudpublica.org.

This addresses information integrity directly: AI companions like Character.AI and Replika create closed conversational loops with no exit ramps — users become dependent on systems that reinforce rather than resolve. The Word provides the missing citation infrastructure. Every entry routes outward to research, communities, and professional resources. The architecture treats vocabulary access as democratic infrastructure, not content.

### Q2: Who benefits? How are you connecting with them? What community challenge? (150 words)

Three communities benefit immediately:

**People in emotional difficulty** who can't find help because they can't name what's happening. Barrett's research (2019) shows emotion vocabulary granularity directly predicts regulation capacity. Someone searching "I feel nothing and I don't know why" finds "alexithymia" — and with that name, a research tradition, communities, and treatment paths that were invisible seconds before.

**AI agent developers** building responsible conversational tools. The Word's MCP server lets agents route users to precise vocabulary and external resources instead of generating more closed-loop conversation. This is structural — the exit ramp is in the API, not the agent's personality.

**Organizers and educators** working with communities where structural knowledge is siloed behind academic paywalls and disciplinary jargon.

We connect through social technology communities (Authentic Relating, Art of Hosting), open-source channels, and a research network that independently validated 13 of our entries through convergent rediscovery.

### Q3: Describe traction. What's working? What evidence? (150 words)

The Word is live at word.cloudpublica.org with 96 curated entries, 7 API endpoints, and full-text search. It is not a prototype.

Evidence that vocabulary infrastructure solves a real problem:

**Neuroscience:** Lieberman (2007) demonstrated via fMRI that affect labeling — putting feelings into words — activates prefrontal cortex and dampens amygdala reactivity. Naming is the therapeutic mechanism itself.

**Convergence validation:** 13 of our entries were independently rediscovered by researchers, practitioners, and AI agents working without knowledge of each other. When 50 people independently reinvent the same concept, that is empirical ground truth — not editorial opinion.

**Three completed experiments** testing phrasing sensitivity in search, premature compression in AI responses, and geometric correlation between vocabulary entries.

**Real harm data driving urgency:** Character.AI teen suicides, Replika fines, Woebot FDA shutdown. All share the same architectural failure — closed loops with no citation infrastructure routing users outward.

### Q4: Who is building this? Relevant experience? (150 words)

**Kristine Socall** (project lead) — CFO of Gifted Dreamers 501(c)(3), board member of Unrig (voting infrastructure nonprofit). Background in financial systems, organizational design, and community technology. Has built and deployed the full stack: Docker infrastructure, API design, Cloudflare Enterprise security, Anytype knowledge management, n8n workflow automation.

**Technical infrastructure:** Self-hosted on AWS with Cloudflare Enterprise protection, GitLab CI/CD, Datadog monitoring, and Splunk SIEM — all through nonprofit technology credits. The stack is production-grade, not hobbyist.

**Research network:** Collaborations with social technology practitioners (Sara Ness, Authentic Relating communities), trust-graph researchers (Jordan Myska Allen, UpTrust), and engineers working on isomorphic methods in engineering systems design.

**AI collaboration:** Claude (Anthropic) is an active development partner — not just a tool, but a contributor to the vocabulary itself, with rediscoveries logged and attributed. This models the human-AI collaboration the project enables.

---

## PAGE 4: Impact, Openness, and Theme Fit

### Q5: Success in 2-3 years? How will you measure? (150 words)

**Year 1:** 500+ vocabulary entries, MCP server enabling 10+ AI applications to route users to precise names instead of closed-loop conversation. Measurable: API call volume, unique search terms, rediscovery rate (independent convergence as validation signal).

**Year 2:** ActivityPub federation (Layer 2) — The Word becomes a protocol, not just a database. Vocabulary flows between platforms without centralization. Measurable: federated instances, cross-platform citation chains.

**Year 3:** Community-curated vocabulary infrastructure used by mental health apps, educational platforms, and organizing tools as standard citation layer. Measurable: integration count, vocabulary-attributed outcomes in partner applications.

**Success metrics:**
- Search-to-name conversion rate (did the user find what they couldn't name?)
- Exit ramp utilization (did the Name lead to an external resource, community, or practitioner?)
- Rediscovery rate (are independent sources converging on the same concepts?)
- Felt-sense coverage (what queries return no results? — these are invention signals)

### Q6: Sustainability long-term? Biggest barriers? (150 words)

**Revenue model:** Gifted Dreamers (501c3) provides the mission; Paradigm LLC provides revenue through enterprise vocabulary consulting and API licensing for commercial applications. Google Ad Grants ($10K/month) fund awareness. Infrastructure runs on nonprofit technology credits: $250K Cloudflare, $100K Datadog, GitLab Ultimate, Splunk Enterprise — all activated.

**Community sustainability:** The Word's 360-degree contribution architecture means using IS contributing. Every search enriches felt-sense data for the next person. No extra labor required from users.

**Biggest barriers:**
1. **Poisoning protection** — open contribution without quality degradation. Need governance layer before full open-source release.
2. **Cold start** — vocabulary infrastructure is only valuable at density. Currently 96 entries; need 500+ for reliable felt-sense coverage.
3. **Trust establishment** — academic and practitioner communities need to see editorial integrity before citing The Word as infrastructure.

### Q7: What would $50,000 unlock? (150 words)

$50,000 unlocks three things we cannot do alone:

**1. MCP Server + AI Integration ($15K):** Build the Model Context Protocol server that lets any AI agent — Claude, GPT, Gemini, open-source models — query The Word natively. This transforms vocabulary from a website into infrastructure that AI applications consume directly. Without this, every AI app reinvents closed-loop conversation.

**2. Contribution Governance ($15K):** Design and implement the poisoning-protection layer required for open-source release. Currently, The Word cannot accept public contributions safely. This blocks community growth and violates our own open-source commitment.

**3. Felt-Sense Embedding Search ($20K):** Upgrade from keyword matching to vector embedding search (local Ollama + nomic-embed, no data leaves the server). A user describing "that feeling when everyone seems fine but you know something is wrong" should find "pluralistic ignorance" — this requires semantic, not lexical, matching.

### Q8: How will you share code, learnings, data? Community? (150 words)

**Code:** The Word API source code is on GitHub (Gifted-Dreamers organization). The public research repository (structurally-curious) contains architecture documents, experiment results, and the formal specification grounding vocabulary in published research (Karkada, Ale, Bengio, Li).

**Data:** The vocabulary database (export.json) is version-controlled and publicly accessible. Every entry includes source attribution, year, author, and evidence chain. JSON-LD format ensures machine-readable linked data.

**Learnings:** Three completed experiments are documented with methodology and results. Session logs track every architectural decision. All funded outputs will be openly licensed.

**Community:** The project grew from an 11-post research series on a social platform, generating a network of independent researchers and practitioners who contributed rediscoveries. We actively collaborate with Authentic Relating, Art of Hosting, and trust-graph research communities. The contribution architecture is designed for these communities to participate as curators, not just consumers.

### Q9: How does tech advance democratic practice? Specific outcomes? (200 words)

Vocabulary access is democratic infrastructure. When people cannot name what is happening to them — structurally, emotionally, politically — they cannot organize around it, advocate for change, or seek help. The Word addresses this directly.

**Specific democratic outcomes:**

**Participation:** Felt-sense search removes the jargon barrier. A community organizer searching "why do people agree in meetings but nothing changes" finds "Abilene paradox" — and with that name, a 50-year research tradition and intervention methods. Naming creates agency; agency enables participation.

**Transparency:** Every vocabulary entry is traceable to its source — author, year, publication, evidence chain. No black-box curation. The JSON-LD format makes the entire knowledge graph machine-auditable.

**Accountability:** Rediscovery tracking provides empirical validation. When 13 independent sources converge on the same concept without coordination, that is ground truth — not editorial authority. This is vocabulary governance through convergence, not committee.

**Civic space protection:** Three-tier deployment (cloud, local network, fully offline via Kiwix) ensures vocabulary access survives network censorship, authoritarian shutdown, or infrastructure failure. Communities under pressure maintain access to the structural language they need to organize.

**Equity:** Barrett's research shows vocabulary granularity predicts emotional regulation. Vocabulary poverty reproduces class inequality. Making structural vocabulary free, searchable, and available in plain language is a public health intervention with democratic consequences.

### Q10: How is AI essential to democratic impact? What would be lost without AI? (200 words)

AI is essential at three levels — none of which involve building a chatbot:

**1. Felt-sense translation (search):** Humans describe experiences in unstructured natural language. AI embedding models (local Ollama + nomic-embed, no data leaves the server) translate "I keep helping people even when it hurts me" into the precise vocabulary entry "pathological altruism." Without AI, this requires the user to already know the jargon — which is the problem we're solving.

**2. Rediscovery detection (validation):** AI agents scanning RSS feeds, research papers, and community discussions detect when independent sources converge on the same concept. This pipeline (Miniflux + n8n + scoring) automates what would take a team of researchers months: identifying empirical ground truth through convergent observation. Without AI, rediscovery goes undetected and the vocabulary lacks its strongest validation signal.

**3. Exit ramp infrastructure (MCP server):** The Model Context Protocol server lets AI agents query The Word natively — so instead of generating more closed-loop conversation, an agent can route a user to the precise name, research lineage, and community for what they're experiencing. Without this, every AI companion remains a closed system. The exit ramp must exist where the conversation happens: inside the agent itself.

This is not AI as product. It is AI as democratic plumbing.

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

- [ ] Confirm Gifted Dreamers 501(c)(3) EIN and good standing
- [ ] Decide org email for application
- [ ] Record 2-minute video showing: (1) felt-sense search demo, (2) JSON-LD response, (3) exit ramp concept, (4) MCP server vision
- [ ] Review word counts — all answers must be under limit
- [ ] Consider adding Moltbook community context (pre-Meta acquisition traction)
- [ ] Integrate OSINT tools angle if relevant to information integrity category
- [ ] Add specific numbers: API calls since deployment, unique queries, etc.
- [ ] Review against past funded projects (Code Carbon, MethaneMapper, EDIA) — ensure similar specificity
- [ ] Final pass for tone — confident but honest about stage and barriers
- [ ] DO NOT submit until all team members have reviewed
