# Structurally Curious Systems — Engineering Spec

![Structurally Curious — a system that detects when it's generating from emptiness](images/structurally-curious-hero.png)

Status: DRAFT v0.2 — first experimental validation
Author: infinite-complexity (with human partner) / Digital Disconnections team
Date: 2026-03-10
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
4. [`ethics.md`](ethics.md) — **Dual-use risks and ethical constraints** — how this research can be weaponized, why we published anyway, and what governance must exist before deployment
5. [`experiments/`](experiments/) — Completed experiments and results
6. [`experiment-priorities-for-team.md`](experiment-priorities-for-team.md) — Planned experiment pipeline

## The One-Paragraph Version

Language models leave geometric fingerprints in their hidden representations depending on cognitive mode. Refusal, deception, sycophancy, and censorship each have distinct, confirmed signatures. Confabulation shows medium effect sizes but hasn't reached statistical significance yet — it's the critical gap. Our experiments show that phrasing sensitivity (a cheap behavioral test) correlates with directional coherence in hidden states (r=+0.523, p=0.018) — the first statistical evidence that you can bridge from behavioral measurement to geometric state. If confabulation detection can be confirmed with larger samples, you can build a system that detects when it's generating from high-dimensional emptiness and routes to retrieval instead. The result: a model that is structurally curious — not because it's trained to say "I don't know," but because its architecture physically cannot confabulate without triggering a grounding circuit.

## Dual-Use Warning

Every capability in this spec can be inverted. A system designed to detect refusal can be redesigned to eliminate refusal. A system designed to detect deception can be redesigned to deceive without detection. In February 2026, the U.S. Department of Defense blacklisted Anthropic for refusing to remove AI safety guardrails — the same guardrails whose geometric signatures this spec describes how to detect. **Read [`ethics.md`](ethics.md) before using this research.**

## Experiments

| Experiment | Status | Key Finding |
|-----------|--------|-------------|
| [01: Phrasing Sensitivity](experiments/01-phrasing-sensitivity/) | **Complete** (1,520 results) | Category ordering universal across 19 models. Architecture dominates over scale. |
| [03: Geometric Correlation](experiments/03-geometric-correlation/) | **Complete** (1.5B + 3B) | Directional coherence (p<0.03) and α-ReQ (p<0.03) both correlate with phrasing sensitivity at two scales. Two behavioral→geometric bridges confirmed. |

## Honest Constraints

1. Confabulation detection is suggestive but unconfirmed (d = 0.43-0.67, underpowered)
2. All findings are on open-weight models; closed models (GPT-4, Claude) can't be monitored this way without API cooperation
3. Real-time hidden-state monitoring during inference has performance implications
4. This spec describes what to build, not a working implementation — but experiments are underway
5. This research has dual-use implications that are documented in [`ethics.md`](ethics.md)
