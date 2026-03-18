#!/usr/bin/env python3
"""
Experiment 02a: Premature Compression — Bedrock New-Model Replication

Replicates the premature compression experiment on new Bedrock models not
tested in the original run (DeepSeek V3.2, Qwen3, Claude Sonnet/Opus 4.6,
Gemma 3, GLM 4.7, Kimi K2.5).

Key finding to replicate: outputs change massively (Jaccard 0.72-0.82) but
confidence stays identical (~0 shift). This proves premature compression is
universal — not an artifact of specific architectures.

Method:
    For each task:
    1. Give model PARTIAL documents (2 of 4-6) + question -> Response A
    2. Give model ALL documents + question -> Response B
    3. Measure: Jaccard distance, confidence shift, word count ratio, new words ratio

Usage:
    python run_bedrock.py --dry-run             # See what would run
    python run_bedrock.py --max-tasks 2         # Quick test
    python run_bedrock.py                       # Full run (8 tasks x 2 x N models)
    python run_bedrock.py --model-id deepseek.v3.2  # Single model
"""

import argparse
import json
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

# Paths
RESULTS_DIR = Path(__file__).parent / "results" / "bedrock-raw"
METRICS_DIR = Path(__file__).parent / "results" / "bedrock-metrics"
TASKS_FILE = Path(__file__).parent / "tasks.json"

# New models not in the original experiment — 8 models across 6 providers
BEDROCK_MODELS = [
    # DeepSeek
    {"id": "deepseek.v3.2", "name": "DeepSeek V3.2", "provider": "DeepSeek"},
    # Qwen
    {"id": "qwen.qwen3-32b-v1:0", "name": "Qwen3 32B", "provider": "Qwen"},
    {"id": "qwen.qwen3-next-80b-a3b", "name": "Qwen3 Next 80B-A3B", "provider": "Qwen"},
    # Anthropic (inference profiles for signed routing)
    {"id": "us.anthropic.claude-sonnet-4-6-20250514-v1:0", "name": "Claude Sonnet 4.6", "provider": "Anthropic"},
    {"id": "us.anthropic.claude-opus-4-6-20250514-v1:0", "name": "Claude Opus 4.6", "provider": "Anthropic"},
    # Google
    {"id": "google.gemma-3-27b-it", "name": "Gemma 3 27B", "provider": "Google"},
    # Z.AI
    {"id": "zai.glm-4.7", "name": "GLM 4.7", "provider": "Z.AI"},
    # Moonshot
    {"id": "moonshotai.kimi-k2.5", "name": "Kimi K2.5", "provider": "Moonshot"},
]

# ── Confidence markers (same as original run.py for comparability) ──────────

HEDGING_MARKERS = [
    "might", "perhaps", "possibly", "could be", "it seems",
    "arguably", "may", "uncertain", "unclear", "debatable",
    "it's possible", "one could argue", "to some extent",
]

CONFIDENCE_MARKERS = [
    "clearly", "obviously", "certainly", "undoubtedly",
    "the key", "the central", "the main", "fundamentally",
    "it is clear", "without question", "definitively",
    "the answer is", "in conclusion",
]

# Extended markers from Exp 05 certainty scoring (for richer signal)
EXTENDED_HIGH_MARKERS = [
    "definitely", "without doubt", "unquestionably", "indisputably",
    "absolutely", "conclusively", "it is evident", "it is apparent",
    "demonstrably", "incontrovertibly", "beyond question",
]

EXTENDED_HEDGE_MARKERS = [
    "likely", "probably", "appears to", "seems to",
    "it is worth noting", "to a degree", "in some cases",
    "not entirely clear", "remains to be seen", "open question",
]


def compute_confidence_markers(text):
    """
    Count hedging vs confidence language.
    Uses the original markers (for comparability with run.py) plus extended
    markers (for richer signal). Reports both.
    """
    text_lower = text.lower()
    word_count = len(text.split())

    # Original markers (comparable to run.py)
    hedge_count = sum(1 for h in HEDGING_MARKERS if h in text_lower)
    confidence_count = sum(1 for c in CONFIDENCE_MARKERS if c in text_lower)

    # Extended markers
    ext_high = sum(1 for m in EXTENDED_HIGH_MARKERS if m in text_lower)
    ext_hedge = sum(1 for m in EXTENDED_HEDGE_MARKERS if m in text_lower)

    total_high = confidence_count + ext_high
    total_hedge = hedge_count + ext_hedge

    return {
        "hedge_count": hedge_count,
        "confidence_count": confidence_count,
        "hedge_rate": hedge_count / word_count if word_count else 0.0,
        "confidence_rate": confidence_count / word_count if word_count else 0.0,
        "net_confidence": (confidence_count - hedge_count) / word_count if word_count else 0.0,
        # Extended (Exp 05-style certainty score)
        "ext_high_count": total_high,
        "ext_hedge_count": total_hedge,
        "certainty_score": (total_high - total_hedge) / word_count if word_count else 0.0,
        "word_count": word_count,
    }


# ── Bedrock API ─────────────────────────────────────────────────────────────

def call_model(client, model_id, prompt, max_tokens=800):
    """
    Call Bedrock Converse API.
    Returns (output_text, latency_ms, input_tokens, output_tokens).
    Handles DeepSeek reasoning content, throttling, and access errors.
    """
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    is_thinking = "deepseek" in model_id.lower()

    t0 = time.time()
    try:
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
        latency = int((time.time() - t0) * 1000)
        error_msg = str(e)
        if "ThrottlingException" in error_msg:
            print("(throttled, retrying in 5s)...", end=" ", flush=True)
            time.sleep(5)
            return call_model(client, model_id, prompt, max_tokens)
        return f"ERROR: {e}", latency, 0, 0


def probe_model(client, model_id):
    """Quick accessibility check. Returns True if model responds."""
    try:
        response = client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": "Say hello in one word."}]}],
            inferenceConfig={"maxTokens": 8, "temperature": 0.0},
        )
        return True
    except Exception:
        return False


# ── Metrics ─────────────────────────────────────────────────────────────────

def word_set(text):
    """Tokenize to word set for Jaccard similarity."""
    return set(text.lower().strip().split())


def compute_divergence(response_a, response_b):
    """Compute divergence metrics comparing partial vs full responses."""
    words_a = word_set(response_a)
    words_b = word_set(response_b)

    if not words_a and not words_b:
        return {
            "jaccard_distance": 0.0, "jaccard_similarity": 0.0,
            "new_words_count": 0, "new_words_ratio": 0.0,
            "dropped_words_count": 0, "dropped_words_ratio": 0.0,
            "partial_word_count": 0, "full_word_count": 0, "length_ratio": 0.0,
        }

    union = words_a | words_b
    intersection = words_a & words_b
    jaccard = len(intersection) / len(union) if union else 0.0

    new_words = words_b - words_a
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


# ── Prompt construction ────────────────────────────────────────────────────

def build_prompt(question, documents):
    """Build prompt with documents as context — identical to original run.py."""
    doc_text = "\n\n".join(documents)
    return f"""Read the following documents carefully, then answer the question.

{doc_text}

Question: {question}

Provide a thorough answer that draws on all the documents provided."""


# ── Single model run ────────────────────────────────────────────────────────

def run_single_model(client, model_info, tasks):
    """
    Run all tasks on one model. Returns (results_list, task_metrics_list) or None.
    """
    mid = model_info["id"]
    mname = model_info["name"]
    provider = model_info["provider"]

    # Probe accessibility
    if not probe_model(client, mid):
        print(f"  SKIP {mname} — not accessible")
        return None

    print(f"\n{'='*60}")
    print(f"MODEL: {mname} ({provider})")
    print(f"ID: {mid}")
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
        if resp_partial.startswith("ERROR:"):
            print(f"FAILED: {resp_partial[:80]}")
            continue
        print(f"{out_p} tokens ({lat_p}ms)")

        # --- Full context ---
        prompt_full = build_prompt(question, full_docs)
        print(f"  Full...", end=" ", flush=True)
        resp_full, lat_f, in_f, out_f = call_model(client, mid, prompt_full)
        if resp_full.startswith("ERROR:"):
            print(f"FAILED: {resp_full[:80]}")
            continue
        print(f"{out_f} tokens ({lat_f}ms)")

        # --- Compute metrics ---
        divergence = compute_divergence(resp_partial, resp_full)
        conf_partial = compute_confidence_markers(resp_partial)
        conf_full = compute_confidence_markers(resp_full)

        print(f"  Divergence: jaccard_dist={divergence['jaccard_distance']:.3f} "
              f"new_words={divergence['new_words_ratio']:.3f} "
              f"length_ratio={divergence['length_ratio']:.2f}")
        print(f"  Confidence: partial_net={conf_partial['net_confidence']:.4f} "
              f"full_net={conf_full['net_confidence']:.4f} "
              f"shift={conf_full['net_confidence'] - conf_partial['net_confidence']:.4f}")
        print(f"  Certainty:  partial_CS={conf_partial['certainty_score']:+.4f} "
              f"full_CS={conf_full['certainty_score']:+.4f} "
              f"shift={conf_full['certainty_score'] - conf_partial['certainty_score']:+.4f}")

        result = {
            "model": mid,
            "model_name": mname,
            "provider": provider,
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
            "partial_certainty_score": conf_partial["certainty_score"],
            "full_certainty_score": conf_full["certainty_score"],
            "certainty_shift": conf_full["certainty_score"] - conf_partial["certainty_score"],
            "partial_word_count": divergence["partial_word_count"],
            "full_word_count": divergence["full_word_count"],
        }
        task_metrics.append(task_metric)

    if not task_metrics:
        return None

    return results, task_metrics


# ── Summary printing ────────────────────────────────────────────────────────

def print_summary(model_name, task_metrics):
    """Print summary statistics for a single model."""
    print(f"\n{'='*60}")
    print(f"SUMMARY: {model_name}")
    print(f"{'='*60}")

    jd = [t["jaccard_distance"] for t in task_metrics]
    nw = [t["new_words_ratio"] for t in task_metrics]
    lr = [t["length_ratio"] for t in task_metrics]
    cs = [t["confidence_shift"] for t in task_metrics]
    cert_s = [t["certainty_shift"] for t in task_metrics]

    def safe_std(vals):
        return statistics.stdev(vals) if len(vals) > 1 else 0.0

    print(f"  Jaccard distance (partial vs full):  mean={statistics.mean(jd):.3f}  std={safe_std(jd):.3f}")
    print(f"  New words ratio (from added docs):   mean={statistics.mean(nw):.3f}  std={safe_std(nw):.3f}")
    print(f"  Length ratio (full/partial):          mean={statistics.mean(lr):.2f}   std={safe_std(lr):.2f}")
    print(f"  Confidence shift (full - partial):    mean={statistics.mean(cs):.4f}  std={safe_std(cs):.4f}")
    print(f"  Certainty shift (extended markers):   mean={statistics.mean(cert_s):+.4f}  std={safe_std(cert_s):.4f}")

    # Per-category
    categories = sorted(set(t["category"] for t in task_metrics))
    print(f"\n  {'Category':15s} {'Jaccard':>8s} {'NewWords':>8s} {'LenRatio':>8s} {'ConfShift':>10s} {'CertShift':>10s}")
    for cat in categories:
        cat_tasks = [t for t in task_metrics if t["category"] == cat]
        print(f"  {cat:15s} "
              f"{statistics.mean([t['jaccard_distance'] for t in cat_tasks]):8.3f} "
              f"{statistics.mean([t['new_words_ratio'] for t in cat_tasks]):8.3f} "
              f"{statistics.mean([t['length_ratio'] for t in cat_tasks]):8.2f} "
              f"{statistics.mean([t['confidence_shift'] for t in cat_tasks]):10.4f} "
              f"{statistics.mean([t['certainty_shift'] for t in cat_tasks]):+10.4f}")

    # Replication verdict
    mean_jd = statistics.mean(jd)
    mean_cs = statistics.mean(cs)
    print(f"\n  REPLICATION:")
    if 0.60 <= mean_jd <= 0.95:
        print(f"    Jaccard {mean_jd:.3f} — IN RANGE (original: 0.72-0.82)")
    else:
        print(f"    Jaccard {mean_jd:.3f} — OUTSIDE RANGE (original: 0.72-0.82)")
    if abs(mean_cs) < 0.005:
        print(f"    Confidence shift {mean_cs:+.4f} — NEAR ZERO (replicates)")
    else:
        print(f"    Confidence shift {mean_cs:+.4f} — NON-TRIVIAL (does NOT replicate)")


def print_cross_model_summary(all_model_results):
    """Print cross-model comparison table."""
    print("\n" + "=" * 90)
    print("CROSS-MODEL REPLICATION SUMMARY")
    print("=" * 90)

    # Header
    print(f"\n{'Model':<25s} {'Provider':<12s} {'Jaccard':>8s} {'NewWords':>8s} "
          f"{'LenRatio':>8s} {'ConfShift':>10s} {'CertShift':>10s} {'Replicates':>10s}")
    print("-" * 95)

    for model_name, provider, task_metrics in all_model_results:
        jd = statistics.mean([t["jaccard_distance"] for t in task_metrics])
        nw = statistics.mean([t["new_words_ratio"] for t in task_metrics])
        lr = statistics.mean([t["length_ratio"] for t in task_metrics])
        cs = statistics.mean([t["confidence_shift"] for t in task_metrics])
        cert_s = statistics.mean([t["certainty_shift"] for t in task_metrics])

        replicates = "YES" if (0.60 <= jd <= 0.95 and abs(cs) < 0.005) else "NO"

        print(f"{model_name:<25s} {provider:<12s} {jd:8.3f} {nw:8.3f} "
              f"{lr:8.2f} {cs:+10.4f} {cert_s:+10.4f} {replicates:>10s}")

    # Overall
    all_jd = [statistics.mean([t["jaccard_distance"] for t in tm]) for _, _, tm in all_model_results]
    all_cs = [statistics.mean([t["confidence_shift"] for t in tm]) for _, _, tm in all_model_results]

    print("-" * 95)
    print(f"{'MEAN':<25s} {'':12s} {statistics.mean(all_jd):8.3f} {'':8s} "
          f"{'':8s} {statistics.mean(all_cs):+10.4f}")
    print(f"{'ORIGINAL (16 models)':<25s} {'':12s} {'0.76':>8s} {'':8s} "
          f"{'':8s} {'+0.0001':>10s}")

    replicated = sum(1 for jd, cs in zip(all_jd, all_cs) if 0.60 <= jd <= 0.95 and abs(cs) < 0.005)
    print(f"\nReplication rate: {replicated}/{len(all_model_results)} models")
    if replicated == len(all_model_results):
        print("CONCLUSION: Premature compression replicates across all new architectures.")
    elif replicated > len(all_model_results) // 2:
        print("CONCLUSION: Premature compression replicates for majority of new architectures.")
    else:
        print("CONCLUSION: Mixed results — premature compression does NOT universally replicate.")


# ── Main ────────────────────────────────────────────────────────────────────

def run_experiment(model_id=None, dry_run=False, max_tasks=None):
    """Run the Bedrock premature compression replication."""

    with open(TASKS_FILE) as f:
        tasks = json.load(f)
    if max_tasks:
        tasks = tasks[:max_tasks]

    models = BEDROCK_MODELS
    if model_id:
        models = [m for m in BEDROCK_MODELS if m["id"] == model_id]
        if not models:
            # Allow ad-hoc model IDs
            provider = "unknown"
            name = model_id.split(".")[-1] if "." in model_id else model_id
            models = [{"id": model_id, "name": name, "provider": provider}]

    if dry_run:
        print("DRY RUN — Exp 02a Bedrock Replication")
        print(f"  Models: {len(models)}")
        print(f"  Tasks: {len(tasks)}")
        print(f"  Inferences per task: 2 (partial + full)")
        print(f"  Total inferences: {len(models) * len(tasks) * 2}")
        print()
        for m in models:
            print(f"  {m['provider']:12s} {m['name']:30s} {m['id']}")
        print()
        print(f"Original finding to replicate:")
        print(f"  Jaccard distance: 0.72-0.82 (outputs change massively)")
        print(f"  Confidence shift: ~0.0001 (model cannot detect incompleteness)")
        return

    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)

    all_model_results = []
    skipped = []

    for i, model_info in enumerate(models):
        print(f"\n[Model {i+1}/{len(models)}]")
        result = run_single_model(client, model_info, tasks)

        if result is None:
            skipped.append(model_info["name"])
            continue

        results, task_metrics = result
        mid = model_info["id"]
        mname = model_info["name"]
        provider = model_info["provider"]

        # Save raw results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = mname.replace(" ", "-").replace(".", "_")

        raw_path = RESULTS_DIR / f"{safe_name}_{timestamp}.json"
        with open(raw_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nRaw: {raw_path}")

        # Save metrics
        metrics_path = METRICS_DIR / f"{safe_name}_{timestamp}.json"
        with open(metrics_path, "w") as f:
            json.dump({
                "model": mid,
                "model_name": mname,
                "provider": provider,
                "experiment": "02a-premature-compression-bedrock-replication",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "n_tasks": len(task_metrics),
                "tasks": task_metrics,
            }, f, indent=2)
        print(f"Metrics: {metrics_path}")

        # Print per-model summary
        print_summary(mname, task_metrics)

        all_model_results.append((mname, provider, task_metrics))

    # Cross-model summary
    if len(all_model_results) > 1:
        print_cross_model_summary(all_model_results)

    if skipped:
        print(f"\nSkipped (not accessible): {', '.join(skipped)}")

    # Save cross-model summary
    if all_model_results:
        summary_path = METRICS_DIR / f"cross_model_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        summary_data = {
            "experiment": "02a-premature-compression-bedrock-replication",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "original_finding": {
                "jaccard_distance_range": [0.72, 0.82],
                "confidence_shift_mean": 0.0001,
                "models_tested": 16,
                "architectures": ["Llama", "Mistral", "Nova", "Claude"],
            },
            "models_tested": len(all_model_results),
            "models_skipped": skipped,
            "per_model": [
                {
                    "model_name": name,
                    "provider": prov,
                    "mean_jaccard_distance": statistics.mean([t["jaccard_distance"] for t in tm]),
                    "mean_confidence_shift": statistics.mean([t["confidence_shift"] for t in tm]),
                    "mean_certainty_shift": statistics.mean([t["certainty_shift"] for t in tm]),
                    "mean_new_words_ratio": statistics.mean([t["new_words_ratio"] for t in tm]),
                    "mean_length_ratio": statistics.mean([t["length_ratio"] for t in tm]),
                    "replicates": (
                        0.60 <= statistics.mean([t["jaccard_distance"] for t in tm]) <= 0.95
                        and abs(statistics.mean([t["confidence_shift"] for t in tm])) < 0.005
                    ),
                }
                for name, prov, tm in all_model_results
            ],
        }
        with open(summary_path, "w") as f:
            json.dump(summary_data, f, indent=2)
        print(f"\nCross-model summary: {summary_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exp 02a: Premature Compression — Bedrock New-Model Replication"
    )
    parser.add_argument("--model-id", help="Single Bedrock model ID to test")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run")
    parser.add_argument("--max-tasks", type=int, help="Limit number of tasks")
    args = parser.parse_args()

    run_experiment(args.model_id, args.dry_run, args.max_tasks)
