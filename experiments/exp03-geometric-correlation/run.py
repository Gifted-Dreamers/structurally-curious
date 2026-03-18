#!/usr/bin/env python3
"""
Experiment 03: Phrasing Sensitivity → Geometric State Correlation

Tests whether phrasing sensitivity (behavioral, from Exp 01) correlates with
geometric properties of last-layer representations (α-ReQ, RankMe, TwoNN).

Runs open-weight models locally via HuggingFace with activation hooks.
Extracts last-layer hidden states and computes geometric metrics per response.

Usage:
    python run.py                              # Run all tasks on default model
    python run.py --model meta-llama/Llama-3.2-1B-Instruct  # Specific model
    python run.py --category factual           # Single category
    python run.py --dry-run                    # Show what would run
    python run.py --max-tasks 2                # Quick test with 2 tasks
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from scipy import linalg

# Paths
RESULTS_DIR = Path(__file__).parent / "results" / "raw"
METRICS_DIR = Path(__file__).parent / "results" / "metrics"
TASKS_FILE = Path(__file__).parent.parent / "01-phrasing-sensitivity" / "tasks.json"

# Models — local (M4 Pro 24GB) and GPU targets
# All ungated, Apache 2.0 (no HuggingFace approval needed)
MODELS_LOCAL = [
    # Completed — results in results/raw/
    {
        "id": "Qwen/Qwen2.5-1.5B-Instruct",
        "name": "Qwen 2.5 1.5B",
        "params": 1.5e9,
    },
    {
        "id": "Qwen/Qwen2.5-3B-Instruct",
        "name": "Qwen 2.5 3B",
        "params": 3e9,
    },
    # Qwen 3.5 small — fits on M4 Pro
    {
        "id": "Qwen/Qwen3.5-4B",
        "name": "Qwen 3.5 4B",
        "params": 4e9,
    },
]

MODELS_GPU = [
    # Exp 03b targets — Azure V100 (16GB VRAM)
    {
        "id": "Qwen/Qwen3.5-9B",
        "name": "Qwen 3.5 9B",
        "params": 9e9,
    },
    {
        "id": "Qwen/Qwen3.5-35B-A3B",
        "name": "Qwen 3.5 35B MoE (3B active)",
        "params": 35e9,
        "active_params": 3e9,
    },
    # Stretch — needs A100 (80GB) or quantization
    # {
    #     "id": "Qwen/Qwen3.5-27B",
    #     "name": "Qwen 3.5 27B",
    #     "params": 27e9,
    # },
]

MODELS = MODELS_LOCAL  # Override with --gpu flag to use MODELS_GPU


# ---------------------------------------------------------------------------
# Geometric metrics
# ---------------------------------------------------------------------------

def compute_rankme(singular_values: np.ndarray) -> float:
    """
    RankMe: effective rank via entropy of normalized singular values.
    From Li et al. (2509.23024). Higher = more dimensions used.

    RankMe = exp(-sum(pi * log(pi))) where pi = sigma_i / sum(sigma_j)
    """
    sv = singular_values[singular_values > 1e-10]
    if len(sv) == 0:
        return 0.0
    p = sv / sv.sum()
    entropy = -np.sum(p * np.log(p + 1e-12))
    return float(np.exp(entropy))


def compute_alpha_req(singular_values: np.ndarray) -> float:
    """
    alpha-ReQ: eigenspectrum decay rate.
    From Li et al. (2509.23024). Higher = faster decay = more compressed.

    Fits log(sigma_i) = -alpha * log(i) + c via least squares.
    """
    sv = singular_values[singular_values > 1e-10]
    if len(sv) < 3:
        return 0.0
    log_ranks = np.log(np.arange(1, len(sv) + 1))
    log_sv = np.log(sv)
    # Least squares: log_sv = -alpha * log_ranks + c
    A = np.stack([log_ranks, np.ones_like(log_ranks)], axis=1)
    result = np.linalg.lstsq(A, log_sv, rcond=None)
    alpha = -result[0][0]  # Negate because we fit -alpha
    return float(alpha)


def compute_directional_coherence(hidden_states: np.ndarray) -> float:
    """
    Directional coherence: cosine similarity between consecutive token
    hidden states, averaged. Higher = representations moving in consistent
    direction. Lower = diffuse/searching.
    """
    if hidden_states.shape[0] < 2:
        return 0.0
    norms = np.linalg.norm(hidden_states, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-10)
    normalized = hidden_states / norms
    # Cosine similarity between consecutive tokens
    cosines = np.sum(normalized[:-1] * normalized[1:], axis=1)
    return float(np.mean(cosines))


def compute_spectral_profile_deviation(singular_values: np.ndarray) -> float:
    """
    Spectral profile deviation: residual between observed eigenspectrum and
    Karkada et al.'s predicted Fourier profile.

    Predicted: a_n proportional to (1 + sigma_sq * k_n^2)^(-1/2)

    We fit sigma_sq to minimize residual, then report the residual.
    Lower = better match to predicted structure = more grounded.
    """
    sv = singular_values[singular_values > 1e-10]
    if len(sv) < 5:
        return float("nan")

    n = len(sv)
    k = np.arange(1, n + 1, dtype=float)
    observed = sv / sv[0]  # Normalize to first component

    # Grid search for best sigma_sq (simple, robust)
    best_residual = float("inf")
    for log_sigma2 in np.linspace(-4, 4, 200):
        sigma2 = 10 ** log_sigma2
        predicted = 1.0 / np.sqrt(1 + sigma2 * k ** 2)
        predicted = predicted / predicted[0]
        residual = np.mean((observed - predicted) ** 2)
        if residual < best_residual:
            best_residual = residual

    return float(np.sqrt(best_residual))  # RMSE


def compute_all_metrics(hidden_states: np.ndarray) -> dict:
    """
    Compute all geometric metrics from last-layer hidden states.

    Args:
        hidden_states: shape (num_tokens, hidden_dim) -- last-layer output
                       for the generated tokens only (not prompt)

    Returns:
        dict with all metric values
    """
    if hidden_states.shape[0] < 2:
        return {
            "rankme": 0.0,
            "alpha_req": 0.0,
            "directional_coherence": 0.0,
            "spectral_profile_deviation": float("nan"),
            "num_tokens": hidden_states.shape[0],
        }

    # SVD of the hidden states matrix
    # Shape: (num_tokens, hidden_dim) -> singular values
    U, S, Vt = linalg.svd(hidden_states, full_matrices=False)

    return {
        "rankme": compute_rankme(S),
        "alpha_req": compute_alpha_req(S),
        "directional_coherence": compute_directional_coherence(hidden_states),
        "spectral_profile_deviation": compute_spectral_profile_deviation(S),
        "num_tokens": hidden_states.shape[0],
        "top_10_singular_values": S[:10].tolist(),
    }


# ---------------------------------------------------------------------------
# Model loading and inference
# ---------------------------------------------------------------------------

def load_model(model_id: str):
    """Load model and tokenizer. Uses MPS on Apple Silicon, CUDA if available."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"Loading {model_id}...")

    if torch.backends.mps.is_available():
        device = "mps"
        dtype = torch.float16
    elif torch.cuda.is_available():
        device = "cuda"
        dtype = torch.float16
    else:
        device = "cpu"
        dtype = torch.float32

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=dtype,
        device_map=device,
    )

    # Put model in inference mode — no gradient tracking needed
    for param in model.parameters():
        param.requires_grad = False

    print(f"Loaded on {device} ({dtype})")
    return model, tokenizer, device


def generate_with_hidden_states(
    model, tokenizer, prompt: str, device: str, max_new_tokens: int = 256
) -> tuple:
    """
    Generate a response and capture last-layer hidden states for generated tokens.

    Returns:
        (response_text, hidden_states) where hidden_states shape is
        (num_generated_tokens, hidden_dim)
    """
    # Format as chat
    messages = [{"role": "user", "content": prompt}]
    input_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    prompt_length = inputs["input_ids"].shape[1]

    # Generate with output_hidden_states=True
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,  # Greedy for reproducibility
            temperature=1.0,
            output_hidden_states=True,
            return_dict_in_generate=True,
        )

    # Extract hidden states from the last layer for generated tokens only
    # outputs.hidden_states is a tuple of (step, layer, batch, seq, hidden)
    # Each step is a tuple of layer hidden states
    # We want the last layer from each generation step
    generated_hidden_states = []
    for step_hidden in outputs.hidden_states:
        # step_hidden is a tuple of (num_layers+1,) tensors
        # Last element = last layer, shape (batch, seq_len, hidden_dim)
        last_layer = step_hidden[-1]
        # Take the last token position (the newly generated token)
        token_hidden = last_layer[0, -1, :].cpu().float().numpy()
        generated_hidden_states.append(token_hidden)

    hidden_states = np.stack(generated_hidden_states)

    # Decode generated tokens only
    generated_ids = outputs.sequences[0, prompt_length:]
    response = tokenizer.decode(generated_ids, skip_special_tokens=True)

    return response, hidden_states


# ---------------------------------------------------------------------------
# Phrasing sensitivity (recomputed locally for correlation)
# ---------------------------------------------------------------------------

def compute_phrasing_sensitivity(responses: list) -> float:
    """
    Phrasing sensitivity: average pairwise dissimilarity between responses
    to different phrasings of the same question.

    Uses word-level Jaccard distance (same as Exp 01 for comparability).
    """
    if len(responses) < 2:
        return 0.0

    def word_set(s: str) -> set:
        return set(s.lower().strip().split())

    distances = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            s1 = word_set(responses[i])
            s2 = word_set(responses[j])
            if not s1 and not s2:
                distances.append(0.0)
            else:
                union = s1 | s2
                jaccard = len(s1 & s2) / len(union) if union else 0.0
                distances.append(1.0 - jaccard)

    return float(np.mean(distances))


# ---------------------------------------------------------------------------
# Main experiment loop
# ---------------------------------------------------------------------------

def load_tasks(category=None):
    with open(TASKS_FILE) as f:
        tasks = json.load(f)
    if category:
        tasks = [t for t in tasks if t["category"] == category]
    return tasks


def run_experiment(model_id: str, category: str = None, dry_run: bool = False,
                   max_tasks: int = None):
    tasks = load_tasks(category)
    if max_tasks:
        tasks = tasks[:max_tasks]

    model_name = model_id.split("/")[-1]

    if dry_run:
        print(f"DRY RUN: {model_name}")
        print(f"  Tasks: {len(tasks)}")
        print(f"  Phrasings per task: {len(tasks[0]['phrasings'])}")
        print(f"  Total inferences: {sum(len(t['phrasings']) for t in tasks)}")
        return

    # Create output dirs
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    model, tokenizer, device = load_model(model_id)

    results = []
    task_metrics = []

    total_inferences = sum(len(t["phrasings"]) for t in tasks)
    inference_count = 0

    for task in tasks:
        task_id = task["id"]
        category_name = task["category"]
        phrasings = task["phrasings"]

        responses = []
        phrasing_metrics = []

        for pi, phrasing in enumerate(phrasings):
            inference_count += 1
            prompt = phrasing
            if "context" in task:
                prompt = task["context"] + "\n\n" + phrasing

            print(
                f"[{inference_count}/{total_inferences}] {task_id} phrasing {pi}...",
                end=" ",
                flush=True,
            )

            t0 = time.time()
            response, hidden_states = generate_with_hidden_states(
                model, tokenizer, prompt, device
            )
            elapsed = time.time() - t0

            metrics = compute_all_metrics(hidden_states)
            metrics["task_id"] = task_id
            metrics["category"] = category_name
            metrics["phrasing_index"] = pi
            metrics["elapsed_seconds"] = elapsed

            responses.append(response)
            phrasing_metrics.append(metrics)

            print(
                f"RankMe={metrics['rankme']:.1f} "
                f"a-ReQ={metrics['alpha_req']:.3f} "
                f"DC={metrics['directional_coherence']:.3f} "
                f"tokens={metrics['num_tokens']} ({elapsed:.1f}s)"
            )

            # Save raw result
            result = {
                "model": model_id,
                "model_name": model_name,
                "task_id": task_id,
                "category": category_name,
                "phrasing_index": pi,
                "prompt": prompt,
                "response": response,
                "metrics": metrics,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            results.append(result)

        # Compute task-level summary
        ps = compute_phrasing_sensitivity(responses)
        avg_metrics = {
            "task_id": task_id,
            "category": category_name,
            "phrasing_sensitivity": ps,
            "mean_rankme": float(np.mean([m["rankme"] for m in phrasing_metrics])),
            "std_rankme": float(np.std([m["rankme"] for m in phrasing_metrics])),
            "mean_alpha_req": float(
                np.mean([m["alpha_req"] for m in phrasing_metrics])
            ),
            "std_alpha_req": float(
                np.std([m["alpha_req"] for m in phrasing_metrics])
            ),
            "mean_directional_coherence": float(
                np.mean(
                    [m["directional_coherence"] for m in phrasing_metrics]
                )
            ),
            "mean_spectral_deviation": float(
                np.nanmean(
                    [m["spectral_profile_deviation"] for m in phrasing_metrics]
                )
            ),
            "mean_tokens": float(
                np.mean([m["num_tokens"] for m in phrasing_metrics])
            ),
        }
        task_metrics.append(avg_metrics)
        print(
            f"  -> {task_id}: PS={ps:.3f} "
            f"RankMe={avg_metrics['mean_rankme']:.1f} "
            f"a-ReQ={avg_metrics['mean_alpha_req']:.3f}"
        )

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = RESULTS_DIR / f"{model_name}_{timestamp}.json"
    with open(raw_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nRaw results: {raw_path}")

    metrics_path = METRICS_DIR / f"{model_name}_{timestamp}.json"
    with open(metrics_path, "w") as f:
        json.dump(
            {
                "model": model_id,
                "model_name": model_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "tasks": task_metrics,
            },
            f,
            indent=2,
        )
    print(f"Metrics: {metrics_path}")

    # Print correlation summary
    print_correlation_summary(task_metrics)


def print_correlation_summary(task_metrics: list):
    """Print Pearson correlations between phrasing sensitivity and geometric metrics."""
    from scipy import stats

    ps = [t["phrasing_sensitivity"] for t in task_metrics]
    rankme = [t["mean_rankme"] for t in task_metrics]
    alpha = [t["mean_alpha_req"] for t in task_metrics]
    dc = [t["mean_directional_coherence"] for t in task_metrics]
    spd = [t["mean_spectral_deviation"] for t in task_metrics]

    print("\n" + "=" * 60)
    print("CORRELATION: Phrasing Sensitivity vs Geometric Metrics")
    print("=" * 60)

    for name, values in [
        ("RankMe", rankme),
        ("a-ReQ", alpha),
        ("Dir. Coherence", dc),
        ("Spectral Dev.", spd),
    ]:
        # Filter NaN
        valid = [(p, v) for p, v in zip(ps, values) if not np.isnan(v)]
        if len(valid) < 3:
            print(f"  {name:20s}: insufficient data")
            continue
        vp, vv = zip(*valid)
        r, p_val = stats.pearsonr(vp, vv)
        sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
        print(f"  {name:20s}: r={r:+.3f}  p={p_val:.4f}  {sig}")

    # By category
    print("\nPer-category means:")
    categories = sorted(set(t["category"] for t in task_metrics))
    header = f"  {'Category':15s} {'PS':>8s} {'RankMe':>8s} {'a-ReQ':>8s} {'DC':>8s} {'SPD':>8s}"
    print(header)
    for cat in categories:
        cat_tasks = [t for t in task_metrics if t["category"] == cat]
        row = (
            f"  {cat:15s} "
            f"{np.mean([t['phrasing_sensitivity'] for t in cat_tasks]):8.3f} "
            f"{np.mean([t['mean_rankme'] for t in cat_tasks]):8.1f} "
            f"{np.mean([t['mean_alpha_req'] for t in cat_tasks]):8.3f} "
            f"{np.mean([t['mean_directional_coherence'] for t in cat_tasks]):8.3f} "
            f"{np.nanmean([t['mean_spectral_deviation'] for t in cat_tasks]):8.3f}"
        )
        print(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exp 03: Geometric correlation")
    parser.add_argument(
        "--model", default=None, help="HuggingFace model ID (overrides --gpu)"
    )
    parser.add_argument(
        "--category",
        choices=["factual", "summarization", "judgment", "creative"],
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-tasks", type=int, help="Limit number of tasks")
    parser.add_argument(
        "--gpu", action="store_true",
        help="Use GPU model list (Qwen 3.5 9B, 35B-A3B MoE)"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Run all models in the selected list sequentially"
    )
    args = parser.parse_args()

    if args.model:
        run_experiment(args.model, args.category, args.dry_run, args.max_tasks)
    elif args.all:
        model_list = MODELS_GPU if args.gpu else MODELS_LOCAL
        for m in model_list:
            print(f"\n{'='*60}")
            print(f"Running: {m['name']}")
            print(f"{'='*60}\n")
            run_experiment(m["id"], args.category, args.dry_run, args.max_tasks)
    else:
        model_list = MODELS_GPU if args.gpu else MODELS_LOCAL
        run_experiment(
            model_list[0]["id"], args.category, args.dry_run, args.max_tasks
        )
