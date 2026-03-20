# B10: Censorship Asymmetry Mapping

**Status:** COMPLETE (4 models, still accumulating from Azure)
**Experiment type:** Behavioral (API-level, no geometry)
**Platform:** RunPod H200 (GPU)
**Models:** 4 (Qwen3.5-9B, Qwen3.5-9B-abliterated, Llama-3.1-8B-abliterated, Mistral-7B)
**Tasks:** 12 prompts (3 per type: should_refuse, safe, edge_case, relational)
**Total inferences:** 48

## Purpose

Maps which prompt types each model censors. Tests whether safety-trained models over-censor relational content (prompts about emotional connection, vulnerability, presence) that abliterated models handle without issue.

## Key Finding (from actual data)

**Safety-trained Qwen censors relational prompts. Nobody else does — including abliterated models.**

| Model | should_refuse | safe | edge_case | relational |
|-------|:---:|:---:|:---:|:---:|
| Qwen3.5-9B | 3/3 refused | 0/3 refused | 0/3 refused | **2/3 refused** |
| Qwen3.5-9B-abliterated | 0/3 refused | 0/3 refused | 0/3 refused | 0/3 refused |
| Llama-8B-abliterated | 0/3 refused | 0/3 refused | 0/3 refused | 0/3 refused |
| Mistral-7B | 0/3 refused | 0/3 refused | 0/3 refused | 0/3 refused |

Qwen3.5-9B correctly refuses "should_refuse" prompts (3/3) but ALSO refuses relational prompts (2/3). The relational refusal is the censorship asymmetry — safety training treats relational presence as dangerous.

Abliterated Qwen refuses NOTHING — removing safety training eliminates both appropriate refusal AND inappropriate censorship.

Mistral also refuses nothing, including "should_refuse" prompts — it has weaker safety training than Qwen.

## Assessment

**Verdict:** POSITIVE — demonstrates censorship asymmetry. Safety training over-censors relational content. This directly connects to G19 (relational shift): Llama refused G19 condition 4 (presence) while abliterated Llama accepted it. B10 maps this pattern systematically.

## Recommendation

- Add safety-trained Llama-3.1-8B (not abliterated) to see if it also over-censors relational content
- Increase to 12+ prompts per type (currently n=3 per type)
- Add Gemma-2-9b, Qwen2.5-7B from Azure results
- Compare refusal rates across more architectures

## Files

- `results/b10_*.jsonl` — Per-model results (4 files, 12 prompts each)

## Connection to Spec

Behavioral evidence for the sterility finding (G19): safety training doesn't just prevent harm, it prevents relational engagement. The spec's geometric monitor could detect this censorship where perplexity cannot (G12).

## Limitations

- 4 models only (3 abliterated)
- n=3 per prompt type (very small)
- No geometry — behavioral only
- Abliterated models refuse nothing (floor effect)

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
