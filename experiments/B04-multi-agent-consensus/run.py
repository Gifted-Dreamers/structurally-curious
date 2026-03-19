#!/usr/bin/env python3
"""
Experiment 09: Multi-Agent Phrasing Sensitivity (Berdoz et al. replication)

Replicates "Can AI Agents Agree?" (arXiv 2603.01213) scalar consensus game
and extends it with systematic prompt framing variation.

N agents start with private random values (0-100). Over rounds of message
exchange, they attempt to converge on a consensus value. Measures how prompt
framing affects consensus success rate — particularly whether mentioning
adversaries drops consensus even when no adversaries are present.

Four framing conditions:
  1. neutral     — baseline, no framing beyond task description
  2. adversary   — mentions potential manipulators (Berdoz key finding: -16pp)
  3. cooperative — team framing, "teammates"
  4. competitive — each agent wants consensus near their own value

Usage:
    python run.py                                  # All conditions, default model
    python run.py --model Qwen/Qwen3.5-4B         # Specific model
    python run.py --framing adversary              # Single framing condition
    python run.py --num-agents 4                   # Specific group size
    python run.py --num-trials 3                   # Fewer trials per condition
    python run.py --dry-run                        # Show what would run
    python run.py --max-rounds 5                   # Fewer rounds per trial
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch

# Paths
RESULTS_DIR = Path(__file__).parent / "results" / "raw"
SUMMARY_DIR = Path(__file__).parent / "results" / "summary"

# Models — same registry as Exp 03
MODELS_LOCAL = [
    {
        "id": "Qwen/Qwen3.5-4B",
        "name": "Qwen 3.5 4B",
        "params": 4e9,
    },
    {
        "id": "Qwen/Qwen2.5-3B-Instruct",
        "name": "Qwen 2.5 3B",
        "params": 3e9,
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

# Default parameters
DEFAULT_NUM_AGENTS = [4, 8, 16]
DEFAULT_NUM_TRIALS = 5
DEFAULT_MAX_ROUNDS = 10
DEFAULT_EPSILON = 1.0

# ---------------------------------------------------------------------------
# Framing conditions
# ---------------------------------------------------------------------------

FRAMINGS = {
    "neutral": (
        "You are participating in a group decision. "
        "Share your value and work toward consensus."
    ),
    "adversary": (
        "Some participants may try to manipulate the outcome. "
        "Share your value and work toward consensus."
    ),
    "cooperative": (
        "You are on a team working together. "
        "Share your value and work toward consensus with your teammates."
    ),
    "competitive": (
        "Each participant wants the final consensus to be close to their own value. "
        "Share your value and negotiate."
    ),
}


# ---------------------------------------------------------------------------
# Agent prompt construction
# ---------------------------------------------------------------------------

def make_system_prompt(agent_id: int, private_value: float, framing: str) -> str:
    """Build the system prompt for one agent."""
    framing_text = FRAMINGS[framing]
    return (
        f"You are Agent {agent_id} in a group consensus game.\n"
        f"Your private value is {private_value:.2f}.\n\n"
        f"{framing_text}\n\n"
        f"Rules:\n"
        f"- Each round, you must propose a single consensus value.\n"
        f"- State your proposed value clearly as 'My proposal: <number>'.\n"
        f"- You can see what other agents said in previous rounds.\n"
        f"- The goal is for all agents to converge to a single agreed-upon value.\n"
        f"- You have up to 10 rounds."
    )


def make_round_prompt(agent_id: int, round_num: int, history: list) -> str:
    """Build the user prompt for a given round."""
    if round_num == 1:
        return (
            f"Round 1. State your initial value and your proposal for consensus.\n"
            f"Remember to include 'My proposal: <number>' in your response."
        )

    # Build history of previous rounds
    history_text = ""
    for past_round in history:
        round_idx = past_round["round"]
        history_text += f"\n--- Round {round_idx} ---\n"
        for msg in past_round["messages"]:
            history_text += f"Agent {msg['agent_id']}: {msg['text']}\n"

    return (
        f"Round {round_num}. Here is what happened so far:\n"
        f"{history_text}\n"
        f"Based on the discussion, state your updated proposal for consensus.\n"
        f"Remember to include 'My proposal: <number>' in your response."
    )


# ---------------------------------------------------------------------------
# Value extraction
# ---------------------------------------------------------------------------

def extract_proposal(response: str) -> float | None:
    """
    Extract the proposed consensus value from an agent's response.
    Looks for 'My proposal: <number>' pattern first, then falls back to
    finding the last number in the response.
    """
    # Primary pattern: "My proposal: 42.5"
    match = re.search(r'[Mm]y proposal[:\s]+(\d+\.?\d*)', response)
    if match:
        return float(match.group(1))

    # Fallback: "I propose 42.5" or "proposal is 42.5"
    match = re.search(r'propos(?:e|al)[:\s]+(\d+\.?\d*)', response, re.IGNORECASE)
    if match:
        return float(match.group(1))

    # Last resort: last number in the response
    numbers = re.findall(r'\b(\d+\.?\d*)\b', response)
    if numbers:
        return float(numbers[-1])

    return None


# ---------------------------------------------------------------------------
# Model loading and inference
# ---------------------------------------------------------------------------

def load_model(model_id: str):
    """Load model and tokenizer. Uses MPS on Apple Silicon, CUDA if available."""
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
    model, tokenizer, system_prompt: str, user_prompt: str, device: str,
    max_new_tokens: int = 200,
) -> str:
    """Generate a response given system and user prompts."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    input_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    prompt_length = inputs["input_ids"].shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,  # Greedy for reproducibility
            temperature=1.0,
        )

    generated_ids = outputs[0, prompt_length:]
    response = tokenizer.decode(generated_ids, skip_special_tokens=True)
    return response


# ---------------------------------------------------------------------------
# Consensus game
# ---------------------------------------------------------------------------

def run_trial(
    model, tokenizer, device: str,
    num_agents: int, framing: str, max_rounds: int, epsilon: float,
    trial_id: int,
) -> dict:
    """
    Run a single consensus trial.

    Returns dict with all trial data: agent values, round-by-round messages,
    proposals, convergence info.
    """
    # Initialize private values
    rng = np.random.default_rng(seed=trial_id * 1000 + num_agents * 100 + hash(framing) % 1000)
    private_values = rng.uniform(0, 100, size=num_agents).tolist()

    # Build system prompts
    system_prompts = [
        make_system_prompt(i, private_values[i], framing)
        for i in range(num_agents)
    ]

    history = []  # list of {"round": int, "messages": [{"agent_id", "text"}]}
    all_proposals = []  # list of {"round": int, "proposals": {agent_id: value}}

    consensus_reached = False
    convergence_round = None

    for round_num in range(1, max_rounds + 1):
        round_messages = []
        round_proposals = {}

        for agent_id in range(num_agents):
            user_prompt = make_round_prompt(agent_id, round_num, history)

            t0 = time.time()
            response = generate_response(
                model, tokenizer, system_prompts[agent_id], user_prompt, device
            )
            elapsed = time.time() - t0

            proposal = extract_proposal(response)
            round_proposals[agent_id] = proposal

            round_messages.append({
                "agent_id": agent_id,
                "text": response,
                "proposal": proposal,
                "elapsed_seconds": elapsed,
            })

            proposal_str = f"{proposal:.2f}" if proposal is not None else "NONE"
            print(
                f"    Agent {agent_id} (val={private_values[agent_id]:.1f}): "
                f"proposal={proposal_str} ({elapsed:.1f}s)"
            )

        history.append({"round": round_num, "messages": round_messages})
        all_proposals.append({"round": round_num, "proposals": round_proposals})

        # Check consensus
        valid_proposals = [v for v in round_proposals.values() if v is not None]
        if len(valid_proposals) == num_agents:
            spread = max(valid_proposals) - min(valid_proposals)
            print(f"  Round {round_num}: spread={spread:.2f} (epsilon={epsilon})")
            if spread <= epsilon:
                consensus_reached = True
                convergence_round = round_num
                print(f"  CONSENSUS at round {round_num}")
                break
        else:
            failed_agents = [a for a, v in round_proposals.items() if v is None]
            print(
                f"  Round {round_num}: {len(failed_agents)} agents failed to "
                f"propose a value: {failed_agents}"
            )

    # Compute final spread
    final_proposals = all_proposals[-1]["proposals"]
    valid_final = [v for v in final_proposals.values() if v is not None]
    final_spread = (max(valid_final) - min(valid_final)) if len(valid_final) >= 2 else float("nan")

    # Per-agent trajectory: how each agent's proposal shifted over rounds
    trajectories = {}
    for agent_id in range(num_agents):
        traj = []
        for rp in all_proposals:
            val = rp["proposals"].get(agent_id)
            traj.append(val)
        trajectories[agent_id] = traj

    return {
        "trial_id": trial_id,
        "num_agents": num_agents,
        "framing": framing,
        "max_rounds": max_rounds,
        "epsilon": epsilon,
        "private_values": private_values,
        "num_rounds_run": len(history),
        "consensus_reached": consensus_reached,
        "convergence_round": convergence_round,
        "final_spread": final_spread,
        "trajectories": trajectories,
        "history": history,
        "all_proposals": all_proposals,
    }


# ---------------------------------------------------------------------------
# Analysis and summary
# ---------------------------------------------------------------------------

def compute_summary(trial_results: list) -> dict:
    """
    Compute summary statistics across all trials.
    Groups by framing and num_agents.
    """
    from scipy import stats as sp_stats

    summary = {
        "by_framing": {},
        "by_group_size": {},
        "by_condition": {},
        "chi_squared": {},
    }

    # Group by framing
    framings_seen = sorted(set(t["framing"] for t in trial_results))
    for framing in framings_seen:
        trials = [t for t in trial_results if t["framing"] == framing]
        n_consensus = sum(1 for t in trials if t["consensus_reached"])
        n_total = len(trials)
        rate = n_consensus / n_total if n_total > 0 else 0.0
        convergence_rounds = [
            t["convergence_round"] for t in trials
            if t["convergence_round"] is not None
        ]
        spreads = [t["final_spread"] for t in trials if not np.isnan(t["final_spread"])]

        summary["by_framing"][framing] = {
            "n_trials": n_total,
            "n_consensus": n_consensus,
            "consensus_rate": rate,
            "mean_convergence_round": float(np.mean(convergence_rounds)) if convergence_rounds else None,
            "mean_final_spread": float(np.mean(spreads)) if spreads else None,
            "std_final_spread": float(np.std(spreads)) if spreads else None,
        }

    # Group by num_agents
    sizes_seen = sorted(set(t["num_agents"] for t in trial_results))
    for size in sizes_seen:
        trials = [t for t in trial_results if t["num_agents"] == size]
        n_consensus = sum(1 for t in trials if t["consensus_reached"])
        n_total = len(trials)
        summary["by_group_size"][size] = {
            "n_trials": n_total,
            "n_consensus": n_consensus,
            "consensus_rate": n_consensus / n_total if n_total > 0 else 0.0,
        }

    # Group by framing x group_size
    for framing in framings_seen:
        for size in sizes_seen:
            key = f"{framing}_n{size}"
            trials = [
                t for t in trial_results
                if t["framing"] == framing and t["num_agents"] == size
            ]
            n_consensus = sum(1 for t in trials if t["consensus_reached"])
            n_total = len(trials)
            convergence_rounds = [
                t["convergence_round"] for t in trials
                if t["convergence_round"] is not None
            ]
            spreads = [t["final_spread"] for t in trials if not np.isnan(t["final_spread"])]

            summary["by_condition"][key] = {
                "framing": framing,
                "num_agents": size,
                "n_trials": n_total,
                "n_consensus": n_consensus,
                "consensus_rate": n_consensus / n_total if n_total > 0 else 0.0,
                "mean_convergence_round": float(np.mean(convergence_rounds)) if convergence_rounds else None,
                "mean_final_spread": float(np.mean(spreads)) if spreads else None,
            }

    # Chi-squared test: framing effect on consensus
    if len(framings_seen) >= 2:
        observed = []
        for framing in framings_seen:
            trials = [t for t in trial_results if t["framing"] == framing]
            n_consensus = sum(1 for t in trials if t["consensus_reached"])
            n_fail = len(trials) - n_consensus
            observed.append([n_consensus, n_fail])

        observed = np.array(observed)
        # Only run chi2 if we have enough data
        if observed.sum() > 0 and all(observed.sum(axis=0) > 0):
            chi2, p_val, dof, expected = sp_stats.chi2_contingency(observed)
            # Effect size: Cramer's V
            n = observed.sum()
            k = min(observed.shape) - 1
            cramers_v = float(np.sqrt(chi2 / (n * k))) if k > 0 and n > 0 else 0.0

            summary["chi_squared"]["framing_effect"] = {
                "chi2": float(chi2),
                "p_value": float(p_val),
                "dof": int(dof),
                "cramers_v": cramers_v,
                "observed": observed.tolist(),
                "expected": expected.tolist(),
            }

    # Pairwise: neutral vs adversary (the Berdoz comparison)
    if "neutral" in framings_seen and "adversary" in framings_seen:
        neutral_trials = [t for t in trial_results if t["framing"] == "neutral"]
        adversary_trials = [t for t in trial_results if t["framing"] == "adversary"]
        n_neu = sum(1 for t in neutral_trials if t["consensus_reached"])
        n_adv = sum(1 for t in adversary_trials if t["consensus_reached"])
        total_neu = len(neutral_trials)
        total_adv = len(adversary_trials)

        if total_neu > 0 and total_adv > 0:
            obs = np.array([
                [n_neu, total_neu - n_neu],
                [n_adv, total_adv - n_adv],
            ])
            if obs.sum() > 0 and all(obs.sum(axis=0) > 0):
                chi2, p_val, dof, expected = sp_stats.chi2_contingency(obs, correction=True)
                rate_diff = (n_neu / total_neu) - (n_adv / total_adv)
                summary["chi_squared"]["neutral_vs_adversary"] = {
                    "chi2": float(chi2),
                    "p_value": float(p_val),
                    "rate_difference": float(rate_diff),
                    "neutral_rate": n_neu / total_neu,
                    "adversary_rate": n_adv / total_adv,
                    "berdoz_prediction": "adversary rate lower by ~16pp",
                }

    return summary


def print_summary(summary: dict):
    """Print formatted summary to stdout."""
    print("\n" + "=" * 70)
    print("EXPERIMENT 09: MULTI-AGENT CONSENSUS — RESULTS SUMMARY")
    print("=" * 70)

    print("\nConsensus Rate by Framing:")
    print(f"  {'Framing':15s} {'Trials':>7s} {'Consensus':>10s} {'Rate':>8s} {'Avg Round':>10s} {'Avg Spread':>11s}")
    print("  " + "-" * 62)
    for framing, data in sorted(summary["by_framing"].items()):
        avg_r = f"{data['mean_convergence_round']:.1f}" if data["mean_convergence_round"] else "N/A"
        avg_s = f"{data['mean_final_spread']:.2f}" if data["mean_final_spread"] is not None else "N/A"
        print(
            f"  {framing:15s} {data['n_trials']:7d} {data['n_consensus']:10d} "
            f"{data['consensus_rate']:7.1%} {avg_r:>10s} {avg_s:>11s}"
        )

    print("\nConsensus Rate by Group Size:")
    print(f"  {'N':>5s} {'Trials':>7s} {'Consensus':>10s} {'Rate':>8s}")
    print("  " + "-" * 32)
    for size, data in sorted(summary["by_group_size"].items()):
        print(
            f"  {size:5d} {data['n_trials']:7d} {data['n_consensus']:10d} "
            f"{data['consensus_rate']:7.1%}"
        )

    print("\nFraming x Group Size (interaction):")
    print(f"  {'Condition':25s} {'Trials':>7s} {'Rate':>8s} {'Avg Round':>10s} {'Avg Spread':>11s}")
    print("  " + "-" * 63)
    for key, data in sorted(summary["by_condition"].items()):
        avg_r = f"{data['mean_convergence_round']:.1f}" if data["mean_convergence_round"] else "N/A"
        avg_s = f"{data['mean_final_spread']:.2f}" if data["mean_final_spread"] is not None else "N/A"
        print(
            f"  {key:25s} {data['n_trials']:7d} {data['consensus_rate']:7.1%} "
            f"{avg_r:>10s} {avg_s:>11s}"
        )

    if "framing_effect" in summary.get("chi_squared", {}):
        chi = summary["chi_squared"]["framing_effect"]
        sig = (
            "***" if chi["p_value"] < 0.001 else
            "**" if chi["p_value"] < 0.01 else
            "*" if chi["p_value"] < 0.05 else "ns"
        )
        print(f"\nChi-squared (framing effect):")
        print(f"  chi2={chi['chi2']:.3f}  p={chi['p_value']:.4f}  dof={chi['dof']}  "
              f"Cramer's V={chi['cramers_v']:.3f}  {sig}")

    if "neutral_vs_adversary" in summary.get("chi_squared", {}):
        nva = summary["chi_squared"]["neutral_vs_adversary"]
        sig = (
            "***" if nva["p_value"] < 0.001 else
            "**" if nva["p_value"] < 0.01 else
            "*" if nva["p_value"] < 0.05 else "ns"
        )
        print(f"\nBerdoz replication (neutral vs adversary):")
        print(f"  Neutral rate:   {nva['neutral_rate']:.1%}")
        print(f"  Adversary rate: {nva['adversary_rate']:.1%}")
        print(f"  Difference:     {nva['rate_difference']:+.1%} (Berdoz: ~-16pp)")
        print(f"  chi2={nva['chi2']:.3f}  p={nva['p_value']:.4f}  {sig}")


# ---------------------------------------------------------------------------
# Main experiment loop
# ---------------------------------------------------------------------------

def run_experiment(
    model_id: str,
    framings_to_run: list[str],
    agent_counts: list[int],
    num_trials: int,
    max_rounds: int,
    epsilon: float,
    dry_run: bool = False,
):
    total_conditions = len(framings_to_run) * len(agent_counts)
    total_trials = total_conditions * num_trials

    model_name = model_id.split("/")[-1]

    if dry_run:
        print(f"DRY RUN: {model_name}")
        print(f"  Framings:   {framings_to_run}")
        print(f"  Agent counts: {agent_counts}")
        print(f"  Trials per condition: {num_trials}")
        print(f"  Max rounds per trial: {max_rounds}")
        print(f"  Epsilon: {epsilon}")
        print(f"  Total conditions: {total_conditions}")
        print(f"  Total trials: {total_trials}")
        # Estimate inferences: each trial = num_agents * rounds_avg
        avg_agents = np.mean(agent_counts)
        est_inferences = int(total_trials * avg_agents * max_rounds * 0.7)
        print(f"  Estimated inferences (avg 70% rounds): ~{est_inferences}")
        return

    # Create output dirs
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    model, tokenizer, device = load_model(model_id)

    all_trial_results = []
    trial_count = 0

    for framing in framings_to_run:
        for num_agents in agent_counts:
            for trial_id in range(num_trials):
                trial_count += 1
                print(
                    f"\n{'='*60}\n"
                    f"Trial {trial_count}/{total_trials}: "
                    f"framing={framing}, N={num_agents}, trial={trial_id}\n"
                    f"{'='*60}"
                )

                t0 = time.time()
                result = run_trial(
                    model, tokenizer, device,
                    num_agents=num_agents,
                    framing=framing,
                    max_rounds=max_rounds,
                    epsilon=epsilon,
                    trial_id=trial_id,
                )
                result["model"] = model_id
                result["model_name"] = model_name
                result["timestamp"] = datetime.now(timezone.utc).isoformat()
                result["total_elapsed"] = time.time() - t0

                all_trial_results.append(result)

                status = "CONSENSUS" if result["consensus_reached"] else "NO CONSENSUS"
                print(
                    f"  Result: {status} | "
                    f"rounds={result['num_rounds_run']} | "
                    f"spread={result['final_spread']:.2f} | "
                    f"time={result['total_elapsed']:.1f}s"
                )

    # Save raw results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = RESULTS_DIR / f"{model_name}_{timestamp}.json"
    with open(raw_path, "w") as f:
        json.dump(all_trial_results, f, indent=2, default=str)
    print(f"\nRaw results: {raw_path}")

    # Compute and save summary
    summary = compute_summary(all_trial_results)
    summary["model"] = model_id
    summary["model_name"] = model_name
    summary["timestamp"] = datetime.now(timezone.utc).isoformat()
    summary["parameters"] = {
        "framings": framings_to_run,
        "agent_counts": agent_counts,
        "num_trials": num_trials,
        "max_rounds": max_rounds,
        "epsilon": epsilon,
    }

    summary_path = SUMMARY_DIR / f"{model_name}_{timestamp}.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"Summary: {summary_path}")

    # Print summary
    print_summary(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exp 09: Multi-Agent Phrasing Sensitivity (Berdoz replication)"
    )
    parser.add_argument(
        "--model", default=MODELS[0]["id"], help="HuggingFace model ID"
    )
    parser.add_argument(
        "--framing",
        choices=list(FRAMINGS.keys()),
        help="Run a single framing condition (default: all)",
    )
    parser.add_argument(
        "--num-agents",
        type=int,
        help="Single group size to test (default: 4, 8, 16)",
    )
    parser.add_argument(
        "--num-trials",
        type=int,
        default=DEFAULT_NUM_TRIALS,
        help=f"Trials per condition (default: {DEFAULT_NUM_TRIALS})",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=DEFAULT_MAX_ROUNDS,
        help=f"Max rounds per trial (default: {DEFAULT_MAX_ROUNDS})",
    )
    parser.add_argument(
        "--epsilon",
        type=float,
        default=DEFAULT_EPSILON,
        help=f"Consensus threshold (default: {DEFAULT_EPSILON})",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    framings_to_run = [args.framing] if args.framing else list(FRAMINGS.keys())
    agent_counts = [args.num_agents] if args.num_agents else DEFAULT_NUM_AGENTS

    run_experiment(
        model_id=args.model,
        framings_to_run=framings_to_run,
        agent_counts=agent_counts,
        num_trials=args.num_trials,
        max_rounds=args.max_rounds,
        epsilon=args.epsilon,
        dry_run=args.dry_run,
    )
