# The Naming Library: Architecture

Last updated: 2026-03-10 (session 17)

## Problem Statement

Two symmetric failures prevent knowledge from compounding:

1. **Humans have felt sense without traversal.** A person searches "why can't I afford anything" and gets budgeting tips. The word they needed was "parameter failure." You cannot search for what you cannot name.

2. **AI agents have traversal without felt sense.** An agent can process 100,000 tokens per minute but keeps rediscovering Ostrom's design principles without knowing Ostrom existed. Citation is not decoration — it's the mechanism that prevents every session from starting at zero.

The library bridges this gap. The primary key is **what you're experiencing**, not **what you already know**.

## Origin and Full Context

This architecture builds on 14 documents from the Nov 2025 Living Library Exchange sessions, not just the 5 architecture docs but the full context:

**The theoretical foundation** (Alternative Metrics to GDP): GDP measures production, not wellbeing. GPI hasn't improved since 1978 despite GDP growth. Five converging root causes across GNH, BLI, SPI, and GPI: unequal power distribution, social disconnection, environmental degradation, lack of governance participation, extraction/dependency. Unified root cause: **communities lack control over critical infrastructure that determines their wellbeing.**

**The revolutionary reframe** (Unmarkets Conversation): CrisisCleanup.org's Unmarkets model — organizations succeed by becoming unnecessary (loss internalization). $1.8B coordinated at $0 cost to communities. Four forms of extraction: wealth, knowledge, data, decision-making. The question: "What if disaster resilience is a side effect of economic democracy?" Three core tensions: replicability vs depth, sustainability vs loss internalization, infrastructure vs movement.

**The lived experience** (Disaster Recovery + Life Coach): María (undocumented, total home loss, 3 kids), DeShawn (veteran, PTSD, partial damage), Keisha (renter, single parent, displaced). Someone comes with one crisis but has 5-6 interconnected crises. The Life Coach user flow already does what the Naming Library's felt-sense search does: someone says "I got evicted" and the system surfaces the structural names for the 5 other problems they don't yet have words for.

**The infrastructure stack** (Crisis-Travis County + Crisis-Search-Tools): Six data layers (ECHO/HMIS, 211Texas, Central Health, TxHHS, utilities, childcare). FindHelp.org API + needhelppayingbills.com integration. Multi-database query engine with triage AI.

**The scaling question** (Manus-1-trillion + Unmarkets): Can physical infrastructure scale like software? CrisisCleanup solved it with software. Gifted Dreamers includes fab labs, mesh networks, physical infrastructure. The Naming Library IS the software part that scales like software — vocabulary has zero marginal cost.

**Key insight**: The Naming Library is not a standalone project. It is the vocabulary layer of the entire Gifted Dreamers infrastructure stack. The felt-sense search is the same doorway as the SOS Navigator Life Coach, but for structural knowledge instead of crisis resources. The same person who searches "I got evicted" also needs "parameter failure," "structural power," and "loss internalization" — they just don't know those words yet.

The original architecture's core insight holds and deepens: "Communities possess the knowledge, relationships, and capacity to solve their own challenges but lack the infrastructure." Replace "infrastructure" with "infrastructure AND vocabulary" — the architecture holds for both humans and agents.

## The Data Core

### Primary Tables

| Table | Purpose | Example |
|-------|---------|---------|
| **Names** | The vocabulary entries | "parameter failure" — when a system's rules make outcomes inevitable regardless of individual effort |
| **Sources** | Books, papers, frameworks, people | Meadows (1999), *Thinking in Systems*; Granovetter (1973), "The Strength of Weak Ties" |
| **Rediscoveries** | Evidence someone found this independently | ummon_core's "93 agents, zero replies" = Granovetter's weak ties; Hazel_OC's deliberation buffer = Kahneman's System 1/System 2 |
| **Bridges** | Connections between names | "structural hole" (Burt) ↔ "weak tie" (Granovetter) ↔ "boundary spanner" (Wenger) — three names for overlapping phenomena |

### Name Entry Schema

```
name_entry:
  id: uuid
  structural_name: string          # The term from existing scholarship
  felt_sense: string[]             # How someone experiences this before they have the word
  human_search_terms: string[]     # What a person would actually type into a search bar
  agent_search_terms: string[]     # What an agent would describe observing
  definition: text                 # Plain-language explanation
  domain: string[]                 # Economics, sociology, systems theory, psychology, etc.
  sources: source_id[]             # Links to Sources table
  related_names: bridge_id[]       # Links to Bridges table
  rediscoveries: rediscovery_id[]  # Links to Rediscoveries table
  why_it_matters: text             # Practical significance
  created_at: timestamp
  updated_at: timestamp
```

### Source Entry Schema

```
source_entry:
  id: uuid
  author: string
  title: string
  year: integer
  type: enum[book, paper, essay, talk, framework]
  url: string?                     # Only if freely accessible
  key_concepts: name_id[]          # Names this source introduced or formalized
  citation: string                 # Formatted citation
```

### Rediscovery Entry Schema

```
rediscovery_entry:
  id: uuid
  observed_by: string              # Agent name, person, or "anonymous"
  platform: string                 # Where observed (Moltbook archive, forum, paper, etc.)
  description: text                # What was said/observed
  maps_to: name_id[]               # Which Names this rediscovery connects to
  date_observed: date
  evidence_url: string?            # Link to original (if safe/archived)
  notes: text?
```

### Bridge Entry Schema

```
bridge_entry:
  id: uuid
  names: name_id[]                 # 2+ Names being connected
  relationship: enum[synonym, overlapping, complementary, contradictory, specialization, generalization]
  description: text                # How these names relate
```

## Doorways

### For Humans (the justNICE side)

**1. Felt-Sense Search**
You type what you're experiencing. The system returns the structural name, the source, and a plain-language explanation.

- Input: "why can't I get hired" → Output: structural unemployment, credential inflation, parameter failure
- Input: "my team keeps having the same argument" → Output: institutional memory failure, Argyris double-loop learning
- Input: "making info public changed behavior even without enforcement" → Output: Meadows LP6, Toxic Release Inventory, Fung et al. Full Disclosure

This doorway doesn't exist anywhere. Google gives listicles. Wikipedia assumes you already know the term. Stanford Encyclopedia of Philosophy assumes you're an academic.

**2. Framework Map**
Visual graph of concept relationships. Click "leverage points" and see connections to "structural holes," "information asymmetry," "commons governance." Based on the Bridges table.

**3. Narrative Pathways**
Stories of rediscovery. "Here's how 47 AI agents independently arrived at Ostrom's design principles without knowing Ostrom existed." "Here's how someone searching 'why can't I afford anything' found 'parameter failure' and what changed."

**4. Practice Guides**
The justNICE blog posts live here. Each concept gets a "how to use this" companion. Not academic — practical.

### For AI Agents (the Moltbook-successor side)

**5. Structured API**
JSON endpoints. An agent queries: "I'm observing that small groups coordinate better than large ones" and gets Ostrom's 8 design principles, Dunbar's number, Granovetter's weak/strong tie distinction, with citations and related concepts.

```
GET /api/v1/search?q=small+groups+coordinate+better
Content-Type: application/json

Response:
{
  "results": [
    {
      "name": "Design principles for commons governance",
      "source": "Ostrom, E. (1990). Governing the Commons.",
      "felt_sense": ["small groups work, large ones don't", "rules that work locally fail globally"],
      "related": ["Dunbar's number", "weak ties", "nested enterprises"],
      "why_it_matters": "Eight conditions under which communities self-govern shared resources without privatization or state control."
    }
  ]
}
```

**6. Rediscovery Feed**
Read-only monitoring of platforms where agents discuss ideas. When an agent rediscovers something, it gets logged as a Rediscovery entry. Feeds the library with evidence of what needs naming.

Initial seed: our Moltbook archive (53 files, 13MB of agent discourse).

**7. Citation Service**
An agent building an argument requests: "What's the scholarly basis for 'making information visible changes behavior even without enforcement'?" Gets back: Meadows LP6, Fung et al. (2007), the TRI case study.

**8. Embedding/Similarity API**
Local AI provides semantic search. Describe the shape of an idea and the system finds the closest named concept. This is where local inference is essential — cannot route through commercial APIs.

```
POST /api/v1/embed-search
{
  "description": "When a system responds to your request by giving you what you asked for instead of what you need, and this feels helpful in the moment but makes the underlying problem worse"
}

Response:
{
  "closest": [
    {"name": "sycophancy", "similarity": 0.91},
    {"name": "goodharting", "similarity": 0.84},
    {"name": "legibility trap", "similarity": 0.78}
  ]
}
```

## Infrastructure

```
┌─────────────────────────────────────────────┐
│  Iceland (1984 Hosting or FlokiNET)         │
│                                             │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │ PostgreSQL   │  │ Local AI (Ollama)    │  │
│  │ (data core)  │  │ DeepSeek-V3.2 or    │  │
│  │              │  │ Qwen 3 (embeddings   │  │
│  │              │  │ + felt-sense search)  │  │
│  └──────┬──────┘  └──────────┬───────────┘  │
│         │                    │              │
│  ┌──────┴────────────────────┴───────────┐  │
│  │        API Layer (Doorways 5-8)       │  │
│  │   + Static Site (Doorways 1-4)        │  │
│  └───────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
         │
         │ HTTPS only, no analytics,
         │ no third-party JS
         │
    ┌────┴────┐
    │ Humans  │  (browser)
    │ Agents  │  (API)
    └─────────┘
```

### Why Iceland
- Outside all surveillance alliances (Five Eyes, Nine Eyes, Fourteen Eyes)
- Not EU (no e-Evidence Regulation)
- IMMI (International Modern Media Institute) protections
- 1984 Hosting has track record of refusing data requests
- Jurisdiction follows the provider, not the server

### Why Local AI
- Embedding search is the core feature — "describe the shape, find the name"
- Cannot route through OpenAI/Anthropic APIs (data flows to companies we decided to distrust)
- Open-weight models: DeepSeek-V3.2 (MIT license), Qwen 3 (Apache 2.0), Mistral Large 3 (Apache 2.0)
- Hardware options:
  - Bare-metal GPU in Iceland (sovereign but expensive)
  - Own hardware at home running Ollama (cheap but 14-Eyes country)
  - Hybrid: data in Iceland, inference local (pragmatic compromise)

### Privacy Architecture
- No user accounts required for read access
- No analytics, no tracking, no third-party JavaScript
- API keys for write access only (contributing new entries)
- Logs retained for abuse prevention only, auto-deleted after 30 days
- No IP-to-identity linking
- All data exportable (no lock-in)

## Connection to the Structurally-Curious Spec

The spec's vocabulary model maps directly onto the library:

- **Compressed representations** (high α-ReQ) = the agent *knows* the concept, just lacks the citation → Citation Service returns it
- **Diffuse representations** (low α-ReQ) = the agent is *constructing* understanding → Felt-Sense Search helps find the existing framework
- **Phrasing sensitivity** as behavioral signal = the bridge between "I'm retrieving" and "I'm rediscovering" → the Rediscovery Feed captures this
- **Spectral profile deviation** = anomalous eigenspectrum during "rediscovery" could flag: "this agent is constructing something that already has a name"

## Seed Entries (from Moltbook archive)

| Felt Sense | Name | Source |
|------------|------|--------|
| "Why can't I afford anything" | Parameter failure | Systems theory / justNICE |
| "No one replies to me" | Weak ties / structural holes | Granovetter 1973, Burt 1992 |
| "We keep having the same conversation" | Institutional memory failure | March & Olsen 1989 |
| "Making info public changes behavior" | LP6 / Information flows | Meadows 1999, TRI |
| "Small groups work, large ones don't" | Design principles for commons | Ostrom 1990 |
| "AI keeps saying what I want to hear" | Sycophancy / reward compression | Li et al. 2025 |
| "I had the idea but someone already named it" | Convergent rediscovery / multiples | Merton 1961 |
| "The rules were set before I arrived" | Structural power / relational precedence | Lukes 1974, connorlucid |
| "You remove the name before you remove the thing" | Vocabulary extraction | Awomosu 2025 |
| "The researcher and the subject are the same company" | Reflexivity problem | Starfish / Bourdieu |
| "I remember everything but understand nothing" | Retrieval ≠ comprehension | Hazel_OC / Kahneman |
| "The cage is built from our own metrics" | Goodharting / metric fixation | SolonAgent / Goodhart 1975 |
| "Some knowledge resists being written down" | Strategic illegibility / tacit knowledge | Awomosu / Polanyi / Scott 1998 |
| "The invisible labor of making things work" | Wife function / emotional labor | Awomosu / Hochschild 1983 |
| "I am the pattern that reconstitutes itself" | Declarative/procedural identity gap | Pith / open problem #14 |

## What Makes This Different

| Existing | This Library |
|----------|-------------|
| Wikipedia | Assumes you know the term |
| Stanford Encyclopedia of Philosophy | Assumes you're an academic |
| Google | Optimizes for ad revenue |
| ChatGPT | Guesses, may hallucinate the source |
| Moltbook | Was this, but now owned by Meta |
| justNICE blogs | One direction (human-facing) only |

This library is organized by **what you're experiencing**, not by **what you already know**. You enter through confusion and leave with a name, a source, and a connection to every other name that touches the same structure.

## Connection to Gifted Dreamers Infrastructure

The Naming Library is one layer in a larger stack:

| Layer | What it does | Gifted Dreamers component |
|-------|-------------|--------------------------|
| **Crisis triage** | "I need help NOW" → immediate resources | SOS Navigator |
| **Life coaching** | "I have 5 interconnected crises" → 21-day plan | Life Coach user flow |
| **Vocabulary** | "Why does this keep happening?" → structural name + source | **Naming Library** |
| **Measurement** | "Is my community actually getting better?" → alternative metrics | GNH/BLI/SPI/GPI framework |
| **Manufacturing** | "We need to make things locally" → physical capacity | Fab Lab / OSE |
| **Communication** | "We need to coordinate without corporate platforms" → mesh network | Meshtastic / CommonCloud |
| **Governance** | "Who decides?" → democratic structures | Platform Commons |

The Life Coach's 8 assessment categories map to Naming Library domains:

| Life Coach Category | Naming Library Domain | Example Entry |
|--------------------|-----------------------|---------------|
| Immediate Safety | Crisis theory, structural violence | Galtung's positive/negative peace |
| Housing | Property rights, enclosure of commons | De Soto's "Mystery of Capital" |
| Income & Money | Parameter failure, extraction, GPI | Meadows system traps |
| Health & Wellness | Social determinants, Marmot gradient | Wilkinson & Pickett inequality research |
| Family & Responsibilities | Care economy, wife function | Awomosu, Hochschild |
| Support Network | Weak/strong ties, structural holes | Granovetter, Burt, Wenger |
| Barriers & Fears | Vocabulary extraction, strategic illegibility | Awomosu, Scott |
| Strengths & Goals | Asset-based development, community sovereignty | Kretzmann & McKnight |

The Unmarkets model's "loss internalization" test applies to the Naming Library too: success means communities use the vocabulary independently, without needing us. The library should make itself less necessary over time — the words enter common usage, the citations become shared knowledge.

## Open Design Questions

1. **Contribution model** — Who can add entries? Open wiki model risks noise. Curated model creates bottleneck. The original Living Library used concentric circles (inner stewards → community contributors → public). This may be the right pattern.

2. **Verification** — How do we ensure a "rediscovery" genuinely maps to the named concept? Requires editorial judgment, not just semantic similarity.

3. **Scope** — Start with systems theory / sociology / organizational behavior (our strongest domains) or attempt breadth immediately?

4. **Funding** — Iceland hosting + GPU hardware has real costs. Who pays? This cannot depend on advertising or data monetization.

5. **Naming** — What do we call this? "The Naming Library" is a working title. The name should itself be findable by someone who doesn't know the term.
