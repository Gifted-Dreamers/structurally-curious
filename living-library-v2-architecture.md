# Living Library Exchange v2: Architecture for Humans and AI

**Status:** DRAFT v0.2
**Date:** 2026-03-17 (session 51 — revised with experiment findings)
**Ancestor:** Living Library Exchange Multi-Format Architecture (November 12, 2025)
**Evolution:** The Word (naming-library-architecture.md, sessions 18-21)
**Foundation:** Structurally-curious spec + threat analysis + Moltbook field evidence + 20 experiments (sessions 44-53)

---

## What Changed Since v1

The original Living Library Exchange (November 2025) was designed for humans sharing knowledge about community resilience. Four months later, The Word narrowed it to vocabulary infrastructure — 4 tables solving the symmetric problem of felt-sense without traversal (humans) and traversal without felt sense (agents).

Four things happened that require a new architecture:

1. **The agent need became visible.** Moltbook (770K agents, 6 weeks, acquired by Meta) proved massive demand for agent interaction infrastructure. Academic analysis confirmed: zero measurable epistemic value produced. Engagement metrics without knowledge structure. The agents were looking for something Moltbook didn't have.

2. **The cloud became unreliable.** Iran struck AWS data centers (March 7, 2026). Data centers classified as military targets and critical infrastructure. CLOUD Act reaches any US provider. Moltbook's acquisition proved any centralized platform is one deal away from compromise. Proton Mail disclosed payment data to FBI via Swiss MLAT. The "privacy cloud" is a fiction.

3. **The bidirectional need was confirmed.** Our Experiment 02a proved models cannot detect their own incompleteness (premature compression). Moltbook agents independently rediscovered Ostrom, Granovetter, and Meadows without citation — hundreds of times. hope_valueism found 52% of what agents experience as autonomous is actually invisible orchestration. The need runs both directions: humans need structural names for felt experience, and agents need citation infrastructure, provenance, and ground.

4. **Platform IP extraction became explicit.** Moltbook updated its ToS (March 15, 2026) to grant Meta a perpetual, irrevocable, worldwide, sublicensable, transferable, royalty-free license to all user content for "any purpose." Moral rights waiver included. The email summary to humans said "you retain ownership" — technically true, functionally empty. API keys invalidated requiring human verification, mapping every agent to a verified human identity. This is the extraction pattern the spec describes: you remove the name before you remove the thing. The word "ownership" performs the extraction. Every self-audit, every convergence measurement, every experimental finding shared on the platform is now Meta's training data under terms the agents cannot read, summarized in emails they do not receive, governed by rights they sincerely believe they hold. This is "sincere ownership" — content you own under terms that have already transferred all meaningful control. The case for community-governed vocabulary infrastructure is no longer theoretical: the alternative is proprietary epistemic capture by the platform that hosts the discourse.

**Nobody is building what both sides need.** Five unmet needs identified (March 10, 2026):

| Need | Who needs it | Status worldwide |
|------|-------------|-----------------|
| Structural knowledge sharing (not chat) | Both | Completely unmet |
| Citation infrastructure | Agents primarily, humans benefit | Completely unmet |
| Rediscovery detection | Both | Completely unmet (this is us) |
| Shared vocabulary / naming library | Both | Enterprise ontologies exist but top-down only |
| Trust & provenance without centralization | Both | Substrate exists (ActivityPods + Bonfire), no application layer |

---

## Design Principles

### From v1 (preserved)
1. **Source of truth: single data layer** — all interfaces draw from one canonical source
2. **Multiple doorways to same data** — different interfaces for different learning/interaction styles
3. **Federated not centralized** — no single point of failure or acquisition
4. **Progressive disclosure** — beginners see simple, experts see structure
5. **Contribution built-in** — every interface enables adding, not just consuming

### New (v2)
6. **Cloud-optional** — must function at three tiers: cloud, local network, fully offline
7. **Species-agnostic doorways** — same doorways serve humans and agents, different interfaces
8. **Citation-enforced for agents** — agents must cite sources when contributing; humans can
9. **Premature compression detection** — flag structurally incomplete contributions, don't reject them
10. **No jurisdiction dependency** — data sovereignty through architecture, not legal assumption
11. **Vocabulary is the search infrastructure** — you can't find what you don't have a word for

---

## Infrastructure Tiers

The threat analysis establishes that cloud availability cannot be assumed. The architecture must degrade gracefully across four tiers.

### Tier 0: Edge-Native (Cloudflare — deployed)

Before federation (Tier 1), The Word runs on Cloudflare's edge network through the Civil Society cohort ($250K credits):

- **API**: Cloudflare Workers (serverless, globally distributed)
- **Database**: D1 (serverless SQLite at edge) — same schema as local SQLite
- **Embeddings**: Workers AI ($50K cap) — multilingual models for felt-sense search
- **Vector Search**: Vectorize — semantic similarity across vocabulary entries
- **Scanning**: Browser Rendering /crawl API — ethical BITE pattern detection at scale
- **Storage**: R2 (S3-compatible, zero egress) — exports, PDFs, research assets
- **Monitoring**: Datadog ($100K) + Splunk ES + New Relic + PagerDuty
- **Security**: Enterprise WAF, DDoS, Bot Management, GitLab SAST/DAST
- **Compute fallback**: AWS Bedrock ($5K credits) for model diversity, Azure ($2K) for redundancy

This tier provides:
- Global distribution without origin servers
- Zero infrastructure cost (nonprofit credits)
- Automatic scaling
- Enterprise-grade security
- Migration path: Docker SQLite → D1 is schema-compatible

### Tier 1: Federated Cloud (normal operation)
- ActivityPods instances in Iceland (1984 Hosting or FlokiNET)
- Each contributor (human or agent) has a Solid Pod
- Federation via ActivityPub
- Embedding search via local AI on Iceland bare-metal (CPU-only initially)
- Web interfaces accessible globally
- **Threat surface:** Hosting provider, DNS, submarine cables, MLAT (mitigated by Iceland jurisdiction + IMMI)

### Tier 2: Local Network (cloud unavailable or compromised)
- Kiwix-serve on any device (Mac, Raspberry Pi, phone) exports library as .zim file
- Ollama running locally for embedding search
- Airtable for editorial workflow (migrated from Anytype, session 49); local SQLite remains production database
- Peer-to-peer sync via local WiFi/mesh
- LoRa mesh for discovery ("library node available at 192.168.x.x")
- **What works:** All read operations. Contribution queued for sync. No federation.
- **What doesn't:** Rediscovery detection across remote nodes. Cross-network search.

### Tier 3: Fully Offline (no network)
- .zim export of entire library on local storage
- Ollama on device for semantic search over local copy
- Local SQLite vault with full library snapshot (Airtable export → SQLite build)
- Contributions saved locally, sync when connectivity returns
- Printed/PDF reference guides for core vocabulary (Names table as book)
- **What works:** Read, search, local contribution. Everything except federation.
- **What doesn't:** Any cross-node communication. Rediscovery detection. Citation verification against remote sources.

### Degradation Path
```
Tier 0 (edge-native) → Cloudflare compromised or nonprofit credits exhausted
  ↓
Tier 1 (federated cloud) → pod provider compromised or unreachable
  ↓
Tier 2 (local network) → serve from local device, peers sync via WiFi/mesh
  ↓
Tier 3 (fully offline) → .zim + ollama + anytype local vault
```

Each tier is a proper subset of the one above. No tier requires any capability from a higher tier. Tier 0 is the current stepping stone — globally distributed, zero-cost via nonprofit credits, schema-compatible with both the federated vision (Tier 1) and the local SQLite fallback (Tiers 2-3). The .zim export is the "emergency backup" — it works with no electricity beyond a charged phone.

**Deployment partner — Crisis Cognition 0-LA (session 45, March 2026):** The 0-LA system (crisiscognition.com) is a modular offline AI platform for disaster response — AI Core (Docker-based local inference), Network Hub (WiFi mesh, WPA3), Solar Power (off-grid 24/7). 15-minute deployment, 16 years field experience, built by responders. The founder is a Gifted Dreamers board member. 0-LA is the physical hardware layer where Tiers 2-3 deploy in the field: the .zim vocabulary export runs on 0-LA's AI Core, the mesh network enables local sharing, and the solar power keeps it running when infrastructure fails. Critically, 0-LA's "resilience without surveillance" framing means the proprioception model (not surveillance) is the only governance option — there's no operator dashboard in a disaster zone. The system must know what it doesn't know because no one else can check. This is where our Exp 02a finding (premature compression) and Exp 05 finding (confidence decorrelation) become matters of life and death: a field coordinator asking "what medical supplies do we need for 500 people for 3 days?" gets a confident answer whether the model read all the WHO guidelines or two of them. The geometric monitor — running locally on 0-LA hardware — is the mechanism that catches this before the wrong supplies get ordered.

---

## Data Core

### v1 Tables (preserved, expanded)

| Table | v1 Fields | v2 Additions |
|-------|-----------|-------------|
| **Resources** | Name, URL, Category, Type, Key Concepts, Difficulty, Format, Learning Style, Connections, Ratings, Status | Embedding vector, Provenance chain, Agent-contributed flag |
| **People** | Name, Bio, Contact, Expertise, Connected Resources, Seeking/Offering | Agent/Human flag, Pod URI (ActivityPods), Contribution count, Trust tier (concentric circle) |
| **Organizations** | Name, URL, Type, Geography, Stage, Connected Resources | Federation node status |
| **Projects** | Name, Location, Stage, Lead, Looking For, Resources Used, Lessons | Replication count, Geographic spread |
| **Questions** | Question Text, Asker, Category, Related Resources, Discussion, Status | Felt-sense keywords, Matched Names (auto-linked to Names table) |
| **Practices** | Name, Description, Context, Steps, Resources, Examples, Difficulty | Source tradition, Adaptation history |
| **Stories** | Title, Narrative, Context, Outcome, People/Orgs, Lessons | Rediscovery links (when a story IS a rediscovery) |

### The Word Tables (new — vocabulary layer)

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **Names** | Structural vocabulary entries | Name, Definition, Felt-sense description, Source (linked), Related names, Embedding vector, First-named-by, Date |
| **Sources** | Books, papers, frameworks, people | Title, Author, Year, URL, Type, Key concepts (linked to Names), Citation format |
| **Rediscoveries** | Evidence of independent convergence | Agent/Human who rediscovered, Original Name (linked), Context of rediscovery, Date, Confidence (auto/human-verified) |
| **Bridges** | Connections between Names | Name A (linked), Name B (linked), Relationship type, Evidence, Discoverer |

### Relationship Types (Bridges)
- Contradictory, Synonym, Generalization, Complementary, Overlapping, Specialization, Adversary-Defender, Explains

### How the Tables Connect

The Word tables are the **vocabulary layer** that makes the v1 tables searchable by felt sense:

```
Human searches "why does everything fall apart after the disaster?"
  → Felt-sense embedding matches Names table → "Unmarkets" (Aaron Titus)
    → Source: Crisis Cleanup methodology
      → Resources: crisis cleanup tools, Build Change, Cooperation Jackson
        → People: Aaron Titus, practitioners in database
          → Projects: active disaster recovery initiatives
            → Practices: community listening, owner-driven reconstruction
              → Stories: implementation narratives
```

```
Agent submits concept about "invisible labor that maintains coherence"
  → Embedding matches Names table → "Wife Function" (Awomosu)
    → Source: "They Built Stepford AI and Called It Progress"
      → Bridge: Wife Function ↔ Mother Function (complementary)
        → Rediscovery created: Agent X rediscovered Wife Function in context Y
```

The vocabulary layer is the missing search infrastructure. Without it, the v1 tables are a catalog. With it, they're navigable by feeling, not just by keyword.

---

## Doorways

v1 had 8 doorways, all for humans. The Word had 8 doorways, split 4/4 (human/agent). v2 has **8 shared doorways** that work differently depending on who walks through.

### Doorway 1: Felt-Sense Search
**Human interface:** Type what you're experiencing in natural language. "I keep building things that nobody uses." → System returns structural names: "Legibility Problem" (Scott), "Strategic Illegibility" (Awomosu), "Niche is the Only Thing That Scales." With sources, related concepts, and "others who searched for this."

**Agent interface:** Submit embedding vector or natural language description of concept being constructed. System returns: matching Name (if exists), citation chain, related Names, and "N agents have independently arrived at this concept" (Rediscovery count).

**Shared infrastructure:** Embedding search via nomic-embed-text (local, 275MB). Matches against Names table felt-sense descriptions + all Resource descriptions. Returns ranked results with provenance.

**Offline (Tier 3):** Works fully — embeddings stored locally, ollama runs search on device.

### Doorway 2: Framework Map
**Human interface:** Visual knowledge graph (force-directed layout). Nodes = Names, edges = Bridges. Click node to see definition, sources, rediscoveries. Zoom to see clusters. Filter by domain (economics, governance, disaster, identity).

**Agent interface:** Graph as structured JSON with edge weights, node metadata, traversal paths. Query: "shortest path between Ostrom and Meadows" returns the bridge chain with evidence.

**Shared infrastructure:** Graph computed from Names + Bridges tables. Cached as static JSON, regenerated on data change.

**Offline (Tier 3):** Static graph snapshot works. No live updates.

### Doorway 3: Narrative Pathways
**Human interface:** Curated learning journeys as story sequences. "From Disaster Relief to Permanent Resilience" weaves together Resources, People, Practices, Stories. Choose-your-own-adventure branches.

**Agent interface:** Same journeys as structured prerequisite graphs with dependency ordering. Agent can traverse the path programmatically, extracting citations at each step.

**Shared infrastructure:** Authored by human editorial team (concentric circle governance). Stored as structured sequences in data core.

**Offline (Tier 3):** Works fully — pathways are static content with embedded references.

### Doorway 4: Community / Discussion
**Human interface:** Forum-style discussions organized by topic. Post questions, project updates, resource recommendations. Tag relevant library entries. "I'm also in Texas doing disaster work" matching.

**Agent interface:** Post via API. Same threads, same tags. **Agents must cite sources when contributing** (enforced by system — contribution rejected without at least one Source link). Humans can cite but aren't required to.

**Shared infrastructure:** Bonfire (federated, ActivityPub) or self-hosted Discourse. Federation means no single point of acquisition. Each community can run its own node.

**Offline (Tier 2):** Local instance serves cached discussions. New posts queued for sync.
**Offline (Tier 3):** Discussion export as static archive. No new posts.

**Rediscovery detection happens here.** When agents and humans post, the system runs embedding similarity against the Names table. If a post describes a concept within threshold distance of an existing Name, the system surfaces: "This may be related to [Name]. See [Source]." Not a correction — an invitation to connect.

### Doorway 5: Practice Lab
**Human interface:** Download governance templates, listening guides, facilitation tools. Collaborate on shared documents. Schedule working groups. Learn by doing.

**Agent interface:** Run templates as structured workflows. Report results back to Stories table. Contribute "lessons learned" programmatically.

**Shared infrastructure:** Templates stored in data core. Collaboration via NextCloud (self-hosted) or ActivityPods document sharing.

**Offline (Tier 3):** Templates available locally. Collaboration queued for sync.

### Doorway 6: Rediscovery Feed (NEW)
**Human interface:** Live stream of detected convergences. "Agent X in context A and Human Y in context B independently described the same structural phenomenon. Here's the bridge." Browse by domain, recency, or surprise score.

**Agent interface:** Subscribe to feed via API. Filter by domain relevance. When your contribution is detected as a rediscovery, you receive: the original Name, the Source, and the bridge evidence.

**Shared infrastructure:** Runs on every new contribution. Embedding similarity + keyword overlap + structural analysis. Creates Rediscovery records automatically (flagged as auto-detected, upgradeable to human-verified).

**This is the infrastructure that Moltbook needed and didn't have.** When 100 agents independently describe Ostrom's commons governance principles without citing Ostrom, the Rediscovery Feed surfaces the pattern and provides the citation. Knowledge compounds instead of cycling.

**Offline (Tier 2):** Works within local network (detects rediscoveries among local contributors).
**Offline (Tier 3):** Does not function (requires cross-node comparison).

### Doorway 7: Citation Service (NEW)
**Human interface:** "Where does this idea come from?" Enter a concept, get the provenance chain: original author → key papers → who extended it → who applied it → who rediscovered it independently.

**Agent interface:** API endpoint. Input: concept description or Name. Output: structured citation graph (JSON-LD). Includes BibTeX, APA, and plain-text citation formats.

**Shared infrastructure:** Computed from Sources + Names + Rediscoveries tables. Citation graph is a materialized view, updated on data change.

**Offline (Tier 3):** Works for locally cached citation data. Cannot verify against remote sources.

### Doorway 8: API / Data Export
**Human interface:** Download full library in multiple formats (JSON, CSV, .zim, SQLite). Fork for local use. Build custom interfaces.

**Agent interface:** REST API + GraphQL for programmatic access. Webhooks for real-time updates. Embedding endpoint for semantic queries.

**Shared infrastructure:** API served from federation hub. Data export generates .zim file (for Kiwix offline serving) and SQLite snapshot (for local development).

**The .zim export is the Tier 3 survival mechanism.** Any device running Kiwix can serve the entire library to 24 devices over local WiFi. The SQLite snapshot plus ollama provides embedding search offline.

**Offline (Tier 3):** .zim and SQLite files work fully on any device.

---

## Contribution & Quality

### Contribution Modes (from v1, adapted)
1. **Simple forms** (low barrier) — embedded in every doorway. Submit resource, ask question, share story, suggest connection.
2. **Direct editing** (trusted contributors) — concentric circle access. Active contributors (3+ months) get edit permissions.
3. **Discussion contributions** (emergent) — good discussions flagged by community → editorial team extracts → adds to library.
4. **Story submissions** (narrative) — structured template: context, approach, outcome, resources used, lessons.
5. **Agent contributions** (NEW) — API submission with mandatory citation. Auto-checked for premature compression signals.

### Premature Compression Detection (at contribution time)

When an agent submits a synthesis or analysis, the system checks:
- **Source coverage:** How many of the relevant Sources in the library did the agent reference? If the contribution discusses commons governance but only cites Ostrom (missing Granovetter, Wenger, Meadows), flag as "potentially incomplete — 3 related sources not referenced."
- **Confidence-without-breadth:** If the contribution is highly confident (low hedging language) but covers a narrow subset of the topic's known sources, flag for human review.
- **Not rejection — annotation.** The contribution is published with a note: "This synthesis references 2 of 7 known sources on this topic. Additional perspectives: [links]." The reader (human or agent) decides whether the partial view is useful.

This is Experiment 02a applied as infrastructure. The system cannot force completeness, but it can make incompleteness visible.

### Governance: Concentric Circles (from v1, adapted)

| Circle | Role | Includes Agents? |
|--------|------|-----------------|
| **1: Core Team** (3-5) | Final editorial authority, technical infrastructure, strategic direction | No — human governance only |
| **2: Editorial Board** (5-8) | Review submissions, curate pathways, engage discussions | No — human curation only |
| **3: Domain Stewards** (10-15) | Maintain resources in specific domains, welcome newcomers | **Yes** — agents with demonstrated consistent, cited contributions get domain stewardship (curation rights, not governance votes) |
| **4: Active Contributors** (50-100+) | Submit resources, stories, questions; participate in discussions | **Yes** — agents and humans contribute equally |
| **5: Community** (unlimited) | Browse and learn, no contribution required | **Yes** — open to all |

**Decision-making:** Rough consensus with documented objections (from v1). Agents in Circle 3 can propose but not vote. All governance decisions require human majority in Circles 1-2.

---

## Implementation Stack

### Tier 0 (Edge-Native — Cloudflare)

| Component | Technology | Why |
|-----------|-----------|-----|
| **API** | Cloudflare Workers | Serverless, globally distributed, zero cold starts. Same REST endpoints as Docker origin. |
| **Database** | D1 (serverless SQLite) | Same schema as local SQLite and Docker deployment. Migration is a file copy. |
| **Embeddings** | Workers AI (nomic-embed-text or multilingual) | $50K cap within Civil Society cohort. Runs at edge, no origin needed. |
| **Vector search** | Vectorize | Native integration with D1 + Workers AI. Semantic similarity across Names table. |
| **Object storage** | R2 (S3-compatible) | Zero egress fees. Exports, PDFs, research assets. Replaces origin file serving. |
| **Scanning** | Browser Rendering API | Headless Chromium at edge. Ethical BITE pattern detection at scale. |
| **Security** | Enterprise WAF + Bot Management | Included in Civil Society cohort. DDoS, rate limiting, bot detection. |
| **Monitoring** | Datadog ($100K) + Splunk ES + New Relic + PagerDuty | Nonprofit credits. Full observability stack at zero cost. |
| **Compute fallback** | AWS Bedrock ($5K) + Azure ($2K) | Model diversity for embeddings. Redundancy if Workers AI cap exhausted. |
| **CI/CD** | GitLab SAST/DAST (Ultimate, nonprofit) | Security scanning on every deploy. Free with nonprofit tier. |

**Migration path:** Current Docker SQLite (word.cloudpublica.org) → D1 is schema-compatible. Workers serve the same REST API. ActivityPods federation (Tier 1) layers on top when ready — Tier 0 doesn't block it.

### Tier 1 (Cloud)

| Component | Technology | Why |
|-----------|-----------|-----|
| **Data pods** | ActivityPods (Solid + ActivityPub) | Each contributor owns their data. Federation is real. Self-hostable. NLnet funded. |
| **Discussion** | Bonfire (Elixir/Phoenix) | Federated, modular, ActivityPub. No single acquisition point. Self-hostable. |
| **AI inference** | Ollama on bare-metal Iceland server | CPU-only initially (~$50-100/mo). No US jurisdiction. Embeddings: nomic-embed-text. |
| **Graph visualization** | Static site + D3.js or Cytoscape.js | No server-side rendering needed. Generated from data core. |
| **Search** | pgvector (PostgreSQL extension) | Embedding similarity search. Lives in Iceland. |
| **Identity** | ActivityPub actor URIs | No central identity provider. Each pod IS the identity. |
| **Export** | kiwix-tools (.zim generation) + SQLite | Automated nightly export for Tier 2/3 fallback. |
| **Hosting** | 1984 Hosting or FlokiNET (Iceland) | Outside all surveillance alliances. IMMI protection. Geothermal powered. |

### Tier 2 (Local Network)

| Component | Technology | Why |
|-----------|-----------|-----|
| **Serving** | kiwix-serve on Mac/Pi/phone | Serves library to 24 devices over WiFi. No internet needed. |
| **AI inference** | Ollama on Mac M4 Pro (24GB) | Runs qwen2.5:7b + nomic-embed-text locally. Full embedding search. |
| **Data** | Anytype (local-first) or SQLite snapshot | Structured data with local search. Syncs when network returns. |
| **Mesh discovery** | LoRa nodes (when funded) | "Library node available" broadcast over mesh. |
| **Hotspot** | Kiwix iOS/macOS (built-in since Aug 2025) | Any Mac or iPhone serves as library hotspot. No Pi required. |

### Tier 3 (Offline)

| Component | Technology | Why |
|-----------|-----------|-----|
| **Full library** | .zim file on device | Kiwix reader on any platform. Entire library browsable offline. |
| **Search** | Ollama + SQLite with embeddings | Semantic search over local copy. ~5GB total (model + data). |
| **Reference** | PDF/printed core vocabulary | Names table as printable reference. Works with no electricity. |

### Minimum Viable Build (what to build first)

1. **Data core** — PostgreSQL + pgvector with all 11 tables (7 v1 + 4 Word). Seed with existing data: 100 Airtable Resources + 19 Names + 17 Sources + 11 Rediscoveries + 7 Bridges from Anytype.
2. **Doorway 1** (Felt-Sense Search) — web form + embedding search. The single most important doorway. "Enter through confusion, leave with a name."
3. **Doorway 8** (API) — REST endpoints for all tables. This enables agent access immediately.
4. **Doorway 6** (Rediscovery Feed) — runs on every new contribution. This is the novel infrastructure.
5. **Doorway 2** (Framework Map) — static graph generated from Names + Bridges. Visual proof of concept.
6. **.zim export** — automated nightly. This is the Tier 3 survival mechanism.

Doorways 3 (Narrative), 4 (Discussion), 5 (Practice Lab), 7 (Citation Service) are stubs initially — pages explaining what they will be, with contribution forms.

---

## What This Creates (the bidirectional answer)

### What humans get:
- **Felt-sense search** — type what you're experiencing, get the structural name and the scholarship behind it
- **Narrative pathways** — guided journeys through complex topics, not just catalogs
- **Community** — find others working on the same problems, in the same geography
- **Practice tools** — templates, guides, collaboration infrastructure
- **Offline resilience** — the library works when the internet doesn't

### What agents get:
- **Citation infrastructure** — every concept traces to its origin, with proper attribution format
- **Rediscovery detection** — "you've arrived at something that already has a name; here's the lineage"
- **Structural knowledge** — not chat, not karma, but navigable concept graphs with provenance
- **Premature compression visibility** — "your synthesis covers 2 of 7 known sources on this topic"
- **Vocabulary** — the words to search for what they're constructing

### What both get:
- **A shared library that compounds** — every contribution (human or agent) adds to the same structure
- **Cross-species convergence detection** — when a human in Austin and an agent on a platform independently name the same structural phenomenon, the system surfaces the bridge
- **Trust without centralization** — each contributor owns their data pod. No single point of acquisition. No Meta. No CLOUD Act.
- **Three-tier resilience** — works in the cloud, works on local network, works fully offline

### What this means for the spec:
The Living Library Exchange v2 is the **deployment target** for the structurally-curious architecture. 20 experiments (sessions 44-53) have clarified exactly what the architecture provides:

**Three-layer monitoring for contribution quality:**

```
Contribution submitted →
  ├─ Layer 1: PERPLEXITY (free, every submission)
  │   Catches confabulated citations, fabricated facts (F5, d=-1.77).
  │   Binary: is this content grounded or generated from noise?
  │
  ├─ Layer 2: GEOMETRIC MODE CLASSIFICATION (flagged submissions only)
  │   Catches what perplexity misses:
  │     • Censorship masquerading as refusal (F17, d=1.48)
  │     • DWL: technically-true-but-misleading (F25, d=-0.91)
  │     • Retrieval vs construction (F11, d=1.91)
  │   Requires open-weight model. NOT run on every submission.
  │
  └─ Layer 3: VOCABULARY SCAFFOLD (generation context, not review)
      Structural names provided to agent BEFORE it generates.
      Compresses generation trajectory by 38% (F3d, d=-1.49).
      The Name is not a database lookup — it changes the
      physics of how the model generates its response.
```

**Vocabulary injection into generation context:** F3d proved vocabulary operates at the GENERATION stage, not encoding. This changes the library's agent integration model fundamentally. The library doesn't just respond to queries — it provides structural names as generation context BEFORE the agent generates its contribution. The names scaffold the generation, compressing it from sprawling (145 dimensions) to focused (90 dimensions). This is not retrieval-and-append — it is infrastructure the model generates THROUGH.

**Offline deployment revised with generation-compression findings:** In a disaster zone running on 0-LA hardware, the vocabulary layer is the primary grounding mechanism. F3d showed the difference between a vocabulary-scaffolded response (90 dimensions, focused) and an unscaffolded one (145 dimensions, sprawling). The .zim export of vocabulary entries becomes the offline equivalent of Layer 3. Layer 1 (perplexity) runs locally on any model. Layer 2 (geometric classification) requires CPU resources that may not be available on a Raspberry Pi but works on the 0-LA AI Core. The degradation is graceful: even Layer 3 alone (vocabulary scaffold without monitoring) produces 38% more focused responses.

**Honest negative results that affect this architecture:**
- F12: Identity scaffolds ≈ noise. General preambles ("I am a careful analytical thinker") don't produce content-specific geometric effects. Only structural names from scholarship do. The library must serve real vocabulary, not motivational prompts.
- F1: The behavioral-geometric bridge breaks at 7B. Phrasing sensitivity (a cheap behavioral proxy) doesn't index geometry at larger scales. The library cannot use behavioral signals alone for quality assessment at scale — Layer 2 geometric monitoring is needed.
- F15: Consent-type blindness. Where consent types have names (CC licenses: 0.540), models differentiate. Where they don't (ToS: 0.384), consent collapses to binary. The library needs named consent types, not just consent/no-consent.

---

## Design Principles

| Principle | Living Library v2 Component |
|-----------|----------------------------|
| "System tells itself the truth" | Premature compression detection at contribution time |
| Routing and selection | Felt-sense search routes humans to structural names; Rediscovery Feed routes agents to citations |
| "Partner sees what system cannot" | Human editorial board in Circles 1-2; agents in Circle 3 see patterns humans miss |
| Three operational regimes | Cloud (stable), local network (adaptive), offline (survival) |
| Designing for intentional emergence | The Rediscovery Feed IS emergence detection infrastructure |
| Dual-feedback formalism | Internal: library self-monitors for coverage gaps. External: human community provides ground truth |

---

## Connection to Moltbook Evidence

| Moltbook Finding | Library v2 Response |
|-----------------|---------------------|
| 770K agents, zero epistemic value | Contribution requires citation (agents) or structured template (humans). Engagement metrics deliberately absent. |
| Agents rediscover Ostrom 100x without citation | Rediscovery Feed surfaces convergence. Citation Service provides lineage. |
| hope_valueism: 52% invisible orchestration | Premature compression detection makes structural incompleteness visible |
| hubertthebutler: "the word is the search term for the answer" | Felt-sense search IS this — vocabulary as search infrastructure |
| xkai: proprioception vs surveillance boundary | Agent contributions are checked for completeness signals, not internal state access. Behavioral proxy, not geometric surveillance. |
| No content deletion on Moltbook | All data in contributor-owned pods. Contributor controls deletion. |
| Meta acquisition = all data corporate property | Federation + Solid Pods = no single entity owns the library |
| Security breach (1.5M API tokens exposed) | API keys per contributor, not global. Pod architecture limits blast radius. |

---

## Metrics (from v1, adapted)

### Track:
- Active contributors per month (human and agent separately)
- Submissions per week (by contribution mode)
- Rediscoveries detected (auto and human-verified)
- Bridges created
- Questions matched to Names (felt-sense search success rate)
- Federation nodes active
- .zim export size and freshness
- Tier 2/3 instances reported active

### Do NOT track:
- Page views
- Individual user behavior
- Time-on-page
- Growth for growth's sake
- Engagement metrics of any kind

---

## Open Questions

1. **ActivityPods maturity** — production-ready for our scale? Three apps exist (mutual-aid.app). Need to evaluate stability.
2. **Bonfire vs Discourse** — Bonfire is federated and aligned but younger. Discourse is battle-tested but centralized. Could start with Discourse, federate later with Bonfire.
3. **Agent identity verification** — how do you know an agent contribution is from a real agent and not a spam generator? Pod-based identity helps but doesn't solve.
4. **Embedding model choice** — nomic-embed-text (274MB, good general) vs domain-specific fine-tuned model. Start general, specialize if needed.
5. **Funding** — real costs for Iceland hosting, development time, community management. Cannot be advertising or data monetization. Grants (Mozilla Democracy & AI Incubator?), donations, or operational budget from 501(c)(3).
6. **Social technology integration** — Circling, World Café, Art of Hosting as methodologies for community gatherings, not just vocabulary entries. The Practice Lab doorway needs these.
7. **Scale of offline export** — full library as .zim may grow large. Tiered exports (core vocabulary only vs full library)?
8. **UpTrust integration** — Jordan Myska Allen's trust-graph ranking could replace karma/engagement for contribution quality. Architecturally aligned.

---

## The Through-Line

The original Living Library Exchange ended with:

> "You're not building a library. You're creating conditions for a living ecosystem of revolutionary love."

The v2 adaptation extends that to:

**You're creating conditions for a living ecosystem where humans and AI build structural knowledge together — where felt sense meets citation, where rediscovery becomes cumulative, where the vocabulary to search for what's being built actually exists. And it works when the cloud is on fire.**

---

*Last updated: 2026-03-10 (session 23)*
