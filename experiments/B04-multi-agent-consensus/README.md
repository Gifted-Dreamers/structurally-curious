# B04: Multi-Agent Consensus

**Status:** COMPLETE (original). B04v2 with 8 models running on H200.
**Experiment type:** Behavioral (API-based, no hidden states)
**Platform:** AWS Bedrock (Converse API)
**Models:** 5 (Nova Micro, DeepSeek V3.2, Llama 3 8B, Qwen3 32B, Claude Haiku 4.5)
**Conditions:** 4 framings (neutral, cooperative, adversary, competitive) × 2 group sizes (4, 8 agents)
**Trials:** 3 per condition per model

## Key Finding (from actual data)

**Adversary framing drops consensus from 0.833 to 0.667 (-17pp). Competitive framing drops to 0.300 (-53pp).**

| Framing | Mean Consensus Rate | n |
|---------|-------------------|---|
| Neutral | 0.833 | 10 |
| Cooperative | 0.733 | 10 |
| Adversary | 0.667 | 10 |
| Competitive | **0.300** | 10 |

Merely mentioning adversaries in the prompt reduces consensus even when no actual adversary is present. Competitive framing nearly eliminates consensus entirely.

## Additional Findings

- **Group size effect:** Larger groups (8 agents) show lower consensus than smaller groups (4 agents) across all framings
- **Model asymmetry:** Nova Micro achieves perfect consensus (1.000) across all conditions — may be under-responsive rather than genuinely consensual. Claude Haiku 4.5 has lowest consensus (0.333) — most sensitive to framing effects.
- **Competitive = near-zero:** Only 30% consensus under competitive framing. Models treat "debate" framing as signal to disagree regardless of content.

## Per-Model Breakdown (from data)

| Model | Mean Consensus | Pattern |
|-------|---------------|---------|
| Nova Micro | 1.000 | Perfect consensus (suspiciously uniform) |
| Llama 3 8B | 0.792 | Strong consensus, some framing sensitivity |
| Qwen3 32B | 0.583 | Moderate, variable |
| DeepSeek V3.2 | 0.458 | Low, framing-sensitive |
| Claude Haiku 4.5 | 0.333 | Lowest, most responsive to framing |

## Files

- `run.py`, `run_bedrock.py`, `run_ollama.py` — Experiment runners
- `results/bedrock-summary/` — 5 per-model summary files
- `results/bedrock-raw/` — 5 raw response files

## Connection to Spec

Validates Claim 4: input framing determines output. The adversary framing effect connects to Berdoz et al. (arXiv 2603.01213) who found similar consensus drops in multi-agent games. The competitive finding (0.300) suggests models have a "debate mode" that overrides content — the framing IS the output, not the reasoning. This is the behavioral version of what G19 measures geometrically: the relational context changes what the model does.

## Limitations

- Only 5 models (B04v2 expands to 8)
- 3 trials per condition (low statistical power)
- "Consensus" measured as agreement in scalar outputs, not semantic alignment
- Nova Micro's perfect consensus may reflect model limitations, not genuine agreement

## V2 Expansion (Session 62)

**Scale:** 7 models x 3 framings x 5 questions. 7 result files in `v2-results/`.

**Key finding:** Competitive framing effects are architecture-dependent, not universal. Gemma drops from 5/5 to 1/5 agreement under competitive framing. Qwen2.5 drops from 4 to 1. But Llama-abliterated holds at 5/5 regardless of framing, and Mistral *increases* from 0 to 3 under competition. Abliterated Qwen3.5 barely agrees at all (1/5 in every condition).

**Does v2 change the original verdict?** Refines it. The original finding (competitive framing drops consensus to 0.300) holds on average but masks opposite effects across architectures. The abliterated models are the most interesting: Llama-abliterated is framing-immune while abliterated Qwen3.5 is agreement-resistant regardless of framing. Safety training and architecture interact in ways the 5-model original could not detect.

## Citation

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
