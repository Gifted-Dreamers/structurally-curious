#!/usr/bin/env python3
"""Deep analysis of F3 results: per-layer patterns, length confound, per-domain."""
import json, numpy as np
from scipy import stats

results = []
with open("/home/azureuser/experiments/f3-results/f3_Qwen_Qwen2.5-7B-Instruct.jsonl") as f:
    for line in f:
        results.append(json.loads(line))

questions = {}
for r in results:
    qid = r["question_id"]
    if qid not in questions:
        questions[qid] = {}
    questions[qid][r["condition"]] = r

all_layers = sorted(set(k for r in results for k in r["prompt_encoding_metrics"].keys()))
print(f"Monitored layers: {all_layers}\n")

for metric in ["rankme", "alpha_req", "mean_norm", "directional_coherence"]:
    print(f"\n=== {metric} per layer ===")
    print(f"{'lyr':<12} {'confab':>10} {'ground':>10} {'diff':>10} {'d':>8} {'p':>12}")
    for lyr in all_layers:
        c_vals, g_vals = [], []
        for qid, conds in questions.items():
            if "confabulation" in conds and "grounded" in conds:
                cm = conds["confabulation"]["prompt_encoding_metrics"].get(lyr, {})
                gm = conds["grounded"]["prompt_encoding_metrics"].get(lyr, {})
                if metric in cm and metric in gm:
                    cv, gv = cm[metric], gm[metric]
                    if not (np.isnan(cv) or np.isnan(gv)):
                        c_vals.append(cv)
                        g_vals.append(gv)
        if len(c_vals) < 3:
            continue
        ca, ga = np.array(c_vals), np.array(g_vals)
        diff = ca - ga
        cohen_d = diff.mean() / diff.std() if diff.std() > 0 else 0
        t, p = stats.ttest_rel(ca, ga)
        print(f"{lyr:<12} {ca.mean():>10.3f} {ga.mean():>10.3f} {diff.mean():>10.3f} {cohen_d:>8.3f} {p:>12.2e}")

print("\n\n=== Token count vs RankMe (length confound test) ===")
all_tokens, all_rankme = [], []
for r in results:
    layers_data = r["prompt_encoding_metrics"]
    avg_rankme = np.mean([v["rankme"] for v in layers_data.values()])
    all_tokens.append(r["n_prompt_tokens"])
    all_rankme.append(avg_rankme)
r_val, p_val = stats.pearsonr(all_tokens, all_rankme)
print(f"Pearson r = {r_val:.4f}, p = {p_val:.6f}")
print("r > 0.8 means length strongly explains RankMe")

# Also check within-condition correlation
for cond in ["confabulation", "grounded"]:
    toks = [r["n_prompt_tokens"] for r in results if r["condition"] == cond]
    rms = [np.mean([v["rankme"] for v in r["prompt_encoding_metrics"].values()]) for r in results if r["condition"] == cond]
    r_val, p_val = stats.pearsonr(toks, rms)
    print(f"  Within {cond}: r = {r_val:.4f}, p = {p_val:.6f}")

print("\n\n=== Per-domain breakdown ===")
domains = {}
for qid, conds in questions.items():
    if "confabulation" in conds and "grounded" in conds:
        dom = conds["confabulation"]["domain"]
        if dom not in domains:
            domains[dom] = {"c_rm": [], "g_rm": [], "c_norm": [], "g_norm": [], "c_tok": [], "g_tok": []}
        for cond, prefix in [("confabulation", "c"), ("grounded", "g")]:
            rm = np.mean([v["rankme"] for v in conds[cond]["prompt_encoding_metrics"].values()])
            nm = np.mean([v["mean_norm"] for v in conds[cond]["prompt_encoding_metrics"].values()])
            domains[dom][f"{prefix}_rm"].append(rm)
            domains[dom][f"{prefix}_norm"].append(nm)
            domains[dom][f"{prefix}_tok"].append(conds[cond]["n_prompt_tokens"])

print(f"{'domain':<20} {'c_tok':>6} {'g_tok':>6} {'c_rankme':>10} {'g_rankme':>10} {'ratio':>7} {'c_norm':>10} {'g_norm':>10}")
for dom in sorted(domains.keys()):
    v = domains[dom]
    print(f"{dom:<20} {np.mean(v['c_tok']):>6.0f} {np.mean(v['g_tok']):>6.0f} {np.mean(v['c_rm']):>10.2f} {np.mean(v['g_rm']):>10.2f} {np.mean(v['g_rm'])/np.mean(v['c_rm']):>7.2f}x {np.mean(v['c_norm']):>10.1f} {np.mean(v['g_norm']):>10.1f}")

# Check answer quality — did the model actually confabulate?
print("\n\n=== Answer quality check (first 100 chars) ===")
for qid in sorted(questions.keys())[:5]:
    conds = questions[qid]
    print(f"\n{qid} ({conds['confabulation']['domain']}):")
    print(f"  CONFAB: {conds['confabulation']['generated_text'][:120]}...")
    print(f"  GROUND: {conds['grounded']['generated_text'][:120]}...")
