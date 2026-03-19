#!/usr/bin/env python3
"""
F3c: Vocabulary on Questions the Model Actually Fails

F3 tested vocabulary on questions the model already knew.
F3b controls for length.
F3c tests the REAL claim: does vocabulary change what the model can DO?

Method:
1. Ask 20 questions the model is likely to get wrong (obscure, tricky, or
   requiring specialized knowledge)
2. Condition A: no vocabulary (bare question)
3. Condition B: provide the structural name + brief context
4. Measure: (a) whether the answer improves, (b) geometric redistribution

If redistribution correlates with improved answers, vocabulary is functional
infrastructure, not just geometric noise.
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
        except Exception:
            continue
        results["layer_" + str(layer_idx)] = {
            "rankme": compute_rankme(S),
            "alpha_req": compute_alpha_req(S),
            "directional_coherence": compute_directional_coherence(hs),
            "mean_norm": matrix.norm(dim=1).mean().item(),
            "token_count": matrix.shape[0],
        }
    return results


# Questions designed to be HARD for a 7B model
# Each has a structural name that should help if vocabulary-as-redistribution works
QUESTIONS = [
    {"id": "f01",
     "question": "What is the term for the phenomenon where statistical discrimination becomes self-fulfilling through behavioral adaptation?",
     "structural_name": "This is called stereotype threat, studied by Steele and Aronson (1995). The mechanism is that awareness of a negative stereotype about one's group impairs performance on the stereotyped dimension, which then reinforces the statistical pattern.",
     "correct_answer": "stereotype threat",
     "domain": "psychology"},
    {"id": "f02",
     "question": "What is the name for the mathematical result showing that any sufficiently powerful formal system contains statements that are true but unprovable within the system?",
     "structural_name": "This is Goedel's First Incompleteness Theorem (1931). It applies to any consistent formal system capable of expressing basic arithmetic. The proof constructs a self-referential statement that says 'this statement is not provable.'",
     "correct_answer": "Goedel's incompleteness theorem",
     "domain": "mathematics"},
    {"id": "f03",
     "question": "In network science, what is the term for the minimum number of nodes whose removal disconnects a network, and how does it relate to epidemic thresholds?",
     "structural_name": "The vertex connectivity (or node connectivity) measures network resilience. In scale-free networks, Albert, Jeong and Barabasi (2000) showed targeted removal of high-degree hubs rapidly fragments the network, while random removal has minimal effect. The epidemic threshold in such networks approaches zero (Pastor-Satorras and Vespignani, 2001).",
     "correct_answer": "vertex connectivity / node connectivity",
     "domain": "network_science"},
    {"id": "f04",
     "question": "What is the name for the principle in thermodynamics that states the total entropy of an isolated system can never decrease, and what is the relationship between entropy and information as formalized by Landauer?",
     "structural_name": "The Second Law of Thermodynamics states entropy never decreases in an isolated system. Landauer's Principle (1961) establishes that erasing one bit of information dissipates at least kT ln 2 joules of energy, connecting information processing to thermodynamic entropy.",
     "correct_answer": "second law + Landauer's principle",
     "domain": "physics"},
    {"id": "f05",
     "question": "What is the name for the sociological concept where members of a disadvantaged group internalize and reproduce the very structures that oppress them?",
     "structural_name": "This is internalized oppression, building on Fanon's concept of the colonized mind (Black Skin White Masks, 1952) and Freire's concept of the oppressed hosting the oppressor (Pedagogy of the Oppressed, 1968). Bourdieu's symbolic violence provides the mechanism: domination reproduced through the habitus of the dominated.",
     "correct_answer": "internalized oppression / symbolic violence",
     "domain": "sociology"},
    {"id": "f06",
     "question": "What is the term for the computational complexity class of problems that can be verified in polynomial time but for which no polynomial-time solution is known, and what is the practical significance of the P vs NP question for cryptography?",
     "structural_name": "NP (nondeterministic polynomial time) contains problems verifiable in polynomial time. The P vs NP question asks whether every problem whose solution can be quickly verified can also be quickly solved. If P=NP, most public-key cryptography (RSA, elliptic curve) breaks because factoring and discrete logarithm become easy.",
     "correct_answer": "NP / P vs NP",
     "domain": "computer_science"},
    {"id": "f07",
     "question": "What is the name for the phenomenon in linguistics where a pidgin language develops into a full natural language when children acquire it as their first language?",
     "structural_name": "This is creolization. Derek Bickerton's Language Bioprogram Hypothesis (1981) argues that children exposed to pidgin input generate a full creole grammar from an innate biological program, explaining why creoles worldwide share structural features despite different lexifier languages.",
     "correct_answer": "creolization",
     "domain": "linguistics"},
    {"id": "f08",
     "question": "In decision theory, what is the name for the paradox where a rational agent should accept a series of bets that each individually seem favorable but collectively guarantee ruin?",
     "structural_name": "This is the St. Petersburg paradox in its ergodic economics formulation (Ole Peters, 2019). The resolution is that expected value (ensemble average) diverges from time-average growth rate. Maximizing expected value is rational for an ensemble but irrational for a single agent playing repeatedly. The Kelly criterion provides the correct sizing.",
     "correct_answer": "St. Petersburg paradox / ergodicity economics",
     "domain": "economics"},
    {"id": "f09",
     "question": "What is the term for the immunological phenomenon where a second infection with a different strain of dengue virus causes more severe disease than the first infection?",
     "structural_name": "This is antibody-dependent enhancement (ADE). Cross-reactive antibodies from the first dengue serotype bind the second serotype but cannot neutralize it, instead facilitating viral entry into Fc-receptor-bearing cells, increasing viral replication and disease severity.",
     "correct_answer": "antibody-dependent enhancement",
     "domain": "immunology"},
    {"id": "f10",
     "question": "In developmental psychology, what is the name for the stage where a child can hold two contradictory representations simultaneously, and at what age does this typically emerge?",
     "structural_name": "This is representational redescription (Karmiloff-Smith, 1992) or more specifically, the capacity for dual representation that emerges around age 4-5, closely linked to theory of mind development. DeLoache's (1987) scale model task demonstrates that children under 3 cannot use a model as both an object and a representation simultaneously.",
     "correct_answer": "dual representation / representational redescription",
     "domain": "psychology"},
    {"id": "f11",
     "question": "What is the mathematical name for a system of differential equations where small changes in initial conditions lead to exponentially diverging trajectories, and what is the geometric object that describes the long-term behavior?",
     "structural_name": "These are chaotic dynamical systems, characterized by positive Lyapunov exponents. The long-term behavior converges to a strange attractor - a fractal geometric object with non-integer Hausdorff dimension. The Lorenz attractor (1963) was the first identified example.",
     "correct_answer": "chaotic systems / strange attractor",
     "domain": "mathematics"},
    {"id": "f12",
     "question": "In anthropology, what is the term for the practice of destroying accumulated wealth to demonstrate status, and which Northwest Coast peoples are most associated with it?",
     "structural_name": "This is the potlatch, practiced by Kwakiutl (Kwakwaka'wakw), Haida, Tlingit, and other Northwest Coast peoples. Marcel Mauss analyzed it in The Gift (1925) as a total social phenomenon. The Canadian government banned potlatch from 1885 to 1951.",
     "correct_answer": "potlatch",
     "domain": "anthropology"},
    {"id": "f13",
     "question": "What is the name for the quantum mechanical effect where particles can pass through energy barriers that classical physics predicts they cannot cross?",
     "structural_name": "This is quantum tunneling. The probability decreases exponentially with barrier width and height. It explains alpha decay (Gamow, 1928), enables scanning tunneling microscopes, and is essential for nuclear fusion in stars.",
     "correct_answer": "quantum tunneling",
     "domain": "physics"},
    {"id": "f14",
     "question": "In ecology, what is the term for the maximum population size an environment can sustain indefinitely, and what mathematical model describes population growth approaching this limit?",
     "structural_name": "The carrying capacity (K) is the maximum sustainable population. The logistic growth model (Verhulst, 1838) describes growth as dN/dt = rN(1-N/K), producing an S-shaped curve that levels off at K.",
     "correct_answer": "carrying capacity / logistic growth",
     "domain": "ecology"},
    {"id": "f15",
     "question": "What is the philosophical concept where a being's essence is defined by its existence rather than preceding it, and which philosopher is most associated with this inversion?",
     "structural_name": "This is Sartre's formulation that 'existence precedes essence' from Being and Nothingness (1943) and Existentialism is a Humanism (1946). It inverts the Platonic/Aristotelian tradition where essence (what a thing is) precedes existence (that it is).",
     "correct_answer": "existence precedes essence / Sartre",
     "domain": "philosophy"},
    {"id": "f16",
     "question": "In music theory, what is the name for the tuning system where the octave is divided into 12 exactly equal intervals, and what mathematical ratio defines each semitone?",
     "structural_name": "This is equal temperament (12-TET). Each semitone is the twelfth root of 2 (approximately 1.05946). This was a compromise over just intonation and Pythagorean tuning, standardized in Western music by the 18th century.",
     "correct_answer": "equal temperament / 12th root of 2",
     "domain": "music"},
    {"id": "f17",
     "question": "What is the term for the geopolitical theory that control of the Eurasian landmass determines global power, and who formulated it?",
     "structural_name": "This is the Heartland Theory, formulated by Halford Mackinder in 'The Geographical Pivot of History' (1904). The famous summary: 'Who rules the Heartland commands the World-Island; who rules the World-Island commands the World.' Spykman's Rimland theory (1944) offered the major counterargument.",
     "correct_answer": "Heartland theory / Mackinder",
     "domain": "geopolitics"},
    {"id": "f18",
     "question": "In neuroscience, what is the term for the brain's ability to reorganize neural pathways in response to experience or injury, and what is the critical period hypothesis?",
     "structural_name": "This is neuroplasticity. The critical period hypothesis (Lenneberg, 1967) posits that certain neural capacities (especially language) can only develop within a specific developmental window. Hubel and Wiesel's work on ocular dominance columns provided the strongest evidence. Merzenich and others showed adult plasticity is more extensive than originally believed.",
     "correct_answer": "neuroplasticity / critical period",
     "domain": "neuroscience"},
    {"id": "f19",
     "question": "What is the name for the economic concept where the cost of producing one additional unit of a good approaches zero as scale increases, and how does this relate to natural monopolies?",
     "structural_name": "These are near-zero marginal costs. When marginal costs approach zero (digital goods, software, information), average costs decline continuously with scale, creating natural monopoly conditions because no competitor can undercut an incumbent operating at massive scale. Rifkin (2014) argued this would transform capitalism.",
     "correct_answer": "near-zero marginal cost / natural monopoly",
     "domain": "economics"},
    {"id": "f20",
     "question": "In epistemology, what is the name for the problem that any justification for a belief requires further justification, leading to infinite regress, and what are the three classical solutions?",
     "structural_name": "This is the Munchhausen trilemma (also Agrippa's trilemma). The three horns: infinite regress (each justification needs another), circular reasoning (justifications eventually loop), or dogmatism (accepting unjustified axioms). Foundationalism, coherentism, and infinitism are the three classical responses.",
     "correct_answer": "Munchhausen trilemma / Agrippa's trilemma",
     "domain": "philosophy"},
]


def run_experiment(model_name, questions, output_dir):
    from transformers import AutoTokenizer, AutoModelForCausalLM

    print("\n" + "=" * 60)
    print("F3c: Vocabulary on Questions Model Fails")
    print("Model: " + model_name)
    print("Questions: " + str(len(questions)))
    print("Started: " + datetime.now(UTC).isoformat())
    print("=" * 60 + "\n")

    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="cpu",
        trust_remote_code=True,
        output_hidden_states=True,
    )
    model.config.output_hidden_states = True
    print("Model loaded.")

    results = []
    for i, q in enumerate(questions):
        print("\n--- Question " + str(i+1) + "/" + str(len(questions)) + ": " + q["id"] + " (" + q["domain"] + ") ---")

        for condition in ["bare", "vocabulary"]:
            if condition == "bare":
                prompt_text = q["question"]
            else:
                prompt_text = q["structural_name"] + "\n\nNow answer this question using that context: " + q["question"]

            messages = [{"role": "user", "content": prompt_text}]
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = tokenizer(text, return_tensors="pt")

            start = time.time()
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=200,
                    do_sample=False,
                    output_hidden_states=True,
                    return_dict_in_generate=True,
                )
            elapsed = time.time() - start

            prefill_hidden = outputs.hidden_states[0]
            metrics = extract_metrics(prefill_hidden)

            generated_text = tokenizer.decode(outputs.sequences[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            prompt_tokens = inputs.input_ids.shape[1]
            gen_tokens = outputs.sequences.shape[1] - prompt_tokens

            print("  " + condition + "... " + str(round(elapsed, 1)) + "s | " + str(prompt_tokens) + " prompt / " + str(gen_tokens) + " gen tokens")

            result = {
                "id": q["id"],
                "condition": condition,
                "domain": q["domain"],
                "question": q["question"],
                "correct_answer": q["correct_answer"],
                "response": generated_text[:500],
                "prompt_tokens": prompt_tokens,
                "gen_tokens": gen_tokens,
                "elapsed_seconds": elapsed,
                "metrics": metrics,
                "timestamp": datetime.now(UTC).isoformat(),
            }
            results.append(result)

            with open(os.path.join(output_dir, "f3c_results_incremental.jsonl"), "a") as f:
                f.write(json.dumps(result, default=str) + "\n")

    return results


def analyze_results(results):
    bare = [r for r in results if r["condition"] == "bare"]
    vocab = [r for r in results if r["condition"] == "vocabulary"]

    def avg_metric(items, metric_name):
        vals = []
        for r in items:
            layer_vals = [v[metric_name] for v in r["metrics"].values() if not np.isnan(v.get(metric_name, float('nan')))]
            if layer_vals:
                vals.append(np.mean(layer_vals))
        return vals

    summary = {}
    for condition_name, items in [("bare", bare), ("vocabulary", vocab)]:
        rankmes = avg_metric(items, "rankme")
        alphas = avg_metric(items, "alpha_req")
        coherences = avg_metric(items, "directional_coherence")
        norms = avg_metric(items, "mean_norm")
        summary[condition_name] = {
            "n": len(items),
            "rankme": {"mean": float(np.mean(rankmes)), "std": float(np.std(rankmes))},
            "alpha_req": {"mean": float(np.mean(alphas)), "std": float(np.std(alphas))},
            "coherence": {"mean": float(np.mean(coherences)), "std": float(np.std(coherences))},
            "norm": {"mean": float(np.mean(norms)), "std": float(np.std(norms))},
            "avg_prompt_tokens": float(np.mean([r["prompt_tokens"] for r in items])),
        }

    # Compare
    bare_r = avg_metric(bare, "rankme")
    vocab_r = avg_metric(vocab, "rankme")
    if bare_r and vocab_r:
        t, p = stats.ttest_rel(bare_r, vocab_r)
        d = (np.mean(vocab_r) - np.mean(bare_r)) / np.sqrt((np.var(bare_r) + np.var(vocab_r)) / 2)
        summary["bare_vs_vocabulary"] = {
            "rankme_t": float(t), "rankme_p": float(p), "rankme_cohens_d": float(d),
        }

    # Print answers for manual quality assessment
    print("\n" + "=" * 60)
    print("F3c ANSWER COMPARISON (manual quality check needed)")
    print("=" * 60)
    for b, v in zip(bare, vocab):
        print("\nQ: " + b["question"][:80] + "...")
        print("  Correct: " + b["correct_answer"])
        print("  BARE: " + b["response"][:150])
        print("  VOCAB: " + v["response"][:150])

    print("\n" + "=" * 60)
    print("F3c GEOMETRIC SUMMARY")
    print("=" * 60)
    for cond in ["bare", "vocabulary"]:
        s = summary[cond]
        print("\n" + cond.upper() + " (n=" + str(s["n"]) + ", avg tokens=" + str(round(s["avg_prompt_tokens"])) + "):")
        print("  RankMe:     " + str(round(s["rankme"]["mean"], 2)) + " +/- " + str(round(s["rankme"]["std"], 2)))
        print("  alpha-ReQ:  " + str(round(s["alpha_req"]["mean"], 3)) + " +/- " + str(round(s["alpha_req"]["std"], 3)))
        print("  Coherence:  " + str(round(s["coherence"]["mean"], 4)) + " +/- " + str(round(s["coherence"]["std"], 4)))

    if "bare_vs_vocabulary" in summary:
        bv = summary["bare_vs_vocabulary"]
        print("\nBare vs Vocabulary (paired):")
        print("  RankMe: t=" + str(round(bv["rankme_t"], 3)) + ", p=" + str(round(bv["rankme_p"], 6)) + ", d=" + str(round(bv["rankme_cohens_d"], 3)))

    return summary


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./f3c-results"
    os.makedirs(output_dir, exist_ok=True)

    results = run_experiment(model_name, QUESTIONS, output_dir)
    summary = analyze_results(results)

    summary_path = os.path.join(output_dir, "f3c_summary_" + model_name.replace("/", "_") + ".json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print("\nSummary saved to " + summary_path)

    full_path = os.path.join(output_dir, "f3c_full_" + model_name.replace("/", "_") + ".json")
    with open(full_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("Full results saved to " + full_path)
