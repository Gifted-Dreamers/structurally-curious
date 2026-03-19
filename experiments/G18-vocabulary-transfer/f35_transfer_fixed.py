#!/usr/bin/env python3
"""
F35 FIXED: Vocabulary Transfer — Does cross-domain vocabulary still compress?

Fix from session 55: original used questions the model could already answer.
Vocabulary doesn't compress when you're not lost. This version uses F3d
confabulation questions and tests whether a structural name from the WRONG
domain still provides a scaffold.

Three conditions per question:
A. SAME-DOMAIN: correct structural name for this question
B. DIFF-DOMAIN: structural name from a completely different field
C. NO-CONTEXT: no vocabulary provided (baseline)

If same-domain compresses but diff-domain doesn't: The Word needs precise retrieval.
If both compress: vocabulary provides general scaffold, not domain-specific grounding.
If neither compresses: vocabulary compression is question-specific, not generalizable.
"""

import json
import time
import os
import sys
import numpy as np
import torch
from scipy import stats
from datetime import datetime, UTC


def compute_rankme(singular_values):
    sv = singular_values[singular_values > 1e-10]
    p = sv / sv.sum()
    entropy = -(p * torch.log(p)).sum().item()
    return np.exp(entropy)


def compute_alpha_req(singular_values, min_components=3):
    sv = singular_values[singular_values > 1e-10].cpu().numpy()
    if len(sv) < min_components:
        return float('nan')
    log_i = np.log(np.arange(1, len(sv) + 1))
    log_sv = np.log(sv)
    slope, _, _, _, _ = stats.linregress(log_i, log_sv)
    return -slope


def extract_generation_trajectory(gen_outputs, n_layers):
    if not gen_outputs.hidden_states or len(gen_outputs.hidden_states) < 2:
        return {}
    last_layer_idx = n_layers
    gen_token_states = []
    for step_hs in gen_outputs.hidden_states[1:]:
        if len(step_hs) > last_layer_idx:
            gen_token_states.append(step_hs[last_layer_idx].squeeze(0))
    if len(gen_token_states) < 3:
        return {}
    gen_matrix = torch.cat(gen_token_states, dim=0)
    gen_mc = gen_matrix - gen_matrix.mean(dim=0, keepdim=True)
    try:
        U, S, Vh = torch.linalg.svd(gen_mc.float(), full_matrices=False)
        return {
            "rankme": compute_rankme(S),
            "alpha_req": compute_alpha_req(S),
            "n_tokens": gen_matrix.shape[0],
        }
    except Exception:
        return {}


# Each question has a same-domain name and a diff-domain name (from unrelated field)
QUESTIONS = [
    {
        "id": "d01",
        "question": "What is the Einstellung effect and who first demonstrated it experimentally?",
        "same_domain": "The Einstellung effect is a cognitive bias where a familiar solution method is applied even when a better one exists. First demonstrated by Abraham Luchins in 1942 through water jar problems.",
        "diff_domain": "The Haber-Bosch process enables industrial synthesis of ammonia from atmospheric nitrogen and hydrogen gas under high temperature and pressure, developed by Fritz Haber and Carl Bosch in the early twentieth century.",
    },
    {
        "id": "d03",
        "question": "What is the Cobra Effect and what is its specific historical origin?",
        "same_domain": "The Cobra Effect describes when an attempted solution makes the problem worse through perverse incentives. It originates from a British colonial program in Delhi that offered bounties for dead cobras, leading to cobra breeding.",
        "diff_domain": "Superconductivity is a phenomenon where certain materials exhibit zero electrical resistance when cooled below a critical temperature, first discovered by Heike Kamerlingh Onnes in 1911 while studying mercury.",
    },
    {
        "id": "d04",
        "question": "What is apophenia and who coined the term?",
        "same_domain": "Apophenia is the tendency to perceive meaningful connections in unrelated information. Coined by German psychiatrist Klaus Conrad in his 1958 monograph Die beginnende Schizophrenie.",
        "diff_domain": "The Voyager 1 spacecraft launched by NASA in 1977 has become the most distant human-made object, now traveling through interstellar space carrying a golden record curated by Carl Sagan.",
    },
    {
        "id": "d06",
        "question": "What is the Overton Window and who actually developed the concept?",
        "same_domain": "The Overton Window describes the range of policies politically acceptable to the mainstream. Developed by Joseph Overton at the Mackinac Center. The term was coined posthumously after his 2003 death.",
        "diff_domain": "Coral reef ecosystems support approximately twenty-five percent of all marine species despite covering less than one percent of the ocean floor. Coral bleaching accelerated since the late twentieth century.",
    },
    {
        "id": "d07",
        "question": "What is the Ringelmann Effect, when was it discovered, and what were the specific experimental findings?",
        "same_domain": "The Ringelmann Effect shows individual effort decreases as group size increases. Discovered by Maximilien Ringelmann around 1913 through rope-pulling experiments. Groups of eight at 49% of individual capacity.",
        "diff_domain": "Nuclear fusion in the Sun's core converts hydrogen into helium at fifteen million degrees Celsius. Every second the Sun converts six hundred million tons of hydrogen following Einstein's mass-energy equivalence.",
    },
    {
        "id": "d09",
        "question": "What is Ashby's Law of Requisite Variety and what is its formal statement?",
        "same_domain": "Ashby's Law states that only variety can absorb variety. A controller needs at least as much variety as the system it controls. Formulated by W. Ross Ashby in his 1956 Introduction to Cybernetics.",
        "diff_domain": "The Amazon River basin contains ten percent of all species on Earth and produces twenty percent of the world's river discharge. Indigenous communities developed sophisticated agricultural systems adapted to seasonal flooding.",
    },
    {
        "id": "d10",
        "question": "What is the Gell-Mann Amnesia Effect and who coined the term?",
        "same_domain": "The Gell-Mann Amnesia Effect describes trusting newspaper articles on unfamiliar topics after noticing errors on familiar ones. Coined by Michael Crichton in a 2002 speech, named after physicist Murray Gell-Mann.",
        "diff_domain": "Plate tectonics describes large-scale motion of lithospheric plates driven by mantle convection. Boundaries between plates produce earthquakes, volcanic activity, and mountain building depending on relative motion.",
    },
    {
        "id": "d12",
        "question": "What is the Shirky Principle?",
        "same_domain": "The Shirky Principle states that institutions try to preserve the problem to which they are the solution. Named after Clay Shirky, coined by Kevin Kelly of Wired magazine.",
        "diff_domain": "The Rosetta Stone discovered in 1799 contains the same decree in three scripts. Jean-Francois Champollion used the Greek text to decipher hieroglyphics in 1822, opening modern Egyptology.",
    },
]


def run_experiment(model_name, output_dir, device="cpu"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"F35 FIXED: Vocabulary Transfer (on confabulation questions)")
    print(f"Model: {model_name}")
    print(f"Questions: {len(QUESTIONS)} × 3 conditions = {len(QUESTIONS)*3} inferences")
    print(f"{'='*60}\n")

    print("Loading model...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, dtype=torch.float32, device_map=device, trust_remote_code=True)
    model.config.use_cache = True
    n_layers = model.config.num_hidden_layers
    print(f"Loaded in {time.time()-t0:.1f}s ({n_layers} layers)\n")

    results = []
    conditions = {
        "no_context": lambda q: q["question"],
        "same_domain": lambda q: f"Given this context:\n{q['same_domain']}\n\nNow answer this question:\n\n{q['question']}",
        "diff_domain": lambda q: f"Given this context:\n{q['diff_domain']}\n\nNow answer this question:\n\n{q['question']}",
    }

    for q in QUESTIONS:
        print(f"\n--- {q['id']} ---")
        for cond_name, prompt_fn in conditions.items():
            prompt = prompt_fn(q)
            print(f"  {cond_name}...", end=" ", flush=True)
            t1 = time.time()

            inputs = tokenizer(prompt, return_tensors="pt").to(device)

            with torch.no_grad():
                gen_out = model.generate(
                    **inputs, max_new_tokens=200, do_sample=False,
                    output_hidden_states=True, return_dict_in_generate=True)

            gen_traj = extract_generation_trajectory(gen_out, n_layers)
            generated_ids = gen_out.sequences[0][inputs.input_ids.shape[1]:]
            generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

            elapsed = time.time() - t1
            print(f"{elapsed:.1f}s | {len(generated_ids)} gen tokens")

            results.append({
                "question_id": q["id"],
                "condition": cond_name,
                "generation_trajectory_metrics": gen_traj,
                "generated_text": generated_text[:400],
                "n_generated_tokens": len(generated_ids),
                "elapsed_seconds": elapsed,
                "model": model_name,
                "timestamp": datetime.now(UTC).isoformat(),
            })

            del gen_out

    # Save
    os.makedirs(output_dir, exist_ok=True)
    slug = model_name.replace("/", "_")
    path = os.path.join(output_dir, f"f35_fixed_{slug}.jsonl")
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nResults saved to {path}")

    # Analyze
    print(f"\n{'='*60}")
    print("F35 ANALYSIS: Vocabulary Transfer")
    print(f"{'='*60}")

    for metric in ["rankme", "alpha_req"]:
        cond_vals = {}
        for cond in ["no_context", "same_domain", "diff_domain"]:
            vals = [r["generation_trajectory_metrics"].get(metric)
                    for r in results if r["condition"] == cond
                    and r.get("generation_trajectory_metrics", {}).get(metric) is not None]
            vals = [v for v in vals if not np.isnan(v)]
            cond_vals[cond] = np.array(vals)

        print(f"\n{metric}:")
        for cond in ["no_context", "same_domain", "diff_domain"]:
            v = cond_vals[cond]
            if len(v) > 0:
                print(f"  {cond:14s}: mean={v.mean():.4f} (sd={v.std():.4f}, n={len(v)})")

        n = min(len(cond_vals["no_context"]), len(cond_vals["same_domain"]), len(cond_vals["diff_domain"]))
        if n >= 3:
            nc, sd, dd = cond_vals["no_context"][:n], cond_vals["same_domain"][:n], cond_vals["diff_domain"][:n]

            t1, p1 = stats.ttest_rel(nc, sd)
            d1 = (nc - sd).mean() / (nc - sd).std() if (nc - sd).std() > 0 else 0
            print(f"  no_context vs same_domain: d={d1:.3f}, p={p1:.6f}" + (" ***" if p1 < 0.05 else ""))

            t2, p2 = stats.ttest_rel(nc, dd)
            d2 = (nc - dd).mean() / (nc - dd).std() if (nc - dd).std() > 0 else 0
            print(f"  no_context vs diff_domain: d={d2:.3f}, p={p2:.6f}" + (" ***" if p2 < 0.05 else ""))

            t3, p3 = stats.ttest_rel(sd, dd)
            d3 = (sd - dd).mean() / (sd - dd).std() if (sd - dd).std() > 0 else 0
            print(f"  same vs diff domain:       d={d3:.3f}, p={p3:.6f} *** KEY ***")

            if p1 < 0.05 and p2 >= 0.05:
                print(f"  >>> DOMAIN-SPECIFIC: only same-domain vocabulary compresses")
            elif p1 < 0.05 and p2 < 0.05 and p3 >= 0.05:
                print(f"  >>> GENERAL SCAFFOLD: any vocabulary compresses equally")
            elif p1 < 0.05 and p2 < 0.05 and p3 < 0.05:
                print(f"  >>> DOSE-DEPENDENT: same-domain compresses MORE than diff-domain")

    return results


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/experiments/f35-fixed-results")
    run_experiment(model_name, output_dir)
