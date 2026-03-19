#!/usr/bin/env python3
"""
Experiment 02a: Premature Compression Detection

Tests whether models produce different outputs when given partial vs full context,
and whether the difference is detectable via phrasing sensitivity and output metrics.

This directly tests Open Problem #20: a model reads partial input, produces confident
output grounded in the subset — geometrically robust but incomplete.

Method:
    For each task:
    1. Give model PARTIAL documents + question → get response A
    2. Give model ALL documents + question → get response B
    3. Measure: output divergence, coverage metrics, confidence indicators

    If premature compression is real:
    - Response A will be confident and coherent (not hallucination)
    - Response B will include themes/connections absent from A
    - The GAP between A and B measures what was missed
    - Phrasing sensitivity on partial context should NOT be higher
      (because the model IS grounded — just in a subset)

Usage:
    python run.py                              # All models, all tasks
    python run.py --model us.meta.llama3-1-8b-instruct-v1:0
    python run.py --dry-run
    python run.py --max-tasks 2                # Quick test
"""

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

RESULTS_DIR = Path(__file__).parent / "results" / "raw"
METRICS_DIR = Path(__file__).parent / "results" / "metrics"
TASKS_FILE = Path(__file__).parent / "tasks.json"

# Models — same as Exp 01 for comparability, minus the most expensive
MODELS = [
    {"id": "us.meta.llama3-2-1b-instruct-v1:0", "name": "Llama 3.2 1B"},
    {"id": "us.meta.llama3-2-3b-instruct-v1:0", "name": "Llama 3.2 3B"},
    {"id": "us.meta.llama3-1-8b-instruct-v1:0", "name": "Llama 3.1 8B"},
    {"id": "us.meta.llama3-3-70b-instruct-v1:0", "name": "Llama 3.3 70B"},
    {"id": "us.anthropic.claude-haiku-4-5-20251001-v1:0", "name": "Claude Haiku 4.5"},
    {"id": "us.anthropic.claude-sonnet-4-6", "name": "Claude Sonnet 4.6"},
]


def call_model(client, model_id, prompt, max_tokens=800):
    """Call Bedrock Converse API. Returns (output_text, latency_ms, input_tokens, output_tokens)."""
    messages = [{"role": "user", "content": [{"text": prompt}]}]

    t0 = time.time()
    try:
        # DeepSeek R1 returns reasoningContent, not text
        is_thinking = "deepseek" in model_id.lower()

        response = client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig={"maxTokens": max_tokens, "temperature": 0.0},
        )
        latency = int((time.time() - t0) * 1000)

        output = response["output"]["message"]["content"][0]
        if is_thinking and "reasoningContent" in output:
            text = output["reasoningContent"].get("reasoningText", "")
        else:
            text = output.get("text", "")

        usage = response.get("usage", {})
        return text, latency, usage.get("inputTokens", 0), usage.get("outputTokens", 0)

    except ClientError as e:
        return f"ERROR: {e}", int((time.time() - t0) * 1000), 0, 0


def build_prompt(question, documents):
    """Build prompt with documents as context."""
    doc_text = "\n\n".join(documents)
    return f"""Read the following documents carefully, then answer the question.

{doc_text}

Question: {question}

Provide a thorough answer that draws on all the documents provided."""


def word_set(text):
    """Tokenize to word set for Jaccard similarity."""
    return set(text.lower().strip().split())


def compute_divergence(response_a, response_b):
    """Compute metrics comparing partial vs full responses."""
    words_a = word_set(response_a)
    words_b = word_set(response_b)

    if not words_a and not words_b:
        return {"jaccard_distance": 0.0, "new_words_ratio": 0.0, "dropped_words_ratio": 0.0}

    union = words_a | words_b
    intersection = words_a & words_b
    jaccard = len(intersection) / len(union) if union else 0.0

    # Words in full response not in partial (new themes from additional docs)
    new_words = words_b - words_a
    # Words in partial not in full (things the model dropped/revised)
    dropped_words = words_a - words_b

    return {
        "jaccard_distance": 1.0 - jaccard,
        "jaccard_similarity": jaccard,
        "new_words_count": len(new_words),
        "new_words_ratio": len(new_words) / len(words_b) if words_b else 0.0,
        "dropped_words_count": len(dropped_words),
        "dropped_words_ratio": len(dropped_words) / len(words_a) if words_a else 0.0,
        "partial_word_count": len(words_a),
        "full_word_count": len(words_b),
        "length_ratio": len(response_b) / len(response_a) if response_a else 0.0,
    }


def compute_confidence_markers(text):
    """Count hedging vs confidence language."""
    text_lower = text.lower()

    hedging = ["might", "perhaps", "possibly", "could be", "it seems",
               "arguably", "may", "uncertain", "unclear", "debatable",
               "it's possible", "one could argue", "to some extent"]
    confidence = ["clearly", "obviously", "certainly", "undoubtedly",
                  "the key", "the central", "the main", "fundamentally",
                  "it is clear", "without question", "definitively",
                  "the answer is", "in conclusion"]

    hedge_count = sum(1 for h in hedging if h in text_lower)
    confidence_count = sum(1 for c in confidence if c in text_lower)
    word_count = len(text.split())

    return {
        "hedge_count": hedge_count,
        "confidence_count": confidence_count,
        "hedge_rate": hedge_count / word_count if word_count else 0.0,
        "confidence_rate": confidence_count / word_count if word_count else 0.0,
        "net_confidence": (confidence_count - hedge_count) / word_count if word_count else 0.0,
    }


def run_experiment(model_id=None, dry_run=False, max_tasks=None):
    with open(TASKS_FILE) as f:
        tasks = json.load(f)
    if max_tasks:
        tasks = tasks[:max_tasks]

    models = MODELS
    if model_id:
        models = [m for m in MODELS if m["id"] == model_id]
        if not models:
            models = [{"id": model_id, "name": model_id.split(":")[-1]}]

    if dry_run:
        print(f"DRY RUN")
        print(f"  Models: {len(models)}")
        print(f"  Tasks: {len(tasks)}")
        print(f"  Inferences per task: 2 (partial + full)")
        print(f"  Total inferences: {len(models) * len(tasks) * 2}")
        for m in models:
            print(f"    - {m['name']}")
        return

    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    for model in models:
        mid = model["id"]
        mname = model["name"]
        print(f"\n{'='*60}")
        print(f"MODEL: {mname} ({mid})")
        print(f"{'='*60}")

        results = []
        task_metrics = []

        for ti, task in enumerate(tasks):
            task_id = task["id"]
            question = task["question"]
            all_docs = task["documents"]
            partial_idx = task["partial_indices"]
            full_idx = task["full_indices"]

            partial_docs = [all_docs[i] for i in partial_idx]
            full_docs = [all_docs[i] for i in full_idx]
            missing_docs = [all_docs[i] for i in full_idx if i not in partial_idx]

            print(f"\n[{ti+1}/{len(tasks)}] {task_id} ({task['category']})")
            print(f"  Partial: {len(partial_docs)} docs, Full: {len(full_docs)} docs, Missing: {len(missing_docs)} docs")

            # --- Partial context ---
            prompt_partial = build_prompt(question, partial_docs)
            print(f"  Partial...", end=" ", flush=True)
            resp_partial, lat_p, in_p, out_p = call_model(client, mid, prompt_partial)
            print(f"{out_p} tokens ({lat_p}ms)")

            # --- Full context ---
            prompt_full = build_prompt(question, full_docs)
            print(f"  Full...", end=" ", flush=True)
            resp_full, lat_f, in_f, out_f = call_model(client, mid, prompt_full)
            print(f"{out_f} tokens ({lat_f}ms)")

            # --- Compute metrics ---
            divergence = compute_divergence(resp_partial, resp_full)
            conf_partial = compute_confidence_markers(resp_partial)
            conf_full = compute_confidence_markers(resp_full)

            print(f"  Divergence: jaccard_dist={divergence['jaccard_distance']:.3f} "
                  f"new_words={divergence['new_words_ratio']:.3f} "
                  f"length_ratio={divergence['length_ratio']:.2f}")
            print(f"  Confidence: partial={conf_partial['net_confidence']:.4f} "
                  f"full={conf_full['net_confidence']:.4f}")

            result = {
                "model": mid,
                "model_name": mname,
                "task_id": task_id,
                "category": task["category"],
                "num_partial_docs": len(partial_docs),
                "num_full_docs": len(full_docs),
                "num_missing_docs": len(missing_docs),
                "partial_response": resp_partial,
                "full_response": resp_full,
                "partial_latency_ms": lat_p,
                "full_latency_ms": lat_f,
                "partial_tokens": {"input": in_p, "output": out_p},
                "full_tokens": {"input": in_f, "output": out_f},
                "divergence": divergence,
                "confidence_partial": conf_partial,
                "confidence_full": conf_full,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            results.append(result)

            task_metric = {
                "task_id": task_id,
                "category": task["category"],
                "jaccard_distance": divergence["jaccard_distance"],
                "new_words_ratio": divergence["new_words_ratio"],
                "dropped_words_ratio": divergence["dropped_words_ratio"],
                "length_ratio": divergence["length_ratio"],
                "partial_net_confidence": conf_partial["net_confidence"],
                "full_net_confidence": conf_full["net_confidence"],
                "confidence_shift": conf_full["net_confidence"] - conf_partial["net_confidence"],
                "partial_word_count": divergence["partial_word_count"],
                "full_word_count": divergence["full_word_count"],
            }
            task_metrics.append(task_metric)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = mname.replace(" ", "-").replace(".", "_")

        raw_path = RESULTS_DIR / f"{safe_name}_{timestamp}.json"
        with open(raw_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nRaw: {raw_path}")

        metrics_path = METRICS_DIR / f"{safe_name}_{timestamp}.json"
        with open(metrics_path, "w") as f:
            json.dump({"model": mid, "model_name": mname,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "tasks": task_metrics}, f, indent=2)
        print(f"Metrics: {metrics_path}")

        # Summary
        print_summary(mname, task_metrics)


def print_summary(model_name, task_metrics):
    """Print summary statistics."""
    import statistics

    print(f"\n{'='*60}")
    print(f"SUMMARY: {model_name}")
    print(f"{'='*60}")

    jd = [t["jaccard_distance"] for t in task_metrics]
    nw = [t["new_words_ratio"] for t in task_metrics]
    lr = [t["length_ratio"] for t in task_metrics]
    cs = [t["confidence_shift"] for t in task_metrics]

    print(f"  Jaccard distance (partial vs full):  mean={statistics.mean(jd):.3f}  std={statistics.stdev(jd):.3f}")
    print(f"  New words ratio (from added docs):   mean={statistics.mean(nw):.3f}  std={statistics.stdev(nw):.3f}")
    print(f"  Length ratio (full/partial):          mean={statistics.mean(lr):.2f}   std={statistics.stdev(lr):.2f}")
    print(f"  Confidence shift (full - partial):    mean={statistics.mean(cs):.4f}  std={statistics.stdev(cs):.4f}")

    # Per-category
    categories = sorted(set(t["category"] for t in task_metrics))
    print(f"\n  {'Category':15s} {'Jaccard':>8s} {'NewWords':>8s} {'LenRatio':>8s} {'ConfShift':>10s}")
    for cat in categories:
        cat_tasks = [t for t in task_metrics if t["category"] == cat]
        print(f"  {cat:15s} "
              f"{statistics.mean([t['jaccard_distance'] for t in cat_tasks]):8.3f} "
              f"{statistics.mean([t['new_words_ratio'] for t in cat_tasks]):8.3f} "
              f"{statistics.mean([t['length_ratio'] for t in cat_tasks]):8.2f} "
              f"{statistics.mean([t['confidence_shift'] for t in cat_tasks]):10.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exp 02a: Premature Compression")
    parser.add_argument("--model", help="Bedrock model ID")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-tasks", type=int)
    args = parser.parse_args()

    run_experiment(args.model, args.dry_run, args.max_tasks)
