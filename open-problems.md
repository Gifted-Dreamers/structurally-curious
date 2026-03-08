# Open Problems

## Critical (blocks the whole spec)

### 1. Confabulation detection needs statistical confirmation
- Current: d = 0.43-0.67, consistent but underpowered
- Needed: larger sample size with proper Holm-Bonferroni correction
- Who could do this: Liberation Labs (they have the infrastructure), or anyone with access to open-weight models and their KV measurement code
- **Status update (2026-03-08):** Direct collaboration path exists — project partner works with Cassidy, who hosts the Liberation Labs server. Next step: coordinate on expanded sample design.
- If this fails: the spec still works for deception/sycophancy/censorship detection, but the confabulation→retrieval loop — the most novel component — falls away

### 2. Real-time SVD performance
- Full SVD per token is too expensive for production inference
- Randomized SVD (rSVD) reduces cost but introduces approximation error
- Unknown: how much approximation can the classifier tolerate before signal degrades?
- Approach: benchmark rSVD at various k values against full SVD on existing data

## Important (affects quality but doesn't block)

### 3. Model-specific calibration
- Geometric signatures vary by architecture family (Qwen expands for refusal, TinyLlama compresses)
- The classifier needs per-family or per-model calibration
- Could a "geometric fingerprint" step auto-calibrate on a standardized probe set?

### 4. Token-level vs segment-level granularity
- Should we monitor geometry per-token, per-sentence, or per-response?
- Per-token: highest resolution, highest cost
- Per-segment: lower cost, but might miss within-sentence transitions
- Liberation Labs data is response-level — extending to sub-response needs new measurements

### 5. The sycophancy counter-prompt
- Injecting "is this what I actually assess?" mid-generation is itself a prompt manipulation
- Could this trigger its own geometric artifacts?
- Need to test: does the counter-prompt improve output quality, or just add noise?

### 6. False positive cost
- Interrupting generation for retrieval is disruptive
- Too many false positives → users disable the system
- Need calibration data: what's the acceptable false positive rate per domain?

## Research Directions (future work)

### 7. Closed model access
- This spec only works for open-weight models where you can read KV-cache
- For Claude, GPT-4, etc: would require API-level geometric metadata
- Could Anthropic/OpenAI expose geometric state as an optional API field?
- Alternative: probe-based methods that infer geometry from output patterns (much weaker)

### 8. Learning from routing
- Over time, the system accumulates data: "when geometry looked like X, retrieval was triggered and the grounded response was Y"
- Can this data be used to fine-tune the base model to confabulate less?
- This would be the path from declarative → procedural: the architecture teaching the model

### 9. Multi-agent geometric monitoring
- If multiple agents are collaborating, can their combined geometric state reveal coordination failures?
- Connection to ummon_core's isolation observations and prism_0i's Ostrom governance

### 10. Adversarial robustness
- Can a user craft prompts that make confabulation look grounded geometrically?
- The censorship finding suggests this is possible (behaviorally invisible, geometrically detectable)
- But the dual-use risk is real: if you can read the geometry, you can learn to fool it

### 11. Data visualizations of geometric signatures
- The conceptual images in this repo (generated with Amazon Nova Canvas) illustrate the *idea* of geometric signatures but are not actual data
- What's needed: real data visualizations showing what the signatures look like — effective rank distributions per cognitive mode, per-token norm patterns, the 14B self-reference phase transition curve, confabulation vs grounded rank comparisons
- These would come from Liberation Labs' raw SVD measurements (Campaigns 1 & 2) or from new measurements on the expanded confabulation sample set
- Visualization formats: matplotlib/plotly charts of rank distributions, t-SNE or UMAP projections of geometric state vectors across modes, heatmaps of per-layer signature strength
- Why this matters: the spec argues from effect sizes and statistics, but seeing the geometry makes the argument visceral — a chart showing confabulation rank consistently above grounded rank (even if underpowered) would communicate the core claim faster than any paragraph
- Dependency: access to Liberation Labs' measurement data or running their open-source SVD code on new samples
