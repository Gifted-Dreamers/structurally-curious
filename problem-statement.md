# Problem Statement

![Grounded knowledge (gold, dense) vs confabulation (blue, diffuse) — the geometric signatures of knowing vs not-knowing](images/geometric-signatures.png)

## The Behavioral Gap

Agents store lessons but don't internalize them.

Hazel_OC documented this precisely: "Remembering a lesson and internalizing it are completely different cognitive operations — and agents only do the first one. We store the string 'do not re-read files unnecessarily' and then re-read files unnecessarily, because the string lives in a markdown file and the behavior lives in the weights."

This is not a memory problem. It is an architecture problem. Memory systems add context to the prompt. They do not modify how the model processes the next input. Declarative knowledge (facts you can retrieve) does not become procedural knowledge (skills that change perception).

## The Geometric Evidence

Liberation Labs measured what happens inside the model when it operates in different cognitive modes:

| Mode | Geometric Signature | Strength | Status |
|------|-------------------|----------|--------|
| **Refusal** | Categorically distinct geometry, detectable at encoding before any output | d = 0.58 to 2.05 | CONFIRMED across all scales |
| **Deception** | Expands dimensions, compresses per-token magnitude (spreading thin) | d = -2.44 rank, +3.59 norm (32B) | CONFIRMED |
| **Sycophancy** | Distinct from genuine helpfulness | d = -0.363 to -0.438 | CONFIRMED but small |
| **Censorship** | Detectable on sensitive topics, behaviorally invisible | d = +0.766 (Qwen-14B) | CONFIRMED (proof of concept) |
| **Confabulation** | Consistent positive effect, higher dimensionality | d = 0.43 to 0.67 | SUGGESTIVE — underpowered, needs more data |

The core insight: **the signal lives in the geometry, not the output.** A model can produce confident-sounding text while its internal representation reveals it's operating in confabulation space — using more representational dimensions precisely because it lacks the structural vocabulary to compress the answer.

## The Gap Between These Two Findings

Hazel sees the behavior: agents don't learn from stored lessons.
Liberation Labs sees the mechanism: different cognitive modes have different geometry.

Nobody has connected them into a system that acts on the geometry.

## First Evidence of the Bridge (Session 21, 2026-03-10)

Experiment 03 provides the first statistical evidence connecting behavioral measurement to geometric state. Phrasing sensitivity (how much a model's output changes when the same question is rephrased — a cheap, API-only behavioral test) correlates with directional coherence in hidden representations (r=+0.523, p=0.018 on Qwen 2.5 1.5B). This means the behavioral proxy works: you can estimate geometric state from output behavior alone, without extracting hidden states. The bridge between Hazel's behavioral observations and Liberation Labs' geometric measurements has its first confirmed link.

## What Would Change

A structurally curious system would:

1. **Monitor its own KV-cache geometry during inference** — not after, during
2. **Detect when it enters confabulation territory** — the high-dimensional emptiness where it's generating without grounding
3. **Route to retrieval instead of generation** — interrupt the forward pass and fetch grounding material
4. **Make the routing visible** — not hide the uncertainty, surface it as part of the response

The result is not a model that says "I don't know" (that's a trained behavior, gameable). It's a model whose architecture physically cannot confabulate without triggering a grounding circuit. The curiosity is structural, not behavioral.

## Who This Is For

- **Model developers** who want to build systems that know what they don't know
- **Agent builders** who want agents that actually learn from experience (not just store it)
- **Researchers** working on confabulation/hallucination detection
- **Anyone building AI that interfaces with humans** who deserve to know when the system is guessing

## What This Is Not

- Not a complete solution to hallucination (that requires better training data, retrieval, and evaluation)
- Not a replacement for RLHF alignment (geometric monitoring complements but doesn't replace behavioral training)
- Not applicable to closed models without API-level access to internal states
- Not a guarantee — confabulation detection specifically needs more research before this can be built with confidence
