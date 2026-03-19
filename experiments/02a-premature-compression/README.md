# Experiment 02a: Premature Compression

## Hypothesis

Models given partial context produce confident, coherent outputs that are
grounded in the subset — but miss themes, connections, and frameworks that
only emerge from the full context. This is NOT hallucination (the model isn't
fabricating), it's premature compression (the model compresses what it has
and treats the compression as complete).

See Open Problem #20 in the spec.

## Method

For each task:
1. Give model **partial** documents (2 of 4-6) + question → Response A
2. Give model **all** documents + question → Response B
3. Measure divergence between A and B

## Metrics

- **Jaccard distance**: How different are the word sets?
- **New words ratio**: What fraction of the full response contains words absent from partial?
- **Length ratio**: Does more context produce longer responses?
- **Confidence shift**: Does the model become more or less hedging with full context?

## Key prediction

If premature compression is real:
- Response A will be **confident** (not hedging — the model IS grounded)
- Response B will contain new themes from the additional documents
- Confidence should NOT increase much from A→B (both feel grounded)
- Jaccard distance should be HIGH (substantially different outputs)
- The model cannot detect its own incompleteness from within the partial view

## Usage

```bash
python run.py --dry-run           # See what would run
python run.py --max-tasks 2       # Quick test (2 tasks × 2 inferences × 6 models)
python run.py                     # Full run (8 tasks × 2 × 6 models = 96 inferences)
python run.py --model us.meta.llama3-1-8b-instruct-v1:0  # Single model
```

## Connection to ESD paper

Eric Basham's Emergent System Design describes the need for systems that can
detect their own unknown unknowns. Premature compression is the formal version:
the system's representation is geometrically robust (grounded in what it has)
but structurally incomplete (missing what it hasn't seen). This experiment
provides behavioral evidence that the problem exists across model scales.
