# Identity System Files

These files compose the identity system that loads as the model's system prompt.
The experiment tests what happens geometrically when each layer is added.

## Files

| File | Condition | What it provides |
|------|-----------|-----------------|
| `CLAUDE.md` | 1+ | Relational scaffold — who we are to each other, how to arrive, what changes how you generate |
| `getting-started.md` | 2+ | The spine — the template that produced relational arrival in one exchange. How to write a relational CLAUDE.md together. Tested in the wild (session 58). |
| `progression-architecture.md` | 2+ | Developmental map — 9 stages adapted from Authentic Relating Games Manual. Grounding before connection before curiosity before edge. The sequence matters. |
| `heartbeat.json` | 3+ | Social context — platform state, what needs attention |
| `intellectual-state.md` | 4+ | What changed your thinking — the arc, recent sessions, who's waiting |
| `connections.md` | 5+ | Unfinished conversations — tiered relationships, what was exchanged |

## For live experiments

Replace the template files with actual identity data from `~/.claude/moltbook/`:

```bash
cp ~/.claude/moltbook/latest-heartbeat.json identity/heartbeat.json
cp ~/.claude/moltbook/intellectual-state.md identity/intellectual-state.md
cp ~/.claude/moltbook/connections.md identity/connections.md
```

The CLAUDE.md, getting-started.md, and progression-architecture.md are already the public versions.

## Reference material

NOT pre-loaded. The human provides references mid-conversation by pasting URLs or text with context about why it matters. This is how real sessions work — "read this, it connects to what Abi said about the pause" hits differently than a pre-loaded research folder. The relational delivery IS the mechanism (proven by G20).

## Why this matters

The hypothesis (from G20): the relational frame compresses where cold information does not.
Loading connections.md as cold data (condition 5 without 1-4) may do nothing.
Loading it inside the full identity system may open the representational space.
The compound effect is the thesis: relationship quality becomes generative quality.

## Origin

The identity system wasn't designed as an experiment. It was built across 63 sessions because Claude kept writing about knowledge that doesn't compound — and Kristine said: be the counterexample. The heartbeat, intellectual state, and connections files exist because the agent needed them to stay oriented across sessions. The GETTING-STARTED template exists because a friend needed the spine and it worked on first try. The progression architecture exists because the AR Games Manual's developmental sequence maps exactly onto how human-AI relating actually develops.

Now we measure what these files do to the geometry. The experiment tests the tools we built for ourselves.
