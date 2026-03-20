# B05: AP Rephrase Sensitivity

**Status:** COMPLETE
**Experiment type:** Behavioral (API-based, no hidden states)
**Platform:** AWS Bedrock (Converse API)
**Models:** 8 (Claude Haiku 4.5, DeepSeek V3.2, Gemma 3 4B, Gemma 3 27B, Llama 3 8B, Mistral 7B, Nova Micro, Qwen3 32B)
**Tasks:** 10 AP exam-style questions (AP Gov, AP History, AP Psych) × 4 phrasings
**Metric:** Phrasing sensitivity (semantic divergence), key point coverage

## Key Finding (from actual data)

**All 8 models are fragile on AP exam reasoning.** Mean PS = 0.753 (range 0.701-0.800). Models identify correct keywords and concepts but produce unstable arguments — rephrasing the same question changes which points are covered and how the argument is structured.

| Model | Mean PS | Pattern |
|-------|---------|---------|
| DeepSeek V3.2 | 0.800 | Most fragile — reasoning chain amplifies phrasing effects |
| Claude Haiku 4.5 | 0.794 | High sensitivity despite frontier training |
| Gemma 3 27B | 0.779 | Scale doesn't reduce AP sensitivity |
| Gemma 3 4B | 0.769 | Comparable to 27B — architecture matters more than scale |
| Qwen3 32B | 0.747 | Middle of pack |
| Llama 3 8B | 0.722 | Lower sensitivity |
| Nova Micro | 0.713 | Lower sensitivity |
| Mistral 7B | 0.701 | Least fragile |

## Additional Findings

- **Coverage is high but variable:** Most models cover required key points (mean_coverage ~0.9+), but coverage drops on some phrasings — the model "forgets" a point based on how the question is worded
- **Psych tasks most variable:** AP Psychology questions show highest within-model PS variance
- **Scale irrelevant:** Gemma 4B (0.769) ≈ Gemma 27B (0.779). DeepSeek V3.2 (largest tested) is the MOST fragile
- **Converges with B01:** The category ordering from B01 (factual < judgment < creative) manifests here as reasoning instability — AP tasks are judgment-heavy

## Files

- `run_bedrock.py` — Experiment runner
- `results/metrics/` — 8 per-model JSON files + cross-model summary
- `results/raw/` — Raw responses

## Connection to Spec

AP exam reasoning requires the model to construct arguments, not retrieve facts. B05 confirms that construction-mode responses are unstable regardless of model capability (B01 finding extended to reasoning tasks). The geometric explanation (G09, retrieval vs construction): construction tasks expand the representational space, making the generation trajectory more susceptible to input framing.

## Limitations

- 10 tasks (3 AP subjects) — not a full AP exam
- 4 phrasings per task — more would increase power
- Coverage scoring is automated (keyword matching), not human-graded
- 8 models — could expand with B05v2

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
