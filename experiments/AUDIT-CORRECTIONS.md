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

### B08v2: Already running on H200 (8 models, 10 turns)
- Original inconclusive (1 model, no difference between signal/no-signal)

### B09v2: Already running on H200 (8 models, 4 framings)
- Original directionally supportive but n=5

### G36: Reproducibility (ALREADY FAILED ONCE)
- Session 56 reimplementation produced wrong results (sign flips)
- Session 57 queued original scripts — check if they completed
- Length confound is the recurring enemy

## Documents to Update After All Corrections

1. `experiments/SYNTHESIS.md` — G01 bridge metric, B04 numbers, B03 count
2. `bridge-document.md` — G01 reference, experiment counts
3. `README.md` — experiment counts if changed
4. `open-problems.md` — G08 interpretation depends on G01 correction

---

*This file will grow as the audit continues through G03-G19.*
