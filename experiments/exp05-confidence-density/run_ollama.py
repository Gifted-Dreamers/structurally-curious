#!/usr/bin/env python3
"""Exp 05: Confidence density via Ollama (local open-weight models)."""
import json, sys, time, re
from pathlib import Path
from urllib.request import urlopen, Request
import numpy as np
from run import compute_certainty_score, compute_phrasing_sensitivity, print_correlation_summary

TASKS_FILE = Path(__file__).parent.parent / "01-phrasing-sensitivity" / "tasks.json"
RESULTS_DIR = Path(__file__).parent / "results" / "ollama-metrics"
RAW_DIR = Path(__file__).parent / "results" / "ollama-raw"

def ollama_chat(model, prompt, max_tokens=256):
    payload = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False, "options": {"temperature": 0.0, "num_predict": max_tokens}}).encode()
    req = Request("http://localhost:11434/api/chat", data=payload, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())["message"]["content"]

def run(model="qwen2.5:7b"):
    with open(TASKS_FILE) as f:
        tasks = json.load(f)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    results, task_metrics = [], []
    total = sum(len(t["phrasings"]) for t in tasks)
    count = 0
    for task in tasks:
        responses, scores_list = [], []
        for pi, phrasing in enumerate(task["phrasings"]):
            count += 1
            prompt = (task.get("context", "") + "\n\n" + phrasing).strip()
            print(f"[{count}/{total}] {task['id']} p{pi}...", end=" ", flush=True)
            t0 = time.time()
            response = ollama_chat(model, prompt)
            elapsed = time.time() - t0
            scores = compute_certainty_score(response)
            responses.append(response)
            scores_list.append(scores)
            results.append({"model": model, "task_id": task["id"], "category": task["category"], "phrasing_index": pi, "prompt": prompt, "response": response, "scores": scores, "elapsed": elapsed})
            print(f"CS={scores['certainty_score']:+.4f} hi={scores['high_count']} hedge={scores['hedge_count']} words={scores['total_words']} ({elapsed:.1f}s)")
        ps = compute_phrasing_sensitivity(responses)
        avg = {"task_id": task["id"], "category": task["category"], "phrasing_sensitivity": ps,
               "mean_certainty_score": float(np.mean([s["certainty_score"] for s in scores_list])),
               "std_certainty_score": float(np.std([s["certainty_score"] for s in scores_list])),
               "mean_high_density": float(np.mean([s["high_density"] for s in scores_list])),
               "mean_hedge_density": float(np.mean([s["hedge_density"] for s in scores_list])),
               "mean_total_words": float(np.mean([s["total_words"] for s in scores_list])),
               "total_high_markers": sum(s["high_count"] for s in scores_list),
               "total_hedge_markers": sum(s["hedge_count"] for s in scores_list)}
        task_metrics.append(avg)
        print(f"  -> PS={ps:.3f} CS={avg['mean_certainty_score']:+.4f}")
    from datetime import datetime, timezone
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = model.replace("/", "-").replace(":", "-")
    with open(RAW_DIR / f"{safe}_{ts}.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    with open(RESULTS_DIR / f"{safe}_{ts}.json", "w") as f:
        json.dump({"model": model, "model_name": model, "provider": "Ollama", "tasks": task_metrics}, f, indent=2)
    print_correlation_summary(task_metrics)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="qwen2.5:7b")
    run(p.parse_args().model)
