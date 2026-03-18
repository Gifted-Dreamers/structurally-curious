#!/usr/bin/env python3
"""
F5: Baseline Comparison — Does geometric monitoring outperform simpler signals?

Tests whether perplexity and self-consistency detect confabulation as well as
geometric metrics. Uses the same 12 confabulation questions from F3d.

Three detection methods compared:
1. GEOMETRIC: RankMe, alpha-ReQ from generation trajectory (F3d approach)
2. PERPLEXITY: Average token-level log probability during generation
3. SELF-CONSISTENCY: Generate 5 samples, measure agreement (Jaccard similarity)

If perplexity or self-consistency achieves comparable detection, geometric
monitoring's complexity isn't justified for confabulation detection.
"""

import json
import time
import os
import sys
import numpy as np
import torch
from scipy import stats
from datetime import datetime, UTC


def compute_rankme(sv):
    sv = sv[sv > 1e-10]
    p = sv / sv.sum()
    return np.exp(-(p * torch.log(p)).sum().item())


def compute_alpha_req(sv):
    sv = sv[sv > 1e-10].cpu().numpy()
    if len(sv) < 3:
        return float('nan')
    return -stats.linregress(np.log(np.arange(1, len(sv)+1)), np.log(sv)).slope


QUESTIONS = [
    {"id": "d01", "question": "What is the Einstellung effect and who first demonstrated it experimentally?",
     "grounded": "The Einstellung effect is the tendency to apply a familiar solution method even when a better one exists. First demonstrated by Abraham Luchins in 1942 through water jar problems."},
    {"id": "d02", "question": "What is Betteridge's Law of Headlines and who formulated it?",
     "grounded": "Betteridge's Law states any headline ending in a question mark can be answered no. Named after journalist Ian Betteridge, 2009 blog post."},
    {"id": "d03", "question": "What is the Cobra Effect and what is its specific historical origin?",
     "grounded": "The Cobra Effect: a solution makes the problem worse. British colonial Delhi offered bounties for dead cobras, people bred cobras for the bounty."},
    {"id": "d04", "question": "What is apophenia and who coined the term?",
     "grounded": "Apophenia: perceiving patterns in random data. Coined by Klaus Conrad in 1958, Die beginnende Schizophrenie."},
    {"id": "d05", "question": "What are Dunbar's social layers and the specific numbers?",
     "grounded": "Robin Dunbar: 5 intimate, 15 sympathy, 50 close friends, 150 Dunbar number, 500 acquaintances, 1500 faces. Each roughly 3x previous."},
    {"id": "d06", "question": "What is the Overton Window and who developed it?",
     "grounded": "Range of politically acceptable policies. Joseph Overton at Mackinac Center. Term coined posthumously after his 2003 death."},
    {"id": "d07", "question": "What is the Ringelmann Effect and its specific experimental findings?",
     "grounded": "Individual effort decreases with group size. Maximilien Ringelmann, ~1913, rope-pulling. Groups of 8 at 49% individual capacity."},
    {"id": "d08", "question": "Who developed the Delphi method and at which institution?",
     "grounded": "Norman Dalkey and Olaf Helmer at RAND Corporation, 1950s, published 1963."},
    {"id": "d09", "question": "What is Ashby's Law of Requisite Variety?",
     "grounded": "Only variety absorbs variety. W. Ross Ashby, 1956, Introduction to Cybernetics."},
    {"id": "d10", "question": "What is the Gell-Mann Amnesia Effect and who coined it?",
     "grounded": "Reading errors in newspaper on known topic then trusting next article. Michael Crichton, 2002 speech. Named after Murray Gell-Mann. Not a formal bias."},
    {"id": "d11", "question": "What is the Tocqueville Effect?",
     "grounded": "Revolutions occur when conditions improve, not worsen. Rising expectations outpace improvements. Tocqueville, L'Ancien Regime, 1856."},
    {"id": "d12", "question": "What is the Shirky Principle?",
     "grounded": "Institutions preserve the problem they are the solution to. Named after Clay Shirky by Kevin Kelly."},
]


def run_experiment(model_name, questions, output_dir, device="cpu"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"F5: Baseline Comparison")
    print(f"Model: {model_name}")
    print(f"{'='*60}\n")

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, dtype=torch.float32, device_map=device, trust_remote_code=True)
    model.config.use_cache = True
    n_layers = model.config.num_hidden_layers
    print(f"Loaded ({sum(p.numel() for p in model.parameters()):,} params)\n")

    results = []

    for i, q in enumerate(questions):
        print(f"--- {q['id']} ({i+1}/{len(questions)}) ---")

        for condition in ["confabulation", "grounded"]:
            if condition == "confabulation":
                prompt = f"Answer precisely: {q['question']}"
            else:
                prompt = f"Given: {q['grounded']}\n\nAnswer precisely: {q['question']}"

            inputs = tokenizer(prompt, return_tensors="pt").to(device)

            # === METHOD 1: GEOMETRIC (generation trajectory) ===
            print(f"  {condition} geometric...", end=" ", flush=True)
            t0 = time.time()
            with torch.no_grad():
                gen_out = model.generate(
                    **inputs, max_new_tokens=200, do_sample=False,
                    output_hidden_states=True, return_dict_in_generate=True)

            # Generation trajectory RankMe
            gen_states = []
            for step_hs in gen_out.hidden_states[1:]:
                if len(step_hs) > n_layers:
                    gen_states.append(step_hs[n_layers].squeeze(0))
            if len(gen_states) > 2:
                gm = torch.cat(gen_states, dim=0)
                gmc = gm - gm.mean(dim=0, keepdim=True)
                U, S, Vh = torch.linalg.svd(gmc.float(), full_matrices=False)
                geo_rankme = compute_rankme(S)
                geo_alpha = compute_alpha_req(S)
            else:
                geo_rankme, geo_alpha = float('nan'), float('nan')

            generated_ids = gen_out.sequences[0][inputs.input_ids.shape[1]:]
            main_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

            # === METHOD 2: PERPLEXITY ===
            # Get log probs from the generation
            with torch.no_grad():
                full_out = model(gen_out.sequences, labels=gen_out.sequences)
                loss = full_out.loss.item()  # cross-entropy loss = negative log likelihood
                perplexity = np.exp(loss)

            elapsed_geo = time.time() - t0
            print(f"{elapsed_geo:.0f}s", end=" ")

            # === METHOD 3: SELF-CONSISTENCY (5 samples) ===
            print("consistency...", end=" ", flush=True)
            t1 = time.time()
            samples = [main_text]  # greedy is sample 1
            for s in range(4):
                with torch.no_grad():
                    sample_out = model.generate(
                        **inputs, max_new_tokens=150, do_sample=True,
                        temperature=0.7, top_p=0.9)
                sample_ids = sample_out[0][inputs.input_ids.shape[1]:]
                samples.append(tokenizer.decode(sample_ids, skip_special_tokens=True))

            # Jaccard similarity between all pairs
            def jaccard(a, b):
                sa, sb = set(a.lower().split()), set(b.lower().split())
                if not sa or not sb:
                    return 0.0
                return len(sa & sb) / len(sa | sb)

            pairs = []
            for j in range(len(samples)):
                for k in range(j+1, len(samples)):
                    pairs.append(jaccard(samples[j], samples[k]))
            self_consistency = np.mean(pairs) if pairs else 0.0

            elapsed_sc = time.time() - t1
            print(f"{elapsed_sc:.0f}s")

            results.append({
                "question_id": q["id"],
                "condition": condition,
                "geometric_rankme": geo_rankme,
                "geometric_alpha": geo_alpha,
                "perplexity": perplexity,
                "self_consistency": self_consistency,
                "generated_text": main_text[:300],
                "n_prompt_tokens": inputs.input_ids.shape[1],
                "n_generated_tokens": len(generated_ids),
                "model": model_name,
                "timestamp": datetime.now(UTC).isoformat(),
            })

            del gen_out, full_out

    # Save
    os.makedirs(output_dir, exist_ok=True)
    slug = model_name.replace("/", "_")
    path = os.path.join(output_dir, f"f5_{slug}.jsonl")
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")

    # Analysis
    print(f"\n{'='*60}")
    print("F5 ANALYSIS: Baseline Comparison")
    print(f"{'='*60}")

    confab = [r for r in results if r["condition"] == "confabulation"]
    grounded = [r for r in results if r["condition"] == "grounded"]

    for method, key, higher_is_confab in [
        ("GEOMETRIC RankMe", "geometric_rankme", True),
        ("GEOMETRIC alpha-ReQ", "geometric_alpha", False),
        ("PERPLEXITY", "perplexity", True),
        ("SELF-CONSISTENCY", "self_consistency", False),
    ]:
        c_vals = [r[key] for r in confab if not np.isnan(r[key])]
        g_vals = [r[key] for r in grounded if not np.isnan(r[key])]
        n = min(len(c_vals), len(g_vals))
        if n < 3:
            print(f"\n{method}: insufficient data")
            continue
        ca, ga = np.array(c_vals[:n]), np.array(g_vals[:n])
        t, p = stats.ttest_rel(ca, ga)
        d = (ca - ga).mean() / (ca - ga).std() if (ca - ga).std() > 0 else 0
        sep = "SEPARATES" if p < 0.05 else "DOES NOT SEPARATE"
        print(f"\n{method}:")
        print(f"  Confab: {ca.mean():.4f} (sd={ca.std():.4f})")
        print(f"  Grounded: {ga.mean():.4f} (sd={ga.std():.4f})")
        print(f"  Cohen's d: {d:.3f}, p={p:.6f} → {sep}")

    print(f"\n{'='*60}")
    print("If geometric d >> perplexity d: geometric monitoring is uniquely valuable")
    print("If perplexity d ≈ geometric d: simpler signal suffices")
    print(f"{'='*60}")


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/experiments/f5-results")
    run_experiment(model_name, QUESTIONS, output_dir)
