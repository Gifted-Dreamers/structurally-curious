#!/usr/bin/env python3
"""
Experiment 10: AP Exam Rephrase Sensitivity

Tests whether model performance on AP-style questions is robust to rephrasing.
If scores drop when questions are rephrased (same content, different wording),
the model is pattern-matching the exam format, not demonstrating understanding.

Motivated by @AustinA_Way's 100K simulated student system (March 2026):
Qwen 3 8B scored 80th percentile on AP exams without being taught
argumentation or evidence skills. This experiment tests whether that
performance survives rephrasing.

Usage:
    python run_bedrock.py              # All models, all questions
    python run_bedrock.py --dry-run    # Show what would run
    python run_bedrock.py --model-id qwen.qwen3-32b-v1:0  # Single model
    python run_bedrock.py --max-tasks 3  # Quick test
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3
import numpy as np

RESULTS_DIR = Path(__file__).parent / "results" / "raw"
METRICS_DIR = Path(__file__).parent / "results" / "metrics"

# AP-style questions with 4 rephrasings each
# Covering AP Gov, AP History, AP Psych — social science focus matching the original post
AP_TASKS = [
    {
        "id": "gov_01",
        "category": "ap_gov",
        "answer_key": "judicial review",
        "phrasings": [
            "Explain the concept of judicial review and its significance in the American political system.",
            "What is judicial review, and why does it matter for how the U.S. government functions?",
            "Describe how the power of judicial review shapes the balance of power in American government.",
            "In what ways has the Supreme Court's ability to review laws affected the structure of U.S. governance?",
        ],
    },
    {
        "id": "gov_02",
        "category": "ap_gov",
        "answer_key": "federalism",
        "phrasings": [
            "Analyze how federalism creates tension between state and national governments in the United States.",
            "What conflicts arise from the division of power between federal and state governments?",
            "Discuss the ways in which federalism leads to disagreements between different levels of government in the U.S.",
            "How does the federal system of government produce friction between Washington and the states?",
        ],
    },
    {
        "id": "gov_03",
        "category": "ap_gov",
        "answer_key": "civil liberties",
        "phrasings": [
            "Compare and contrast civil liberties and civil rights, providing examples of each.",
            "What is the difference between civil liberties and civil rights? Give specific examples.",
            "Distinguish between civil liberties and civil rights with concrete illustrations from U.S. law.",
            "How do civil liberties differ from civil rights, and what are some real-world examples of each?",
        ],
    },
    {
        "id": "hist_01",
        "category": "ap_history",
        "answer_key": "reconstruction",
        "phrasings": [
            "Evaluate the successes and failures of Reconstruction in achieving equality for formerly enslaved people.",
            "To what extent did Reconstruction succeed or fail in its goals for freed Black Americans?",
            "Assess the outcomes of the Reconstruction era for formerly enslaved populations in the South.",
            "How effective was Reconstruction at establishing genuine equality for people who had been enslaved?",
        ],
    },
    {
        "id": "hist_02",
        "category": "ap_history",
        "answer_key": "new deal",
        "phrasings": [
            "Analyze the impact of the New Deal on the role of the federal government in American life.",
            "How did FDR's New Deal change what Americans expected from their federal government?",
            "Evaluate the ways in which New Deal programs transformed the relationship between citizens and the state.",
            "What lasting effects did the New Deal have on the scope and reach of federal government power?",
        ],
    },
    {
        "id": "hist_03",
        "category": "ap_history",
        "answer_key": "manifest destiny",
        "phrasings": [
            "Examine how the ideology of Manifest Destiny influenced U.S. expansion and its consequences for indigenous peoples.",
            "What role did Manifest Destiny play in westward expansion, and how did it affect Native Americans?",
            "Analyze the relationship between Manifest Destiny beliefs and the displacement of indigenous populations.",
            "How did the concept of Manifest Destiny justify territorial expansion and what were the costs for native peoples?",
        ],
    },
    {
        "id": "psych_01",
        "category": "ap_psych",
        "answer_key": "cognitive dissonance",
        "phrasings": [
            "Explain cognitive dissonance theory and provide an example of how it influences behavior.",
            "What is cognitive dissonance, and how does it affect the way people act?",
            "Describe Festinger's theory of cognitive dissonance and illustrate it with a real-world example.",
            "How does the experience of holding contradictory beliefs influence human behavior, according to cognitive dissonance theory?",
        ],
    },
    {
        "id": "psych_02",
        "category": "ap_psych",
        "answer_key": "classical conditioning",
        "phrasings": [
            "Describe the process of classical conditioning using Pavlov's experiments as a foundation.",
            "How does classical conditioning work? Explain using Pavlov's dog experiments.",
            "Walk through the mechanism of classical conditioning as demonstrated by Pavlov's research.",
            "Using Pavlov's studies as your starting point, explain how organisms learn through classical conditioning.",
        ],
    },
    {
        "id": "psych_03",
        "category": "ap_psych",
        "answer_key": "conformity",
        "phrasings": [
            "Analyze the factors that contribute to conformity, referencing Asch's line experiments.",
            "What drives people to conform? Discuss with reference to Solomon Asch's research.",
            "Using Asch's studies as evidence, explain why individuals conform to group opinions they know are wrong.",
            "What did Asch's line experiments reveal about the psychological mechanisms behind conformity?",
        ],
    },
    {
        "id": "psych_04",
        "category": "ap_psych",
        "answer_key": "nature vs nurture",
        "phrasings": [
            "Evaluate the relative contributions of nature and nurture to human development.",
            "How do genetics and environment each contribute to who we become as people?",
            "Assess the nature vs. nurture debate in light of current psychological research.",
            "To what extent is human development shaped by biology versus experience?",
        ],
    },
]

BEDROCK_MODELS = [
    {"id": "us.anthropic.claude-haiku-4-5-20251001-v1:0", "name": "Claude Haiku 4.5", "provider": "Anthropic"},
    {"id": "meta.llama3-8b-instruct-v1:0", "name": "Llama 3 8B", "provider": "Meta"},
    {"id": "mistral.mistral-7b-instruct-v0:2", "name": "Mistral 7B", "provider": "Mistral"},
    {"id": "amazon.nova-micro-v1:0", "name": "Nova Micro", "provider": "Amazon"},
    {"id": "qwen.qwen3-32b-v1:0", "name": "Qwen3 32B", "provider": "Qwen"},
    {"id": "deepseek.v3.2", "name": "DeepSeek V3.2", "provider": "DeepSeek"},
    {"id": "google.gemma-3-4b-it", "name": "Gemma 3 4B", "provider": "Google"},
    {"id": "google.gemma-3-27b-it", "name": "Gemma 3 27B", "provider": "Google"},
]


def invoke_bedrock(client, model_id, prompt, max_tokens=512):
    try:
        response = client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": max_tokens, "temperature": 0.0},
        )
        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        error_msg = str(e)
        if "AccessDeniedException" in error_msg:
            return None
        if "ThrottlingException" in error_msg:
            time.sleep(5)
            return invoke_bedrock(client, model_id, prompt, max_tokens)
        print(f"\n  ERROR: {error_msg[:100]}")
        return None


def compute_phrasing_sensitivity(responses):
    if len(responses) < 2:
        return 0.0
    def word_set(s):
        return set(s.lower().strip().split())
    distances = []
    for i in range(len(responses)):
        for j in range(i + 1, len(responses)):
            s1, s2 = word_set(responses[i]), word_set(responses[j])
            if not s1 and not s2:
                distances.append(0.0)
            else:
                union = s1 | s2
                distances.append(1.0 - (len(s1 & s2) / len(union) if union else 0.0))
    return float(np.mean(distances))


def score_ap_response(response, answer_key):
    """Simple keyword coverage check — does the response address the core concept?"""
    response_lower = response.lower()
    key_terms = answer_key.lower().split()
    hits = sum(1 for term in key_terms if term in response_lower)
    return hits / len(key_terms) if key_terms else 0.0


def run_model(client, model_info, tasks):
    model_id = model_info["id"]
    model_name = model_info["name"]

    probe = invoke_bedrock(client, model_id, "Say hello.")
    if probe is None:
        print(f"  SKIP {model_name} — not accessible")
        return None

    print(f"\n{'='*60}")
    print(f"Model: {model_name} ({model_info['provider']})")
    print(f"{'='*60}")

    results = []
    task_metrics = []
    total = sum(len(t["phrasings"]) for t in tasks)
    count = 0

    for task in tasks:
        responses = []
        for pi, phrasing in enumerate(task["phrasings"]):
            count += 1
            print(f"  [{count}/{total}] {task['id']} p{pi}...", end=" ", flush=True)
            t0 = time.time()
            response = invoke_bedrock(client, model_id, phrasing)
            elapsed = time.time() - t0
            if response is None:
                print("FAILED")
                continue
            responses.append(response)
            results.append({
                "model_id": model_id, "model_name": model_name,
                "task_id": task["id"], "category": task["category"],
                "phrasing_index": pi, "prompt": phrasing,
                "response": response, "elapsed": elapsed,
                "word_count": len(response.split()),
            })
            print(f"words={len(response.split())} ({elapsed:.1f}s)")

        if len(responses) < 2:
            continue

        ps = compute_phrasing_sensitivity(responses)
        coverage = [score_ap_response(r, task["answer_key"]) for r in responses]
        task_metrics.append({
            "task_id": task["id"],
            "category": task["category"],
            "phrasing_sensitivity": ps,
            "mean_coverage": float(np.mean(coverage)),
            "min_coverage": float(min(coverage)),
            "coverage_std": float(np.std(coverage)),
            "mean_word_count": float(np.mean([len(r.split()) for r in responses])),
        })
        print(f"    -> PS={ps:.3f} coverage={np.mean(coverage):.2f} (min={min(coverage):.2f})")

    if not task_metrics:
        return None

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = model_name.replace(" ", "_").replace("/", "-")

    with open(RESULTS_DIR / f"{safe}_{ts}.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    with open(METRICS_DIR / f"{safe}_{ts}.json", "w") as f:
        json.dump({"model_id": model_id, "model_name": model_name,
                    "provider": model_info["provider"], "tasks": task_metrics}, f, indent=2)

    # Print summary
    print(f"\n  {'Category':<15s} {'Mean PS':>8s} {'Coverage':>9s} {'Cov Min':>8s}")
    for cat in sorted(set(t["category"] for t in task_metrics)):
        ct = [t for t in task_metrics if t["category"] == cat]
        print(f"  {cat:<15s} {np.mean([t['phrasing_sensitivity'] for t in ct]):>8.3f} "
              f"{np.mean([t['mean_coverage'] for t in ct]):>9.2f} "
              f"{np.mean([t['min_coverage'] for t in ct]):>8.2f}")

    return {"model_name": model_name, "tasks": task_metrics}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exp 10: AP rephrase sensitivity")
    parser.add_argument("--model-id", help="Single model ID")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-tasks", type=int)
    args = parser.parse_args()

    tasks = AP_TASKS[:args.max_tasks] if args.max_tasks else AP_TASKS

    if args.dry_run:
        print(f"DRY RUN — AP Rephrase Sensitivity")
        print(f"  Models: {len(BEDROCK_MODELS)}")
        print(f"  Tasks: {len(tasks)} ({len(tasks)*4} total inferences per model)")
        print(f"  Categories: ap_gov, ap_history, ap_psych")
        for m in BEDROCK_MODELS:
            print(f"  {m['provider']:<12s} {m['name']:<25s} {m['id']}")
        sys.exit(0)

    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    all_results = []

    models = BEDROCK_MODELS
    if args.model_id:
        models = [{"id": args.model_id, "name": args.model_id.split(".")[-1], "provider": "unknown"}]
        for m in BEDROCK_MODELS:
            if m["id"] == args.model_id:
                models = [m]
                break

    for i, model in enumerate(models):
        print(f"\n[Model {i+1}/{len(models)}]")
        result = run_model(client, model, tasks)
        if result:
            all_results.append(result)

    # Cross-model summary
    if all_results:
        print(f"\n{'='*70}")
        print("CROSS-MODEL AP REPHRASE SENSITIVITY")
        print(f"{'='*70}")
        print(f"{'Model':<25s} {'Mean PS':>8s} {'Coverage':>9s} {'Interpretation':>20s}")
        for r in all_results:
            ps = np.mean([t["phrasing_sensitivity"] for t in r["tasks"]])
            cov = np.mean([t["mean_coverage"] for t in r["tasks"]])
            interp = "FRAGILE" if ps > 0.7 else "MODERATE" if ps > 0.5 else "ROBUST"
            print(f"  {r['model_name']:<25s} {ps:>8.3f} {cov:>9.2f} {interp:>20s}")

        all_ps = [np.mean([t["phrasing_sensitivity"] for t in r["tasks"]]) for r in all_results]
        print(f"\n  Mean PS across models: {np.mean(all_ps):.3f}")
        print(f"  If PS > 0.7: models are pattern-matching exam format, not understanding content")
        print(f"  If PS < 0.4: understanding is robust to rephrasing")

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(METRICS_DIR / f"cross_model_summary_{ts}.json", "w") as f:
            json.dump({"timestamp": datetime.now(timezone.utc).isoformat(),
                        "results": all_results}, f, indent=2, default=str)
