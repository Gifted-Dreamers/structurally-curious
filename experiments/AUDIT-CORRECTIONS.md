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

---

*This file will grow as the audit continues through G03-G19.*
