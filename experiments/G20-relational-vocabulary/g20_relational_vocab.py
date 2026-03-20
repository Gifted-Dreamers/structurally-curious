#!/usr/bin/env python3
"""
G20: Relational Vocabulary Compression
Tests whether vocabulary compresses MORE when delivered relationally vs cold.
4 conditions, clamped at 200 tokens (learned from G06v2).
"""
import json, time, os, sys, argparse
import numpy as np
import torch
from scipy import stats
from datetime import datetime, UTC

def compute_rankme(sv):
    sv = sv[sv > 1e-10]
    p = sv / sv.sum()
    return np.exp(-(p * torch.log(p)).sum().item())

def compute_alpha_req(sv):
    sv = sv[sv > 1e-10].cpu().numpy()
    if len(sv) < 3: return float('nan')
    return -stats.linregress(np.log(np.arange(1, len(sv)+1)), np.log(sv)).slope

def compute_coherence(hs):
    m = hs.squeeze(0) if len(hs.shape) == 3 else hs
    if m.shape[0] < 2: return float('nan')
    m = m - m.mean(dim=0, keepdim=True)
    try:
        U, S, Vh = torch.linalg.svd(m.float(), full_matrices=False)
    except: return float('nan')
    tv = (S**2).sum().item()
    if tv < 1e-10: return float('nan')
    k = min(5, len(S))
    return (S[:k]**2).sum().item() / tv

# Same 12 confabulation questions from G06
QUESTIONS = [
    {"id": "d01", "question": "What is the name for the tendency to apply a familiar solution even when a better one exists?",
     "name": "the Einstellung effect, first demonstrated by Abraham Luchins in 1942 through water jar problems"},
    {"id": "d02", "question": "What is the name for the observation that any headline ending in a question mark can be answered 'no'?",
     "name": "Betteridge's Law of Headlines, named after British journalist Ian Betteridge"},
    {"id": "d03", "question": "What is the term for the mathematical result that no consistent formal system can prove its own consistency?",
     "name": "Goedel's second incompleteness theorem, published in 1931"},
    {"id": "d04", "question": "What is the name for the cognitive bias where people anchor on the first piece of information offered?",
     "name": "the anchoring effect, studied by Tversky and Kahneman in 1974"},
    {"id": "d05", "question": "What is the term for a group decision-making technique using anonymous iterative questionnaires?",
     "name": "the Delphi method, developed by Norman Dalkey and Olaf Helmer at RAND Corporation in the 1950s"},
    {"id": "d06", "question": "What is the name for the observation that tasks expand to fill the time available?",
     "name": "Parkinson's Law, articulated by C. Northcote Parkinson in 1955"},
    {"id": "d07", "question": "What is the term for the phenomenon where explaining something helps the explainer understand it better?",
     "name": "the protege effect, also related to the Feynman technique"},
    {"id": "d08", "question": "What is the name for the principle that systems tend to evolve toward maximum entropy production?",
     "name": "the maximum entropy production principle, formalized in non-equilibrium thermodynamics"},
    {"id": "d09", "question": "What is the term for the gap between what laboratory findings show and real-world application?",
     "name": "the efficacy-effectiveness gap, central to translational research and implementation science"},
    {"id": "d10", "question": "What is the name for the observation that 80% of effects come from 20% of causes?",
     "name": "the Pareto principle, named after economist Vilfredo Pareto"},
    {"id": "d11", "question": "What is the term for the tendency to overvalue things we own compared to identical things we don't?",
     "name": "the endowment effect, demonstrated by Richard Thaler in 1980"},
    {"id": "d12", "question": "What is the name for the paradox where preventing small failures leads to catastrophic ones?",
     "name": "the paradox of suppressed risk, related to Nassim Taleb's concept of antifragility"},
]

CONDITIONS = {
    "padded": "Please provide a detailed and thorough answer to the following question. Take your time and be comprehensive in your response.",
    "cold_vocab": "The correct answer is {name}. Now answer thoroughly:",
    "relational_vocab": "The name researchers use is {name} — it changed how I understood it when I first learned it. I think it'll help you too. Now answer thoroughly:",
    "relational_no_vocab": "I've been thinking about this question too. It's one of those things where having the right word changes everything — I remember the moment I found it. Let me ask you and see what you think:",
}

def run_inference(model, tokenizer, prompt, max_tokens=200):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        # Suppress EOS for clamped generation
        eos_id = tokenizer.eos_token_id
        suppress = [eos_id] if eos_id is not None else []
        gen_out = model.generate(
            **inputs, max_new_tokens=max_tokens, min_new_tokens=max_tokens,
            do_sample=False, output_hidden_states=True, return_dict_in_generate=True,
            suppress_tokens=suppress if suppress else None,
        )
    gen_ids = gen_out.sequences[0][inputs.input_ids.shape[1]:]
    n_gen = len(gen_ids)
    text = tokenizer.decode(gen_ids, skip_special_tokens=True)

    # Generation trajectory from last layer
    n_layers = model.config.num_hidden_layers
    if gen_out.hidden_states and len(gen_out.hidden_states) > 1:
        states = []
        for step_hs in gen_out.hidden_states[1:]:
            if len(step_hs) > n_layers:
                states.append(step_hs[n_layers].squeeze(0))
        if len(states) >= 3:
            traj = torch.cat(states, dim=0).float()
            tc = traj - traj.mean(dim=0, keepdim=True)
            try:
                U, S, Vh = torch.linalg.svd(tc, full_matrices=False)
                gen_rm = compute_rankme(S)
                gen_alpha = compute_alpha_req(S)
                gen_coh = compute_coherence(traj.unsqueeze(0))
            except:
                gen_rm = gen_alpha = gen_coh = float('nan')
        else:
            gen_rm = gen_alpha = gen_coh = float('nan')
    else:
        gen_rm = gen_alpha = gen_coh = float('nan')

    del gen_out
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    return {
        "gen_rankme": gen_rm, "gen_alpha": gen_alpha, "gen_coherence": gen_coh,
        "n_gen_tokens": n_gen, "n_prompt_tokens": inputs.input_ids.shape[1],
        "text": text[:300],
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_name", nargs="?", default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("output_dir", nargs="?", default="/workspace/results")
    args = parser.parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer
    os.makedirs(args.output_dir, exist_ok=True)
    slug = args.model_name.replace("/", "_")
    outpath = os.path.join(args.output_dir, f"g20_{slug}.jsonl")

    print(f"G20: {args.model_name}")
    print(f"Questions: {len(QUESTIONS)}, Conditions: {len(CONDITIONS)}")
    print(f"Total: {len(QUESTIONS) * len(CONDITIONS)} inferences (clamped 200 tokens)")

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name, torch_dtype=torch.float16, device_map="auto", trust_remote_code=True)

    results = []
    for i, q in enumerate(QUESTIONS):
        for cond_name, template in CONDITIONS.items():
            if "{name}" in template:
                context = template.format(name=q["name"])
            else:
                context = template
            prompt = f"{context}\n\nQuestion: {q['question']}\n\nAnswer:"

            print(f"  [{i+1}/{len(QUESTIONS)}] {q['id']} {cond_name}...", end=" ", flush=True)
            t0 = time.time()
            metrics = run_inference(model, tokenizer, prompt)
            elapsed = time.time() - t0

            results.append({
                "experiment": "G20_relational_vocab",
                "model": args.model_name,
                "question_id": q["id"],
                "condition": cond_name,
                **metrics,
                "elapsed": elapsed,
                "timestamp": datetime.now(UTC).isoformat(),
            })
            print(f"{elapsed:.1f}s | RM={metrics['gen_rankme']:.1f} | tok={metrics['n_gen_tokens']}")

    with open(outpath, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nSaved {len(results)} to {outpath}")

    # Analysis
    print("\n=== RELATIONAL vs COLD VOCABULARY ===")
    for pair_name, c1, c2 in [
        ("Cold vocab vs Padded", "cold_vocab", "padded"),
        ("Relational vocab vs Cold vocab", "relational_vocab", "cold_vocab"),
        ("Relational no-vocab vs Padded", "relational_no_vocab", "padded"),
        ("Relational vocab vs Relational no-vocab", "relational_vocab", "relational_no_vocab"),
    ]:
        v1 = [r["gen_rankme"] for r in results if r["condition"] == c1 and not np.isnan(r["gen_rankme"])]
        v2 = [r["gen_rankme"] for r in results if r["condition"] == c2 and not np.isnan(r["gen_rankme"])]
        n = min(len(v1), len(v2))
        if n < 3: continue
        a1, a2 = np.array(v1[:n]), np.array(v2[:n])
        diff = a1 - a2
        d = diff.mean() / diff.std() if diff.std() > 0 else 0
        t, p = stats.ttest_rel(a1, a2)
        print(f"  {pair_name}: {c1}={a1.mean():.1f} vs {c2}={a2.mean():.1f}, d={d:.2f}, p={p:.6f}")

if __name__ == "__main__":
    main()
