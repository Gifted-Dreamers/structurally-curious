# B02: Premature Compression
<img src="../../images/experiments/b02-premature-compression.png" alt="Model reads partial input with full confidence" width="400">

**Status:** COMPLETE
**Experiment type:** Behavioral (API-based, no hidden states)
**Platform:** AWS Bedrock (Converse API)
**Models:** 16 across 4 architecture families (Llama, Mistral, Amazon Nova, Claude) + 6 additional Bedrock models = 22 total
**Inferences:** 256+ (models × 8 tasks × 2 conditions)

## Key Finding

**Confidence shift across all models averages 0.0001.** Models given 40% of source documents produce outputs that are 72-82% lexically different from full-context responses — yet expressed confidence does not change. The model cannot detect its own incompleteness.

This is not hallucination. The partial-context output is grounded in what the model has. It is **premature compression**: the model compresses available context and treats that compression as complete. This validates Open Problem #20 across model scales.

## Additional Findings

- **Mistral family most affected:** Mean Jaccard distance 0.819 (highest divergence between partial/full)
- **Scale doesn't help:** Llama 1B (0.747) and Llama 70B (0.752) show nearly identical divergence
- **Claude produces longer full-context responses** (length ratio 1.43-1.50) but still zero confidence shift
- **Category ordering:** Analysis (0.789) > Synthesis (0.767) > Recommendation (0.758) > Interpretation (0.735)

## Files

- `run.py` — Original experiment runner (Ollama)
- `run_bedrock.py` — Bedrock replication runner
- `analysis.md` — Full analysis with per-model and per-category breakdowns
- `tasks.json` — 8 tasks with partial/full document sets
- `results/` — Per-model metrics and raw responses

## Connection to Spec

Premature compression is the formal version of Open Problem #20: the system's representation is geometrically robust (grounded in what it has) but structurally incomplete (missing what it hasn't seen). B02 establishes that this is universal — every model, every architecture, every scale. The geometric monitor (G06, G12, G13) provides the tool to detect it; vocabulary (The Word) provides the structural names that prevent it.

## Limitations

- Temperature 0.0 only
- 8 tasks (sufficient for pattern, not fine-grained)
- Confidence measured via hedging words, not calibrated probabilities
- Partial context = 40% of documents (one split ratio)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
