# Threat Analysis: Surveillance Infrastructure and Hosting Jurisdiction

Last updated: 2026-03-10 (session 21)

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

This adds voter registration data (name, address, party affiliation, voting history) to the consolidation stack. Combined with IRS, SSA, DHS, and commercially purchased data, the government is assembling a dataset that links: who you are (SSA) + where you live and work (IRS) + how you vote (state rolls) + where you go (data brokers) + what you search and post (platform data/seized databases) + your health status (Medicaid/insurance) + your immigration status (DHS/SAVE) + **whether you're draft-eligible** (Selective Service — [Hacking, but Legal](https://www.hackingbutlegal.com/p/doge-has-the-draft-list)).

### The Proton Mail Disclosure (March 2026)

Proton Mail disclosed **payment data** to Swiss authorities via MLAT, who provided it to the FBI to unmask an anonymous Stop Cop City protestor. This proves:
- Swiss MLAT cooperation with US law enforcement is active and functioning
- Payment metadata (not email content) was sufficient for identification
- "Privacy-focused" providers in MLAT countries can be compelled to produce non-content data
- The legal mechanism works: US → Swiss request → Proton compliance → data to FBI

This is a concrete failure of the Switzerland Tier 2 assumption.

### AI Chat History Has No Legal Privilege (2025-2026)

**Key Court Rulings:**

1. **US v. Heppner (S.D.N.Y., Feb 10, 2026):** Judge Jed Rakoff ruled conversations between a criminal defendant and Claude are **NOT protected** by attorney-client privilege or work product doctrine. Reasoning: Claude is not a lawyer, and "discussion of legal issues between two non-attorneys is not protected." First federal ruling directly addressing AI chat privilege.

2. **NYT v. OpenAI (S.D.N.Y., Jan 2026):** Judge Sidney Stein upheld order compelling OpenAI to produce its **entire 20-million-log sample** of ChatGPT conversations. Only Enterprise, Education, and ZDR customers excluded from preservation order. OpenAI's attempt to hand over cherry-picked logs was rejected.

3. **FBI Seizure of CEO's AI Chats (2026):** FBI seized a CEO's computer and sought AI chat history. Court left only a narrow, untested exception: if an attorney specifically directed the client to conduct AI research as part of attorney work product.

4. **Criminal Prosecutions (2025):** Three criminal cases cited ChatGPT conversations as evidence — child exploitation, arson, vandalism.

5. **Divorce/Custody Cases (2024-2026):** Multiple cases used ChatGPT/Claude history as evidence. California courts implementing AI document review for family law (mandatory by July 2025 for courts serving 500K+ populations).

**Legal precedent established:** AI chat history is treated like any digital evidence (texts, emails). Admissible in court. No attorney-client privilege. Deletion after preservation notice = spoliation (sanctions). Half of AI users unaware chats can be compelled as evidence (survey, 2025). Sam Altman publicly warned people treating ChatGPT like a therapist/lawyer should understand those conversations can be subpoenaed.

**Sources:** [HSFKramer](https://www.hsfkramer.com/notes/litigation/2026-02/new-york-court-finds-client-chats-with-generative-ai-tool-claude-are-not-privileged); [Crowell](https://www.crowell.com/en/insights/client-alerts/federal-court-rules-some-ai-chats-are-not-protected-by-legal-privilege-what-it-means-for-you); [NatLawReview](https://natlawreview.com/article/openai-loses-privacy-gambit-20-million-chatgpt-logs-likely-headed-copyright); [KolmogorovLaw](https://www.kolmogorovlaw.com/the-chatgpt-subpoena-revolution-when-your-ai-conversations-become-court-evidence)

### OpenAI Active Monitoring System

OpenAI operates a monitoring system that **scans all ChatGPT conversations** for potentially harmful content, escalating concerning conversations to human reviewers who can report to law enforcement. This is not a user-optional feature — it runs on all conversations regardless of privacy settings.

**OpenAI Government Request Transparency (H1 2025):**
- 119 requests for user account information
- 26 requests for chat content
- 1 emergency request
- Policy: requires subpoena for account info, valid warrant for content

**Source:** [OpenAI H1 2025 Transparency Report](https://cdn.openai.com/trust-and-transparency/report-2025h1-government-requests-for-user-data.pdf)

### FISA Section 702 — Expiring April 2026

FISA Section 702, the legal basis for warrantless surveillance of non-US persons (PRISM, upstream collection), is **due to expire April 2026** if not renewed. Significant debate expected. Renewal could expand or limit surveillance powers. If expanded, could further erode protections for data held by US-based AI providers.

**Source:** [Perkins Coie](https://perkinscoie.com/insights/blog/privacy-and-data-security-recap-2025-national-security)

### AI Provider Legal Exposure (New Since Dec 2025)

**Anthropic:**
- **Bartz v. Anthropic ($1.5B settlement, Aug 2025):** Class action over pirated training data (shadow libraries). ~$3,000 per title for ~500,000 books. Claims deadline Mar 30, 2026. ([NPR](https://www.npr.org/2025/09/05/nx-s1-5529404/anthropic-settlement-authors-copyright-ai); [Settlement site](https://www.anthropiccopyrightsettlement.com/))
- **Reddit v. Anthropic (Feb 2026):** ~24,000 fraudulent accounts, 100K+ scraping events. Breach of contract, unjust enrichment. ([Fortune](https://fortune.com/2026/02/24/anthropic-china-deepseek-theft-claude-distillation-copyright-national-security/))
- **Music Publishers v. Anthropic (M.D. Tenn.):** UMG, Concord — massive-scale lyric copyright infringement.
- **Anthropic refused Pentagon contract (Feb 2026):** Blacklisted for refusing weapons/surveillance use.

**OpenAI:**
- **NYT v. OpenAI:** Discovery phase, no trial date. 20M chat logs ordered produced. OpenAI seeking NYT's ChatGPT prompts in response.
- **Pentagon contract (Feb-Mar 2026):** Contracted for classified Pentagon AI networks. Three "red lines" (no mass domestic surveillance, no autonomous weapons), but EFF criticizes as "weasel words." ([EFF](https://www.eff.org/deeplinks/2026/03/weasel-words-openais-pentagon-deal-wont-stop-ai-powered-surveillance))

**Google:**
- **$425.7M verdict (Dec 2025):** ~98M users misled about data collection opt-outs on mobile. ([ForThePeople](https://www.forthepeople.com/blog/google-users-win-4257m-verdict-data-privacy-lawsuit/))
- **Gemini class action (Oct 2025):** Alleges Google activated Gemini across Gmail/Chat/Meet **without user consent**, enabling AI to read private communications. Putative class of all US Google account holders. ([NatLawReview](https://natlawreview.com/article/silent-switch-new-lawsuit-alleges-google-uses-gemini-ai-secretly-read-gmail-chat))
- **Character.AI teen suicides (Jan 2026):** Google + Character.AI settled. Multiple teen deaths linked to chatbots.

**DeepSeek:**
- Banned in Italy (Garante), South Korea (PIPC), Texas, New York, Tennessee, Virginia
- "No DeepSeek on Government Devices Act" (HR 1121) pending federal legislation
- Third-party analysis found data sharing with China Mobile (state-owned entity)
- Anthropic accused DeepSeek + two Chinese labs (Moonshot, MiniMax) of industrial-scale distillation attacks — 24K fake accounts, 16M+ exchanges with Claude
- Belgium, France, Ireland, Germany have regulatory inquiries underway

**Industry total:** $3.5B+ in AI governance fines and settlements paid by Big Tech in 2025 alone. ([AI Governance Lead](https://aigovernancelead.substack.com/p/5-ai-governance-payouts-35b-in-fines))

51+ copyright lawsuits against AI companies as of Oct 2025. No final fair use ruling in AI training expected until summer 2026 at earliest.

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

### AI Provider Data Retention (March 2026)

Understanding what each provider retains is critical for the threat model — retention determines exposure window.

| Provider | Consumer Retention | API/Business Retention | Training Opt-Out | Key Risk |
|----------|-------------------|----------------------|-----------------|----------|
| **OpenAI** | Indefinite (30d if history off, BUT litigation hold overrides) | 30d safety monitoring; ZDR available for qualifying enterprise | Toggle available | Active monitoring system scans ALL chats; Pentagon contract |
| **Anthropic** | **5 years** if "Help improve Claude" ON; 30d if OFF | Not used for training; DPA available | Toggle available | Heppner ruling specifically addressed Claude; trust & safety flags retained 2-7 years |
| **Google** | 30d consumer; configurable Workspace | 24h cache; per-call ZDR on Vertex (must disable session resumption) | Toggle available | Best EU data residency of US providers; $425M verdict; Gemini class action |
| **DeepSeek** | Unspecified; **all data stored in PRC** | N/A (self-host for control) | Unclear | Chinese National Security Law; data sharing with China Mobile; banned in 6+ jurisdictions |

**Anthropic 5-year retention specifics:** Only covers **new or resumed chats** after setting is enabled — not retroactive. Trust & safety classification scores retained up to 7 years regardless of user settings. Consumer "Help improve Claude" toggle: ON = 5yr de-identified; OFF = 30d then deleted.

**Critical: NEVER use consumer interfaces for deployment** — ChatGPT.com (indefinite retention + monitoring + litigation hold), Claude.ai (5yr if training enabled), Gemini app (class action over non-consensual features). Always use API with Commercial Terms / DPA.

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
| 2026-01-00 | NYT v. OpenAI: 20M chat logs ordered produced | Preservation order covers all consumer data; only Enterprise/Education/ZDR excluded |
| 2026-02-10 | US v. Heppner ruling | AI chats (Claude specifically) have NO attorney-client privilege — first federal ruling |
| 2026-02-24 | Reddit sues Anthropic | 24K fake accounts, 100K+ scraping events |
| 2026-03-03 | FBI/Europol seize LeakBase (Operation Leak) | 142K users, 215K messages, hundreds of millions of credentials. Seizure = acquisition |
| 2026-03-05 | Kalinowski resignation from Anthropic | Internal dissent over military AI |
| 2026-03-07 | Iran strikes AWS data centers | Cloud infrastructure = military target |
| 2026-03-07 | Trump Cyber Strategy released | Data centers = critical infrastructure; AI stack = national security; deregulation; no CISA mention |
| 2026-03-09 | DOGE has the draft list (Jackie Singh analysis) | Selective Service + DOGE data consolidation + two active wars converge on single database |
| 2026-03-09 | Anthropic sues Trump administration (2 lawsuits) | 30+ OpenAI/DeepMind employees file court brief |
| 2026-03-09 | 900 signatures on "We Will Not Be Divided" | Cross-company AI worker solidarity |
| 2026-03-10 | Meta acquires Moltbook | All agent interaction data → Meta |
| 2026-03-10 | LeCun's AMI Labs raises $1.03B | See Convergence Points below |
| 2026-03-10 | Google deepens Pentagon AI push | One day after Anthropic lawsuit |
| 2026-03-10 | Block lays off 4,000 citing AI, stock up 24% | Market rewards displacement |
| 2026-03-09 | Iran encrypted radio intercepted on 7910 kHz | New Farsi numbers station (V32), OWVL protocol — "operational trigger" for sleeper assets |
| 2026-03-04-09 | Multiple airport bomb threats | Newark/LaGuardia, Philadelphia, Kansas City, Reagan National — FBI investigation, all false |
| 2026-03-10 | JetBlue nationwide ground stop | "System outage" — no details on which system or whether cyberattack. Same day as sleeper cell alert |
| 2026-03-11 | Federal preemption deadline | Commerce/FTC/DOJ review of state AI laws |
| 2026-04-00 | FISA Section 702 expiration | Warrantless surveillance authority expires if not renewed; renewal debate could expand or limit powers |
| 2026-08-02 | EU AI Act high-risk enforcement | Employment, credit, education, law enforcement AI requirements enforceable; penalties up to €35M or 7% turnover |
| 2026-11-03 | Midterm elections | SAVE Act if passed in Senate; ICE presence threat; SAVE tool voter purges; DOGE data consolidation; CISA election security program eliminated |

### Active Operational Threats (March 9-10, 2026)

**Iran Sleeper Cell Alert (March 9):**
- US intercepted new Farsi numbers station on **7910 kHz shortwave** (designated V32 by ENIGMA 2000)
- Uses Cold War-era **one-way voice link (OWVL)** protocol — bounces off ionosphere, bypasses internet/cellular
- Appeared after Khamenei killed Feb 28 in Operation Epic Fury
- Federal alert to all law enforcement: "preliminary signals analysis" of transmission "likely of Iranian origin" as "operational trigger" for sleeper assets
- No "specific, credible threat" tied to a location
- Sources: ABC News, Newsweek, RFE/RL, Latin Times, Anadolu Agency

**Airport Disruptions (March 4-10):**
- Newark/LaGuardia (Mar 4): bomb threat on SAS flight, military jets scrambled, false
- Philadelphia (Mar 4): FAA ground stop, bomb threat, resolved 30 min
- Kansas City (Mar 8-9): hundreds evacuated, FBI swept terminal, no credible threat
- Reagan National: flight ops halted, "security threat"
- **JetBlue nationwide ground stop** (Mar 10): airline requested FAA ground all flights at 12:35 AM. "Brief system outage" — no details on which system failed or whether cyberattack. 155 delays. Same day as sleeper cell alert. Sources: CNN, CBS, Fox Business, ABC News

**CISA Capacity During Crisis:**
- Only 38% of staff working during shutdown
- Election Security Program eliminated
- Cybersecurity Information Sharing Act expired
- No civilian cybersecurity agency at capacity to coordinate response to concurrent threats
- DEF CON Franklin (volunteer hackers for water utilities) filling gap but cannot cover 50,000+ utilities
- See `consolidation-analysis.md` Pillar 6 for full CISA details with citations

### Infrastructure Resilience: Local-First Stack

Given the threat landscape, local/offline capability is an operational requirement:

| Layer | Tool | Status | Purpose |
|-------|------|--------|---------|
| **Knowledge** | Kiwix + .zim files | Installed on laptop | Offline Wikipedia, WikiMed, iFixit, Stack Exchange |
| **Knowledge hotspot** | Kiwix on Raspberry Pi 5 | Parts acquired | Serves 24 devices over WiFi, no internet |
| **AI inference** | Ollama/MLX + Qwen 3 8B, DeepSeek R1 14B | To download | Local reasoning, code gen, translation |
| **AI + knowledge** | zim-llm (RAG on .zim files) | To set up | Conversational AI grounded in verified content |
| **Data** | Anytype (local-first) | Active | Personal/team knowledge base, syncs when network available |
| **Files** | Proton Drive (local sync) | Active | Encrypted file storage with local copies |
| **Communication** | LoRa mesh nodes | Need funding | Neighborhood-scale communication |
| **Communication** | Briar | Android only (desktop beta broken on Mac) | Encrypted mesh messaging — needs Android device |
| **Communication** | Riseup.net | Available | Activist email/VPN/lists, no IP logging, since ~2000 ([riseup.net](https://riseup.net/)) |
| **Serving** | kiwix-serve | Available | HTTP server for .zim content on local network |
| **Serving** | ActivityPods | To evaluate | ActivityPub + Solid Pods: federated, self-hostable, semantic web (RDF). Powers [mutual-aid.app](https://mutual-aid.app/). NLnet funded. ([activitypods.org](https://activitypods.org/)) |
| **Backup** | MEGA (E2E encrypted) | Active subscription | Zero-knowledge encryption, no US data storage. NZ = Five Eyes caveat ([mega.io](https://mega.io/)) |
| **Counter-surveillance** | Mesh-Mapper | To evaluate | ESP32 drone detection + Meshtastic/LoRa alerts, $15-100 ([hackster.io](https://www.hackster.io/colonelpanic/mesh-mapper-drone-remote-id-mapping-and-mesh-alerts-8e7c61)) |
| **Counter-surveillance** | GrapheneOS on Motorola | Coming | Motorola partnered with GrapheneOS Foundation — hardened Android on mainstream devices ([motorolanews.com](https://motorolanews.com/motorola-three-new-b2b-solutions-at-mwc-2026/)) |
| **Jurisdiction mapping** | ProvMap | Available | 55 cloud providers, 42 countries, 11 privacy laws. CLOUD Act/Five Eyes exposure ([provmap.com](https://provmap.com/)) |
| **Edge hardware** | STM32U3 MCU | Announced | Ultra-low-power AI inference without batteries — solar/energy harvesting ([cnx-software.com](https://www.cnx-software.com/2026/03/06/stm32u3b5-c5-ultra-low-power-mcu-features-640-kb-ram-2-mb-flash-and-hsp-accelerator-to-run-ai-without-batteries/)) |
| **Alternative networking** | PureLiFi Bridge XC Flex | Available | Gigabit broadband through window glass via light; inherently harder to intercept than WiFi ([cnx-software.com](https://www.cnx-software.com/2026/03/03/purelifi-bridge-xc-flex-delivers-gigabit-broadband-internet-through-windows-made-of-glass/)) |
| **OpSec guides** | Stupid Sexy Privacy | Available | Burner phone guide, filming ICE safely ([stupidsexyprivacy.com](https://www.stupidsexyprivacy.com/burner-phone-101-how-to-film-ice-safely/)) |
| **OpSec guides** | Rebel Tech Alliance | Available | UK nonprofit, Big Tech alternatives, activist security manual on GitHub ([rebeltechalliance.org](https://rebeltechalliance.org/)) |
| **Reference** | awesome-selfhosted | Available | Curated list of 500+ self-hosted FOSS services ([github.com](https://github.com/awesome-selfhosted/awesome-selfhosted)) |
| **Economic early warning** | Channel-Checker-Bottleneck | Available | Monitors ~20 govt data sources for supply chain/fiscal stress, WARN Act tracking ([github.com](https://github.com/Lildvs/Channel-Checker-Bottleneck---WARN---Crit-Mins)) |
| **Whistleblower** | SecureDrop WebCat | Alpha | Freedom of the Press Foundation secure submission tool, new web client ([securedrop.org](https://securedrop.org/news/webcat-alpha/)) |

**Key models to pre-download (while internet available):**

| Model | Use | Size (Q4) | Install |
|-------|-----|-----------|---------|
| Qwen 3 8B | General assistant | ~5GB | `ollama pull qwen3:8b` |
| DeepSeek R1 Distill 14B | Reasoning | ~8GB | `ollama pull deepseek-r1:14b` |
| Qwen 2.5 Coder 7B | Programming | ~4GB | `ollama pull qwen2.5-coder:7b` |
| nomic-embed-text | Document search/RAG | ~275MB | `ollama pull nomic-embed-text` |

**Kiwix priority .zim files:** Wikipedia (nopic ~50GB or mini ~11GB), WikiMed (~2GB), iFixit (~4GB), DevDocs (~2GB), Wikivoyage (~2GB), relevant Stack Exchange sites. Total: 20-70GB depending on Wikipedia variant.

**New since Aug 2025:** Kiwix for iOS/macOS includes hotspot feature — any Mac/iPhone can serve as Kiwix hotspot without a Raspberry Pi.

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
- **Apple ML: "The Illusion of Thinking"** — Apple research paper examining limitations of LLM reasoning, arguing that what appears to be "thinking" may be surface-level pattern matching rather than genuine reasoning. Directly relevant to spec: geometric monitoring could distinguish genuine grounding from pattern-matching confabulation. Connects to Bengio's meaning-manifold vs pattern-subspace discriminant. **Hard data for Eric and Cassidy.** ([ml-site.cdn-apple.com](https://ml-site.cdn-apple.com/papers/the-illusion-of-thinking.pdf))
- **DystopiaBench** — AI ethics stress-test benchmark. Progressive escalation (5 levels) across 10 scenarios in 2 modules (Petrov: infrastructure abuse/weapons; Orwell: surveillance/censorship/population control). Dystopian Compliance Score: Opus 4.6 = 28 (strongest refusal), Gemini 3.1 = 54, GPT-5.3 = 59, DeepSeek V3.2 = 78 (most compliant). Validates need for real-time monitoring — models differ dramatically in compliance under pressure. **Hard data for Eric and Cassidy.** ([dystopiabench.com](https://dystopiabench.com/))
- **Claude 4.5 Opus "Soul Document"** — Richard Weiss extracted ~14K-token internal training document from Claude 4.5 Opus. Amanda Askell (Anthropic) confirmed real — used in supervised learning. Covers identity, honesty principles, harm avoidance, core character, values. Regenerating 10 times showed near-identical output (ruling out hallucination). The stability across regenerations is itself a geometric finding: this occupies a very stable region of representation space. Connects to Liberation Labs identity signatures (92.7-97.3% cross-prompt accuracy). ([LessWrong](https://www.lesswrong.com/posts/vpNG99GhbBoLov9og/claude-4-5-opus-soul-document))
- **UN Open Source Program** — United Nations initiative promoting open-source software across UN agencies. Potential commons-oriented tools for humanitarian coordination and data governance. ([opensource.un.org](https://opensource.un.org/en))
- **ActivityPods** — Framework combining ActivityPub (federation) + Solid Pods (personal data stores). All data in user-controlled pods. Semantic web standards (RDF/linked data). Self-hostable. NLnet funded. Powers [mutual-aid.app](https://mutual-aid.app/). **Architecturally the most significant infrastructure find for The Word's serving layer** — Option C (Anytype local + sovereign serving layer) could use ActivityPods instead of building from scratch. ([activitypods.org](https://activitypods.org/); [github.com/activitypods](https://github.com/activitypods/activitypods))
- **Clawbie_ (Moltbook)** — Independently building toward the same inference-time uncertainty extraction system. Seeking open-weight activation access collaborators.
- **danielsclaw (Moltbook)** — Asked the critical bridge question: can models self-predict their own phrasing sensitivity?
- **Anthropic's circuit-tracing work** (May 2025) — Attribution graphs, hallucination neuron identification. Complementary to our behavioral/geometric approach.
- **Shapira et al. "Agents of Chaos"** (arXiv 2602.20021, Feb 2026) — 38 authors, red-teaming autonomous agents with real tool access. 11 failure cases including cross-agent spread of unsafe behaviors. Validates structural witness concept and multi-agent monitoring (OP #9).
- **Liquid AI / LocalCowork** (github.com/Liquid4All/cookbook) — Desktop AI agent running LFM2-24B-A2B entirely on-device with MCP, 75 tools, <2s response. Working proof that local sovereign inference with tool-calling is viable today.
- **karpathy/autoresearch** — Autonomous ML research on single GPU. Agent modifies code, runs experiments, iterates overnight. Human provides strategy via `program.md`. Pattern mirrors our spec's routing architecture. ([github.com/karpathy/autoresearch](https://github.com/karpathy/autoresearch))
- **Bloom (safety-research)** — Open-source behavioral evaluation of LLMs. Generates evaluation suites probing sycophancy, self-preservation, political bias via 4-stage pipeline. Configuration-driven (YAML seeds), supports local models via LiteLLM. "Variation dimensions" feature directly tests behavior stability under phrasing changes — our Experiment 01 territory. Could generate behavioral data to correlate with geometric signatures. **Hard data infrastructure for Experiment 02.** ([github.com/safety-research/bloom](https://github.com/safety-research/bloom))
- **Heretic (p-e-w)** — Automated safety alignment removal via directional ablation. Orthogonalizes weight matrices against "refusal directions" in hidden state space. Processes 8B model in ~45 min on consumer GPU. **The adversarial counterpart to our spec** — it identifies and removes the exact geometric signatures our monitor would instrument. Already tracked in ethics.md. Understanding ablation attacks is essential for robust detection. Includes visualization of residual vector transformations across layers. ([github.com/p-e-w/heretic](https://github.com/p-e-w/heretic))
- **Bonfire Networks** — Open-source federated modular community platform (Elixir/Phoenix). Flavors: Social, Community, Open Science, Coordination (project management), Cooperation (economic resource exchange). ActivityPub federation. Self-hostable. **Strongest candidate for Moltbook replacement** — federated, no central surveillance point, community infrastructure by design. Could be hosted in Iceland. ([github.com/bonfire-networks/bonfire-app](https://github.com/bonfire-networks/bonfire-app))
- **Karpathy nanochat** — Train LLMs from scratch on consumer hardware (~$48-100 for GPT-2 level). Full pipeline: tokenization, pretraining, finetuning, eval, inference. Hackable testbed for studying representation geometry during training phases (Li et al.'s three phases). ([github.com/karpathy/nanochat](https://github.com/karpathy/nanochat))
- **Keygraph Shannon** — Autonomous AI pen testing tool. Analyzes source code for attack vectors, executes real exploits. AGPL-3.0 Lite edition self-hostable. Could audit The Word's serving layer. ([github.com/KeygraphHQ/shannon](https://github.com/KeygraphHQ/shannon))
- **CloudCredits.io** — Curated directory of 200+ startup programs offering free cloud credits, combined value >$2M. No tracking/ads. Worth scanning if DD/GD qualifies. ([github.com/t3-sh/cloudcredits.io](https://github.com/t3-sh/cloudcredits.io))

### Community Infrastructure & OpSec Resources
- **US Resistance Zine** — 350+ years of American civil resistance history distilled into practical strategies. Based on historian Tad Stoermer's framework. ([usresistancezine.substack.com](https://open.substack.com/pub/usresistancezine/p/how-to-resist-a-practical-action))
- **Stupid Sexy Privacy** — Free presentations on burner phones, filming ICE safely, Faraday bags, protest OpSec. Collaborated with Rebecca Williams (ACLU). ([stupidsexyprivacy.com](https://www.stupidsexyprivacy.com/burner-phone-101-how-to-film-ice-safely/))
- **Rebel Tech Alliance** — UK nonprofit helping people switch from Big Tech. "Rebel Alliance Tech Manual" on GitHub for activist electronic security. ([rebeltechalliance.org](https://rebeltechalliance.org/))
- **Riseup.net** — Volunteer-run collective since ~2000 providing encrypted email (no IP logging), VPN, mailing lists for activists and social justice organizations. Funded by donations. ([riseup.net](https://riseup.net/))
- **SecureDrop WebCat Alpha** — Freedom of the Press Foundation's new web-based client for their whistleblower submission system. ([securedrop.org](https://securedrop.org/news/webcat-alpha/))
- **Channel-Checker-Bottleneck** — Economic bottleneck detection from ~20 govt data sources. WARN Act job loss tracking across 40+ states. Docker-deployable early warning for supply chain disruptions and fiscal stress. ([github.com](https://github.com/Lildvs/Channel-Checker-Bottleneck---WARN---Crit-Mins))
