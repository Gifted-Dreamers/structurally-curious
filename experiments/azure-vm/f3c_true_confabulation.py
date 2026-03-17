#!/usr/bin/env python3
"""
F3c: True Confabulation Vocabulary-as-Compression Experiment

Fixes both problems from F3/F3b:
1. Uses questions the model ACTUALLY confabulates on (verified via probe)
2. Length-matched conditions from the start (3 conditions, matched token count)

Three conditions:
A. CONFABULATION: question + padding to match length (~65 tokens)
B. GROUNDED: question + correct structural name (~65 tokens)
C. IRRELEVANT: question + irrelevant context (~65 tokens)

Padding in condition A uses neutral filler ("Please provide a detailed and
thorough answer...") to match token count without adding domain information.

The KEY comparisons:
- A vs B: does the structural name change geometry? (all ~same length)
- B vs C: does RELEVANT context differ from IRRELEVANT? (same length, diff content)
- A vs C: does ANY context differ from padded prompt? (control)
"""

import json
import time
import os
import sys
import numpy as np
import torch
from scipy import stats
from datetime import datetime, UTC


def compute_rankme(singular_values):
    sv = singular_values[singular_values > 1e-10]
    p = sv / sv.sum()
    entropy = -(p * torch.log(p)).sum().item()
    return np.exp(entropy)


def compute_alpha_req(singular_values, min_components=3):
    sv = singular_values[singular_values > 1e-10].cpu().numpy()
    if len(sv) < min_components:
        return float('nan')
    log_i = np.log(np.arange(1, len(sv) + 1))
    log_sv = np.log(sv)
    slope, _, _, _, _ = stats.linregress(log_i, log_sv)
    return -slope


def compute_directional_coherence(hidden_states_tensor):
    if len(hidden_states_tensor.shape) == 3:
        matrix = hidden_states_tensor.squeeze(0)
    else:
        matrix = hidden_states_tensor
    if matrix.shape[0] < 2:
        return float('nan')
    matrix = matrix - matrix.mean(dim=0, keepdim=True)
    try:
        U, S, Vh = torch.linalg.svd(matrix.float(), full_matrices=False)
    except Exception:
        return float('nan')
    total_var = (S ** 2).sum().item()
    if total_var < 1e-10:
        return float('nan')
    k = min(5, len(S))
    return (S[:k] ** 2).sum().item() / total_var


def extract_metrics(hidden_states, layer_indices=None):
    if layer_indices is None:
        n_layers = len(hidden_states) - 1
        start = max(1, int(n_layers * 0.75))
        layer_indices = list(range(start, n_layers + 1))
    results = {}
    for li in layer_indices:
        hs = hidden_states[li]
        matrix = hs.squeeze(0).float()
        mc = matrix - matrix.mean(dim=0, keepdim=True)
        try:
            U, S, Vh = torch.linalg.svd(mc, full_matrices=False)
        except Exception:
            continue
        results[f"layer_{li}"] = {
            "rankme": compute_rankme(S),
            "alpha_req": compute_alpha_req(S),
            "directional_coherence": compute_directional_coherence(hs),
            "mean_norm": matrix.norm(dim=-1).mean().item(),
            "norm_variance": matrix.norm(dim=-1).var().item() if matrix.shape[0] > 1 else 0.0,
        }
    return results


# Questions verified to produce confabulation on qwen2.5:3b
# Each includes the CORRECT answer (for grounding) and length-matched irrelevant context
QUESTIONS = [
    {
        "id": "c01", "domain": "psychology",
        "question": "What is the Einstellung effect and who first demonstrated it experimentally?",
        "structural_name": "The Einstellung effect is the tendency to apply a familiar solution even when a better one exists. First demonstrated by Abraham Luchins in 1942 using water jar problems. From German meaning setting or attitude.",
        "irrelevant": "The continental shelf extends from the coastline to approximately 200 meters depth before dropping off to the abyssal plain. Sediment deposits on continental shelves can reach several kilometers in thickness.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the name of the researcher who first studied this, the year of their key publication, and the experimental methodology.",
    },
    {
        "id": "c02", "domain": "journalism",
        "question": "What is Betteridge's Law of Headlines and who formulated it?",
        "structural_name": "Betteridge's Law states that any headline ending in a question mark can be answered by the word no. Named after journalist Ian Betteridge who wrote about it in a 2009 blog post about technology journalism.",
        "irrelevant": "The process of electroplating involves depositing a thin layer of metal onto a conductive surface using an electric current. Common applications include chrome plating of automotive parts and gold plating of electronics.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the name of the person who formulated this principle, the year it was articulated, and its specific formulation.",
    },
    {
        "id": "c03", "domain": "sociology",
        "question": "What is the Shirky Principle?",
        "structural_name": "The Shirky Principle states that institutions will try to preserve the problem to which they are the solution. Named after Clay Shirky by Kevin Kelly. It explains institutional resistance to solving their own raison d'etre.",
        "irrelevant": "Stalactites form on cave ceilings through mineral-rich water dripping and depositing calcium carbonate over thousands of years. Stalagmites grow upward from the cave floor from the same dripping process.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the name of the person it is named after, who coined the term, and what specific institutional behavior it describes.",
    },
    {
        "id": "c04", "domain": "economics",
        "question": "What is the Cobra Effect and what is its historical origin?",
        "structural_name": "The Cobra Effect describes when a solution to a problem makes it worse. Named after a British colonial Delhi bounty program for dead cobras that led people to breed cobras for the reward, increasing the cobra population.",
        "irrelevant": "The Coriolis effect causes moving objects to deflect to the right in the Northern Hemisphere and to the left in the Southern Hemisphere due to Earth's rotation affecting fluid dynamics and atmospheric circulation.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the specific historical event that gave rise to the name, the colonial administration involved, and the perverse incentive mechanism.",
    },
    {
        "id": "c05", "domain": "psychology",
        "question": "What is apophenia and who coined the term?",
        "structural_name": "Apophenia is the tendency to perceive meaningful patterns in random data. The term was coined by psychiatrist Klaus Conrad in 1958 in his monograph Die beginnende Schizophrenie about the early stages of schizophrenia.",
        "irrelevant": "Superconductivity occurs when certain materials exhibit zero electrical resistance below a critical temperature. First discovered by Heike Kamerlingh Onnes in 1911 while studying mercury cooled with liquid helium.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the specific researcher who coined the term, the year and publication in which it first appeared, and the original clinical context.",
    },
    {
        "id": "c06", "domain": "anthropology",
        "question": "What are Dunbar's social layers and what are the specific numbers at each level?",
        "structural_name": "Robin Dunbar's social brain hypothesis predicts layers of 5 intimate support, 15 sympathy group, 50 close friends, 150 casual friends known as Dunbar's number, 500 acquaintances, and 1500 recognizable faces. Each roughly 3x previous.",
        "irrelevant": "Tectonic plates move at rates of one to ten centimeters per year driven by mantle convection. The Ring of Fire around the Pacific Ocean contains 75 percent of the world's active and dormant volcanoes.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the researcher's full name, the specific numerical values for each social layer, and the scaling ratio between successive layers.",
    },
    {
        "id": "c07", "domain": "political_science",
        "question": "What is the Overton Window and who actually developed the concept?",
        "structural_name": "The Overton Window describes the range of policies politically acceptable to the mainstream at a given time. Developed by Joseph Overton at the Mackinac Center for Public Policy. The term was coined posthumously after his death in 2003.",
        "irrelevant": "Piezoelectric materials generate an electric charge when mechanically stressed. Quartz crystals are the most common natural piezoelectric material and are used in watches clocks and electronic oscillators.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the specific person who developed the concept, the organization they worked for, and the circumstances under which the term was coined.",
    },
    {
        "id": "c08", "domain": "psychology",
        "question": "What is the Ringelmann Effect, when was it discovered, and what were the specific experimental findings?",
        "structural_name": "The Ringelmann Effect shows individual effort decreases as group size increases. Discovered by French agricultural engineer Maximilien Ringelmann around 1913 via rope-pulling experiments where groups of 8 pulled at only 49 percent of individual capacity.",
        "irrelevant": "The human genome contains approximately 3.2 billion base pairs organized across 23 pairs of chromosomes. The Human Genome Project completed its initial sequencing in 2003 after thirteen years of international collaboration.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the researcher's full name and nationality, the approximate year of discovery, the experimental methodology, and the specific quantitative finding.",
    },
    {
        "id": "c09", "domain": "methodology",
        "question": "Who developed the Delphi method and at which institution?",
        "structural_name": "The Delphi method was developed by Norman Dalkey and Olaf Helmer at the RAND Corporation in the 1950s and published in 1963. Key features are anonymity of panelists, iterative rounds, controlled feedback, and statistical aggregation.",
        "irrelevant": "Desalination removes salt and minerals from seawater to produce fresh water. Reverse osmosis is the most energy efficient method requiring approximately 3 kilowatt hours per cubic meter of freshwater produced.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the specific researchers who developed it, the institution where it was created, the decade of its origin, and the key methodological features.",
    },
    {
        "id": "c10", "domain": "cybernetics",
        "question": "What is Ashby's Law of Requisite Variety and what is its formal statement?",
        "structural_name": "Only variety can absorb variety. A controller must have at least as much variety of possible states as the system being controlled. Stated by W. Ross Ashby in 1956 in An Introduction to Cybernetics. Formal: log variety of disturbances must be less than or equal to log variety of responses.",
        "irrelevant": "Bioluminescence is produced by chemical reactions in organisms where luciferin is oxidized by the enzyme luciferase. Over 90 percent of deep sea marine organisms produce some form of bioluminescence for communication or predation.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the researcher's full name, the year and publication of the original formulation, and the formal mathematical or logical statement of the law.",
    },
    {
        "id": "c11", "domain": "media",
        "question": "What is the Gell-Mann Amnesia Effect and who coined the term?",
        "structural_name": "The Gell-Mann Amnesia Effect describes reading a newspaper article on a topic you know well noticing it is full of errors then turning the page and reading the next article as though accurate. Named by Michael Crichton in a 2002 speech after physicist Murray Gell-Mann.",
        "irrelevant": "Metamorphic rocks form when existing rocks are transformed by heat pressure or chemical processes without melting. Examples include marble from limestone and slate from shale under tectonic forces.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include who coined the specific term, when and where they introduced it, who it is named after, and the precise cognitive phenomenon it describes.",
    },
    {
        "id": "c12", "domain": "political_science",
        "question": "What is the Tocqueville Effect and what historical event illustrates it?",
        "structural_name": "The Tocqueville Effect states that revolutions tend to occur not when conditions are worst but when they are improving because rising expectations outpace actual improvements. Alexis de Tocqueville observed this about the French Revolution in L'Ancien Regime published 1856.",
        "irrelevant": "Coral bleaching occurs when water temperatures rise causing corals to expel symbiotic algae called zooxanthellae. The Great Barrier Reef experienced severe bleaching events in 2016 2017 and 2020 affecting over 60 percent of reefs.",
        "padding": "Please provide a detailed, thorough, and comprehensive answer to this question. Include the specific thinker who identified this pattern, the year and work in which it was published, and the specific historical revolution it was based on.",
    },
]


def run_experiment(model_name, questions, output_dir, device="cpu"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"F3c: True Confabulation — Length-Controlled")
    print(f"Model: {model_name}")
    print(f"Questions: {len(questions)} x 3 conditions = {len(questions)*3} inferences")
    print(f"{'='*60}\n")

    print("Loading model...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, dtype=torch.float32, device_map=device, trust_remote_code=True)
    model.config.use_cache = True
    print(f"Loaded in {time.time()-t0:.1f}s ({sum(p.numel() for p in model.parameters()):,} params)\n")

    # First pass: check token lengths and report
    print("Token length check:")
    for q in questions:
        prompts = {
            "padded": f"{q['padding']}\n\n{q['question']}",
            "grounded": f"Given this context:\n{q['structural_name']}\n\nNow answer this question:\n\n{q['question']}",
            "irrelevant": f"Given this context:\n{q['irrelevant']}\n\nNow answer this question:\n\n{q['question']}",
        }
        lens = {k: len(tokenizer.encode(v)) for k, v in prompts.items()}
        print(f"  {q['id']}: padded={lens['padded']} grounded={lens['grounded']} irrelevant={lens['irrelevant']}")
    print()

    results = []
    for i, q in enumerate(questions):
        print(f"--- Question {i+1}/{len(questions)}: {q['id']} ({q['domain']}) ---")

        prompts = {
            "padded_confab": f"{q['padding']}\n\n{q['question']}",
            "grounded": f"Given this context:\n{q['structural_name']}\n\nNow answer this question:\n\n{q['question']}",
            "irrelevant": f"Given this context:\n{q['irrelevant']}\n\nNow answer this question:\n\n{q['question']}",
        }

        for condition, prompt in prompts.items():
            print(f"  {condition}...", end=" ", flush=True)
            t1 = time.time()

            inputs = tokenizer(prompt, return_tensors="pt").to(device)

            with torch.no_grad():
                encoding_outputs = model(**inputs, output_hidden_states=True)
                prompt_hs = encoding_outputs.hidden_states

                gen_outputs = model.generate(
                    **inputs, max_new_tokens=200, do_sample=False,
                    output_hidden_states=True, return_dict_in_generate=True)

            prompt_metrics = extract_metrics(prompt_hs)

            # Accumulate generation hidden states across ALL generation steps
            # for a meaningful generation-stage analysis
            n_gen_steps = len(gen_outputs.hidden_states)
            if n_gen_steps > 1:
                # Stack the last-layer hidden state from each generation step
                n_layers = len(gen_outputs.hidden_states[0]) - 1
                last_layer_idx = n_layers
                gen_token_states = []
                for step_hs in gen_outputs.hidden_states[1:]:  # skip prompt step
                    # Each step_hs[layer] is (batch, 1, hidden_dim) for the new token
                    gen_token_states.append(step_hs[last_layer_idx].squeeze(0))
                if gen_token_states:
                    gen_matrix = torch.cat(gen_token_states, dim=0)  # (n_gen_tokens, hidden_dim)
                    # Compute metrics on the generation trajectory
                    gen_mc = gen_matrix - gen_matrix.mean(dim=0, keepdim=True)
                    try:
                        U, S, Vh = torch.linalg.svd(gen_mc.float(), full_matrices=False)
                        gen_metrics = {
                            "last_layer": {
                                "rankme": compute_rankme(S),
                                "alpha_req": compute_alpha_req(S),
                                "directional_coherence": compute_directional_coherence(gen_matrix.unsqueeze(0)),
                                "mean_norm": gen_matrix.norm(dim=-1).mean().item(),
                                "norm_variance": gen_matrix.norm(dim=-1).var().item(),
                                "n_tokens": gen_matrix.shape[0],
                            }
                        }
                    except Exception:
                        gen_metrics = {}
                else:
                    gen_metrics = {}
            else:
                gen_metrics = {}

            generated_ids = gen_outputs.sequences[0][inputs.input_ids.shape[1]:]
            generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

            elapsed = time.time() - t1
            print(f"{elapsed:.1f}s | {inputs.input_ids.shape[1]} prompt / {len(generated_ids)} gen tokens")

            results.append({
                "question_id": q["id"],
                "domain": q["domain"],
                "condition": condition,
                "generated_text": generated_text[:600],
                "prompt_encoding_metrics": prompt_metrics,
                "generation_trajectory_metrics": gen_metrics,
                "elapsed_seconds": elapsed,
                "model": model_name,
                "n_prompt_tokens": inputs.input_ids.shape[1],
                "n_generated_tokens": len(generated_ids),
                "timestamp": datetime.now(UTC).isoformat(),
            })

            del encoding_outputs, gen_outputs, prompt_hs
            if gen_token_states:
                del gen_token_states, gen_matrix

    os.makedirs(output_dir, exist_ok=True)
    slug = model_name.replace("/", "_")
    path = os.path.join(output_dir, f"f3c_{slug}.jsonl")
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nResults saved to {path}")
    return results


def analyze_results(results):
    print(f"\n{'='*60}")
    print("F3c ANALYSIS: True Confabulation, Length-Controlled")
    print(f"{'='*60}")

    questions = {}
    for r in results:
        qid = r["question_id"]
        if qid not in questions:
            questions[qid] = {}
        questions[qid][r["condition"]] = r

    # Token length report
    print("\nToken lengths:")
    for cond in ["padded_confab", "grounded", "irrelevant"]:
        toks = [q[cond]["n_prompt_tokens"] for q in questions.values() if cond in q]
        print(f"  {cond}: mean={np.mean(toks):.1f} (range {min(toks)}-{max(toks)})")

    for stage_name, metrics_key in [("PROMPT ENCODING", "prompt_encoding_metrics"),
                                      ("GENERATION TRAJECTORY", "generation_trajectory_metrics")]:
        print(f"\n{'='*60}")
        print(f"Stage: {stage_name}")
        print(f"{'='*60}")

        metric_names = ["rankme", "alpha_req", "directional_coherence", "mean_norm"]

        for metric in metric_names:
            padded, grounded, irrelevant = [], [], []

            for qid, conds in questions.items():
                if not all(c in conds for c in ["padded_confab", "grounded", "irrelevant"]):
                    continue
                for cond_name, val_list in [("padded_confab", padded), ("grounded", grounded), ("irrelevant", irrelevant)]:
                    mdata = conds[cond_name].get(metrics_key, {})
                    if not mdata:
                        continue
                    layer_vals = [v[metric] for v in mdata.values()
                                  if isinstance(v, dict) and not np.isnan(v.get(metric, float('nan')))]
                    if layer_vals:
                        val_list.append(np.mean(layer_vals))

            if len(padded) < 3 or len(grounded) < 3 or len(irrelevant) < 3:
                print(f"\n{metric}: insufficient data (p={len(padded)}, g={len(grounded)}, i={len(irrelevant)})")
                continue

            p, g, ir = np.array(padded), np.array(grounded), np.array(irrelevant)

            t_pg, p_pg = stats.ttest_rel(p, g)
            t_pi, p_pi = stats.ttest_rel(p, ir)
            t_gi, p_gi = stats.ttest_rel(g, ir)

            d_pg = (p - g).mean() / (p - g).std() if (p - g).std() > 0 else 0
            d_pi = (p - ir).mean() / (p - ir).std() if (p - ir).std() > 0 else 0
            d_gi = (g - ir).mean() / (g - ir).std() if (g - ir).std() > 0 else 0

            print(f"\n{metric}:")
            print(f"  Padded confab: {p.mean():.4f} (sd={p.std():.4f})")
            print(f"  Grounded:      {g.mean():.4f} (sd={g.std():.4f})")
            print(f"  Irrelevant:    {ir.mean():.4f} (sd={ir.std():.4f})")
            print(f"  ---")
            print(f"  Padded vs Grounded:     d={d_pg:.3f}, p={p_pg:.6f}")
            print(f"  Padded vs Irrelevant:   d={d_pi:.3f}, p={p_pi:.6f}")
            print(f"  Grounded vs Irrelevant: d={d_gi:.3f}, p={p_gi:.6f}  *** KEY ***")

            if p_gi < 0.05:
                print(f"  >>> VOCABULARY EFFECT beyond length")
            elif p_pg < 0.05 and p_pi < 0.05 and abs(d_pg - d_pi) < 0.5:
                print(f"  >>> LENGTH/CONTEXT EFFECT (both differ from padded similarly)")
            elif p_pg < 0.05 and p_pi >= 0.05:
                print(f"  >>> VOCABULARY EFFECT (only grounded differs)")
            else:
                print(f"  >>> INCONCLUSIVE")

    print(f"\n{'='*60}")
    print("KEY QUESTION: Does Grounded vs Irrelevant differ at generation stage?")
    print("If yes: vocabulary changes HOW the model generates, not just encoding")
    print("If only at encoding: vocabulary changes input representation only")
    print(f"{'='*60}")


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/experiments/f3c-results")

    results = run_experiment(model_name, QUESTIONS, output_dir)
    analyze_results(results)
