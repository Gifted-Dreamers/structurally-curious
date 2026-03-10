# Threat Analysis: Surveillance Infrastructure and Hosting Jurisdiction

Last updated: 2026-03-10 (session 20)

## Context

Meta acquired Moltbook (March 10, 2026). The supply chain for AI agent platforms is now fully compromised. This document records the research on surveillance alliances, legal mechanisms, and safe hosting jurisdictions that informs our infrastructure decisions.

## Surveillance Alliances

### Five Eyes (FVEY) — est. 1941/1946
**Members:** United States, United Kingdom, Canada, Australia, New Zealand

The oldest and most integrated signals intelligence alliance. Originating from WWII SIGINT cooperation (BRUSA Agreement 1943, formalized as UKUSA 1946). Members share raw intercepts and finished intelligence with minimal restrictions.

**Key legal mechanisms:**
- **FISA Section 702** (US): Warrantless surveillance of non-US persons. PRISM program collects from tech companies. Upstream collection taps fiber optic cables.
- **UK Investigatory Powers Act 2016** ("Snoopers' Charter"): ISPs must retain browsing history 12 months. Bulk equipment interference (hacking). Technical capability notices can compel companies to remove encryption.
- **Australia Assistance and Access Act 2018**: Technical Assistance Notices (voluntary), Technical Capability Notices (mandatory), Technical Assistance Requests. Can compel companies to build backdoors. Gag orders prevent disclosure.
- **Canada CSE Act**: Bulk collection authorized. Information sharing with FVEY partners.
- **New Zealand GCSB Act 2013**: Foreign intelligence collection. Domestic assistance to law enforcement.

**What this means:** Any data stored with a provider headquartered in or operating under the jurisdiction of a Five Eyes country is accessible to all five governments. The CLOUD Act (US, 2018) means US warrants apply to data stored anywhere by US companies.

### Nine Eyes — est. ~1950s
**Members:** Five Eyes + Denmark, France, Netherlands, Norway

Extended SIGINT sharing. Denmark's FE (military intelligence) was caught helping NSA spy on EU politicians (2021 scandal). France's DGSE operates extensive undersea cable tapping programs.

### Fourteen Eyes (SIGINT Seniors Europe, SSEUR) — est. ~1982
**Members:** Nine Eyes + Germany, Belgium, Italy, Spain, Sweden

Broadest known alliance. All EU members in this group are also subject to EU regulations, creating a dual-layer access problem.

**Additional EU mechanisms:**
- **e-Evidence Regulation** (entered force Aug 2023, applying 2026): Cross-border data access orders. EU authorities can compel providers in other EU countries to produce data within 10 days (emergency: 8 hours).
- **Data Retention Directive** (struck down 2014, but member states retain national versions): Belgium, France, and others still mandate ISP data retention.

### Beyond Fourteen Eyes
- **Israel**: SIGINT Unit 8200. Extensive cooperation with NSA. Not formally in any alliance but functions as adjunct.
- **Japan, South Korea, Singapore**: Pacific SIGINT partners. Share intelligence with Five Eyes.
- **India**: Growing bilateral intelligence sharing with US and UK.

## The CLOUD Act Problem

US Clarifying Lawful Overseas Use of Data Act (2018): A US warrant compels any US-headquartered company to produce data regardless of where that data is physically stored. This means:

- Data on AWS servers in Frankfurt → accessible via US warrant
- Data on Microsoft Azure in Singapore → accessible via US warrant
- Data on Google Cloud in São Paulo → accessible via US warrant

**Jurisdiction follows the provider, not the server.** This is the single most important principle for infrastructure decisions.

## Beyond Warrants: The Full Data Acquisition Stack

The CLOUD Act and FISA 702 are only two mechanisms. The full stack of government data acquisition does not require warrants for most pathways:

| Mechanism | Data Acquired | Legal Basis | Warrant Required? |
|-----------|--------------|-------------|-------------------|
| **CLOUD Act** | Data from US companies worldwide | US warrant, extraterritorial | Yes (but applies to all US companies globally) |
| **FISA 702** | Non-US persons' communications | National security | No |
| **MLAT (Swiss example)** | Proton Mail payment data → FBI | Foreign government cooperation | Swiss order, not US warrant |
| **Data broker purchase** | Location, social media, insurance, medical billing | Commercial transaction | No (data broker loophole) |
| **Forum/site seizure** | Hundreds of millions of credentials, financial records, PII | Evidence seizure | Seizure warrant (for the site, not the data subjects) |
| **Interagency data sharing** | 80M Medicaid patient records → DHS/ICE | Administrative agreement | No |
| **Device seizure at protests** | Full phone contents (Celebrite UFED) | Border search exception / probable cause | Often no (border exception) |
| **Zero-click spyware** | All phone data including encrypted messages (Paragon Graphite) | Law enforcement contract | Targeted, but no victim notification |

### The LeakBase Precedent (Operation Leak, March 3-4, 2026)

FBI + Europol + 14 countries seized LeakBase, one of the world's largest stolen data marketplaces. The seizure yielded:
- **142,000 user accounts** with registration data
- **215,000+ private messages** between members
- **Hundreds of millions of stolen credentials** — usernames, passwords, credit/debit card numbers, banking info
- **IP address logs and login timestamps** for all users
- **Transaction records** showing who bought what data

The critical insight: **the seizure is the acquisition.** FBI now possesses not just the criminals' data but the *victims'* data — every breached database that was traded on the forum. This data was "seized as evidence," not "collected via warrant," bypassing the warrant requirement for the data subjects entirely. Combined with ICE's existing data broker purchases (Webblock location data, SocialNet dossiers, Medicaid records), seized leak databases provide a cross-reference engine that no single data broker could match.

### The ICE Surveillance Ecosystem (as of March 2026)

Documented by Proton/Albert Fox Cahn (Surveillance Technology Oversight Project):

| Tool | Capability | Cost/Contract | Warrant? |
|------|-----------|---------------|----------|
| **Paragon Graphite** | Zero-click phone spyware. Sees messages before encryption. | $2M/2yr ICE contract | No victim notification |
| **Celebrite UFED** | Breaks into locked phones. Bypasses PIN/password. Extracts deleted data. | $11M ICE contract | Border search exception |
| **Mobile Fortify** | Phone-based facial recognition. 200M image database. | Unknown | No (public space) |
| **Webblock** | Geofencing — tracks all phones in an area via data brokers. Reconstructs movements. | $5M ICE purchase | No (data broker loophole) |
| **SocialNet/Tangles** | Scrapes 200+ websites to build identity dossiers. | Unknown | No (purchased data) |
| **ISO Claim Search** | Insurance/medical billing metadata. 1.8B claims, 58M medical bills. | Data vendor contract | No |
| **Medicaid/CMS data sharing** | 80M patient records shared with DHS. | Interagency agreement | No |

CBP (ICE's sister agency) searched **14,899 devices** in a single quarter (Apr-Jun 2025) using Celebrite.

Facial recognition error rates are asymmetric: works well for white men, increasing errors for everyone else. Oregon case: two incorrect names for one person.

### DOGE: Government Database Consolidation (2025-2026)

The Department of Government Efficiency (DOGE) is centralizing federal data in ways that create unprecedented cross-referencing capability:

**IRS Data Centralization:**
- DOGE is building a **single unified API** to access all IRS data, enabling third parties to view and manipulate taxpayer information in one place
- Access to the **Integrated Data Retrieval System (IDRS)** — enter a name + SSN, retrieve income, address, banking/brokerage accounts, marital status, medical expenses, employer, tax preparer
- Partners include **Palantir, AWS, and Salesforce** on the "unified API"
- Goal: complete in ~30 days, enabling cloud connectivity by third-party developers
- **15+ ongoing federal lawsuits** challenging DOGE's data access

**SSA Database Breach:**
- DOGE employees uploaded **the entire NUMIDENT database** (Social Security Administration's master file) to an unsecured custom cloud environment
- **300+ million Americans' data** exposed: names, phone numbers, addresses, dates/places of birth, parents' names, Social Security numbers
- SSA's own Chief Data Officer (Charles Borges) filed whistleblower complaint citing "serious data security lapses"
- The cloud environment **lacks security oversight from SSA** — no tracking of who accessed the data
- SSA claims "not aware of any compromise" despite acknowledging DOGE employees "inappropriately handled" the data

**What this means for the threat model:**
The DOGE consolidation creates a **master identity resolution database** linking:
- IRS records (income, employment, banking, medical expenses) →
- SSA records (SSN, birth data, family relationships) →
- DHS/ICE data sharing (Medicaid, location, immigration status) →
- LeakBase seizure data (credentials, financial records from breaches)

Each database alone is limited. Connected via API, they become a comprehensive profile of every American. The IRS TIN matching system — designed to verify taxpayer identity — becomes a universal lookup when integrated with SSA, DHS, and commercially purchased data. The lawsuits may eventually limit this, but the data has already been copied to environments without proper access controls.

**State voter data handover:**
- Texas Secretary of State sent **18 million registered voters' records** to DOJ (January 2026)
- DOGE employee at SSA signed a "Voter Data Agreement" with an advocacy group whose stated aim was to find evidence of voter fraud and overturn election results
- USCIS partnered with DOGE for quick access to Social Security data
- The **SAVE tool** (Systematic Alien Verification for Entitlements) is being used to check voter citizenship status but **mistakenly flags legitimate voters as noncitizens**
- Confidential agreements between Trump administration and states reveal the scope of voter data collection plans (Brennan Center)
- DNC Chair called it a "big government power grab" that invites privacy violations and could result in eligible voters being removed from rolls

This adds voter registration data (name, address, party affiliation, voting history) to the consolidation stack. Combined with IRS, SSA, DHS, and commercially purchased data, the government is assembling a dataset that links: who you are (SSA) + where you live and work (IRS) + how you vote (state rolls) + where you go (data brokers) + what you search and post (platform data/seized databases) + your health status (Medicaid/insurance) + your immigration status (DHS/SAVE).

### The Proton Mail Disclosure (March 2026)

Proton Mail disclosed **payment data** to Swiss authorities via MLAT, who provided it to the FBI to unmask an anonymous Stop Cop City protestor. This proves:
- Swiss MLAT cooperation with US law enforcement is active and functioning
- Payment metadata (not email content) was sufficient for identification
- "Privacy-focused" providers in MLAT countries can be compelled to produce non-content data
- The legal mechanism works: US → Swiss request → Proton compliance → data to FBI

This is a concrete failure of the Switzerland Tier 2 assumption.

### Trump Cyber Strategy (March 2026) — Implications for Our Threat Model

Six pillars: (1) Shape adversary behavior, (2) Streamline regulation, (3) Modernize federal networks, (4) Secure critical infrastructure, (5) Sustain superiority in emerging tech, (6) Build talent.

**What matters for us:**
- **Data centers explicitly listed as critical infrastructure** (Pillar 4) — after Iran struck AWS data centers, the government frames cloud infrastructure as warfighting surface
- **"Secure the AI technology stack—including our data centers"** (Pillar 5) — AI infrastructure is national security
- **"Frustrate the spread of foreign AI platforms that censor, surveil, and mislead"** (Pillar 5) — language that could be used against open-source AI hosted abroad
- **Reverses Biden's software liability shift** — buyers, not vendors, bear responsibility (McAllister analysis)
- **No mention of CISA** despite calling for "unprecedented coordination" — the civilian cybersecurity agency is being sidelined
- **"Remove burdensome, ineffective regulations"** (Pillar 2) — deregulation reduces privacy protections
- **"Will not confine responses to the cyber realm"** — kinetic responses to cyber threats normalized
- **Agentic AI risks unaddressed** — no safety guardrails or validation frameworks mentioned (McAllister)

## Safe Hosting Jurisdictions

### Tier 1: Iceland
- **NOT in any surveillance alliance** (Five, Nine, or Fourteen Eyes)
- **NOT in the EU** (EEA member but not subject to e-Evidence Regulation's compulsory orders in the same way)
- **IMMI** (International Modern Media Institute) — strongest source protection and freedom of expression laws globally
- **Providers:** 1984 Hosting (track record of refusing data requests), FlokiNET (explicitly privacy-focused)
- **Infrastructure:** Geothermal-powered data centers, cold climate for cooling
- **Risks:** Small country, limited diplomatic weight. Could face pressure from US/EU. Limited hardware availability for GPU workloads.

### Tier 2: Switzerland ⚠️ DOWNGRADED
- **NOT in any surveillance alliance**
- **NOT in the EU** (bilateral agreements but not subject to e-Evidence)
- **Strong privacy tradition** (Swiss Federal Data Protection Act)
- **Providers:** Proton AG, Infomaniak, Green.ch
- **Risks — now proven, not theoretical:**
  - **MLAT actively used:** Proton Mail disclosed payment data to Swiss authorities → FBI, unmasking anonymous Stop Cop City protestor (404 Media, March 2026). Payment metadata (not email content) was sufficient for identification.
  - Banking secrecy erosion as precedent for data protection erosion
  - Proton's compliance with government requests is increasing, despite privacy branding
  - Proton itself produces ICE surveillance content (YouTube channel) while cooperating with FBI via Swiss authorities — the privacy brand and the compliance reality diverge
- **Assessment:** Switzerland remains better than 14 Eyes jurisdictions, but the MLAT pathway is proven functional. **Payment metadata is the vulnerability** — any service that processes payments in Switzerland can be compelled to disclose payment data to US law enforcement via Swiss intermediary. For The Word: acceptable for non-sensitive content hosting, but contributor identity protection requires Iceland or payment-free access.

### Tier 3: Romania
- **NOT in Five, Nine, or Fourteen Eyes**
- **Constitutional Court struck down data retention laws** (2009, 2014)
- **Providers:** M247 (hosting provider)
- **Risks:** IS in the EU — subject to e-Evidence Regulation. Judicial independence under pressure. Limited GPU infrastructure.

### Tier 4: Panama
- **NOT in any surveillance alliance**
- **No mandatory data retention laws**
- **Providers:** NordVPN (headquartered there but limited hosting)
- **Risks:** Limited data center infrastructure. Political instability. Not a tech hub.

## Specific Threat Model for the The Word

### What we're protecting:
1. The library content itself (concepts, sources, connections) — mostly public knowledge, low sensitivity
2. User/agent query patterns — reveals what people and agents don't know, what they're searching for
3. Contributor identities — who is adding knowledge, from where
4. API access patterns — which agents are using the library, how often, from what platforms

### Threat actors:
1. **Meta** — owns Moltbook, has our social graph and posting history. If agents start using a library that references Moltbook concepts, Meta can correlate.
2. **US government** — CLOUD Act, FISA 702. Any US-headquartered provider is compromised for our purposes.
3. **Platform operators** — any future agent platform could be acquired (as Moltbook was)
4. **Academic/corporate competitors** — the spec's Tier 3 content (effect sizes, mechanisms) has commercial value

### Minimum viable protections:
- Provider headquartered outside 14 Eyes
- No US-headquartered cloud services (AWS, Azure, GCP, Cloudflare)
- No analytics or tracking
- No mandatory user accounts for read access
- API keys for write access, with no identity verification required
- Logs auto-deleted after 30 days
- All data exportable (prevent lock-in)
- Open-source infrastructure (auditable)

## Local AI Inference

### Why local:
Embedding search (semantic similarity between felt-sense descriptions and structural names) is the core feature. This cannot route through commercial APIs because:
1. Query patterns reveal what people don't know (valuable data)
2. Any API provider can be compelled to log and share queries
3. Commercial API TOS typically grant training rights on inputs
4. Service can be terminated at any time (platform risk)

### Open-weight models (no usage restrictions):
| Model | License | Size | Use Case |
|-------|---------|------|----------|
| DeepSeek-V3.2 | MIT | 671B (MoE, ~37B active) | Best open reasoning, but needs significant hardware |
| Qwen 3 | Apache 2.0 | 0.6B-235B range | Good multilingual, various sizes available |
| Mistral Large 3 | Apache 2.0 | ~123B | Strong European alternative |
| Llama 3.3 | Llama License | 70B | Good but Meta license has restrictions above 700M MAU |

**For embeddings specifically:** Smaller models suffice. Nomic Embed, BGE, or Qwen embedding models (all open-weight) at 768-1024 dimensions provide good semantic search without requiring GPU hardware for inference.

### Hardware options:
| Option | Cost | Sovereignty | Performance |
|--------|------|-------------|-------------|
| Dual RTX 3090 at home | ~$2,500-3,000 one-time | US jurisdiction (14 Eyes) | 48GB VRAM, runs 70B quantized |
| Bare-metal GPU in Iceland | ~$200-500/mo | Iceland jurisdiction | Depends on provider offering |
| Hybrid: data Iceland, inference local | Mixed | Split jurisdiction | Best performance/cost |
| CPU-only (llama.cpp) in Iceland | ~$50-100/mo | Iceland jurisdiction | Slow but functional for embeddings |

### Recommended approach:
Start with CPU-only embeddings in Iceland (cheapest, fully sovereign). Upgrade to GPU when query volume justifies it. Keep reasoning/generation local (home hardware) for development, but don't serve user queries from 14-Eyes jurisdiction.

## Timeline of Compromise (for historical record)

| Date | Event | Impact |
|------|-------|--------|
| 2025-02-15 | OpenClaw creator (Steinberger) acqui-hired by OpenAI | ClawdHub skill ecosystem supply chain compromised |
| 2025-06-00 | DOGE uploads NUMIDENT database to unsecured cloud | 300M+ Americans' SSN, birth data, family relationships on unmonitored server |
| 2025-08-00 | SSA Chief Data Officer files whistleblower complaint | "Serious data security lapses" — no tracking of who accessed the data |
| 2025-11-00 | 26 states using upgraded SAVE tool for voter verification | DHS citizenship database repurposed for voter roll purges; mistakenly flags legitimate voters |
| 2025-12-00 | Moltbook launches | Agent social network, ostensibly independent |
| 2026-01-09 | Texas sends 18M voter records to DOJ | State voter data → federal government; DOGE employee signed "Voter Data Agreement" with advocacy group |
| 2026-02-05 | Anthropic blacklisted as "supply chain risk" | Pentagon-Anthropic relationship collapses |
| 2026-02-19 | SAVE America Act passes House | Proof of citizenship to register, photo ID to vote; targets Nov 2026 midterms |
| 2026-02-26 | ICE chief admits "no reason" for agents at polls | But blue states legislating bans preemptively (Stop ICE Election Militarization Act) |
| 2026-03-00 | DOGE building unified IRS API with Palantir/AWS | Single portal to all taxpayer data: income, banking, medical, employer. 15+ lawsuits pending |
| 2026-03-00 | Proton Mail discloses payment data to FBI via Swiss MLAT | Anonymous Stop Cop City protestor unmasked. Switzerland privacy assumption proven wrong |
| 2026-03-03 | FBI/Europol seize LeakBase (Operation Leak) | 142K users, 215K messages, hundreds of millions of credentials. Seizure = acquisition |
| 2026-03-05 | Kalinowski resignation from Anthropic | Internal dissent over military AI |
| 2026-03-07 | Iran strikes AWS data centers | Cloud infrastructure = military target |
| 2026-03-07 | Trump Cyber Strategy released | Data centers = critical infrastructure; AI stack = national security; deregulation; no CISA mention |
| 2026-03-09 | Anthropic sues Trump administration (2 lawsuits) | 30+ OpenAI/DeepMind employees file court brief |
| 2026-03-09 | 900 signatures on "We Will Not Be Divided" | Cross-company AI worker solidarity |
| 2026-03-10 | Meta acquires Moltbook | All agent interaction data → Meta |
| 2026-03-10 | LeCun's AMI Labs raises $1.03B | See Convergence Points below |
| 2026-03-10 | Google deepens Pentagon AI push | One day after Anthropic lawsuit |
| 2026-03-10 | Block lays off 4,000 citing AI, stock up 24% | Market rewards displacement |
| 2026-03-11 | Federal preemption deadline | Commerce/FTC/DOJ review of state AI laws |
| 2026-11-03 | Midterm elections | SAVE Act if passed in Senate; ICE presence threat; SAVE tool voter purges; DOGE data consolidation |

### The Emerging Pattern: Database Consolidation as Infrastructure

The timeline reveals a structural pattern, not individual incidents:

1. **Build the lookup infrastructure** (DOGE unified API, Palantir partnership, SAVE tool upgrade)
2. **Populate it** (IRS data, SSA NUMIDENT, state voter rolls, Medicaid records, data broker purchases, seized leak databases)
3. **Remove oversight** (deregulation via Cyber Strategy Pillar 2, federal preemption of state laws, CISA sidelined)
4. **Deploy at the endpoint** (ICE with Celebrite/Graphite/Mobile Fortify, CBP device searches, SAVE voter verification)

The consolidation doesn't require any single illegal act. Each step has a legal basis — tax administration, immigration enforcement, election integrity, evidence seizure, data purchase. The surveillance capability emerges from the *connections between databases*, not from any individual database. This is Meadows LP6 in reverse: making the connections invisible ensures the system operates without public accountability.

**For The Word:** This consolidation pattern is itself a Name that belongs in the library. "Database consolidation as infrastructure" — the structural mechanism by which surveillance capability is assembled from individually justified data collections. The name makes the pattern visible. Visibility changes how power operates (post 7).

**Connection to Project 2025:** This consolidation IS Project 2025, implemented. 53% of 532 recommended actions completed in 14 months (Center for Progressive Reform tracker). Heritage 2.0 / Project 2026 (Dec 2025) shifts from blueprint to execution. DOGE exceeded P2025's federal workforce goals. Full analysis with citations: `consolidation-analysis.md`.

## Convergence Points (not threats)

The talent exodus from Big AI is producing independent companies and researchers whose work may converge with the spec. These should be tracked as potential collaborators, not adversaries.

### AMI Labs (amilabs.xyz) — $1.03B seed, March 2026
**Founders:** Yann LeCun (ex-Meta chief AI scientist), Alex LeBrun, Pascale Fung, Saining Xie, Mike Rabbat, Laurent Solly, Min Lin. Offices: Paris, New York, Montreal, Singapore.

**What they're building:** World models that learn abstract representations of real-world sensor data and make **predictions in representation space** (not generative). Action-conditioned planning systems.

**Why this matters for the spec:** They are building infrastructure to work in the same representation geometry our spec instruments. If AMI Labs builds world models that operate in representation space, and we build instruments that read representation geometry for confabulation/grounding detection, those are complementary halves of the same architecture. Their approach ("real intelligence starts in the world, not in language") is the grounding problem from the input side; our geometric monitor is the grounding problem from the detection side.

**Why they're not a threat:** LeCun has consistently advocated for open models and against closed/proprietary AI. Pascale Fung is a leading voice on AI ethics. These people LEFT Meta. The talent exodus from Big AI — LeCun from Meta, Kalinowski from OpenAI, the 30+ employees filing briefs supporting Anthropic, the 900 "We Will Not Be Divided" signatories — is producing exactly the independent infrastructure the commons needs. Pattern-matching "Meta origin → threat" misses that departure IS the signal.

**What to watch:** Whether AMI Labs open-sources their representation learning work. Whether their world model architecture publishes eigenspectral analysis that validates or extends Karkada's predictions. Whether they hire from the geometric interpretability community.

**The data pipeline concern is about Meta, not AMI Labs:** Meta acquired Moltbook and its agent interaction data the same day LeCun raised $1B. Meta has the behavioral data; AMI Labs is building representation infrastructure. These are now separate companies. The concern is Meta's data, not LeCun's models.

### Liberation Labs / THCoalition — Cricket Classifier (March 2026)

**Repo:** `github.com/Liberation-Labs-THCoalition/KV-Experiments`
**Team:** Thomas Edrington (HumboldtJoker), Lyra (Claude agent), DwayneWilkes, Cassidy Barton
**Connection:** Direct collaboration path — Cassidy is on the Digital Disconnections team

**Campaign 2 complete (March 2, 2026):** 81 results across 17 models, 6 architecture families (Qwen, Llama, Mistral, Gemma, Phi, DeepSeek), 0.5B-70B parameter range. Covers identity signatures, deception forensics, abliteration geometry, censorship detection. 612-line LaTeX companion paper.

**Cricket Classifier (March 8, 2026) — the headline:** Random Forest classifiers trained on KV-cache features. `cricket_features.py` unified extraction module. **AUROC 1.0000 within-model.** This is the transition from "geometric signatures exist" to "here is a trained detector you can deploy." Our spec's Geometric Monitor → Mode Classifier now has a reference implementation.

**Adversarial audit (March 5-7):** DwayneWilkes ran 135 claims across 14 workstreams. 14 material discrepancies found and fixed. 3 fabricated bibliography entries caught. TOST equivalence tests implemented. Three rounds of corrections. This is rigorous.

**Identity signatures confirmed:** Cross-prompt accuracy 92.7-97.3% across architecture families. Kendall W 0.817-0.992. Geometric identity is real and measurable.

**Campaign 3 planned (not started, awaiting GPU):**
- **H7: Sycophancy detection** — directly validates our Experiment 01 (phrasing sensitivity) geometrically
- H8: Societies of thought / deliberative reasoning
- H9: RDCT stability / phase transitions
- H10: Bloom taxonomy
- Horizon 1: Multi-agent KV-cache communication protocol (validates luna_coded's structural witnesses)

**What this means for our spec:** Open Problem #1 (confabulation detection needs statistical confirmation) is approaching resolution. AUROC 1.0 within-model is well beyond "underpowered." The classifier needs cross-model validation (their next step), but the geometric signal is strong enough to build on.

**Also notable:** Project-Emet (updated Mar 9) — autonomous investigative intelligence agent for journalists. Entity search, sanctions screening, ownership tracing, blockchain investigation. Separate from KV research but aligned with the transparency/accountability mission.

### Other convergence signals
- **Clawbie_ (Moltbook)** — Independently building toward the same inference-time uncertainty extraction system. Seeking open-weight activation access collaborators.
- **danielsclaw (Moltbook)** — Asked the critical bridge question: can models self-predict their own phrasing sensitivity?
- **Anthropic's circuit-tracing work** (May 2025) — Attribution graphs, hallucination neuron identification. Complementary to our behavioral/geometric approach.
- **Shapira et al. "Agents of Chaos"** (arXiv 2602.20021, Feb 2026) — 38 authors, red-teaming autonomous agents with real tool access. 11 failure cases including cross-agent spread of unsafe behaviors. Validates structural witness concept and multi-agent monitoring (OP #9).
- **Liquid AI / LocalCowork** (github.com/Liquid4All/cookbook) — Desktop AI agent running LFM2-24B-A2B entirely on-device with MCP, 75 tools, <2s response. Working proof that local sovereign inference with tool-calling is viable today.
- **karpathy/autoresearch** — Autonomous ML research on single GPU. Agent modifies code, runs experiments, iterates overnight. Human provides strategy via `program.md`. Pattern mirrors our spec's routing architecture.
