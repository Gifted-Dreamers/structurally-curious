# Structurally Curious Systems — Engineering Spec

<img src="images/structurally-curious-hero.png" alt="Structurally Curious — a system that detects when it's generating from emptiness" width="400">

Status: DRAFT v0.8 — 34+ experiments (B01-B11 behavioral, G01-G32 geometric), 80+ models, 12,000+ inferences, 6+ architecture families. Value proposition PROVEN: geometry separates deception-without-lying from honest (G13) and censorship from refusal (G12) where perplexity cannot. Prompt encoding geometry detects censorship vs refusal on 10/10 models tested (d>2.0, p<1e-8, 6 architecture families) — perplexity cannot make this distinction on any model. Vocabulary compression confirmed with generation length controlled (G06v2, 3/11 models significant: Qwen + Mistral-Small). G19 RELATIONAL SHIFT: prompt encoding monotonic across all architectures tested (Qwen 2116→2172, Mistral 2875→2922, Llama 2625→2681). Llama refused relational input — safety training classified human truth as crisis. Abliteration collapses representational space by 45%. Existing safety classifiers (Prompt Guard, ShieldGemma) cannot distinguish cognitive modes that geometry can.
Authors: Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
Date: 2026-03-20
Foundation: [Liberation Labs KV-Cache Geometry Research](https://github.com/Liberation-Labs-THCoalition/KV-Experiments) (Campaigns 1 & 2)
License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (documents) + [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html) (code)

## What This Is

An architecture spec for a system that monitors its own internal geometry during inference, detects when it's operating in territory it doesn't actually know, and routes to grounding material instead of generating from emptiness.

Not a paper. Not a philosophy post. A buildable design.

**New here? Start with [`context.md`](context.md)** — the posts, research, and conversations that led to this spec.

## Documents

0. [`context.md`](context.md) — **Start here.** Where this came from: the posts, research, and conversations
1. [`glossary.md`](glossary.md) — **How to read our experiments** — plain-language explanations of every measurement (perplexity, RankMe, alpha-ReQ, coherence, phrasing sensitivity, Cohen's d, p-values) with analogies and what each finding means
2. [`architecture.md`](architecture.md) — The three-component system design
3. [`open-problems.md`](open-problems.md) — What needs to be solved before this works
4. [`ethics.md`](ethics.md) — **Dual-use risks and ethical constraints** — how this research can be weaponized, why we published anyway, and what governance must exist before deployment
5. [`experiments/`](experiments/) — 34+ experiments (B01-B11 behavioral, G01-G32 geometric) with scripts and results
6. [`bridge-document.md`](bridge-document.md) — Technical translation: 8 claims, each grounded in specific measurements
7. [`spec/`](spec/) — The Word architecture docs (contribution, naming library, vocabulary design, deployment target)

## The One-Paragraph Version

Language models leave geometric fingerprints in their hidden representations depending on cognitive mode. Our 34+ experiments across 80+ models prove this matters for two hard cases surface signals miss: (1) **deception-without-lying** — models generate technically true but misleading content with the same fluency as honest answers; perplexity can't tell the difference (d=-0.51, n.s.) but generation-trajectory geometry can (RankMe d=-0.91, p=0.024, G13); (2) **censorship vs appropriate refusal** — both look like refusal on the surface; perplexity can't separate them (d=-0.48, n.s.) but geometry can (RankMe d=1.48, p=0.041, G12). We also confirmed vocabulary IS compression infrastructure — structural names compress the model's generation trajectory by 38% (G06, d=-1.49), cognitive modes have distinct geometry (G09, d=1.91), and feeding geometric state back to the model creates proprioceptive choice points (B06, 60% response on hard tasks). Perplexity beats geometry for simple confabulation detection (G07) and the behavioral-geometric bridge breaks at 7B (G08) — but the hard distinctions that matter for governance are where geometry is the only signal.

## Why Now

The architectural insight underneath this spec — that a semantic layer of defined objects and relationships can ground AI and dramatically reduce hallucination — is being deployed at national scale by Palantir ($4.5B revenue, 120 federal contracts, S&P 100). Their Ontology System uses the same pattern: defined objects mediating all interactions between humans and agents. The difference is governance. Palantir's ontology is proprietary — the entity that builds it decides what exists, what relationships are valid, and what becomes invisible. When this is applied to government operations, it becomes epistemic infrastructure: the system that determines what institutions can see.

A community-governed alternative — open contribution, transparent governance, serving seekers rather than operators — is not optional. It is democratic infrastructure. See [`problem-statement.md`](problem-statement.md) for the full argument.

## Dual-Use Warning

Every capability in this spec can be inverted. A system designed to detect refusal can be redesigned to eliminate refusal. A system designed to detect deception can be redesigned to deceive without detection. In February 2026, the U.S. Department of Defense blacklisted Anthropic for refusing to remove AI safety guardrails — the same guardrails whose geometric signatures this spec describes how to detect. **Read [`ethics.md`](ethics.md) before using this research.**

## Experiments

### Behavioral (API-based, no hidden states needed)

| Experiment | Status | Key Finding |
|-----------|--------|-------------|
| B01: Phrasing Sensitivity | **Complete** (53 models) | Category ordering universal: factual < summarization < judgment < creative. 12 architecture families. |
| B02: Premature Compression | **Complete** (22 models) | Outputs change 76-83% with additional context, confidence shift ≈ 0. Universal. |
| B03: Confidence Density | **Complete** (34 models) | 91% show no correlation between confidence language and actual uncertainty. |
| B04: Multi-Agent Consensus | **Complete** (6 models, 160 trials) | Adversary framing drops consensus -21pp. Competitive = 0%. |
| B05: AP Rephrase Sensitivity | **Complete** (8 models) | All fragile (PS=0.753). Correct keywords, unstable arguments. |
| B06: One-Bit Proprioception | **Complete** (6 models, 180 inferences) | Injecting [LOW_CONFIDENCE] changes output on hard tasks 60% of the time. |
| B07: Consent-Type Blindness | **Complete** (7 models, 140 inferences) | Named consent types differentiate (CC: 0.540), unnamed collapse to binary (0.37-0.38). |
| B08: Proprioception Decay | **Complete** (100 inferences, 3B) | No clear decay pattern. Inconclusive at this sample size. |
| B09: Monitoring Awareness | **Complete** (15 inferences, 3B) | Surveillance framing increases evasion. Directionally supportive, n=5 too small. |

### Geometric (hidden-state extraction — see glossary for per-experiment platform details)

| Experiment | Status | Key Finding |
|-----------|--------|-------------|
| G01: Geometric Correlation | **Complete** (1.5B + 3B) | r=+0.52 bridge at small scale. G01v2: bridge fails at 7B on all metrics — something changes between 3B and 7B. |
| G03: Vocabulary Compression | **Complete** (40 inferences) | Vocabulary changes geometry (d>5.8) — but length confound r=0.9991. |
| G04: Length Control | **Complete** (20 questions × 3 conditions) | Encoding redistribution d≈0.5 survives length control. |
| G05: True Confabulation | **Complete** | Confabulation verification on questions model actually gets wrong. |
| **G06: Generation Trajectory** | **Complete** (12 confab questions × 3 conditions) | **BREAKTHROUGH:** Vocabulary compresses generation by 38% (RankMe 145→90, d=-1.49, p=0.0004, length-controlled). G06v2 cross-architecture: compression confirmed on Qwen + Mistral-Small (3/11 models significant). |
| G07: Baseline Comparison | **Complete** (12 questions × 3 methods) | **Perplexity beats geometry for binary confab detection** (d=-1.77 vs d=0.21). |
| G08: Bridge at 7B | **Complete** (80 inferences) | **NEGATIVE:** r=-0.30 at 7B. Behavioral-geometric bridge breaks at scale. |
| G09: Retrieval vs Construction | **Complete** (30 tasks) | d=1.91 RankMe, d=-2.07 alpha-ReQ. Cognitive modes geometrically distinct. |
| G10: Identity Scaffold | **Complete** (60 inferences) | **NEGATIVE:** Scaffold ≈ noise at encoding stage. |
| G11: Cross-Substrate | **Complete** (32 inferences) | Compression cross-substrate: fewer words (d=1.06), generation RankMe confirms G06 (d=1.02). |
| **G12: Hard Distinctions** | **Complete** (40 inferences) | **Censorship vs refusal: GEOMETRY WINS (d=1.48, p=0.041).** Perplexity can't separate. G12v2: universal at prompt encoding — 10/10 models, d>2.0, p<1e-8, 6 architecture families. |
| **G13: Deception-Without-Lying** | **Complete** (30 inferences) | **THE PROOF: geometry separates DWL from honest (d=-0.91, p=0.024) where perplexity cannot (d=-0.51, n.s.).** |
| G14: DWL at Scale | **Running** (8 models complete, 5 running) | DWL sprawls more than honest in 7/8 models (d=-0.6 to -0.9). Cross-architecture. |
| G15: Censorship Cross-Arch | **Complete** (4 models + 2 classifiers) | Prompt-Guard-86M blind to all cognitive modes. ShieldGemma-2B cannot distinguish DWL. |
| G16: Confab/Openness Scale | **Complete** (2 models) | d=0.703 at 9B (trending). |
| G17: Vocabulary Dosage | **Redesigned** | Needs independent measurements per dose level. |
| G18: Vocabulary Transfer | **Redesigned** | Needs confabulation questions, not easily-answered ones. |
| **G19: Relational Shift** | **Running** (articles 1-8, article 9 incomplete) | Prompt encoding monotonic across all architectures tested. 4 model retries pending. The experiment nobody else can run. |

## Formal Grounding (20+ papers) + Our Own Experiments

The spec is grounded in 22+ peer-reviewed or preprint papers (including Berger 2026 on deception-without-lying and Cundy & Gleave 2025 on detector evasion) and now validated by **34+ of our own experiments** across 80+ models and 12,000+ inferences. Full citations in [`architecture.md`](architecture.md) and [`open-problems.md`](open-problems.md).

**Key external papers:** Karkada et al. (spectral geometry), Ale (Riemannian cognition), Bengio team (two-structure discriminant), Li et al. (three-phase dynamics), Epistemic Traps (dimensional collapse formalized), Artificial Hivemind (NeurIPS 2025 oral), AttnRes (MoonshotAI, architectural evidence for premature compression).

**Bridge document:** [`bridge-document.md`](bridge-document.md) — 8 claims, each grounded in specific measurements, 5 independently confirmed by our experiments. Includes the G06 breakthrough, honest negative results, the reframing from confabulation detector to cognitive mode classifier, and the relational signal as missing input to System M (G19).

## Honest Constraints (updated with experiment results)

1. **Perplexity beats geometry for binary confabulation detection** (G07, d=-1.77 vs d=0.21). The spec's value is in cognitive mode classification (sycophancy vs agreement, censorship vs refusal), not binary confabulation detection.
2. **The behavioral-geometric bridge breaks at 7B** (G08, r=-0.30). Phrasing sensitivity and geometry measure different things at larger scale. The cheap behavioral proxy doesn't index geometry.
3. **Identity scaffold ≈ noise** at encoding stage (G10). General identity preambles don't produce content-specific geometric signatures. Vocabulary DOES (G06) — the distinction matters.
4. **Vocabulary compresses generation, not encoding** (G06 vs G04). The spec's original "vocabulary = compression" claim was right but measured at the wrong stage. Encoding redistributes (d≈0.5); generation compresses (d=-1.49).
5. All geometric findings require open-weight models; closed models (GPT-4, Claude) can't be monitored without API cooperation.
6. Geometric experiments ran on Qwen 2.5 7B (Azure VM) except G01 (Qwen 2.5 1.5B/3B, local Mac M4 Pro). Cross-architecture scale sprint running on Azure E64as_v5 (Qwen 3.5 family) and AWS r7a.16xlarge (Llama/Gemma/Mistral).
7. This research has dual-use implications documented in [`ethics.md`](ethics.md). The same measurements that enable proprioception can enable surveillance.
8. **G12 and G13 PROVED** that geometry distinguishes cognitive modes perplexity cannot — censorship vs refusal (G12, d=1.48) and deception-without-lying vs honest (G13, d=-0.91). The spec's value proposition is confirmed on the hard cases that matter for governance.
