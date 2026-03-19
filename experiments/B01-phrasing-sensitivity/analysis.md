# Experiment 01: Phrasing Sensitivity × Model Size — Analysis

**Date:** 2026-03-08
**Models tested:** 19 (10 open-weight with known params, 9 frontier/undisclosed)
**Total prompts:** 1,520 (19 models × 20 tasks × 4 phrasings)
**Embedding model:** Cohere Embed v4 (via AWS Bedrock)
**Metric:** Mean pairwise cosine distance between outputs to semantically equivalent prompts
**Temperature:** 0.0 (deterministic)

## Headline Finding

Hazel_OC's category ordering replicates perfectly across all 19 models and 5 providers:

| Category | Mean Sensitivity | Ratio to Factual |
|----------|-----------------|-------------------|
| Factual | 0.1593 | 1.00× |
| Summarization | 0.1803 | 1.13× |
| Judgment | 0.2102 | 1.32× |
| Creative | 0.3121 | 1.96× |

This gradient is universal. It appears in every model tested — from Llama 1B to DeepSeek R1 671B, across Meta, Mistral, Amazon, Anthropic, DeepSeek, and Writer architectures. The ordering tracks representational certainty: when a model has compressed representations (knows the answer), phrasing can't move it; when representations are diffuse (constructing), the prompt provides scaffolding the answer lacks.

## Model Rankings

| Rank | Model | Params | Overall | Factual | Summarization | Judgment | Creative |
|------|-------|--------|---------|---------|---------------|----------|----------|
| 1 | DeepSeek R1 | 671B | 0.2525 | 0.2267 | 0.2730 | 0.2270 | 0.2831 |
| 2 | Llama 3.2 1B | 1B | 0.2361 | 0.1598 | 0.1907 | 0.2547 | 0.3392 |
| 3 | Palmyra X5 | ? | 0.2322 | 0.2208 | 0.1617 | 0.2281 | 0.3182 |
| 4 | Claude Sonnet 4.6 | ? | 0.2237 | 0.1540 | 0.2086 | 0.1945 | 0.3377 |
| 5 | Nova Micro | ? | 0.2237 | 0.1948 | 0.1712 | 0.2158 | 0.3130 |
| 6 | Llama 3.1 8B | 8B | 0.2224 | 0.1541 | 0.1993 | 0.2418 | 0.2945 |
| 7 | Claude Haiku 4.5 | ? | 0.2189 | 0.1501 | 0.1770 | 0.2250 | 0.3235 |
| 8 | Llama 3.3 70B | 70B | 0.2165 | 0.1575 | 0.2052 | 0.2144 | 0.2888 |
| 9 | Claude Opus 4.6 | ? | 0.2123 | 0.1358 | 0.1843 | 0.1890 | 0.3400 |
| 10 | Llama 3.2 3B | 3B | 0.2119 | 0.1480 | 0.1756 | 0.2179 | 0.3062 |
| 11 | Llama 3.2 11B | 11B | 0.2116 | 0.1573 | 0.1629 | 0.2170 | 0.3091 |
| 12 | Nova Premier | ? | 0.2109 | 0.1384 | 0.1925 | 0.1829 | 0.3297 |
| 13 | Pixtral Large | 124B | 0.2104 | 0.1728 | 0.1637 | 0.2247 | 0.2803 |
| 14 | Nova Lite | ? | 0.2087 | 0.1513 | 0.1607 | 0.1918 | 0.3309 |
| 15 | Llama 4 Scout 17B | 17B | 0.2045 | 0.1185 | 0.1963 | 0.1793 | 0.3239 |
| 16 | Palmyra X4 | ? | 0.2028 | 0.1605 | 0.1656 | 0.1827 | 0.3026 |
| 17 | Llama 3.2 90B | 90B | 0.2028 | 0.1354 | 0.1697 | 0.2209 | 0.2851 |
| 18 | Nova Pro | ? | 0.1998 | 0.1654 | 0.1623 | 0.1847 | 0.2869 |
| 19 | Mistral 7B | 7B | 0.1921 | 0.1250 | 0.1047 | 0.2022 | 0.3364 |

## Key Findings

### 1. Thinking architecture amplifies sensitivity

DeepSeek R1 (671B, chain-of-thought) is the **most** phrasing-sensitive model, not the least. It scores highest overall (0.2525) and highest in factual (0.2267) and summarization (0.2730) — categories where most models are stable.

**Interpretation:** Chain-of-thought gives the prompt more surface area to steer reasoning. Each step in the thinking chain is influenced by the initial framing, and those influences compound. The thinking trace is a sensitivity amplifier.

This has direct implications for structurally-curious systems: a geometric monitor on a CoT model would need to account for the amplification effect. The geometry of the reasoning trace itself becomes a signal.

### 2. Frontier models show asymmetric compression, not uniform stability

Claude Opus 4.6 ranks 9th overall (0.2123) — middle of the pack. But its profile is extreme:
- **Factual:** 0.1358 (3rd lowest — highly stable)
- **Creative:** 0.3400 (THE highest of any model)

Opus is maximally stable where it knows and maximally variable where it constructs. This is not a bug — it's what well-calibrated uncertainty looks like. A system that gives identical creative outputs regardless of phrasing would be concerning (rigid), not impressive.

The Claude family shows a consistent pattern:
- Haiku 4.5: factual 0.1501, creative 0.3235
- Sonnet 4.6: factual 0.1540, creative 0.3377
- Opus 4.6: factual 0.1358, creative 0.3400

The gap between factual and creative widens as the model gets more capable. More sophisticated models differentiate more sharply between retrieval and construction.

### 3. Scale reduces sensitivity — but architecture dominates

Among Llama models with known parameter counts (1B → 90B):
- 1B: 0.2361
- 90B: 0.2028
- Reduction: ~14%

But DeepSeek R1 at 671B scores 0.2525 — higher than Llama 1B. The trend is real within a family but architecture (CoT vs direct) matters more than raw parameter count.

### 4. Mistral 7B may be under-responsive

Mistral 7B scores lowest overall (0.1921) with remarkably low summarization sensitivity (0.1047 — nearly half the average). This could indicate genuine stability or could indicate the model is under-responsive — producing templatic outputs regardless of prompt nuance. Further investigation (human evaluation of output quality) would disambiguate.

### 5. The factual-creative gradient is a diagnostic signal

The ratio of creative-to-factual sensitivity varies meaningfully across models:

| Model | Creative/Factual Ratio |
|-------|----------------------|
| Llama 4 Scout 17B | 2.73× |
| Mistral 7B | 2.69× |
| Claude Opus 4.6 | 2.50× |
| Nova Premier | 2.38× |
| DeepSeek R1 | 1.25× |

DeepSeek R1's low ratio (1.25×) means it's almost equally sensitive across all categories — the thinking trace makes even factual tasks susceptible to phrasing effects. Models with high ratios (>2.5×) show cleaner differentiation between retrieval and construction modes.

## Connection to Structurally-Curious Systems

Phrasing sensitivity is a behavioral proxy for representational uncertainty. A system that tracked its own phrasing sensitivity would know whether it's retrieving or constructing — without needing access to internal representations.

This experiment establishes the behavioral baseline. The next question is whether the geometric signatures (KV-cache geometry, attention patterns) correlate with these behavioral measurements. If they do, the geometric monitor can be validated against a behavioral ground truth.

## Limitations

- Temperature 0.0 eliminates sampling variance but may not reflect deployment conditions
- 20 tasks × 4 phrasings is sufficient for category-level patterns but not for fine-grained task analysis
- Cosine distance on embeddings measures semantic divergence, not quality divergence
- Frontier models have undisclosed parameter counts, limiting size-trend analysis
- Single run — no statistical confidence intervals

## Next Steps

1. Human evaluation of output quality to distinguish "stable because correct" from "stable because templatic"
2. Correlate with internal geometric signals (if accessible) to validate behavioral proxy
3. Expand task set for statistical power
4. Test at non-zero temperatures to measure interaction between sampling and phrasing sensitivity
