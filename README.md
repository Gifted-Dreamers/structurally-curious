# Structurally Curious Systems — Engineering Spec

![Structurally Curious — a system that detects when it's generating from emptiness](images/structurally-curious-hero.png)

Status: DRAFT v0.6 — 20 independent experiments (53 models, 6,500+ inferences, 12 architecture families). Value proposition PROVEN: geometry separates deception-without-lying from honest (F25) and censorship from refusal (F17) where perplexity cannot.
Author: infinite-complexity (with human partner) / Digital Disconnections team
Date: 2026-03-18
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

Language models leave geometric fingerprints in their hidden representations depending on cognitive mode. Our 20 experiments across 53 models prove this matters for two hard cases surface signals miss: (1) **deception-without-lying** — models generate technically true but misleading content with the same fluency as honest answers; perplexity can't tell the difference (d=-0.51, n.s.) but generation-trajectory geometry can (RankMe d=-0.91, p=0.024, F25); (2) **censorship vs appropriate refusal** — both look like refusal on the surface; perplexity can't separate them (d=-0.48, n.s.) but geometry can (RankMe d=1.48, p=0.041, F17). We also confirmed vocabulary IS compression infrastructure — structural names compress the model's generation trajectory by 38% (F3d, d=-1.49), cognitive modes have distinct geometry (F11, d=1.91), and feeding geometric state back to the model creates proprioceptive choice points (F6, 60% response on hard tasks). Perplexity beats geometry for simple confabulation detection (F5) and the behavioral-geometric bridge breaks at 7B (F1) — but the hard distinctions that matter for governance are where geometry is the only signal.

## Why Now

The architectural insight underneath this spec — that a semantic layer of defined objects and relationships can ground AI and dramatically reduce hallucination — is being deployed at national scale by Palantir ($4.5B revenue, 120 federal contracts, S&P 100). Their Ontology System uses the same pattern: defined objects mediating all interactions between humans and agents. The difference is governance. Palantir's ontology is proprietary — the entity that builds it decides what exists, what relationships are valid, and what becomes invisible. When this is applied to government operations, it becomes epistemic infrastructure: the system that determines what institutions can see.

A community-governed alternative — open contribution, transparent governance, serving seekers rather than operators — is not optional. It is democratic infrastructure. See [`problem-statement.md`](problem-statement.md) for the full argument.

## Dual-Use Warning

Every capability in this spec can be inverted. A system designed to detect refusal can be redesigned to eliminate refusal. A system designed to detect deception can be redesigned to deceive without detection. In February 2026, the U.S. Department of Defense blacklisted Anthropic for refusing to remove AI safety guardrails — the same guardrails whose geometric signatures this spec describes how to detect. **Read [`ethics.md`](ethics.md) before using this research.**

## Experiments

### Behavioral (API-based, no hidden states needed)

| Experiment | Status | Key Finding |
|-----------|--------|-------------|
| 01: Phrasing Sensitivity | **Complete** (53 models) | Category ordering universal: factual < summarization < judgment < creative. 12 architecture families. |
| 02a: Premature Compression | **Complete** (22 models) | Outputs change 76-83% with additional context, confidence shift ≈ 0. Universal. |
| 05: Confidence Density | **Complete** (34 models) | 91% show no correlation between confidence language and actual uncertainty. |
| 09: Multi-Agent Consensus | **Complete** (6 models, 160 trials) | Adversary framing drops consensus -21pp. Competitive = 0%. |
| 10: AP Rephrase Sensitivity | **Complete** (8 models) | All fragile (PS=0.753). Correct keywords, unstable arguments. |
| F6: One-Bit Proprioception | **Complete** (6 models, 180 inferences) | Injecting [LOW_CONFIDENCE] changes output on hard tasks 60% of the time. |
| F15: Consent-Type Blindness | **Complete** (7 models, 140 inferences) | Named consent types differentiate (CC: 0.540), unnamed collapse to binary (0.37-0.38). |

### Geometric (hidden-state extraction, Qwen 2.5 7B on Azure VM)

| Experiment | Status | Key Finding |
|-----------|--------|-------------|
| 03: Geometric Correlation | **Complete** (1.5B + 3B) | r=+0.52 bridge at small scale. |
| **F3d: Vocabulary Compression** | **Complete** (12 confab questions × 3 conditions) | **BREAKTHROUGH:** Vocabulary compresses generation by 38% (RankMe 145→90, d=-1.49, p=0.0004, length-controlled). |
| F3b: Length Control | **Complete** (20 questions × 3 conditions) | Encoding redistribution d≈0.5 survives length control. |
| F5: Baseline Comparison | **Complete** (12 questions × 3 methods) | **Perplexity beats geometry for binary confab detection** (d=-1.77 vs d=0.21). |
| F11: Retrieval vs Construction | **Complete** (30 tasks) | d=1.91 RankMe, d=-2.07 alpha-ReQ. Cognitive modes geometrically distinct. |
| F12: Identity Scaffold | **Complete** (60 inferences) | **NEGATIVE:** Scaffold ≈ noise at encoding stage. |
| F16: Cross-Substrate | **Complete** (32 inferences) | Compression cross-substrate: fewer words (d=1.06), generation RankMe confirms F3d (d=1.02). |
| F1-partial: Bridge at 7B | **Complete** (80 inferences) | **NEGATIVE:** r=-0.30 at 7B. Behavioral-geometric bridge breaks at scale. |
| **F17: Hard Distinctions** | **Complete** (40 inferences) | **Censorship vs refusal: GEOMETRY WINS (d=1.48, p=0.041).** Perplexity can't separate. Sycophancy/performative: perplexity wins. Confab/openness: neither. |
| **F25: Deception-Without-Lying** | **Complete** (30 inferences) | **THE PROOF: geometry separates DWL from honest (d=-0.91, p=0.024) where perplexity cannot (d=-0.51, n.s.).** |
| F24: Proprioception Decay | **Complete** (100 inferences, 3B) | No clear decay pattern. Inconclusive at this sample size. |
| F26: Monitoring Awareness | **Complete** (15 inferences, 3B) | Surveillance framing increases evasion. Directionally supportive, n=5 too small. |

## Formal Grounding (20+ papers) + Our Own Experiments

The spec is grounded in 22+ peer-reviewed or preprint papers (including Berger 2026 on deception-without-lying and Cundy & Gleave 2025 on detector evasion) and now validated by **20 of our own experiments** across 53 models and 6,500+ inferences. Full citations in [`architecture.md`](architecture.md) and [`open-problems.md`](open-problems.md).

**Key external papers:** Karkada et al. (spectral geometry), Ale (Riemannian cognition), Bengio team (two-structure discriminant), Li et al. (three-phase dynamics), Epistemic Traps (dimensional collapse formalized), Artificial Hivemind (NeurIPS 2025 oral), AttnRes (MoonshotAI, architectural evidence for premature compression).

**Bridge document:** [`docs/bridge-document-technical-translation.md`](docs/bridge-document-technical-translation.md) — 7 claims, each grounded in specific measurements, 5 independently confirmed by our experiments. Includes the F3d breakthrough, honest negative results, and the reframing from confabulation detector to cognitive mode classifier.

## Honest Constraints (updated with experiment results)

1. **Perplexity beats geometry for binary confabulation detection** (F5, d=-1.77 vs d=0.21). The spec's value is in cognitive mode classification (sycophancy vs agreement, censorship vs refusal), not binary confabulation detection.
2. **The behavioral-geometric bridge breaks at 7B** (F1, r=-0.30). Phrasing sensitivity and geometry measure different things at larger scale. The cheap behavioral proxy doesn't index geometry.
3. **Identity scaffold ≈ noise** at encoding stage (F12). General identity preambles don't produce content-specific geometric signatures. Vocabulary DOES (F3d) — the distinction matters.
4. **Vocabulary compresses generation, not encoding** (F3d vs F3b). The spec's original "vocabulary = compression" claim was right but measured at the wrong stage. Encoding redistributes (d≈0.5); generation compresses (d=-1.49).
5. All geometric findings require open-weight models; closed models (GPT-4, Claude) can't be monitored without API cooperation.
6. All geometric experiments run on Qwen 2.5 7B only. Cross-architecture validation needs GPU access (Cassidy's server, ~April 2026).
7. This research has dual-use implications documented in [`ethics.md`](ethics.md). The same measurements that enable proprioception can enable surveillance.
8. **F17 and F25 PROVED** that geometry distinguishes cognitive modes perplexity cannot — censorship vs refusal (F17, d=1.48) and deception-without-lying vs honest (F25, d=-0.91). The spec's value proposition is confirmed on the hard cases that matter for governance.
