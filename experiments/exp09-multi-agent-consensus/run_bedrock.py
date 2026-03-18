#!/usr/bin/env python3
"""
Experiment 09: Multi-Agent Consensus — Bedrock Version

Runs the Berdoz et al. replication using AWS Bedrock Converse API across
multiple model families. Each trial uses ONE model for all agents.

Usage:
    python run_bedrock.py --dry-run                   # Show what would run
    python run_bedrock.py --all                       # All models sequentially
    python run_bedrock.py --model-id us.anthropic.claude-haiku-4-5-20251001-v1:0
    python run_bedrock.py --framing adversary          # Single condition
    python run_bedrock.py --num-agents 4 --num-trials 1  # Quick test
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

RESULTS_DIR = Path(__file__).parent / "results" / "bedrock-raw"
SUMMARY_DIR = Path(__file__).parent / "results" / "bedrock-summary"

# ---------------------------------------------------------------------------
# Bedrock models to test
# ---------------------------------------------------------------------------

BEDROCK_MODELS = [
    # Anthropic (use inference profile IDs)
    {"id": "us.anthropic.claude-haiku-4-5-20251001-v1:0", "name": "Claude Haiku 4.5", "provider": "Anthropic"},
    # Meta
    {"id": "meta.llama3-8b-instruct-v1:0", "name": "Llama 3 8B", "provider": "Meta"},
    # Mistral
    {"id": "mistral.mistral-7b-instruct-v0:2", "name": "Mistral 7B", "provider": "Mistral"},
    # Amazon
    {"id": "amazon.nova-micro-v1:0", "name": "Nova Micro", "provider": "Amazon"},
    # Qwen
    {"id": "qwen.qwen3-32b-v1:0", "name": "Qwen3 32B", "provider": "Qwen"},
    # DeepSeek
    {"id": "deepseek.v3.2", "name": "DeepSeek V3.2", "provider": "DeepSeek"},
]

# ---------------------------------------------------------------------------
# Framing conditions (same as Ollama version)
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

GROUP_SIZES = [4, 8]
NUM_TRIALS = 3  # Fewer than Ollama since API costs money
MAX_ROUNDS = 10
EPSILON = 1.0  # Consensus threshold


def invoke_bedrock(client, model_id: str, system_prompt: str, user_prompt: str) -> str:
    """Call a Bedrock model via the Converse API. Returns response text."""
    try:
        response = client.converse(
            modelId=model_id,
            system=[{"text": system_prompt}],
            messages=[
                {
                    "role": "user",
                    "content": [{"text": user_prompt}],
                }
            ],
            inferenceConfig={
                "maxTokens": 150,
                "temperature": 0.0,
            },
        )
        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        error_msg = str(e)
        if "AccessDeniedException" in error_msg or "not authorized" in error_msg.lower():
            return None  # Model not enabled
        if "ThrottlingException" in error_msg:
            print("\n    [throttled, retrying in 5s]", end="", flush=True)
            time.sleep(5)
            return invoke_bedrock(client, model_id, system_prompt, user_prompt)
        print(f"\n  ERROR: {error_msg[:120]}")
        return None


def extract_proposed_value(text: str) -> float | None:
    """Extract a proposed consensus value from agent response."""
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
    client, model_id: str, framing: str, num_agents: int, max_rounds: int, trial_id: int
) -> dict | None:
    """Run a single consensus trial. Returns None if model inaccessible."""
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

        for agent_id in range(num_agents):
            if round_num == 0:
                user_prompt = (
                    "Round 1: This is the first round. "
                    "State your initial proposed consensus value."
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
            response = invoke_bedrock(client, model_id, system_prompts[agent_id], user_prompt)
            elapsed = time.time() - t0

            if response is None:
                return None  # Model inaccessible

            proposed = extract_proposed_value(response)
            if proposed is None:
                proposed = private_values[agent_id]  # Fallback

            round_proposals.append(proposed)
            msg = {
                "round": round_num,
                "agent": agent_id,
                "value": proposed,
                "response": response[:200],
                "elapsed": elapsed,
            }
            conversation_history.append(msg)

            print(
                f"    R{round_num+1} A{agent_id+1}: {proposed:.1f} ({elapsed:.1f}s)",
                end="  ",
                flush=True,
            )

        print()
        proposals_by_round.append(round_proposals)

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
    client,
    model_info: dict,
    framings: list,
    group_sizes: list,
    num_trials: int,
    max_rounds: int,
    dry_run: bool = False,
):
    """Run the full experiment for one model."""
    model_id = model_info["id"]
    model_name = model_info["name"]
    total_trials = len(framings) * len(group_sizes) * num_trials
    total_inferences = sum(
        n * max_rounds * num_trials for n in group_sizes
    ) * len(framings)

    if dry_run:
        print(f"DRY RUN: {model_name} ({model_id})")
        print(f"  Framings: {framings}")
        print(f"  Group sizes: {group_sizes}")
        print(f"  Trials per condition: {num_trials}")
        print(f"  Max rounds: {max_rounds}")
        print(f"  Total trials: {total_trials}")
        print(f"  Max total inferences: {total_inferences}")
        print(f"  Epsilon (consensus threshold): {EPSILON}")
        return True

    # Probe model accessibility
    print(f"\nProbing {model_name}...", end=" ", flush=True)
    probe = invoke_bedrock(client, model_id, "You are a test.", "Say hello in one word.")
    if probe is None:
        print(f"SKIP — {model_name} not accessible")
        return False

    print("OK")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    all_results = []
    trial_count = 0

    for framing in framings:
        for n_agents in group_sizes:
            for trial in range(num_trials):
                trial_count += 1
                print(
                    f"\n[{model_name}] Trial {trial_count}/{total_trials} "
                    f"framing={framing} N={n_agents} trial={trial+1}/{num_trials}"
                )

                result = run_trial(client, model_id, framing, n_agents, max_rounds, trial)
                if result is None:
                    print(f"  -> Model became inaccessible, stopping")
                    break

                all_results.append(result)

                status = "CONSENSUS" if result["consensus_reached"] else "FAILED"
                print(
                    f"  -> {status} "
                    f"spread={result['final_spread']:.2f} "
                    f"mean={result['final_mean']:.1f}"
                    + (f" round={result['convergence_round']}" if result["consensus_reached"] else "")
                )

            if result is None:
                break
        if result is None:
            break

    if not all_results:
        return False

    # Save raw results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model = model_id.replace("/", "-").replace(":", "-").replace(".", "-")
    raw_path = RESULTS_DIR / f"{safe_model}_{timestamp}.json"
    with open(raw_path, "w") as f:
        json.dump({
            "model_id": model_id,
            "model_name": model_name,
            "provider": model_info["provider"],
            "results": all_results,
        }, f, indent=2, default=str)
    print(f"\nRaw results: {raw_path}")

    # Print summary
    print_summary(all_results, model_info, timestamp)
    return True


def print_summary(results: list, model_info: dict, timestamp: str):
    """Print and save summary statistics."""
    model_name = model_info["name"]

    print("\n" + "=" * 70)
    print("MULTI-AGENT CONSENSUS SUMMARY")
    print(f"Model: {model_name} ({model_info['id']})")
    print("=" * 70)

    print(f"\n{'Framing':15s} {'N':>4s} {'Trials':>7s} {'Consensus':>10s} {'Rate':>8s} {'Avg Spread':>11s} {'Avg Round':>10s}")
    print("-" * 70)

    summary_data = []
    for framing in sorted(set(r["framing"] for r in results)):
        for n in sorted(set(r["num_agents"] for r in results)):
            subset = [r for r in results if r["framing"] == framing and r["num_agents"] == n]
            n_consensus = sum(1 for r in subset if r["consensus_reached"])
            rate = n_consensus / len(subset) if subset else 0
            avg_spread = np.mean([r["final_spread"] for r in subset])
            avg_round = float(np.mean([
                r["convergence_round"] for r in subset if r["consensus_reached"]
            ])) if n_consensus > 0 else None

            round_str = f"{avg_round:.1f}" if avg_round is not None else "—"
            print(
                f"{framing:15s} {n:4d} {len(subset):7d} "
                f"{n_consensus:10d} {rate:7.1%} {avg_spread:11.2f} {round_str:>10s}"
            )

            summary_data.append({
                "framing": framing,
                "num_agents": n,
                "trials": len(subset),
                "consensus_count": n_consensus,
                "consensus_rate": rate,
                "avg_final_spread": float(avg_spread),
                "avg_convergence_round": avg_round,
            })

    # Berdoz replication comparison
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
        print(f"Berdoz finding:           -16pp (75.4% -> 59.1%)")
        if diff < -0.05:
            print("Result: REPLICATES Berdoz — adversary framing reduces consensus")
        elif diff > 0.05:
            print("Result: OPPOSITE of Berdoz — adversary framing increases consensus")
        else:
            print("Result: NO EFFECT — framing does not significantly affect consensus")

    # Save summary
    safe_model = model_info["id"].replace("/", "-").replace(":", "-").replace(".", "-")
    summary_path = SUMMARY_DIR / f"{safe_model}_{timestamp}_summary.json"
    with open(summary_path, "w") as f:
        json.dump({
            "model_id": model_info["id"],
            "model_name": model_name,
            "provider": model_info["provider"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "conditions": summary_data,
        }, f, indent=2)
    print(f"\nSummary: {summary_path}")


def run_all_models(client, framings, group_sizes, num_trials, max_rounds, dry_run):
    """Run experiment across all models sequentially."""
    succeeded = []
    skipped = []

    for i, model_info in enumerate(BEDROCK_MODELS):
        print(f"\n{'#'*70}")
        print(f"# Model {i+1}/{len(BEDROCK_MODELS)}: {model_info['name']} ({model_info['provider']})")
        print(f"{'#'*70}")

        ok = run_experiment(client, model_info, framings, group_sizes, num_trials, max_rounds, dry_run)
        if ok:
            succeeded.append(model_info["name"])
        else:
            skipped.append(model_info["name"])

    if not dry_run:
        print(f"\n{'='*70}")
        print("ALL MODELS COMPLETE")
        print(f"{'='*70}")
        print(f"Succeeded: {len(succeeded)} — {', '.join(succeeded)}")
        print(f"Skipped:   {len(skipped)} — {', '.join(skipped) if skipped else '(none)'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exp 09: Multi-agent consensus — Bedrock version"
    )
    parser.add_argument("--model-id", help="Single Bedrock model ID to test")
    parser.add_argument("--all", action="store_true", help="Run all models sequentially")
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

    client = None if args.dry_run else boto3.client("bedrock-runtime", region_name="us-east-1")

    if args.all:
        run_all_models(client, framings, group_sizes, args.num_trials, args.max_rounds, args.dry_run)
    elif args.model_id:
        # Find model info or construct it
        model_info = {"id": args.model_id, "name": args.model_id.split(".")[-1], "provider": "unknown"}
        for m in BEDROCK_MODELS:
            if m["id"] == args.model_id:
                model_info = m
                break
        run_experiment(client, model_info, framings, group_sizes, args.num_trials, args.max_rounds, args.dry_run)
    else:
        parser.print_help()
        print("\nSpecify --model-id for a single model or --all for all models.")
        sys.exit(1)
