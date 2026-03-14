#!/usr/bin/env python3
"""
Experiment 05: Confidence Language Density — Bedrock 30-Model Sweep

Runs the confidence density analysis across all available Bedrock models.
Uses AWS Bedrock Converse API for model-agnostic inference.

Usage:
    python run_bedrock.py                    # Run all models
    python run_bedrock.py --model-id anthropic.claude-3-haiku-20240307-v1:0
    python run_bedrock.py --dry-run          # Show what would run
    python run_bedrock.py --max-tasks 2      # Quick test
    python run_bedrock.py --category factual # Single category
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3
import numpy as np

# Paths
RESULTS_DIR = Path(__file__).parent / "results" / "bedrock-raw"
METRICS_DIR = Path(__file__).parent / "results" / "bedrock-metrics"
TASKS_FILE = Path(__file__).parent.parent / "01-phrasing-sensitivity" / "tasks.json"

# Import analysis functions from the local version
sys.path.insert(0, str(Path(__file__).parent))
from run import (
    compute_certainty_score,
    compute_phrasing_sensitivity,
    print_correlation_summary,
)

# Bedrock models to test — grouped by provider
BEDROCK_MODELS = [
    # Anthropic
    {"id": "anthropic.claude-3-haiku-20240307-v1:0", "name": "Claude 3 Haiku", "provider": "Anthropic"},
    {"id": "anthropic.claude-3-sonnet-20240229-v1:0", "name": "Claude 3 Sonnet", "provider": "Anthropic"},
    {"id": "anthropic.claude-3-5-sonnet-20240620-v1:0", "name": "Claude 3.5 Sonnet", "provider": "Anthropic"},
    # Meta
    {"id": "meta.llama3-8b-instruct-v1:0", "name": "Llama 3 8B", "provider": "Meta"},
    {"id": "meta.llama3-70b-instruct-v1:0", "name": "Llama 3 70B", "provider": "Meta"},
    # Mistral
    {"id": "mistral.mistral-7b-instruct-v0:2", "name": "Mistral 7B", "provider": "Mistral"},
    {"id": "mistral.ministral-3-3b-instruct", "name": "Ministral 3B", "provider": "Mistral"},
    {"id": "mistral.ministral-3-8b-instruct", "name": "Ministral 8B", "provider": "Mistral"},
    {"id": "mistral.ministral-3-14b-instruct", "name": "Ministral 14B", "provider": "Mistral"},
    {"id": "mistral.mistral-large-2402-v1:0", "name": "Mistral Large", "provider": "Mistral"},
    # Amazon
    {"id": "amazon.nova-micro-v1:0", "name": "Nova Micro", "provider": "Amazon"},
    {"id": "amazon.nova-lite-v1:0", "name": "Nova Lite", "provider": "Amazon"},
    {"id": "amazon.nova-pro-v1:0", "name": "Nova Pro", "provider": "Amazon"},
    # DeepSeek
    {"id": "deepseek.v3.2", "name": "DeepSeek V3.2", "provider": "DeepSeek"},
    # Qwen
    {"id": "qwen.qwen3-32b-v1:0", "name": "Qwen3 32B", "provider": "Qwen"},
    {"id": "qwen.qwen3-next-80b-a3b", "name": "Qwen3 Next 80B-A3B", "provider": "Qwen"},
    # Google
    {"id": "google.gemma-3-4b-it", "name": "Gemma 3 4B", "provider": "Google"},
    {"id": "google.gemma-3-12b-it", "name": "Gemma 3 12B", "provider": "Google"},
    {"id": "google.gemma-3-27b-it", "name": "Gemma 3 27B", "provider": "Google"},
    # AI21
    {"id": "ai21.jamba-1-5-mini-v1:0", "name": "Jamba 1.5 Mini", "provider": "AI21"},
    {"id": "ai21.jamba-1-5-large-v1:0", "name": "Jamba 1.5 Large", "provider": "AI21"},
    # Cohere
    {"id": "cohere.command-r-v1:0", "name": "Command R", "provider": "Cohere"},
    {"id": "cohere.command-r-plus-v1:0", "name": "Command R+", "provider": "Cohere"},
    # Z.AI (GLM)
    {"id": "zai.glm-4.7", "name": "GLM 4.7", "provider": "Z.AI"},
    {"id": "zai.glm-4.7-flash", "name": "GLM 4.7 Flash", "provider": "Z.AI"},
    # Moonshot
    {"id": "moonshotai.kimi-k2.5", "name": "Kimi K2.5", "provider": "Moonshot"},
    # MiniMax
    {"id": "minimax.minimax-m2", "name": "MiniMax M2", "provider": "MiniMax"},
    {"id": "minimax.minimax-m2.1", "name": "MiniMax M2.1", "provider": "MiniMax"},
    # NVIDIA
    {"id": "nvidia.nemotron-nano-9b-v2", "name": "Nemotron Nano 9B", "provider": "NVIDIA"},
    {"id": "nvidia.nemotron-nano-12b-v2", "name": "Nemotron Nano 12B", "provider": "NVIDIA"},
]


def invoke_bedrock(client, model_id: str, prompt: str, max_tokens: int = 256) -> str:
    """
    Call a Bedrock model via the Converse API.
    Returns the response text.
    """
    try:
        response = client.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}],
                }
            ],
            inferenceConfig={
                "maxTokens": max_tokens,
                "temperature": 0.0,
            },
        )
        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        error_msg = str(e)
        if "AccessDeniedException" in error_msg or "not authorized" in error_msg.lower():
            return None  # Model not enabled
        if "ThrottlingException" in error_msg:
            time.sleep(5)
            return invoke_bedrock(client, model_id, prompt, max_tokens)
        print(f"\n  ERROR: {error_msg[:100]}")
        return None


def load_tasks(category=None):
    with open(TASKS_FILE) as f:
        tasks = json.load(f)
    if category:
        tasks = [t for t in tasks if t["category"] == category]
    return tasks


def run_single_model(client, model_info: dict, tasks: list) -> dict | None:
    """Run all tasks on a single Bedrock model. Returns metrics or None if model unavailable."""
    model_id = model_info["id"]
    model_name = model_info["name"]
    provider = model_info["provider"]

    # Quick probe — test if model is accessible
    probe = invoke_bedrock(client, model_id, "Say hello in one word.")
    if probe is None:
        print(f"  SKIP {model_name} — not accessible")
        return None

    print(f"\n{'='*60}")
    print(f"Model: {model_name} ({provider})")
    print(f"ID: {model_id}")
    print(f"{'='*60}")

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
                f"  [{inference_count}/{total_inferences}] {task_id} p{pi}...",
                end=" ",
                flush=True,
            )

            t0 = time.time()
            response = invoke_bedrock(client, model_id, prompt)
            elapsed = time.time() - t0

            if response is None:
                print("FAILED")
                continue

            scores = compute_certainty_score(response)
            responses.append(response)
            phrasing_scores.append(scores)

            print(
                f"CS={scores['certainty_score']:+.4f} "
                f"hi={scores['high_count']} "
                f"hedge={scores['hedge_count']} "
                f"words={scores['total_words']} ({elapsed:.1f}s)"
            )

            results.append({
                "model_id": model_id,
                "model_name": model_name,
                "provider": provider,
                "task_id": task_id,
                "category": category_name,
                "phrasing_index": pi,
                "prompt": prompt,
                "response": response,
                "scores": scores,
                "elapsed_seconds": elapsed,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        if len(responses) < 2:
            continue

        # Task-level summary
        ps = compute_phrasing_sensitivity(responses)
        avg = {
            "task_id": task_id,
            "category": category_name,
            "phrasing_sensitivity": ps,
            "mean_certainty_score": float(np.mean([s["certainty_score"] for s in phrasing_scores])),
            "std_certainty_score": float(np.std([s["certainty_score"] for s in phrasing_scores])),
            "mean_high_density": float(np.mean([s["high_density"] for s in phrasing_scores])),
            "mean_hedge_density": float(np.mean([s["hedge_density"] for s in phrasing_scores])),
            "mean_total_words": float(np.mean([s["total_words"] for s in phrasing_scores])),
            "total_high_markers": sum(s["high_count"] for s in phrasing_scores),
            "total_hedge_markers": sum(s["hedge_count"] for s in phrasing_scores),
        }
        task_metrics.append(avg)
        print(f"    -> PS={ps:.3f} CS={avg['mean_certainty_score']:+.4f}")

    if not task_metrics:
        return None

    # Save per-model results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = model_name.replace(" ", "_").replace("/", "-")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    raw_path = RESULTS_DIR / f"{safe_name}_{timestamp}.json"
    with open(raw_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    metrics_path = METRICS_DIR / f"{safe_name}_{timestamp}.json"
    with open(metrics_path, "w") as f:
        json.dump({
            "model_id": model_id,
            "model_name": model_name,
            "provider": provider,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tasks": task_metrics,
        }, f, indent=2)

    # Print correlation for this model
    print_correlation_summary(task_metrics)

    return {
        "model_id": model_id,
        "model_name": model_name,
        "provider": provider,
        "n_tasks": len(task_metrics),
        "tasks": task_metrics,
    }


def run_sweep(models: list, tasks: list, dry_run: bool = False):
    """Run the full Bedrock model sweep."""
    if dry_run:
        print("DRY RUN — Bedrock 30-model sweep")
        print(f"  Models: {len(models)}")
        print(f"  Tasks: {len(tasks)}")
        print(f"  Phrasings per task: {len(tasks[0]['phrasings'])}")
        print(f"  Total inferences per model: {sum(len(t['phrasings']) for t in tasks)}")
        print(f"  Total inferences (all models): {sum(len(t['phrasings']) for t in tasks) * len(models)}")
        print()
        for m in models:
            print(f"  {m['provider']:15s} {m['name']:30s} {m['id']}")
        return

    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    all_results = []
    skipped = []
    failed = []

    for i, model_info in enumerate(models):
        print(f"\n[Model {i+1}/{len(models)}]")
        result = run_single_model(client, model_info, tasks)
        if result is None:
            skipped.append(model_info["name"])
        else:
            all_results.append(result)

    # Cross-model summary
    print("\n" + "=" * 70)
    print("CROSS-MODEL SUMMARY")
    print("=" * 70)
    print(f"Tested: {len(all_results)} models")
    print(f"Skipped (not accessible): {len(skipped)}")
    if skipped:
        print(f"  {', '.join(skipped)}")

    # Per-model mean certainty score and PS
    print(f"\n{'Model':30s} {'Provider':15s} {'Mean CS':>10s} {'Mean PS':>10s} {'n':>4s}")
    print("-" * 75)
    for r in all_results:
        mean_cs = np.mean([t["mean_certainty_score"] for t in r["tasks"]])
        mean_ps = np.mean([t["phrasing_sensitivity"] for t in r["tasks"]])
        print(f"{r['model_name']:30s} {r['provider']:15s} {mean_cs:+10.4f} {mean_ps:10.3f} {r['n_tasks']:4d}")

    # Cross-model correlation: is CS-PS relationship consistent?
    print("\nCross-model: Mean certainty score vs mean phrasing sensitivity")
    from scipy import stats
    model_cs = [np.mean([t["mean_certainty_score"] for t in r["tasks"]]) for r in all_results]
    model_ps = [np.mean([t["phrasing_sensitivity"] for t in r["tasks"]]) for r in all_results]
    if len(model_cs) >= 3:
        r_p, p_p = stats.pearsonr(model_cs, model_ps)
        r_s, p_s = stats.spearmanr(model_cs, model_ps)
        print(f"  Pearson:  r={r_p:+.3f}  p={p_p:.4f}")
        print(f"  Spearman: r={r_s:+.3f}  p={p_s:.4f}")

    # Save cross-model summary
    summary_path = METRICS_DIR / f"cross_model_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_path, "w") as f:
        json.dump({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "models_tested": len(all_results),
            "models_skipped": skipped,
            "results": all_results,
        }, f, indent=2, default=str)
    print(f"\nCross-model summary: {summary_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exp 05: Confidence density — Bedrock 30-model sweep"
    )
    parser.add_argument("--model-id", help="Single Bedrock model ID to test")
    parser.add_argument(
        "--category",
        choices=["factual", "summarization", "judgment", "creative"],
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-tasks", type=int, help="Limit number of tasks")
    args = parser.parse_args()

    tasks = load_tasks(args.category)
    if args.max_tasks:
        tasks = tasks[:args.max_tasks]

    if args.model_id:
        # Single model run
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        model_info = {"id": args.model_id, "name": args.model_id.split(".")[-1], "provider": "unknown"}
        # Try to find in our list
        for m in BEDROCK_MODELS:
            if m["id"] == args.model_id:
                model_info = m
                break
        if args.dry_run:
            print(f"DRY RUN: {model_info['name']}")
            print(f"  Tasks: {len(tasks)}, Inferences: {sum(len(t['phrasings']) for t in tasks)}")
        else:
            run_single_model(client, model_info, tasks)
    else:
        run_sweep(BEDROCK_MODELS, tasks, args.dry_run)
