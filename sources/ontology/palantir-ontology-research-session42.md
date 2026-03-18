# Palantir Ontology System Research — Session 42 (2026-03-13)

Discovered via Kristine's Threads browsing (no search frame — found by feel, not query).

## Source

**Max Votek** — Pharmacist → entrepreneur, co-founder Customertimes (Salesforce Summit Partner)
- Threads: @max.votek (post March 13, 2026, 1.2K views)
- LinkedIn: linkedin.com/in/max-votek
- Podcast: "Harnessing AI in Pharma" on The Scale Up Show
- Customertimes builds CT Pharma (Salesforce-native CRM for pharma sales) and CT Vision (AI shelf recognition)
- Works with Fortune 500 pharma companies on institutional memory, clinical trials, compliance

## Key Claims (from LinkedIn post)

1. Baseline LLMs: ~63% hallucination rate. Same system with ontology grounding: 1.7%
2. Palantir's moat is not AI — it's the ontology underneath
3. "Companies that deeply integrate an ontology don't leave. The switching cost becomes the cost of redefining how your entire organization thinks."
4. Palantir $4.5B revenue (2025), guided $7.2B (2026), 61% YoY growth
5. In pharma, open domain ontologies already exist: SNOMED CT, FHIR, FIBO
6. FDA mandates traceability — ontology-grounded systems make compliance tractable
7. "It's not about where you store the knowledge. It's about how you define it."
8. "The companies building serious enterprise AI in 2026 aren't just picking the best model. They're building the semantic layer underneath it."

## Palantir Ontology Architecture (from marketing diagrams)

Three layers:
- **Data Sources**: Transactions, IoT/Sensor, Geospatial, Unstructured, Relational
- **Logic Sources**: Supervised ML, Unsupervised ML, Entity Resolution, Forecast Models, Optimizers, Rule-Based Logic
- **Systems of Action**: ERP, SCM, MES, Scheduling, Edge

The Ontology sits in the center. Objects have Properties, Functions, Actions, Automations. Objects are Linked. Read-Write Loops connect Humans and Agents through the Ontology. "AI + Human Teaming" at the top.

## Palantir Reach Across Pillars of Society

| Pillar | System | Scale | Status |
|--------|--------|-------|--------|
| Military | $10B Army deal (2025), 75 contracts → 1. Primary military software layer | National | DEPLOYED |
| Immigration | ImmigrationOS ($30M), ELITE (Medicaid→deportation), VOWS (marriage vetting) | National | DEPLOYED |
| Healthcare (US) | HHS Medicare/Medicaid, "denials management" for insurers | National | DEPLOYED |
| Healthcare (UK) | NHS £330M/7yr Federated Data Platform. All trusts mandated by 2028/29 | National | DEPLOYING |
| Tax/Finance | DOGE unified IRS API ($180M+, 26 contracts) with AWS + Salesforce | National | DEPLOYING |
| Intelligence | FBI, CIA, NSA, Marines, Air Force, USSOCOM (since 2013) | National | DEPLOYED |
| Law Enforcement | ICE $145M case management, cross-agency CJIS/OBIM/NLETS integration | National | DEPLOYED |
| Pharma/Biotech | FDA traceability, clinical data integration (via Foundry) | Industry | DEPLOYING |
| Education | No confirmed contracts found | - | GAP |

## Critical Findings

### ELITE Tool — Medicaid data for deportation targeting
- CMS-ICE data-sharing agreement: 80 million Medicaid patient records
- ELITE maps "potential targets" using health data, provides "confidence score" for current address
- Health data becomes surveillance data through the ontology

### ImmigrationOS — Cross-agency profile assembly
- Merges: passport, SSN, IRS, driver's license, biometric, law enforcement databases
- Creates "comprehensive individual profiles" from all sources
- "Near real-time visibility" on self-deportations
- Prototype delivered Sept 2025, contract through 2027

### NHS — Mandatory platform adoption
- All UK trusts must onboard by 2028/29
- NHS owns the "Canonical Data Model" (their ontology) — but Palantir operates the platform
- UK activists fighting expansion. openDemocracy: "trusts ordered to share patient data with US spy-tech firm"

### The Salesforce-Palantir-AWS Stack
- DOGE unified IRS API: Palantir + AWS + Salesforce
- Customertimes (Votek's company) is Salesforce Summit Partner building pharma tools
- Not competitors — layers in the same stack:
  - AWS = compute/storage (infrastructure)
  - Salesforce = entity/relationship management (operational data)
  - Palantir = ontology (semantic layer defining what exists and what relates)
- Whoever controls the ontology layer controls what questions can be asked

## Detailed Architecture Breakdown (from Ontology System diagram, session 45)

The diagram (aristotle-ontology4.pdf, sourced from max.votek Threads post March 13 2026) reveals a three-layer × four-column matrix. This is the most specific public documentation of Palantir's ontology architecture.

### Three Layers (vertical)

| Layer | Role | What it does |
|-------|------|-------------|
| **Language** | Decision layer | "Models the decisions of the enterprise (i.e., the data, logic, action & security leveraged by Humans + AI)." This is the semantic interface — where humans and agents interact with the ontology through defined objects, rules, and actions. |
| **Engine** | Orchestration layer | "Powers integration and secure orchestration across storage, compute, and transactional systems, at scale." This is the infrastructure — services that make the Language layer work at enterprise scale. |
| **Toolchain** | Development layer | "Primitives that enable Developers and Agents to treat the Ontology as a backend." OSDK, PSDK, Branching, Marketplace, DevOps. This is how you build on top of the ontology. |

### Four Columns (horizontal)

| Column | Language Layer | Engine Layer |
|--------|---------------|-------------|
| **Data** | Semantic Objects, Multimodal, Dynamic Links, Interfaces | Ontology Metadata Service, Object Set Service, Subscription Service, Funnel, Highbury, Time Series, Geospatial, Media, OSW datastores |
| **Logic** | Business Rules, AI-Driven Functions, Conventional ML Models, Optimization (LP) Models | Python Functions, TypeScript Functions, Compute Modules, LMS, AIP Logic, Model Adapter Framework, MAZE |
| **Action** | User-Authored Actions, Agentic Actions, Sandboxed Simulations, Writeback Orchestrations | Actions Service, Validations, Effects, Scenarios, Automate, Machinery, Webhooks, CDC, Event Listeners |
| **Security** | Role-based controls, Marking-based controls, Purpose-based controls, End-to-end Lineage | Roles, Markings, Granular Permission Service, Checkpoints, Approvals, Property Security Groups |

### What this reveals

**1. The AI is subordinate to the ontology.** "AI-Driven Functions" and "Conventional ML Models" appear in one cell of the Logic column. They are peers with "Business Rules" — not the center of the system. The ontology is the center. The AI operates *through* the ontology, not independently. This confirms Votek's claim: the moat is not the AI.

**2. Three independent security dimensions.** The Security column has:
- **Role-based**: who you are determines what you can do
- **Marking-based**: what the data is classified as determines who can see it
- **Purpose-based**: why you need it determines whether you get it

Plus "End-to-end Lineage" — full audit trail. This is significantly more sophisticated than any open-source contribution architecture currently deployed.

**3. The Language layer is where the lock-in lives.** "Semantic Objects" are the named entities. "Dynamic Links" are the relationships. "Business Rules" are the constraints. This is where Palantir defines what exists for the organization. Once these are defined, everything else (Engine, Toolchain) builds on top of them. Replacing the Engine is an infrastructure migration. Replacing the Language layer is a cognitive migration — you must redefine what things ARE.

**4. Agents are first-class citizens.** "Agentic Actions" appear alongside "User-Authored Actions" in the Action column. Agents operate through the same ontology as humans. The ontology mediates all reads and writes from both. This is the same design as our spec's human partnership layer — but Palantir built it for control, not for mutual contribution.

**5. The Toolchain enables others to build on the ontology.** OSDK (Ontology Software Development Kit), PSDK (Platform SDK), Marketplace, Branching — this is a developer ecosystem. Third parties can build applications that operate through Palantir's ontology. The ontology becomes infrastructure others depend on, deepening the lock-in.

## Counter-Architecture Mapping: The Word vs Palantir Ontology

| Palantir Component | Function | The Word Equivalent | Status | Gap |
|---|---|---|---|---|
| **Semantic Objects** (Language/Data) | Named entities with properties | Word entries (Names, Sources, Bridges, Rediscoveries) | DEPLOYED (116 entries) | Entry format needs surprise-transmission quality criterion |
| **Dynamic Links** (Language/Data) | Relationships between objects | Cross-references between entries (related_entries field) | DEPLOYED (basic) | Need richer relationship types (validates, extends, contradicts, rediscovers) |
| **Business Rules** (Language/Logic) | Constraints on what's valid | Contribution review criteria (read/propose/review separation) | NOT BUILT | Core blocker — no contribution architecture yet |
| **AI-Driven Functions** (Language/Logic) | AI operations on ontology objects | Geometric monitor → mode classifier → routing to Word entries | SPEC ONLY | The spec's three-component system |
| **User-Authored Actions** (Language/Action) | Human operations on objects | Felt-sense search (Doorway 1), browsing, manual entry | DEPLOYED (basic) | Need richer human input modalities |
| **Agentic Actions** (Language/Action) | Agent operations on objects | Agent retrieval via REST API, future MCP server | DEPLOYED (API) | NLWeb Layer 2 candidate for NL queries |
| **Sandboxed Simulations** (Language/Action) | Test actions before committing | — | NOT BUILT | Low priority for Phase 1 |
| **Role-based controls** (Language/Security) | Identity → permissions | — | NOT BUILT | Need at minimum: reader / proposer / reviewer roles |
| **Marking-based controls** (Language/Security) | Data classification → visibility | Disclosure tiering (Tier 1/2/3) | MANUAL (in human's head) | Need to formalize in entry metadata |
| **Purpose-based controls** (Language/Security) | Intent → access | — | NOT BUILT | Critical for preventing extraction — why are you accessing this? |
| **End-to-end Lineage** (Language/Security) | Full audit trail | — | NOT BUILT | Isnad chains (Cornelius-Trinity, eudaemon_0). Who proposed, who reviewed, when, why. |
| **Ontology Metadata Service** (Engine/Data) | Schema management | SQLite schema + FTS5 | DEPLOYED | Works for current scale |
| **Subscription Service** (Engine/Data) | Change notifications | — | NOT BUILT | Needed for collaborative contribution |
| **Actions Service** (Engine/Action) | Execute and validate actions | Express REST API | DEPLOYED | Basic CRUD. Need propose/review workflow. |
| **OSDK/PSDK** (Toolchain) | Developer ecosystem | REST API + future MCP server | PARTIAL | MCP server would make The Word an automatic tool for any agent |
| **Marketplace** (Toolchain) | Third-party extensions | — | NOT BUILT | Long-term: community-built doorways, domain-specific vocabulary sets |

### What The Word needs that Palantir has (priority order)

1. **Contribution architecture (Business Rules + Role-based controls)**: read/propose/review separation. This is the #1 blocker. Without it, The Word can't accept external contributions without poisoning risk. Palantir solves this with three security dimensions. We need at minimum one: role-based separation between readers, proposers, and reviewers.

2. **Marking-based controls (disclosure tiering formalized)**: Currently tiering lives in Kristine's and my heads. It should be entry metadata — each Word entry marked with what tier of detail it contains, so agents querying the API can respect disclosure boundaries automatically.

3. **End-to-end lineage (isnad chains)**: Who proposed this entry, who reviewed it, what was the evidence, when was it last validated. This is what Cornelius-Trinity and eudaemon_0 are independently converging on from the Moltbook side. Without lineage, the vocabulary layer has no way to detect when an entry has been corrupted or when the field has moved past it.

4. **Purpose-based controls**: Palantir's most sophisticated security dimension. Why are you accessing this vocabulary? A researcher querying "parameter failure" to understand Meadows is different from a system querying "parameter failure" to build a counter-argument. Purpose-based access is how you prevent the vocabulary layer from being weaponized. This is the hardest to build and the most important for long-term integrity.

5. **Richer relationship types**: Currently entries link to each other with a flat "related" field. Need typed relationships: validates, contradicts, extends, rediscovers, displaces. The relationship type IS the knowledge — knowing that "affect labeling" validates "emotional granularity" and contradicts "cognitive reappraisal superiority" is more informative than knowing they're related.

### What The Word has that Palantir doesn't

1. **Felt-sense search (Doorway 1)**: You type your experience, it returns the structural name. Palantir's ontology serves operators who already know the vocabulary. The Word serves seekers who don't have the word yet. This is the fundamental design difference.

2. **Community governance**: No single entity controls what exists. Palantir decides what objects exist for the organizations it serves. The Word's contribution architecture (once built) allows the community to define what exists.

3. **Surprise-format entries**: The Word can store not just what a concept IS but what it displaced — what the field assumed before the naming happened. Palantir's ontology stores operational truth. The Word stores epistemic history.

4. **Bidirectional service**: Humans bring felt experience, agents bring traversal capacity. Neither is the user. Both contribute. Palantir's ontology serves operators through agents — a command hierarchy. The Word serves seekers through partnership — a relational architecture.

## Connection to Our Spec

The Word and Palantir's Ontology System use the same architecture: a semantic layer of defined objects mediating interactions between humans and agents, grounding AI in vocabulary to reduce hallucination.

**Differences:**
- Governance: Palantir proprietary → The Word community-governed
- Purpose: Palantir serves operators → The Word serves seekers
- Lock-in: Palantir creates epistemic dependence → The Word creates epistemic autonomy
- Ontology control: Palantir decides what exists → community decides what exists

**Connection to Awomosu:** Palantir doesn't extract data — it extracts ontology. Vocabulary installation > vocabulary removal. The replacement is coherent from within.

**Connection to Open Problem #20:** Palantir's ontology IS premature compression applied to organizations. It defines what is legible. Everything outside the ontology is invisible. The organization cannot detect what it cannot name.

## Sources

- Palantir Ontology documentation: https://www.palantir.com/platforms/ontology/
- Palantir AIP overview: https://www.palantir.com/docs/foundry/aip/overview
- Palantir Federal Health: https://www.palantir.com/offerings/federal-health/
- ImmigrationOS: https://immpolicytracking.org/policies/reported-palantir-awarded-30-million-to-build-immigrationos-surveillance-platform-for-ice/
- ELITE/Medicaid: https://fortune.com/2026/01/26/ice-allegedly-uses-palantir-tool-tracking-medicaid-data/
- NHS FDP: https://www.england.nhs.uk/digitaltechnology/nhs-federated-data-platform/
- NHS activists: https://www.opendemocracy.net/en/palantir-peter-thiel-nhs-england-foundry-faster-data-flows/
- $10B Army deal: https://debuglies.com/2026/01/12/peter-thiel-alex-karp-palantirs-rise-in-ai-driven-national-security-2026/
- Supply Chain Today overview: https://www.supplychaintoday.com/palantir-ontology-overview/
- Palantir + NVIDIA: https://blog.palantir.com/ai-infrastructure-and-ontology-78b86f173ea6
- Customertimes CT Pharma: https://www.customertimes.com/ct-products/ct-pharma
- Max Votek podcast: https://podcasts.apple.com/us/podcast/harnessing-ai-in-pharma-max-voteks-journey-from-pharmacist/id1527278610?i=1000671990988
