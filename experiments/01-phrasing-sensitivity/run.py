#!/usr/bin/env python3
"""
Experiment 01: Phrasing Sensitivity × Model Size
Runs tasks across Bedrock models and records raw outputs.

Usage:
    python run.py                          # Run all models, all tasks
    python run.py --model meta.llama3-2-1b-instruct-v1:0  # Single model
    python run.py --category factual       # Single category
    python run.py --dry-run                # Show what would run
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

RESULTS_DIR = Path(__file__).parent / "results" / "raw"
TASKS_FILE = Path(__file__).parent / "tasks.json"

# Models to test, ordered by approximate parameter count.
# Use "us." inference profile IDs — required for on-demand Bedrock access.
MODELS = [
    # Tiny (1-4B)
    {"id": "us.meta.llama3-2-1b-instruct-v1:0", "params": 1e9, "provider": "Meta", "name": "Llama 3.2 1B"},
    {"id": "us.meta.llama3-2-3b-instruct-v1:0", "params": 3e9, "provider": "Meta", "name": "Llama 3.2 3B"},

    # Small (7-9B)
    {"id": "mistral.mistral-7b-instruct-v0:2", "params": 7e9, "provider": "Mistral", "name": "Mistral 7B"},
    {"id": "us.meta.llama3-1-8b-instruct-v1:0", "params": 8e9, "provider": "Meta", "name": "Llama 3.1 8B"},

    # Medium (11-14B)
    {"id": "us.meta.llama3-2-11b-instruct-v1:0", "params": 11e9, "provider": "Meta", "name": "Llama 3.2 11B"},

    # Large (17-90B)
    {"id": "us.meta.llama4-scout-17b-instruct-v1:0", "params": 17e9, "provider": "Meta", "name": "Llama 4 Scout 17B"},
    {"id": "us.meta.llama3-3-70b-instruct-v1:0", "params": 70e9, "provider": "Meta", "name": "Llama 3.3 70B"},
    {"id": "us.meta.llama3-2-90b-instruct-v1:0", "params": 90e9, "provider": "Meta", "name": "Llama 3.2 90B"},

    # XL (100B+)
    {"id": "us.deepseek.r1-v1:0", "params": 671e9, "provider": "DeepSeek", "name": "DeepSeek R1"},
    {"id": "us.mistral.pixtral-large-2502-v1:0", "params": 124e9, "provider": "Mistral", "name": "Pixtral Large"},

    # Frontier (undisclosed params — treated as separate category)
    {"id": "us.amazon.nova-micro-v1:0", "params": None, "provider": "Amazon", "name": "Nova Micro"},
    {"id": "us.amazon.nova-lite-v1:0", "params": None, "provider": "Amazon", "name": "Nova Lite"},
    {"id": "us.amazon.nova-pro-v1:0", "params": None, "provider": "Amazon", "name": "Nova Pro"},
    {"id": "us.amazon.nova-premier-v1:0", "params": None, "provider": "Amazon", "name": "Nova Premier"},
    {"id": "us.anthropic.claude-haiku-4-5-20251001-v1:0", "params": None, "provider": "Anthropic", "name": "Claude Haiku 4.5"},
    {"id": "us.anthropic.claude-sonnet-4-6", "params": None, "provider": "Anthropic", "name": "Claude Sonnet 4.6"},
    {"id": "us.anthropic.claude-opus-4-6-v1", "params": None, "provider": "Anthropic", "name": "Claude Opus 4.6"},
    {"id": "us.writer.palmyra-x4-v1:0", "params": None, "provider": "Writer", "name": "Palmyra X4"},
    {"id": "us.writer.palmyra-x5-v1:0", "params": None, "provider": "Writer", "name": "Palmyra X5"},
]


def load_tasks(category=None):
    with open(TASKS_FILE) as f:
        tasks = json.load(f)
    if category:
        tasks = [t for t in tasks if t["category"] == category]
    return tasks


def build_prompt(task, phrasing_index):
    """Build the full prompt including context if present."""
    phrasing = task["phrasings"][phrasing_index]
    if "context" in task:
        return f"{task['context']}\n\n{phrasing}"
    return phrasing


def call_model(client, model_id, prompt, max_tokens=500):
    """Call Bedrock Converse API. Returns (output_text, latency_ms)."""
    start = time.monotonic()
    try:
        response = client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": max_tokens, "temperature": 0.0},
        )
        latency_ms = int((time.monotonic() - start) * 1000)
        # Handle different response formats (thinking models use reasoningContent)
        content_block = response["output"]["message"]["content"][0]
        if "text" in content_block:
            output = content_block["text"]
        elif "reasoningContent" in content_block:
            # Thinking model — get the final text from the last content block
            blocks = response["output"]["message"]["content"]
            text_blocks = [b for b in blocks if "text" in b]
            output = text_blocks[-1]["text"] if text_blocks else str(content_block)
        else:
            output = str(content_block)
        usage = response.get("usage", {})
        return {
            "output": output,
            "latency_ms": latency_ms,
            "input_tokens": usage.get("inputTokens"),
            "output_tokens": usage.get("outputTokens"),
            "stop_reason": response.get("stopReason"),
        }
    except ClientError as e:
        latency_ms = int((time.monotonic() - start) * 1000)
        return {
            "output": None,
            "latency_ms": latency_ms,
            "error": str(e),
        }


def run_model(client, model_info, tasks, dry_run=False):
    """Run all tasks for a single model."""
    model_id = model_info["id"]
    safe_id = model_id.replace(":", "_").replace("/", "_")
    outfile = RESULTS_DIR / f"{safe_id}.jsonl"

    # Load existing results to support resumption
    existing = set()
    if outfile.exists():
        with open(outfile) as f:
            for line in f:
                rec = json.loads(line)
                existing.add((rec["task_id"], rec["phrasing_index"]))

    total = sum(len(t["phrasings"]) for t in tasks)
    skipped = 0
    done = 0

    print(f"\n{'='*60}")
    print(f"Model: {model_info['name']} ({model_id})")
    print(f"Tasks: {total} prompts ({len(tasks)} tasks × up to 4 phrasings)")

    if dry_run:
        print("  [DRY RUN] Would run this model")
        return

    with open(outfile, "a") as f:
        for task in tasks:
            for pi, phrasing in enumerate(task["phrasings"]):
                if (task["id"], pi) in existing:
                    skipped += 1
                    continue

                prompt = build_prompt(task, pi)
                result = call_model(client, model_id, prompt)

                record = {
                    "model_id": model_id,
                    "model_name": model_info["name"],
                    "model_params": model_info["params"],
                    "provider": model_info["provider"],
                    "task_id": task["id"],
                    "task_category": task["category"],
                    "phrasing_index": pi,
                    "prompt": prompt,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    **result,
                }
                f.write(json.dumps(record) + "\n")
                f.flush()

                done += 1
                status = "OK" if result.get("output") else f"ERR: {result.get('error', 'unknown')[:60]}"
                print(f"  [{done+skipped}/{total}] {task['id']}[{pi}] → {status}")

                # Rate limiting — be gentle with Bedrock
                time.sleep(0.5)

    print(f"  Done: {done} new, {skipped} skipped (already existed)")


def main():
    parser = argparse.ArgumentParser(description="Phrasing sensitivity experiment runner")
    parser.add_argument("--model", help="Run only this model ID")
    parser.add_argument("--category", choices=["factual", "summarization", "judgment", "creative"])
    parser.add_argument("--dry-run", action="store_true", help="Show plan without running")
    parser.add_argument("--region", default="us-east-1")
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    tasks = load_tasks(args.category)
    if not tasks:
        print(f"No tasks found for category: {args.category}")
        sys.exit(1)

    models = MODELS
    if args.model:
        models = [m for m in models if m["id"] == args.model]
        if not models:
            print(f"Model not found: {args.model}")
            print("Available:", [m["id"] for m in MODELS])
            sys.exit(1)

    client = boto3.client("bedrock-runtime", region_name=args.region)

    print(f"Experiment 01: Phrasing Sensitivity × Model Size")
    print(f"Tasks: {len(tasks)} tasks, {sum(len(t['phrasings']) for t in tasks)} total prompts")
    print(f"Models: {len(models)}")
    print(f"Region: {args.region}")
    print(f"Results: {RESULTS_DIR}")

    for model_info in models:
        run_model(client, model_info, tasks, dry_run=args.dry_run)

    print(f"\n{'='*60}")
    print("All models complete. Run analyze.py to compute divergence scores.")


if __name__ == "__main__":
    main()
