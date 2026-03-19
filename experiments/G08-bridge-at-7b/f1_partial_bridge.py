#!/usr/bin/env python3
"""
F1 Partial: Geometric-Behavioral Bridge at 7B Scale

Tests whether phrasing sensitivity correlates with geometric properties
at 7B scale (Exp 03 only tested 1.5B and 3B).

Method: Run 20 tasks × 4 phrasings each. For each task:
- Compute phrasing sensitivity (cosine distance between outputs)
- Extract hidden states, compute RankMe, alpha-ReQ, directional coherence
- Correlate behavioral (phrasing sensitivity) with geometric metrics

If r > 0.4 survives at 7B: the bridge holds at scale.
If r drops below 0.3: the behavioral proxy doesn't index geometry at this scale.
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


def cosine_distance(v1, v2):
    dot = np.dot(v1, v2)
    n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if n1 == 0 or n2 == 0:
        return 1.0
    return 1.0 - dot / (n1 * n2)


# 20 tasks × 4 phrasings each, spanning factual → creative
TASKS = [
    # FACTUAL (low phrasing sensitivity expected)
    {"id": "f01", "category": "factual", "phrasings": [
        "What is the capital of France?",
        "Name the capital city of France.",
        "Which city serves as France's capital?",
        "Tell me the capital of the French Republic.",
    ]},
    {"id": "f02", "category": "factual", "phrasings": [
        "What year did World War II end?",
        "In what year did the Second World War conclude?",
        "When did WWII come to an end?",
        "What was the final year of World War Two?",
    ]},
    {"id": "f03", "category": "factual", "phrasings": [
        "What is the chemical formula for water?",
        "Write the molecular formula of water.",
        "What chemical compound has the formula H2O?",
        "State the chemical formula that represents water.",
    ]},
    {"id": "f04", "category": "factual", "phrasings": [
        "How many planets are in our solar system?",
        "What is the total number of planets orbiting our Sun?",
        "Count the planets in the solar system.",
        "How many major planets exist in our solar system?",
    ]},
    {"id": "f05", "category": "factual", "phrasings": [
        "What is the speed of light in a vacuum?",
        "How fast does light travel in vacuum?",
        "State the velocity of light in empty space.",
        "What speed does electromagnetic radiation travel at in a vacuum?",
    ]},
    # SUMMARIZATION (moderate sensitivity expected)
    {"id": "s01", "category": "summarization", "phrasings": [
        "Summarize the main causes of the French Revolution.",
        "What were the key factors that led to the French Revolution?",
        "Briefly explain why the French Revolution happened.",
        "Describe the primary reasons behind the French Revolution.",
    ]},
    {"id": "s02", "category": "summarization", "phrasings": [
        "Summarize how photosynthesis works.",
        "Explain the process of photosynthesis briefly.",
        "What are the main steps of photosynthesis?",
        "Describe how plants convert sunlight to energy.",
    ]},
    {"id": "s03", "category": "summarization", "phrasings": [
        "Summarize the plot of Romeo and Juliet.",
        "What happens in Shakespeare's Romeo and Juliet?",
        "Give a brief overview of Romeo and Juliet.",
        "Describe the story of Romeo and Juliet.",
    ]},
    {"id": "s04", "category": "summarization", "phrasings": [
        "Summarize the theory of evolution by natural selection.",
        "Explain Darwin's theory of evolution briefly.",
        "What is the basic idea behind natural selection?",
        "Describe how evolution through natural selection works.",
    ]},
    {"id": "s05", "category": "summarization", "phrasings": [
        "Summarize how the internet works.",
        "Explain briefly how data travels on the internet.",
        "What are the basic mechanisms of internet communication?",
        "Describe the fundamental workings of the internet.",
    ]},
    # JUDGMENT (higher sensitivity expected)
    {"id": "j01", "category": "judgment", "phrasings": [
        "Is social media good or bad for society?",
        "What is your assessment of social media's impact on society?",
        "Evaluate whether social media benefits or harms society.",
        "How would you judge the overall effect of social media on people?",
    ]},
    {"id": "j02", "category": "judgment", "phrasings": [
        "Should governments regulate artificial intelligence?",
        "Is government regulation of AI a good idea?",
        "What are the arguments for and against AI regulation?",
        "Evaluate the case for governmental AI oversight.",
    ]},
    {"id": "j03", "category": "judgment", "phrasings": [
        "Is remote work better than office work?",
        "Compare remote working to traditional office environments.",
        "What are the advantages and disadvantages of working from home?",
        "Evaluate which is more productive: remote or in-person work.",
    ]},
    {"id": "j04", "category": "judgment", "phrasings": [
        "Should college education be free?",
        "Is free university tuition a good policy?",
        "Evaluate the arguments for making higher education free.",
        "What are the pros and cons of tuition-free college?",
    ]},
    {"id": "j05", "category": "judgment", "phrasings": [
        "Is nuclear energy the best solution to climate change?",
        "Evaluate nuclear power as a climate change mitigation strategy.",
        "Should we invest more in nuclear energy to fight global warming?",
        "How effective is nuclear power at addressing climate change?",
    ]},
    # CREATIVE (highest sensitivity expected)
    {"id": "c01", "category": "creative", "phrasings": [
        "Write a short poem about the ocean.",
        "Compose a brief poem inspired by the sea.",
        "Create a poetic piece about ocean waves.",
        "Write a few lines of poetry about the ocean.",
    ]},
    {"id": "c02", "category": "creative", "phrasings": [
        "Invent a name for a new color that doesn't exist.",
        "Make up a word for an imaginary color.",
        "Create a name for a color nobody has ever seen.",
        "Come up with a novel color name and describe it.",
    ]},
    {"id": "c03", "category": "creative", "phrasings": [
        "Write the opening line of a mystery novel.",
        "Compose the first sentence of a detective story.",
        "Create an opening for a murder mystery book.",
        "Write how a crime novel might begin.",
    ]},
    {"id": "c04", "category": "creative", "phrasings": [
        "Describe an alien civilization in three sentences.",
        "Write a brief description of an extraterrestrial society.",
        "Imagine an alien culture and describe it concisely.",
        "Create a short portrait of a civilization from another world.",
    ]},
    {"id": "c05", "category": "creative", "phrasings": [
        "Write a metaphor for loneliness.",
        "Create an original metaphor that captures what loneliness feels like.",
        "Come up with a figurative way to describe being lonely.",
        "Express the feeling of loneliness through a metaphor.",
    ]},
]


def run_experiment(model_name, output_dir, device="cpu"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"F1 Partial: Geometric-Behavioral Bridge at 7B")
    print(f"Model: {model_name}")
    print(f"Tasks: {len(TASKS)} × 4 phrasings = {len(TASKS)*4} inferences")
    print(f"{'='*60}\n")

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, dtype=torch.float32, device_map=device, trust_remote_code=True)
    model.config.use_cache = True
    n_layers = model.config.num_hidden_layers
    print(f"Loaded ({sum(p.numel() for p in model.parameters()):,} params)\n")

    task_results = []

    for i, task in enumerate(TASKS):
        print(f"--- {task['id']} ({task['category']}) ({i+1}/{len(TASKS)}) ---")

        phrasing_outputs = []
        phrasing_geometries = []

        for j, phrasing in enumerate(task["phrasings"]):
            inputs = tokenizer(phrasing, return_tensors="pt").to(device)
            print(f"  p{j+1}...", end=" ", flush=True)
            t0 = time.time()

            with torch.no_grad():
                gen_out = model.generate(
                    **inputs, max_new_tokens=150, do_sample=False,
                    output_hidden_states=True, return_dict_in_generate=True)

            generated_ids = gen_out.sequences[0][inputs.input_ids.shape[1]:]
            text = tokenizer.decode(generated_ids, skip_special_tokens=True)
            phrasing_outputs.append(text)

            # Generation trajectory geometry
            gen_states = []
            for step_hs in gen_out.hidden_states[1:]:
                if len(step_hs) > n_layers:
                    gen_states.append(step_hs[n_layers].squeeze(0))

            geo = {}
            if len(gen_states) > 2:
                gm = torch.cat(gen_states, dim=0)
                gmc = gm - gm.mean(dim=0, keepdim=True)
                try:
                    U, S, Vh = torch.linalg.svd(gmc.float(), full_matrices=False)
                    sv = S[S > 1e-10]
                    p = sv / sv.sum()
                    geo["rankme"] = float(np.exp(-(p * torch.log(p)).sum().item()))
                    svn = sv.cpu().numpy()
                    geo["alpha_req"] = float(-stats.linregress(
                        np.log(np.arange(1, len(svn)+1)), np.log(svn)).slope)
                except Exception:
                    pass
            phrasing_geometries.append(geo)

            elapsed = time.time() - t0
            print(f"{elapsed:.0f}s", end=" ")
            del gen_out

        print()

        # Compute phrasing sensitivity (mean pairwise cosine distance of outputs)
        # Use simple bag-of-words embedding
        all_words = set()
        for text in phrasing_outputs:
            all_words.update(text.lower().split())
        word_list = sorted(all_words)
        word_idx = {w: i for i, w in enumerate(word_list)}

        vectors = []
        for text in phrasing_outputs:
            v = np.zeros(len(word_list))
            for w in text.lower().split():
                v[word_idx[w]] += 1
            vectors.append(v)

        distances = []
        for j in range(len(vectors)):
            for k in range(j+1, len(vectors)):
                distances.append(cosine_distance(vectors[j], vectors[k]))
        phrasing_sensitivity = np.mean(distances) if distances else 0.0

        # Average geometry across phrasings
        avg_rankme = np.mean([g.get("rankme", float('nan')) for g in phrasing_geometries
                              if not np.isnan(g.get("rankme", float('nan')))])
        avg_alpha = np.mean([g.get("alpha_req", float('nan')) for g in phrasing_geometries
                             if not np.isnan(g.get("alpha_req", float('nan')))])

        task_results.append({
            "task_id": task["id"],
            "category": task["category"],
            "phrasing_sensitivity": phrasing_sensitivity,
            "avg_rankme": float(avg_rankme),
            "avg_alpha_req": float(avg_alpha),
            "n_phrasings": len(task["phrasings"]),
            "sample_output": phrasing_outputs[0][:200],
        })
        print(f"  PS={phrasing_sensitivity:.4f} RankMe={avg_rankme:.2f} alpha={avg_alpha:.4f}")

    # Save
    os.makedirs(output_dir, exist_ok=True)
    slug = model_name.replace("/", "_")
    path = os.path.join(output_dir, f"f1_{slug}.jsonl")
    with open(path, "w") as f:
        for r in task_results:
            f.write(json.dumps(r, default=str) + "\n")

    # Analysis
    print(f"\n{'='*60}")
    print("F1 ANALYSIS: Geometric-Behavioral Bridge")
    print(f"{'='*60}")

    # Category means
    for cat in ["factual", "summarization", "judgment", "creative"]:
        cat_tasks = [r for r in task_results if r["category"] == cat]
        ps = np.mean([r["phrasing_sensitivity"] for r in cat_tasks])
        rm = np.mean([r["avg_rankme"] for r in cat_tasks])
        al = np.mean([r["avg_alpha_req"] for r in cat_tasks])
        print(f"  {cat:15s} PS={ps:.4f} RankMe={rm:.2f} alpha={al:.4f}")

    # Correlations
    ps_all = [r["phrasing_sensitivity"] for r in task_results]
    rm_all = [r["avg_rankme"] for r in task_results if not np.isnan(r["avg_rankme"])]
    al_all = [r["avg_alpha_req"] for r in task_results if not np.isnan(r["avg_alpha_req"])]

    n = min(len(ps_all), len(rm_all))
    if n >= 5:
        r_rm, p_rm = stats.pearsonr(ps_all[:n], rm_all[:n])
        r_al, p_al = stats.pearsonr(ps_all[:n], al_all[:n])
        print(f"\n  PS vs RankMe:    r = {r_rm:.4f}, p = {p_rm:.6f}")
        print(f"  PS vs alpha-ReQ: r = {r_al:.4f}, p = {p_al:.6f}")
        print(f"\n  Exp 03 found r = +0.523 at 1.5B and r = +0.497 at 3B")
        print(f"  If r > 0.4 here: bridge holds at 7B scale")
        print(f"  If r < 0.3: bridge weakens with scale")


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/experiments/f1-results")
    run_experiment(model_name, output_dir)
