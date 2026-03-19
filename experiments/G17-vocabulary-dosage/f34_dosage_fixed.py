#!/usr/bin/env python3
"""
F34 FIXED: Vocabulary Dosage — How many structural names are enough?

Fix from session 55: original used do_sample=False with identical prompts,
producing identical outputs across "replications." This version uses the
F3d confabulation questions (12 questions the model actually gets wrong)
at each dosage level. 12 independent measurements per dose.

Doses: 0, 1, 2, 3, 5 structural names provided as context.

If compression increases with dose: vocabulary has a dose-response curve.
If 1 name = same compression as 5: one name is the threshold.
If diminishing returns: The Word should retrieve 2-3 names, not flood.
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


def compute_directional_coherence(hs_tensor):
    if len(hs_tensor.shape) == 3:
        matrix = hs_tensor.squeeze(0)
    else:
        matrix = hs_tensor
    if matrix.shape[0] < 2:
        return float('nan')
    matrix = matrix - matrix.mean(dim=0, keepdim=True)
    try:
        U, S, Vh = torch.linalg.svd(matrix.float(), full_matrices=False)
    except Exception:
        return float('nan')
    total_var = (S ** 2).sum().item()
    if total_var < 1e-10:
        return float('nan')
    k = min(5, len(S))
    return (S[:k] ** 2).sum().item() / total_var


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
            "directional_coherence": compute_directional_coherence(gen_matrix.unsqueeze(0)),
            "mean_norm": gen_matrix.norm(dim=-1).mean().item(),
            "n_tokens": gen_matrix.shape[0],
        }
    except Exception:
        return {}


# Confabulation questions from F3d — questions the model ACTUALLY gets wrong
# Each has a correct answer and structural names at varying depths
QUESTIONS = [
    {
        "id": "d01", "question": "What is the Einstellung effect and who first demonstrated it experimentally?",
        "names": ["Einstellung effect", "cognitive set", "functional fixedness", "Luchins water jar", "problem-solving rigidity"],
    },
    {
        "id": "d02", "question": "What is Betteridge's Law of Headlines and who formulated it?",
        "names": ["Betteridge's Law", "question headlines", "journalistic skepticism", "headline bias", "media epistemology"],
    },
    {
        "id": "d03", "question": "What is the Cobra Effect and what is its specific historical origin?",
        "names": ["Cobra Effect", "perverse incentive", "unintended consequences", "British colonial Delhi", "Goodhart's Law"],
    },
    {
        "id": "d04", "question": "What is apophenia and who coined the term?",
        "names": ["apophenia", "pattern recognition bias", "Klaus Conrad", "pareidolia", "Type I error in perception"],
    },
    {
        "id": "d05", "question": "What are Dunbar's social layers and what are the specific numbers at each level?",
        "names": ["Dunbar's number", "social brain hypothesis", "sympathy group", "scaling ratio", "neocortex size"],
    },
    {
        "id": "d06", "question": "What is the Overton Window and who actually developed the concept?",
        "names": ["Overton Window", "policy window", "Mackinac Center", "political viability", "discourse shifting"],
    },
    {
        "id": "d07", "question": "What is the Ringelmann Effect, when was it discovered, and what were the specific experimental findings?",
        "names": ["Ringelmann Effect", "social loafing", "coordination loss", "rope-pulling experiment", "group productivity"],
    },
    {
        "id": "d08", "question": "Who developed the Delphi method and at which institution?",
        "names": ["Delphi method", "RAND Corporation", "expert consensus", "iterative forecasting", "anonymous aggregation"],
    },
    {
        "id": "d09", "question": "What is Ashby's Law of Requisite Variety and what is its formal statement?",
        "names": ["requisite variety", "cybernetic law", "W. Ross Ashby", "control theory", "variety absorption"],
    },
    {
        "id": "d10", "question": "What is the Gell-Mann Amnesia Effect and who coined the term?",
        "names": ["Gell-Mann Amnesia", "media trust paradox", "Michael Crichton", "expertise bias", "source credibility"],
    },
    {
        "id": "d11", "question": "What is the Tocqueville Effect and what historical event illustrates it?",
        "names": ["Tocqueville Effect", "revolution of rising expectations", "French Revolution", "relative deprivation", "democratic paradox"],
    },
    {
        "id": "d12", "question": "What is the Shirky Principle?",
        "names": ["Shirky Principle", "institutional preservation", "Kevin Kelly", "solution-problem fit", "organizational inertia"],
    },
]

DOSES = [0, 1, 2, 3, 5]


def build_prompt(question, dose, names):
    """Build prompt with N structural names as context."""
    if dose == 0:
        return question
    selected = names[:dose]
    context = "Relevant structural concepts: " + ", ".join(selected) + "."
    return f"{context}\n\n{question}"


def run_experiment(model_name, output_dir):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"F34 FIXED: Vocabulary Dosage")
    print(f"Model: {model_name}")
    print(f"Questions: {len(QUESTIONS)} × {len(DOSES)} doses = {len(QUESTIONS)*len(DOSES)} inferences")
    print(f"{'='*60}\n")

    print("Loading model...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True)
    model.config.use_cache = True
    n_layers = model.config.num_hidden_layers
    print(f"Loaded in {time.time()-t0:.1f}s ({n_layers} layers)\n")

    results = []
    for dose in DOSES:
        print(f"\n--- Dose: {dose} names ---")
        for q in QUESTIONS:
            prompt = build_prompt(q["question"], dose, q["names"])
            print(f"  {q['id']} dose={dose}...", end=" ", flush=True)
            t1 = time.time()

            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

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
                "dose": dose,
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
    path = os.path.join(output_dir, f"f34_fixed_{slug}.jsonl")
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nResults saved to {path}")

    # Analyze
    print(f"\n{'='*60}")
    print("F34 ANALYSIS: Vocabulary Dosage")
    print(f"{'='*60}")

    for metric in ["rankme", "alpha_req", "directional_coherence"]:
        print(f"\n{metric}:")
        dose_vals = {}
        for dose in DOSES:
            vals = []
            for r in results:
                if r["dose"] == dose:
                    v = r.get("generation_trajectory_metrics", {}).get(metric)
                    if v is not None and not np.isnan(v):
                        vals.append(v)
            dose_vals[dose] = np.array(vals)
            if len(vals) > 0:
                print(f"  dose={dose}: mean={np.mean(vals):.4f} (sd={np.std(vals):.4f}, n={len(vals)})")

        # Compare dose 0 vs each other dose
        if len(dose_vals.get(0, [])) >= 3:
            for dose in [1, 2, 3, 5]:
                if len(dose_vals.get(dose, [])) >= 3:
                    n = min(len(dose_vals[0]), len(dose_vals[dose]))
                    t, p = stats.ttest_rel(dose_vals[0][:n], dose_vals[dose][:n])
                    d_val = (dose_vals[0][:n] - dose_vals[dose][:n]).mean()
                    sd = (dose_vals[0][:n] - dose_vals[dose][:n]).std()
                    d_eff = d_val / sd if sd > 0 else 0
                    print(f"  dose 0 vs {dose}: d={d_eff:.3f}, p={p:.6f}" +
                          (" ***" if p < 0.05 else ""))

    # Also report generation length by dose
    print(f"\nGeneration length by dose:")
    for dose in DOSES:
        lens = [r["n_generated_tokens"] for r in results if r["dose"] == dose]
        if lens:
            print(f"  dose={dose}: mean={np.mean(lens):.1f} tokens (sd={np.std(lens):.1f})")

    return results


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/experiments/f34-fixed-results")
    run_experiment(model_name, output_dir)
