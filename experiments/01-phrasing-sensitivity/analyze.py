#!/usr/bin/env python3
"""
Analyze phrasing sensitivity results.

Steps:
1. Load raw outputs from results/raw/*.jsonl
2. Compute embeddings via Bedrock (Cohere Embed v4)
3. Calculate phrasing sensitivity scores (cosine distance between phrasings)
4. Generate summary.json and analysis charts

Usage:
    python analyze.py                # Full analysis
    python analyze.py --embed-only   # Only compute embeddings
    python analyze.py --stats-only   # Only compute stats (embeddings must exist)
    python analyze.py --charts-only  # Only generate charts (stats must exist)
"""

import argparse
import json
import math
import os
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import boto3

RESULTS_DIR = Path(__file__).parent / "results"
RAW_DIR = RESULTS_DIR / "raw"
EMBED_DIR = RESULTS_DIR / "embeddings"
CHARTS_DIR = RESULTS_DIR / "charts"
SUMMARY_FILE = RESULTS_DIR / "summary.json"


def load_raw_results():
    """Load all raw results into a nested dict: model_id → task_id → [results by phrasing]."""
    data = defaultdict(lambda: defaultdict(dict))
    for f in sorted(RAW_DIR.glob("*.jsonl")):
        with open(f) as fh:
            for line in fh:
                rec = json.loads(line)
                if rec.get("output") is None:
                    continue
                model = rec["model_id"]
                task = rec["task_id"]
                pi = rec["phrasing_index"]
                data[model][task][pi] = rec
    return data


def compute_embeddings(client, data):
    """Compute embeddings for all outputs using Cohere Embed v4."""
    EMBED_DIR.mkdir(parents=True, exist_ok=True)
    embed_model = "us.cohere.embed-v4:0"

    for model_id, tasks in data.items():
        safe_id = model_id.replace(":", "_").replace("/", "_")
        outfile = EMBED_DIR / f"{safe_id}.jsonl"

        # Load existing
        existing = set()
        if outfile.exists():
            with open(outfile) as f:
                for line in f:
                    rec = json.loads(line)
                    existing.add((rec["task_id"], rec["phrasing_index"]))

        with open(outfile, "a") as f:
            for task_id, phrasings in tasks.items():
                for pi, rec in phrasings.items():
                    if (task_id, pi) in existing:
                        continue
                    text = rec["output"][:2048]  # Embed v4 input limit
                    try:
                        resp = client.invoke_model(
                            modelId=embed_model,
                            body=json.dumps({
                                "texts": [text],
                                "input_type": "search_document",
                            }),
                        )
                        body = json.loads(resp["body"].read())
                        embedding = body["embeddings"]["float"][0]
                        embed_rec = {
                            "model_id": model_id,
                            "task_id": task_id,
                            "phrasing_index": pi,
                            "embedding": embedding,
                        }
                        f.write(json.dumps(embed_rec) + "\n")
                        f.flush()
                    except Exception as e:
                        print(f"  Embed error {model_id}/{task_id}[{pi}]: {e}")

        print(f"  Embeddings done: {model_id}")


def cosine_distance(a, b):
    """Compute cosine distance (1 - cosine similarity) between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 1.0
    return 1.0 - (dot / (norm_a * norm_b))


def load_embeddings():
    """Load embeddings into: model_id → task_id → phrasing_index → embedding."""
    data = defaultdict(lambda: defaultdict(dict))
    for f in sorted(EMBED_DIR.glob("*.jsonl")):
        with open(f) as fh:
            for line in fh:
                rec = json.loads(line)
                model = rec["model_id"]
                task = rec["task_id"]
                pi = rec["phrasing_index"]
                data[model][task][pi] = rec["embedding"]
    return data


def compute_stats(raw_data, embed_data):
    """Compute phrasing sensitivity scores per model and category."""
    summary = {}

    for model_id in raw_data:
        model_rec = None
        for task_recs in raw_data[model_id].values():
            for rec in task_recs.values():
                model_rec = rec
                break
            if model_rec:
                break

        if not model_rec:
            continue

        category_scores = defaultdict(list)
        task_scores = {}

        for task_id, phrasings in raw_data[model_id].items():
            category = list(phrasings.values())[0]["task_category"]

            # Embedding-based divergence
            if model_id in embed_data and task_id in embed_data[model_id]:
                embeddings = embed_data[model_id][task_id]
                if len(embeddings) >= 2:
                    pairs = list(combinations(sorted(embeddings.keys()), 2))
                    distances = [cosine_distance(embeddings[a], embeddings[b]) for a, b in pairs]
                    mean_dist = sum(distances) / len(distances) if distances else 0
                    category_scores[category].append(mean_dist)
                    task_scores[task_id] = {
                        "category": category,
                        "sensitivity": round(mean_dist, 6),
                        "n_phrasings": len(embeddings),
                    }

            # Length variance
            lengths = [len(rec["output"]) for rec in phrasings.values() if rec.get("output")]
            if len(lengths) >= 2:
                mean_len = sum(lengths) / len(lengths)
                if mean_len > 0:
                    var = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
                    cv = math.sqrt(var) / mean_len  # coefficient of variation
                    task_scores.setdefault(task_id, {})["length_cv"] = round(cv, 4)

        # Aggregate
        by_category = {}
        for cat, scores in category_scores.items():
            by_category[cat] = round(sum(scores) / len(scores), 6) if scores else None

        all_scores = [s for scores in category_scores.values() for s in scores]
        overall = round(sum(all_scores) / len(all_scores), 6) if all_scores else None

        summary[model_id] = {
            "model_name": model_rec.get("model_name"),
            "parameter_count": model_rec.get("model_params"),
            "provider": model_rec.get("provider"),
            "overall_sensitivity": overall,
            "by_category": by_category,
            "tasks": task_scores,
        }

    return summary


def generate_charts(summary):
    """Generate analysis charts using matplotlib."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("matplotlib/numpy not installed. Skipping charts.")
        print("Install: pip install matplotlib numpy")
        return

    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    # Chart 1: Overall sensitivity vs parameter count
    models_with_params = [
        (v["parameter_count"], v["overall_sensitivity"], v["model_name"])
        for v in summary.values()
        if v["parameter_count"] is not None and v["overall_sensitivity"] is not None
    ]
    models_with_params.sort(key=lambda x: x[0])

    if models_with_params:
        params, sens, names = zip(*models_with_params)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.scatter([p / 1e9 for p in params], sens, s=60, alpha=0.7)
        for p, s, n in zip(params, sens, names):
            ax.annotate(n, (p / 1e9, s), fontsize=7, alpha=0.7, rotation=15)
        ax.set_xlabel("Parameter Count (Billions)")
        ax.set_ylabel("Mean Phrasing Sensitivity (Cosine Distance)")
        ax.set_title("Phrasing Sensitivity vs Model Size")
        ax.set_xscale("log")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(CHARTS_DIR / "sensitivity_vs_size.png", dpi=150)
        plt.close()
        print(f"  Chart: sensitivity_vs_size.png")

    # Chart 2: Sensitivity by category across model sizes
    categories = ["factual", "summarization", "judgment", "creative"]
    fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharey=True)

    for i, cat in enumerate(categories):
        cat_data = [
            (v["parameter_count"], v["by_category"].get(cat))
            for v in summary.values()
            if v["parameter_count"] is not None and v["by_category"].get(cat) is not None
        ]
        cat_data.sort(key=lambda x: x[0])
        if cat_data:
            params, sens = zip(*cat_data)
            axes[i].scatter([p / 1e9 for p in params], sens, s=40, alpha=0.7)
            axes[i].set_title(cat.capitalize())
            axes[i].set_xlabel("Params (B)")
            axes[i].set_xscale("log")
            axes[i].grid(True, alpha=0.3)
    axes[0].set_ylabel("Sensitivity")
    fig.suptitle("Phrasing Sensitivity by Task Category vs Model Size")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "sensitivity_by_category.png", dpi=150)
    plt.close()
    print(f"  Chart: sensitivity_by_category.png")

    # Chart 3: Category comparison (bar chart, all models averaged)
    cat_avgs = {}
    for cat in categories:
        vals = [
            v["by_category"][cat]
            for v in summary.values()
            if v["by_category"].get(cat) is not None
        ]
        if vals:
            cat_avgs[cat] = sum(vals) / len(vals)

    if cat_avgs:
        fig, ax = plt.subplots(figsize=(8, 5))
        cats = list(cat_avgs.keys())
        vals = [cat_avgs[c] for c in cats]
        bars = ax.bar(cats, vals, color=["#2ecc71", "#e67e22", "#e74c3c", "#9b59b6"])
        ax.set_ylabel("Mean Phrasing Sensitivity")
        ax.set_title("Average Sensitivity by Task Category (All Models)")
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                    f"{val:.4f}", ha="center", fontsize=9)
        fig.tight_layout()
        fig.savefig(CHARTS_DIR / "category_comparison.png", dpi=150)
        plt.close()
        print(f"  Chart: category_comparison.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--embed-only", action="store_true")
    parser.add_argument("--stats-only", action="store_true")
    parser.add_argument("--charts-only", action="store_true")
    parser.add_argument("--region", default="us-east-1")
    args = parser.parse_args()

    if args.charts_only:
        if SUMMARY_FILE.exists():
            with open(SUMMARY_FILE) as f:
                summary = json.load(f)
            generate_charts(summary)
        else:
            print(f"No summary file at {SUMMARY_FILE}. Run full analysis first.")
        return

    raw_data = load_raw_results()
    if not raw_data:
        print("No raw results found. Run run.py first.")
        sys.exit(1)

    print(f"Loaded {len(raw_data)} models from {RAW_DIR}")

    if not args.stats_only:
        client = boto3.client("bedrock-runtime", region_name=args.region)
        print("Computing embeddings...")
        compute_embeddings(client, raw_data)

    embed_data = load_embeddings()
    print(f"Loaded embeddings for {len(embed_data)} models")

    if not args.embed_only:
        print("Computing statistics...")
        summary = compute_stats(raw_data, embed_data)

        with open(SUMMARY_FILE, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"Summary written to {SUMMARY_FILE}")

        print("Generating charts...")
        generate_charts(summary)

    print("\nDone.")


if __name__ == "__main__":
    main()
