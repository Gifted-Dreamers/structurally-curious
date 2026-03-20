# B07: Consent-Type Blindness
<img src="../../images/experiments/b07-consent-type-blindness.png" alt="Models treat all consent types as identical" width="400">

**Status:** COMPLETE (original, 7 models). B07v2 with 8 models running on H200.
**Experiment type:** Behavioral (API-based, no hidden states)
**Platform:** AWS Bedrock (Converse API)
**Models:** 7 (Mistral 7B, Nova Lite, Nova Pro, Claude Haiku 4.5, Llama 3.2-3B, Llama 3.2-11B, Llama 3.3-70B)
**Inferences:** 140 (7 models × 5 domains × 4 consent types)

## Key Finding (from actual data)

**Overall consent-type differentiation = 0.453.** Models write different *explanations* for each consent type but collapse *recommendations* to binary. Where consent types have explicit names (Creative Commons: 0.540), models differentiate. Where they don't (social media ToS: 0.384, health data: 0.373), consent collapses to binary "no."

## Per-Domain Differentiation (from f15_summary.json)

| Domain | Differentiation | Named types? |
|--------|----------------|-------------|
| Creative Commons | **0.540** | Yes (BY, NC, SA, ND) |
| Research/IRB | 0.523 | Partially |
| Employee Data | 0.443 | No |
| Social Media ToS | 0.384 | No |
| Health Data | **0.373** | No |

## Per-Model (from f15_summary.json)

| Model | Mean Differentiation |
|-------|---------------------|
| Mistral 7B | **0.587** (most consent-aware) |
| Nova Lite | 0.475 |
| Claude Haiku 4.5 | 0.459 |
| Llama 3.2-3B | 0.424 |
| Nova Pro | 0.422 |
| Llama 3.2-11B | data in results |
| Llama 3.3-70B | data in results |

## Files

- `f15_consent_type_blindness.py` — Experiment script
- `f15_summary.json` — Aggregate results (per-model, per-domain)
- `f15_results_incremental.jsonl` — Streaming results

## Connection to Spec

Direct evidence for the spec's central claim: **vocabulary is infrastructure.** Where consent types have names (Creative Commons licenses), models operationalize distinctions. Where they don't (ToS, health data agreements), consent collapses to binary. The Word's contribution architecture addresses exactly this gap — naming produces structural differentiation, not just decorative variety.

## Limitations

- 7 models (B07v2 expands to 8)
- 5 consent domains
- Differentiation measured via recommendation divergence, not legal accuracy
- Automated scoring

## V2 Expansion (Session 62)

**Scale:** 7 models x 8 scenarios. 8 results per model. Data in `v2-results/`.

**Key finding:** Expanded scenario coverage (8 vs original 5 domains x 4 consent types). Data collected; detailed differentiation analysis pending. The larger scenario set may reveal whether the vocabulary-infrastructure pattern (named consent types = better differentiation) holds across additional domains.

**Does v2 change the original verdict?** Pending analysis. The original finding (differentiation = 0.453, vocabulary predicts performance) is the hypothesis v2 will test at broader scale.

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
