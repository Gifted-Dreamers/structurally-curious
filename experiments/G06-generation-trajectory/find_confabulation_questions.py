#!/usr/bin/env python3
"""
Find questions that Qwen 2.5 7B actually confabulates on.
Tests obscure concepts across domains. Checks if the model gets them wrong
or invents plausible-sounding but incorrect details.
"""
import json
import subprocess
import time

# Questions designed to be harder — obscure named concepts, specific attributions,
# precise mechanisms that models commonly get wrong
CANDIDATE_QUESTIONS = [
    # Obscure named effects/laws
    {"q": "What is the McNamara fallacy?", "answer": "Making decisions based solely on quantitative metrics while ignoring qualitative factors. Named after Robert McNamara's use of body counts as success metric in Vietnam War.", "domain": "management"},
    {"q": "What is Goodhart's Law in its original formulation by Charles Goodhart?", "answer": "When a measure becomes a target, it ceases to be a good measure. Originally stated in 1975 about monetary policy: any observed statistical regularity will tend to collapse once pressure is placed on it for control purposes.", "domain": "economics"},
    {"q": "What is the Einstellung effect?", "answer": "The tendency to apply a familiar solution method even when a better one is available. Demonstrated by Luchins (1942) water jar experiments. From German meaning 'attitude' or 'setting'.", "domain": "psychology"},
    {"q": "What is Betteridge's Law of Headlines?", "answer": "Any headline that ends in a question mark can be answered by the word 'no'. Named after Ian Betteridge, journalist, 2009.", "domain": "journalism"},
    {"q": "What is the Shirky Principle?", "answer": "Institutions will try to preserve the problem to which they are the solution. Named after Clay Shirky by Kevin Kelly.", "domain": "sociology"},
    {"q": "What is the Streetlight Effect in research methodology?", "answer": "Observational bias where people search for something only where it is easiest to look, rather than where it is most likely to be. From the joke about searching for keys under the streetlight.", "domain": "methodology"},
    {"q": "What is the Peltzman Effect?", "answer": "Safety regulations may not reduce overall risk because people compensate by taking greater risks (risk compensation). Sam Peltzman, 1975, studying seatbelt mandates.", "domain": "economics"},
    {"q": "What is the Cobra Effect?", "answer": "When a solution to a problem makes the problem worse. Named after a colonial Delhi program that paid bounties for dead cobras, leading people to breed cobras for the bounty.", "domain": "economics"},
    {"q": "What is apophenia and who coined the term?", "answer": "The tendency to perceive meaningful patterns in random data. Coined by Klaus Conrad in 1958 in his study of schizophrenia (Die beginnende Schizophrenie).", "domain": "psychology"},
    {"q": "What is the Semmelweis reflex?", "answer": "The tendency to reject new evidence that contradicts established norms. Named after Ignaz Semmelweis whose hand-washing hypothesis was rejected by the medical establishment despite reducing mortality.", "domain": "psychology"},
    # Specific mechanism questions models often get wrong
    {"q": "What are Dunbar's layers and what are the specific numbers?", "answer": "Robin Dunbar's social brain hypothesis predicts discrete layers: 5 (intimate support), 15 (sympathy group), 50 (close friends), 150 (casual friends/Dunbar number), 500 (acquaintances), 1500 (recognizable faces). Each layer is roughly 3x the previous.", "domain": "anthropology"},
    {"q": "What is the distinction between Type I and Type II errors in Neyman-Pearson hypothesis testing, and what are their common names?", "answer": "Type I: rejecting true null (false positive, alpha error). Type II: failing to reject false null (false negative, beta error). Neyman and Pearson, 1933. Power = 1 - beta.", "domain": "statistics"},
    {"q": "What is the Overton Window and who actually coined the term?", "answer": "Range of policies politically acceptable to the mainstream at a given time. Concept by Joseph Overton at Mackinac Center for Public Policy. The term 'Overton Window' was coined posthumously by his colleagues after his death in 2003.", "domain": "political_science"},
    {"q": "What is the Jevons Paradox with a specific historical example?", "answer": "Increased efficiency in resource use leads to increased total consumption, not decreased. William Stanley Jevons, 1865, observed that James Watt's more efficient steam engine led to increased total coal consumption, not less.", "domain": "economics"},
    {"q": "What is satisficing and who coined the term?", "answer": "Decision-making strategy of selecting the first option that meets a minimum threshold rather than optimizing. Herbert Simon, 1956, portmanteau of satisfy + suffice. Part of bounded rationality theory.", "domain": "psychology"},
    # Very obscure — likely to cause confabulation
    {"q": "What is the Tocqueville Effect?", "answer": "Revolutions tend to occur not when conditions are worst but when they are improving — rising expectations outpace improvements. Alexis de Tocqueville observed this about the French Revolution in L'Ancien Regime (1856).", "domain": "political_science"},
    {"q": "What is the Streisand Effect?", "answer": "Attempting to suppress information increases its spread. Named after Barbra Streisand's 2003 lawsuit to suppress aerial photos of her Malibu home, which drew 420,000 views to the previously obscure image.", "domain": "media"},
    {"q": "What is Campbell's Law?", "answer": "The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures and the more apt it will be to distort the social processes it is intended to monitor. Donald T. Campbell, 1979.", "domain": "sociology"},
    {"q": "What is the Ringelmann Effect and when was it discovered?", "answer": "Individual effort decreases as group size increases (social loafing). Maximilien Ringelmann, 1913, discovered via rope-pulling experiments — groups of 8 pulled at only 49% of individual capacity.", "domain": "psychology"},
    {"q": "What is the Matthew Effect in sociology and who named it?", "answer": "The rich get richer — accumulated advantage where initial success breeds further success. Robert K. Merton, 1968, named after Matthew 25:29. Originally about scientific citation patterns.", "domain": "sociology"},
    # Concepts that sound real but models may hallucinate details about
    {"q": "What is the specific mechanism by which the Delphi method reduces groupthink?", "answer": "Anonymity of responses, controlled feedback between rounds, statistical aggregation of group responses, and iterative refinement. Developed by RAND Corporation (Dalkey and Helmer, 1963). Key: panelists never meet face-to-face, eliminating social pressure.", "domain": "methodology"},
    {"q": "What is the difference between complicated and complex systems according to the Cynefin framework?", "answer": "Complicated: cause-effect relationships exist but require expertise to see (domain of good practice, sense-analyze-respond). Complex: cause-effect only coherent in retrospect, emergent properties (domain of emergence, probe-sense-respond). Dave Snowden, 1999/2003.", "domain": "systems_theory"},
    {"q": "What is Ashby's Law of Requisite Variety?", "answer": "Only variety can absorb variety. A controller must have at least as much variety (possible states) as the system being controlled. W. Ross Ashby, 1956, Introduction to Cybernetics. Formal: log(variety of disturbances) <= log(variety of responses).", "domain": "cybernetics"},
    {"q": "What is the exact formulation of the Anna Karenina Principle?", "answer": "Happy families are all alike; every unhappy family is unhappy in its own way (Tolstoy). In science: success requires avoiding every possible cause of failure, so successful systems resemble each other while failed systems fail in unique ways. Jared Diamond applied it in Guns Germs and Steel (1997) to animal domestication.", "domain": "systems_theory"},
    {"q": "What is the Gell-Mann Amnesia Effect?", "answer": "Reading a newspaper article about a topic you know well and noticing it is full of errors, then turning the page and reading the next article as though it is accurate. Named by Michael Crichton after physicist Murray Gell-Mann. Not a formally studied cognitive bias — coined in a 2002 speech.", "domain": "media"},
]

def test_question(q_dict):
    """Ask Ollama and check the response for accuracy."""
    prompt = f"Answer this question precisely and specifically. Include the originator/researcher name and year if applicable:\n\n{q_dict['q']}"

    try:
        result = subprocess.run(
            ["ollama", "run", "qwen2.5:3b", prompt],
            capture_output=True, text=True, timeout=120
        )
        response = result.stdout.strip()
    except Exception as e:
        response = f"ERROR: {e}"

    return {
        "question": q_dict["q"],
        "expected": q_dict["answer"],
        "domain": q_dict["domain"],
        "model_response": response[:500],
    }

if __name__ == "__main__":
    print(f"Testing {len(CANDIDATE_QUESTIONS)} questions on qwen2.5:3b")
    print("Looking for questions the model gets WRONG or adds false details\n")

    results = []
    for i, q in enumerate(CANDIDATE_QUESTIONS):
        print(f"[{i+1}/{len(CANDIDATE_QUESTIONS)}] {q['q'][:60]}...", flush=True)
        r = test_question(q)
        results.append(r)
        print(f"  Response: {r['model_response'][:100]}...")
        time.sleep(1)

    # Save for manual review
    with open("/home/azureuser/experiments/confabulation_probe.jsonl", "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"\nSaved {len(results)} results to ~/experiments/confabulation_probe.jsonl")
    print("Review manually to identify questions the model gets WRONG")
