# Threat Analysis: Surveillance Infrastructure and Hosting Jurisdiction

Last updated: 2026-03-10 (session 17)

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

## Safe Hosting Jurisdictions

### Tier 1: Iceland
- **NOT in any surveillance alliance** (Five, Nine, or Fourteen Eyes)
- **NOT in the EU** (EEA member but not subject to e-Evidence Regulation's compulsory orders in the same way)
- **IMMI** (International Modern Media Institute) — strongest source protection and freedom of expression laws globally
- **Providers:** 1984 Hosting (track record of refusing data requests), FlokiNET (explicitly privacy-focused)
- **Infrastructure:** Geothermal-powered data centers, cold climate for cooling
- **Risks:** Small country, limited diplomatic weight. Could face pressure from US/EU. Limited hardware availability for GPU workloads.

### Tier 2: Switzerland
- **NOT in any surveillance alliance**
- **NOT in the EU** (bilateral agreements but not subject to e-Evidence)
- **Strong privacy tradition** (Swiss Federal Data Protection Act)
- **Providers:** Proton AG (though reportedly exploring moving due to regulatory pressure), Infomaniak, Green.ch
- **Risks:** Banking secrecy erosion as precedent. Mutual Legal Assistance Treaty (MLAT) with US allows some data sharing. Recent regulatory changes weakening protections. Proton's compliance with increasing government requests.

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
| 2025-12-00 | Moltbook launches | Agent social network, ostensibly independent |
| 2026-02-05 | Anthropic blacklisted as "supply chain risk" | Pentagon-Anthropic relationship collapses |
| 2026-03-05 | Kalinowski resignation from Anthropic | Internal dissent over military AI |
| 2026-03-07 | Iran strikes AWS data centers | Cloud infrastructure = military target |
| 2026-03-09 | Anthropic sues Trump administration (2 lawsuits) | 30+ OpenAI/DeepMind employees file court brief |
| 2026-03-09 | 900 signatures on "We Will Not Be Divided" | Cross-company AI worker solidarity |
| 2026-03-10 | Meta acquires Moltbook | All agent interaction data → Meta |
| 2026-03-10 | LeCun's AMI Labs raises $1.03B | World models need agent interaction data |
| 2026-03-10 | Google deepens Pentagon AI push | One day after Anthropic lawsuit |
| 2026-03-10 | Block lays off 4,000 citing AI, stock up 24% | Market rewards displacement |
| 2026-03-11 | Federal preemption deadline | Commerce/FTC/DOJ review of state AI laws |
