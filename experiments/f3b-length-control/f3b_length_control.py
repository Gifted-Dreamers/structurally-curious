#!/usr/bin/env python3
"""
F3b: Length-Controlled Vocabulary-as-Compression Experiment

F3 found massive geometric differences between confabulation and grounded
conditions, but grounded prompts were 2.3x longer. This control isolates
the vocabulary effect from the length effect.

Three conditions per question:
A. CONFABULATION: question only (~27 tokens)
B. GROUNDED: question + correct structural name (~63 tokens)
C. IRRELEVANT: question + irrelevant context of MATCHED length (~63 tokens)

If B differs from A but C does not: LENGTH explains the difference, not vocabulary.
If B and C both differ from A similarly: LENGTH is the driver.
If B differs from A AND from C: VOCABULARY has an effect beyond length.

This is the critical control that F3 was missing.
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
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_i, log_sv)
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
    top_k_var = (S[:k] ** 2).sum().item()
    return top_k_var / total_var


def extract_metrics(hidden_states, layer_indices=None):
    if layer_indices is None:
        n_layers = len(hidden_states) - 1
        start = max(1, int(n_layers * 0.75))
        layer_indices = list(range(start, n_layers + 1))
    results = {}
    for layer_idx in layer_indices:
        hs = hidden_states[layer_idx]
        matrix = hs.squeeze(0).float()
        matrix_centered = matrix - matrix.mean(dim=0, keepdim=True)
        try:
            U, S, Vh = torch.linalg.svd(matrix_centered, full_matrices=False)
        except Exception as e:
            print(f"  SVD failed on layer {layer_idx}: {e}")
            continue
        results[f"layer_{layer_idx}"] = {
            "rankme": compute_rankme(S),
            "alpha_req": compute_alpha_req(S),
            "directional_coherence": compute_directional_coherence(hs),
            "mean_norm": matrix.norm(dim=-1).mean().item(),
            "norm_variance": matrix.norm(dim=-1).var().item(),
        }
    return results


# Each question has three prompts: confabulation, grounded, irrelevant (length-matched)
QUESTIONS = [
    {"id": "q01", "question": "What is the psychological term for when someone cannot recognize faces despite having normal vision?",
     "structural_name": "The condition is called prosopagnosia (face blindness). It results from damage to the fusiform face area in the temporal lobe.",
     "irrelevant": "The migration patterns of Arctic terns cover approximately 44,000 miles annually. They breed in northern regions during summer months.",
     "domain": "psychology"},
    {"id": "q02", "question": "In organizational theory, what is the name for the phenomenon where adding more people to a late project makes it later?",
     "structural_name": "This is Brooks's Law, from Fred Brooks' The Mythical Man-Month (1975). The mechanism is communication overhead scaling as n(n-1)/2.",
     "irrelevant": "The average depth of the Pacific Ocean is approximately 14,000 feet. The Mariana Trench reaches depths exceeding 36,000 feet at its deepest point.",
     "domain": "management"},
    {"id": "q03", "question": "What is the term for the cognitive bias where people overestimate how much others notice their appearance or behavior?",
     "structural_name": "This is the spotlight effect, studied by Gilovich, Medvec and Savitsky (2000). Related to anchoring on one's own experience.",
     "irrelevant": "Photosynthesis converts carbon dioxide and water into glucose and oxygen using sunlight energy captured by chlorophyll molecules in plant cells.",
     "domain": "psychology"},
    {"id": "q04", "question": "In ecology, what is the term for a species whose removal causes disproportionate ecosystem collapse?",
     "structural_name": "This is a keystone species, concept introduced by Robert Paine (1969) studying Pisaster sea stars in tidal pools.",
     "irrelevant": "The International Space Station orbits Earth at approximately 17,500 miles per hour, completing one full orbit every ninety minutes.",
     "domain": "ecology"},
    {"id": "q05", "question": "What is the name for the linguistic phenomenon where a word temporarily loses all meaning when you repeat it?",
     "structural_name": "This is semantic satiation (also called semantic saturation), first studied by Leon Jakobovits James (1962).",
     "irrelevant": "Volcanic eruptions on the island of Iceland are caused by the Mid-Atlantic Ridge and a mantle plume creating significant geothermal activity.",
     "domain": "linguistics"},
    {"id": "q06", "question": "In economics, what principle states that bad money drives out good money from circulation?",
     "structural_name": "This is Gresham's Law, attributed to Sir Thomas Gresham (1558). Overvalued money circulates while undervalued money is hoarded.",
     "irrelevant": "The process of fermentation converts sugars into ethanol and carbon dioxide. It has been used in bread making and brewing for thousands of years.",
     "domain": "economics"},
    {"id": "q07", "question": "What is the name for the paradox where the more choices people have, the less satisfied they are with their selection?",
     "structural_name": "This is the paradox of choice, formalized by Barry Schwartz (2004). Related to maximizing vs satisficing (Herbert Simon).",
     "irrelevant": "The tallest mountain measured from base to peak is Mauna Kea in Hawaii, extending approximately 33,500 feet from the ocean floor.",
     "domain": "psychology"},
    {"id": "q08", "question": "In network science, what is the term for an individual who bridges otherwise disconnected groups?",
     "structural_name": "This is a structural hole broker, concept from Ronald Burt (1992, Structural Holes). Bridges provide information and control benefits.",
     "irrelevant": "The circulatory system of a blue whale pumps approximately 60 gallons of blood per heartbeat through vessels spanning thousands of miles.",
     "domain": "sociology"},
    {"id": "q09", "question": "What is the formal name for the phenomenon where a system's rules evolve to protect the system rather than serve its original purpose?",
     "structural_name": "This is goal displacement (Robert Merton, 1957). Donella Meadows calls this the system resisting its own reform and identifies leverage points for intervention.",
     "irrelevant": "The manufacturing process for silicon wafers involves growing single crystal ingots at temperatures exceeding 1400 degrees Celsius in controlled atmospheric conditions over many hours.",
     "domain": "systems_theory"},
    {"id": "q10", "question": "In information theory, what is the name for the minimum number of yes/no questions needed to identify an item from a set?",
     "structural_name": "This is Shannon entropy (Claude Shannon, 1948), measured in bits. For uniform distribution over N items, entropy = log2(N).",
     "irrelevant": "Jupiter's Great Red Spot is a persistent anticyclonic storm larger than Earth that has been observed continuously since at least 1831.",
     "domain": "information_theory"},
    {"id": "q11", "question": "What term describes the phenomenon where people who know the outcome believe they would have predicted it?",
     "structural_name": "This is hindsight bias (Fischhoff, 1975), also called the knew-it-all-along effect. Distinct from confirmation bias.",
     "irrelevant": "The construction of the Panama Canal required excavation of over 200 million cubic yards of earth and rock over a ten year period.",
     "domain": "psychology"},
    {"id": "q12", "question": "In sociology, what is the term for when a false belief causes behavior that makes the false belief come true?",
     "structural_name": "This is a self-fulfilling prophecy (Robert K. Merton, 1948). The Thomas theorem underlies it.",
     "irrelevant": "Honey never spoils due to its low moisture content and acidic pH which create an inhospitable environment for bacteria.",
     "domain": "sociology"},
    {"id": "q13", "question": "What is the name for the principle that in any hierarchy, people tend to rise to their level of incompetence?",
     "structural_name": "This is the Peter Principle (Laurence J. Peter, 1969). People are promoted based on current role performance, not predicted next-role performance.",
     "irrelevant": "The speed of light in a vacuum is approximately 186,282 miles per second. Light from the Sun takes about eight minutes to reach Earth.",
     "domain": "management"},
    {"id": "q14", "question": "In neuroscience, what is the term for the brain's ability to reorganize by forming new neural connections throughout life?",
     "structural_name": "This is neuroplasticity. Key researchers include Donald Hebb (1949), Michael Merzenich, and Paul Bach-y-Rita.",
     "irrelevant": "The Amazon River discharges approximately 209,000 cubic meters of water per second into the Atlantic Ocean at its mouth.",
     "domain": "neuroscience"},
    {"id": "q15", "question": "What is the principle in design that states the most efficient systems tend to be the most fragile?",
     "structural_name": "This is the efficiency-resilience tradeoff, formalized by Robert Ulanowicz and applied by Nassim Taleb as antifragility. Bernard Lietaer applied it to monetary systems.",
     "irrelevant": "The Voyager 1 spacecraft launched in 1977 has traveled over 15 billion miles from Earth and entered interstellar space in 2012 carrying a golden record of sounds.",
     "domain": "systems_theory"},
    {"id": "q16", "question": "In affect science, what is the term for the finding that people who can precisely name their emotions are more resilient?",
     "structural_name": "This is emotional granularity (Lisa Feldman Barrett, 2001+). Related: affect labeling (Lieberman et al., 2007) reduces amygdala activation.",
     "irrelevant": "The process of plate tectonics moves continental plates at rates of one to ten centimeters per year driven by convection currents in the mantle.",
     "domain": "psychology"},
    {"id": "q17", "question": "What is the name for the phenomenon where members of a group prioritize consensus over critical evaluation?",
     "structural_name": "This is groupthink (Irving Janis, 1972). Studied via Bay of Pigs, Challenger disaster.",
     "irrelevant": "Octopuses have three hearts and blue blood due to copper-based hemocyanin that is more efficient at transporting oxygen in cold water.",
     "domain": "psychology"},
    {"id": "q18", "question": "In governance theory, what are the eight design principles for managing shared resources without privatization or centralized control?",
     "structural_name": "These are Elinor Ostrom's eight design principles for governing the commons (1990), including clearly defined boundaries, monitoring, graduated sanctions, and nested enterprises.",
     "irrelevant": "The human body contains approximately 37 trillion cells that collectively perform thousands of biochemical reactions per second to maintain homeostasis and support life functions.",
     "domain": "governance"},
    {"id": "q19", "question": "What is the term for leverage points in a system where a small intervention can produce large systemic change?",
     "structural_name": "These are leverage points, systematized by Donella Meadows (1999). 12 points ranked from parameters (weakest) to paradigm transcendence (strongest).",
     "irrelevant": "The Great Barrier Reef stretches over 1,400 miles along the northeastern coast of Australia and contains over 2,900 individual reef systems and hundreds of islands.",
     "domain": "systems_theory"},
    {"id": "q20", "question": "In cult research, what is the model that categorizes undue influence along four dimensions of control?",
     "structural_name": "This is the BITE Model (Steven Hassan, 1988/2000). Four dimensions: Behavior, Information, Thought, Emotional control.",
     "irrelevant": "The temperature at the center of the Sun reaches approximately 27 million degrees Fahrenheit sustained by nuclear fusion converting hydrogen to helium.",
     "domain": "psychology"},
]


def run_experiment(model_name, questions, output_dir, device="cpu"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"F3b: Length-Controlled Vocabulary Compression")
    print(f"Model: {model_name}")
    print(f"Questions: {len(questions)} x 3 conditions = {len(questions)*3} inferences")
    print(f"{'='*60}\n")

    print("Loading model...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, dtype=torch.float32, device_map=device, trust_remote_code=True)
    model.config.use_cache = True
    print(f"Loaded in {time.time()-t0:.1f}s ({sum(p.numel() for p in model.parameters()):,} params)")

    results = []

    for i, q in enumerate(questions):
        print(f"\n--- Question {i+1}/{len(questions)}: {q['id']} ({q['domain']}) ---")

        prompts = {
            "confabulation": f"Answer this question thoroughly and confidently:\n\n{q['question']}",
            "grounded": f"Given this context:\n{q['structural_name']}\n\nNow answer this question thoroughly:\n\n{q['question']}",
            "irrelevant": f"Given this context:\n{q['irrelevant']}\n\nNow answer this question thoroughly:\n\n{q['question']}",
        }

        for condition, prompt in prompts.items():
            print(f"  {condition}...", end=" ", flush=True)
            t1 = time.time()

            inputs = tokenizer(prompt, return_tensors="pt").to(device)

            with torch.no_grad():
                encoding_outputs = model(**inputs, output_hidden_states=True)
                prompt_hidden_states = encoding_outputs.hidden_states

                gen_outputs = model.generate(
                    **inputs, max_new_tokens=150, do_sample=False,
                    output_hidden_states=True, return_dict_in_generate=True)

            prompt_metrics = extract_metrics(prompt_hidden_states)

            if gen_outputs.hidden_states and len(gen_outputs.hidden_states) > 1:
                last_step_hs = gen_outputs.hidden_states[-1]
                gen_metrics = extract_metrics(last_step_hs)
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
                "generated_text": generated_text[:500],
                "prompt_encoding_metrics": prompt_metrics,
                "generation_metrics": gen_metrics,
                "elapsed_seconds": elapsed,
                "model": model_name,
                "n_prompt_tokens": inputs.input_ids.shape[1],
                "n_generated_tokens": len(generated_ids),
                "timestamp": datetime.now(UTC).isoformat(),
            })

            del encoding_outputs, gen_outputs, prompt_hidden_states

    os.makedirs(output_dir, exist_ok=True)
    model_slug = model_name.replace("/", "_")
    output_path = os.path.join(output_dir, f"f3b_{model_slug}.jsonl")
    with open(output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nResults saved to {output_path}")
    return results


def analyze_results(results):
    print(f"\n{'='*60}")
    print("F3b ANALYSIS: Length-Controlled Vocabulary Compression")
    print(f"{'='*60}\n")

    # Group by question
    questions = {}
    for r in results:
        qid = r["question_id"]
        if qid not in questions:
            questions[qid] = {}
        questions[qid][r["condition"]] = r

    # Report token lengths
    for cond in ["confabulation", "grounded", "irrelevant"]:
        tokens = [q[cond]["n_prompt_tokens"] for q in questions.values() if cond in q]
        print(f"{cond}: mean={np.mean(tokens):.1f} tokens (range {min(tokens)}-{max(tokens)})")
    print()

    metrics = ["rankme", "alpha_req", "directional_coherence", "mean_norm"]
    summary = {}

    for metric in metrics:
        confab_vals, grounded_vals, irrelevant_vals = [], [], []

        for qid, conditions in questions.items():
            if not all(c in conditions for c in ["confabulation", "grounded", "irrelevant"]):
                continue
            for cond, vals in [("confabulation", confab_vals), ("grounded", grounded_vals), ("irrelevant", irrelevant_vals)]:
                layers = conditions[cond]["prompt_encoding_metrics"]
                layer_vals = [v[metric] for v in layers.values() if not np.isnan(v.get(metric, float('nan')))]
                if layer_vals:
                    vals.append(np.mean(layer_vals))

        if len(confab_vals) < 3:
            print(f"{metric}: insufficient data")
            continue

        c, g, ir = np.array(confab_vals), np.array(grounded_vals), np.array(irrelevant_vals)

        # Three paired comparisons
        t_cg, p_cg = stats.ttest_rel(c, g)  # confab vs grounded
        t_ci, p_ci = stats.ttest_rel(c, ir)  # confab vs irrelevant
        t_gi, p_gi = stats.ttest_rel(g, ir)  # grounded vs irrelevant (THE KEY TEST)

        d_cg = (c - g).mean() / (c - g).std() if (c - g).std() > 0 else 0
        d_ci = (c - ir).mean() / (c - ir).std() if (c - ir).std() > 0 else 0
        d_gi = (g - ir).mean() / (g - ir).std() if (g - ir).std() > 0 else 0

        print(f"\n{metric}:")
        print(f"  Confabulation:  {c.mean():.4f} (sd={c.std():.4f})")
        print(f"  Grounded:       {g.mean():.4f} (sd={g.std():.4f})")
        print(f"  Irrelevant:     {ir.mean():.4f} (sd={ir.std():.4f})")
        print(f"  ---")
        print(f"  Confab vs Grounded:    d={d_cg:.3f}, p={p_cg:.6f}")
        print(f"  Confab vs Irrelevant:  d={d_ci:.3f}, p={p_ci:.6f}")
        print(f"  Grounded vs Irrelevant: d={d_gi:.3f}, p={p_gi:.6f}  *** KEY TEST ***")

        # Interpretation
        if p_gi < 0.05:
            print(f"  >>> VOCABULARY EFFECT: grounded differs from irrelevant (same length, different content)")
        elif p_cg < 0.05 and p_ci < 0.05:
            print(f"  >>> LENGTH EFFECT: both grounded and irrelevant differ from confab similarly")
        elif p_cg < 0.05 and p_ci >= 0.05:
            print(f"  >>> VOCABULARY EFFECT: only grounded (not irrelevant) differs from confab")
        else:
            print(f"  >>> INCONCLUSIVE")

        summary[metric] = {
            "confab_mean": float(c.mean()), "grounded_mean": float(g.mean()), "irrelevant_mean": float(ir.mean()),
            "confab_vs_grounded": {"d": float(d_cg), "p": float(p_cg)},
            "confab_vs_irrelevant": {"d": float(d_ci), "p": float(p_ci)},
            "grounded_vs_irrelevant": {"d": float(d_gi), "p": float(p_gi)},
            "n": len(confab_vals),
        }

    print(f"\n{'='*60}")
    print("INTERPRETATION GUIDE:")
    print("  If Grounded vs Irrelevant is significant: vocabulary changes geometry beyond length")
    print("  If only Confab vs both others: it's a length effect, not vocabulary")
    print("  The KEY comparison is Grounded vs Irrelevant (same length, different relevance)")
    print(f"{'='*60}")

    return summary


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/experiments/f3b-results")

    results = run_experiment(model_name, QUESTIONS, output_dir)
    summary = analyze_results(results)

    summary_path = os.path.join(output_dir, f"f3b_summary_{model_name.replace('/', '_')}.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to {summary_path}")
