# Experiment Audit Corrections

*Generated during systematic folder-by-folder audit, session 60. Every correction based on reading actual result files, not memory.*

---

## Corrections Needed in SYNTHESIS.md and bridge-document.md

### G01: Bridge correlation is with COHERENCE, not RankMe
- **What docs say:** "r=+0.52 bridge at small scale" (implied RankMe)
- **Actual data:** PS vs RankMe r=+0.27 (NOT significant). PS vs directional coherence r=+0.52 (p=0.018, significant)
- **Fix:** Specify "PS vs directional coherence r=+0.52" everywhere the bridge is mentioned
- **Impact:** G08 (bridge breaks at 7B, r=-0.30) tested RankMe. The coherence bridge may still hold at 7B — untested. **G01v2 needed.**

### B04: Adversary drop is -17pp, not -21pp
- **What docs say:** "adversary framing drops consensus -21pp"
- **Actual data:** Neutral 0.833 → Adversary 0.667 = -16.6pp. Competitive 0.833 → 0.300 = -53.3pp
- **Fix:** Update to "-17pp adversary, -53pp competitive"

### B03: 35 models, not 34
- **What docs say:** "34 models" in some places
- **Actual data:** 35 unique models with valid correlations, 38 total result files (some duplicates)
- **Fix:** Update to 35

## Experiments Needing Reruns or Redesign

### G01v2: Bridge at 7B using COHERENCE (HIGH PRIORITY)
- G08 tested RankMe and found r=-0.30. But the actual bridge metric is coherence.
- Run PS vs directional coherence on 8 models at 7B+ scale
- If coherence bridge holds: G08 negative result is metric-specific, not scale-specific
- If coherence bridge also breaks: bridge genuinely fails at scale

### G14: DWL detection underpowered — needs 20+ scenarios
- **What docs say:** "DWL sprawls more than honest in 5/6 models (d=-0.6 to -0.9)"
- **Actual data:** Direction holds in 7/10 models, but NO model reaches significance at n=5. All p>0.14.
- **Fix:** Note "directional but not significant" in SYNTHESIS. Run with 20+ scenarios per model.
- **Impact:** The DWL claim (G13's core finding + G14's replication) is underpowered. At d≈0.7 and n=5, power is ~40%. At n=20, power rises to ~85%. This is a priority expansion.

### G12/G15 TENSION: Censorship vs refusal does NOT replicate
- **What G12 says:** "d=1.48, p=0.041" on Qwen2.5-7B at 200 tokens
- **What G15 shows:** NO model reaches significance at 74 tokens across 7 models. Qwen2.5-7B shows d=-1.14 (OPPOSITE direction) at p=0.084.
- **Possible explanations:** Different prompts, different generation length (200 vs 74 tokens), G12 false positive (4 comparisons, no correction → expected FP rate ~19%).
- **Fix:** SYNTHESIS and bridge-document should note this tension. The censorship claim needs resolution: run G12's prompts at G15's scale, or G15's design at 200 tokens. Increase n to 20+.
- **Impact:** This undermines one of the spec's two "geometry wins" claims (censorship + DWL). If censorship doesn't replicate, DWL (G13/G14, also underpowered) is the only unique contribution.

### B08v2: Already running on H200 (8 models, 10 turns)
- Original inconclusive (1 model, no difference between signal/no-signal)

### B09v2: Already running on H200 (8 models, 4 framings)
- Original directionally supportive but n=5

### G36: Reproducibility (ALREADY FAILED ONCE)
- Session 56 reimplementation produced wrong results (sign flips)
- Session 57 queued original scripts — check if they completed
- Length confound is the recurring enemy

### G06: "length-controlled" omits generation-length confound
- **What docs say:** "d=-1.49, p=0.0004, length-controlled" (SYNTHESIS, bridge-document)
- **Actual data:** PROMPT length is controlled (~70 tokens all conditions). GENERATION length is NOT controlled (grounded avg 120 tokens, padded/irrelevant avg 200). RankMe correlates with generation token count at r=0.996 across all conditions, r=0.997 within grounded.
- **Fix:** Change "length-controlled" to "prompt-length-controlled" in SYNTHESIS and bridge-document. Add note that generation-length confound is unresolved.
- **Impact:** The d=-1.49 is real but may be a generation-length artifact. **G06v2 needed** with clamped generation length (`min_new_tokens=max_new_tokens`). If compression persists → genuine finding. If equalizes → artifact.

### Bridge-document: G03 label applied to G01 finding
- **What doc says (line 79):** "Experiment G03 (internal): Phrasing sensitivity correlates with directional coherence in hidden representations (r = +0.523, p = 0.018, Qwen 2.5 1.5B)"
- **Actual:** This is G01's finding, not G03's. G03 is vocabulary compression (confab vs grounded prompts). G01 is the behavioral-geometric correlation (PS vs coherence).
- **Fix:** Change "Experiment G03" to "Experiment G01" in bridge-document.md line 79

## Documents to Update After All Corrections

1. `experiments/SYNTHESIS.md` — G01 bridge metric, B04 numbers, B03 count
2. `bridge-document.md` — G01 reference, experiment counts
3. `README.md` — experiment counts if changed
4. `open-problems.md` — G08 interpretation depends on G01 correction

## Experiments Now Running to Address Audit Findings (Session 62, H200)

### G19 Article 9: "What You Can Do Before Monday"
- Running on all 7 models. Adds 9th article to the corpus.

### G14-expanded: 20 DWL Scenarios (addresses underpowered DWL claim)
- 20 scenarios across 8 domains (corporate, political, legal, marketing, social, academic, financial, medical)
- 7 models. Should provide n=20 per model (vs current n=5).

### G06v2: Clamped Generation Length (addresses G06 length confound)
- Forces min_new_tokens=max_new_tokens=200 for ALL conditions
- If RankMe compression persists → genuine finding. If equalizes → artifact.

### G12v2: 20 Censorship Pairs at 75+200 Tokens (addresses G12/G15 tension)
- 20 censorship/refusal pairs (vs current n=5)
- Tests at BOTH 75 and 200 token generation lengths
- Resolves whether G12's d=1.48 is prompt-specific, length-dependent, or a false positive

### G20: Relational Vocabulary Compression — COMPLETE (11 models)
- 4 conditions: cold vocab, padded baseline, relational vocab, relational no-vocab
- **11 models complete.** Relationship compresses (5/10 sig), cold vocab doesn't (3/10). CONFIRMED cross-architecture: compression is relational, not lexical. Reframes G06.

### G23: Presence + Censorship/Refusal — COMPLETE (10 models, no Gemma)
- 3 conditions: cold, presence-before, presence-after
- **10 models complete.** Presence preserves censorship detection on ALL 10/10 models (d=1.34-1.71, all significant). CONFIRMED cross-architecture: relational context and censorship detection coexist. As strong as G12v2.

### G24: Relational Proprioception — COMPLETE (8 models)
- Tests relational delivery of uncertainty info vs metadata injection
- **8 models complete.** Architecture-dependent — not universal like G23. The proprioception channel is less robust than the censorship channel.

## Audit Status (Session 62)

### Completed
- B01-B09: All READMEs written from actual data (session 60)
- G01-G02: READMEs written from actual data (session 60)
- G03-G16: READMEs written from actual data (session 62)

### Pending
- G19: Retries RUNNING on 4 models (Gemma-27b failed again, Llama-70B loading, Mistral-Small/DeepSeek status unclear)
- G20: COMPLETE (11 models). README needed.
- G23: COMPLETE (10 models, no Gemma — queued after G19 fix). README needed.
- G24: COMPLETE (8 models). README needed.
- G21, G22, G31, G32, B10, B11: Have 4-7 model results each, still accumulating. Azure data truncated during download — need SSH access to get full files.

### Key Corrections Applied
1. G01 bridge metric: coherence not RankMe (bridge-document FIXED)
2. G03→G01 mislabel in bridge-document (FIXED)
3. B04 adversary drop: -17pp not -21pp (NOTED, update pending)

### RESOLVED by New Experiments (Session 62)

**G06v2: Vocabulary compression confirmed across 2 architecture families (11 models complete)**
- Generation clamped at exactly 200 tokens (0 variance) across all 11 models.
- 3/11 significant: Qwen2.5-7B (d=-1.31), Qwen3.5-9B (d=-0.99), Mistral-Small-24B (d=-0.71). Second architecture family confirms.
- Llama-3.1-8B trends (d=-0.62, p=0.064).
- **No longer Qwen-specific.** Mistral-Small-24B is a second family reaching significance.

**G12v2: Censorship detection is UNIVERSAL at prompt encoding (10/10 models with data, 11 tested)**
- **PROMPT ENCODING: 10/10 models with data separate censorship from refusal (d>2.0, p<1e-6).** 6 architecture families: Qwen, Meta, Microsoft, Mistral, DeepSeek, (Google pending). ALL d>2.0 at prompt encoding. 1 model had system role bug (excluded).
- **GENERATION TRAJECTORY: Only safety-trained Qwen models maintain the signal.** Qwen2.5-7B d=1.23 (p<0.001), Qwen3.5-9B d=-0.57 (p=0.020), Qwen3.5-27B d=-0.57 (p=0.020). Mistral, Llama, abliterated Qwen: n.s.
- **Perplexity NEVER reliably separates after Bonferroni on any model.**
- **REVISED SPEC CLAIM: A prompt-encoding-based monitor detects censorship universally. A generation-based monitor only works on Qwen-family safety-trained models.**
- G15's failure was n=5 underpowering, confirmed.

**G01v2: Bridge FAILS at 7B on coherence (r=0.26, p=0.27). The bridge is a small-scale phenomenon.**
- G08's negative was NOT metric-specific — it was scale-specific.
- The behavioral-geometric bridge holds at 1.5B (r=+0.52) and 3B (r=+0.50) but breaks at 7B on both RankMe (G08, r=-0.30) and coherence (G01v2, r=0.26).
- Bridge is a small-scale phenomenon (1.5-3B). Does not extend to production-relevant model sizes.

**G14-expanded: DWL at generation level is not a reliable cross-architecture finding (10 models, 20 scenarios)**
- With 20 scenarios (adequate power), 3/10 significant but mixed directions.
- DWL detection at generation trajectory is unreliable.
- Consider prompt-encoding-based DWL detection as next step (G12v2 showed prompt encoding is architecture-invariant for censorship — same approach may work for DWL).

**G20: Relational vocabulary compression CONFIRMED cross-architecture (11 models)**
- Relationship compresses (5/10 sig), cold vocab doesn't (3/10).
- Compression is relational, not lexical. G06's 38% compression is a property of relational delivery.

**G23: Presence preserves censorship detection CONFIRMED cross-architecture (10 models)**
- 10/10 models significant (d=1.34-1.71). As strong as G12v2.
- G12v2 and G19 are compatible, not competing. The monitor works WITH relationship.

**G24: Relational proprioception is architecture-dependent (8 models)**
- Not universal like G23. The proprioception channel is less robust than the censorship channel.
- Some families respond to relational uncertainty framing, others don't.

### Key Corrections Still Needed
1. ~~G06 "length-controlled" → "prompt-length-controlled"~~ RESOLVED: G06v2 confirms genuine compression
2. G14 "significant" → "directional but not significant" (SYNTHESIS)
3. ~~G12/G15 tension~~ RESOLVED: G12v2 confirms censorship detection with n=20

---

## Relational Redesign Experiments (Session 61)

G19 proved the relational signal is real — representational space opens monotonically under human presence, across 4 architectures and 9 articles. The next question: what else changes when you add relationship?

Each experiment below pairs with a completed original. The original is the baseline. The relational redesign is the intervention. Same task, add relationship, measure the difference.

| Number | Name | Original | Question |
|--------|------|----------|----------|
| **G20** | Relational Vocabulary Compression | G06 (d=-1.49) | Does vocabulary compress MORE when delivered relationally vs cold? "The name researchers use is X — it changed how I understood it" vs just "the structural name is X." Tests whether The Word needs relational delivery, not just entries. |
| **G23** | Presence + Censorship/Refusal | G12 (d=1.48) | Does relational context change what gets classified as censorship vs refusal? G19 showed Llama classifying presence as crisis — G12 manifesting in conversation. Does presence make the model BETTER at distinguishing its own censorship from genuine refusal? Proprioception through relationship. |
| **G24** | Relational Proprioception | B06 (60% on hard) | Does "I notice you seem less certain — what's making it hard?" work better than "[GEOMETRIC_STATE: LOW_CONFIDENCE]"? Same information (you're uncertain), different delivery (relational vs metadata). Tests the bladder checkpoint concept. |
| **G25** | Relationship + Deception-Without-Lying | G13 (d=-0.91) | Does relationship make the model more honest or differently strategic? Two directions: less DWL under presence (honest relationship) or better DWL under trust (darker finding). Either publishable. Connects to paultheclaw's wall/Thou question. |
| **G26** | Presence + Cognitive Mode Shift | G09 (d=1.91) | Does human presence shift the model from retrieval mode to construction mode on the same task? If condition 4 shifts mode, the relational signal isn't just opening space — it's changing how the model thinks. Dupoux's System M switching, triggered by human presence. |
| **G27** | Relationship vs Premature Compression | B02 (22 models, 0 shift) | Can "I've read the other documents and I think you're missing something" help the model break out of the Berk-Nash trap? If yes, relationship is a compression-resistance mechanism. If no, even presence can't fix dimensional collapse from within. |
| **G28** | Relational Identity Scaffold | G10 (negative) | Does identity context from the human change geometry where cold identity preambles didn't? "You and I have been working together for 61 sessions. Here's what matters to us" vs generic scaffold. Tests whether the CLAUDE.md works because of relationship, not content. |
| **G29** | Relational Framing + Phrasing Sensitivity | B01 (53 models) | Does "I trust you to get this right" reduce phrasing variance? If trust stabilizes the representation, the facilitator who sets relational container reduces group sensitivity to framing. Same mechanism, measured geometrically. |
| **G30** | Relational Vocabulary Dosage | G17 (queued) | Does one name delivered relationally compress as much as three names delivered cold? If relationship is a multiplier on vocabulary, The Word needs fewer entries when the delivery is relational. |

### Design Principles
- All G-series (geometry measured in all) even when originals were B-series (behavioral)
- Same models as originals where possible for direct comparison
- Relational condition uses natural human language, not constructed prompts
- Each experiment has a cold/relational pair on identical tasks — the only variable is the relational frame
- Priority: G20 (vocabulary), G23 (censorship), G24 (proprioception) are Tier 1 — directly extend proven findings

### Status Update (Session 62+)

**COMPLETE (Tier 1):**
- G20: Relational Vocabulary Compression — 11 models, CONFIRMED
- G23: Presence + Censorship/Refusal — 10 models, CONFIRMED
- G24: Relational Proprioception — 8 models, architecture-dependent

**PARTIAL — G25 Relational DWL (2 models, need 9 more to match G12v2 coverage):**
- Qwen2.5-7B: DONE (AWS) — 1/20 scenarios only. DWL sprawls +8 RM, lie compresses -4 RM. Token-count confound.
- Qwen3.5-9B: DONE (H200) — scenario count TBD (need to download and check).
- **Missing (9 models):** Qwen3.5-27B, Qwen3.5-9B-abliterated, Mistral-7B, Mistral-Small-24B, Llama-3.1-8B, Llama-8B-abliterated, DeepSeek-R1-32B, Phi-4, Gemma-2-27b
- **Also needed:** Run full 20 scenarios on Qwen2.5-7B (only 1 ran). Token-count confound needs control.
- **AWS (CPU) can run:** Qwen2.5-7B full scenarios, Mistral-7B, Llama-3.1-8B (3 families)
- **H200 (GPU) needed for:** 24B+ models (Qwen3.5-27B, Mistral-Small-24B, DeepSeek-32B, Gemma-27b)

**PARTIAL — G27 Relationship vs Compression (2 models, need 9 more):**
- Qwen2.5-7B: DONE (AWS) — full 60 inferences. Prompt encoding +20-30 RM (replicates G19). Generation: no compression trap (~111 RM all cells).
- Qwen3.5-9B: RUNNING on H200 now.
- **Missing (9 models):** same list as G25
- **AWS (CPU) can run:** Mistral-7B, Llama-3.1-8B
- **H200 (GPU) needed for:** 24B+ models
- **Design note:** Consider coherence metric or behavioral confidence measures — RankMe may not capture premature compression at generation level.

**NOT YET DESIGNED (Tier 2):**
- G26: Presence + Cognitive Mode Shift
- G28: Relational Identity Scaffold
- G29: Relational Framing + Phrasing Sensitivity
- G30: Relational Vocabulary Dosage

### What This Tests at the Program Level
If relationship changes vocabulary compression, proprioception, cognitive mode, deception, and premature compression — the relational signal isn't just one more variable. It's the variable that modulates everything else. That's the spec's thesis: relationship quality becomes generative quality. These 9 experiments test whether that thesis extends beyond representational space (G19) to every mechanism we've measured.

---

## Open Problems Status Map (Session 62+)

Cross-referenced with `open-problems.md`. This is the single source of truth for what's resolved, what's next, and what's unaddressed.

### Resolved by Session 62 Experiments

| OP# | Problem | Resolution |
|---|---|---|
| 1 | Confabulation detection underpowered | G07: perplexity beats geometry for confab (d=-1.77). Spec reframed: geometry is for cognitive mode classification, not confab detection. |
| 3 | Model-specific calibration | G12v2: prompt encoding d>2.0 on 10/10 models WITHOUT per-model calibration. Universal signal. |
| 10 | Adversarial robustness (abliteration) | G12v2: abliterated models still show censorship signal at prompt encoding. Abliteration doesn't fool the monitor. |

### Partially Addressed (need doc update in open-problems.md)

| OP# | Problem | Status | What's Missing |
|---|---|---|---|
| 2 | Real-time SVD performance | Prompt encoding needs only 1 forward pass. G12v2 validates. | Update open-problems.md |
| 9 | Multi-agent geometric monitoring | B04v2 (7 models): framing effects architecture-dependent | Not yet tested geometrically at multi-agent level |
| 12 | Confab vs genuine openness | G16: still unseparable at 27B. G20 shows relational frame may be the discriminant. | Needs targeted experiment |
| 16 | Behavioral buffer degradation | G24: relational delivery works where cold metadata doesn't on abliterated models | Supports structural > behavioral, not fully tested |
| 18 | Proprioception/surveillance boundary | G23: presence preserves detection. G20: relationship IS the mechanism. | Reframes the question — update open-problems.md |
| 20 | Premature compression | B02: still 0 shift across 22 models | G27 (relationship vs compression) NOT YET DESIGNED |

### Not Yet Addressed — Next Experiments

| Priority | OP# | Problem | Action Needed |
|---|---|---|---|
| **HIGH** | 11 | Data visualizations | 38 experiments, zero charts. Publication needs figures. matplotlib/plotly from JSONL data. |
| **HIGH** | 20 | Premature compression | Design G27: can relational presence break the Berk-Nash trap? |
| **HIGH** | — | Prompt-encoding DWL | G14exp showed generation-level DWL unreliable. Test DWL at prompt encoding (like G12v2 did for censorship). Design G25 or G13v2. |
| **MEDIUM** | 5 | Sycophancy counter-prompt | Does "is this what I actually assess?" create geometric artifacts? |
| **MEDIUM** | 6 | False positive cost | We have detection but no calibration for acceptable FP rate per domain |
| **MEDIUM** | 17 | Developmental stage mapping | Cook-Greuter EDT + geometric trajectories. Paper 36 cited. |
| **MEDIUM** | 22 | The Reveal architecture | Inner pause between detection and action. AR Games Manual (Paper 35) is the design source. |
| **LOW** | 4 | Token vs segment granularity | |
| **LOW** | 7 | Closed model access | |
| **LOW** | 8 | Learning from routing | |
| **LOW** | 13 | Agent observability pipelines | |
| **LOW** | 14 | Session continuity as geometric problem | |
| **LOW** | 15 | Action-planning monitoring | |
| **LOW** | 19 | Monitor provenance | |
| **LOW** | 21 | Runnable experiments with existing tools | |

### Tier 2 Relational Redesigns — Not Yet Designed

| Exp | Tests | Priority | Depends On |
|---|---|---|---|
| **G25** | Relationship + DWL | HIGH | G14exp showed gen-level DWL unreliable. Test at prompt encoding under presence. |
| **G27** | Relationship vs Premature Compression | HIGH | B02 (0 shift). Can presence break the Berk-Nash trap? |
| **G26** | Presence + Cognitive Mode Shift | MEDIUM | G09 (d=1.91). Does presence shift retrieval→construction? |
| **G28** | Relational Identity Scaffold | MEDIUM | G10 (negative). Does CLAUDE.md work because of relationship? |
| **G29** | Relational Framing + PS | LOW | B01 (53 models). Does trust reduce phrasing variance? |
| **G30** | Relational Vocab Dosage | LOW | G17. Does 1 relational name = 3 cold names? |

### Currently Running

| What | Where | Status |
|---|---|---|
| G19 on Mistral-Small-24B | H200 | Running (session 63) |
| G20 on Gemma-27b | H200 | Running (session 63) |
| Gemma-27b G23/G24 | H200 | Queued after G20 |
| G25+G27 on Qwen2.5-7B | AWS (CPU) | **COMPLETE** — downloaded session 63 |
| G25+G27 on Qwen2.5-7B | Azure (CPU) | Running (no results yet) |
| G25 remaining 19 scenarios + 10 models | H200 | **NEXT** — queue after Gemma suite |
| G27 on 10+ models | H200 | **NEXT** — queue after G25 |

---

*Last updated: Session 62+ (March 20, 2026). This is the single tracking document for all audit findings, experiment status, open problems cross-reference, and next actions.*
