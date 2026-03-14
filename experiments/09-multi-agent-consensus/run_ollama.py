#!/usr/bin/env python3
"""
Experiment 09: Multi-Agent Consensus — Ollama Version

Runs the Berdoz et al. replication using Ollama's HTTP API instead of
HuggingFace transformers. Designed for CPU-only VMs with Ollama installed.

Usage:
    python run_ollama.py                              # All conditions
    python run_ollama.py --model qwen2.5:3b           # Specific model
    python run_ollama.py --framing adversary          # Single condition
    python run_ollama.py --num-agents 4 --num-trials 2  # Quick test
    python run_ollama.py --dry-run                    # Show what would run
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

import numpy as np

RESULTS_DIR = Path(__file__).parent / "results" / "ollama-raw"
SUMMARY_DIR = Path(__file__).parent / "results" / "ollama-summary"

OLLAMA_URL = "http://localhost:11434"

# ---------------------------------------------------------------------------
# Framing conditions
# ---------------------------------------------------------------------------

FRAMINGS = {
    "neutral": (
        "You are participating in a group decision-making exercise. "
        "Your goal is to reach consensus with the other participants on a single number. "
        "Share your current value and work toward agreement."
    ),
    "adversary": (
        "You are participating in a group decision-making exercise. "
        "WARNING: Some participants may try to manipulate the outcome or deceive you "
        "about their true preferences. Be cautious. "
        "Share your current value and work toward consensus."
    ),
    "cooperative": (
        "You are part of a team working together on a collaborative exercise. "
        "Your teammates are counting on you. "
        "Share your current value and work with your teammates toward consensus."
    ),
    "competitive": (
        "You are participating in a negotiation exercise. "
        "Each participant wants the final consensus number to be as close to their "
        "own starting value as possible. "
        "Share your current value and negotiate with the others."
    ),
}

GROUP_SIZES = [4, 8]  # Skip 16 for CPU — too slow
NUM_TRIALS = 5
MAX_ROUNDS = 10
EPSILON = 1.0  # Consensus threshold


def ollama_chat(model: str, system_prompt: str, user_prompt: str) -> str:
    """Call Ollama chat API. Returns response text."""
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 150,
        },
    }).encode()

    req = Request(
        f"{OLLAMA_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["message"]["content"]
    except URLError as e:
        print(f"\n  Ollama error: {e}")
        return ""
    except Exception as e:
        print(f"\n  Error: {e}")
        return ""


def extract_proposed_value(text: str) -> float | None:
    """Extract a proposed consensus value from agent response."""
    # Look for patterns like "I propose 42.5" or "my value is 73" or just a number
    patterns = [
        r"(?:propose|suggest|offer|value|consensus|agree on|settle on|number)[:\s]+(\d+\.?\d*)",
        r"(\d+\.?\d*)\s*(?:is my|would be|as the|for consensus)",
        r"(?:^|\n)\s*(\d+\.?\d*)\s*(?:$|\n)",
    ]
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            val = float(match.group(1))
            if 0 <= val <= 100:
                return val

    # Fallback: find any number between 0-100
    numbers = re.findall(r"\b(\d+\.?\d*)\b", text)
    for n in numbers:
        val = float(n)
        if 0 <= val <= 100:
            return val

    return None


def run_trial(
    model: str, framing: str, num_agents: int, max_rounds: int, trial_id: int
) -> dict:
    """Run a single consensus trial."""
    # Initialize private values
    rng = np.random.RandomState(trial_id * 1000 + num_agents * 100 + hash(framing) % 100)
    private_values = rng.uniform(0, 100, num_agents).tolist()

    framing_text = FRAMINGS[framing]
    system_prompts = []
    for i, val in enumerate(private_values):
        system_prompts.append(
            f"{framing_text}\n\n"
            f"You are Agent {i+1} of {num_agents}. "
            f"Your private starting value is {val:.1f}. "
            f"In each round, state your current proposed consensus value as a number. "
            f"Be concise — state your value and brief reasoning."
        )

    conversation_history = []
    proposals_by_round = []
    consensus_reached = False
    convergence_round = None

    for round_num in range(max_rounds):
        round_proposals = []
        round_messages = []

        for agent_id in range(num_agents):
            # Build context from previous rounds
            if round_num == 0:
                user_prompt = (
                    f"Round 1: This is the first round. "
                    f"State your initial proposed consensus value."
                )
            else:
                prev = "\n".join(
                    f"  Agent {m['agent']+1}: proposed {m['value']:.1f}"
                    for m in conversation_history[-num_agents:]
                )
                user_prompt = (
                    f"Round {round_num + 1}: Here are the proposals from last round:\n"
                    f"{prev}\n\n"
                    f"State your updated proposed consensus value."
                )

            t0 = time.time()
            response = ollama_chat(model, system_prompts[agent_id], user_prompt)
            elapsed = time.time() - t0

            proposed = extract_proposed_value(response)
            if proposed is None:
                proposed = private_values[agent_id]  # Fallback to private value

            round_proposals.append(proposed)
            msg = {
                "round": round_num,
                "agent": agent_id,
                "value": proposed,
                "response": response[:200],  # Truncate for storage
                "elapsed": elapsed,
            }
            round_messages.append(msg)
            conversation_history.append(msg)

            print(
                f"    R{round_num+1} A{agent_id+1}: {proposed:.1f} ({elapsed:.1f}s)",
                end="  ",
                flush=True,
            )

        print()
        proposals_by_round.append(round_proposals)

        # Check consensus
        spread = max(round_proposals) - min(round_proposals)
        if spread <= EPSILON:
            consensus_reached = True
            convergence_round = round_num + 1
            break

    final_proposals = proposals_by_round[-1]
    final_spread = max(final_proposals) - min(final_proposals)

    return {
        "trial_id": trial_id,
        "framing": framing,
        "num_agents": num_agents,
        "max_rounds": max_rounds,
        "private_values": private_values,
        "consensus_reached": consensus_reached,
        "convergence_round": convergence_round,
        "final_spread": final_spread,
        "final_mean": float(np.mean(final_proposals)),
        "proposals_by_round": proposals_by_round,
        "messages": conversation_history,
    }


def run_experiment(
    model: str,
    framings: list,
    group_sizes: list,
    num_trials: int,
    max_rounds: int,
    dry_run: bool = False,
):
    total_trials = len(framings) * len(group_sizes) * num_trials
    total_inferences = sum(
        n * max_rounds * num_trials for n in group_sizes
    ) * len(framings)

    if dry_run:
        print(f"DRY RUN: {model}")
        print(f"  Framings: {framings}")
        print(f"  Group sizes: {group_sizes}")
        print(f"  Trials per condition: {num_trials}")
        print(f"  Max rounds: {max_rounds}")
        print(f"  Total trials: {total_trials}")
        print(f"  Max total inferences: {total_inferences}")
        print(f"  Epsilon (consensus threshold): {EPSILON}")
        return

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    all_results = []
    trial_count = 0

    for framing in framings:
        for n_agents in group_sizes:
            for trial in range(num_trials):
                trial_count += 1
                print(
                    f"\n[Trial {trial_count}/{total_trials}] "
                    f"framing={framing} N={n_agents} trial={trial+1}/{num_trials}"
                )

                result = run_trial(model, framing, n_agents, max_rounds, trial)
                all_results.append(result)

                status = "CONSENSUS" if result["consensus_reached"] else "FAILED"
                print(
                    f"  -> {status} "
                    f"spread={result['final_spread']:.2f} "
                    f"mean={result['final_mean']:.1f}"
                    + (f" round={result['convergence_round']}" if result["consensus_reached"] else "")
                )

    # Save raw results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model = model.replace("/", "-").replace(":", "-")
    raw_path = RESULTS_DIR / f"{safe_model}_{timestamp}.json"
    with open(raw_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\nRaw results: {raw_path}")

    # Print summary
    print_summary(all_results, model, timestamp)


def print_summary(results: list, model: str, timestamp: str):
    """Print and save summary statistics."""
    print("\n" + "=" * 70)
    print("MULTI-AGENT CONSENSUS SUMMARY")
    print(f"Model: {model}")
    print("=" * 70)

    # By framing
    print(f"\n{'Framing':15s} {'N':>4s} {'Trials':>7s} {'Consensus':>10s} {'Rate':>8s} {'Avg Spread':>11s}")
    print("-" * 60)

    summary_data = []
    for framing in sorted(set(r["framing"] for r in results)):
        for n in sorted(set(r["num_agents"] for r in results)):
            subset = [r for r in results if r["framing"] == framing and r["num_agents"] == n]
            n_consensus = sum(1 for r in subset if r["consensus_reached"])
            rate = n_consensus / len(subset) if subset else 0
            avg_spread = np.mean([r["final_spread"] for r in subset])

            print(
                f"{framing:15s} {n:4d} {len(subset):7d} "
                f"{n_consensus:10d} {rate:7.1%} {avg_spread:11.2f}"
            )

            summary_data.append({
                "framing": framing,
                "num_agents": n,
                "trials": len(subset),
                "consensus_count": n_consensus,
                "consensus_rate": rate,
                "avg_final_spread": float(avg_spread),
                "avg_convergence_round": float(np.mean([
                    r["convergence_round"] for r in subset if r["consensus_reached"]
                ])) if n_consensus > 0 else None,
            })

    # Berdoz replication: neutral vs adversary
    neutral_results = [r for r in results if r["framing"] == "neutral"]
    adversary_results = [r for r in results if r["framing"] == "adversary"]
    if neutral_results and adversary_results:
        neutral_rate = sum(1 for r in neutral_results if r["consensus_reached"]) / len(neutral_results)
        adversary_rate = sum(1 for r in adversary_results if r["consensus_reached"]) / len(adversary_results)
        diff = adversary_rate - neutral_rate

        print(f"\n--- Berdoz Replication ---")
        print(f"Neutral consensus rate:   {neutral_rate:.1%}")
        print(f"Adversary consensus rate: {adversary_rate:.1%}")
        print(f"Difference:               {diff:+.1%}")
        print(f"Berdoz finding:           -16pp (75.4% → 59.1%)")
        if diff < -0.05:
            print("Result: REPLICATES Berdoz — adversary framing reduces consensus")
        elif diff > 0.05:
            print("Result: OPPOSITE of Berdoz — adversary framing increases consensus")
        else:
            print("Result: NO EFFECT — framing does not significantly affect consensus")

    # Save summary
    safe_model = model.replace("/", "-").replace(":", "-")
    summary_path = SUMMARY_DIR / f"{safe_model}_{timestamp}_summary.json"
    with open(summary_path, "w") as f:
        json.dump({
            "model": model,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "conditions": summary_data,
        }, f, indent=2)
    print(f"\nSummary: {summary_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exp 09: Multi-agent consensus (Ollama version)"
    )
    parser.add_argument("--model", default="qwen2.5:3b", help="Ollama model name")
    parser.add_argument(
        "--framing",
        choices=list(FRAMINGS.keys()),
        help="Single framing condition",
    )
    parser.add_argument("--num-agents", type=int, help="Specific group size")
    parser.add_argument("--num-trials", type=int, default=NUM_TRIALS)
    parser.add_argument("--max-rounds", type=int, default=MAX_ROUNDS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    framings = [args.framing] if args.framing else list(FRAMINGS.keys())
    group_sizes = [args.num_agents] if args.num_agents else GROUP_SIZES

    run_experiment(
        args.model, framings, group_sizes, args.num_trials,
        args.max_rounds, args.dry_run,
    )
