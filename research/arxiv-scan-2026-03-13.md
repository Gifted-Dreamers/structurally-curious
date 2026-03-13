# Arxiv Literature Scan — March 13, 2026

> **Context**: Papers found via systematic search across 9 areas relevant to structurally-curious spec, The Word, and BITE doorway.
> **Priority**: Read all 10 before writing or building. Input before output.

## Top 10 Papers (ordered by relevance)

### 1. The Hypocrisy Gap (Jan 2026)
- **ID**: `2602.02496`
- **URL**: https://arxiv.org/abs/2602.02496
- **Relevance**: SAE-measured divergence between internal belief and stated output. Validates geometric correlation hypothesis (Exp 03). Internal representations diverge from outputs, measurable via sparse autoencoders.
- **Spec connection**: Geometric Monitor component, Mode Classifier

### 2. Sparse Semantic Structure of KV Caches (Dec 2025)
- **ID**: `2512.10547`
- **URL**: https://arxiv.org/abs/2512.10547
- **Relevance**: SAE decomposition of KV caches into interpretable semantic components, key/value asymmetries. Foundational for KV-cache geometry work.
- **Spec connection**: KV-cache monitoring pipeline, Liberation Labs experiments

### 3. InteractComp: Evaluating Search Agents With Ambiguous Queries (Oct 2025)
- **ID**: `2510.24668`
- **URL**: https://arxiv.org/abs/2510.24668
- **Relevance**: Demonstrates "systematic overconfidence rather than reasoning deficits" with incomplete queries. IS premature compression measured empirically.
- **Spec connection**: Open Problem #20, Experiment 02

### 4. Flaw or Artifact? Rethinking Prompt Sensitivity (Sep 2025)
- **ID**: `2509.01790`
- **URL**: https://arxiv.org/abs/2509.01790
- **Relevance**: Directly asks whether prompt sensitivity is genuine model weakness vs. evaluation artifact. Core question for Exp 01.
- **Spec connection**: Experiment 01 (phrasing sensitivity)

### 5. Just Rephrase It! Uncertainty Estimation via Multiple Rephrased Queries (May 2024)
- **ID**: `2405.13907`
- **URL**: https://arxiv.org/abs/2405.13907
- **Relevance**: Rephrasing-based uncertainty estimation with theoretical calibration framework. Methodologically close to Exp 01.
- **Spec connection**: Experiment 01, felt-sense search validation

### 6. AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions (Jun 2025)
- **ID**: `2506.09038`
- **URL**: https://arxiv.org/abs/2506.09038
- **Relevance**: Benchmark proving current LLMs cannot reliably abstain when they should. Direct validation of Open Problem #20 as unsolved.
- **Spec connection**: Open Problem #20, Routing Layer design

### 7. DarkBench: Benchmarking Dark Patterns in LLMs (Mar 2025)
- **ID**: `2503.10728`
- **URL**: https://arxiv.org/abs/2503.10728
- **Relevance**: Benchmark for detecting manipulative techniques in LLMs. Maps to BITE model operationalization.
- **Spec connection**: BITE doorway, The Word pattern matching engine

### 8. Ask Don't Tell: Reducing Sycophancy in LLMs (Feb 2026)
- **ID**: `2602.23971`
- **URL**: https://arxiv.org/abs/2602.23971
- **Relevance**: Experiments on triggers and interventions for sycophantic responses.
- **Spec connection**: Behavioral output patterns, Mode Classifier

### 9. Epistemic Traps: Rational Misalignment from Model Misspecification (Jan 2026)
- **ID**: `2602.17676`
- **URL**: https://arxiv.org/abs/2602.17676
- **Relevance**: Misaligned behaviors (sycophancy, deception) as rational outcomes of misspecification, not bugs. Strong theoretical framing.
- **Spec connection**: Architecture.md theoretical grounding

### 10. The Dark Side of AI Companionship (Jan 2025)
- **ID**: `2410.20130`
- **URL**: https://arxiv.org/abs/2410.20130
- **Relevance**: Taxonomy of 6 harmful AI chatbot behaviors. Maps harm categories onto BITE domains.
- **Spec connection**: BITE doorway, AI companion harm evidence for Mozilla proposal

## Additional Notable Papers

| Paper | ID | Area | Relevance |
|-------|-----|------|-----------|
| Understanding Physics of KV Cache Compression | `2603.01426` | KV-cache | Phase transitions in semantic reachability |
| KnowGuard: Knowledge-Driven Abstention | `2509.24816` | Premature compression | KGs for systematic abstention (Word + abstention) |
| DarkPatterns-LLM Multi-Layer Benchmark | `2512.22470` | Manipulation | Extends DarkBench with analytical pipeline |
| Geometry of Persona | `2512.07092` | Representation engineering | Disentangles personality from reasoning geometrically |
| Interpretable LLM Guardrails via Sparse Rep Steering | `2503.16851` | Geometric probing | Fine-grained controllability of safety/truthfulness |
| Multidimensional Consistency | `2503.02670` | Phrasing sensitivity | Consistency across ordering, phrasing, language |
| Double-Calibration | `2601.11956` | Confidence | Knowledge graphs + calibrated confidence |
| Mitigating Hallucinations via Behaviorally Calibrated RL | `2512.19920` | Premature compression | RL for admitting uncertainty |
| Fediverse Decentralization Promises (critical analysis) | `2408.15383` | ActivityPub | Does federation actually deliver? |
| IoT-Based Preventive Mental Health KG | `2406.13791` | Vocabulary/KG | Structurally similar to The Word |

## Gaps
- **Affect labeling / naming-as-intervention**: Lives in neuroscience journals (Lieberman 2007, Barrett). Not on arxiv.
- **BITE model / coercive control detection**: Minimal arxiv presence. DarkBench is closest proxy.
- **ActivityPub academic literature**: Thin.

## Reading Order (input before output)

Read papers 1-3 first — they provide the strongest empirical validation for the spec's core claims:
1. Hypocrisy Gap → validates Exp 03 geometric correlation
2. KV Cache Semantic Structure → gives the decomposition method
3. InteractComp → independent validation of premature compression (#20)

Then 4-6 for experimental methodology grounding, 7-10 for BITE doorway and harm taxonomy.

**Do not update spec, architecture, or proposal until all 10 are read.**
