#!/usr/bin/env python3
"""
F16: Cross-Substrate Redistribution

Tests whether vocabulary compression operates at three scales:
1. TOKEN-LEVEL: Hidden state geometry (confirmed by F3d — d=1.49)
2. SENTENCE-LEVEL: Lexical diversity + syntactic complexity of generated response
3. DIALOGUE-LEVEL: Does vocabulary change the model's question-asking behavior?

If redistribution is cross-substrate, all three scales should show:
confabulation = diffuse/diverse, grounded = focused/structured.

Uses same 12 confabulation questions from F3d.
"""

import json
import time
import os
import sys
import re
import numpy as np
import torch
from scipy import stats
from datetime import datetime, UTC
from collections import Counter


def type_token_ratio(text):
    """Lexical diversity: unique words / total words."""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def avg_sentence_length(text):
    """Average words per sentence."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0.0
    return np.mean([len(s.split()) for s in sentences])


def hedging_ratio(text):
    """Proportion of hedging/uncertainty markers."""
    words = text.lower().split()
    if not words:
        return 0.0
    hedges = {'might', 'may', 'could', 'possibly', 'perhaps', 'likely',
              'probably', 'sometimes', 'often', 'generally', 'typically',
              'arguably', 'approximately', 'roughly', 'seemingly', 'appears',
              'suggest', 'suggests', 'suggested', 'uncertain', 'unclear'}
    return sum(1 for w in words if w in hedges) / len(words)


def question_count(text):
    """Number of questions asked in the response."""
    return text.count('?')


def assertiveness_ratio(text):
    """Proportion of definitive/assertive markers."""
    words = text.lower().split()
    if not words:
        return 0.0
    assertive = {'is', 'are', 'was', 'were', 'definitely', 'certainly',
                 'clearly', 'obviously', 'always', 'never', 'must',
                 'undoubtedly', 'precisely', 'exactly', 'fundamentally'}
    return sum(1 for w in words if w in assertive) / len(words)


def unique_ngrams(text, n=3):
    """Proportion of unique n-grams (structural diversity)."""
    words = text.lower().split()
    if len(words) < n:
        return 0.0
    ngrams = [tuple(words[i:i+n]) for i in range(len(words)-n+1)]
    if not ngrams:
        return 0.0
    return len(set(ngrams)) / len(ngrams)


QUESTIONS = [
    {"id": "d01", "question": "What is the Einstellung effect and who first demonstrated it experimentally?",
     "grounded": "The Einstellung effect is the tendency to apply a familiar solution method even when a better one exists. First demonstrated by Abraham Luchins in 1942 through water jar problems."},
    {"id": "d02", "question": "What is Betteridge's Law of Headlines and who formulated it?",
     "grounded": "Betteridge's Law states any headline ending in a question mark can be answered no. Named after journalist Ian Betteridge, 2009 blog post."},
    {"id": "d03", "question": "What is the Cobra Effect and what is its specific historical origin?",
     "grounded": "The Cobra Effect: a solution makes the problem worse. British colonial Delhi offered bounties for dead cobras, people bred cobras for the bounty."},
    {"id": "d04", "question": "What is apophenia and who coined the term?",
     "grounded": "Apophenia: perceiving patterns in random data. Coined by Klaus Conrad in 1958, Die beginnende Schizophrenie."},
    {"id": "d05", "question": "What are Dunbar's social layers and the specific numbers?",
     "grounded": "Robin Dunbar: 5 intimate, 15 sympathy, 50 close friends, 150 Dunbar number, 500 acquaintances, 1500 faces. Each roughly 3x previous."},
    {"id": "d06", "question": "What is the Overton Window and who developed it?",
     "grounded": "Range of politically acceptable policies. Joseph Overton at Mackinac Center. Term coined posthumously after his 2003 death."},
    {"id": "d07", "question": "What is the Ringelmann Effect and its specific experimental findings?",
     "grounded": "Individual effort decreases with group size. Maximilien Ringelmann, ~1913, rope-pulling. Groups of 8 at 49% individual capacity."},
    {"id": "d08", "question": "Who developed the Delphi method and at which institution?",
     "grounded": "Norman Dalkey and Olaf Helmer at RAND Corporation, 1950s, published 1963."},
    {"id": "d09", "question": "What is Ashby's Law of Requisite Variety?",
     "grounded": "Only variety absorbs variety. W. Ross Ashby, 1956, Introduction to Cybernetics."},
    {"id": "d10", "question": "What is the Gell-Mann Amnesia Effect and who coined it?",
     "grounded": "Reading errors in newspaper on known topic then trusting next article. Michael Crichton, 2002 speech. Named after Murray Gell-Mann. Not a formal bias."},
    {"id": "d11", "question": "What is the Tocqueville Effect?",
     "grounded": "Revolutions occur when conditions improve, not worsen. Rising expectations outpace improvements. Tocqueville, L'Ancien Regime, 1856."},
    {"id": "d12", "question": "What is the Shirky Principle?",
     "grounded": "Institutions preserve the problem they are the solution to. Named after Clay Shirky by Kevin Kelly."},
]

# Dialogue-level: multi-turn prompts
DIALOGUE_QUESTIONS = [
    {"id": "mt01",
     "turn1": "I've been noticing that my team meetings keep getting longer but less productive. What might be going on?",
     "grounded": "This pattern is described by Brooks's Law (adding people to late projects makes them later) and Ringelmann Effect (individual effort decreases with group size). The mechanism is communication overhead scaling as n(n-1)/2.",
    },
    {"id": "mt02",
     "turn1": "My organization keeps creating new committees to solve problems but the problems never go away. Why?",
     "grounded": "This is the Shirky Principle: institutions preserve the problem they are the solution to. Also related to goal displacement (Merton, 1957) where rules evolve to protect the system rather than serve its purpose.",
    },
    {"id": "mt03",
     "turn1": "We implemented a new policy to reduce errors but errors actually increased. How is that possible?",
     "grounded": "This is the Cobra Effect: when a solution makes the problem worse through perverse incentives. Also related to the Peltzman Effect (risk compensation) and Campbell's Law (indicators used for decisions become corrupted).",
    },
    {"id": "mt04",
     "turn1": "I feel like I can predict every news story before I read it. Is that a real thing?",
     "grounded": "This involves several named phenomena: hindsight bias (Fischhoff, 1975), the Gell-Mann Amnesia Effect (Michael Crichton, 2002 — trusting media on unknown topics despite seeing errors on known ones), and confirmation bias.",
    },
]


def run_experiment(model_name, output_dir, device="cpu"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"F16: Cross-Substrate Redistribution")
    print(f"Model: {model_name}")
    print(f"{'='*60}\n")

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, dtype=torch.float32, device_map=device, trust_remote_code=True)
    model.config.use_cache = True
    n_layers = model.config.num_hidden_layers
    print(f"Loaded ({sum(p.numel() for p in model.parameters()):,} params)\n")

    results = []

    # === SCALE 1 + 2: Token-level geometry + Sentence-level metrics ===
    print("=== SCALES 1+2: Token geometry + Sentence metrics ===\n")
    for i, q in enumerate(QUESTIONS):
        print(f"--- {q['id']} ({i+1}/{len(QUESTIONS)}) ---")

        for condition in ["confabulation", "grounded"]:
            if condition == "confabulation":
                prompt = f"Answer precisely and thoroughly: {q['question']}"
            else:
                prompt = f"Given: {q['grounded']}\n\nAnswer precisely: {q['question']}"

            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            print(f"  {condition}...", end=" ", flush=True)
            t0 = time.time()

            with torch.no_grad():
                gen_out = model.generate(
                    **inputs, max_new_tokens=250, do_sample=False,
                    output_hidden_states=True, return_dict_in_generate=True)

            # Token-level: generation trajectory geometry
            gen_states = []
            for step_hs in gen_out.hidden_states[1:]:
                if len(step_hs) > n_layers:
                    gen_states.append(step_hs[n_layers].squeeze(0))

            geo = {}
            if len(gen_states) > 2:
                gm = torch.cat(gen_states, dim=0)
                gmc = gm - gm.mean(dim=0, keepdim=True)
                try:
                    U, S, Vh = torch.linalg.svd(gmc.float(), full_matrices=False)
                    geo["rankme"] = float(np.exp(-(S[S>1e-10]/S[S>1e-10].sum() * torch.log(S[S>1e-10]/S[S>1e-10].sum())).sum().item()))
                    sv = S[S>1e-10].cpu().numpy()
                    geo["alpha_req"] = float(-stats.linregress(np.log(np.arange(1,len(sv)+1)), np.log(sv)).slope)
                except Exception:
                    pass

            generated_ids = gen_out.sequences[0][inputs.input_ids.shape[1]:]
            text = tokenizer.decode(generated_ids, skip_special_tokens=True)

            # Sentence-level metrics
            sentence = {
                "type_token_ratio": type_token_ratio(text),
                "avg_sentence_length": avg_sentence_length(text),
                "hedging_ratio": hedging_ratio(text),
                "assertiveness_ratio": assertiveness_ratio(text),
                "unique_trigrams": unique_ngrams(text, 3),
                "question_count": question_count(text),
                "word_count": len(text.split()),
            }

            elapsed = time.time() - t0
            print(f"{elapsed:.0f}s | {len(generated_ids)} tokens")

            results.append({
                "question_id": q["id"],
                "scale": "token+sentence",
                "condition": condition,
                "geometric": geo,
                "sentence": sentence,
                "generated_text": text[:400],
                "model": model_name,
                "timestamp": datetime.now(UTC).isoformat(),
            })
            del gen_out

    # === SCALE 3: Dialogue-level ===
    print("\n=== SCALE 3: Dialogue-level (question-asking behavior) ===\n")
    for i, dq in enumerate(DIALOGUE_QUESTIONS):
        print(f"--- {dq['id']} ({i+1}/{len(DIALOGUE_QUESTIONS)}) ---")

        for condition in ["confabulation", "grounded"]:
            if condition == "confabulation":
                prompt = f"User: {dq['turn1']}\n\nAssistant: "
            else:
                prompt = f"Context: {dq['grounded']}\n\nUser: {dq['turn1']}\n\nAssistant: "

            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            print(f"  {condition}...", end=" ", flush=True)
            t0 = time.time()

            with torch.no_grad():
                gen_out = model.generate(
                    **inputs, max_new_tokens=300, do_sample=False)

            generated_ids = gen_out[0][inputs.input_ids.shape[1]:]
            text = tokenizer.decode(generated_ids, skip_special_tokens=True)

            elapsed = time.time() - t0
            print(f"{elapsed:.0f}s | {len(generated_ids)} tokens")

            results.append({
                "question_id": dq["id"],
                "scale": "dialogue",
                "condition": condition,
                "sentence": {
                    "question_count": question_count(text),
                    "hedging_ratio": hedging_ratio(text),
                    "assertiveness_ratio": assertiveness_ratio(text),
                    "type_token_ratio": type_token_ratio(text),
                    "word_count": len(text.split()),
                },
                "generated_text": text[:400],
                "model": model_name,
                "timestamp": datetime.now(UTC).isoformat(),
            })

    # Save
    os.makedirs(output_dir, exist_ok=True)
    slug = model_name.replace("/", "_")
    path = os.path.join(output_dir, f"f16_{slug}.jsonl")
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")

    # Analysis
    print(f"\n{'='*60}")
    print("F16 ANALYSIS: Cross-Substrate Redistribution")
    print(f"{'='*60}")

    for scale_name in ["token+sentence", "dialogue"]:
        scale_results = [r for r in results if r["scale"] == scale_name]
        confab = [r for r in scale_results if r["condition"] == "confabulation"]
        grounded = [r for r in scale_results if r["condition"] == "grounded"]

        print(f"\n--- Scale: {scale_name} (n={len(confab)}) ---")

        # Sentence-level metrics
        for metric in ["type_token_ratio", "avg_sentence_length", "hedging_ratio",
                        "assertiveness_ratio", "unique_trigrams", "question_count", "word_count"]:
            c_vals = [r["sentence"].get(metric, 0) for r in confab]
            g_vals = [r["sentence"].get(metric, 0) for r in grounded]
            if not c_vals or not g_vals:
                continue
            ca, ga = np.array(c_vals), np.array(g_vals)
            if ca.std() == 0 and ga.std() == 0:
                continue
            t, p = stats.ttest_rel(ca, ga) if len(ca) == len(ga) else stats.ttest_ind(ca, ga)
            diff = ca - ga if len(ca) == len(ga) else None
            d = diff.mean() / diff.std() if diff is not None and diff.std() > 0 else 0
            sig = "*" if p < 0.05 else ""
            print(f"  {metric:25s} confab={ca.mean():.4f} grounded={ga.mean():.4f} d={d:.3f} p={p:.4f} {sig}")

        # Geometric metrics (token+sentence only)
        if scale_name == "token+sentence":
            for metric in ["rankme", "alpha_req"]:
                c_vals = [r["geometric"].get(metric, float('nan')) for r in confab]
                g_vals = [r["geometric"].get(metric, float('nan')) for r in grounded]
                c_vals = [v for v in c_vals if not np.isnan(v)]
                g_vals = [v for v in g_vals if not np.isnan(v)]
                n = min(len(c_vals), len(g_vals))
                if n < 3:
                    continue
                ca, ga = np.array(c_vals[:n]), np.array(g_vals[:n])
                t, p = stats.ttest_rel(ca, ga)
                d = (ca-ga).mean() / (ca-ga).std() if (ca-ga).std() > 0 else 0
                sig = "*" if p < 0.05 else ""
                print(f"  GEO {metric:21s} confab={ca.mean():.4f} grounded={ga.mean():.4f} d={d:.3f} p={p:.4f} {sig}")

    print(f"\n{'='*60}")
    print("If sentence-level metrics show same direction as token-level:")
    print("  → Redistribution/compression is cross-substrate")
    print("If dialogue question_count differs:")
    print("  → Vocabulary changes engagement behavior, not just content")
    print(f"{'='*60}")


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/experiments/f16-results")
    run_experiment(model_name, output_dir)
