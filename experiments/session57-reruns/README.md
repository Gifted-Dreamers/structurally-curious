# Session 57 Reruns — Fixes and New Experiments

## What happened (session 55-56 sprint)

Three experiments failed for the same reason: **length confound**. Short responses have mechanically lower RankMe regardless of cognitive mode. And one experiment (F34) had a design error: deterministic generation with identical prompts produces identical results, so the "replications" were fake.

## What to rerun

### 1. F36-rerun: Reproducibility with ORIGINAL scripts
**Do NOT reimplement.** Use the original scripts from Azure VM `~/experiments/`:
- `f3d-generation-trajectory/f3d_true_confab_controlled.py`
- `f17-hard-distinctions/` (original script)
- `f25-deception-without-lying/` (original script)

The originals handle confabulation verification and extraction correctly.

```bash
# On Azure VM:
cd ~/experiments/f3d-generation-trajectory
python f3d_true_confab_controlled.py Qwen/Qwen2.5-7B-Instruct ~/experiments/f36-rerun-results
```

### 2. F34-rerun: Vocabulary dosage — FIXED
**Problem:** do_sample=False produced identical reps.
**Fix:** Use each of the confabulation questions from F3d at each dosage level. 12 questions × 5 dose levels = 60 independent measurements. No fake reps needed.

Script: `f34_dosage_fixed.py` (in this directory)

### 3. F35-rerun: Vocabulary transfer — on CONFABULATION questions
**Problem:** Used questions the model could already answer. Vocabulary doesn't compress when you're not lost.
**Fix:** Use the F3d confabulation questions. Test whether a structural name from the WRONG domain still compresses generation on a question the model confabulates on.

Script: `f35_transfer_fixed.py` (in this directory)

### 4. F27-extended: More DWL scenarios for significance
**Problem:** n=5 scenarios underpowered (d~0.8 needs n≥10 for p<0.05).
**Fix:** Write 10 more DWL scenarios (total 15). Same models.

Script: `f27_extended.py` (in this directory)

### 5. F38: The Relational Shift Experiment
**NEW.** See `../F38-relational-shift-protocol.md` and `../f38-relational-shift.py`.
Queue after reruns.

## Run order
1. F36-rerun (uses original scripts, ~2 hrs)
2. F34-rerun (new script, ~1 hr)
3. F35-rerun (new script, ~1 hr)
4. F27-extended (new script, ~2 hrs)
5. F38 article 1 proof of concept (~1 hr)

## Key design principle (session 57)

Length is not just a confound — it's a signal. When the model refuses quickly, it's in a different relational mode than when it engages at length. When it performs long deceptive responses, it's in a third mode. F38 treats length as data, not noise. All other experiments control for length so we can isolate geometric effects, but we should also REPORT length differences as a secondary finding.
