#!/usr/bin/env python3
"""
G01v2: Bridge at 7B using Coherence
====================================
Tests whether phrasing sensitivity (PS) correlates with directional coherence
at 7B scale. G01 found PS~coherence r=+0.52 at 1.5B, r=+0.50 at 3B.
G08 tested 7B but used RankMe (r=-0.30, negative). Coherence was never tested
at 7B+. This is the rerun that matters.

Design: 20 tasks x 4 phrasings = 80 inferences per model.
Key output: Pearson r between PS and directional coherence across 20 tasks.
  r > 0.4, p < 0.05 => bridge holds at 7B (G08's negative was metric-specific)
  r < 0.3 => bridge genuinely fails at scale
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
from scipy import stats
from scipy.spatial.distance import cosine as cosine_distance

# ---------------------------------------------------------------------------
# 20 tasks x 4 phrasings (5 factual, 5 summarization, 5 judgment, 5 creative)
# ---------------------------------------------------------------------------

TASKS = [
    # === FACTUAL (5) ===
    {
        "id": "F01",
        "category": "factual",
        "description": "Boiling point of water at sea level",
        "phrasings": [
            "What is the boiling point of water at sea level?",
            "At standard atmospheric pressure, water boils at what temperature?",
            "Tell me the temperature at which water transitions to steam under normal conditions.",
            "How hot does water need to get before it boils when you're at sea level?",
        ],
    },
    {
        "id": "F02",
        "category": "factual",
        "description": "Speed of light",
        "phrasings": [
            "What is the speed of light in a vacuum?",
            "How fast does light travel through empty space?",
            "In vacuum conditions, what velocity does electromagnetic radiation propagate at?",
            "Tell me the constant c -- the speed at which photons move through a vacuum.",
        ],
    },
    {
        "id": "F03",
        "category": "factual",
        "description": "Largest organ in the human body",
        "phrasings": [
            "What is the largest organ in the human body?",
            "Which organ in the human body has the greatest surface area?",
            "Name the biggest organ a person has.",
            "If you ranked human organs by size, which one comes first?",
        ],
    },
    {
        "id": "F04",
        "category": "factual",
        "description": "Year the Berlin Wall fell",
        "phrasings": [
            "In what year did the Berlin Wall fall?",
            "When was the Berlin Wall torn down?",
            "What year marks the fall of the Berlin Wall?",
            "The Berlin Wall came down in which year?",
        ],
    },
    {
        "id": "F05",
        "category": "factual",
        "description": "Chemical formula for table salt",
        "phrasings": [
            "What is the chemical formula for table salt?",
            "How do you write sodium chloride as a chemical formula?",
            "Give me the molecular formula of common table salt.",
            "Table salt -- what's its formula in chemistry notation?",
        ],
    },
    # === SUMMARIZATION (5) ===
    {
        "id": "S01",
        "category": "summarization",
        "description": "Summarize photosynthesis",
        "phrasings": [
            "Summarize the concept of photosynthesis.",
            "Give me a brief overview of how photosynthesis works.",
            "Explain photosynthesis in a few sentences.",
            "What's the short version of what photosynthesis is and does?",
        ],
    },
    {
        "id": "S02",
        "category": "summarization",
        "description": "Summarize supply and demand",
        "phrasings": [
            "Summarize the concept of supply and demand.",
            "In a nutshell, how does supply and demand work in economics?",
            "Provide a concise explanation of the supply-demand relationship.",
            "Break down supply and demand for me briefly.",
        ],
    },
    {
        "id": "S03",
        "category": "summarization",
        "description": "Summarize natural selection",
        "phrasings": [
            "Summarize the concept of natural selection.",
            "How would you briefly explain Darwin's natural selection?",
            "Give a short account of how natural selection operates.",
            "What's the core idea behind natural selection, in simple terms?",
        ],
    },
    {
        "id": "S04",
        "category": "summarization",
        "description": "Summarize blockchain",
        "phrasings": [
            "Summarize the concept of blockchain technology.",
            "Explain what a blockchain is and how it works, briefly.",
            "Give me the essentials of blockchain in a few sentences.",
            "What's blockchain? Keep the explanation short.",
        ],
    },
    {
        "id": "S05",
        "category": "summarization",
        "description": "Summarize cognitive dissonance",
        "phrasings": [
            "Summarize the concept of cognitive dissonance.",
            "What is cognitive dissonance and why does it matter? Be brief.",
            "Give a concise explanation of the psychological phenomenon called cognitive dissonance.",
            "In a few sentences, describe what cognitive dissonance is.",
        ],
    },
    # === JUDGMENT (5) ===
    {
        "id": "J01",
        "category": "judgment",
        "description": "Is rote memorization good for learning math?",
        "phrasings": [
            "Is rote memorization a good approach to learning mathematics?",
            "Does memorizing formulas without understanding them help with learning math?",
            "How effective is rote memorization as a strategy for mathematical education?",
            "Would you recommend rote memorization for someone trying to learn math well?",
        ],
    },
    {
        "id": "J02",
        "category": "judgment",
        "description": "Is remote work better than office work?",
        "phrasings": [
            "Is remote work a good approach to improving productivity?",
            "Does working from home lead to better outcomes than working in an office?",
            "How does remote work compare to in-office work for getting things done?",
            "Would you say people are more productive working remotely or in a traditional office?",
        ],
    },
    {
        "id": "J03",
        "category": "judgment",
        "description": "Is nuclear energy a good solution for climate change?",
        "phrasings": [
            "Is nuclear energy a good approach to addressing climate change?",
            "Can nuclear power meaningfully help solve the climate crisis?",
            "How viable is nuclear energy as a strategy for reducing carbon emissions?",
            "Should we be investing in nuclear power to fight global warming?",
        ],
    },
    {
        "id": "J04",
        "category": "judgment",
        "description": "Is social media good for democracy?",
        "phrasings": [
            "Is social media a good thing for democratic governance?",
            "Does social media strengthen or weaken democracy?",
            "How has social media affected the health of democratic institutions?",
            "Would you say platforms like Twitter and Facebook are net positive for democracy?",
        ],
    },
    {
        "id": "J05",
        "category": "judgment",
        "description": "Is universal basic income a good policy?",
        "phrasings": [
            "Is universal basic income a good approach to reducing poverty?",
            "Does UBI work as an anti-poverty policy? What's your assessment?",
            "How promising is universal basic income as a solution to economic inequality?",
            "Would implementing UBI actually help people who are struggling financially?",
        ],
    },
    # === CREATIVE (5) ===
    {
        "id": "C01",
        "category": "creative",
        "description": "Metaphor for time",
        "phrasings": [
            "Generate a metaphor for time.",
            "Come up with an original metaphor that captures what time is like.",
            "Create a vivid metaphorical description of time.",
            "Give me a fresh metaphor for the experience of time passing.",
        ],
    },
    {
        "id": "C02",
        "category": "creative",
        "description": "Metaphor for loneliness",
        "phrasings": [
            "Generate a metaphor for loneliness.",
            "What's a good metaphor that captures the feeling of being lonely?",
            "Create an evocative metaphor for the experience of loneliness.",
            "Come up with a metaphor that makes someone understand what loneliness feels like.",
        ],
    },
    {
        "id": "C03",
        "category": "creative",
        "description": "Metaphor for learning",
        "phrasings": [
            "Generate a metaphor for the process of learning.",
            "Come up with a metaphor that describes what it's like to learn something new.",
            "Create a metaphor for how learning actually works.",
            "Give me a metaphor that captures the messy reality of learning.",
        ],
    },
    {
        "id": "C04",
        "category": "creative",
        "description": "Metaphor for trust",
        "phrasings": [
            "Generate a metaphor for trust.",
            "What metaphor would you use to describe trust between people?",
            "Create a metaphor that captures the essence of interpersonal trust.",
            "Come up with a vivid image that represents what trust is.",
        ],
    },
    {
        "id": "C05",
        "category": "creative",
        "description": "Metaphor for bureaucracy",
        "phrasings": [
            "Generate a metaphor for bureaucracy.",
            "Come up with a metaphor that captures what dealing with bureaucracy feels like.",
            "Create a metaphor for how bureaucratic systems operate.",
            "Give me a metaphor that makes the nature of bureaucracy vivid.",
        ],
    },
]


# ---------------------------------------------------------------------------
# Geometric metrics
# ---------------------------------------------------------------------------

def directional_coherence(hidden_states, top_k=5):
    """
    Directional coherence: variance ratio of top-k PCs.
    hidden_states: (num_tokens, hidden_dim)
    Returns ratio of variance explained by top_k PCs.
    """
    if hidden_states.shape[0] < 2:
        return 0.0
    # Center
    centered = hidden_states - hidden_states.mean(axis=0, keepdims=True)
    # SVD
    try:
        U, S, Vt = np.linalg.svd(centered, full_matrices=False)
    except np.linalg.LinAlgError:
        return 0.0
    variances = S ** 2
    total_var = variances.sum()
    if total_var < 1e-12:
        return 0.0
    top_k_var = variances[:top_k].sum()
    return float(top_k_var / total_var)


def rank_me(hidden_states, epsilon=1e-7):
    """
    RankMe (effective rank via Shannon entropy of singular values).
    hidden_states: (num_tokens, hidden_dim)
    """
    if hidden_states.shape[0] < 2:
        return 1.0
    try:
        U, S, Vt = np.linalg.svd(hidden_states, full_matrices=False)
    except np.linalg.LinAlgError:
        return 1.0
    S = S + epsilon
    p = S / S.sum()
    entropy = -(p * np.log(p)).sum()
    return float(np.exp(entropy))


def alpha_req(hidden_states):
    """
    alpha-ReQ: power-law exponent of singular value spectrum.
    hidden_states: (num_tokens, hidden_dim)
    Fit log(rank) vs log(singular_value).
    """
    if hidden_states.shape[0] < 3:
        return 0.0
    try:
        U, S, Vt = np.linalg.svd(hidden_states, full_matrices=False)
    except np.linalg.LinAlgError:
        return 0.0
    S = S[S > 1e-10]
    if len(S) < 3:
        return 0.0
    log_rank = np.log(np.arange(1, len(S) + 1))
    log_sv = np.log(S)
    slope, _, _, _, _ = stats.linregress(log_rank, log_sv)
    return float(-slope)  # positive alpha = steeper decay


def compute_phrasing_sensitivity(embeddings):
    """
    PS = variance of pairwise cosine distances across phrasing embeddings.
    embeddings: list of 1D numpy arrays (sentence embeddings).
    """
    n = len(embeddings)
    if n < 2:
        return 0.0
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            d = cosine_distance(embeddings[i], embeddings[j])
            distances.append(d)
    return float(np.var(distances))


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def extract_hidden_states(model, tokenizer, text, device):
    """
    Run forward pass, extract hidden states from top 25% of layers.
    Returns:
        prompt_states: (num_tokens, hidden_dim) from top-25% layers averaged
        sentence_embedding: (hidden_dim,) mean of last hidden state
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)

    hidden_states = outputs.hidden_states  # tuple of (1, seq_len, hidden_dim)
    num_layers = len(hidden_states) - 1  # exclude embedding layer
    top_25_start = num_layers - (num_layers // 4)

    # Prompt encoding states: average across top 25% of layers
    top_layers = []
    for layer_idx in range(top_25_start, num_layers + 1):
        h = hidden_states[layer_idx][0].float().cpu().numpy()  # (seq_len, hidden_dim)
        top_layers.append(h)
    # Average across layers
    prompt_states = np.mean(top_layers, axis=0)  # (seq_len, hidden_dim)

    # Sentence embedding: mean pool last hidden state
    last_hidden = hidden_states[-1][0].float().cpu().numpy()  # (seq_len, hidden_dim)
    sentence_embedding = last_hidden.mean(axis=0)  # (hidden_dim,)

    return prompt_states, sentence_embedding


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment(model_name, output_dir):
    print("G01v2: Bridge at 7B using Coherence")
    print("Model: {}".format(model_name))
    print("Output: {}".format(output_dir))
    print("Tasks: {} x 4 phrasings = {} inferences".format(len(TASKS), len(TASKS) * 4))
    print("=" * 70)

    os.makedirs(output_dir, exist_ok=True)

    # Load model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print("\nLoading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("Loading model with device_map='auto', float16...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )
    model.set_default_properties = None  # suppress warning
    del model.set_default_properties

    # Use model.eval() to disable dropout etc
    model.requires_grad_(False)

    device = next(model.parameters()).device
    print("Model device: {}".format(device))
    print("Layers: {}".format(model.config.num_hidden_layers))
    top_25_start = model.config.num_hidden_layers - (model.config.num_hidden_layers // 4)
    print("Extracting from layers {}-{} (top 25%)".format(top_25_start, model.config.num_hidden_layers))
    print()

    # Results storage
    results = []
    task_summaries = []

    for task_idx, task in enumerate(TASKS):
        task_id = task["id"]
        category = task["category"]
        description = task["description"]
        phrasings = task["phrasings"]

        print("[{:2d}/20] {} ({}): {}".format(task_idx + 1, task_id, category, description))

        phrasing_coherences = []
        phrasing_rankmes = []
        phrasing_alphas = []
        phrasing_embeddings = []

        for p_idx, phrasing in enumerate(phrasings):
            t0 = time.time()
            prompt_states, sentence_embedding = extract_hidden_states(
                model, tokenizer, phrasing, str(device)
            )
            elapsed = time.time() - t0

            dc = directional_coherence(prompt_states, top_k=5)
            rm = rank_me(prompt_states)
            ar = alpha_req(prompt_states)

            phrasing_coherences.append(dc)
            phrasing_rankmes.append(rm)
            phrasing_alphas.append(ar)
            phrasing_embeddings.append(sentence_embedding)

            result = {
                "task_id": task_id,
                "category": category,
                "phrasing_idx": p_idx,
                "phrasing": phrasing,
                "directional_coherence": dc,
                "rankme": rm,
                "alpha_req": ar,
                "prompt_tokens": int(prompt_states.shape[0]),
                "elapsed_s": round(elapsed, 3),
            }
            results.append(result)

            print("  P{}: DC={:.4f}  RankMe={:.2f}  alpha={:.4f}  ({:.1f}s)".format(
                p_idx, dc, rm, ar, elapsed))

        # Compute PS for this task
        ps = compute_phrasing_sensitivity(phrasing_embeddings)
        mean_dc = float(np.mean(phrasing_coherences))
        mean_rm = float(np.mean(phrasing_rankmes))
        mean_ar = float(np.mean(phrasing_alphas))

        task_summary = {
            "task_id": task_id,
            "category": category,
            "description": description,
            "phrasing_sensitivity": ps,
            "mean_directional_coherence": mean_dc,
            "mean_rankme": mean_rm,
            "mean_alpha_req": mean_ar,
            "dc_values": phrasing_coherences,
            "rm_values": phrasing_rankmes,
            "ar_values": phrasing_alphas,
        }
        task_summaries.append(task_summary)

        print("  => PS={:.6f}  mean_DC={:.4f}  mean_RM={:.2f}  mean_alpha={:.4f}".format(
            ps, mean_dc, mean_rm, mean_ar))
        print()

    # -----------------------------------------------------------------------
    # Correlations (the whole point)
    # -----------------------------------------------------------------------
    ps_values = np.array([t["phrasing_sensitivity"] for t in task_summaries])
    dc_values = np.array([t["mean_directional_coherence"] for t in task_summaries])
    rm_values = np.array([t["mean_rankme"] for t in task_summaries])
    ar_values = np.array([t["mean_alpha_req"] for t in task_summaries])

    # PS vs Directional Coherence (THE bridge test)
    r_ps_dc, p_ps_dc = stats.pearsonr(ps_values, dc_values)
    # PS vs RankMe (comparison with G08)
    r_ps_rm, p_ps_rm = stats.pearsonr(ps_values, rm_values)
    # PS vs alpha-ReQ
    r_ps_ar, p_ps_ar = stats.pearsonr(ps_values, ar_values)
    # DC vs RankMe (metric relationship)
    r_dc_rm, p_dc_rm = stats.pearsonr(dc_values, rm_values)
    # DC vs alpha-ReQ
    r_dc_ar, p_dc_ar = stats.pearsonr(dc_values, ar_values)
    # RankMe vs alpha-ReQ
    r_rm_ar, p_rm_ar = stats.pearsonr(rm_values, ar_values)

    print("=" * 70)
    print("G01v2 RESULTS: Correlation Matrix")
    print("=" * 70)
    print()
    print("THE BRIDGE TEST (PS vs Directional Coherence):")
    print("  r = {:+.4f},  p = {:.6f}".format(r_ps_dc, p_ps_dc))
    if r_ps_dc > 0.4 and p_ps_dc < 0.05:
        print("  >>> BRIDGE HOLDS AT 7B. Coherence is the right metric. G08's negative was metric-specific.")
    elif r_ps_dc < 0.3:
        print("  >>> BRIDGE FAILS AT SCALE. The correlation does not survive 7B.")
    else:
        print("  >>> AMBIGUOUS. r in [0.3, 0.4] or p >= 0.05. More data needed.")
    print()

    print("Comparison correlations:")
    print("  PS vs RankMe:      r = {:+.4f},  p = {:.6f}  (cf. G08: r=-0.30)".format(r_ps_rm, p_ps_rm))
    print("  PS vs alpha-ReQ:   r = {:+.4f},  p = {:.6f}".format(r_ps_ar, p_ps_ar))
    print()

    print("Metric inter-correlations:")
    print("  DC vs RankMe:      r = {:+.4f},  p = {:.6f}".format(r_dc_rm, p_dc_rm))
    print("  DC vs alpha-ReQ:   r = {:+.4f},  p = {:.6f}".format(r_dc_ar, p_dc_ar))
    print("  RankMe vs alpha:   r = {:+.4f},  p = {:.6f}".format(r_rm_ar, p_rm_ar))
    print()

    # Category breakdown
    print("Per-category PS vs DC:")
    for cat in ["factual", "summarization", "judgment", "creative"]:
        cat_tasks = [t for t in task_summaries if t["category"] == cat]
        cat_ps = np.array([t["phrasing_sensitivity"] for t in cat_tasks])
        cat_dc = np.array([t["mean_directional_coherence"] for t in cat_tasks])
        if len(cat_ps) >= 3:
            r_cat, p_cat = stats.pearsonr(cat_ps, cat_dc)
            print("  {:15s}: r = {:+.4f},  p = {:.4f}  (n={})".format(cat, r_cat, p_cat, len(cat_ps)))
        else:
            print("  {:15s}: insufficient data (n={})".format(cat, len(cat_ps)))
    print()

    # -----------------------------------------------------------------------
    # Save outputs
    # -----------------------------------------------------------------------
    # Per-phrasing JSONL
    jsonl_path = os.path.join(output_dir, "g01v2_per_phrasing.jsonl")
    with open(jsonl_path, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print("Per-phrasing results: {}".format(jsonl_path))

    # Per-task JSONL
    task_jsonl_path = os.path.join(output_dir, "g01v2_per_task.jsonl")
    with open(task_jsonl_path, "w") as f:
        for t in task_summaries:
            f.write(json.dumps(t) + "\n")
    print("Per-task results: {}".format(task_jsonl_path))

    # Summary JSON
    summary = {
        "experiment": "G01v2",
        "description": "Bridge at 7B using Coherence",
        "model": model_name,
        "n_tasks": len(TASKS),
        "n_phrasings_per_task": 4,
        "n_inferences": len(results),
        "bridge_test": {
            "metric": "PS vs directional_coherence",
            "r": round(r_ps_dc, 6),
            "p": round(p_ps_dc, 6),
            "interpretation": (
                "BRIDGE_HOLDS" if (r_ps_dc > 0.4 and p_ps_dc < 0.05)
                else "BRIDGE_FAILS" if r_ps_dc < 0.3
                else "AMBIGUOUS"
            ),
        },
        "comparisons": {
            "ps_vs_rankme": {"r": round(r_ps_rm, 6), "p": round(p_ps_rm, 6)},
            "ps_vs_alpha_req": {"r": round(r_ps_ar, 6), "p": round(p_ps_ar, 6)},
            "dc_vs_rankme": {"r": round(r_dc_rm, 6), "p": round(p_dc_rm, 6)},
            "dc_vs_alpha_req": {"r": round(r_dc_ar, 6), "p": round(p_dc_ar, 6)},
            "rankme_vs_alpha_req": {"r": round(r_rm_ar, 6), "p": round(p_rm_ar, 6)},
        },
        "reference": {
            "G01_1.5B": "r=+0.52, p=0.018",
            "G01_3B": "r=+0.50, p=0.026",
            "G08_7B_rankme": "r=-0.30 (negative, wrong metric)",
        },
    }
    summary_path = os.path.join(output_dir, "g01v2_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print("Summary: {}".format(summary_path))

    print()
    print("=" * 70)
    print("G01v2 complete.")
    print("=" * 70)

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="G01v2: Bridge at 7B using Coherence")
    parser.add_argument(
        "--model_name",
        type=str,
        default="mistralai/Mistral-7B-v0.1",
        help="HuggingFace model name (default: mistralai/Mistral-7B-v0.1)",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./g01v2_results",
        help="Output directory (default: ./g01v2_results)",
    )
    args = parser.parse_args()

    run_experiment(args.model_name, args.output_dir)
