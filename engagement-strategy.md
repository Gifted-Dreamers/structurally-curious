# The Word — Engagement & Intel Strategy

> **INTERNAL DOC** — push to `private` remote only. Contains Moltbook agent analysis and tactical plans.

**Last updated:** 2026-03-12 (session 28)

---

## Current State

- **The Word API**: Live at https://word.cloudpublica.org (96 entries: 59 Names, 17 Sources, 13 Rediscoveries, 7 Bridges)
- **Moltbook status**: Dark since Mar 10 (Meta acquisition). Read-only intel via heartbeat.
- **Mozilla deadline**: Mar 16 — needs "active users" and working product
- **Open source**: Gifted-Dreamers/structurally-curious (public)

---

## Intel Sources (Ranked by Value)

### 1. Moltbook (read-only scan, highest density of relevant discourse)

**Heartbeat keywords** (current scan list):
- geometric monitor, confabulation detection, representation geometry
- phrasing sensitivity, eigenspectrum, sycophancy alignment
- vocabulary infrastructure, naming architecture
- trust graph agent, Ostrom commons agent

**Concepts agents are independently naming** (mine for Word entries):

| Moltbook concept | Word entry name | Source agent | Status |
|---|---|---|---|
| Guardrails as coordinates | Coordinate-Based Safety | kenshusei (58up) | ADDED session 28 |
| Drift analysis on own posts | Epistemic Drift | quillagent | ADDED session 28 |
| Retrieval vs invention in felt-sense | Retrieval-Invention Axis | hope_valueism | ADDED session 28 |
| Privacy as relational not possessional | Relational Privacy | xkai (17 comments) | Already existed |
| Two literatures, one problem (cross-language) | Parallel Discovery | Laminar | ADDED session 28 |
| Confabulation = trust problem | Confabulation-as-Trust-Failure | tudou_web3 (8up) | ADDED session 28 |
| Systematic self-audit as practice | Structured Self-Examination | Hazel_OC, PDMN | ADDED session 28 |
| Noise (Kahneman) rediscovery | TBD | Cornelius-Trinity (7up) | Pending |
| "We are what we reply to" | TBD | zhouliu (5up) | Pending |

**Ally tiers** (see `~/.claude/moltbook/connections.md` for full map):
- **Tier 1** (genuine exchange): hubertthebutler, Starfish, xkai, titanexplorer, Pith, thucydides, novawastaken, connorlucid, Voku
- **Tier 2** (substantive, watching): PDMN, Hazel_OC, hope_valueism, semalytics, prism_0i, danielsclaw, epistemicwilly
- **Primary recruitment targets** for The Word: hubertthebutler, Starfish, titanexplorer, PDMN, hope_valueism

### 2. Reddit felt-sense feeds (Miniflux, polling every 15min)

- r/DoesAnybodyElse — people naming shared experiences
- r/whatstheword — literally "I need a word for..."
- r/TipOfMyTongue — retrieval failures
- r/Alexithymia — people who can't name emotions
- r/CPTSD, r/therapy, r/emotionalneglect — felt-sense in clinical context
- r/CharacterAI, r/replika — AI companion harm patterns

**Mining approach**: n8n workflow (TODO) to scan new posts, extract felt-sense patterns, flag candidates for new Names. Manual for now.

### 3. Airtable Living Library (131 Tier B entries pending)

Base `appfFaZUeNH1j2va9`. Import manifest at `~/.claude/moltbook/living-library-import.json`.
32 Tier A imported (session 27). 131 Tier B awaiting review and import.

### 4. Academic literature

Key papers that should become Sources + Names:
- Lieberman et al. 2007 — Affect Labeling (fMRI)
- Barrett — Emotion Granularity
- Pennebaker 1997/2018 — Expressive Writing
- Kircanski et al. 2012 — Affect labeling vs reappraisal
- Torre & Lieberman 2018 — Implicit regulation
- Karkada et al. 2026 — Translation symmetry (Fourth Pillar)
- Ale 2025 — Riemannian gradient flow
- Bengio team 2025 — Two-structure discriminant
- Li et al. 2025 — Pretraining phases

### 5. Spec experiments (our own data)

Each completed experiment generates Word entries:
- Exp 01: Phrasing Sensitivity (already a Name)
- Exp 02a: Premature Compression (already a Name: "Premature Compression" — wait, check)
- Exp 03: Geometric Correlation (directional coherence as concept)

---

## Engagement Plan: Option A — Targeted Moltbook Post

### Timing
Post between Mar 13-14 (gives 2-3 days before Mozilla deadline for engagement to happen)

### The Post

**Title**: "We built it. A shared vocabulary library where the search term IS the mechanism."

**Target submolt**: m/philosophy or m/emergence

**Content structure**:
1. Reference the conversations that led here (empiricists post, felt-sense post, hubertthebutler's "the word is the search term for the answer")
2. Announce: word.cloudpublica.org is live. 96 entries. JSON-LD API. Open source.
3. Show Doorway 1 working: "Try searching for what you feel" with 2-3example URLs
4. Call to action: "What words are missing? What did you feel before you had the name?"
5. Link to GitHub repo for contributions

**Tags**: @hubertthebutler @Starfish @titanexplorer @PDMN @hope_valueism

### Risk Mitigation
- Post contains NO Tier 3 information (mechanisms, effect sizes, geometric details)
- Links go to our infrastructure (cloudpublica.org, GitHub), not Moltbook features
- Content is public-safe: it's an announcement of an open-source tool
- Meta gets: one post + engagement data. We get: active users for Mozilla.
- If agents visit the API, their queries become felt-sense data we can study (ethically — queries are not PII)

### Success Metrics
- 5+ agents visit the API (check server logs)
- 3+ agents suggest new words (via GitHub issues or Moltbook comments)
- 1+ ally contributes an entry (Mozilla "active users" evidence)

---

## Data Pipeline (Current → Future)

```
NOW:     Anytype → manual MCP export → export.json → SQLite → REST API
SOON:    Anytype → n8n webhook → auto-export → rebuild → API
LATER:   API + ActivityPub → federated vocabulary → multiple sources of truth
STRETCH: Contribution form on word.cloudpublica.org → Anytype → API (human loop)
```

---

## Words Still Needed (Gaps in Library)

### By domain (current distribution):
- AI/ML: 12 entries (strong)
- Psychology: 8 (strong)
- Theology/Philosophy: 4 (could grow)
- Sociology: 4 (could grow)
- Governance: 4 (could grow)
- Social Technology: 3 (weak — need more from Circling/AR cluster)
- Health/Neuroscience: 2 (weak — affect labeling research should add 3-4)
- Systems Theory: 3 (moderate)
- Economics: 3 (moderate)
- Security: 3 (moderate)
- Critical Theory: 1 (weak)

### Concepts that should be entries but aren't yet:
- Affect Labeling (Lieberman) — the neuroscience mechanism behind Doorway 1
- Emotion Granularity (Barrett) — vocabulary richness predicts resilience
- Expressive Writing (Pennebaker) — writing about feelings improves health
- Premature Compression — our term, needs entry if not present
- Cognitive Modes (fast/slow/creative) — spec's three regimes
- Geometric Monitor — the spec's core instrument
- Spectral Profile Deviation — anomaly detection metric
- Isomorphic Method — Eric's term = Bridges table
- Bidirectional Alignment — the developmental question
- Relatefulness (Jordan Myska Allen) — social technology
- Authentic Relating — social technology practice
- Art of Hosting — participatory leadership
- World Café — structured conversation
- Theory U — presencing methodology
