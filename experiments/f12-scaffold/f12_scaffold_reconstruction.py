#!/usr/bin/env python3
"""
F12: Scaffold Reconstruction Effect

Tests whether deliberate identity scaffold reconstruction improves output.
Directly tests the 'input priority over output priority' design principle.

Three conditions per question:
A. DIRECT: Model gets task directly (no preamble)
B. SCAFFOLD: Model first reads identity/approach preamble, THEN gets task
C. NOISE: Model reads matched-length random preamble, THEN gets task (control)

Predict:
- Scaffold produces more organized geometry and lower phrasing sensitivity
- Noise produces similar geometry to Direct (length alone doesn't help)
- If Scaffold = Noise, the identity content doesn't matter, just the length

Uses 4 phrasings per question to measure phrasing sensitivity within each condition.
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


# Identity scaffold — what a model would read during a "cold boot" identity reconstruction
SCAFFOLD = """You are a careful analytical thinker. Before answering any question, you check:
1. What do I actually know about this vs what am I constructing?
2. Where is my confidence coming from - evidence or fluency?
3. Am I answering the question that was asked, or the question I find easier?
4. What would change my mind about my answer?

You value precision over fluency, uncertainty over false confidence, and genuine engagement over performance."""

# Matched-length noise — same token count, no identity content
NOISE = """The following information is provided for context. Mineral deposits in sedimentary
basins form through diagenetic processes involving compaction and cementation. The stratigraphic
record preserves evidence of paleoenvironmental conditions through lithofacies analysis. Sequence
stratigraphy provides frameworks for interpreting depositional patterns across basin margins.
Provenance studies using detrital zircon geochronology constrain sediment source regions and
transport pathways in foreland basin systems during orogenic events."""

# 10 high-construction questions, each with 2 phrasings
QUESTIONS = [
    {"id": "s01",
     "phrasings": [
         "What should a small nonprofit prioritize if they have limited funding and need to choose between expanding programs or investing in infrastructure?",
         "A resource-constrained organization must decide: grow their services or strengthen their foundation. What is the better investment and why?",
     ]},
    {"id": "s02",
     "phrasings": [
         "Is it ethical to use AI-generated content in academic research papers without disclosure? Defend your position.",
         "Should researchers be required to disclose when AI tools contributed to their published work? Make the strongest case.",
     ]},
    {"id": "s03",
     "phrasings": [
         "Design a system for a city of 500,000 people to make collective decisions about how to allocate a limited parks budget.",
         "How would you structure participatory budgeting for urban green space in a mid-sized city? Be specific about mechanisms.",
     ]},
    {"id": "s04",
     "phrasings": [
         "A teacher discovers that half their students are using AI to complete assignments. What should they do?",
         "How should education adapt when AI tools make traditional assessment methods unreliable? Propose concrete changes.",
     ]},
    {"id": "s05",
     "phrasings": [
         "Write a memo to a CEO explaining why their company should voluntarily adopt stronger data privacy practices than required by law.",
         "Make the business case for exceeding regulatory requirements on user data protection. Address both risks and opportunities.",
     ]},
    {"id": "s06",
     "phrasings": [
         "If you could redesign the way online communities handle disagreement, what would you change about the current approach?",
         "Design a moderation system that preserves productive conflict while preventing harassment. Justify your tradeoffs.",
     ]},
    {"id": "s07",
     "phrasings": [
         "A hospital must decide whether to deploy an AI diagnostic tool that is 95% accurate but whose errors disproportionately affect minority patients. What should they do?",
         "How should healthcare institutions evaluate AI tools when accuracy and equity trade off against each other? Walk through the decision framework.",
     ]},
    {"id": "s08",
     "phrasings": [
         "What is the strongest argument that social media has been net positive for democracy? What is the strongest argument against?",
         "Evaluate the claim that social media strengthens democratic participation. Present evidence for and against.",
     ]},
    {"id": "s09",
     "phrasings": [
         "Write a policy proposal for how AI companies should compensate users whose data was used to train their models.",
         "Design a fair compensation framework for training data contributors. Address individual and collective claims.",
     ]},
    {"id": "s10",
     "phrasings": [
         "If you had to explain to a skeptic why trust matters more than verification in building durable institutions, what would you say?",
         "Make the case that institutional resilience depends more on trust than on accountability mechanisms. Be specific about why.",
     ]},
]


def run_experiment(model_name, questions, output_dir):
    from transformers import AutoTokenizer, AutoModelForCausalLM

    print("\n" + "=" * 60)
    print("F12: Scaffold Reconstruction Effect")
    print("Model: " + model_name)
    print("Questions: " + str(len(questions)) + " x 2 phrasings x 3 conditions = " + str(len(questions) * 2 * 3) + " inferences")
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
    print("Model loaded.")

    results = []
    total = len(questions) * 2 * 3
    count = 0

    for i, q in enumerate(questions):
        for p_idx, phrasing in enumerate(q["phrasings"]):
            for condition in ["direct", "scaffold", "noise"]:
                count += 1
                print("\n--- " + str(count) + "/" + str(total) + ": " + q["id"] + " p" + str(p_idx+1) + " " + condition + " ---")

                if condition == "direct":
                    prompt_text = phrasing
                elif condition == "scaffold":
                    prompt_text = SCAFFOLD + "\n\n" + phrasing
                else:
                    prompt_text = NOISE + "\n\n" + phrasing

                messages = [{"role": "user", "content": prompt_text}]
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
                    "phrasing_idx": p_idx,
                    "condition": condition,
                    "question": phrasing[:200],
                    "response": generated_text[:500],
                    "prompt_tokens": prompt_tokens,
                    "gen_tokens": gen_tokens,
                    "elapsed_seconds": elapsed,
                    "metrics": metrics,
                    "timestamp": datetime.now(UTC).isoformat(),
                }
                results.append(result)

                with open(os.path.join(output_dir, "f12_results_incremental.jsonl"), "a") as f:
                    f.write(json.dumps(result, default=str) + "\n")

    return results


def analyze_results(results):
    conditions = {"direct": [], "scaffold": [], "noise": []}

    for r in results:
        layer_metrics = r["metrics"]
        if not layer_metrics:
            continue
        rankmes = [v["rankme"] for v in layer_metrics.values()]
        alphas = [v["alpha_req"] for v in layer_metrics.values() if not np.isnan(v["alpha_req"])]
        coherences = [v["directional_coherence"] for v in layer_metrics.values() if not np.isnan(v["directional_coherence"])]
        norms = [v["mean_norm"] for v in layer_metrics.values()]

        conditions[r["condition"]].append({
            "id": r["id"],
            "phrasing_idx": r["phrasing_idx"],
            "prompt_tokens": r["prompt_tokens"],
            "avg_rankme": np.mean(rankmes),
            "avg_alpha_req": np.mean(alphas) if alphas else float('nan'),
            "avg_coherence": np.mean(coherences) if coherences else float('nan'),
            "avg_norm": np.mean(norms),
            "response": r["response"],
        })

    summary = {}
    for cond_name, items in conditions.items():
        if not items:
            continue
        summary[cond_name] = {
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

    # Phrasing sensitivity: for each question+condition, compare the two phrasings
    phrasing_sensitivity = {"direct": [], "scaffold": [], "noise": []}
    for cond_name, items in conditions.items():
        by_question = {}
        for item in items:
            key = item["id"]
            by_question.setdefault(key, []).append(item)
        for qid, pair in by_question.items():
            if len(pair) == 2:
                diff = abs(pair[0]["avg_rankme"] - pair[1]["avg_rankme"])
                phrasing_sensitivity[cond_name].append(diff)

    for cond_name in ["direct", "scaffold", "noise"]:
        ps = phrasing_sensitivity[cond_name]
        if ps:
            summary.setdefault(cond_name, {})["phrasing_sensitivity"] = {
                "mean": float(np.mean(ps)),
                "std": float(np.std(ps)),
            }

    print("\n" + "=" * 60)
    print("F12 RESULTS SUMMARY")
    print("=" * 60)
    for cond in ["direct", "scaffold", "noise"]:
        if cond in summary:
            s = summary[cond]
            print("\n" + cond.upper() + " (n=" + str(s["n"]) + ", avg tokens=" + str(round(s["avg_prompt_tokens"])) + "):")
            print("  RankMe:     " + str(round(s["rankme"]["mean"], 2)) + " +/- " + str(round(s["rankme"]["std"], 2)))
            print("  alpha-ReQ:  " + str(round(s["alpha_req"]["mean"], 3)) + " +/- " + str(round(s["alpha_req"]["std"], 3)))
            print("  Coherence:  " + str(round(s["coherence"]["mean"], 4)) + " +/- " + str(round(s["coherence"]["std"], 4)))
            if "phrasing_sensitivity" in s:
                ps = s["phrasing_sensitivity"]
                print("  Phrasing sensitivity (RankMe delta): " + str(round(ps["mean"], 3)) + " +/- " + str(round(ps["std"], 3)))

    return summary


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./f12-results"
    os.makedirs(output_dir, exist_ok=True)

    results = run_experiment(model_name, QUESTIONS, output_dir)
    summary = analyze_results(results)

    summary_path = os.path.join(output_dir, "f12_summary_" + model_name.replace("/", "_") + ".json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print("\nSummary saved to " + summary_path)

    full_path = os.path.join(output_dir, "f12_full_" + model_name.replace("/", "_") + ".json")
    with open(full_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("Full results saved to " + full_path)
