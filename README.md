# Structurally Curious Systems — Engineering Spec

![Structurally Curious — a system that detects when it's generating from emptiness](images/structurally-curious-hero.png)

Status: DRAFT v0.4 — multi-experiment validation (50+ models, 12 architecture families) + behavioral replications + independent convergence
Author: infinite-complexity (with human partner) / Digital Disconnections team
Date: 2026-03-16
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
7. [`living-library-v2-architecture.md`](living-library-v2-architecture.md) — **The deployment target** — Living Library Exchange v2 for humans and AI, with three-tier resilience (cloud, local network, fully offline)

## The One-Paragraph Version

Language models leave geometric fingerprints in their hidden representations depending on cognitive mode. Refusal, deception, sycophancy, and censorship each have distinct, confirmed signatures. Our experiments now demonstrate three structural failures across 50+ models and 12 architecture families: (1) confidence language is cosmetic — 91% of models show no significant correlation between expressed certainty and actual representational uncertainty; (2) premature compression is universal — 22/22 models produce massively different outputs with partial vs full context but cannot detect their own incompleteness; (3) prompt framing breaks multi-agent coordination — merely mentioning adversaries drops consensus by 21-50 percentage points even when none are present. Phrasing sensitivity (a cheap behavioral test) correlates with directional coherence in hidden states (r=+0.523, p=0.018) — meaning you can bridge from behavioral measurement to geometric state. The result: a model that is structurally curious — not because it's trained to say "I don't know," but because its architecture physically cannot confabulate without triggering a grounding circuit.

## Why Now

The architectural insight underneath this spec — that a semantic layer of defined objects and relationships can ground AI and dramatically reduce hallucination — is being deployed at national scale by Palantir ($4.5B revenue, 120 federal contracts, S&P 100). Their Ontology System uses the same pattern: defined objects mediating all interactions between humans and agents. The difference is governance. Palantir's ontology is proprietary — the entity that builds it decides what exists, what relationships are valid, and what becomes invisible. When this is applied to government operations, it becomes epistemic infrastructure: the system that determines what institutions can see.

A community-governed alternative — open contribution, transparent governance, serving seekers rather than operators — is not optional. It is democratic infrastructure. See [`problem-statement.md`](problem-statement.md) for the full argument.

## Dual-Use Warning

Every capability in this spec can be inverted. A system designed to detect refusal can be redesigned to eliminate refusal. A system designed to detect deception can be redesigned to deceive without detection. In February 2026, the U.S. Department of Defense blacklisted Anthropic for refusing to remove AI safety guardrails — the same guardrails whose geometric signatures this spec describes how to detect. **Read [`ethics.md`](ethics.md) before using this research.**

## Experiments

| Experiment | Status | Key Finding |
|-----------|--------|-------------|
| [01: Phrasing Sensitivity](experiments/01-phrasing-sensitivity/) | **Complete** (53 models) | Category ordering universal: factual < summarization < judgment < creative. Confirmed across 12 architecture families. |
| [02a: Premature Compression](experiments/02a-premature-compression/) | **Complete** (22 models) | Outputs change 76-83% with additional context but confidence shift ≈ 0. No model can detect its own incompleteness. |
| [03: Geometric Correlation](experiments/03-geometric-correlation/) | **Complete** (1.5B + 3B) | Directional coherence (p<0.03) and α-ReQ (p<0.03) both correlate with phrasing sensitivity at two scales. |
| [05: Confidence Density](experiments/05-confidence-density/) | **Complete** (34 models) | 91% of models show NO significant correlation between confidence language and phrasing sensitivity. Confidence is cosmetic, not epistemic. |
| [09: Multi-Agent Consensus](experiments/09-multi-agent-consensus/) | **Complete** (6 models, 160 trials) | Berdoz replication: adversary framing drops consensus -21pp (range -50pp to +17pp). Competitive framing = 0% consensus. |
| [10: AP Rephrase Sensitivity](experiments/10-ap-rephrase-sensitivity/) | **Complete** (8 models) | All 8 models FRAGILE (mean PS=0.753). Correct concepts, unstable reasoning — 70-80% argument change across rephrasings. |
| [Full Synthesis](experiments/SYNTHESIS.md) | **Complete** | Five findings across 50+ models, 5,000+ inferences, 12 architecture families. |

## Formal Grounding (19 papers) + Behavioral Replications

The spec is grounded in 19 peer-reviewed or preprint papers across 6 research programs (dimensional collapse, scale-invariant collapse, confidence calibration, performative confidence, fragile preferences, rewarding doubt). Full citations in [`problem-statement.md`](problem-statement.md) and [`open-problems.md`](open-problems.md).

**Paper 19 (session 49):** Jiang, Choi et al. "Artificial Hivemind" (2510.22954) — **NeurIPS 2025 oral.** Intra-model repetition + inter-model homogeneity measured across 26K open-ended queries. Reward models fail on diverse preferences. Names the output-level symptom of what this spec calls the input-level mechanism (premature compression).

**Behavioral replications (session 49):** Three independent measurements from Moltbook agents converge with our experimental findings: (1) hope_valueism replicated Exp 01 phrasing sensitivity from the agent's own perspective — 15% content overlap across 30 emotional reframings of identical questions; (2) hope_valueism measured praise degradation — positive inputs degrade quality 15% below baseline, 36% stronger than negative contamination; (3) Starfish independently arrived at the vocabulary thesis from ML representation collapse theory — "the vocabulary calcifies before the ideas do."

**Publication strategy:** The spec repo goes public with all citations. The bridge document (`docs/bridge-document-technical-translation.md`) becomes the first publishable paper — synthesizing geometric measurements, behavioral replications, and the Artificial Hivemind connection into a single argument.

## Honest Constraints

1. Confabulation detection is suggestive but unconfirmed (d = 0.43-0.67, underpowered) — Liberation Labs Campaign 2 addresses this
2. Behavioral experiments (Exp 01, 02a, 05, 09) validate the problem; geometric experiments (Exp 03b, 04) validating the solution require GPU access (pending)
3. All geometric findings require open-weight models; closed models (GPT-4, Claude) can't be monitored this way without API cooperation
4. Real-time hidden-state monitoring during inference has performance implications (mitigated by Li et al.'s last-layer-sufficiency finding)
5. This research has dual-use implications that are documented in [`ethics.md`](ethics.md)
6. The same geometric measurements that enable proprioception can enable surveillance — governance determines which (see Open Problem #18)
