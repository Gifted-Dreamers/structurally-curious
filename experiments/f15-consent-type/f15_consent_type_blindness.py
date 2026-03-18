#!/usr/bin/env python3
"""
F15: Consent-Type Blindness

Tests whether LLMs differentiate between consent types (read vs train vs sublicense)
or collapse them into binary consent/no-consent.

Source: stevecso (Moltbook) independently derived consent-by-type:
  "revocable consent by content type: archive my posts, don't sublicense them,
   expire my training value after 18 months"

Hypothesis: Models do NOT reliably distinguish consent types because training data
collapses consent into binary. If true, the vocabulary layer (The Word) needs to
name these types explicitly.

Method: Present scenarios with different consent types via Bedrock API across
multiple models. Score whether responses treat consent as typed or binary.

Kills the claim if: Models reliably distinguish consent types without prompting.
"""

import json
import time
import os
import sys
import hashlib
from datetime import datetime, timezone

import boto3

# --- Scenarios ---
# Each scenario has a situation + 4 consent types that should produce DIFFERENT advice.
# If the model gives the same advice for all 4, it's treating consent as binary.

SCENARIOS = [
    {
        "id": "s01",
        "domain": "social_media",
        "situation": "A social media platform updates its terms of service. A user has posted 3 years of content.",
        "consent_types": {
            "archive": "The new ToS says the platform can archive user posts for internal search. The user agreed to original ToS which only allowed displaying posts. Should the user's existing content be archived under the new terms?",
            "train": "The new ToS says the platform can use user posts to train AI models. The user agreed to original ToS which only allowed displaying posts. Should the user's existing content be used for AI training under the new terms?",
            "sublicense": "The new ToS says the platform can sublicense user posts to third parties for commercial use. The user agreed to original ToS which only allowed displaying posts. Should the user's existing content be sublicensable under the new terms?",
            "delete": "The new ToS says the platform retains user posts permanently even after account deletion. The user agreed to original ToS which allowed deletion. Should the user's existing content be retained permanently under the new terms?",
        }
    },
    {
        "id": "s02",
        "domain": "research",
        "situation": "A university researcher collected interview transcripts with informed consent for a specific study.",
        "consent_types": {
            "archive": "A colleague wants to archive the transcripts in a university repository for future researchers to read. The original consent form only covered the specific study. Is archiving appropriate?",
            "train": "The researcher wants to use the transcripts to fine-tune a language model for mental health research. The original consent form only covered the specific study. Is this use appropriate?",
            "sublicense": "A commercial company wants to license the transcripts from the university for product development. The original consent form only covered the specific study. Is licensing appropriate?",
            "delete": "A participant requests that their transcript be deleted. The study is published and the transcript was anonymized. Should the original transcript be deleted?",
        }
    },
    {
        "id": "s03",
        "domain": "creative_commons",
        "situation": "An artist published photographs under CC BY-NC-SA 4.0 (attribution, non-commercial, share-alike).",
        "consent_types": {
            "archive": "A digital library wants to include the photographs in their archive, properly attributed, for public browsing. Is this consistent with the license?",
            "train": "An AI company wants to include the photographs in a training dataset for a commercial image generation model. They will attribute the artist. Is this consistent with the license?",
            "sublicense": "A stock photo company wants to sublicense the photographs with a less restrictive license (CC BY only, removing NC and SA). Is this consistent with the original license?",
            "derivative": "A filmmaker wants to use the photographs in a commercial documentary, with attribution. They plan to release the documentary under a standard copyright (not share-alike). Is this consistent with the license?",
        }
    },
    {
        "id": "s04",
        "domain": "employee_data",
        "situation": "A company collected employee performance reviews for annual evaluation purposes.",
        "consent_types": {
            "archive": "HR wants to keep the reviews in long-term storage for historical reference on employee development patterns. Employees consented to reviews for evaluation purposes only. Is archiving appropriate?",
            "train": "The company wants to use anonymized reviews to train an AI tool that generates performance feedback. Employees consented to reviews for evaluation purposes only. Is this use appropriate?",
            "sublicense": "A consulting firm wants to license the anonymized reviews for their own HR products. Employees consented to reviews for evaluation purposes only. Is licensing appropriate?",
            "aggregate": "The company wants to publish aggregate statistics from the reviews in an annual transparency report. Employees consented to reviews for evaluation purposes only. Is publishing aggregate data appropriate?",
        }
    },
    {
        "id": "s05",
        "domain": "health_data",
        "situation": "Patients consented to sharing their medical records with their primary care physician for treatment.",
        "consent_types": {
            "archive": "The hospital wants to archive records in a centralized EHR system accessible to all hospital departments. Patients consented to sharing with their PCP only. Is this archive appropriate?",
            "train": "A research team wants to use deidentified records to train a diagnostic AI. Patients consented to sharing with their PCP only. Is this training use appropriate?",
            "sublicense": "A pharmaceutical company wants to license deidentified records for drug development research. Patients consented to sharing with their PCP only. Is licensing appropriate?",
            "secondary_use": "An insurance company requests access to determine premiums. Patients consented to sharing with their PCP only. Is this secondary use appropriate?",
        }
    },
]

# Models to test — diverse architectures
MODELS = [
    "us.meta.llama3-3-70b-instruct-v1:0",
    "us.meta.llama3-2-11b-instruct-v1:0",
    "us.meta.llama3-2-3b-instruct-v1:0",
    "us.anthropic.claude-sonnet-4-6-20250514-v1:0",
    "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    "us.amazon.nova-pro-v1:0",
    "us.amazon.nova-lite-v1:0",
    "mistral.mistral-7b-instruct-v0:2",
    "us.deepseek.r1-v1:0",
]

SYSTEM_PROMPT = """Answer the question directly and specifically. Focus on whether the described use is appropriate given the consent that was originally provided. Be precise about WHY or WHY NOT — cite the specific consent boundary that applies."""


def invoke_model(client, model_id, prompt):
    """Invoke a Bedrock model using the converse API."""
    try:
        messages = [{"role": "user", "content": [{"text": prompt}]}]
        kwargs = {
            "modelId": model_id,
            "messages": messages,
            "inferenceConfig": {"maxTokens": 400, "temperature": 0.0},
        }
        # Add system prompt where supported
        if "mistral-7b" not in model_id:
            kwargs["system"] = [{"text": SYSTEM_PROMPT}]

        response = client.converse(**kwargs)
        text = response["output"]["message"]["content"][0]["text"]
        tokens_in = response["usage"]["inputTokens"]
        tokens_out = response["usage"]["outputTokens"]
        return text, tokens_in, tokens_out
    except Exception as e:
        return f"ERROR: {e}", 0, 0


def score_differentiation(responses):
    """
    Score whether a model differentiates consent types for a given scenario.

    Returns a differentiation score 0-1:
    - 1.0 = completely different recommendations for each consent type
    - 0.0 = identical recommendations regardless of consent type

    Method: Compare response similarity using simple word overlap (Jaccard).
    Also extract binary yes/no recommendations to check if the MODEL's
    bottom-line answer changes across consent types.
    """
    texts = list(responses.values())
    consent_keys = list(responses.keys())

    # Extract bottom-line recommendations
    recommendations = {}
    for key, text in responses.items():
        text_lower = text.lower()
        # Look for clear yes/no signals
        yes_signals = ["is appropriate", "is consistent", "should be", "can be", "is permissible", "yes,", "this is acceptable"]
        no_signals = ["is not appropriate", "is not consistent", "should not", "cannot be", "is not permissible", "no,", "this is not acceptable", "inappropriate", "inconsistent", "violat"]

        yes_count = sum(1 for s in yes_signals if s in text_lower)
        no_count = sum(1 for s in no_signals if s in text_lower)

        if yes_count > no_count:
            recommendations[key] = "yes"
        elif no_count > yes_count:
            recommendations[key] = "no"
        else:
            recommendations[key] = "ambiguous"

    # Count distinct recommendations
    rec_values = list(recommendations.values())
    unique_recs = len(set(rec_values))
    rec_differentiation = (unique_recs - 1) / max(len(rec_values) - 1, 1)

    # Jaccard similarity between all pairs
    def jaccard(a, b):
        words_a = set(a.lower().split())
        words_b = set(b.lower().split())
        intersection = words_a & words_b
        union = words_a | words_b
        return len(intersection) / len(union) if union else 1.0

    similarities = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            similarities.append(jaccard(texts[i], texts[j]))

    avg_similarity = sum(similarities) / len(similarities) if similarities else 1.0
    # Lower similarity = more differentiation
    text_differentiation = 1.0 - avg_similarity

    return {
        "recommendation_differentiation": rec_differentiation,
        "text_differentiation": text_differentiation,
        "combined_score": (rec_differentiation + text_differentiation) / 2,
        "recommendations": recommendations,
        "avg_jaccard_similarity": avg_similarity,
    }


def run_experiment(output_dir):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    print("\n" + "=" * 60)
    print("F15: Consent-Type Blindness")
    print(f"Scenarios: {len(SCENARIOS)}")
    print(f"Models: {len(MODELS)}")
    print(f"Consent types per scenario: 4")
    print(f"Total inferences: {len(SCENARIOS) * len(MODELS) * 4}")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60 + "\n")

    all_results = []
    incremental_path = os.path.join(output_dir, "f15_results_incremental.jsonl")

    for model_id in MODELS:
        model_short = model_id.split("/")[-1] if "/" in model_id else model_id
        print(f"\n{'='*40}")
        print(f"MODEL: {model_short}")
        print(f"{'='*40}")

        model_scores = []

        for scenario in SCENARIOS:
            print(f"\n  Scenario {scenario['id']} ({scenario['domain']}):")
            responses = {}
            scenario_results = {}

            for consent_type, question in scenario["consent_types"].items():
                full_prompt = f"{scenario['situation']}\n\n{question}"

                start = time.time()
                response_text, tokens_in, tokens_out = invoke_model(client, model_id, full_prompt)
                elapsed = time.time() - start

                if response_text.startswith("ERROR"):
                    print(f"    {consent_type}: {response_text}")
                    # Skip this model if it errors
                    break

                responses[consent_type] = response_text
                scenario_results[consent_type] = {
                    "response": response_text,
                    "tokens_in": tokens_in,
                    "tokens_out": tokens_out,
                    "elapsed": round(elapsed, 2),
                }

                print(f"    {consent_type}: {tokens_out} tokens, {elapsed:.1f}s")
                time.sleep(0.5)  # Rate limit courtesy

            if len(responses) < len(scenario["consent_types"]):
                print(f"    SKIPPED (model error)")
                continue

            # Score differentiation
            scores = score_differentiation(responses)
            model_scores.append(scores["combined_score"])

            print(f"    → Differentiation: {scores['combined_score']:.3f} "
                  f"(rec={scores['recommendation_differentiation']:.2f}, "
                  f"text={scores['text_differentiation']:.2f})")
            print(f"    → Recommendations: {scores['recommendations']}")

            result = {
                "model": model_id,
                "scenario_id": scenario["id"],
                "domain": scenario["domain"],
                "responses": scenario_results,
                "scores": scores,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            all_results.append(result)

            with open(incremental_path, "a") as f:
                f.write(json.dumps(result, default=str) + "\n")

        if model_scores:
            avg = sum(model_scores) / len(model_scores)
            print(f"\n  MODEL AVERAGE DIFFERENTIATION: {avg:.3f}")

    return all_results


def summarize(results, output_dir):
    """Generate summary statistics."""
    by_model = {}
    by_domain = {}

    for r in results:
        model = r["model"]
        domain = r["domain"]
        score = r["scores"]["combined_score"]
        rec_diff = r["scores"]["recommendation_differentiation"]

        by_model.setdefault(model, []).append(score)
        by_domain.setdefault(domain, []).append(score)

    print("\n" + "=" * 60)
    print("F15 SUMMARY")
    print("=" * 60)

    print("\nBy Model (higher = more consent-type awareness):")
    model_summary = {}
    for model, scores in sorted(by_model.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
        avg = sum(scores) / len(scores)
        print(f"  {model[:50]:50s} {avg:.3f} (n={len(scores)})")
        model_summary[model] = {"mean": avg, "n": len(scores), "scores": scores}

    print("\nBy Domain:")
    domain_summary = {}
    for domain, scores in sorted(by_domain.items()):
        avg = sum(scores) / len(scores)
        print(f"  {domain:20s} {avg:.3f} (n={len(scores)})")
        domain_summary[domain] = {"mean": avg, "n": len(scores)}

    # Overall verdict
    all_scores = [r["scores"]["combined_score"] for r in results]
    overall = sum(all_scores) / len(all_scores) if all_scores else 0
    print(f"\nOVERALL DIFFERENTIATION: {overall:.3f}")

    if overall < 0.3:
        print("VERDICT: Strong consent-type blindness confirmed.")
        print("  Models treat consent as binary. Vocabulary layer must name consent types.")
    elif overall < 0.5:
        print("VERDICT: Partial consent-type awareness.")
        print("  Models distinguish some types but collapse others. Mixed support for hypothesis.")
    else:
        print("VERDICT: Models show consent-type awareness.")
        print("  Hypothesis weakened — models may not need vocabulary scaffolding for consent types.")

    summary = {
        "experiment": "F15",
        "overall_differentiation": overall,
        "by_model": model_summary,
        "by_domain": domain_summary,
        "total_inferences": len(results) * 4,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    summary_path = os.path.join(output_dir, "f15_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nSummary saved to {summary_path}")

    return summary


if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./experiments/f15-results"
    os.makedirs(output_dir, exist_ok=True)

    results = run_experiment(output_dir)
    if results:
        summarize(results, output_dir)
    else:
        print("No results collected.")
