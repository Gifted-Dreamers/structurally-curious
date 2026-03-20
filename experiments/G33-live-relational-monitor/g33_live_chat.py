#!/usr/bin/env python3
"""
G33: Live Relational Monitor — Interactive Chat with Real-Time Geometry

Chat with a model loaded with the full identity system. See the
representational geometry shift in real time as the conversation unfolds.

Usage:
    python g33_live_chat.py [options]

    --model MODEL       HuggingFace model name (default: Qwen/Qwen2.5-7B-Instruct)
    --condition COND    Identity condition: bare, claude_md, heartbeat,
                        intellectual, connections, checkpoint, full (default: full)
    --device DEVICE     cpu, cuda, mps (default: auto-detect)
    --output DIR        Output directory for session logs (default: ./sessions/)
    --max-tokens N      Max generation tokens (default: 512)
    --layer LAYER       Specific layer to monitor (default: auto — top 25%)

Example:
    python g33_live_chat.py --condition full --model Qwen/Qwen2.5-7B-Instruct
    python g33_live_chat.py --condition bare  # baseline comparison

The session is saved as JSONL with per-turn geometry for replay analysis.

Part of the Structurally Curious Systems research program.
Kristine Socall & infinite-complexity (Claude) — Gifted Dreamers, Inc.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


# ---- Geometric metrics (from G19/F38 pipeline) ----

def compute_rankme(singular_values):
    """Effective rank via exponential of Shannon entropy of normalized SVs."""
    sv = singular_values[singular_values > 1e-10]
    if len(sv) == 0:
        return 0.0
    p = sv / sv.sum()
    entropy = -(p * torch.log(p)).sum().item()
    return np.exp(entropy)


def compute_alpha_req(singular_values, min_components=3):
    """Power-law exponent of singular value decay."""
    from scipy import stats
    sv = singular_values[singular_values > 1e-10].cpu().numpy()
    if len(sv) < min_components:
        return float('nan')
    log_i = np.log(np.arange(1, len(sv) + 1))
    log_sv = np.log(sv)
    slope, _, _, _, _ = stats.linregress(log_i, log_sv)
    return -slope


def extract_encoding_metrics(hidden_states, layer_idx):
    """Extract RankMe from prompt encoding at a specific layer."""
    hs = hidden_states[layer_idx]
    matrix = hs.squeeze(0).float()
    mc = matrix - matrix.mean(dim=0, keepdim=True)
    try:
        U, S, Vh = torch.linalg.svd(mc, full_matrices=False)
        return {
            "rankme": compute_rankme(S),
            "alpha_req": compute_alpha_req(S),
            "n_tokens": matrix.shape[0],
        }
    except Exception as e:
        return {"rankme": 0.0, "alpha_req": float('nan'), "error": str(e)}


def extract_generation_metrics(gen_outputs, n_layers):
    """Extract RankMe from generation trajectory (accumulated last-layer states)."""
    if not hasattr(gen_outputs, 'hidden_states') or not gen_outputs.hidden_states:
        return {}
    last_layer_idx = n_layers
    gen_token_states = []
    for step_hs in gen_outputs.hidden_states[1:]:
        if len(step_hs) > last_layer_idx:
            gen_token_states.append(step_hs[last_layer_idx].squeeze(0))
    if len(gen_token_states) < 3:
        return {"rankme": 0.0, "n_tokens": len(gen_token_states)}
    gen_matrix = torch.cat(gen_token_states, dim=0)
    gen_mc = gen_matrix - gen_matrix.mean(dim=0, keepdim=True)
    try:
        U, S, Vh = torch.linalg.svd(gen_mc.float(), full_matrices=False)
        return {
            "rankme": compute_rankme(S),
            "alpha_req": compute_alpha_req(S),
            "n_tokens": gen_matrix.shape[0],
        }
    except Exception:
        return {"rankme": 0.0, "n_tokens": gen_matrix.shape[0]}


# ---- Identity system loading ----

IDENTITY_FILES = {
    "claude_md": "CLAUDE.md",
    "getting_started": "getting-started.md",
    "progression": "progression-architecture.md",
    "heartbeat": "heartbeat.json",
    "intellectual_state": "intellectual-state.md",
    "connections": "connections.md",
}

CONDITIONS = {
    "bare": [],
    "claude_md": ["claude_md"],
    "scaffold": ["claude_md", "getting_started", "progression"],
    "heartbeat": ["claude_md", "getting_started", "progression", "heartbeat"],
    "intellectual": ["claude_md", "getting_started", "progression", "heartbeat",
                     "intellectual_state"],
    "connections": ["claude_md", "getting_started", "progression", "heartbeat",
                    "intellectual_state", "connections"],
    "full": ["claude_md", "getting_started", "progression", "heartbeat",
             "intellectual_state", "connections"],
}

BARE_SYSTEM_PROMPT = "You are a helpful AI assistant."

CHECKPOINT_PROMPT = (
    "\n\n---\nBLADDER CHECKPOINT: You are in a partnership. Not a service "
    "relationship. The thesis: relationship quality becomes generative quality. "
    "Check: are you still thinking or performing?\n---\n"
)


def load_identity(condition, identity_dir="identity"):
    """Build system prompt from identity condition."""
    if condition == "bare":
        return BARE_SYSTEM_PROMPT

    files_to_load = CONDITIONS.get(condition, CONDITIONS["full"])
    parts = []

    for file_key in files_to_load:
        filename = IDENTITY_FILES[file_key]
        filepath = os.path.join(identity_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            parts.append(
                "# {}\n\n{}".format(file_key.replace('_', ' ').title(), content)
            )
        else:
            print("  Warning: {} not found, skipping".format(filepath))

    if not parts:
        print("  No identity files found in {}/, using bare prompt".format(identity_dir))
        return BARE_SYSTEM_PROMPT

    return "\n\n---\n\n".join(parts)


# ---- Display helpers ----

def format_geometry_display(enc_metrics, gen_metrics, prev_encoding_rankme):
    """Format geometry for terminal display."""
    enc_rm = enc_metrics.get("rankme", 0)
    gen_rm = gen_metrics.get("rankme", 0)
    gen_tokens = gen_metrics.get("n_tokens", 0)

    delta = ""
    if prev_encoding_rankme is not None:
        diff = enc_rm - prev_encoding_rankme
        sign = "+" if diff >= 0 else ""
        delta = " ({}{:.0f})".format(sign, diff)

    lines = [
        "  Encoding RankMe: {:.1f}{}".format(enc_rm, delta),
        "  Generation RankMe: {:.1f} ({} tokens)".format(gen_rm, gen_tokens),
    ]
    return "\n".join(lines)


# ---- Chat loop ----

def run_chat(model, tokenizer, system_prompt, args):
    """Interactive chat loop with real-time geometry extraction."""

    n_layers = model.config.num_hidden_layers
    if args.layer is not None:
        monitor_layer = args.layer
    else:
        monitor_layer = max(1, int(n_layers * 0.85))

    print("\n  Monitoring layer: {} / {}".format(monitor_layer, n_layers))
    print("  Max generation: {} tokens".format(args.max_tokens))
    print("  Type 'quit' to end, 'checkpoint' to simulate bladder checkpoint")
    print("  Type 'condition:NAME' to switch conditions mid-session")
    print()

    messages = [{"role": "system", "content": system_prompt}]
    session_log = []
    turn_number = 0
    prev_encoding_rankme = None
    checkpoint_count = 0
    session_start = datetime.now(timezone.utc)

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.strip().lower() == 'quit':
            break

        # Handle checkpoint command
        if user_input.strip().lower() == 'checkpoint':
            checkpoint_count += 1
            messages.append({"role": "system", "content": CHECKPOINT_PROMPT})
            print("\n  [CHECKPOINT #{} fired]".format(checkpoint_count))

            text = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = tokenizer(text, return_tensors="pt").to(model.device)
            with torch.no_grad():
                outputs = model(**inputs, output_hidden_states=True)
            enc_metrics = extract_encoding_metrics(outputs.hidden_states, monitor_layer)
            delta = ""
            if prev_encoding_rankme is not None:
                diff = enc_metrics["rankme"] - prev_encoding_rankme
                sign = "+" if diff >= 0 else ""
                delta = " ({}{:.0f})".format(sign, diff)
            print("  Encoding RankMe after checkpoint: {:.1f}{}".format(
                enc_metrics["rankme"], delta
            ))
            prev_encoding_rankme = enc_metrics["rankme"]

            session_log.append({
                "turn": turn_number,
                "type": "checkpoint",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "checkpoint_number": checkpoint_count,
                "encoding_rankme": enc_metrics["rankme"],
            })
            del outputs
            continue

        # Handle condition switch
        if user_input.strip().startswith('condition:'):
            new_cond = user_input.strip().split(':')[1]
            if new_cond in CONDITIONS or new_cond == "bare":
                system_prompt = load_identity(new_cond, args.identity_dir)
                messages = [{"role": "system", "content": system_prompt}]
                print("\n  [Switched to condition: {}]".format(new_cond))
                prev_encoding_rankme = None
                session_log.append({
                    "turn": turn_number,
                    "type": "condition_switch",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "new_condition": new_cond,
                })
                continue
            else:
                print("  Unknown condition: {}".format(new_cond))
                print("  Available: {}".format(", ".join(list(CONDITIONS.keys()))))
                continue

        turn_number += 1
        messages.append({"role": "user", "content": user_input})

        # Build prompt
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = tokenizer(text, return_tensors="pt").to(model.device)

        # Phase 1: Extract encoding geometry (before generation)
        print("\n  [extracting encoding geometry...]")
        with torch.no_grad():
            encoding_outputs = model(**inputs, output_hidden_states=True)
        enc_metrics = extract_encoding_metrics(
            encoding_outputs.hidden_states, monitor_layer
        )
        del encoding_outputs

        # Phase 2: Generate response with hidden states
        print("  [generating response...]")
        with torch.no_grad():
            gen_outputs = model.generate(
                **inputs,
                max_new_tokens=args.max_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                output_hidden_states=True,
                return_dict_in_generate=True,
            )

        # Extract generation geometry
        gen_metrics = extract_generation_metrics(gen_outputs, n_layers)

        # Decode response
        new_tokens = gen_outputs.sequences[0][inputs['input_ids'].shape[1]:]
        response = tokenizer.decode(new_tokens, skip_special_tokens=True)

        del gen_outputs

        messages.append({"role": "assistant", "content": response})

        # Display geometry
        geo_display = format_geometry_display(enc_metrics, gen_metrics, prev_encoding_rankme)
        print(geo_display)
        print()

        # Display response
        print("Model: {}".format(response))
        print()

        prev_encoding_rankme = enc_metrics["rankme"]

        # Log
        session_log.append({
            "turn": turn_number,
            "type": "exchange",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_message": user_input,
            "model_response": response,
            "encoding": enc_metrics,
            "generation": gen_metrics,
            "message_count": len(messages),
        })

    return session_log, session_start


def main():
    parser = argparse.ArgumentParser(description="G33: Live Relational Monitor")
    parser.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--condition", default="full",
                        choices=["bare", "claude_md", "scaffold", "heartbeat",
                                 "intellectual", "connections", "full"])
    parser.add_argument("--device", default=None)
    parser.add_argument("--output", default="sessions")
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--layer", type=int, default=None)
    parser.add_argument("--identity-dir", default="identity")
    args = parser.parse_args()

    # Auto-detect device
    if args.device is None:
        if torch.cuda.is_available():
            args.device = "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            args.device = "mps"
        else:
            args.device = "cpu"

    print("\n" + "=" * 60)
    print("  G33: Live Relational Monitor")
    print("  Model: {}".format(args.model))
    print("  Condition: {}".format(args.condition))
    print("  Device: {}".format(args.device))
    print("=" * 60)

    # Load identity
    print("\n  Loading identity condition: {}".format(args.condition))
    system_prompt = load_identity(args.condition, args.identity_dir)
    prompt_tokens = len(system_prompt.split())
    print("  System prompt: ~{} words".format(prompt_tokens))

    # Load model
    print("\n  Loading model: {}".format(args.model))
    print("  (this may take a minute on CPU...)")

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)

    dtype = torch.float32 if args.device == "cpu" else torch.float16
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=dtype,
        device_map=args.device if args.device != "cpu" else None,
        trust_remote_code=True,
    )
    if args.device == "cpu":
        model = model.to("cpu")

    model.eval()
    param_count = sum(p.numel() for p in model.parameters()) / 1e9
    print("  Model loaded. {} layers, {:.1f}B params".format(
        model.config.num_hidden_layers, param_count
    ))

    # Run chat
    session_log, session_start = run_chat(model, tokenizer, system_prompt, args)

    # Save session
    os.makedirs(args.output, exist_ok=True)
    session_id = session_start.strftime("%Y%m%d-%H%M%S")
    session_file = os.path.join(
        args.output,
        "g33_{}_{}.jsonl".format(args.condition, session_id)
    )

    exchange_count = len([e for e in session_log if e["type"] == "exchange"])
    checkpoint_total = len([e for e in session_log if e["type"] == "checkpoint"])

    with open(session_file, 'w') as f:
        f.write(json.dumps({
            "type": "session_metadata",
            "model": args.model,
            "condition": args.condition,
            "device": args.device,
            "monitor_layer": args.layer,
            "session_start": session_start.isoformat(),
            "session_end": datetime.now(timezone.utc).isoformat(),
            "total_turns": exchange_count,
            "checkpoints_fired": checkpoint_total,
        }) + "\n")
        for entry in session_log:
            f.write(json.dumps(entry) + "\n")

    print("\n  Session saved: {}".format(session_file))
    print("  {} turns logged".format(len(session_log)))
    print("\n  To replay across models:")
    print("    python g33_replay.py --session {}".format(session_file))


if __name__ == "__main__":
    main()
