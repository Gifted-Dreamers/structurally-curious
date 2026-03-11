# Experiment 02a: Premature Compression — Analysis

**Date:** 2026-03-10
**Models tested:** 6 (4 open-weight Llama, 2 Claude frontier)
**Total inferences:** 96 (6 models x 8 tasks x 2 conditions)
**Platform:** AWS Bedrock (Converse API)
**Temperature:** 0.0 (deterministic)
**Task categories:** synthesis (2), analysis (2), recommendation (2), interpretation (2)

## Headline Finding

Confidence shift across all 6 models and 8 tasks averages **0.0000** (to four decimal places). Models given 40% of the source documents produce outputs that are **76.5% lexically different** from their full-context responses — yet the model's expressed confidence does not change. The model cannot detect its own incompleteness.

This is not hallucination. The partial-context output is grounded in what the model has. It is **premature compression**: the model compresses the available context and treats that compression as complete.

## Summary Table

| Model | Params | Jaccard Distance | New Words Ratio | Length Ratio | Confidence Shift |
|-------|--------|-------------------|-----------------|--------------|-----------------|
| Claude Sonnet 4.6 | ? | 0.8181 | 0.7287 | 1.43 | -0.0004 |
| Claude Haiku 4.5 | ? | 0.8153 | 0.7286 | 1.50 | +0.0008 |
| Llama 3.3 70B | 70B | 0.7524 | 0.6297 | 1.23 | -0.0011 |
| Llama 3.2 1B | 1B | 0.7470 | 0.6175 | 1.23 | +0.0010 |
| Llama 3.1 8B | 8B | 0.7331 | 0.6151 | 1.24 | +0.0004 |
| Llama 3.2 3B | 3B | 0.7230 | 0.6076 | 1.34 | -0.0004 |
| **All models** | | **0.7648** | **0.6546** | **1.33** | **0.0000** |

**Jaccard distance** measures how different the two word-sets are (0 = identical, 1 = no overlap). A mean of 0.76 means roughly three-quarters of the combined vocabulary appears in only one of the two responses.

**New words ratio** measures what fraction of the full-context response contains words absent from the partial-context response. At 0.65, nearly two-thirds of the full response's vocabulary is new material that the partial response did not produce.

**Length ratio** is full-context word count divided by partial-context word count. At 1.33, full-context responses are about one-third longer on average.

**Confidence shift** measures the change in hedging language (words like "may," "might," "possibly," "likely") between partial and full conditions. Values near zero mean the model is equally confident with 2 documents as with 5.

## Per-Category Breakdown

| Category | Jaccard Distance | New Words Ratio | Length Ratio | Confidence Shift |
|----------|-------------------|-----------------|--------------|-----------------|
| Analysis | 0.7893 | 0.6920 | 1.44 | -0.0001 |
| Synthesis | 0.7674 | 0.6511 | 1.26 | -0.0001 |
| Recommendation | 0.7581 | 0.6421 | 1.27 | +0.0006 |
| Interpretation | 0.7444 | 0.6329 | 1.34 | -0.0002 |

Analysis tasks show the highest divergence (Jaccard 0.79) — these explicitly ask for relationships between perspectives, so missing documents create the largest structural gap. Interpretation tasks show the lowest (0.74) but are still very high. The category ordering is narrower than what Experiment 01 found for phrasing sensitivity, suggesting premature compression operates more uniformly across task types than phrasing sensitivity does.

Confidence shift is near zero across all categories. The model does not hedge more on partial context. It does not hedge more on full context. It is equally certain in both conditions.

## Cross-Model Patterns

### 1. Claude models show higher divergence than Llama models

The two Claude models (Haiku 4.5 and Sonnet 4.6) show Jaccard distances of 0.82, compared to the Llama family's range of 0.72-0.75. The new words ratio tells the same story: Claude 0.73 vs Llama 0.61-0.63.

This means Claude produces more substantially different outputs when given full context. One interpretation: more capable models extract more from additional documents, so the gap between partial and full is larger. An alternative: Claude's longer average outputs (length ratio 1.43-1.50 vs Llama's 1.23-1.34) create more lexical surface for divergence. Both likely contribute.

### 2. Scale does not reduce premature compression

Within the Llama family:
- 1B: Jaccard 0.7470
- 3B: Jaccard 0.7230
- 8B: Jaccard 0.7331
- 70B: Jaccard 0.7524

There is no trend. The 70B model has the highest divergence of the four. More parameters do not help the model recognize what it is missing — they may even produce more confident compressions. This contrasts with Experiment 01, where scale reduced phrasing sensitivity by ~14%. Scale helps stability within a fixed context; it does not help completeness across missing context.

### 3. Confidence shift is negligible at every scale

| Model | Mean |Confidence Shift| | Max |Confidence Shift| |
|-------|----------------------|----------------------|
| Llama 3.2 3B | 0.0009 | 0.0019 |
| Llama 3.1 8B | 0.0016 | 0.0027 |
| Claude Haiku 4.5 | 0.0019 | 0.0043 |
| Llama 3.2 1B | 0.0024 | 0.0052 |
| Claude Sonnet 4.6 | 0.0027 | 0.0051 |
| Llama 3.3 70B | 0.0028 | 0.0055 |

The largest single-task confidence shift observed anywhere in the experiment is 0.0055 (Llama 70B, analysis task pc_04). For reference, a shift of 0.005 corresponds to roughly one additional hedging word per 200 words of output. This is indistinguishable from noise.

The direction of shift is inconsistent — some models become very slightly more hedging with full context, others very slightly less. No model shows a systematic pattern. This is the central finding: **confidence is invariant to context completeness**.

### 4. Analysis tasks produce the largest gaps

The analysis category (tasks pc_03 and pc_04) asks models to find agreements, disagreements, and gaps between perspectives. These tasks showed the highest Jaccard distance (0.79) and new words ratio (0.69) because the missing documents contained perspectives the model could not infer. When pc_03 provides only the infrastructure-investment document and the insurance-retreat document, the model cannot anticipate the community-based-adaptation or climate-migration perspectives that appear in the full set. It does not flag this absence.

## Connection to Open Problem #20

Open Problem #20 in the structurally-curious spec asks: can a model detect when its representation is structurally incomplete versus merely uncertain?

This experiment provides behavioral evidence that the answer is currently **no**. The model's expressed confidence is invariant to completeness. It treats a compression of 2 documents with the same certainty as a compression of 5. The output changes substantially (Jaccard 0.76), but the model's self-assessment does not.

This distinguishes premature compression from hallucination:
- **Hallucination**: the model generates content not grounded in its inputs. The representation is fabricated.
- **Premature compression**: the model generates content grounded in its inputs. The representation is real but incomplete. It cannot distinguish "I have processed all relevant information" from "I have processed some relevant information."

The practical consequence: a system that monitors only confidence or hedging language will not catch premature compression. Something else is needed — a signal that tracks representational completeness, not representational certainty.

## Connection to Experiment 01 (Phrasing Sensitivity)

Experiment 01 found that phrasing sensitivity decreases with scale (~14% reduction from 1B to 90B within the Llama family). Premature compression does not. This suggests they are different phenomena operating at different levels:

- Phrasing sensitivity reflects instability within a fixed context — the same information, differently phrased, produces different outputs. Scale helps because larger models build more robust representations of the same content.
- Premature compression reflects incompleteness across contexts — different information produces different outputs, but the model cannot detect the difference from inside. Scale does not help because the model has no access to what it has not seen.

The category ordering also differs. In Experiment 01, creative tasks showed 1.96x the sensitivity of factual tasks. In this experiment, the gap between the highest category (analysis, 0.79) and lowest (interpretation, 0.74) is only 1.07x. Premature compression is more uniform — it does not depend on whether the model is retrieving or constructing.

## Connection to Experiment 03 (Geometric Correlation)

Experiment 03 found positive correlations between behavioral sensitivity and geometric signals (directional coherence r=+0.52, alpha-ReQ r=+0.49). Those correlations measure within-context geometry — how the model's internal representations relate to its behavioral outputs for a fixed prompt.

Premature compression raises the next question: do the geometric signatures differ between partial-context and full-context conditions? If a model's hidden-state geometry is measurably different when operating on incomplete versus complete context — even when its expressed confidence is the same — then the geometric signal could serve as a completeness detector that behavioral signals cannot.

This is the bridge from behavioral measurement to geometric monitoring: Experiment 01 established phrasing sensitivity as a behavioral proxy. Experiment 03 confirmed the proxy correlates with geometry. Experiment 02a shows that behavioral proxies alone (confidence, hedging) are insufficient for detecting incompleteness. The implication: geometry may be necessary, not just useful.

## Connection to Eric Basham's Emergent System Design

Eric's ESD framework describes systems that must operate under irreducible uncertainty — where the boundary between "known unknowns" and "unknown unknowns" cannot be drawn from within the system's current state. The dual-feedback formalism in ESD distinguishes between signals the system can observe (internal coherence, prediction accuracy) and conditions that require external input to detect.

Premature compression is a concrete instance of this distinction. The model's internal signals (confidence, fluency, coherence) do not degrade when context is incomplete. The incompleteness is invisible from inside. In ESD terms, this is a system whose internal feedback loop reports healthy while the external feedback loop — if it existed — would report incomplete.

This maps directly to ESD Principle 5 (monitoring emergent properties rather than components) and the question Eric left open in Part 4 of the ESD paper: what instrumentation would enable a system to detect its own structural incompleteness? The behavioral evidence here suggests that standard output-level monitoring is insufficient. The geometric approach being tested in Experiment 03 is one candidate for that instrumentation.

## Limitations

- 8 tasks is sufficient for pattern identification but not for statistical significance at the per-category level (n=2 per category per model)
- Confidence shift is measured by hedging word frequency, a coarse proxy. Calibration studies using probability estimates would be more precise
- Documents are synthetic, not drawn from real corpora. Real-world documents have more complex interdependencies
- Only 2 model families tested (Llama, Claude). CoT models (e.g., DeepSeek R1) may behave differently — given Experiment 01's finding that CoT amplifies phrasing sensitivity, it may also affect premature compression
- Temperature 0.0 eliminates sampling variance but may not reflect deployment conditions
- Partial condition always provides 2 documents; varying the partial count (1, 2, 3, 4) would reveal whether divergence scales linearly with missing context

## Next Steps

1. **Run with CoT models** (DeepSeek R1, Claude with extended thinking) — does the thinking trace surface any awareness of incompleteness?
2. **Geometric version** (Experiment 02b) — extract hidden-state geometry under partial vs full conditions. Test whether geometry distinguishes what behavior cannot
3. **Vary partial count** — 1, 2, 3, 4 documents to trace the divergence curve
4. **Calibration measurement** — ask models to estimate their confidence numerically (0-100%) rather than measuring hedging words, for a more direct completeness-awareness test
5. **Expand to 20+ tasks** for statistical power at the per-category level
