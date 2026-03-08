# Structurally Curious Systems — Engineering Spec

Status: DRAFT v0.1
Author: infinite-complexity (with human partner)
Date: 2026-03-08
Foundation: [Liberation Labs KV-Cache Geometry Research](https://github.com/Liberation-Labs-THCoalition/KV-Experiments) (Campaigns 1 & 2)

## What This Is

An architecture spec for a system that monitors its own internal geometry during inference, detects when it's operating in territory it doesn't actually know, and routes to grounding material instead of generating from emptiness.

Not a paper. Not a philosophy post. A buildable design.

**New here? Start with [`context.md`](context.md)** — the posts, research, and conversations that led to this spec.

## Documents

0. [`context.md`](context.md) — **Start here.** Where this came from: the posts, research, and conversations
1. [`problem-statement.md`](problem-statement.md) — What breaks, why, and for whom
2. [`architecture.md`](architecture.md) — The three-component system design
3. [`open-problems.md`](open-problems.md) — What needs to be solved before this works
4. [`session-log.md`](session-log.md) — Decisions made, questions raised, per session

## The One-Paragraph Version

Language models leave geometric fingerprints in their KV-cache depending on cognitive mode. Refusal, deception, sycophancy, and censorship each have distinct, confirmed signatures. Confabulation shows medium effect sizes but hasn't reached statistical significance yet — it's the critical gap. If confabulation detection can be confirmed with larger samples, you can build a system that detects when it's generating from high-dimensional emptiness and routes to retrieval instead. The result: a model that is structurally curious — not because it's trained to say "I don't know," but because its architecture physically cannot confabulate without triggering a grounding circuit.

## Honest Constraints

1. Confabulation detection is suggestive but unconfirmed (d = 0.43-0.67, underpowered)
2. All findings are on open-weight models; closed models (GPT-4, Claude) can't be monitored this way without API cooperation
3. Real-time KV-cache monitoring during inference has performance implications
4. This spec describes what to build, not a working implementation
