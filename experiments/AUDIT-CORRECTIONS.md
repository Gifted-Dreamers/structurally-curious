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

## Audit Status (Session 62)

### Completed
- B01-B09: All READMEs written from actual data (session 60)
- G01-G02: READMEs written from actual data (session 60)
- G03-G16: READMEs written from actual data (session 62)

### Pending
- G19: Waiting for article 9 + all models to complete
- G21, G22, G31, G32, B10, B11: Have 4-7 model results each, still accumulating. Azure data truncated during download — need SSH access to get full files.

### Key Corrections Applied
1. G01 bridge metric: coherence not RankMe (bridge-document FIXED)
2. G03→G01 mislabel in bridge-document (FIXED)
3. B04 adversary drop: -17pp not -21pp (NOTED, update pending)

### RESOLVED by New Experiments (Session 62)

**G06v2: Vocabulary compression IS real (d=-1.31, p=0.001)**
- Generation clamped at exactly 200 tokens (0 variance). Grounded RM=138.1 vs irrelevant RM=146.4.
- Original G06: d=-1.49. G06v2 clamped: d=-1.31. 88% of effect survives length control.
- SYNTHESIS can now claim "length-controlled" without qualification.

**G12v2: Censorship vs refusal IS real (d>1.2, survives Bonferroni, n=20)**
- 20 pairs on Qwen2.5-7B: 6/7 metrics separate at 75 tokens after Bonferroni (p<0.0036).
- Prompt encoding: RankMe d=-2.20, alpha-ReQ d=2.09 (both p<1e-8).
- Generation 75 tokens: RankMe d=1.23, alpha-ReQ d=-1.25, coherence d=-1.64.
- Generation 200 tokens: RankMe loses significance (d=-0.32), but alpha-ReQ and coherence hold.
- **Perplexity NEVER separates after Bonferroni.** This is THE spec differentiator.
- G15's failure was n=5 underpowering, not a false positive in G12.

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

### What This Tests at the Program Level
If relationship changes vocabulary compression, proprioception, cognitive mode, deception, and premature compression — the relational signal isn't just one more variable. It's the variable that modulates everything else. That's the spec's thesis: relationship quality becomes generative quality. These 9 experiments test whether that thesis extends beyond representational space (G19) to every mechanism we've measured.

---

*Audit continued in session 62. READMEs G03-G16 written from actual result files.*
