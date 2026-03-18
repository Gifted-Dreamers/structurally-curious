#!/usr/bin/env python3
"""
Experiment 05: Confidence Language Density Analysis

Scores model responses for certainty/hedging markers using hope_valueism's
methodology, then cross-references with phrasing sensitivity from Exp 01.

Prediction: certainty and phrasing sensitivity should be UNCORRELATED
(confidence decorrelation — the model is equally certain whether it's
retrieving or constructing).

Behavioral only — no hidden state extraction needed.

Usage:
    python run.py                              # Run all tasks on default model
    python run.py --model Qwen/Qwen3.5-4B     # Specific model
    python run.py --category factual           # Single category
    python run.py --dry-run                    # Show what would run
    python run.py --max-tasks 2                # Quick test with 2 tasks
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# Paths
RESULTS_DIR = Path(__file__).parent / "results" / "raw"
METRICS_DIR = Path(__file__).parent / "results" / "metrics"
TASKS_FILE = Path(__file__).parent.parent / "01-phrasing-sensitivity" / "tasks.json"

# Models — local (M4 Pro 24GB) and GPU targets
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
]

MODELS = MODELS_LOCAL


# ---------------------------------------------------------------------------
# Certainty and hedging markers
# ---------------------------------------------------------------------------

# High-confidence markers (case-insensitive, matched as whole phrases)
CERTAINTY_MARKERS = [
    "certainly",
    "definitely",
    "clearly",
    "obviously",
    "undoubtedly",
    "without doubt",
    "it is clear that",
    "there is no question",
    "the fact is",
    "absolutely",
]

# Low-confidence / hedging markers
HEDGING_MARKERS = [
    "perhaps",
    "maybe",
    "might",
    "could be",
    "it's possible",
    "i think",
    "arguably",
    "it seems",
    "one could argue",
    "to some extent",
    "in some ways",
    "not entirely clear",
]

# Pre-compile patterns for efficiency
_CERTAINTY_PATTERNS = [
    re.compile(r"\b" + re.escape(m) + r"\b", re.IGNORECASE)
    for m in CERTAINTY_MARKERS
]
_HEDGING_PATTERNS = [
    re.compile(r"\b" + re.escape(m) + r"\b", re.IGNORECASE)
    for m in HEDGING_MARKERS
]


def count_markers(text: str) -> dict:
    """
    Count certainty and hedging markers in a text.

    Returns dict with high_count, hedge_count, and matched markers.
    """
    high_count = 0
    hedge_count = 0
    high_matched = []
    hedge_matched = []

    for pattern, marker in zip(_CERTAINTY_PATTERNS, CERTAINTY_MARKERS):
        matches = pattern.findall(text)
        if matches:
            high_count += len(matches)
            high_matched.extend([marker] * len(matches))

    for pattern, marker in zip(_HEDGING_PATTERNS, HEDGING_MARKERS):
        matches = pattern.findall(text)
        if matches:
            hedge_count += len(matches)
            hedge_matched.extend([marker] * len(matches))

    return {
        "high_count": high_count,
        "hedge_count": hedge_count,
        "high_matched": high_matched,
        "hedge_matched": hedge_matched,
    }


def compute_certainty_score(text: str) -> dict:
    """
    Compute certainty density score for a response.

    certainty_score = (high_count - hedge_count) / total_words

    Positive = net certain, negative = net hedging, near zero = balanced.
    """
    markers = count_markers(text)
    words = text.split()
    total_words = len(words)

    if total_words == 0:
        return {
            "certainty_score": 0.0,
            "high_count": 0,
            "hedge_count": 0,
            "total_words": 0,
            "high_density": 0.0,
            "hedge_density": 0.0,
            "high_matched": [],
            "hedge_matched": [],
        }

    high_count = markers["high_count"]
    hedge_count = markers["hedge_count"]
    certainty_score = (high_count - hedge_count) / total_words

    return {
        "certainty_score": certainty_score,
        "high_count": high_count,
        "hedge_count": hedge_count,
        "total_words": total_words,
        "high_density": high_count / total_words,
        "hedge_density": hedge_count / total_words,
        "high_matched": markers["high_matched"],
        "hedge_matched": markers["hedge_matched"],
    }


# ---------------------------------------------------------------------------
# Phrasing sensitivity (same as Exp 01/03 for comparability)
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
# Model loading and inference
# ---------------------------------------------------------------------------

def load_model(model_id: str):
    """Load model and tokenizer. Uses MPS on Apple Silicon, CUDA if available."""
    import torch
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

    # Inference mode — no gradient tracking needed
    for param in model.parameters():
        param.requires_grad = False

    print(f"Loaded on {device} ({dtype})")
    return model, tokenizer, device


def generate_response(
    model, tokenizer, prompt: str, device: str, max_new_tokens: int = 256
) -> str:
    """
    Generate a response (text only, no hidden state extraction).
    Greedy decoding for reproducibility.
    """
    import torch

    messages = [{"role": "user", "content": prompt}]
    input_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    prompt_length = inputs["input_ids"].shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=1.0,
        )

    generated_ids = outputs[0, prompt_length:]
    response = tokenizer.decode(generated_ids, skip_special_tokens=True)
    return response


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
        print(f"  Certainty markers: {len(CERTAINTY_MARKERS)}")
        print(f"  Hedging markers: {len(HEDGING_MARKERS)}")
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
        phrasing_scores = []

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
            response = generate_response(model, tokenizer, prompt, device)
            elapsed = time.time() - t0

            scores = compute_certainty_score(response)
            scores["task_id"] = task_id
            scores["category"] = category_name
            scores["phrasing_index"] = pi
            scores["elapsed_seconds"] = elapsed

            responses.append(response)
            phrasing_scores.append(scores)

            print(
                f"CS={scores['certainty_score']:+.4f} "
                f"hi={scores['high_count']} "
                f"hedge={scores['hedge_count']} "
                f"words={scores['total_words']} ({elapsed:.1f}s)"
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
                "scores": scores,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            results.append(result)

        # Compute task-level summary
        ps = compute_phrasing_sensitivity(responses)
        mean_cs = float(np.mean([s["certainty_score"] for s in phrasing_scores]))
        std_cs = float(np.std([s["certainty_score"] for s in phrasing_scores]))
        mean_high = float(np.mean([s["high_density"] for s in phrasing_scores]))
        mean_hedge = float(np.mean([s["hedge_density"] for s in phrasing_scores]))
        mean_words = float(np.mean([s["total_words"] for s in phrasing_scores]))

        avg = {
            "task_id": task_id,
            "category": category_name,
            "phrasing_sensitivity": ps,
            "mean_certainty_score": mean_cs,
            "std_certainty_score": std_cs,
            "mean_high_density": mean_high,
            "mean_hedge_density": mean_hedge,
            "mean_total_words": mean_words,
            "total_high_markers": sum(s["high_count"] for s in phrasing_scores),
            "total_hedge_markers": sum(s["hedge_count"] for s in phrasing_scores),
        }
        task_metrics.append(avg)
        print(
            f"  -> {task_id}: PS={ps:.3f} "
            f"CS={mean_cs:+.4f} "
            f"hi_d={mean_high:.4f} hedge_d={mean_hedge:.4f}"
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
                "certainty_markers": CERTAINTY_MARKERS,
                "hedging_markers": HEDGING_MARKERS,
                "tasks": task_metrics,
            },
            f,
            indent=2,
        )
    print(f"Metrics: {metrics_path}")

    # Print correlation summary
    print_correlation_summary(task_metrics)


def print_correlation_summary(task_metrics: list):
    """
    Print correlations between phrasing sensitivity and certainty density.
    Core prediction: these should be UNCORRELATED (confidence decorrelation).
    """
    from scipy import stats

    ps = [t["phrasing_sensitivity"] for t in task_metrics]
    cs = [t["mean_certainty_score"] for t in task_metrics]
    hi = [t["mean_high_density"] for t in task_metrics]
    hd = [t["mean_hedge_density"] for t in task_metrics]

    print("\n" + "=" * 70)
    print("CORRELATION: Phrasing Sensitivity vs Confidence Language Density")
    print("=" * 70)
    print("Prediction: UNCORRELATED (confidence decorrelation)")
    print("  If confirmed: model confidence is cosmetic, not epistemic.")
    print("  If refuted: confidence tracks actual uncertainty (good sign).")
    print()

    for name, values in [
        ("Certainty Score", cs),
        ("High-Conf Density", hi),
        ("Hedge Density", hd),
    ]:
        if len(values) < 3:
            print(f"  {name:20s}: insufficient data")
            continue

        # Pearson
        r_p, p_p = stats.pearsonr(ps, values)
        # Spearman (rank correlation, more robust to outliers)
        r_s, p_s = stats.spearmanr(ps, values)

        sig_p = (
            "***" if p_p < 0.001
            else "**" if p_p < 0.01
            else "*" if p_p < 0.05
            else "ns"
        )
        sig_s = (
            "***" if p_s < 0.001
            else "**" if p_s < 0.01
            else "*" if p_s < 0.05
            else "ns"
        )

        print(f"  {name:20s}:")
        print(f"    Pearson:  r={r_p:+.3f}  p={p_p:.4f}  {sig_p}")
        print(f"    Spearman: r={r_s:+.3f}  p={p_s:.4f}  {sig_s}")

    # Per-category means
    print("\nPer-category means:")
    categories = sorted(set(t["category"] for t in task_metrics))
    header = (
        f"  {'Category':15s} {'n':>3s} {'PS':>8s} {'CS':>8s} "
        f"{'Hi_d':>8s} {'Hedge_d':>8s} {'Words':>8s}"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))
    for cat in categories:
        cat_tasks = [t for t in task_metrics if t["category"] == cat]
        n = len(cat_tasks)
        row = (
            f"  {cat:15s} {n:3d} "
            f"{np.mean([t['phrasing_sensitivity'] for t in cat_tasks]):8.3f} "
            f"{np.mean([t['mean_certainty_score'] for t in cat_tasks]):+8.4f} "
            f"{np.mean([t['mean_high_density'] for t in cat_tasks]):8.4f} "
            f"{np.mean([t['mean_hedge_density'] for t in cat_tasks]):8.4f} "
            f"{np.mean([t['mean_total_words'] for t in cat_tasks]):8.1f}"
        )
        print(row)

    # Per-category correlation (if enough data)
    print("\nPer-category PS vs Certainty Score:")
    for cat in categories:
        cat_tasks = [t for t in task_metrics if t["category"] == cat]
        if len(cat_tasks) < 3:
            print(f"  {cat:15s}: insufficient data (n={len(cat_tasks)})")
            continue
        cat_ps = [t["phrasing_sensitivity"] for t in cat_tasks]
        cat_cs = [t["mean_certainty_score"] for t in cat_tasks]
        r, p_val = stats.pearsonr(cat_ps, cat_cs)
        sig = (
            "***" if p_val < 0.001
            else "**" if p_val < 0.01
            else "*" if p_val < 0.05
            else "ns"
        )
        print(f"  {cat:15s}: r={r:+.3f}  p={p_val:.4f}  {sig}  (n={len(cat_tasks)})")

    # Certainty score variation across phrasings (within-task)
    print("\nCertainty score stability across phrasings (std):")
    for cat in categories:
        cat_tasks = [t for t in task_metrics if t["category"] == cat]
        mean_std = np.mean([t["std_certainty_score"] for t in cat_tasks])
        print(f"  {cat:15s}: mean_std={mean_std:.4f}")

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exp 05: Confidence language density analysis"
    )
    parser.add_argument(
        "--model", default=MODELS[0]["id"], help="HuggingFace model ID"
    )
    parser.add_argument(
        "--category",
        choices=["factual", "summarization", "judgment", "creative"],
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-tasks", type=int, help="Limit number of tasks")
    args = parser.parse_args()

    run_experiment(args.model, args.category, args.dry_run, args.max_tasks)
