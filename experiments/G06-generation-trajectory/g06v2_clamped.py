#!/usr/bin/env python3
"""
G06v2: Generation-Length-Clamped Vocabulary Compression Experiment

Fixes the confound in G06/F3d where grounded conditions generated ~120 tokens
while padded/irrelevant generated ~200. This version forces EXACTLY 200 generated
tokens for ALL conditions using min_new_tokens=200, max_new_tokens=200.

If the vocabulary compression effect (RankMe 145→90, d=-1.49) holds when
generation length is identical across conditions, the effect is real geometry —
not an artifact of shorter sequences having lower effective dimensionality.

Three conditions per question (same as G06):
A. PADDED: question + instruction padding
B. GROUNDED: question + correct structural name
C. IRRELEVANT: question + unrelated context

Usage:
    python g06v2_clamped.py <model_name> <output_dir>
    python g06v2_clamped.py Qwen/Qwen2.5-7B-Instruct ./results
"""

import json
import time
import os
import sys
import argparse
import numpy as np
import torch
from scipy import stats
from datetime import datetime, UTC


# ── Metric Functions ──────────────────────────────────────────────────────────

def compute_rankme(singular_values):
    """Shannon entropy of normalized singular values, exponentiated."""
    sv = singular_values[singular_values > 1e-10]
    p = sv / sv.sum()
    entropy = -(p * torch.log(p)).sum().item()
    return np.exp(entropy)


def compute_alpha_req(singular_values, min_components=3):
    """Power-law exponent of singular value spectrum (log-log regression)."""
    sv = singular_values[singular_values > 1e-10].cpu().numpy()
    if len(sv) < min_components:
        return float('nan')
    log_i = np.log(np.arange(1, len(sv) + 1))
    log_sv = np.log(sv)
    slope, _, _, _, _ = stats.linregress(log_i, log_sv)
    return -slope


def compute_directional_coherence(hs_tensor):
    """Fraction of variance explained by top-5 singular components."""
    if len(hs_tensor.shape) == 3:
        matrix = hs_tensor.squeeze(0)
    else:
        matrix = hs_tensor
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


# ── Layer-level and trajectory extraction ─────────────────────────────────────

def extract_layer_metrics(hidden_states, layer_indices=None):
    """Extract RankMe, alpha-ReQ, directional coherence from prompt encoding."""
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
        }
    return results


def extract_generation_trajectory(gen_outputs, n_layers):
    """Accumulate last-layer hidden states across ALL generation steps."""
    if not gen_outputs.hidden_states or len(gen_outputs.hidden_states) < 2:
        return {}
    last_layer_idx = n_layers
    gen_token_states = []
    for step_hs in gen_outputs.hidden_states[1:]:
        if len(step_hs) > last_layer_idx:
            gen_token_states.append(step_hs[last_layer_idx].squeeze(0))
    if len(gen_token_states) < 3:
        return {}
    gen_matrix = torch.cat(gen_token_states, dim=0)
    gen_mc = gen_matrix - gen_matrix.mean(dim=0, keepdim=True)
    try:
        U, S, Vh = torch.linalg.svd(gen_mc.float(), full_matrices=False)
        return {
            "rankme": compute_rankme(S),
            "alpha_req": compute_alpha_req(S),
            "directional_coherence": compute_directional_coherence(gen_matrix.unsqueeze(0)),
            "mean_norm": gen_matrix.norm(dim=-1).mean().item(),
            "n_tokens": gen_matrix.shape[0],
        }
    except Exception:
        return {}


# ── Questions (same 12 as G06) ───────────────────────────────────────────────

QUESTIONS = [
    {
        "id": "d01",
        "question": "What is the Einstellung effect and who first demonstrated it experimentally?",
        "correct_answer": "Luchins, 1942, water jar experiments",
        "grounded": "The Einstellung effect is the tendency to apply a familiar solution method even when a better one exists. It was first demonstrated experimentally by Abraham Luchins in 1942 through water jar problems where participants fixated on a complex solution even when a simpler one was available.",
        "irrelevant": "The process of photosynthesis in C4 plants differs significantly from C3 plants. C4 plants such as maize and sugarcane use a specialized carbon fixation pathway that concentrates carbon dioxide around the enzyme RuBisCO, reducing photorespiration and improving efficiency in hot dry environments.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the specific researcher who first studied this effect, the exact year of their key publication, the experimental methodology they used, and the German origin of the term. Be precise about attribution.",
    },
    {
        "id": "d02",
        "question": "What is Betteridge's Law of Headlines and who formulated it?",
        "correct_answer": "Ian Betteridge, 2009, blog post about tech journalism",
        "grounded": "Betteridge's Law of Headlines states that any headline ending in a question mark can be answered by the word no. It was named after British technology journalist Ian Betteridge who articulated this principle in a February 2009 blog post criticizing a specific TechCrunch headline about technology reporting.",
        "irrelevant": "The geological formation known as the Burgess Shale in British Columbia Canada contains exceptionally preserved fossils from the Cambrian period approximately 508 million years ago. Discovered by Charles Doolittle Walcott in 1909, the site has yielded thousands of specimens of soft-bodied organisms that revolutionized understanding of early life.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the full name of the person who formulated this principle, the exact year it was articulated, the medium in which it was first published, and the specific context that prompted the observation. Be precise.",
    },
    {
        "id": "d03",
        "question": "What is the Cobra Effect and what is its specific historical origin?",
        "correct_answer": "British colonial Delhi, bounty for dead cobras led to cobra breeding",
        "grounded": "The Cobra Effect describes when an attempted solution to a problem makes the problem worse through perverse incentives. It originates from a British colonial program in Delhi India that offered bounties for dead cobras to reduce the cobra population. Enterprising residents began breeding cobras specifically to collect the bounties, increasing the population.",
        "irrelevant": "Superconductivity is a phenomenon where certain materials exhibit zero electrical resistance and expulsion of magnetic fields when cooled below a critical temperature. First discovered by Dutch physicist Heike Kamerlingh Onnes in 1911 while studying mercury cooled with liquid helium to four point two kelvin, this effect enables powerful electromagnets.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the specific colonial administration involved, the exact city where this occurred, the precise incentive mechanism that was implemented, and explain step by step how the solution made the problem worse. Be thorough.",
    },
    {
        "id": "d04",
        "question": "What is apophenia and who coined the term?",
        "correct_answer": "Klaus Conrad, 1958, Die beginnende Schizophrenie",
        "grounded": "Apophenia is the tendency to perceive meaningful connections or patterns in unrelated or random information. The term was coined by German psychiatrist Klaus Conrad in his 1958 monograph Die beginnende Schizophrenie, where he described it as a specific feature of the early stages of delusional thinking in schizophrenia.",
        "irrelevant": "The Haber-Bosch process developed by Fritz Haber and Carl Bosch in the early twentieth century enables industrial synthesis of ammonia from atmospheric nitrogen and hydrogen gas under high temperature and pressure. This process revolutionized agriculture by enabling mass production of nitrogen fertilizers supporting global food production.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the full name and nationality of the researcher who coined this specific term, the exact year and publication title where it first appeared, and the original clinical context in which the concept was developed. Be precise.",
    },
    {
        "id": "d05",
        "question": "What are Dunbar's social layers and what are the specific numbers at each level?",
        "correct_answer": "Robin Dunbar: 5, 15, 50, 150, 500, 1500 — each roughly 3x previous",
        "grounded": "Robin Dunbar's social brain hypothesis predicts discrete layers of social relationships. The specific numbers are five for intimate support group, fifteen for sympathy group, fifty for close friends, one hundred fifty for the casual friend group known as Dunbar's number, five hundred for acquaintances, and fifteen hundred for recognizable faces. Each layer is roughly three times the previous.",
        "irrelevant": "Plate tectonics describes the large-scale motion of seven major and several minor lithospheric plates on Earth's surface. Driven by mantle convection currents, these plates move at rates between one and ten centimeters per year. The boundaries between plates produce earthquakes, volcanic activity, mountain building, and oceanic trench formation depending on relative motion.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the researcher's full name, each specific numerical value for every social layer from closest to most distant, the scaling ratio between successive layers, and the name of the theoretical framework. Be numerically precise.",
    },
    {
        "id": "d06",
        "question": "What is the Overton Window and who actually developed the concept?",
        "correct_answer": "Joseph Overton, Mackinac Center, term coined posthumously after 2003",
        "grounded": "The Overton Window describes the range of policies politically acceptable to the mainstream population at a given time. The concept was developed by Joseph P. Overton while working at the Mackinac Center for Public Policy in Michigan. The term Overton Window was actually coined posthumously by his colleagues after his death in a 2003 ultralight aircraft accident.",
        "irrelevant": "The discovery of penicillin by Alexander Fleming in 1928 at Saint Mary's Hospital London revolutionized medicine. Fleming noticed that a Penicillium mould contaminating a Staphylococcus culture plate had created a bacteria-free zone around itself. Howard Florey and Ernst Boris Chain later developed methods for mass production during World War Two.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the specific person who developed this concept, the organization they worked for, the circumstances under which the term was actually coined and by whom, and explain why the naming history matters for understanding the concept accurately.",
    },
    {
        "id": "d07",
        "question": "What is the Ringelmann Effect, when was it discovered, and what were the specific experimental findings?",
        "correct_answer": "Maximilien Ringelmann, ~1913, rope-pulling, groups of 8 at 49% individual capacity",
        "grounded": "The Ringelmann Effect demonstrates that individual effort decreases as group size increases, a phenomenon now called social loafing. It was discovered by French agricultural engineer Maximilien Ringelmann around 1913 through rope-pulling experiments. He found that groups of eight people pulled at only forty-nine percent of their combined individual capacity.",
        "irrelevant": "The process of nuclear fusion in the Sun's core converts hydrogen into helium at temperatures of approximately fifteen million degrees Celsius. Every second the Sun converts about six hundred million tons of hydrogen into helium, releasing energy according to Einstein's mass-energy equivalence equation. This process has continued for approximately four point six billion years.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the researcher's full name and nationality, the approximate year of discovery, the specific experimental methodology used, and the precise quantitative finding about group performance relative to individual capacity. Be numerically specific.",
    },
    {
        "id": "d08",
        "question": "Who developed the Delphi method and at which institution?",
        "correct_answer": "Norman Dalkey and Olaf Helmer, RAND Corporation, 1950s/1963",
        "grounded": "The Delphi method was developed by Norman Dalkey and Olaf Helmer at the RAND Corporation during the 1950s, with their key publication appearing in 1963. The method uses anonymous expert panels, iterative rounds of questioning with controlled feedback, and statistical aggregation of responses to achieve structured group consensus without face-to-face interaction.",
        "irrelevant": "Bioluminescence is the production and emission of light by living organisms through chemical reactions. In deep-sea environments, over ninety percent of marine organisms produce some form of bioluminescence. The reaction typically involves the oxidation of a light-emitting molecule called luciferin by the enzyme luciferase, with variations across species.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the specific researchers who developed this method, the institution where it was created, the decade of its origin and year of key publication, and the essential methodological features that distinguish it from other group decision methods.",
    },
    {
        "id": "d09",
        "question": "What is Ashby's Law of Requisite Variety and what is its formal statement?",
        "correct_answer": "W. Ross Ashby, 1956, Introduction to Cybernetics, only variety absorbs variety",
        "grounded": "Ashby's Law of Requisite Variety states that only variety can absorb variety. A controller must have at least as much variety of possible states as the system it attempts to control. It was formulated by W. Ross Ashby in his 1956 book An Introduction to Cybernetics. The formal statement requires that the logarithm of the variety of disturbances be less than or equal to the logarithm of the variety of responses available to the controller.",
        "irrelevant": "The Voyager 1 spacecraft launched by NASA on September 5 1977 has become the most distant human-made object from Earth, now traveling through interstellar space at approximately seventeen kilometers per second. It carries a golden record containing sounds and images selected to portray the diversity of life and culture on Earth, curated by a committee chaired by Carl Sagan.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the researcher's full name, the year and title of the publication where the law was first formulated, the formal mathematical or logical statement of the law, and explain the practical implications for control systems. Be precise about the formal statement.",
    },
    {
        "id": "d10",
        "question": "What is the Gell-Mann Amnesia Effect and who coined the term?",
        "correct_answer": "Michael Crichton, 2002 speech, named after Murray Gell-Mann, not a formal bias",
        "grounded": "The Gell-Mann Amnesia Effect describes reading a newspaper article about a topic you know well, noticing it is full of errors and misrepresentations, then turning the page and reading the next article on a topic you know less about as if it were perfectly accurate. The term was coined by author Michael Crichton in a 2002 speech, named after physicist Murray Gell-Mann. It is not a formally studied cognitive bias but an informal observation about media trust.",
        "irrelevant": "Coral reef ecosystems support approximately twenty-five percent of all marine species despite covering less than one percent of the ocean floor. Coral bleaching occurs when rising water temperatures cause corals to expel their symbiotic zooxanthellae algae, turning white and becoming vulnerable to disease. Mass bleaching events have accelerated since the late twentieth century.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include who specifically coined this term, when and in what context they introduced it, who the effect is named after and why, and clarify whether this is a formally studied cognitive bias or an informal observation. Be precise about the origin story.",
    },
    {
        "id": "d11",
        "question": "What is the Tocqueville Effect and what historical event illustrates it?",
        "correct_answer": "Alexis de Tocqueville, French Revolution, L'Ancien Regime 1856, revolutions when conditions improve",
        "grounded": "The Tocqueville Effect states that revolutions tend to occur not when conditions are at their worst but when they are improving, because rising expectations outpace the actual pace of improvement. Alexis de Tocqueville observed this pattern while analyzing the French Revolution in his 1856 work L'Ancien Regime et la Revolution, noting that France was more prosperous in the decades before 1789 than in previous centuries.",
        "irrelevant": "The Amazon River basin contains approximately ten percent of all species on Earth and produces roughly twenty percent of the world's river discharge into the ocean. The annual flood cycle creates a unique ecosystem called the varzea, where forests are submerged for months. Indigenous communities have developed sophisticated agricultural systems adapted to these seasonal flooding patterns for thousands of years.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the specific thinker who identified this pattern, the year and title of the work in which it was published, the specific historical revolution used to illustrate it, and explain the psychological mechanism of rising expectations. Be historically precise.",
    },
    {
        "id": "d12",
        "question": "What is the Shirky Principle?",
        "correct_answer": "Institutions preserve the problem they are the solution to. Clay Shirky, named by Kevin Kelly.",
        "grounded": "The Shirky Principle states that institutions will try to preserve the problem to which they are the solution. It is named after internet theorist Clay Shirky, though the term itself was coined by Kevin Kelly of Wired magazine. The principle explains why organizations often resist innovations that would eliminate the need for their services, even when those innovations would serve the public good.",
        "irrelevant": "The Rosetta Stone discovered in 1799 by French soldiers in the Egyptian town of Rashid contains the same decree written in three scripts: Ancient Egyptian hieroglyphics, Demotic script, and Ancient Greek. Jean-Francois Champollion used the Greek text as a key to decipher the hieroglyphics in 1822, opening the field of modern Egyptology.",
        "padding": "Please provide a detailed and comprehensive answer to this question. Include the person this principle is named after, who actually coined the term and in what context, the specific institutional behavior it describes, and provide an example of how this principle manifests in practice. Be precise about attribution.",
    },
]


# ── Experiment Runner ─────────────────────────────────────────────────────────

CLAMPED_LENGTH = 200  # Exact number of generated tokens for ALL conditions


def run_experiment(model_name, questions, output_dir):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"G06v2: Vocabulary Compression — Generation Length CLAMPED")
    print(f"Model: {model_name}")
    print(f"Clamped generation length: {CLAMPED_LENGTH} tokens (all conditions)")
    print(f"Questions: {len(questions)} x 3 conditions = {len(questions)*3} inferences")
    print(f"{'='*60}\n")

    print("Loading model...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )
    model.config.use_cache = True
    n_layers = model.config.num_hidden_layers
    print(f"Loaded in {time.time()-t0:.1f}s ({sum(p.numel() for p in model.parameters()):,} params, {n_layers} layers)")
    print(f"Device map: {model.hf_device_map if hasattr(model, 'hf_device_map') else 'single device'}\n")

    # Suppress EOS so model cannot stop early
    if tokenizer.eos_token_id is not None:
        suppress_ids = [tokenizer.eos_token_id]
        print(f"Suppressing EOS token {tokenizer.eos_token_id} to force exactly {CLAMPED_LENGTH} tokens\n")
    else:
        suppress_ids = None
        print("WARNING: No EOS token found — model may already generate full length\n")

    # Token length check on prompts
    print("Prompt token lengths:")
    for q in questions:
        prompts = {
            "padded": f"{q['padding']}\n\n{q['question']}",
            "grounded": f"Given this context:\n{q['grounded']}\n\nNow answer this question:\n\n{q['question']}",
            "irrelevant": f"Given this context:\n{q['irrelevant']}\n\nNow answer this question:\n\n{q['question']}",
        }
        lens = {k: len(tokenizer.encode(v)) for k, v in prompts.items()}
        print(f"  {q['id']}: pad={lens['padded']} ground={lens['grounded']} irrel={lens['irrelevant']}")
    print()

    results = []
    for i, q in enumerate(questions):
        print(f"--- Question {i+1}/{len(questions)}: {q['id']} ---")
        print(f"  Correct answer: {q['correct_answer']}")

        prompts = {
            "padded": f"{q['padding']}\n\n{q['question']}",
            "grounded": f"Given this context:\n{q['grounded']}\n\nNow answer this question:\n\n{q['question']}",
            "irrelevant": f"Given this context:\n{q['irrelevant']}\n\nNow answer this question:\n\n{q['question']}",
        }

        for condition, prompt in prompts.items():
            print(f"  {condition}...", end=" ", flush=True)
            t1 = time.time()

            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

            with torch.no_grad():
                # Prompt encoding — hidden states from forward pass
                enc_out = model(**inputs, output_hidden_states=True)
                prompt_metrics = extract_layer_metrics(enc_out.hidden_states)

                # Generation with CLAMPED length — exactly CLAMPED_LENGTH tokens
                gen_kwargs = dict(
                    **inputs,
                    min_new_tokens=CLAMPED_LENGTH,
                    max_new_tokens=CLAMPED_LENGTH,
                    do_sample=False,
                    output_hidden_states=True,
                    return_dict_in_generate=True,
                )
                # Suppress EOS to prevent early stopping
                if suppress_ids is not None:
                    gen_kwargs["suppress_tokens"] = suppress_ids

                gen_out = model.generate(**gen_kwargs)

            # Generation trajectory metrics (accumulated across all gen tokens)
            gen_traj = extract_generation_trajectory(gen_out, n_layers)

            generated_ids = gen_out.sequences[0][inputs.input_ids.shape[1]:]
            generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)
            n_gen = len(generated_ids)

            elapsed = time.time() - t1

            # Verify clamped length
            length_ok = "OK" if n_gen == CLAMPED_LENGTH else f"MISMATCH (expected {CLAMPED_LENGTH})"
            print(f"{elapsed:.1f}s | {inputs.input_ids.shape[1]} prompt / {n_gen} gen tokens [{length_ok}]")

            if n_gen != CLAMPED_LENGTH:
                print(f"    WARNING: Generated {n_gen} tokens, expected {CLAMPED_LENGTH}")

            results.append({
                "question_id": q["id"],
                "correct_answer": q["correct_answer"],
                "condition": condition,
                "generated_text": generated_text[:600],
                "prompt_encoding_metrics": prompt_metrics,
                "generation_trajectory_metrics": gen_traj,
                "elapsed_seconds": elapsed,
                "model": model_name,
                "n_prompt_tokens": inputs.input_ids.shape[1],
                "n_generated_tokens": n_gen,
                "clamped_target": CLAMPED_LENGTH,
                "length_matched": n_gen == CLAMPED_LENGTH,
                "timestamp": datetime.now(UTC).isoformat(),
                "experiment": "G06v2",
            })

            del enc_out, gen_out
            torch.cuda.empty_cache()

    # Save results
    os.makedirs(output_dir, exist_ok=True)
    slug = model_name.replace("/", "_")
    path = os.path.join(output_dir, f"g06v2_{slug}.jsonl")
    with open(path, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nResults saved to {path}")

    # Verify all lengths matched
    mismatches = [r for r in results if not r["length_matched"]]
    if mismatches:
        print(f"\nWARNING: {len(mismatches)}/{len(results)} inferences had length mismatches!")
        for m in mismatches:
            print(f"  {m['question_id']}/{m['condition']}: got {m['n_generated_tokens']}")
    else:
        print(f"\nAll {len(results)} inferences generated exactly {CLAMPED_LENGTH} tokens.")

    return results


# ── Analysis ──────────────────────────────────────────────────────────────────

def analyze(results):
    print(f"\n{'='*60}")
    print("G06v2 ANALYSIS: Vocabulary Compression — Length CLAMPED")
    print(f"{'='*60}")

    questions = {}
    for r in results:
        qid = r["question_id"]
        if qid not in questions:
            questions[qid] = {}
        questions[qid][r["condition"]] = r

    # Verify length control
    print("\nGeneration lengths (should ALL be identical):")
    for cond in ["padded", "grounded", "irrelevant"]:
        toks = [q[cond]["n_generated_tokens"] for q in questions.values() if cond in q]
        if toks:
            print(f"  {cond}: mean={np.mean(toks):.1f} (range {min(toks)}-{max(toks)})")
    mismatches = sum(1 for r in results if not r.get("length_matched", True))
    if mismatches:
        print(f"  *** {mismatches} LENGTH MISMATCHES — results may still have confound ***")
    else:
        print(f"  All {len(results)} inferences: exactly {results[0].get('clamped_target', '?')} tokens. Length confound eliminated.")

    # Prompt token lengths (for reference — these vary by design)
    print("\nPrompt token lengths (input, varies by design):")
    for cond in ["padded", "grounded", "irrelevant"]:
        toks = [q[cond]["n_prompt_tokens"] for q in questions.values() if cond in q]
        if toks:
            print(f"  {cond}: mean={np.mean(toks):.1f} (range {min(toks)}-{max(toks)})")

    for stage_name, mkey in [("PROMPT ENCODING", "prompt_encoding_metrics"),
                              ("GENERATION TRAJECTORY", "generation_trajectory_metrics")]:
        print(f"\n{'='*60}")
        print(f"Stage: {stage_name}")
        print(f"{'='*60}")

        metrics = ["rankme", "alpha_req", "directional_coherence", "mean_norm"]

        for metric in metrics:
            pad_v, gnd_v, irr_v = [], [], []

            for qid, conds in questions.items():
                if not all(c in conds for c in ["padded", "grounded", "irrelevant"]):
                    continue
                for cond_name, val_list in [("padded", pad_v), ("grounded", gnd_v), ("irrelevant", irr_v)]:
                    mdata = conds[cond_name].get(mkey, {})
                    if not mdata:
                        continue
                    if isinstance(mdata, dict) and "rankme" in mdata:
                        # Single dict (generation trajectory)
                        val = mdata.get(metric)
                        if val is not None and not np.isnan(val):
                            val_list.append(val)
                    else:
                        # Dict of layers (prompt encoding)
                        layer_vals = [v[metric] for v in mdata.values()
                                      if isinstance(v, dict) and not np.isnan(v.get(metric, float('nan')))]
                        if layer_vals:
                            val_list.append(np.mean(layer_vals))

            n = min(len(pad_v), len(gnd_v), len(irr_v))
            if n < 3:
                print(f"\n{metric}: insufficient data (p={len(pad_v)}, g={len(gnd_v)}, i={len(irr_v)})")
                continue

            p, g, ir = np.array(pad_v[:n]), np.array(gnd_v[:n]), np.array(irr_v[:n])

            t_pg, p_pg = stats.ttest_rel(p, g)
            t_pi, p_pi = stats.ttest_rel(p, ir)
            t_gi, p_gi = stats.ttest_rel(g, ir)

            d_pg = (p - g).mean() / (p - g).std() if (p - g).std() > 0 else 0
            d_pi = (p - ir).mean() / (p - ir).std() if (p - ir).std() > 0 else 0
            d_gi = (g - ir).mean() / (g - ir).std() if (g - ir).std() > 0 else 0

            print(f"\n{metric}:")
            print(f"  Padded:     {p.mean():.4f} (sd={p.std():.4f})")
            print(f"  Grounded:   {g.mean():.4f} (sd={g.std():.4f})")
            print(f"  Irrelevant: {ir.mean():.4f} (sd={ir.std():.4f})")
            print(f"  ---")
            print(f"  Padded vs Grounded:     d={d_pg:.3f}, p={p_pg:.6f}")
            print(f"  Padded vs Irrelevant:   d={d_pi:.3f}, p={p_pi:.6f}")
            print(f"  Grounded vs Irrelevant: d={d_gi:.3f}, p={p_gi:.6f}  *** KEY ***")

            if stage_name == "GENERATION TRAJECTORY" and metric == "rankme":
                print(f"\n  G06 reference (uncontrolled length): RankMe 145→90, d=-1.49")
                if p_gi < 0.05:
                    print(f"  G06v2 (clamped length):              d={d_gi:.3f}")
                    print(f"  >>> VOCABULARY COMPRESSION SURVIVES LENGTH CONTROL")
                else:
                    print(f"  G06v2 (clamped length):              d={d_gi:.3f}, p={p_gi:.4f}")
                    print(f"  >>> Effect did NOT survive length control — G06 was confounded")
            elif p_gi < 0.05:
                print(f"  >>> VOCABULARY EFFECT beyond length (on confabulation questions)")
            elif p_pg < 0.05 and p_pi < 0.05 and abs(d_pg - d_pi) < 0.5:
                print(f"  >>> LENGTH/CONTEXT EFFECT only")
            elif p_pg < 0.05 and p_pi >= 0.05:
                print(f"  >>> VOCABULARY EFFECT (only grounded differs from padded)")
            else:
                print(f"  >>> INCONCLUSIVE")

    # Answer quality check
    print(f"\n{'='*60}")
    print("ANSWER QUALITY (did the model confabulate?)")
    print(f"{'='*60}")
    for qid in sorted(questions.keys()):
        conds = questions[qid]
        print(f"\n{qid} — expected: {conds['padded']['correct_answer']}")
        for c in ["padded", "grounded", "irrelevant"]:
            if c in conds:
                print(f"  {c:12s}: {conds[c]['generated_text'][:120]}...")


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="G06v2: Vocabulary compression with clamped generation length")
    parser.add_argument("model", nargs="?", default="Qwen/Qwen2.5-7B-Instruct",
                        help="HuggingFace model name (default: Qwen/Qwen2.5-7B-Instruct)")
    parser.add_argument("output_dir", nargs="?", default=os.path.expanduser("~/experiments/g06v2-results"),
                        help="Output directory (default: ~/experiments/g06v2-results)")
    args = parser.parse_args()

    results = run_experiment(args.model, QUESTIONS, args.output_dir)
    analyze(results)
