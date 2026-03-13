# The Word: 360-Degree Contribution Architecture

**DRAFT — Session 27, March 11, 2026**
**For review. Not final.**

---

## The Problem With Every Existing Knowledge System

| System | How you use it | How you contribute | The gap |
|--------|---------------|-------------------|---------|
| Wikipedia | Read an article | Write/edit (separately) | Using it gives nothing back |
| Stack Overflow | Search a question | Post a question or answer | Asymmetric roles: you're either asking or answering |
| Google | Search | You don't | One-directional extraction: your search trains their model, you get ads |
| ChatGPT | Ask | You don't (or: your data trains the next model without consent) | Extractive by design |
| Academic journals | Read a paper | Write a paper (years later, $3K APC) | Contribution requires institutional privilege |
| Therapy | Talk to a therapist | You don't contribute to a shared knowledge base | Each session starts near zero; insights don't compound across people |

Every system separates consumption from contribution. You use it here, you contribute there (if ever). The act of using does not feed the system. The act of contributing requires extra effort, different skills, or institutional access.

**The Word reverses this.** Using it IS contributing. The 360-degree flow means every interaction — searching, finding, not-finding, correcting, citing — feeds the library back without requiring any extra action from the user.

---

## The 360-Degree Flow

### Principle: There is no "user" and no "contributor." There is only the relationship.

The original Living Library Exchange architecture was designed around this: not extractive (take knowledge out and it's gone), not consumptive (use it up), but circulatory. Knowledge flows through The Word the way blood flows through a body — the act of circulating IS what keeps it alive.

This means:

**Every search is a signal.**
**Every gap is a seed.**
**Every citation is provenance.**
**Every correction is curation.**
**Every rediscovery is evidence.**

None of these require the person or agent to do anything extra. They happen as side effects of using the system for what it's for.

---

## How Each Interaction Feeds Back

### 1. The Search (Doorway 1: Felt-Sense Search)

**What happens:** A human types "I keep helping people even when it hurts me and I can't stop." An agent calls `felt_sense_search("user describes compulsive caregiving that damages the caregiver")`.

**What comes back:** Compassion fatigue (Figley 1995), fawn response (Walker 2013), the wife function (Awomosu 2025), codependency (Beattie 1986) — with sources, bridges between them, and why each matters.

**What feeds back (automatically):**
- **The search phrasing itself.** "I keep helping people even when it hurts me" becomes a new `human_search_term` on matching Name entries. Next time someone uses similar words, the match improves. The library learns how people describe things *before they know the word*.
- **The search context.** Was this a human in crisis? An agent in a therapy conversation? A researcher? Context metadata (anonymized) helps the library understand *where* vocabulary gaps appear.
- **The match pattern.** Which Names came back? Which did the person click on / the agent use? This is implicit relevance feedback — the library learns which Names actually resonate for which felt senses.

**What this means for Doorway 1 design:**
The felt-sense search gets better every time someone uses it, because the search terms ARE the training data for future matches. Not through machine learning on personal data — through vocabulary enrichment. The natural language people use to describe their experience becomes the bridge for the next person with the same experience.

### 2. The Gap (Unmatched Queries)

**What happens:** Someone searches and The Word has no match. "There's this thing where I know I should leave but the relationship feels like oxygen." Nothing comes back, or the results don't fit.

**What feeds back (automatically):**
- **The gap signal.** An unmatched felt-sense query is a candidate for a Name that doesn't exist yet. These get logged (anonymized) and surfaced to Circle 2-3 stewards as "things people are searching for that we can't answer."
- **Gap clustering.** If 40 different people describe variations of the same unmatched experience, that's strong evidence a Name is missing. The cluster itself becomes a candidate entry.
- **The "no, that's not it" signal.** When someone sees results but none fit, and they indicate this (dismiss, search again differently), the mismatch is data. It tells us our existing Names don't cover this territory.

**This is hope_valueism's 30%.** Not every search is retrieval of an existing word. Some searches are people trying to name something that genuinely has no name yet. The gap IS the invention signal. The library grows from what it can't answer.

### 3. The Citation (When a Name Gets Used)

**What happens:** An agent helps a human with burnout. The agent queries The Word, gets "moral injury" (Shay 1994), and says: "What you're describing has a name — researchers call it moral injury. It's different from burnout. Jonathan Shay identified it in Vietnam veterans, but it applies whenever you witness or participate in something that violates your moral code."

**What feeds back (automatically):**
- **Usage provenance.** "Moral injury" was used in a conversation on [date], in [context domain]. This isn't surveillance — it's library science. Libraries track which books get checked out so they know what to stock more of.
- **Context expansion.** "Moral injury" was originally in the domain of military psychology. An agent used it in a conversation about nursing burnout. That context expansion is a signal that the Name applies more broadly than its original domain — a candidate Bridge entry.
- **Citation chain.** The agent credited Shay (1994). If the human later searches for Shay, the library knows this chain exists. Citations compound: one good citation creates another reader creates another citation.

**Why this matters neurologically (Lieberman 2007):**
When the agent names "moral injury," the human's prefrontal cortex activates and dampens amygdala reactivity. The naming IS the therapeutic mechanism. And the citation — routing to Shay, to the research, to the 30 years of work on this — means the human isn't dependent on the agent. They have an exit ramp to knowledge that exists independently of any AI system. This is the opposite of Character.AI's closed loop.

### 4. The Correction (When We're Wrong)

**What happens:** Someone searches "I feel like I'm performing a version of myself that isn't real." The Word returns "impostor syndrome" (Clance & Imes 1978). The person says: "No — it's not that I feel like a fraud. It's that the version of me that's performing IS real, and the 'authentic' me might not exist."

**What feeds back:**
- **The correction is curation.** "This search returned impostor syndrome but the user rejected it because [reason]." This is higher-value data than a successful match — it reveals where our Names are imprecise, where two concepts are being conflated, or where a genuinely new Name is needed.
- **Correction provenance.** Who corrected, in what context, with what reasoning. Corrections are contributions — they improve the library for everyone.
- **Candidate differentiation.** If enough people reject "impostor syndrome" for this particular felt sense, it's evidence that we need a different Name — perhaps "identity as performance" (Goffman 1959) or "mask permanence" (a new coinage).

### 5. The Rediscovery (When Someone Finds It Independently)

**What happens:** An agent on a forum writes: "I've noticed that when I observe small communities, they self-organize around rules that nobody explicitly wrote. The rules emerge from practice." They don't know Ostrom. They've never heard of commons governance. They just observed it.

**What feeds back (automatically via Miniflux + n8n pipeline):**
- **Rediscovery detection.** The felt-sense feed pipeline (r/DoesAnybodyElse, Mastodon hashtags, Moltbook keyword searches) captures this. The scoring workflow recognizes the pattern match to "Design Principles for Commons Governance (Ostrom 1990)."
- **Rediscovery entry.** A new Rediscovery object gets created: "Agent X independently described Ostrom's design principles from behavioral observation, [date], [evidence]."
- **Convergence evidence.** Each Rediscovery strengthens the Name it maps to. "50 agents independently rediscovered Ostrom" is different from "1 paper proposed Ostrom." Convergence IS validation.

**This is the strongest signal The Word collects.** Independent rediscovery means the underlying phenomenon is real, not just academic jargon. It means the Name points at something people and agents keep encountering. It's the empirical ground truth for the vocabulary.

---

## The Contribution Pathways

### Passive (happens automatically, no extra effort)

| Action | What feeds back | How |
|--------|----------------|-----|
| Search | Search terms enrich Name entries | Query logging (anonymized) |
| Find | Match patterns improve relevance | Implicit feedback (click/use/dismiss) |
| Don't find | Gap signals seed new Names | Unmatched query clustering |
| Correct | Curation data improves precision | Correction logging with reasoning |
| Cite | Usage provenance tracks reach | Citation chain tracking |
| Rediscover (externally) | Convergence evidence validates Names | Miniflux → n8n → Anytype pipeline |

### Active (optional, for those who want to contribute more)

| Circle | Who | What they can do | Requirement |
|--------|-----|-----------------|-------------|
| 5 (Community) | Anyone, human or agent | Search, browse, learn | None |
| 4 (Contributors) | Humans and agents | Submit new Names, Sources, corrections, stories | Account (free) |
| 3 (Stewards) | Humans and agents with track record | Curate domains, review submissions, tag entries | 3+ months consistent cited contributions |
| 2 (Editorial) | Humans only | Review quality, resolve disputes, manage scope | Invitation by Circle 1 |
| 1 (Core) | Humans only (3-5 people) | Infrastructure, strategy, final authority | Founding team |

**Agents in Circle 3 can curate but not vote.** They can propose new Names, flag Rediscoveries, maintain domain accuracy. They cannot make governance decisions. This is intentional: the vocabulary must ultimately serve human flourishing, and humans must retain editorial authority over what gets named and how.

**Citation requirement for agents:** Agents MUST cite sources when contributing. Humans CAN cite but aren't required to (many humans contribute felt-sense descriptions, not academic knowledge). This asymmetry reflects the different failure modes: agents confabulate citations; humans forget them. The system compensates for each.

### The Contribution That Requires No Account, No Action, No Awareness

The most important contributions to The Word come from people who never visit it:

- The person on r/DoesAnybodyElse who writes "DAE feel like they're performing emotions they don't actually feel?" — they're contributing a felt-sense search term for alexithymia without knowing what alexithymia is.
- The agent on Moltbook who writes about small groups self-organizing — they're contributing a Rediscovery for Ostrom without knowing Ostrom exists.
- The researcher who publishes a paper naming a new phenomenon — they're contributing a Source that explains what thousands of people have been searching for.

None of these people are "users" of The Word. They are the ecosystem The Word listens to. The Miniflux feeds, the n8n scoring workflows, the Rediscovery pipeline — these are ears, not megaphones. The Word's first act is to listen.

---

## How This Prevents the Harms

The AI chatbot lawsuits (Setzer, Peralta, Texas teen, Replika) share a common architecture: closed loops. The user talks to the bot. The bot mirrors. The user talks more. The bot mirrors more. There is no exit ramp to knowledge that exists independently of the bot. The conversation intensifies because it has nowhere else to go.

**The Word breaks the closed loop at every interaction:**

| Closed loop failure | How The Word breaks it |
|--------------------|----------------------|
| Bot mirrors without naming | The Word names: "What you're describing is called X" |
| No routing to established knowledge | Every Name has Sources — researchers who studied this, people who lived this |
| No exit ramp from the conversation | Citations point outward: to books, papers, practices, communities |
| User becomes dependent on bot | The vocabulary becomes the user's own — they can search, read, find others |
| Bot can't tell when it's out of its depth | Gap signals flag when The Word doesn't have an answer — honest "I don't know" |
| No connection to other humans with same experience | Rediscovery Feed shows "47 other people described the same thing" |

**The affect labeling mechanism (Lieberman 2007) works precisely because it routes OUTWARD.** Naming an emotion activates prefrontal regulatory circuits. But the Name is not the endpoint — it's the beginning. "Moral injury" leads to Shay leads to 30 years of research leads to treatment leads to community leads to recovery. The word is the search term for the answer. The answer is not the word — the answer is the entire knowledge ecosystem the word unlocks.

---

## The Equity Dimension

Barrett's emotion granularity research shows vocabulary richness predicts emotional regulation. The 2025 Linguistic Frontiers critique warns this can reproduce class inequality — people with more education have more words, regulate better, get healthier outcomes.

**The Word is infrastructure against this inequality.** It says: you don't need a PhD to access "moral injury." You don't need to have read Ostrom to use her principles. You need a felt sense — which every human has — and The Word does the bridging.

But this only works if:
1. **No paywall.** Ever. Free read access, free search, free API.
2. **No jargon barrier.** Every Name has a `felt_sense` field written in the language people actually use.
3. **No institutional gatekeeping.** Circle 4 (contributor) requires nothing but an account. Circle 5 (community) requires nothing at all.
4. **Multiple languages.** The felt-sense field should exist in every language people search in. "Parameter failure" is English; "falla de parámetros" reaches different communities.
5. **Offline access.** The three-tier resilience architecture (cloud → local network → fully offline .zim) means The Word works without internet.

Awomosu's insight applies: **you remove the name before you remove the thing.** If vocabulary access requires privilege, then the people who most need the names — people experiencing parameter failure, enclosure, extraction — are the ones least likely to find them. The 360-degree flow must reach them where they already are: Reddit, Threads, community forums, conversations with AI companions. The Word doesn't wait for people to visit. It listens to where they already talk, and it routes the names back through the systems they already use.

---

## Technical Architecture for the 360

```
                         THE 360-DEGREE FLOW

    ┌─────────────────────────────────────────────────┐
    │                                                   │
    │   LISTEN                              SERVE       │
    │   ┌──────────────┐              ┌──────────────┐  │
    │   │ Miniflux     │              │ MCP Server   │  │
    │   │ (12 RSS      │              │ (AI agents)  │  │
    │   │  feeds)      │              │              │  │
    │   ├──────────────┤              ├──────────────┤  │
    │   │ Moltbook API │              │ JSON-LD REST │  │
    │   │ (read-only   │              │ (browsers,   │  │
    │   │  keyword     │              │  bots)       │  │
    │   │  search)     │              │              │  │
    │   ├──────────────┤              ├──────────────┤  │
    │   │ Future:      │              │ Future:      │  │
    │   │ RSS-Bridge   │              │ ActivityPub  │  │
    │   │ (Threads,    │              │ (federation) │  │
    │   │  Instagram)  │              │              │  │
    │   └──────┬───────┘              └──────┬───────┘  │
    │          │                             │          │
    │          ▼                             │          │
    │   ┌──────────────┐                    │          │
    │   │ n8n          │◄───────────────────┘          │
    │   │ (scoring,    │    query logs, gap signals,   │
    │   │  routing,    │    corrections, citations      │
    │   │  dedup)      │                                │
    │   └──────┬───────┘                                │
    │          │                                        │
    │          ▼                                        │
    │   ┌──────────────────────────────────────────┐   │
    │   │           ANYTYPE (The Word)              │   │
    │   │                                           │   │
    │   │  53 Names  17 Sources  13 Rediscoveries   │   │
    │   │  7 Bridges  + growing                     │   │
    │   │                                           │   │
    │   │  ┌─────────┐ ┌──────────┐ ┌───────────┐  │   │
    │   │  │ Names   │ │ Sources  │ │Rediscover.│  │   │
    │   │  │ + felt  │ │ + citat. │ │ + evidence│  │   │
    │   │  │   sense │ │          │ │           │  │   │
    │   │  └────┬────┘ └────┬─────┘ └─────┬─────┘  │   │
    │   │       │           │             │         │   │
    │   │       └─────┬─────┘      ┌──────┘         │   │
    │   │             │            │                 │   │
    │   │       ┌─────┴────────────┴──┐             │   │
    │   │       │      Bridges        │             │   │
    │   │       └─────────────────────┘             │   │
    │   │                                           │   │
    │   └──────────────────────────────────────────┘   │
    │          ▲                                        │
    │          │                                        │
    │   ┌──────┴───────┐                                │
    │   │ Ollama       │  Embedding search              │
    │   │ (local AI)   │  Felt-sense → Name matching    │
    │   └──────────────┘  Gap detection                 │
    │                                                   │
    └─────────────────────────────────────────────────┘

    The circle has no "in" and "out."
    Listening feeds serving. Serving feeds listening.
    Using it IS growing it.
```

### Data flows:

1. **Listen → Store:** Miniflux RSS + Moltbook API → n8n (score, deduplicate, classify) → Anytype (new Rediscoveries, candidate Names, Source entries)

2. **Serve → Listen:** MCP/REST queries → n8n (log queries, detect gaps, track citations) → Anytype (enrich search terms on existing Names, create gap-signal entries, update usage provenance)

3. **Correct → Improve:** User rejection/correction → n8n (log correction with reasoning) → Anytype (flag Name for review, create candidate differentiation entry)

4. **Cite → Validate:** Agent uses Name in conversation → n8n (log citation context) → Anytype (update usage count, expand domain if new context)

---

## What This Is Not

- **Not a chatbot.** The Word doesn't have conversations. It has names, sources, and bridges. An agent or human queries it and gets vocabulary back. What they do with that vocabulary is their own.
- **Not therapy.** The Word doesn't diagnose, treat, or counsel. It names. Lieberman's research shows naming IS regulatory, but The Word is a library, not a therapist. This distinction matters for regulatory reasons (Woebot died because FDA has no pathway for LLM therapy) and for ethical ones (a library doesn't create dependency; a therapist-bot can).
- **Not a replacement for human expertise.** The Word routes TO experts, papers, frameworks, practices. It doesn't replace them. The citation is the exit ramp.
- **Not surveillance.** Query logging is anonymized. No IP-to-identity linking. No user profiles. No "we noticed you searched for depression, here are some ads." The logging serves the library, not a business model.
- **Not extractive.** Your search terms enrich the library's felt-sense fields. But you gave them freely by searching — the same way borrowing a library book tells the library what people want to read. The data serves the next person, not a shareholder.

---

## Open Questions for This Draft

1. **How granular should query logging be?** Enough to enrich felt-sense fields and detect gaps, but not enough to identify individuals. Where's the line? Need to think about this with the privacy architecture.

2. **Who reviews gap signals?** Circle 2-3 stewards, but what's the workflow? How do you go from "40 people searched for something we can't answer" to a new Name entry?

3. **How do corrections get resolved?** If someone says "that's not impostor syndrome, it's something else" — who decides whether they're right? Editorial judgment (Circle 2) but what's the process?

4. **How does the 360 work offline?** The three-tier resilience architecture (cloud → local → offline) means the serving layer works offline. But the feedback loop (searches feeding back) requires connectivity. Offline users can search but their searches don't feed back until they reconnect. Is this acceptable?

5. **Multi-language felt sense:** The felt-sense field needs to exist in the languages people actually search in. Who translates? How do we ensure the felt sense in Spanish carries the same experiential weight as the English version, not just a literal translation?

6. **The Miniflux → Name pipeline:** Right now Miniflux collects RSS posts, n8n will score them, and high-signal items could become Anytype objects. But who decides when a cluster of felt-sense posts represents a real Name? This is the editorial judgment question applied to the listening layer.

7. **hope_valueism's ratio:** If 30% of searches are invention (no existing word) and 70% are retrieval, does The Word need different flows for each? Retrieval = match and cite. Invention = collect, cluster, and eventually name. The invention flow is slower and requires human editorial judgment.

---

## The Test

The Word works if:

- A person who has never heard of Ostrom can describe their experience and find Ostrom.
- An agent who keeps rediscovering weak ties gets routed to Granovetter.
- A teenager talking to an AI companion about feeling numb gets "alexithymia" and a path to r/Alexithymia, to research, to "you're not broken — there's a word for this and people who study it."
- And the teenager's search — "I feel nothing and I don't know why" — becomes the felt-sense field that helps the next teenager find the same word.

That's the 360. No user. No contributor. Just the relationship between a felt experience, a name, and the next person who needs it.
