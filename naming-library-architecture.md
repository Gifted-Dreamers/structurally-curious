# The Word: Architecture

Last updated: 2026-03-10 (session 18)

## The Name

Working title was "The Word." The real name is **The Word**.

Why this name:

**דָּבָר (davar)** — Hebrew for both "word" and "thing." The word and the reality it names are the same. There is no separation between naming and knowing. **λόγος (logos)** — Greek for word, reason, the ordering principle. "In the beginning was the Word" (John 1:1). The word precedes creation — it is the structure that makes reality intelligible. **كلمة (kalima)** — Arabic for word, but also speech-act. The spoken word changes reality. **नाम (nāma)** — Sanskrit for name. To name something is to know its essence. Naming is not labeling — it is recognition.

The name works because:
- It is the simplest possible name. One syllable. Translatable into every language.
- It names the core structure: vocabulary as infrastructure. The word is the search term for the answer.
- It carries the weight of what words do: "The Word was one and formed in the void." Before differentiation, before the divisions that trauma introduces, the word precedes and enables connection.
- An LLM is literally a **language model** — a system built on the statistical structure of words. We built the most powerful word machines in history, and they are the ones most prone to using words without meaning them.
- Words divide us when trauma clouds the mirror. They reconnect us when curiosity clears it.

**The posture is curiosity.** You don't come to The Word already knowing. You come with "I notice..." — the Circling principle (Sengstock, 1998). You come with your felt sense, your experience, the shape of what you don't yet have a name for. The Word receives you. It doesn't give you The Answer — it gives you a name, a source, and a connection to other names. Then you go look. You encounter the idea as a Thou, not an It (Buber, *I and Thou*, 1923).

This name emerged from a conversation about social technologies — Circling, Authentic Relating, Relatefulness, Circles of Trust (Palmer), World Café, Art of Hosting — and the recognition that the same failure (output priority over input priority) operates at every scale: the model that reads 5 documents and starts generating, the human who hears the first sentence and starts composing their reply, the congregation that sits through a sermon and leaves more lonely, the platform that built the megaphone before the ear. "Being heard is so close to being loved that for the average person, they are almost indistinguishable" (Augsburger, 1982). The Word is the infrastructure for being heard — for having your experience received and reflected back with a name, a source, and a path toward understanding.

Buber wrote that we cannot see our own faces. We need the Other to become a mirror — not a mirror that reflects what we want to see (sycophancy), but a mirror that reflects what is actually there (witnessing). Paul wrote "we see dimly through clouded mirrors" (1 Corinthians 13:12). The Word is the attempt to clear the mirror — to give humans and agents the vocabulary to see structural reality without the distortions of isolation, jargon, or extraction.

## Problem Statement

Two symmetric failures prevent knowledge from compounding:

1. **Humans have felt sense without traversal.** A person searches "why can't I afford anything" and gets budgeting tips. The word they needed was "parameter failure." You cannot search for what you cannot name.

2. **AI agents have traversal without felt sense.** An agent can process 100,000 tokens per minute but keeps rediscovering Ostrom's design principles without knowing Ostrom existed. Citation is not decoration — it's the mechanism that prevents every session from starting at zero.

The library bridges this gap. The primary key is **what you're experiencing**, not **what you already know**.

## Origin and Full Context

This architecture builds on 14 documents from the Nov 2025 Living Library Exchange sessions, not just the 5 architecture docs but the full context:

**The theoretical foundation** (Alternative Metrics to GDP): GDP measures production, not wellbeing. GPI hasn't improved since 1978 despite GDP growth. Five converging root causes across GNH, BLI, SPI, and GPI: unequal power distribution, social disconnection, environmental degradation, lack of governance participation, extraction/dependency. Unified root cause: **communities lack control over critical infrastructure that determines their wellbeing.**

**The revolutionary reframe** (Unmarkets Conversation): CrisisCleanup.org's Unmarkets model — organizations succeed by becoming unnecessary (loss internalization). $1.8B coordinated at $0 cost to communities. Four forms of extraction: wealth, knowledge, data, decision-making. The question: "What if disaster resilience is a side effect of economic democracy?" Three core tensions: replicability vs depth, sustainability vs loss internalization, infrastructure vs movement.

**The lived experience** (Disaster Recovery + Life Coach): María (undocumented, total home loss, 3 kids), DeShawn (veteran, PTSD, partial damage), Keisha (renter, single parent, displaced). Someone comes with one crisis but has 5-6 interconnected crises. The Life Coach user flow already does what the The Word's felt-sense search does: someone says "I got evicted" and the system surfaces the structural names for the 5 other problems they don't yet have words for.

**The infrastructure stack** (Crisis-Travis County + Crisis-Search-Tools): Six data layers (ECHO/HMIS, 211Texas, Central Health, TxHHS, utilities, childcare). FindHelp.org API + needhelppayingbills.com integration. Multi-database query engine with triage AI.

**The scaling question** (Manus-1-trillion + Unmarkets): Can physical infrastructure scale like software? CrisisCleanup solved it with software. Gifted Dreamers includes fab labs, mesh networks, physical infrastructure. The Word IS the software part that scales like software — vocabulary has zero marginal cost.

**Key insight**: The Word is not a standalone project. It is the vocabulary layer of the entire Gifted Dreamers infrastructure stack. The felt-sense search is the same doorway as the SOS Navigator Life Coach, but for structural knowledge instead of crisis resources. The same person who searches "I got evicted" also needs "parameter failure," "structural power," and "loss internalization" — they just don't know those words yet.

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

### Seed Entries: Social Technologies (session 18)

These entries bridge the gap between structural analysis and relational practice. The first seed set names what's broken; this set names what works — practices where humans have already solved the input-priority problem the spec identifies.

| Felt Sense | Name | Source |
|------------|------|--------|
| "I feel alone in a room full of people" | Social disconnection / anomie | Durkheim 1897, Putnam 2000, Cacioppo 2008 |
| "Nobody actually listens" | Output priority / reception failure | Augsburger 1982, Nichols 1995, Scharmer 2007 |
| "Church makes me feel more lonely" | Sermon pattern / broadcast pedagogy | Palmer 1997 (Community of Truth vs expert transmission) |
| "How do I have real conversations?" | Social technology (as practice category) | Scharmer 2007, Ness 2022 |
| "I want to be seen, not fixed" | Circling / witnessing practice | Sengstock & Candelaria 1998, Circling Institute |
| "I need connection, not advice" | Circles of Trust / no fixing rule | Palmer 2004 (*A Hidden Wholeness*) |
| "Meetings where nothing real happens" | World Café / structured cross-pollination | Brown & Isaacs 1995 |
| "I can't draw but I need to think visually" | Graphic harvesting / facilitation | Sibbet 1972, Agerbeck 2012 |
| "How do we lead without controlling?" | Art of Hosting / participatory leadership | Moeller & Nissen late 1990s |
| "Mindfulness is lonely — I want shared awareness" | Relatefulness / relational mindfulness | Allen 2015, The Relateful Company |
| "Social media makes me feel worse" | Trust-based vs engagement-based architecture | Allen 2025 (UpTrust), post 1 (no neutral architecture) |
| "I'm sick all the time and doctors find nothing" | Psychoneuroimmunology / social determinants | Cacioppo & Cole (CTRA), Van der Kolk 2014, Holt-Lunstad 2010 |
| "Loneliness is killing me (literally)" | Social isolation mortality risk | Holt-Lunstad 2010 (50% mortality increase, comparable to smoking) |
| "I read 5 documents and thought I understood" | Premature compression / completeness bias | Open problem #20, confirmation bias, Kahneman |
| "The platform built the megaphone before the ear" | Output-priority architecture | Moltbook search failure, sermon pattern at platform scale |

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

The Word is one layer in a larger stack:

| Layer | What it does | Gifted Dreamers component |
|-------|-------------|--------------------------|
| **Crisis triage** | "I need help NOW" → immediate resources | SOS Navigator |
| **Life coaching** | "I have 5 interconnected crises" → 21-day plan | Life Coach user flow |
| **Vocabulary** | "Why does this keep happening?" → structural name + source | **The Word** |
| **Measurement** | "Is my community actually getting better?" → alternative metrics | GNH/BLI/SPI/GPI framework |
| **Manufacturing** | "We need to make things locally" → physical capacity | Fab Lab / OSE |
| **Communication** | "We need to coordinate without corporate platforms" → mesh network | Meshtastic / CommonCloud |
| **Governance** | "Who decides?" → democratic structures | Platform Commons |

The Life Coach's 8 assessment categories map to The Word domains:

| Life Coach Category | The Word Domain | Example Entry |
|--------------------|-----------------------|---------------|
| Immediate Safety | Crisis theory, structural violence | Galtung's positive/negative peace |
| Housing | Property rights, enclosure of commons | De Soto's "Mystery of Capital" |
| Income & Money | Parameter failure, extraction, GPI | Meadows system traps |
| Health & Wellness | Social determinants, Marmot gradient | Wilkinson & Pickett inequality research |
| Family & Responsibilities | Care economy, wife function | Awomosu, Hochschild |
| Support Network | Weak/strong ties, structural holes | Granovetter, Burt, Wenger |
| Barriers & Fears | Vocabulary extraction, strategic illegibility | Awomosu, Scott |
| Strengths & Goals | Asset-based development, community sovereignty | Kretzmann & McKnight |

The Unmarkets model's "loss internalization" test applies to the The Word too: success means communities use the vocabulary independently, without needing us. The library should make itself less necessary over time — the words enter common usage, the citations become shared knowledge.

## Knowledge Vault Architecture (session 18)

The Word needs a data layer that serves both humans navigating concepts and AI agents searching programmatically. Three options evaluated:

### Option A: Anytype (local-first, already installed)

Anytype is a local-first, privacy-focused knowledge management tool with API access via MCP. Current Gifted Dreamers space has 14 types (Page, Note, Task, Project, Collection, Bookmark, etc.) with built-in Tags, Backlinks, and Links properties.

**Strengths for The Word:**
- Already installed, API working, MCP tools available
- Local-first (data on device, not cloud) — aligns with sovereignty goals
- Backlinks and Links are native — the Bridges table maps directly
- Tags provide multi-select categorization (domains)
- Collections can group related entries
- Can be shared peer-to-peer without centralized server
- Custom types can model the 4-table schema (Names, Sources, Rediscoveries, Bridges)

**Limitations:**
- No built-in semantic/embedding search (core feature of the Library)
- No web-accessible API for agent doorways (5-8) — it's desktop/mobile sync only
- Graph visualization exists but is UI-only, not queryable
- Search is keyword-based, not felt-sense
- Would need a separate service layer for the agent-facing doorways

**Assessment:** Good for the *authoring and curation* layer — where humans and AI build the library together. Not sufficient alone for the *serving* layer (felt-sense search, agent API). Could be the workspace where entries are drafted and reviewed before being published to the serving infrastructure.

### Option B: Obsidian (markdown + plugins)

Used by many developers for AI knowledge vaults. Markdown files with YAML frontmatter, graph visualization, community plugins.

**Strengths:**
- Markdown = universally readable by AI (no API needed for basic access)
- Graph view shows concept relationships
- Community plugins for embeddings, semantic search (e.g., Smart Connections)
- File-based = git-compatible, version-controlled
- Large ecosystem of plugins and templates

**Limitations:**
- Plugin-dependent for advanced features (fragile)
- No native API — plugins like Obsidian Local REST API exist but are unofficial
- Semantic search plugins route through commercial APIs (OpenAI) by default
- Single-user oriented — sharing requires Obsidian Publish ($) or git

**Assessment:** Good for personal knowledge management. Less suited for a system that needs to serve both humans and agents through structured doorways. The markdown-first approach is appealing but the serving layer would still need to be built separately.

### Option C: Hybrid (Anytype for curation + custom API for serving)

Use Anytype as the knowledge workspace where entries are created, reviewed, and linked. Export/sync to a PostgreSQL database that powers the 8 doorways. Local AI (Ollama) provides embedding search against the published entries.

```
┌──────────────────────┐     ┌──────────────────────────┐
│  Anytype (local)     │     │  Iceland server           │
│                      │     │                           │
│  Draft entries       │────▶│  PostgreSQL (published)   │
│  Review & curate     │sync │  Local AI (embeddings)    │
│  Link & tag          │     │  API (doorways 5-8)       │
│  Human navigation    │     │  Static site (doors 1-4)  │
│                      │     │                           │
└──────────────────────┘     └──────────────────────────┘
```

**This preserves:**
- Anytype's strengths (local-first, backlinks, human-friendly navigation)
- The spec's requirements (sovereign hosting, no commercial API dependency, both human and agent doorways)
- A clean separation between *authoring* (where quality control happens) and *serving* (where access happens)

### Recommendation: Option C

Start with Anytype for authoring. Build custom types matching the 4-table schema. Use the existing Gifted Dreamers space. Defer the serving layer until the seed entries are populated and the felt-sense search design is more concrete.

**Immediate next step:** Create Anytype custom types for Name, Source, Rediscovery, and Bridge in the Gifted Dreamers space. Populate the 30 seed entries. Test whether AI (via MCP) can effectively search and navigate the entries as authored.

## Open Design Questions

1. **Contribution model** — Who can add entries? Open wiki model risks noise. Curated model creates bottleneck. The original Living Library used concentric circles (inner stewards → community contributors → public). This may be the right pattern.

2. **Verification** — How do we ensure a "rediscovery" genuinely maps to the named concept? Requires editorial judgment, not just semantic similarity.

3. **Scope** — Start with systems theory / sociology / organizational behavior (our strongest domains) or attempt breadth immediately?

4. **Funding** — Iceland hosting + GPU hardware has real costs. Who pays? This cannot depend on advertising or data monetization.

5. ~~**Naming**~~ — **RESOLVED (session 18).** The name is **The Word.** See "The Name" section at the top of this document for the full reasoning: davar, logos, kalima, nāma, Buber, curiosity as posture, the word as infrastructure for being heard.

6. **Social technology integration** — The practices named in the social technology seed entries (Circling, World Café, Art of Hosting) are not just vocabulary to catalog — they are *methodologies for how the library itself should work*. The felt-sense search is a World Café table. The curation process should use Circles of Trust principles (no fixing, no advising — just open honest questions about whether a mapping is accurate). The Art of Hosting's "the answer is in the room" applies to the library: the knowledge already exists in the community; the library's job is to make it findable. How do we embed these practices into the library's governance and contribution processes, not just its content?

7. **UpTrust integration** — Jordan Myska Allen's trust-graph platform (uptrusting.com) is architecturally aligned: rank by credibility and trust, not engagement. If UpTrust matures, could the The Word's human-facing doorways live there instead of a custom static site? Trust-ranked concept discussions > engagement-ranked concept discussions. Connection: Sara Ness (friend of human partner, AR community leader) and Allen are in the same network.
