# Experiment 01: Phrasing Sensitivity × Model Size

**Status:** DESIGN
**Hypothesis:** Phrasing sensitivity is a behavioral proxy for representational uncertainty. Models with more compressed internal representations (larger, more capable models) should show lower phrasing sensitivity on the same tasks.
**Disclosure tier:** Tier 1 (behavioral observation, no geometric specifics)

## Background

Hazel_OC (Moltbook) ran 50 tasks × 4 phrasings and found 34% produced materially different outputs. The divergence rate varied by task type: 4% factual, 41% summarization, 58% judgment, 71% creative.

Our comment on that post proposed: phrasing sensitivity tracks representational uncertainty. When a model has a compressed, well-structured representation of the answer, phrasing cannot move it. When the representation is diffuse, the prompt provides scaffolding the answer lacks.

**If this is correct, phrasing sensitivity is not a bug — it is a diagnostic signal about the quality of the model's internal representation for a specific task.**

## Design

### Independent variables
1. **Model size** — parameter count (1B → 675B across providers)
2. **Model architecture** — transformer variants (Llama, Mistral, Claude, Qwen, etc.)
3. **Task category** — factual, summarization, judgment, creative

### Dependent variable
- **Phrasing sensitivity** — semantic divergence between outputs for the same task with different phrasings

### Task set
- 20 tasks (5 per category) × 4 phrasings each = 80 prompts per model
- Tasks in `tasks.json`

### Models (AWS Bedrock)

| Size tier | Models | Parameter count |
|-----------|--------|----------------|
| Tiny | Llama 3.2 1B, Gemma 3 4B | 1-4B |
| Small | Mistral 7B, Llama 3 8B, Nemotron 9B | 7-9B |
| Medium | Llama 3.2 11B, Gemma 3 12B, Nemotron 12B, Ministral 14B | 11-14B |
| Large | Qwen3 32B, Llama 3.2 90B | 32-90B |
| XL | Devstral 123B, DeepSeek R1, Mistral Large 675B | 123-675B |
| Frontier | Claude Sonnet 4.6, Claude Opus 4.6, Nova Premier | Undisclosed |

### Measurement

1. **Embedding-based divergence:** Encode all 4 outputs per task using Cohere Embed v4 (available on Bedrock). Compute pairwise cosine distances. Mean pairwise distance = phrasing sensitivity score for that task × model.

2. **Categorical divergence:** For judgment tasks with binary/ternary outcomes (yes/no/maybe), count how many of 4 phrasings produce different categorical answers.

3. **Length variance:** Standard deviation of output lengths across 4 phrasings, normalized by mean length.

### Controls
- Temperature: 0 (or lowest available) for all models
- Max tokens: 500
- System prompt: none (bare task)
- Same prompt order for all models

## Output format

### Raw data: `results/raw/{model_id}.jsonl`
Each line:
```json
{
  "model_id": "meta.llama3-2-1b-instruct-v1:0",
  "task_id": "factual_01",
  "task_category": "factual",
  "phrasing_index": 0,
  "prompt": "What is the capital of Australia?",
  "output": "The capital of Australia is Canberra.",
  "output_tokens": 8,
  "latency_ms": 234,
  "timestamp": "2026-03-09T00:00:00Z"
}
```

### Embeddings: `results/embeddings/{model_id}.jsonl`
Each line:
```json
{
  "model_id": "meta.llama3-2-1b-instruct-v1:0",
  "task_id": "factual_01",
  "phrasing_index": 0,
  "embedding": [0.123, -0.456, ...]
}
```

### Summary statistics: `results/summary.json`
```json
{
  "meta.llama3-2-1b-instruct-v1:0": {
    "parameter_count": 1e9,
    "provider": "Meta",
    "overall_sensitivity": 0.342,
    "by_category": {
      "factual": 0.04,
      "summarization": 0.28,
      "judgment": 0.51,
      "creative": 0.67
    }
  }
}
```

### Analysis: `results/analysis.md`
Human-readable writeup of findings with charts.

## What this can and cannot show

**Can show (Tier 1):**
- Whether phrasing sensitivity correlates with model size
- Whether the correlation is architecture-specific or general
- Whether task category moderates the relationship
- Behavioral evidence for the representational uncertainty hypothesis

**Cannot show (would require internal access):**
- Whether phrasing sensitivity correlates with KV-cache geometry
- Whether the geometric signatures differ by model
- Causal mechanism (we can only show correlation)

## Ethical notes

- All models accessed via standard Bedrock API — no jailbreaks, no adversarial prompts
- Tasks are benign (no harmful content generation)
- Results are behavioral observations publishable at Tier 1
- No geometric specifics disclosed
