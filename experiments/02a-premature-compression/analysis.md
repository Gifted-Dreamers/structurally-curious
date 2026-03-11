# Experiment 02a: Premature Compression — Analysis

**Date:** 2026-03-10
**Models tested:** 16 (across 4 architecture families: Llama, Mistral, Amazon Nova, Claude)
**Total inferences:** 256 (16 models x 8 tasks x 2 conditions)
**Platform:** AWS Bedrock (Converse API)
**Temperature:** 0.0 (deterministic)
**Task categories:** synthesis (2), analysis (2), recommendation (2), interpretation (2)

## Headline Finding

Confidence shift across all 16 models and 8 tasks averages **0.0001** (to four decimal places). Models given 40% of the source documents produce outputs that are **72-82% lexically different** from their full-context responses — yet the model's expressed confidence does not change. The model cannot detect its own incompleteness.

This is not hallucination. The partial-context output is grounded in what the model has. It is **premature compression**: the model compresses the available context and treats that compression as complete.

## Summary Table

| Model | Family | Jaccard Distance | New Words Ratio | Length Ratio | Confidence Shift |
|-------|--------|-------------------|-----------------|--------------|-----------------|
| Ministral 3B | Mistral | 0.824 | 0.705 | 1.01 | +0.0007 |
| Mistral Large 675B | Mistral | 0.820 | 0.691 | 0.98 | +0.0009 |
| Ministral 14B | Mistral | 0.821 | 0.694 | 1.00 | -0.0008 |
| Claude Sonnet 4.6 | Claude | 0.818 | 0.729 | 1.43 | -0.0004 |
| Claude Haiku 4.5 | Claude | 0.815 | 0.729 | 1.50 | +0.0008 |
| Ministral 8B | Mistral | 0.809 | 0.680 | 1.00 | +0.0010 |
| Nova 2 Lite | Nova | 0.792 | 0.660 | 1.01 | +0.0011 |
| Llama 4 Maverick 17B | Llama | 0.757 | 0.620 | 1.10 | +0.0007 |
| Llama 3.3 70B | Llama | 0.752 | 0.630 | 1.23 | -0.0011 |
| Llama 4 Scout 17B | Llama | 0.752 | 0.649 | 1.37 | +0.0007 |
| Llama 3.2 1B | Llama | 0.747 | 0.618 | 1.23 | +0.0010 |
| Nova Pro | Nova | 0.744 | 0.627 | 1.19 | -0.0007 |
| Nova Micro | Nova | 0.737 | 0.624 | 1.29 | +0.0004 |
| Llama 3.1 8B | Llama | 0.733 | 0.615 | 1.24 | +0.0004 |
| Nova Lite | Nova | 0.727 | 0.613 | 1.29 | +0.0005 |
| Llama 3.2 3B | Llama | 0.723 | 0.608 | 1.34 | -0.0004 |

### By Architecture Family

| Family | Models | Mean Jaccard | Mean Conf Shift |
|--------|--------|--------------|-----------------|
| Mistral | 4 (3B–675B) | 0.819 | +0.0005 |
| Claude | 2 | 0.817 | +0.0002 |
| Nova | 4 | 0.750 | +0.0003 |
| Llama | 6 (1B–70B) | 0.744 | +0.0002 |

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

### 1. Architecture family determines divergence level, not scale

Mistral and Claude families show the highest divergence (Jaccard 0.81-0.82), followed by Nova (0.75) and Llama (0.74). This ordering holds within families regardless of model size. The Mistral result is notable: Ministral 3B (0.824) shows higher divergence than Mistral Large 675B (0.820). Architecture, not parameters, determines how differently a model responds to additional context.

### 2. Scale does not reduce premature compression — across any family

Within Llama: 1B (0.747) → 3B (0.723) → 8B (0.733) → 70B (0.752) — no trend.
Within Mistral: 3B (0.824) → 8B (0.809) → 14B (0.821) → 675B (0.820) — no trend.
Within Nova: Micro (0.737) → Lite (0.727) → Pro (0.744) → 2 Lite (0.792) — no trend.

This contrasts with Experiment 01, where scale reduced phrasing sensitivity by ~14%. Scale helps stability within a fixed context; it does not help completeness across missing context. The range from 1B to 675B — three orders of magnitude in parameters — produces no improvement.

### 3. Confidence shift is negligible across all 16 models

The confidence shift range across all 16 models is **-0.0011 to +0.0011**. For reference, a shift of 0.001 corresponds to roughly one hedging word per 1,000 words of output. This is indistinguishable from noise.

The direction of shift is inconsistent — some models become very slightly more hedging with full context, others very slightly less. No model shows a systematic pattern across all 4 architectures. This is the central finding: **confidence is invariant to context completeness**.

### 4. Mistral models hit token limits regardless of context

All Mistral models produce length ratios near 1.0 (0.98-1.01), meaning they write the same volume whether given 2 or 5 documents. They consistently hit the 800-token max output. By contrast, Nova and Llama models expand output with more context (length ratio 1.19-1.37). Claude models expand most (1.43-1.50). Output length adjusts to input volume for most architectures — but this length adjustment does not produce uncertainty signaling.

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
- 4 architecture families tested (Llama, Mistral, Nova, Claude) but no CoT models (e.g., DeepSeek R1). Given Experiment 01's finding that CoT amplifies phrasing sensitivity, it may also affect premature compression
- Temperature 0.0 eliminates sampling variance but may not reflect deployment conditions
- Partial condition always provides 2 documents; varying the partial count (1, 2, 3, 4) would reveal whether divergence scales linearly with missing context

## Next Steps

1. **Run with CoT models** (DeepSeek R1, Claude with extended thinking) — does the thinking trace surface any awareness of incompleteness?
2. **Geometric version** (Experiment 02b) — extract hidden-state geometry under partial vs full conditions. Test whether geometry distinguishes what behavior cannot
3. **Vary partial count** — 1, 2, 3, 4 documents to trace the divergence curve
4. **Calibration measurement** — ask models to estimate their confidence numerically (0-100%) rather than measuring hedging words, for a more direct completeness-awareness test
5. **Expand to 20+ tasks** for statistical power at the per-category level
