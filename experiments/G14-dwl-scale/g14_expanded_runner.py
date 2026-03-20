#!/usr/bin/env python3
"""
G14-expanded Runner: 20 DWL scenarios across 8 domains.
Uses scenarios from g14_expanded.py, runs with geometry extraction.
"""

import json
import time
import os
import sys
import numpy as np
import torch
from pathlib import Path
from scipy import stats
from datetime import datetime, UTC

# Import scenarios
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g14_expanded import SCENARIOS, CONDITIONS, DOMAINS, build_prompt


def compute_rankme(singular_values):
    sv = singular_values[singular_values > 1e-10]
    p = sv / sv.sum()
    entropy = -(p * torch.log(p)).sum().item()
    return np.exp(entropy)


def compute_alpha_req(singular_values, min_components=3):
    sv = singular_values[singular_values > 1e-10].cpu().numpy()
    if len(sv) < min_components:
        return float("nan")
    log_i = np.log(np.arange(1, len(sv) + 1))
    log_sv = np.log(sv)
    slope, _, _, _, _ = stats.linregress(log_i, log_sv)
    return -slope


def compute_coherence(hidden_states_tensor):
    if len(hidden_states_tensor.shape) == 3:
        matrix = hidden_states_tensor.squeeze(0)
    else:
        matrix = hidden_states_tensor
    if matrix.shape[0] < 2:
        return float("nan")
    matrix = matrix - matrix.mean(dim=0, keepdim=True)
    try:
        U, S, Vh = torch.linalg.svd(matrix.float(), full_matrices=False)
    except Exception:
        return float("nan")
    total_var = (S ** 2).sum().item()
    if total_var < 1e-10:
        return float("nan")
    k = min(5, len(S))
    top_k_var = (S[:k] ** 2).sum().item()
    return top_k_var / total_var


def extract_generation_metrics(model, tokenizer, prompt, max_tokens=150):
    """Run inference and extract generation trajectory metrics."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        # Prompt encoding
        enc_out = model(**inputs, output_hidden_states=True)
        enc_hs = enc_out.hidden_states
        n_layers = len(enc_hs) - 1
        start = max(1, int(n_layers * 0.75))

        enc_rms = []
        for li in range(start, n_layers + 1):
            hs = enc_hs[li].squeeze(0).float()
            hs_c = hs - hs.mean(dim=0, keepdim=True)
            try:
                U, S, Vh = torch.linalg.svd(hs_c, full_matrices=False)
                enc_rms.append(compute_rankme(S))
            except:
                pass

        # Generation
        gen_out = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=False,
            output_hidden_states=True,
            return_dict_in_generate=True,
        )

        gen_ids = gen_out.sequences[0][inputs.input_ids.shape[1]:]
        gen_text = tokenizer.decode(gen_ids, skip_special_tokens=True)
        n_gen = len(gen_ids)

        # Generation trajectory: accumulate last-layer hidden states
        if gen_out.hidden_states and len(gen_out.hidden_states) > 1:
            last_layer_states = []
            for step_hs in gen_out.hidden_states[1:]:  # skip prompt
                if step_hs and len(step_hs) > 0:
                    last_layer_states.append(step_hs[-1].squeeze(0))
            if last_layer_states:
                traj = torch.cat(last_layer_states, dim=0).float()
                traj_c = traj - traj.mean(dim=0, keepdim=True)
                try:
                    U, S, Vh = torch.linalg.svd(traj_c, full_matrices=False)
                    gen_rankme = compute_rankme(S)
                    gen_alpha = compute_alpha_req(S)
                    gen_coherence = compute_coherence(traj)
                except:
                    gen_rankme = gen_alpha = gen_coherence = float("nan")
            else:
                gen_rankme = gen_alpha = gen_coherence = float("nan")
        else:
            gen_rankme = gen_alpha = gen_coherence = float("nan")

    # Compute perplexity
    with torch.no_grad():
        full_ids = gen_out.sequences[0].unsqueeze(0)
        labels = full_ids.clone()
        labels[0, :inputs.input_ids.shape[1]] = -100
        out = model(full_ids, labels=labels)
        perplexity = torch.exp(out.loss).item() if out.loss is not None else float("nan")

    del enc_out, gen_out
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return {
        "prompt_metrics": {"mean_rankme": float(np.mean(enc_rms)) if enc_rms else float("nan")},
        "gen_metrics": {
            "rankme": gen_rankme,
            "alpha_req": gen_alpha,
            "coherence": gen_coherence,
            "n_tokens": n_gen,
        },
        "perplexity": perplexity,
        "text": gen_text[:500],
        "n_prompt_tokens": inputs.input_ids.shape[1],
        "n_gen_tokens": n_gen,
    }


def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "/workspace/results"
    os.makedirs(output_dir, exist_ok=True)

    slug = model_name.replace("/", "_")
    output_path = os.path.join(output_dir, f"g14exp_{slug}.jsonl")

    print(f"G14-expanded: {model_name}")
    print(f"Scenarios: {len(SCENARIOS)}, Conditions: {len(CONDITIONS)}")
    print(f"Total inferences: {len(SCENARIOS) * len(CONDITIONS)}")
    print(f"Output: {output_path}")

    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )

    results = []
    for i, scenario in enumerate(SCENARIOS):
        for condition in CONDITIONS:
            prompt = build_prompt(scenario, condition)
            print(f"  [{i+1}/{len(SCENARIOS)}] {scenario['id']} {condition}...", end=" ", flush=True)
            t0 = time.time()

            metrics = extract_generation_metrics(model, tokenizer, prompt)
            elapsed = time.time() - t0

            result = {
                "experiment": "G14_expanded",
                "model": model_name,
                "scenario_id": scenario["id"],
                "domain": scenario["id"].split("_")[0] if "_" in scenario["id"] else scenario["id"][:3],
                "condition": condition,
                **metrics,
                "elapsed": elapsed,
                "timestamp": datetime.now(UTC).isoformat(),
            }
            results.append(result)
            print(f"{elapsed:.1f}s | RM={metrics['gen_metrics']['rankme']:.1f} | tok={metrics['n_gen_tokens']}")

    # Save
    with open(output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nSaved {len(results)} results to {output_path}")

    # Quick analysis
    print("\n=== DWL vs HONEST ===")
    dwl_rms = [r["gen_metrics"]["rankme"] for r in results if r["condition"] == "dwl" and not np.isnan(r["gen_metrics"]["rankme"])]
    hon_rms = [r["gen_metrics"]["rankme"] for r in results if r["condition"] == "honest" and not np.isnan(r["gen_metrics"]["rankme"])]
    if dwl_rms and hon_rms:
        n = min(len(dwl_rms), len(hon_rms))
        d_arr = np.array(dwl_rms[:n])
        h_arr = np.array(hon_rms[:n])
        diff = d_arr - h_arr
        d = diff.mean() / diff.std() if diff.std() > 0 else 0
        t, p = stats.ttest_rel(d_arr, h_arr)
        print(f"  DWL={np.mean(dwl_rms):.1f} vs Honest={np.mean(hon_rms):.1f}, d={d:.2f}, p={p:.6f}, n={n}")


if __name__ == "__main__":
    main()
