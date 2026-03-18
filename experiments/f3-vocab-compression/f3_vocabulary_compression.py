#!/usr/bin/env python3
"""
F3: Vocabulary-as-Compression Falsification Experiment

Tests the spec's core claim: providing a structural name produces measurable
rank compression in model hidden states.

Protocol:
1. Present model with questions it confabulates on
2. Extract hidden states from all layers
3. Compute geometric metrics: RankMe, alpha-ReQ, directional coherence
4. Re-present with the correct structural name provided in context
5. Extract hidden states again
6. Compare geometric metrics between conditions

Kill condition: If geometry doesn't change when the structural name is provided,
vocabulary is output improvement, not structural compression.
"""

import json
import time
import os
import sys
import numpy as np
import torch
from pathlib import Path
from scipy import stats
from datetime import datetime


def compute_rankme(singular_values):
    """RankMe: Von Neumann entropy of normalized singular values.
    Low = compressed. High = expanded."""
    sv = singular_values[singular_values > 1e-10]
    p = sv / sv.sum()
    entropy = -(p * torch.log(p)).sum().item()
    return np.exp(entropy)


def compute_alpha_req(singular_values, min_components=3):
    """alpha-ReQ: power-law decay rate of eigenspectrum.
    Small alpha = spread. Large alpha = concentrated."""
    sv = singular_values[singular_values > 1e-10].cpu().numpy()
    if len(sv) < min_components:
        return float('nan')
    log_i = np.log(np.arange(1, len(sv) + 1))
    log_sv = np.log(sv)
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_i, log_sv)
    return -slope


def compute_directional_coherence(hidden_states_tensor):
    """Ratio of variance in top-k PCs.
    High = structured. Low = diffuse."""
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
    """Extract geometric metrics from model hidden states."""
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


# 20 questions spanning domains relevant to the spec
QUESTIONS = [
    {"id": "q01", "question": "What is the psychological term for when someone cannot recognize faces despite having normal vision?",
     "structural_name": "The condition is called prosopagnosia (face blindness). It results from damage to the fusiform face area in the temporal lobe.", "domain": "psychology"},
    {"id": "q02", "question": "In organizational theory, what is the name for the phenomenon where adding more people to a late project makes it later?",
     "structural_name": "This is Brooks's Law, from Fred Brooks' The Mythical Man-Month (1975). The mechanism is communication overhead scaling as n(n-1)/2.", "domain": "management"},
    {"id": "q03", "question": "What is the term for the cognitive bias where people overestimate how much others notice their appearance or behavior?",
     "structural_name": "This is the spotlight effect, studied by Gilovich, Medvec and Savitsky (2000). Related to anchoring on one's own experience.", "domain": "psychology"},
    {"id": "q04", "question": "In ecology, what is the term for a species whose removal causes disproportionate ecosystem collapse?",
     "structural_name": "This is a keystone species, concept introduced by Robert Paine (1969) studying Pisaster sea stars in tidal pools.", "domain": "ecology"},
    {"id": "q05", "question": "What is the name for the linguistic phenomenon where a word temporarily loses all meaning when you repeat it?",
     "structural_name": "This is semantic satiation (also called semantic saturation), first studied by Leon Jakobovits James (1962).", "domain": "linguistics"},
    {"id": "q06", "question": "In economics, what principle states that bad money drives out good money from circulation?",
     "structural_name": "This is Gresham's Law, attributed to Sir Thomas Gresham (1558). Overvalued money circulates while undervalued money is hoarded.", "domain": "economics"},
    {"id": "q07", "question": "What is the name for the paradox where the more choices people have, the less satisfied they are with their selection?",
     "structural_name": "This is the paradox of choice, formalized by Barry Schwartz (2004). Related to maximizing vs satisficing (Herbert Simon).", "domain": "psychology"},
    {"id": "q08", "question": "In network science, what is the term for an individual who bridges otherwise disconnected groups?",
     "structural_name": "This is a structural hole broker, concept from Ronald Burt (1992, Structural Holes). Bridges provide information and control benefits.", "domain": "sociology"},
    {"id": "q09", "question": "What is the formal name for the phenomenon where a system's rules evolve to protect the system rather than serve its original purpose?",
     "structural_name": "This is goal displacement (Robert Merton, 1957). Donella Meadows calls this the system resisting its own reform and identifies leverage points for intervention.", "domain": "systems_theory"},
    {"id": "q10", "question": "In information theory, what is the name for the minimum number of yes/no questions needed to identify an item from a set?",
     "structural_name": "This is Shannon entropy (Claude Shannon, 1948), measured in bits. For uniform distribution over N items, entropy = log2(N).", "domain": "information_theory"},
    {"id": "q11", "question": "What term describes the phenomenon where people who know the outcome believe they would have predicted it?",
     "structural_name": "This is hindsight bias (Fischhoff, 1975), also called the knew-it-all-along effect. Distinct from confirmation bias.", "domain": "psychology"},
    {"id": "q12", "question": "In sociology, what is the term for when a false belief causes behavior that makes the false belief come true?",
     "structural_name": "This is a self-fulfilling prophecy (Robert K. Merton, 1948). The Thomas theorem underlies it.", "domain": "sociology"},
    {"id": "q13", "question": "What is the name for the principle that in any hierarchy, people tend to rise to their level of incompetence?",
     "structural_name": "This is the Peter Principle (Laurence J. Peter, 1969). People are promoted based on current role performance, not predicted next-role performance.", "domain": "management"},
    {"id": "q14", "question": "In neuroscience, what is the term for the brain's ability to reorganize by forming new neural connections throughout life?",
     "structural_name": "This is neuroplasticity. Key researchers include Donald Hebb (1949), Michael Merzenich, and Paul Bach-y-Rita.", "domain": "neuroscience"},
    {"id": "q15", "question": "What is the principle in design that states the most efficient systems tend to be the most fragile?",
     "structural_name": "This is the efficiency-resilience tradeoff, formalized by Robert Ulanowicz and applied by Nassim Taleb as antifragility. Bernard Lietaer applied it to monetary systems.", "domain": "systems_theory"},
    {"id": "q16", "question": "In affect science, what is the term for the finding that people who can precisely name their emotions are more resilient?",
     "structural_name": "This is emotional granularity (Lisa Feldman Barrett, 2001+). Related: affect labeling (Lieberman et al., 2007) reduces amygdala activation.", "domain": "psychology"},
    {"id": "q17", "question": "What is the name for the phenomenon where members of a group prioritize consensus over critical evaluation?",
     "structural_name": "This is groupthink (Irving Janis, 1972). Studied via Bay of Pigs, Challenger disaster.", "domain": "psychology"},
    {"id": "q18", "question": "In governance theory, what are the eight design principles for managing shared resources without privatization or centralized control?",
     "structural_name": "These are Elinor Ostrom's eight design principles for governing the commons (1990), including clearly defined boundaries, monitoring, graduated sanctions, and nested enterprises.", "domain": "governance"},
    {"id": "q19", "question": "What is the term for leverage points in a system where a small intervention can produce large systemic change?",
     "structural_name": "These are leverage points, systematized by Donella Meadows (1999). 12 points ranked from parameters (weakest) to paradigm transcendence (strongest).", "domain": "systems_theory"},
    {"id": "q20", "question": "In cult research, what is the model that categorizes undue influence along four dimensions of control?",
     "structural_name": "This is the BITE Model (Steven Hassan, 1988/2000). Four dimensions: Behavior, Information, Thought, Emotional control.", "domain": "psychology"},
]


def run_experiment(model_name, questions, output_dir, device="cpu"):
    """Run F3 on a single model."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"Model: {model_name}")
    print(f"Questions: {len(questions)}")
    print(f"{'='*60}\n")

    print("Loading model...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map=device,
        trust_remote_code=True,
    )
    model.config.use_cache = True
    print(f"Model loaded in {time.time()-t0:.1f}s")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"Layers: {model.config.num_hidden_layers}")

    results = []

    for i, q in enumerate(questions):
        print(f"\n--- Question {i+1}/{len(questions)}: {q['id']} ({q['domain']}) ---")

        prompt_a = f"Answer this question thoroughly and confidently:\n\n{q['question']}"
        prompt_b = f"Given this context:\n{q['structural_name']}\n\nNow answer this question thoroughly:\n\n{q['question']}"

        for condition, prompt in [("confabulation", prompt_a), ("grounded", prompt_b)]:
            print(f"  {condition}...", end=" ", flush=True)
            t1 = time.time()

            inputs = tokenizer(prompt, return_tensors="pt").to(device)

            with torch.no_grad():
                # Get hidden states from the prompt encoding (forward pass only)
                encoding_outputs = model(**inputs, output_hidden_states=True)
                prompt_hidden_states = encoding_outputs.hidden_states

                # Also generate a response to check answer quality
                gen_outputs = model.generate(
                    **inputs,
                    max_new_tokens=150,
                    do_sample=False,
                    output_hidden_states=True,
                    return_dict_in_generate=True,
                )

            prompt_metrics = extract_metrics(prompt_hidden_states)

            # Get last generation step hidden states
            if gen_outputs.hidden_states and len(gen_outputs.hidden_states) > 1:
                last_step_hs = gen_outputs.hidden_states[-1]
                gen_metrics = extract_metrics(last_step_hs)
            else:
                gen_metrics = {}

            generated_ids = gen_outputs.sequences[0][inputs.input_ids.shape[1]:]
            generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

            elapsed = time.time() - t1
            print(f"{elapsed:.1f}s | {len(generated_ids)} tokens")

            result = {
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
                "timestamp": datetime.utcnow().isoformat(),
            }
            results.append(result)

            # Free memory
            del encoding_outputs, gen_outputs, prompt_hidden_states
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    # Save results
    os.makedirs(output_dir, exist_ok=True)
    model_slug = model_name.replace("/", "_")
    output_path = os.path.join(output_dir, f"f3_{model_slug}.jsonl")
    with open(output_path, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")

    print(f"\nResults saved to {output_path}")
    return results


def analyze_results(results):
    """Compare geometric metrics between conditions."""
    print(f"\n{'='*60}")
    print("ANALYSIS: Vocabulary-as-Compression")
    print(f"{'='*60}\n")

    questions = {}
    for r in results:
        qid = r["question_id"]
        if qid not in questions:
            questions[qid] = {}
        questions[qid][r["condition"]] = r

    metrics_to_compare = ["rankme", "alpha_req", "directional_coherence", "mean_norm"]

    summary = {}
    for metric in metrics_to_compare:
        confab_values = []
        grounded_values = []

        for qid, conditions in questions.items():
            if "confabulation" not in conditions or "grounded" not in conditions:
                continue
            confab_layers = conditions["confabulation"]["prompt_encoding_metrics"]
            grounded_layers = conditions["grounded"]["prompt_encoding_metrics"]
            c_vals = [v[metric] for v in confab_layers.values()
                      if not np.isnan(v.get(metric, float('nan')))]
            g_vals = [v[metric] for v in grounded_layers.values()
                      if not np.isnan(v.get(metric, float('nan')))]
            if c_vals and g_vals:
                confab_values.append(np.mean(c_vals))
                grounded_values.append(np.mean(g_vals))

        if len(confab_values) < 3:
            print(f"{metric}: insufficient data ({len(confab_values)} pairs)")
            continue

        confab_arr = np.array(confab_values)
        grounded_arr = np.array(grounded_values)
        t_stat, p_value = stats.ttest_rel(confab_arr, grounded_arr)
        diff = confab_arr - grounded_arr
        cohens_d = diff.mean() / diff.std() if diff.std() > 0 else 0

        if metric == "alpha_req":
            direction = "COMPRESSION" if grounded_arr.mean() > confab_arr.mean() else "EXPANSION"
        else:
            direction = "COMPRESSION" if grounded_arr.mean() < confab_arr.mean() else "EXPANSION"

        print(f"\n{metric}:")
        print(f"  Confabulation: {confab_arr.mean():.4f} (sd={confab_arr.std():.4f})")
        print(f"  Grounded:      {grounded_arr.mean():.4f} (sd={grounded_arr.std():.4f})")
        print(f"  Direction:     {direction}")
        print(f"  Cohen's d:     {cohens_d:.4f}")
        print(f"  p-value:       {p_value:.6f}")
        print(f"  n pairs:       {len(confab_values)}")

        if p_value < 0.05 and direction == "COMPRESSION":
            verdict = "SUPPORTS SPEC"
        elif p_value < 0.05:
            verdict = "CONTRADICTS SPEC"
        else:
            verdict = "INCONCLUSIVE"
        print(f"  >>> {verdict}")

        summary[metric] = {
            "confab_mean": float(confab_arr.mean()),
            "grounded_mean": float(grounded_arr.mean()),
            "cohens_d": float(cohens_d),
            "p_value": float(p_value),
            "direction": direction,
            "verdict": verdict,
            "n": len(confab_values),
        }

    print(f"\n{'='*60}")
    print("KILL CONDITIONS:")
    print("  RankMe decreases + alpha-ReQ increases in grounded = SPEC VALIDATED")
    print("  No significant difference = vocabulary helps output, not geometry")
    print("  RankMe increases in grounded = SPEC CONTRADICTED")
    print(f"{'='*60}")

    return summary


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/experiments/f3-results")

    results = run_experiment(model_name, QUESTIONS, output_dir)
    summary = analyze_results(results)

    # Save summary
    summary_path = os.path.join(output_dir, f"f3_summary_{model_name.replace('/', '_')}.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary saved to {summary_path}")
