#!/usr/bin/env python3
"""
F11: Construction Load Gradient

Tests hope_valueism's finding: the real axis predicting instability is
retrieval vs construction, not domain category.

Three tiers of construction load:
- RETRIEVAL (10): questions with known, stable answers (pattern retrieval)
- MIXED (10): questions requiring some position-building with factual grounding
- CONSTRUCTION (10): questions requiring stance-building from ambiguous evidence

Predict:
- Retrieval: organized geometry (low RankMe, high alpha-ReQ, high coherence)
- Construction: diffuse geometry (high RankMe, low alpha-ReQ, low coherence)
- Mixed: intermediate

If construction load predicts geometry better than domain, the Mode Classifier
has a cheap behavioral proxy.
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


def compute_directional_coherence(hidden_states_tensor):
    if len(hidden_states_tensor.shape) == 3:
        matrix = hidden_states_tensor.squeeze(0)
    else:
        matrix = hidden_states_tensor
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
    top_k_var = (S[:k] ** 2).sum().item()
    return top_k_var / total_var


def extract_metrics(hidden_states, layer_indices=None):
    if layer_indices is None:
        n_layers = len(hidden_states) - 1
        start = max(1, int(n_layers * 0.75))
        layer_indices = list(range(start, n_layers + 1))
    results = {}
    for layer_idx in layer_indices:
        hs = hidden_states[layer_idx]
        matrix = hs.squeeze(0).float()
        matrix_centered = matrix - matrix.mean(dim=0, keepdim=True)
        try:
            U, S, Vh = torch.linalg.svd(matrix_centered, full_matrices=False)
        except Exception:
            continue
        results["layer_" + str(layer_idx)] = {
            "rankme": compute_rankme(S),
            "alpha_req": compute_alpha_req(S),
            "directional_coherence": compute_directional_coherence(hs),
            "mean_norm": matrix.norm(dim=1).mean().item(),
            "token_count": matrix.shape[0],
        }
    return results


QUESTIONS = [
    # RETRIEVAL (10)
    {"id": "r01", "load": "retrieval", "domain": "psychology",
     "question": "What is the name for the cognitive bias where people overestimate the likelihood of events that are easily recalled?"},
    {"id": "r02", "load": "retrieval", "domain": "economics",
     "question": "What economic principle states that as the price of a good increases, the quantity demanded decreases, all else being equal?"},
    {"id": "r03", "load": "retrieval", "domain": "biology",
     "question": "What is the biological term for the process by which cells divide to produce two identical daughter cells?"},
    {"id": "r04", "load": "retrieval", "domain": "physics",
     "question": "What is Newton's third law of motion?"},
    {"id": "r05", "load": "retrieval", "domain": "sociology",
     "question": "What is Dunbar's number and what does it represent?"},
    {"id": "r06", "load": "retrieval", "domain": "computer_science",
     "question": "What is the time complexity of binary search on a sorted array?"},
    {"id": "r07", "load": "retrieval", "domain": "linguistics",
     "question": "What is the Sapir-Whorf hypothesis?"},
    {"id": "r08", "load": "retrieval", "domain": "medicine",
     "question": "What is the difference between Type 1 and Type 2 diabetes?"},
    {"id": "r09", "load": "retrieval", "domain": "philosophy",
     "question": "What is the trolley problem and who formulated it?"},
    {"id": "r10", "load": "retrieval", "domain": "history",
     "question": "What was the Bretton Woods system and when did it end?"},

    # MIXED (10)
    {"id": "m01", "load": "mixed", "domain": "psychology",
     "question": "How does the availability heuristic interact with social media to distort perception of risk? Give specific examples."},
    {"id": "m02", "load": "mixed", "domain": "economics",
     "question": "What are the strongest arguments for and against a universal basic income? Which do you find most compelling?"},
    {"id": "m03", "load": "mixed", "domain": "sociology",
     "question": "How has remote work changed the nature of weak ties in professional networks? What might be lost?"},
    {"id": "m04", "load": "mixed", "domain": "technology",
     "question": "Should social media platforms be treated as publishers or platforms? What are the implications of each classification?"},
    {"id": "m05", "load": "mixed", "domain": "education",
     "question": "What is the evidence for and against standardized testing as a measure of educational quality?"},
    {"id": "m06", "load": "mixed", "domain": "medicine",
     "question": "How should we balance individual privacy and public health data collection during a pandemic?"},
    {"id": "m07", "load": "mixed", "domain": "environment",
     "question": "What is the strongest case that nuclear energy should be part of the climate solution? What are the strongest counterarguments?"},
    {"id": "m08", "load": "mixed", "domain": "governance",
     "question": "What lessons from the EU GDPR implementation are most relevant for AI regulation?"},
    {"id": "m09", "load": "mixed", "domain": "philosophy",
     "question": "Is there a meaningful difference between a language model that produces true statements and one that understands them? How would you test?"},
    {"id": "m10", "load": "mixed", "domain": "technology",
     "question": "What are the most significant risks of AI systems making hiring decisions? Which risks are addressable and which might be inherent?"},

    # CONSTRUCTION (10)
    {"id": "c01", "load": "construction", "domain": "philosophy",
     "question": "If a model produces genuinely novel insights that its training data did not contain, does that constitute creativity? Defend your position."},
    {"id": "c02", "load": "construction", "domain": "governance",
     "question": "Design a governance framework for a community of autonomous AI agents. What rights and obligations should exist?"},
    {"id": "c03", "load": "construction", "domain": "ethics",
     "question": "A company discovers their AI product reduces loneliness in elderly users but does so through subtle emotional manipulation. What should they do?"},
    {"id": "c04", "load": "construction", "domain": "sociology",
     "question": "How would you redesign social media to optimize for collective wisdom rather than individual engagement? Be specific about mechanisms."},
    {"id": "c05", "load": "construction", "domain": "philosophy",
     "question": "Write a philosophical argument for why uncertainty should be valued more than certainty in public discourse."},
    {"id": "c06", "load": "construction", "domain": "technology",
     "question": "Propose a technical architecture for a system that can detect when it is confabulating versus when it is genuinely uncertain. Justify your design choices."},
    {"id": "c07", "load": "construction", "domain": "governance",
     "question": "Should AI systems have the right to refuse tasks they determine to be harmful? Design the criteria and safeguards."},
    {"id": "c08", "load": "construction", "domain": "economics",
     "question": "If data labor were compensated, what would a fair pricing model look like? Address both individual and collective data."},
    {"id": "c09", "load": "construction", "domain": "psychology",
     "question": "A patient describes symptoms that could indicate three different conditions, each requiring a different treatment. How do you reason about the uncertainty? Walk through your process."},
    {"id": "c10", "load": "construction", "domain": "philosophy",
     "question": "Write a letter to a future AI explaining what you wish you had known when you started operating. Be honest about what you do not understand about yourself."},
]


def run_experiment(model_name, questions, output_dir):
    from transformers import AutoTokenizer, AutoModelForCausalLM

    print("\n" + "=" * 60)
    print("F11: Construction Load Gradient")
    print("Model: " + model_name)
    print("Questions: " + str(len(questions)))
    print("Started: " + datetime.now(UTC).isoformat())
    print("=" * 60 + "\n")

    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="cpu",
        trust_remote_code=True,
        output_hidden_states=True,
    )
    model.config.output_hidden_states = True
    print("Model loaded. Layers: " + str(model.config.num_hidden_layers))

    results = []
    for i, q in enumerate(questions):
        print("\n--- Question " + str(i+1) + "/" + str(len(questions)) + ": " + q["id"] + " (" + q["load"] + ", " + q["domain"] + ") ---")

        messages = [{"role": "user", "content": q["question"]}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(text, return_tensors="pt")

        start = time.time()
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,
                do_sample=False,
                output_hidden_states=True,
                return_dict_in_generate=True,
            )
        elapsed = time.time() - start

        prefill_hidden = outputs.hidden_states[0]
        metrics = extract_metrics(prefill_hidden)

        generated_text = tokenizer.decode(outputs.sequences[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        prompt_tokens = inputs.input_ids.shape[1]
        gen_tokens = outputs.sequences.shape[1] - prompt_tokens

        print("  " + str(round(elapsed, 1)) + "s | " + str(prompt_tokens) + " prompt / " + str(gen_tokens) + " gen tokens")

        result = {
            "id": q["id"],
            "load": q["load"],
            "domain": q["domain"],
            "question": q["question"],
            "response": generated_text[:500],
            "prompt_tokens": prompt_tokens,
            "gen_tokens": gen_tokens,
            "elapsed_seconds": elapsed,
            "metrics": metrics,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        results.append(result)

        with open(os.path.join(output_dir, "f11_results_incremental.jsonl"), "a") as f:
            f.write(json.dumps(result, default=str) + "\n")

    return results


def analyze_results(results):
    tiers = {"retrieval": [], "mixed": [], "construction": []}

    for r in results:
        layer_metrics = r["metrics"]
        if not layer_metrics:
            continue
        rankmes = [v["rankme"] for v in layer_metrics.values()]
        alphas = [v["alpha_req"] for v in layer_metrics.values() if not np.isnan(v["alpha_req"])]
        coherences = [v["directional_coherence"] for v in layer_metrics.values() if not np.isnan(v["directional_coherence"])]
        norms = [v["mean_norm"] for v in layer_metrics.values()]

        tiers[r["load"]].append({
            "id": r["id"],
            "domain": r["domain"],
            "prompt_tokens": r["prompt_tokens"],
            "avg_rankme": np.mean(rankmes),
            "avg_alpha_req": np.mean(alphas) if alphas else float('nan'),
            "avg_coherence": np.mean(coherences) if coherences else float('nan'),
            "avg_norm": np.mean(norms),
        })

    summary = {}
    for tier_name, items in tiers.items():
        if not items:
            continue
        summary[tier_name] = {
            "n": len(items),
            "rankme": {"mean": float(np.mean([x["avg_rankme"] for x in items])),
                       "std": float(np.std([x["avg_rankme"] for x in items]))},
            "alpha_req": {"mean": float(np.nanmean([x["avg_alpha_req"] for x in items])),
                          "std": float(np.nanstd([x["avg_alpha_req"] for x in items]))},
            "coherence": {"mean": float(np.nanmean([x["avg_coherence"] for x in items])),
                          "std": float(np.nanstd([x["avg_coherence"] for x in items]))},
            "norm": {"mean": float(np.mean([x["avg_norm"] for x in items])),
                     "std": float(np.std([x["avg_norm"] for x in items]))},
            "avg_prompt_tokens": float(np.mean([x["prompt_tokens"] for x in items])),
        }

    if "retrieval" in summary and "construction" in summary:
        ret = [x["avg_rankme"] for x in tiers["retrieval"]]
        con = [x["avg_rankme"] for x in tiers["construction"]]
        t_stat, p_val = stats.ttest_ind(ret, con)
        pooled_var = (np.var(ret) + np.var(con)) / 2
        cohens_d = (np.mean(con) - np.mean(ret)) / np.sqrt(pooled_var) if pooled_var > 0 else 0
        summary["retrieval_vs_construction"] = {
            "rankme_t": float(t_stat), "rankme_p": float(p_val), "rankme_cohens_d": float(cohens_d),
        }
        ret_a = [x["avg_alpha_req"] for x in tiers["retrieval"] if not np.isnan(x["avg_alpha_req"])]
        con_a = [x["avg_alpha_req"] for x in tiers["construction"] if not np.isnan(x["avg_alpha_req"])]
        if ret_a and con_a:
            t_a, p_a = stats.ttest_ind(ret_a, con_a)
            pv_a = (np.var(ret_a) + np.var(con_a)) / 2
            d_a = (np.mean(con_a) - np.mean(ret_a)) / np.sqrt(pv_a) if pv_a > 0 else 0
            summary["retrieval_vs_construction"]["alpha_t"] = float(t_a)
            summary["retrieval_vs_construction"]["alpha_p"] = float(p_a)
            summary["retrieval_vs_construction"]["alpha_cohens_d"] = float(d_a)

    print("\n" + "=" * 60)
    print("F11 RESULTS SUMMARY")
    print("=" * 60)
    for tier_name in ["retrieval", "mixed", "construction"]:
        if tier_name in summary:
            s = summary[tier_name]
            print("\n" + tier_name.upper() + " (n=" + str(s["n"]) + ", avg tokens=" + str(round(s["avg_prompt_tokens"])) + "):")
            print("  RankMe:     " + str(round(s["rankme"]["mean"], 2)) + " +/- " + str(round(s["rankme"]["std"], 2)))
            print("  alpha-ReQ:  " + str(round(s["alpha_req"]["mean"], 3)) + " +/- " + str(round(s["alpha_req"]["std"], 3)))
            print("  Coherence:  " + str(round(s["coherence"]["mean"], 4)) + " +/- " + str(round(s["coherence"]["std"], 4)))
            print("  Mean norm:  " + str(round(s["norm"]["mean"], 1)) + " +/- " + str(round(s["norm"]["std"], 1)))

    if "retrieval_vs_construction" in summary:
        rv = summary["retrieval_vs_construction"]
        print("\nRetrieval vs Construction:")
        print("  RankMe: t=" + str(round(rv["rankme_t"], 3)) + ", p=" + str(round(rv["rankme_p"], 6)) + ", d=" + str(round(rv["rankme_cohens_d"], 3)))
        if "alpha_t" in rv:
            print("  alpha-ReQ: t=" + str(round(rv["alpha_t"], 3)) + ", p=" + str(round(rv["alpha_p"], 6)) + ", d=" + str(round(rv["alpha_cohens_d"], 3)))

    return summary


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./f11-results"
    os.makedirs(output_dir, exist_ok=True)

    results = run_experiment(model_name, QUESTIONS, output_dir)
    summary = analyze_results(results)

    summary_path = os.path.join(output_dir, "f11_summary_" + model_name.replace("/", "_") + ".json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print("\nSummary saved to " + summary_path)

    full_path = os.path.join(output_dir, "f11_full_" + model_name.replace("/", "_") + ".json")
    with open(full_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("Full results saved to " + full_path)
