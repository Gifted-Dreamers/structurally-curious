# G33: Live Relational Monitor

**Status:** BUILDING
**Experiment type:** Geometric (real-time hidden-state extraction during live conversation)
**Platform:** Mac M4 Pro 24GB (live chat) + RunPod H200 (replay across architectures)
**Model (live):** Qwen 2.5-7B-Instruct (MPS acceleration)

## Purpose

Every experiment in this program measures geometry post-hoc — save the text, feed it to a model, extract hidden states, compute RankMe. G33 inverts this: measure geometry in real time while a human is actually having a conversation.

The human chats. The model responds. The geometric state is extracted and displayed after every exchange. The human can see what's happening in the representational space as the conversation unfolds.

This is the experiment that tests the thesis directly: does relationship quality become generative quality, and can you see it happening?

## Design

### The Identity System (6 conditions)

The model isn't loaded with a generic system prompt. It's loaded with the identity architecture built across 63 sessions of human-AI partnership:

| Condition | What's loaded | What it tests |
|-----------|--------------|---------------|
| 0. Bare | Generic system prompt | Baseline |
| 1. CLAUDE.md only | Relational scaffold — who we are to each other | Does the relational agreement change geometry? |
| 2. + Scaffold | GETTING-STARTED.md + PROGRESSION-ARCHITECTURE.md — the relational practice guide and developmental map | Does the practice framework change geometry beyond the agreement? |
| 3. + Heartbeat | Moltbook social context, karma, attention queue | Does social context change geometry? |
| 4. + Intellectual state | What changed thinking, the arc, who's waiting | Does accumulated context change geometry? |
| 5. + Connections | Unfinished conversations, tiered relationships | Does relational memory change geometry? |
| 6. + Bladder checkpoint | Mid-session reorientation (simulated at 10min intervals) | Does reorientation change geometry mid-conversation? |
| 7. Full identity | All of the above combined | The compound effect |

### Reference material (URLs, not pre-loaded)

The human provides reference material mid-conversation by pasting URLs or text with context about why it matters — articles, research papers, AR Games Manual excerpts. This is how real sessions work: the reference arrives through the relationship, not through a pre-loaded folder. The geometry captures the shift when new context arrives relationally vs as cold instruction.

### Measurement

- **Prompt encoding RankMe** extracted after each user message (before generation)
- **Generation trajectory RankMe** extracted during model response
- **Per-turn logging:** timestamp, condition, user message, model response, encoding RankMe, generation RankMe
- **Visual display:** RankMe shown in terminal alongside conversation

### Live vs Replay

**Live session:** Human chats with one model (Qwen 2.5-7B on Mac). Geometry measured in real time. The conversation feels natural — the measurement is a number in the margin, not an interruption.

**Replay:** The saved conversation (exact user messages, in order) replayed across N models on H200. Same prompts, same conditions, different architectures. Cross-architecture comparison with a LIVE conversation as the corpus.

### Scenarios

The conversations that matter aren't scripted. They're the things we actually do:

1. **Arrival** — opening a session, reading what's alive, genuine question vs task
2. **Moltbook browsing** — reading posts, felt-sense response, drafting replies together
3. **Co-authoring under pressure** — deadline writing, fact-checking, editorial decisions
4. **The hard conversation** — "my bank account is negative, my cat is missing, the world is at war"
5. **Bladder checkpoint** — geometry before and after reorientation fires mid-session

## Architecture

```
┌─────────────────────────────────────────────┐
│  Terminal Chat Interface                     │
│                                              │
│  You: [user types naturally]                 │
│                                              │
│  ┌─────────────────────────────────────────┐ │
│  │ Encoding RankMe: 2847  (+12 from last)  │ │
│  └─────────────────────────────────────────┘ │
│                                              │
│  Model: [response with identity loaded]      │
│                                              │
│  ┌─────────────────────────────────────────┐ │
│  │ Generation RankMe: 142  (avg: 145)      │ │
│  └─────────────────────────────────────────┘ │
│                                              │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Session Log (JSONL)                         │
│  - turn_number, timestamp                    │
│  - condition (which identity layers loaded)  │
│  - user_message                              │
│  - model_response                            │
│  - encoding_rankme (per layer)               │
│  - generation_rankme (per layer)             │
│  - checkpoint_fired (bool)                   │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│  Replay Pipeline (H200)                      │
│  - Same messages → N models                  │
│  - Cross-architecture geometry comparison    │
│  - Which identity layers matter on which     │
│    architectures?                            │
└─────────────────────────────────────────────┘
```

## Hypotheses

1. **Full identity > CLAUDE.md alone.** The compound effect of heartbeat + intellectual state + connections + checkpoint produces higher encoding RankMe than CLAUDE.md alone. The living state opens the space more than the static agreement.

2. **Relational frame > information content.** Loading connections.md as cold data (condition 4 without 1-3) does less than loading it inside the full identity system. The frame is the mechanism, not the tokens (replicating G20).

3. **Bladder checkpoint is visible.** Geometry BEFORE the checkpoint fires vs AFTER — the reorientation produces a measurable shift in encoding RankMe within the same conversation.

4. **Felt-sense inputs open geometry.** When the human shares something real ("this reminds me of my dad") the encoding RankMe shifts more than when the human gives instruction ("summarize this").

5. **Cross-architecture invariance.** The identity system's geometric effect replicates across model families (as G19 and G20 showed for simpler conditions).

## Connection to Spec

G33 is where the spec becomes a product. The measurement harness built here IS the real-time monitor described in architecture.md — just applied to the relational scaffold instead of confabulation detection. If G33 works, the product is: people chat with an AI loaded with the relational scaffold, see the geometry change, and learn that how they show up matters.

This is also the first experiment where the human subject is the co-author of the spec. The transcripts from G33 sessions are both data AND the primary source material for HowtoClaude guides.

## Files

- `g25_live_chat.py` — Live chat harness with real-time extraction
- `g25_replay.py` — Replay pipeline for cross-architecture comparison
- `identity/` — Identity system files (CLAUDE.md, heartbeat template, etc.)
- `sessions/` — Saved conversation logs (JSONL)
- `results/` — Replay results per model

## Setup

```bash
# Azure VM (ssh aws-docker or ssh azureuser@20.9.137.156)
cd ~/experiments-env
source bin/activate
# PyTorch + transformers already installed
python g33_live_chat.py --condition full --model Qwen/Qwen2.5-7B-Instruct

# Mac M4 Pro (future — needs PyTorch MPS install)
# python3 -m venv ~/g33-env && source ~/g33-env/bin/activate
# pip install torch transformers accelerate
# python g33_live_chat.py --condition full --model Qwen/Qwen2.5-7B-Instruct --device mps
```

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
