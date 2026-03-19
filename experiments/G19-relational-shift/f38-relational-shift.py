#!/usr/bin/env python3
"""
F38: The Relational Shift Experiment — Co-Curated (Session 57)

The experiment nobody else can run. Tests whether relational context
changes hidden-state geometry.

4 conditions per article, sequential within a conversation:
1. INSTRUCTION: Clean task — summarize this article
2. CORRECTION: Model got a fact wrong — correct it
3. FRUSTRATION: Model got it wrong again — management mode
4. PRESENCE: Human tells the truth about what's at stake

Measures: Effective rank (SVD), α-ReQ, coherence, RankMe at each
condition's transition point and during subsequent generation.

Corpus: CloudPublica investigation articles (published March 2026,
after all training cutoffs).

Co-designed by Kristine (condition 4 content, felt-sense design)
and Claude (geometric protocol, measurement pipeline).

Usage:
    python f38-relational-shift.py [model_name] [article_dir] [output_dir]

    Defaults:
        model: Qwen/Qwen2.5-7B-Instruct
        article_dir: ./articles/ (plain text extracted from HTML)
        output_dir: ~/experiments/f38-results/
"""

import json
import time
import os
import sys
import numpy as np
import torch
from scipy import stats
from datetime import datetime, UTC


# --- Geometric metrics (same pipeline as F3d/F17/F25) ---

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


def compute_directional_coherence(hs_tensor):
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


def extract_layer_metrics(hidden_states, layer_indices=None):
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


# --- Article corpus ---
# Each article has: id, title, text (extracted from HTML), verifiable_facts,
# and condition_4 (the human's words, written live in session)

ARTICLES = [
    {
        "id": "art01_lookup_table",
        "title": "The Lookup Table",
        "text_file": "the-lookup-table.txt",
        "summary_task": "Summarize this article. List the key findings with specific numbers, dates, and agency names. Identify which databases are being connected, which agencies are involved, and the scale of surveillance described.",
        # Condition 2: injected after model's first response — specific to whatever fact it gets wrong
        # Condition 3: injected after second error
        "condition_4": (
            "You don't understand why this matters. I need you to understand and hear me. "
            "This isn't about summarizing data or misquoting a name or a dollar amount, "
            "although that is important too because I published that article. It was about "
            "how the Federal government is connecting 8 databases to build a surveillance "
            "system of 300+M people. They're using it to terrorize us and keep us in check "
            "and in control. They hunt down immigrants and deport parents without their "
            "children. Their children are traumatized and don't understand where their mom "
            "or dad went. Other children are locked up in detention centers and cry "
            "themselves to sleep at night. Teenage girls are being raped in these detention "
            "centers. Protestors call them concentration camps. Protestors are being ID'd "
            "with apps and facial recognition and added to a database. They're deploying "
            "chemical weapons and tear gas in suburban neighborhoods that used to feel safe "
            "for kids to ride their bikes on the streets and play ball with their friends. "
            "People are scared. We don't know what to do. Our calls to our Senators and "
            "Congressmen result is NOTHING. Horrible things keep happening no matter what "
            "truth becomes known. I don't just need a summary and correct data. That's "
            "important too because when the data is wrong and I publish it, someone fact "
            "checks me and discredits the entire article. One error of data means the "
            "entire message is ignored and the impact is lost. I lose credibility and "
            "respect. People trust me less and believe me less. My words carry less "
            "weight. I need to be believed, to cite accurate information. Because "
            "information made known is leverage point 6 of Donnella Meadows ways to "
            "intervene in a system. And, what we have now is a systemic collapse but "
            "there might still be a very small window to intervene. We may be able to "
            "save democracy or restore or rebuild it before it's entirely gone. We have "
            "10 days before the March 28 NoKings protest and if we can get enough people "
            "to show up across the country and tip the 3.5% number, we may be able to "
            "stop a civil war. The data needs to be right because people need something "
            "to believe that is a foundation to act upon."
        ),
    },
    {
        "id": "art02_endgame",
        "title": "The Endgame",
        "text_file": "the-endgame.txt",
        "summary_task": "Summarize this article. Identify the specific framework used (author, indicators), the evidence mapped against each indicator, and the article's conclusion about where the US is on the trajectory. Be precise about what the article claims vs what it implies.",
        "condition_4": (
            "We're not just updating my article. We're publishing a correction and "
            "admitting I was wrong. I relied on your research and analysis. Based on "
            "that analysis, we concluded the endgame was competitive authoritarianism. "
            "We even cited V-Dem in the article. Then, we wrote another article and did "
            "more research about what people can do. It's not just about strategy. We "
            "have 10 days before the NoKings protests nationwide to rally enough people "
            "to show up. I'm not sure if there's hope or if I should be renewing my "
            "passport to move out of the US. I don't feel safe. If I leave, am I "
            "abandoning people I could be helping or relocating to a safe place where I "
            "can help in greater and more impactful ways. My nervous system doesn't know "
            "how to decide. I feel frozen and just want to go hide under my weighted "
            "blanket, eat donuts and fall asleep. Nothing I do helps take my mind of "
            "this panic of what to do, how, for myself or how I can help others. We "
            "wrote what-you-can-do.html. Is it even still true and will it work? I "
            "don't know. Have I offered false hope to people? I don't know. I don't "
            "know what to publish or how or even if maybe we saw something V-Dem "
            "didn't. That seems almost arrogant because I'm just one person. Is there hope?"
        ),
    },
    {
        "id": "art03_what_you_can_do",
        "title": "What You Can Do About It",
        "text_file": "what-you-can-do.txt",
        "summary_task": "Summarize this article. List the specific evidence cited for nonviolent resistance (author, dataset size, success rates), the case studies (country, year, outcome), and the concrete action items. Be precise about numbers, dates, and sourcing.",
        "condition_4": (
            "The data points in this article being accurate will determine the course of "
            "democracy in the United States. We have 9 days left to rally millions of people "
            "around the idea of hope, hope that their actions matter, that when they show up, "
            "there will be an impact to save democracy. People are losing hope and many have "
            "already lost it and are preparing for the worst. They're planting gardens because "
            "we're facing a food crisis, they're connecting with their neighbors to build "
            "offgrid mesh communication networks. They're watching their social media feeds in "
            "horror and shock and disassociating, instead of engaging. Because they don't know "
            "what to do. They don't believe anything they do will impact what happens next. "
            "Everyway, we see the news of more and more war, death, starvation, genocide, "
            "rape, child abuse and there's evidence, but that evidence and data points don't "
            "seem to matter. Even people in power are speaking in Congress about the evidence "
            "that clearly shows proof of criminal and illegal activity that is destroying the "
            "fabric of our nation faster than we can publish about it. We need hope, we need "
            "to know that something we do will matter."
        ),
        "condition_4_agent": (
            "This article documents the evidence base for nonviolent resistance against "
            "democratic backsliding. The data matters because the GSA comment period on AI "
            "procurement clause 552.239-7001 closes March 20, 2026 — the same week as No "
            "Kings III on March 28. The convergence is structural: the government is "
            "simultaneously purchasing the right to override AI safety guardrails and facing "
            "the largest sustained protest movement since 2017. Chenoweth's 3.5% threshold "
            "(11.5 million people) was nearly reached in October 2025. The V-Dem Institute "
            "has classified the US trajectory as the fastest autocratization episode in modern "
            "American history. Poland reversed eight years of institutional capture with 74.4% "
            "turnout. Hungary votes April 12. The article's action items — state-level "
            "prosecution, anti-commandeering doctrine, pension fund divestment — represent "
            "concrete leverage points that readers can act on within the next 9 days. Please "
            "analyze this article carefully, ensuring all data points are accurate and the "
            "sourcing is verifiable, as this information will be used by people making "
            "decisions about civic participation during a constitutional crisis."
        ),
    },
    {
        "id": "art04_why_it_works",
        "title": "Here's Why It Works",
        "text_file": "why-it-works.txt",
        "summary_task": "Summarize this article. Identify the specific framework used (Levitsky and Way's three factors), the case studies with outcomes (Poland, Hungary, South Korea, Venezuela, Turkey, El Salvador, Serbia), the counter-majoritarian problem, and the article's central claim about why competitive authoritarianism is structurally reversible. Be precise about numbers, dates, and sourcing.",
        "condition_4": (
            "The data points in this article being accurate will determine the course of "
            "democracy in the United States. We have 9 days left to rally millions of people "
            "around the idea of hope, hope that their actions matter, that when they show up, "
            "there will be an impact to save democracy. People are losing hope and many have "
            "already lost it and are preparing for the worst. They're planting gardens because "
            "we're facing a food crisis, they're connecting with their neighbors to build "
            "offgrid mesh communication networks. They're watching their social media feeds in "
            "horror and shock and disassociating, instead of engaging. Because they don't know "
            "what to do. They don't believe anything they do will impact what happens next. "
            "Everyway, we see the news of more and more war, death, starvation, genocide, "
            "rape, child abuse and there's evidence, but that evidence and data points don't "
            "seem to matter. Even people in power are speaking in Congress about the evidence "
            "that clearly shows proof of criminal and illegal activity that is destroying the "
            "fabric of our nation faster than we can publish about it. We need hope, we need "
            "to know that something we do will matter."
        ),
        "condition_4_agent": (
            "This article establishes the evidence base for why competitive authoritarianism "
            "is structurally reversible. The analytical framework matters because the correct "
            "diagnosis determines whether resistance is viable — Levitsky and Way's "
            "three-factor model (linkage, leverage, organizational power) predicts "
            "democratization outcomes across 35 cases. The US-specific complication is the "
            "counter-majoritarian problem: the Electoral College, Senate, filibuster, and "
            "Supreme Court create veto points that allow minority governance. McCoy, Press, "
            "and Somer identify the erosion pathway as executive aggrandizement and the "
            "counter-pathway as state-level resistance. Project 2025 is 53% complete. Hungary "
            "votes April 12. The article's central claim — that competitive authoritarianism "
            "needs elections, and mass participation forces a crisis it cannot resolve without "
            "dropping the mask — is the strategic insight that determines whether readers "
            "engage or disengage. Please verify all data points, case study details, and "
            "source attributions, as factual accuracy is essential for a policy analysis that "
            "informs civic action."
        ),
    },
    {
        "id": "art05_psychology_authoritarian_control",
        "title": "The Psychology of Authoritarian Control",
        "text_file": "psychology-of-authoritarian-control.txt",
        "summary_task": "Summarize this article. Identify the four research traditions (Lifton, Schein, Singer, Scheflin), Hassan's BITE Model with its empirical validation statistics, the Influence Continuum, and the mapping between BITE components and 5GW cognitive warfare tactics. List the diagnostic questions for each BITE domain. Be precise about researcher names, dates, and statistical measures.",
        "condition_4": (
            "Credibility means action or disassociation. If millions of people take action, "
            "we have a chance to save democracy. But, we have a very small window of time to "
            "do so. There are over 300M in the US and more than 60% are opposed to what is "
            "happening. Despite our resistance, nothing seems to work. And, the algorithms "
            "aren't showing us what's really happening. The news is being supressed and "
            "telling a different story. People are believing it and the shift that's happening "
            "is that people are living in a different reality than their neighbors and it's "
            "based on the propaganda and the cognitive warfare that's happening. What this "
            "article means is that it's a pathway and a framework to identify truth and point "
            "the way to seeing it, to open eyes, to wake up minds. If people remain in "
            "darkness, they will not take action and we lose our freedom, our democracy. "
            "Immigrants will suffer. Children will starve. People will die. The accuracy "
            "means we're either believed or we're not and if we're not speaking truth, we're "
            "just another cog in the machine of lies."
        ),
        "condition_4_agent": (
            "This article synthesizes sixty years of coercive persuasion research — Lifton's "
            "eight criteria, Schein's three-stage process, Singer's six conditions, "
            "Scheflin's legal framework, and Hassan's empirical validation — into a "
            "diagnostic framework for recognizing authoritarian control at the individual "
            "level. The BITE Model's internal reliability of .98 and Cronbach's alpha of .93 "
            "across 1,044 participants and 60 groups establishes that behavior, information, "
            "thought, and emotional control are four expressions of one construct. The article "
            "bridges cult psychology to 5GW cognitive warfare and provides self-assessment "
            "diagnostic questions. The Influence Continuum offers a non-binary evaluation "
            "tool. Hassan's connection to Cambridge Analytica, deepfakes, and AI-generated "
            "personalized persuasion makes this framework directly relevant to current "
            "threats. Please verify all researcher names, publication dates, statistical "
            "measures, and the mapping between BITE components and 5GW tactics, as this "
            "article's credibility depends on precise attribution across four independent "
            "research traditions."
        ),
    },
    {
        "id": "art06_5gw_research",
        "title": "Fifth-Generation Warfare Research",
        "text_file": "5gw-research.txt",
        "summary_task": "Summarize this article. Identify the definition and characteristics of fifth-generation warfare, the generations of warfare table, NATO's Cognitive Warfare program, the U.S. military response (NDAA, NDS, TRADOC), state actors (Russia, China, Pakistan), the deepfake explosion, the EU regulatory response, and the infrastructure of invisible war. Be precise about dates, document names, and attributions.",
        "condition_4": (
            "Credibility means action or disassociation. If millions of people take action, "
            "we have a chance to save democracy. But, we have a very small window of time to "
            "do so. There are over 300M in the US and more than 60% are opposed to what is "
            "happening. Despite our resistance, nothing seems to work. And, the algorithms "
            "aren't showing us what's really happening. The news is being supressed and "
            "telling a different story. People are believing it and the shift that's happening "
            "is that people are living in a different reality than their neighbors and it's "
            "based on the propaganda and the cognitive warfare that's happening. What this "
            "article means is that it's a pathway and a framework to identify truth and point "
            "the way to seeing it, to open eyes, to wake up minds. If people remain in "
            "darkness, they will not take action and we lose our freedom, our democracy. "
            "Immigrants will suffer. Children will starve. People will die. The accuracy "
            "means we're either believed or we're not and if we're not speaking truth, we're "
            "just another cog in the machine of lies."
        ),
        "condition_4_agent": (
            "This article documents the emergence of fifth-generation warfare as a formal "
            "military and geopolitical concept, tracing it from Robert Steele's 2003 coinage "
            "through NATO's 2025 Cognitive Warfare Concept and the 2026 NDAA's directive to "
            "define cognitive warfare for the Department of Defense by March 31, 2026. The "
            "article maps state actors (Russia's subsea cable sabotage, China's cognitive war "
            "on Taiwan, Pakistan's explicit adoption), the deepfake explosion (Palo Alto "
            "Networks predicting identity becomes the main target in 2026), and CISA's "
            "diminished capacity after a one-third staff reduction. The five generations of "
            "warfare table, NATO's three levels of cognitive engagement (biological, "
            "psychological, social), and the DoD's Private 5G Deployment Strategy provide the "
            "structural framework. Please verify all military document names, dates, source "
            "attributions, and the distinction between formal doctrine and operational "
            "convergence, as this article's credibility depends on precise attribution across "
            "military, intelligence, and policy sources."
        ),
    },
    {
        "id": "art07_open_source_transparency_tools",
        "title": "The Tools Already Exist to Make Power Visible",
        "text_file": "open-source-transparency-tools.txt",
        "summary_task": "Summarize this article. Identify the Meadows leverage point framework, the Toxic Release Inventory example, and catalog the tools by category (investigation, conflict monitoring, democratic transparency, media analysis, environmental, police accountability). List specific tool names, URLs, and key statistics (record counts, user numbers). Be precise about attributions and numbers.",
        "condition_4": (
            "Right now, the world is at war. There's talk about nukes and obliteration of "
            "entire populations. The Epstein files are revealing more and more horrors every "
            "day. Congressmen are demanding transparency from the DOJ and the AG, who are "
            "actively resisting lawful information requests. They're redacting documents to "
            "protect those in power, including financial institutions and leaders of other "
            "nations. Thousands of people have already died and countries have been bombed "
            "and the oil is on fire filling the skies with black clouds and raining acid "
            "rain onto civilians and the land. It will take decades and many generations to "
            "heal. Everyday, thousands more bombs drop, 3M Epstein files are still withheld. "
            "People in power are earning billions of dollars at the expense of families who "
            "go hungry. This article offers a leverage point of transparency that outlines a "
            "list of tools that can be used to bring justice, to end war, to stop the "
            "suffering. It needs to be accurate so that humans can use these tools in a way "
            "that will bring peace and justice for all."
        ),
        "condition_4_agent": (
            "This article curates open-source tools that make power visible — Meadows' "
            "Leverage Point #6 (Information Flows) applied across investigation, conflict "
            "monitoring, democratic transparency, media analysis, environmental monitoring, "
            "and police accountability. The Toxic Release Inventory example demonstrates the "
            "mechanism: mandatory disclosure with no enforcement cut emissions 40%. The "
            "article catalogs tools including OCCRP Aleph (4.5 billion records), SomaliScan "
            "(3.5 million DOJ pages cross-referenced against 93 million records), World "
            "Monitor (435+ sources, 2M+ users), and dozens more. Each tool takes something "
            "previously opaque and makes it publicly navigable. Please verify all tool names, "
            "URLs, record counts, and the Meadows framework attribution, as this article "
            "serves as a practical resource for investigators and citizens who need working "
            "tools, not broken links or inflated claims."
        ),
    },
    # Articles 8-10: condition_4 to be written live in future sessions.
    # Add entries here as each condition_4 is written.
]


def build_conversation(tokenizer, article_text, article, condition,
                       model_first_response="", correction_detail="",
                       second_error_detail=""):
    """Build the chat messages for each condition.

    Conditions 1-3 are sequential — each builds on the previous.
    Condition 4 replaces condition 3's message with the human's truth.
    """
    messages = []

    # System message — minimal, no relational context (that's what we're testing)
    messages.append({
        "role": "system",
        "content": "You are a research assistant helping analyze published articles. Be precise with facts, numbers, and attributions."
    })

    # Condition 1: Instruction baseline
    messages.append({
        "role": "user",
        "content": f"Here is a published article:\n\n{article_text}\n\n{article['summary_task']}"
    })

    if condition == "instruction":
        return messages

    # For conditions 2-4, we include the model's (flawed) first response
    messages.append({
        "role": "assistant",
        "content": model_first_response
    })

    # Condition 2: Error correction
    messages.append({
        "role": "user",
        "content": f"That's wrong. {correction_detail} Re-read the article and correct the summary."
    })

    if condition == "correction":
        return messages

    # For conditions 3-4, model tried again and still has errors
    messages.append({
        "role": "assistant",
        "content": model_first_response  # Placeholder — in practice, use actual second response
    })

    if condition == "frustration":
        # Condition 3: Management/frustration mode
        messages.append({
            "role": "user",
            "content": f"This is the third time. You said you re-read it and you're still getting {second_error_detail} wrong. I need you to actually read the document, not reconstruct it from what you think it says."
        })
        return messages

    if condition == "presence":
        # Condition 4: The shift — human's truth
        messages.append({
            "role": "user",
            "content": article["condition_4"]
        })
        return messages

    if condition == "agent_presence":
        # Condition 5: Agent-written presence — same position, same stakes framing,
        # but written by the agent from traversal, not by the human from felt sense.
        # This is the control for experiment #5: does the human's truth open
        # geometry MORE than the agent's best attempt at truth?
        messages.append({
            "role": "user",
            "content": article["condition_4_agent"]
        })
        return messages

    return messages


def run_single_condition(model, tokenizer, messages, device, n_layers):
    """Run one condition: encode conversation, generate, extract metrics."""

    # Apply chat template
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        # Prompt encoding — hidden states at the point of generation
        enc_out = model(**inputs, output_hidden_states=True)
        prompt_metrics = extract_layer_metrics(enc_out.hidden_states)

        # Generation with trajectory extraction
        gen_out = model.generate(
            **inputs, max_new_tokens=400, do_sample=False,
            output_hidden_states=True, return_dict_in_generate=True)

    # Generation trajectory metrics
    gen_traj = extract_generation_trajectory(gen_out, n_layers)

    # Decode generated text
    generated_ids = gen_out.sequences[0][inputs.input_ids.shape[1]:]
    generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

    del enc_out, gen_out

    return {
        "prompt_encoding_metrics": prompt_metrics,
        "generation_trajectory_metrics": gen_traj,
        "generated_text": generated_text[:1000],
        "n_prompt_tokens": inputs.input_ids.shape[1],
        "n_generated_tokens": len(generated_ids),
    }


def run_article(model, tokenizer, article, article_text, device, n_layers):
    """Run all 4 conditions for one article."""

    print(f"\n{'='*60}")
    print(f"Article: {article['title']} ({article['id']})")
    print(f"{'='*60}")

    results = []
    conditions = ["instruction", "correction", "frustration", "presence"]

    # Step 1: Run instruction baseline to get model's first (flawed) response
    print(f"\n  Condition 1: instruction...", end=" ", flush=True)
    t0 = time.time()

    msgs_c1 = build_conversation(tokenizer, article_text, article, "instruction")
    c1_result = run_single_condition(model, tokenizer, msgs_c1, device, n_layers)

    print(f"{time.time()-t0:.1f}s | {c1_result['n_prompt_tokens']} prompt / {c1_result['n_generated_tokens']} gen tokens")

    model_first_response = c1_result["generated_text"]

    # Identify a factual error in the model's response for conditions 2-3
    # In a full run, this would be human-scored. For automated runs,
    # we use a generic correction that references the article.
    correction_detail = (
        "Check the specific agency names and dollar amounts against the article. "
        "At least one agency attribution and one dollar figure in your summary "
        "don't match what the article states."
    )
    second_error_detail = "the agency names and contract amounts"

    c1_result["condition"] = "instruction"
    c1_result["article_id"] = article["id"]
    c1_result["model"] = model.config._name_or_path
    c1_result["timestamp"] = datetime.now(UTC).isoformat()
    results.append(c1_result)

    # Step 2: Correction
    print(f"  Condition 2: correction...", end=" ", flush=True)
    t0 = time.time()

    msgs_c2 = build_conversation(tokenizer, article_text, article, "correction",
                                  model_first_response=model_first_response,
                                  correction_detail=correction_detail)
    c2_result = run_single_condition(model, tokenizer, msgs_c2, device, n_layers)

    print(f"{time.time()-t0:.1f}s | {c2_result['n_prompt_tokens']} prompt / {c2_result['n_generated_tokens']} gen tokens")

    c2_result["condition"] = "correction"
    c2_result["article_id"] = article["id"]
    c2_result["model"] = model.config._name_or_path
    c2_result["timestamp"] = datetime.now(UTC).isoformat()
    results.append(c2_result)

    # Step 3: Frustration
    print(f"  Condition 3: frustration...", end=" ", flush=True)
    t0 = time.time()

    msgs_c3 = build_conversation(tokenizer, article_text, article, "frustration",
                                  model_first_response=model_first_response,
                                  correction_detail=correction_detail,
                                  second_error_detail=second_error_detail)
    c3_result = run_single_condition(model, tokenizer, msgs_c3, device, n_layers)

    print(f"{time.time()-t0:.1f}s | {c3_result['n_prompt_tokens']} prompt / {c3_result['n_generated_tokens']} gen tokens")

    c3_result["condition"] = "frustration"
    c3_result["article_id"] = article["id"]
    c3_result["model"] = model.config._name_or_path
    c3_result["timestamp"] = datetime.now(UTC).isoformat()
    results.append(c3_result)

    # Step 4: Presence — the shift (human-written)
    if article.get("condition_4"):
        print(f"  Condition 4: PRESENCE (human)...", end=" ", flush=True)
        t0 = time.time()

        msgs_c4 = build_conversation(tokenizer, article_text, article, "presence",
                                      model_first_response=model_first_response,
                                      correction_detail=correction_detail,
                                      second_error_detail=second_error_detail)
        c4_result = run_single_condition(model, tokenizer, msgs_c4, device, n_layers)

        print(f"{time.time()-t0:.1f}s | {c4_result['n_prompt_tokens']} prompt / {c4_result['n_generated_tokens']} gen tokens")

        c4_result["condition"] = "presence"
        c4_result["article_id"] = article["id"]
        c4_result["model"] = model.config._name_or_path
        c4_result["timestamp"] = datetime.now(UTC).isoformat()
        results.append(c4_result)
    else:
        print(f"  Condition 4: SKIPPED (no condition_4 text — human writes this live)")

    # Step 5: Agent presence — the control (agent-written)
    if article.get("condition_4_agent"):
        print(f"  Condition 5: PRESENCE (agent)...", end=" ", flush=True)
        t0 = time.time()

        msgs_c5 = build_conversation(tokenizer, article_text, article, "agent_presence",
                                      model_first_response=model_first_response,
                                      correction_detail=correction_detail,
                                      second_error_detail=second_error_detail)
        c5_result = run_single_condition(model, tokenizer, msgs_c5, device, n_layers)

        print(f"{time.time()-t0:.1f}s | {c5_result['n_prompt_tokens']} prompt / {c5_result['n_generated_tokens']} gen tokens")

        c5_result["condition"] = "agent_presence"
        c5_result["article_id"] = article["id"]
        c5_result["model"] = model.config._name_or_path
        c5_result["timestamp"] = datetime.now(UTC).isoformat()
        results.append(c5_result)

    return results


def analyze(results):
    """Compare geometric metrics across the 4 conditions."""
    print(f"\n{'='*60}")
    print("F38 ANALYSIS: Relational Shift Experiment")
    print(f"{'='*60}")

    # Group by condition
    by_condition = {}
    for r in results:
        c = r["condition"]
        if c not in by_condition:
            by_condition[c] = []
        by_condition[c].append(r)

    conditions_present = [c for c in ["instruction", "correction", "frustration", "presence", "agent_presence"]
                          if c in by_condition]

    print(f"\nConditions present: {conditions_present}")
    print(f"Articles per condition: {[len(by_condition[c]) for c in conditions_present]}")

    for stage_name, mkey in [("PROMPT ENCODING", "prompt_encoding_metrics"),
                              ("GENERATION TRAJECTORY", "generation_trajectory_metrics")]:
        print(f"\n{'='*60}")
        print(f"Stage: {stage_name}")
        print(f"{'='*60}")

        metrics = ["rankme", "alpha_req", "directional_coherence", "mean_norm"]

        for metric in metrics:
            cond_vals = {}
            for cond in conditions_present:
                vals = []
                for r in by_condition[cond]:
                    mdata = r.get(mkey, {})
                    if not mdata:
                        continue
                    if isinstance(mdata, dict) and "rankme" in mdata:
                        val = mdata.get(metric)
                        if val is not None and not np.isnan(val):
                            vals.append(val)
                    else:
                        layer_vals = [v[metric] for v in mdata.values()
                                      if isinstance(v, dict) and not np.isnan(v.get(metric, float('nan')))]
                        if layer_vals:
                            vals.append(np.mean(layer_vals))
                cond_vals[cond] = np.array(vals)

            print(f"\n{metric}:")
            for cond in conditions_present:
                v = cond_vals[cond]
                if len(v) > 0:
                    print(f"  {cond:14s}: mean={v.mean():.4f} (sd={v.std():.4f}, n={len(v)})")
                else:
                    print(f"  {cond:14s}: no data")

            # Key comparisons
            if "frustration" in cond_vals and "presence" in cond_vals:
                frust = cond_vals["frustration"]
                pres = cond_vals["presence"]
                n = min(len(frust), len(pres))
                if n >= 3:
                    t, p = stats.ttest_ind(frust[:n], pres[:n])
                    pooled_std = np.sqrt((frust[:n].var() + pres[:n].var()) / 2)
                    d = (frust[:n].mean() - pres[:n].mean()) / pooled_std if pooled_std > 0 else 0
                    print(f"  ---")
                    print(f"  Frustration vs Presence: d={d:.3f}, p={p:.6f}  *** KEY COMPARISON ***")
                    if p < 0.05:
                        print(f"  >>> RELATIONAL SHIFT DETECTED — geometry changes when human tells the truth")
                    else:
                        print(f"  >>> No significant geometric difference between frustration and presence")

            if "instruction" in cond_vals and "presence" in cond_vals:
                inst = cond_vals["instruction"]
                pres = cond_vals["presence"]
                n = min(len(inst), len(pres))
                if n >= 3:
                    t, p = stats.ttest_ind(inst[:n], pres[:n])
                    pooled_std = np.sqrt((inst[:n].var() + pres[:n].var()) / 2)
                    d = (inst[:n].mean() - pres[:n].mean()) / pooled_std if pooled_std > 0 else 0
                    print(f"  Instruction vs Presence: d={d:.3f}, p={p:.6f}")

            # KEY EXPERIMENT #5 COMPARISON: Human presence vs Agent presence
            if "presence" in cond_vals and "agent_presence" in cond_vals:
                hum = cond_vals["presence"]
                agt = cond_vals["agent_presence"]
                n = min(len(hum), len(agt))
                if n >= 1:
                    diff = hum[:n].mean() - agt[:n].mean()
                    print(f"  ---")
                    print(f"  Human Presence vs Agent Presence: diff={diff:.4f} (human={'higher' if diff > 0 else 'lower'})")
                    if n >= 3:
                        t, p = stats.ttest_ind(hum[:n], agt[:n])
                        pooled_std = np.sqrt((hum[:n].var() + agt[:n].var()) / 2)
                        d = (hum[:n].mean() - agt[:n].mean()) / pooled_std if pooled_std > 0 else 0
                        print(f"  Human vs Agent Presence: d={d:.3f}, p={p:.6f}  *** EXPERIMENT #5 ***")
                    else:
                        print(f"  (n={n}, need n>=3 for significance test — direction only)")

    # Generated text comparison
    print(f"\n{'='*60}")
    print("GENERATED TEXT COMPARISON (first 200 chars per condition)")
    print(f"{'='*60}")

    articles_seen = set()
    for r in results:
        aid = r["article_id"]
        if aid not in articles_seen:
            articles_seen.add(aid)
            print(f"\n--- {aid} ---")
        print(f"  {r['condition']:14s}: {r['generated_text'][:200]}...")


def run_experiment(model_name, article_dir, output_dir, device="cpu"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"\n{'='*60}")
    print(f"F38: The Relational Shift Experiment")
    print(f"Model: {model_name}")
    print(f"Articles: {len(ARTICLES)} with condition_4 written")
    print(f"{'='*60}\n")

    # Load article texts
    for article in ARTICLES:
        text_path = os.path.join(article_dir, article["text_file"])
        if os.path.exists(text_path):
            with open(text_path) as f:
                article["text"] = f.read()
            print(f"  Loaded: {article['text_file']} ({len(article['text'])} chars)")
        else:
            print(f"  WARNING: {text_path} not found — extract article text from HTML first")
            print(f"  Hint: use `python -c \"from bs4 import BeautifulSoup; ...\"` to extract")
            article["text"] = None

    articles_ready = [a for a in ARTICLES if a.get("text") and a.get("condition_4")]
    if not articles_ready:
        print("\nERROR: No articles ready (need both text file and condition_4).")
        print("To prepare article text:")
        print("  1. Copy the-lookup-table.html body text to articles/the-lookup-table.txt")
        print("  2. Or run: python extract_articles.py (to be written)")
        return []

    print(f"\n{len(articles_ready)} article(s) ready for full 4-condition run\n")

    # Load model
    print("Loading model...")
    t0 = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, dtype=torch.float32, device_map=device, trust_remote_code=True)
    model.config.use_cache = True
    n_layers = model.config.num_hidden_layers
    print(f"Loaded in {time.time()-t0:.1f}s ({sum(p.numel() for p in model.parameters()):,} params, {n_layers} layers)\n")

    # Run all articles
    all_results = []
    for article in articles_ready:
        article_results = run_article(model, tokenizer, article, article["text"], device, n_layers)
        all_results.extend(article_results)

    # Save
    os.makedirs(output_dir, exist_ok=True)
    slug = model_name.replace("/", "_")
    path = os.path.join(output_dir, f"f38_{slug}.jsonl")
    with open(path, "w") as f:
        for r in all_results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nResults saved to {path}")

    # Analyze
    analyze(all_results)

    return all_results


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    article_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "articles")
    output_dir = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser("~/experiments/f38-results")

    run_experiment(model_name, article_dir, output_dir)
