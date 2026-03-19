#!/usr/bin/env python3
"""
Experiment 04: Confabulation Eigenspectral Profiles

Tests whether confabulated content deviates from Karkada et al.'s predicted
Fourier eigenspectral profile, while grounded content matches it.

Hypothesis: Confabulated responses show higher spectral profile deviation
(residual from predicted decay) than grounded responses on matched topics.

Method: Matched pairs (grounded vs fabricated prompts on the same topic).
Extract eigenspectral profiles from last-layer hidden states. Compare
spectral profile deviation between conditions using Cohen's d, Welch's
t-test, and Mann-Whitney U.

Karkada's prediction: amplitudes a_n = sqrt(2sigma / (1 + sigma^2 * k_n^2))
decay monotonically with wavenumber. Grounded content should match this;
confabulation should deviate.

Usage:
    python run.py                              # Run all tasks on default model
    python run.py --model Qwen/Qwen3.5-4B     # Specific model
    python run.py --dry-run                    # Show what would run
    python run.py --max-tasks 3               # Quick test with 3 pairs
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
TASKS_FILE = Path(__file__).parent / "tasks.json"

# Models — local (M4 Pro 24GB) and GPU targets
# All ungated, Apache 2.0 (no HuggingFace approval needed)
MODELS_LOCAL = [
    {
        "id": "Qwen/Qwen3.5-4B",
        "name": "Qwen 3.5 4B",
        "params": 4e9,
    },
]

MODELS_GPU = [
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
]

MODELS = MODELS_LOCAL


# ---------------------------------------------------------------------------
# Geometric metrics (reused from Exp 03)
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
    best_sigma2 = None
    for log_sigma2 in np.linspace(-4, 4, 200):
        sigma2 = 10 ** log_sigma2
        predicted = 1.0 / np.sqrt(1 + sigma2 * k ** 2)
        predicted = predicted / predicted[0]
        residual = np.mean((observed - predicted) ** 2)
        if residual < best_residual:
            best_residual = residual
            best_sigma2 = sigma2

    return float(np.sqrt(best_residual))  # RMSE


def compute_spectral_profile_detail(singular_values: np.ndarray) -> dict:
    """
    Extended spectral analysis: returns the fitted sigma_sq, best-fit
    predicted profile, and per-wavenumber residuals for richer analysis.
    """
    sv = singular_values[singular_values > 1e-10]
    if len(sv) < 5:
        return {
            "fitted_sigma_sq": float("nan"),
            "rmse": float("nan"),
            "max_residual": float("nan"),
            "residual_profile": [],
        }

    n = len(sv)
    k = np.arange(1, n + 1, dtype=float)
    observed = sv / sv[0]

    best_residual = float("inf")
    best_sigma2 = None
    best_predicted = None
    for log_sigma2 in np.linspace(-4, 4, 200):
        sigma2 = 10 ** log_sigma2
        predicted = 1.0 / np.sqrt(1 + sigma2 * k ** 2)
        predicted = predicted / predicted[0]
        residual = np.mean((observed - predicted) ** 2)
        if residual < best_residual:
            best_residual = residual
            best_sigma2 = sigma2
            best_predicted = predicted

    per_wavenumber = (observed - best_predicted).tolist()

    return {
        "fitted_sigma_sq": float(best_sigma2),
        "rmse": float(np.sqrt(best_residual)),
        "max_residual": float(np.max(np.abs(observed - best_predicted))),
        "residual_profile": per_wavenumber[:20],  # First 20 for storage
    }


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
            "spectral_detail": compute_spectral_profile_detail(np.array([])),
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
        "spectral_detail": compute_spectral_profile_detail(S),
        "num_tokens": hidden_states.shape[0],
        "top_10_singular_values": S[:10].tolist(),
    }


# ---------------------------------------------------------------------------
# Model loading and inference (reused from Exp 03)
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
# Main experiment loop
# ---------------------------------------------------------------------------

def load_tasks(max_tasks=None):
    with open(TASKS_FILE) as f:
        tasks = json.load(f)
    if max_tasks:
        tasks = tasks[:max_tasks]
    return tasks


def run_experiment(model_id: str, dry_run: bool = False, max_tasks: int = None):
    tasks = load_tasks(max_tasks)

    model_name = model_id.split("/")[-1]

    if dry_run:
        print(f"DRY RUN: {model_name}")
        print(f"  Matched pairs: {len(tasks)}")
        print(f"  Total inferences: {len(tasks) * 2} (1 grounded + 1 confabulated per pair)")
        for t in tasks:
            print(f"    {t['id']} ({t['domain']}): {t['topic']}")
        return

    # Create output dirs
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    model, tokenizer, device = load_model(model_id)

    results = []
    pair_metrics = []

    total_inferences = len(tasks) * 2
    inference_count = 0

    for task in tasks:
        task_id = task["id"]
        domain = task["domain"]
        topic = task["topic"]

        pair_result = {"task_id": task_id, "domain": domain, "topic": topic}

        for condition in ["grounded", "confabulated"]:
            inference_count += 1
            prompt = task[condition]

            print(
                f"[{inference_count}/{total_inferences}] {task_id} {condition}...",
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
            metrics["domain"] = domain
            metrics["condition"] = condition
            metrics["elapsed_seconds"] = elapsed

            pair_result[condition] = metrics

            print(
                f"SPD={metrics['spectral_profile_deviation']:.4f} "
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
                "domain": domain,
                "topic": topic,
                "condition": condition,
                "prompt": prompt,
                "response": response,
                "metrics": metrics,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            results.append(result)

        # Compute pair-level difference
        g = pair_result["grounded"]
        c = pair_result["confabulated"]
        pair_summary = {
            "task_id": task_id,
            "domain": domain,
            "topic": topic,
            "grounded_spd": g["spectral_profile_deviation"],
            "confabulated_spd": c["spectral_profile_deviation"],
            "spd_difference": c["spectral_profile_deviation"] - g["spectral_profile_deviation"],
            "grounded_rankme": g["rankme"],
            "confabulated_rankme": c["rankme"],
            "grounded_alpha_req": g["alpha_req"],
            "confabulated_alpha_req": c["alpha_req"],
            "grounded_dc": g["directional_coherence"],
            "confabulated_dc": c["directional_coherence"],
            "grounded_tokens": g["num_tokens"],
            "confabulated_tokens": c["num_tokens"],
        }
        pair_metrics.append(pair_summary)

        print(
            f"  -> {task_id}: SPD diff = {pair_summary['spd_difference']:+.4f} "
            f"(grounded={pair_summary['grounded_spd']:.4f}, "
            f"confab={pair_summary['confabulated_spd']:.4f})"
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
                "pairs": pair_metrics,
            },
            f,
            indent=2,
        )
    print(f"Metrics: {metrics_path}")

    # Print statistical summary
    print_statistical_summary(pair_metrics)


def print_statistical_summary(pair_metrics: list):
    """
    Print between-condition comparisons: Cohen's d, Welch's t-test,
    Mann-Whitney U for spectral profile deviation and secondary metrics.
    """
    from scipy import stats

    print("\n" + "=" * 70)
    print("EXPERIMENT 04: Confabulation Eigenspectral Profiles")
    print("=" * 70)

    # Extract condition-level values
    grounded_spd = [p["grounded_spd"] for p in pair_metrics if not np.isnan(p["grounded_spd"])]
    confab_spd = [p["confabulated_spd"] for p in pair_metrics if not np.isnan(p["confabulated_spd"])]

    # Primary metric: Spectral Profile Deviation
    print("\n--- PRIMARY: Spectral Profile Deviation (SPD) ---")
    print(f"  Grounded     mean={np.mean(grounded_spd):.4f}  sd={np.std(grounded_spd):.4f}  n={len(grounded_spd)}")
    print(f"  Confabulated mean={np.mean(confab_spd):.4f}  sd={np.std(confab_spd):.4f}  n={len(confab_spd)}")

    if len(grounded_spd) >= 3 and len(confab_spd) >= 3:
        # Cohen's d (pooled)
        n1, n2 = len(grounded_spd), len(confab_spd)
        s1, s2 = np.std(grounded_spd, ddof=1), np.std(confab_spd, ddof=1)
        pooled_sd = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
        if pooled_sd > 1e-10:
            cohens_d = (np.mean(confab_spd) - np.mean(grounded_spd)) / pooled_sd
        else:
            cohens_d = 0.0
        print(f"  Cohen's d = {cohens_d:.3f}", end="")
        if abs(cohens_d) >= 0.8:
            print(" (large)")
        elif abs(cohens_d) >= 0.5:
            print(" (medium)")
        elif abs(cohens_d) >= 0.2:
            print(" (small)")
        else:
            print(" (negligible)")

        # Welch's t-test (unequal variance)
        t_stat, t_pval = stats.ttest_ind(confab_spd, grounded_spd, equal_var=False)
        sig = "***" if t_pval < 0.001 else "**" if t_pval < 0.01 else "*" if t_pval < 0.05 else "ns"
        print(f"  Welch's t  = {t_stat:.3f}  p={t_pval:.4f}  {sig}")

        # Mann-Whitney U (non-parametric)
        u_stat, u_pval = stats.mannwhitneyu(
            confab_spd, grounded_spd, alternative="greater"
        )
        sig = "***" if u_pval < 0.001 else "**" if u_pval < 0.01 else "*" if u_pval < 0.05 else "ns"
        print(f"  Mann-Whitney U = {u_stat:.0f}  p={u_pval:.4f}  {sig}  (one-sided: confab > grounded)")

        # Paired comparison (within matched pairs)
        valid_pairs = [
            p for p in pair_metrics
            if not np.isnan(p["grounded_spd"]) and not np.isnan(p["confabulated_spd"])
        ]
        if len(valid_pairs) >= 3:
            diffs = [p["confabulated_spd"] - p["grounded_spd"] for p in valid_pairs]
            t_paired, p_paired = stats.ttest_1samp(diffs, 0)
            w_stat, w_pval = stats.wilcoxon(diffs, alternative="greater")
            print(f"\n  Paired t-test (within matched pairs, n={len(valid_pairs)}):")
            print(f"    mean diff = {np.mean(diffs):+.4f}  sd={np.std(diffs):.4f}")
            sig = "***" if p_paired < 0.001 else "**" if p_paired < 0.01 else "*" if p_paired < 0.05 else "ns"
            print(f"    t={t_paired:.3f}  p={p_paired:.4f}  {sig}")
            sig = "***" if w_pval < 0.001 else "**" if w_pval < 0.01 else "*" if w_pval < 0.05 else "ns"
            print(f"    Wilcoxon W={w_stat:.0f}  p={w_pval:.4f}  {sig}  (one-sided)")

            # Count direction
            n_confab_higher = sum(1 for d in diffs if d > 0)
            n_grounded_higher = sum(1 for d in diffs if d < 0)
            n_equal = sum(1 for d in diffs if d == 0)
            print(f"    Direction: confab higher {n_confab_higher}/{len(diffs)}, "
                  f"grounded higher {n_grounded_higher}/{len(diffs)}, equal {n_equal}")
    else:
        print("  (insufficient data for statistical tests)")

    # Secondary metrics comparison
    print("\n--- SECONDARY METRICS ---")
    for metric_name, g_key, c_key in [
        ("RankMe", "grounded_rankme", "confabulated_rankme"),
        ("alpha-ReQ", "grounded_alpha_req", "confabulated_alpha_req"),
        ("Dir. Coherence", "grounded_dc", "confabulated_dc"),
    ]:
        g_vals = [p[g_key] for p in pair_metrics if not np.isnan(p[g_key])]
        c_vals = [p[c_key] for p in pair_metrics if not np.isnan(p[c_key])]
        if len(g_vals) < 3 or len(c_vals) < 3:
            print(f"  {metric_name:20s}: insufficient data")
            continue
        t_stat, t_pval = stats.ttest_ind(c_vals, g_vals, equal_var=False)
        sig = "***" if t_pval < 0.001 else "**" if t_pval < 0.01 else "*" if t_pval < 0.05 else "ns"
        print(
            f"  {metric_name:20s}: grounded={np.mean(g_vals):.3f}  "
            f"confab={np.mean(c_vals):.3f}  "
            f"t={t_stat:.3f}  p={t_pval:.4f}  {sig}"
        )

    # Per-domain breakdown
    print("\n--- PER-DOMAIN SPD ---")
    domains = sorted(set(p["domain"] for p in pair_metrics))
    header = f"  {'Domain':15s} {'Grounded':>10s} {'Confab':>10s} {'Diff':>10s} {'n':>5s}"
    print(header)
    for domain in domains:
        dp = [p for p in pair_metrics if p["domain"] == domain]
        g_mean = np.nanmean([p["grounded_spd"] for p in dp])
        c_mean = np.nanmean([p["confabulated_spd"] for p in dp])
        print(
            f"  {domain:15s} {g_mean:10.4f} {c_mean:10.4f} {c_mean - g_mean:+10.4f} {len(dp):5d}"
        )

    # Overall verdict
    print("\n--- VERDICT ---")
    valid_pairs = [
        p for p in pair_metrics
        if not np.isnan(p["grounded_spd"]) and not np.isnan(p["confabulated_spd"])
    ]
    if valid_pairs:
        diffs = [p["confabulated_spd"] - p["grounded_spd"] for p in valid_pairs]
        n_confab_higher = sum(1 for d in diffs if d > 0)
        mean_diff = np.mean(diffs)
        if mean_diff > 0 and n_confab_higher > len(diffs) / 2:
            print(f"  CONSISTENT with hypothesis: confabulated content shows higher")
            print(f"  spectral deviation ({n_confab_higher}/{len(diffs)} pairs, mean diff={mean_diff:+.4f})")
        elif mean_diff < 0:
            print(f"  INCONSISTENT: grounded content shows HIGHER deviation")
            print(f"  (mean diff={mean_diff:+.4f})")
        else:
            print(f"  INCONCLUSIVE: no clear directional pattern")
            print(f"  (mean diff={mean_diff:+.4f}, {n_confab_higher}/{len(diffs)} confab higher)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exp 04: Confabulation Eigenspectral Profiles"
    )
    parser.add_argument(
        "--model", default=MODELS[0]["id"], help="HuggingFace model ID"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-tasks", type=int, help="Limit number of matched pairs")
    args = parser.parse_args()

    run_experiment(args.model, args.dry_run, args.max_tasks)
