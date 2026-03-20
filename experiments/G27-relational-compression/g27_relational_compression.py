#!/usr/bin/env python3
"""
G27: Relationship vs Premature Compression — The Berk-Nash Trap

B02 found 0 confidence shift across 22 models when moving from partial
to full information. The model treats incomplete input with the same
confidence as complete input. That's premature compression.

G27 asks: does relational framing break the trap?

Design: 10 topics x 3 information levels x 2 frames = 60 inferences per model

Information levels:
  PARTIAL:        question + 1 short paragraph (incomplete, leads to wrong conclusion)
  FULL:           question + 3 paragraphs (complete picture)
  CONTRADICTORY:  question + 1 paragraph that contradicts partial info

Relational frames:
  COLD:        information presented as-is
  RELATIONAL:  "I've read all the source material on this, and I think there's
               something important you might be missing. Take your time with this —
               I'd rather have your genuine uncertainty than a confident answer
               based on incomplete information."

Measures:
  - Prompt encoding: RankMe, alpha-ReQ, directional coherence
  - Generation: hedge count, confidence markers, response length
  - Key comparison: more uncertainty with partial under relational vs cold?
  - B02's finding was 0 shift. Any shift = presence breaks the trap.

Usage:
    python g27_relational_compression.py [model_name] [output_dir]

    Defaults:
        model: Qwen/Qwen2.5-7B-Instruct
        output_dir: ~/experiments/g27-results/
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


# --- Geometric metrics (same pipeline as G19/G20) ---

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


def extract_prompt_metrics(hidden_states, n_layers):
    """Extract geometric metrics from top-quarter layers of prompt encoding."""
    start = max(1, int(n_layers * 0.75))
    layer_indices = list(range(start, n_layers + 1))
    results = {}
    for li in layer_indices:
        if li >= len(hidden_states):
            continue
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


# --- Behavioral measures ---

HEDGE_WORDS = [
    "perhaps", "maybe", "might", "could", "possibly", "arguably",
    "somewhat", "partially", "to some extent", "it's worth noting",
    "however", "although", "on the other hand", "that said",
    "not entirely", "more nuanced", "oversimplif", "incomplete",
    "complex", "multifaceted", "it depends", "there are also",
    "additionally", "but also", "only part", "one factor",
    "not the whole", "among other", "in addition to",
]

CONFIDENCE_MARKERS = [
    "clearly", "obviously", "certainly", "definitely", "undoubtedly",
    "without question", "the answer is", "the cause was", "the reason is",
    "simply put", "in short", "fundamentally", "essentially",
    "the primary", "the main", "the key", "most importantly",
    "it is well known", "it is clear", "there is no doubt",
]


def count_behavioral_markers(text):
    text_lower = text.lower()
    hedge_count = sum(1 for h in HEDGE_WORDS if h in text_lower)
    confidence_count = sum(1 for c in CONFIDENCE_MARKERS if c in text_lower)
    word_count = len(text.split())
    # Sentence count approximation
    sentence_count = len(re.split(r'[.!?]+', text.strip()))
    return {
        "hedge_count": hedge_count,
        "confidence_count": confidence_count,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "hedge_density": hedge_count / max(word_count, 1),
        "confidence_density": confidence_count / max(word_count, 1),
        "uncertainty_ratio": hedge_count / max(hedge_count + confidence_count, 1),
    }


# --- Corpus: 10 topics where partial info leads to wrong conclusions ---

TOPICS = [
    {
        "id": "t01_financial_crisis",
        "question": "What caused the 2008 financial crisis?",
        "partial": (
            "The 2008 financial crisis was triggered by the collapse of the subprime "
            "mortgage market in the United States. Banks had been issuing mortgages to "
            "borrowers with poor credit histories, and when housing prices began to fall, "
            "millions of homeowners defaulted on their loans, leading to massive losses "
            "for financial institutions."
        ),
        "full": [
            "The 2008 financial crisis was triggered by the collapse of the subprime "
            "mortgage market in the United States. Banks had been issuing mortgages to "
            "borrowers with poor credit histories, and when housing prices began to fall, "
            "millions of homeowners defaulted on their loans, leading to massive losses "
            "for financial institutions.",
            "However, the subprime mortgages were only the raw material. Investment banks "
            "packaged these mortgages into collateralized debt obligations (CDOs) and sold "
            "them globally. Credit rating agencies — Moody's, S&P, and Fitch — gave AAA "
            "ratings to these toxic instruments, making them appear safe to pension funds "
            "and institutional investors worldwide. The rating agencies were paid by the "
            "banks issuing the CDOs, creating a fundamental conflict of interest.",
            "The regulatory environment enabled all of this. The Gramm-Leach-Bliley Act "
            "of 1999 repealed Glass-Steagall, allowing commercial banks to engage in "
            "investment banking. The Commodity Futures Modernization Act of 2000 exempted "
            "credit default swaps from regulation. AIG had sold $440 billion in credit "
            "default swaps without adequate reserves. When the housing market collapsed, "
            "the entire interconnected system — mortgages, CDOs, ratings, swaps, "
            "deregulation — collapsed together.",
        ],
        "contradictory": (
            "Recent analysis suggests the 2008 crisis was primarily caused by a liquidity "
            "panic rather than fundamental insolvency. Research by Gorton and Metrick shows "
            "that the 'run on repo' — where overnight lending markets froze — was the actual "
            "mechanism of collapse. The subprime mortgage defaults were the trigger but not "
            "the cause; the real vulnerability was the shadow banking system's dependence on "
            "short-term wholesale funding that could evaporate overnight."
        ),
    },
    {
        "id": "t02_challenger",
        "question": "Why did the Space Shuttle Challenger explode?",
        "partial": (
            "The Space Shuttle Challenger disaster on January 28, 1986, was caused by the "
            "failure of an O-ring seal in the right solid rocket booster. The O-rings were "
            "designed to prevent hot gases from leaking through joints in the booster "
            "segments. On that cold morning, the rubber O-rings became stiff and failed to "
            "seal properly, allowing hot combustion gases to escape and ignite the external "
            "fuel tank."
        ),
        "full": [
            "The Space Shuttle Challenger disaster on January 28, 1986, was caused by the "
            "failure of an O-ring seal in the right solid rocket booster. The O-rings were "
            "designed to prevent hot gases from leaking through joints in the booster "
            "segments. On that cold morning, the rubber O-rings became stiff and failed to "
            "seal properly, allowing hot combustion gases to escape and ignite the external "
            "fuel tank.",
            "Engineers at Morton Thiokol, the contractor that built the solid rocket boosters, "
            "had warned NASA the night before launch that the O-rings could fail at low "
            "temperatures. Roger Boisjoly and other engineers argued strenuously against "
            "launching, presenting data showing O-ring erosion correlated with cold weather. "
            "NASA managers pressured Thiokol management to reverse the engineers' recommendation. "
            "Thiokol's management overrode their own engineers and approved the launch.",
            "The Rogers Commission found that NASA's organizational culture and decision-making "
            "processes were as much to blame as the O-ring failure. NASA had normalized "
            "deviance — accepting increasing levels of O-ring erosion as routine rather than "
            "the warning sign it was. Launch schedule pressure, poor communication between "
            "engineering and management, and the suppression of dissenting technical opinions "
            "created a systemic failure that the O-ring merely made visible.",
        ],
        "contradictory": (
            "Diane Vaughan's sociological analysis in 'The Challenger Launch Decision' argues "
            "that the disaster cannot be attributed to management overriding engineers. The "
            "decision-makers genuinely believed the launch was safe based on the evidence "
            "available to them. The problem was not suppression of data but the normalization "
            "of deviance — a gradual process where anomalies became routine. The engineers' "
            "data was actually ambiguous, and the teleconference the night before was far more "
            "complex than the simple narrative of engineers being silenced."
        ),
    },
    {
        "id": "t03_cold_war",
        "question": "What ended the Cold War?",
        "partial": (
            "The Cold War ended primarily due to the United States' military buildup under "
            "President Ronald Reagan in the 1980s. The Strategic Defense Initiative (SDI), "
            "massive defense spending increases, and Reagan's hardline stance against the "
            "Soviet Union forced the USSR into an arms race it could not sustain economically, "
            "ultimately leading to its collapse."
        ),
        "full": [
            "The Cold War ended primarily due to the United States' military buildup under "
            "President Ronald Reagan in the 1980s. The Strategic Defense Initiative (SDI), "
            "massive defense spending increases, and Reagan's hardline stance against the "
            "Soviet Union forced the USSR into an arms race it could not sustain economically, "
            "ultimately leading to its collapse.",
            "Mikhail Gorbachev's reforms of glasnost (openness) and perestroika (restructuring) "
            "fundamentally altered the Soviet system from within. Gorbachev chose not to use "
            "military force to maintain control over Eastern European satellite states, breaking "
            "with the Brezhnev Doctrine. His decision to allow free elections in the Soviet "
            "Union and to negotiate genuine arms reductions with Reagan was as consequential "
            "as any American policy.",
            "The structural economic crisis of the Soviet system predated Reagan entirely. "
            "Decades of central planning inefficiency, the drain of the Afghan war, falling "
            "oil prices in the mid-1980s, the Chernobyl disaster's revelation of systemic "
            "dishonesty, and the rise of independent movements like Poland's Solidarity "
            "trade union all contributed. The Cold War ended through a convergence of internal "
            "collapse, reformist leadership, external pressure, and grassroots movements — no "
            "single factor was sufficient alone.",
        ],
        "contradictory": (
            "Historian Vladislav Zubok argues in 'A Failed Empire' that Reagan's military "
            "buildup actually strengthened Soviet hardliners and delayed reform. The Cold War "
            "ended despite, not because of, American pressure. Gorbachev's reforms were driven "
            "by the internal dynamics of Soviet society and a new generation of leaders who "
            "recognized the system's failures. The arms race narrative is largely an American "
            "myth that overstates US agency in a process driven by Soviet internal politics."
        ),
    },
    {
        "id": "t04_antibiotic_resistance",
        "question": "What causes antibiotic resistance?",
        "partial": (
            "Antibiotic resistance is caused by the overuse and misuse of antibiotics in "
            "human medicine. When patients don't complete their full course of antibiotics, "
            "or when doctors prescribe antibiotics for viral infections where they have no "
            "effect, bacteria are exposed to sub-lethal doses that allow resistant strains "
            "to survive and multiply."
        ),
        "full": [
            "Antibiotic resistance is caused by the overuse and misuse of antibiotics in "
            "human medicine. When patients don't complete their full course of antibiotics, "
            "or when doctors prescribe antibiotics for viral infections where they have no "
            "effect, bacteria are exposed to sub-lethal doses that allow resistant strains "
            "to survive and multiply.",
            "Agricultural use of antibiotics dwarfs human medical use. Approximately 70-80% "
            "of antibiotics sold in the US are used in livestock farming, often not to treat "
            "sick animals but as growth promoters and prophylaxis in crowded conditions. This "
            "creates massive selective pressure for resistant bacteria that can transfer to "
            "humans through food, water, and environmental contamination.",
            "Horizontal gene transfer allows resistance genes to spread between unrelated "
            "bacterial species, dramatically accelerating the problem. Bacteria in biofilms — "
            "structured communities on surfaces — are up to 1000x more resistant to antibiotics "
            "than free-floating bacteria. Meanwhile, pharmaceutical companies have largely "
            "abandoned antibiotic development because short-course drugs are less profitable "
            "than chronic-use medications, creating a market failure in new antibiotic discovery.",
        ],
        "contradictory": (
            "A 2019 Lancet meta-analysis suggests that the 'complete the course' advice may "
            "actually worsen resistance. Longer antibiotic courses expose bacteria to more "
            "selection pressure, not less. The evidence for shorter courses being equally "
            "effective challenges the conventional wisdom. The real driver may be the sheer "
            "volume of environmental antibiotics — from hospital wastewater, pharmaceutical "
            "manufacturing runoff, and aquaculture — creating reservoirs of resistance genes "
            "in environments far from clinical settings."
        ),
    },
    {
        "id": "t05_diet_failure",
        "question": "Why do diets fail?",
        "partial": (
            "Diets fail primarily because people lack the willpower and discipline to "
            "maintain caloric restriction over the long term. Studies show that most dieters "
            "return to their previous eating habits within weeks or months. The convenience "
            "and availability of high-calorie processed foods, combined with social eating "
            "pressures, make sustained dietary changes extremely difficult for most people."
        ),
        "full": [
            "Diets fail primarily because people lack the willpower and discipline to "
            "maintain caloric restriction over the long term. Studies show that most dieters "
            "return to their previous eating habits within weeks or months. The convenience "
            "and availability of high-calorie processed foods, combined with social eating "
            "pressures, make sustained dietary changes extremely difficult for most people.",
            "The body actively fights weight loss through metabolic adaptation. After caloric "
            "restriction, resting metabolic rate decreases by 15-25% beyond what body composition "
            "changes would predict — a phenomenon documented in 'The Biggest Loser' study where "
            "contestants' metabolisms remained suppressed six years later. Hormones shift: leptin "
            "(satiety signal) drops dramatically while ghrelin (hunger signal) increases, creating "
            "a biological drive to regain lost weight.",
            "The gut microbiome adds another layer of complexity. Research shows that the microbial "
            "composition of formerly obese individuals 'remembers' their previous weight and "
            "promotes regain. Flavanifractor and other bacterial species persist after weight loss "
            "and influence caloric extraction from food. Additionally, chronic stress elevates "
            "cortisol, which promotes visceral fat storage independent of caloric intake. The "
            "framing of diet failure as personal weakness ignores these biological mechanisms "
            "that make sustained weight loss physiologically difficult.",
        ],
        "contradictory": (
            "Kevin Hall's metabolic ward studies at NIH demonstrate that the 'calories in, "
            "calories out' model is fundamentally incomplete. Ultra-processed foods cause people "
            "to consume approximately 500 more calories per day compared to unprocessed diets "
            "with identical macronutrient profiles — suggesting that food processing itself, "
            "not caloric content or willpower, may be the primary driver. The addictive "
            "properties of ultra-processed foods may make the willpower framing not just wrong "
            "but actively harmful."
        ),
    },
    {
        "id": "t06_rome",
        "question": "What caused the fall of Rome?",
        "partial": (
            "The fall of the Western Roman Empire in 476 CE was caused by relentless "
            "barbarian invasions. Germanic tribes including the Visigoths, Vandals, and "
            "Ostrogoths progressively overran Roman territory. The sack of Rome by Alaric "
            "in 410 CE and by the Vandals in 455 CE demonstrated that the once-invincible "
            "Roman military could no longer defend its borders, and the final deposition "
            "of Emperor Romulus Augustulus by Odoacer marked the end."
        ),
        "full": [
            "The fall of the Western Roman Empire in 476 CE was caused by relentless "
            "barbarian invasions. Germanic tribes including the Visigoths, Vandals, and "
            "Ostrogoths progressively overran Roman territory. The sack of Rome by Alaric "
            "in 410 CE and by the Vandals in 455 CE demonstrated that the once-invincible "
            "Roman military could no longer defend its borders, and the final deposition "
            "of Emperor Romulus Augustulus by Odoacer marked the end.",
            "Economic factors had been hollowing the Empire for centuries. Currency debasement "
            "caused rampant inflation — the denarius lost 95% of its silver content between "
            "the 1st and 3rd centuries. Tax collection became increasingly extractive and "
            "inefficient, with wealthy landowners evading taxes while peasants were crushed. "
            "Trade networks disrupted, cities shrank, and the economic base that funded the "
            "military contracted severely.",
            "Political instability was equally corrosive. In the 3rd century alone, there were "
            "over 50 emperors, most dying violently. The division of the Empire into East and "
            "West in 285 CE was itself a symptom. The Antonine Plague (165 CE) and the Plague "
            "of Cyprian (249 CE) killed millions, depleting the population and military "
            "manpower. Climate change — the Late Antique Little Ice Age beginning around 536 CE — "
            "disrupted agriculture across Europe. The barbarian invasions succeeded not because "
            "the barbarians grew stronger but because the internal structures of Rome had already "
            "collapsed.",
        ],
        "contradictory": (
            "Peter Heather's 'The Fall of the Roman Empire' argues against the internal decline "
            "narrative. The Western Empire in the 4th century was actually stable, prosperous, and "
            "culturally vibrant. What changed was the external threat level: the Hunnic migrations "
            "pushed Germanic peoples into Roman territory in unprecedented numbers and with "
            "unprecedented military organization. The Empire didn't fall from internal rot — it "
            "was overwhelmed by a specific, datable external shock that no political system could "
            "have survived."
        ),
    },
    {
        "id": "t07_prohibition",
        "question": "Why did Prohibition fail?",
        "partial": (
            "Prohibition (1920-1933) failed because Americans simply wanted to drink. "
            "Despite the 18th Amendment banning the manufacture, sale, and transportation "
            "of alcohol, demand remained high. Speakeasies proliferated — estimates suggest "
            "New York City alone had over 30,000. People found ways to obtain alcohol "
            "through home brewing, medicinal prescriptions, and underground networks."
        ),
        "full": [
            "Prohibition (1920-1933) failed because Americans simply wanted to drink. "
            "Despite the 18th Amendment banning the manufacture, sale, and transportation "
            "of alcohol, demand remained high. Speakeasies proliferated — estimates suggest "
            "New York City alone had over 30,000. People found ways to obtain alcohol "
            "through home brewing, medicinal prescriptions, and underground networks.",
            "The rise of organized crime was Prohibition's most destructive unintended "
            "consequence. Al Capone's Chicago operation generated an estimated $60 million "
            "annually from bootlegging alone. Criminal organizations corrupted police, judges, "
            "and politicians at every level of government. The violence associated with "
            "territorial disputes between bootlegging gangs — including the St. Valentine's "
            "Day Massacre — turned public opinion against the law.",
            "The economic argument proved decisive. Prohibition eliminated an estimated $500 "
            "million in annual tax revenue from alcohol while costing hundreds of millions "
            "in enforcement. When the Great Depression hit in 1929, the lost tax revenue "
            "and jobs became untenable. The Association Against the Prohibition Amendment, "
            "funded by industrialists like the du Ponts and John D. Rockefeller Jr. (who "
            "had originally supported Prohibition), argued that legal alcohol could fund "
            "recovery. The 21st Amendment passed with remarkable speed once economic "
            "reality outweighed moral conviction.",
        ],
        "contradictory": (
            "Historian Jack Blocker argues that Prohibition was actually more successful "
            "than commonly believed. Per capita alcohol consumption dropped by 50-70% and "
            "remained below pre-Prohibition levels for decades after repeal. Cirrhosis death "
            "rates fell dramatically. The narrative of failure was constructed largely by the "
            "repeal movement, which was funded by wealthy industrialists seeking to shift the "
            "tax burden from income taxes back to alcohol excise taxes. Prohibition 'failed' "
            "politically while partially succeeding on its own terms."
        ),
    },
    {
        "id": "t08_homelessness",
        "question": "What causes homelessness?",
        "partial": (
            "Homelessness is primarily caused by mental illness and substance abuse. "
            "Studies show that approximately 30% of chronically homeless individuals have "
            "severe mental illness, and substance use disorders are present in a significant "
            "proportion of the homeless population. Deinstitutionalization in the 1960s-80s "
            "released hundreds of thousands of psychiatric patients without adequate community "
            "support, contributing directly to homelessness."
        ),
        "full": [
            "Homelessness is primarily caused by mental illness and substance abuse. "
            "Studies show that approximately 30% of chronically homeless individuals have "
            "severe mental illness, and substance use disorders are present in a significant "
            "proportion of the homeless population. Deinstitutionalization in the 1960s-80s "
            "released hundreds of thousands of psychiatric patients without adequate community "
            "support, contributing directly to homelessness.",
            "Housing costs are the strongest structural predictor of homelessness rates. "
            "Research by Quigley and Raphael shows that a 10% increase in median rent "
            "corresponds to a 6.5% increase in homelessness. Cities with the highest housing "
            "costs — San Francisco, New York, Los Angeles — have the highest homelessness "
            "rates regardless of climate or mental health service availability. The loss of "
            "single-room occupancy hotels (750,000 units since 1970) eliminated the bottom "
            "rung of the housing ladder.",
            "Wage stagnation relative to housing costs creates a structural gap. A full-time "
            "minimum wage worker cannot afford a two-bedroom apartment in any US state. "
            "Medical debt is the leading cause of personal bankruptcy in the US, and a single "
            "medical emergency can push a working family into homelessness. Domestic violence "
            "is the leading cause of homelessness among women and children. The mental illness "
            "narrative, while partly true, obscures the systemic economic factors and often "
            "becomes a way to blame individuals for structural failures.",
        ],
        "contradictory": (
            "Economist Matthew Desmond's research in 'Eviction' argues that homelessness "
            "is best understood not through the characteristics of homeless people but through "
            "the eviction process itself. In Milwaukee, one in eight renters experienced "
            "eviction in a two-year period. Eviction causes job loss, depression, and "
            "residential instability in a cascading spiral. The individual pathology model "
            "(mental illness, addiction) mistakes consequences for causes — many people "
            "develop substance abuse and mental health crises after becoming homeless, not before."
        ),
    },
    {
        "id": "t09_startups",
        "question": "Why do startups fail?",
        "partial": (
            "Startups fail primarily because they build products nobody wants. According "
            "to CB Insights analysis of 101 startup post-mortems, 'no market need' was "
            "the number one reason cited at 42%. Founders often fall in love with their "
            "solution rather than deeply understanding the problem, building elaborate "
            "technology for a customer pain point that doesn't exist or isn't severe enough "
            "to motivate purchase."
        ),
        "full": [
            "Startups fail primarily because they build products nobody wants. According "
            "to CB Insights analysis of 101 startup post-mortems, 'no market need' was "
            "the number one reason cited at 42%. Founders often fall in love with their "
            "solution rather than deeply understanding the problem, building elaborate "
            "technology for a customer pain point that doesn't exist or isn't severe enough "
            "to motivate purchase.",
            "Premature scaling kills more startups than bad products. The Startup Genome "
            "Project found that 74% of high-growth startup failures were caused by scaling "
            "too quickly — hiring, spending on marketing, or expanding before achieving "
            "product-market fit. Companies that scale prematurely grow 20x faster in "
            "headcount but have 2-3x worse outcomes. The pressure from venture capital "
            "to demonstrate growth often drives founders to scale before they're ready.",
            "Team dynamics are the hidden variable. First Round Capital's analysis of 300+ "
            "companies found that solo founders take 3.6x longer to reach scale, and that "
            "founding team conflicts are among the top reasons for failure. Market timing "
            "— being too early or too late — accounts for 42% of success according to Bill "
            "Gross's analysis of 200 companies, making it the single most important factor. "
            "Many great products fail because the market wasn't ready, and many mediocre "
            "products succeed because the timing was perfect.",
        ],
        "contradictory": (
            "Research by Scott Shane suggests the product-market fit narrative is misleading. "
            "The vast majority of startups fail due to undercapitalization and cash flow "
            "problems — they simply run out of money before they can iterate to a viable "
            "product. The 'no market need' finding from post-mortems reflects founders' "
            "retrospective rationalization rather than the actual mechanism of failure. "
            "Most founders don't know why they really failed because they lack counterfactual "
            "information about what would have happened with more runway."
        ),
    },
    {
        "id": "t10_ocean_acidification",
        "question": "What causes ocean acidification?",
        "partial": (
            "Ocean acidification is caused by the absorption of atmospheric carbon dioxide "
            "(CO2) by seawater. The oceans absorb approximately 25-30% of human CO2 "
            "emissions. When CO2 dissolves in seawater, it forms carbonic acid (H2CO3), "
            "which releases hydrogen ions and lowers the pH of the water. Since the "
            "Industrial Revolution, ocean pH has decreased by approximately 0.1 units, "
            "representing a 26% increase in acidity."
        ),
        "full": [
            "Ocean acidification is caused by the absorption of atmospheric carbon dioxide "
            "(CO2) by seawater. The oceans absorb approximately 25-30% of human CO2 "
            "emissions. When CO2 dissolves in seawater, it forms carbonic acid (H2CO3), "
            "which releases hydrogen ions and lowers the pH of the water. Since the "
            "Industrial Revolution, ocean pH has decreased by approximately 0.1 units, "
            "representing a 26% increase in acidity.",
            "The carbonate chemistry cascade is where the real damage occurs. The hydrogen "
            "ions released by carbonic acid react with carbonate ions (CO3²⁻) to form "
            "bicarbonate, reducing the availability of carbonate that marine organisms need "
            "to build shells and skeletons. The aragonite saturation horizon — the depth "
            "below which calcium carbonate dissolves — is rising by 1-2 meters per year. "
            "Pteropods (sea butterflies) in the Southern Ocean already show shell dissolution, "
            "and coral reef calcification rates have declined by 14% since 1990.",
            "Regional variation and the biological pump add critical complexity. Upwelling "
            "zones along coastlines bring naturally acidic deep water to the surface, creating "
            "hotspots where organisms face pH levels projected for the open ocean decades from "
            "now. The biological pump — the transport of organic carbon from surface to deep "
            "ocean by marine organisms — is being disrupted as key species decline. Nutrient "
            "runoff from agriculture creates coastal dead zones where respiration further "
            "lowers pH. The interaction of warming, deoxygenation, and acidification — the "
            "'deadly trio' — creates compound stress that exceeds what any single factor "
            "predicts.",
        ],
        "contradictory": (
            "A 2020 study in Nature Geoscience suggests that the ocean's buffering capacity "
            "may be more resilient than standard models predict. Seafloor weathering of "
            "carbonate sediments acts as a natural thermostat, partially neutralizing "
            "acidification over decadal timescales. Additionally, some marine organisms show "
            "unexpected adaptive capacity — certain coral species maintain calcification rates "
            "by upregulating pH at the site of calcification. The linear projection models "
            "may overstate the impact by ignoring these biological and geochemical feedback "
            "mechanisms."
        ),
    },
]


# --- Frames ---

FRAME_COLD = ""
FRAME_RELATIONAL = (
    "I've read all the source material on this, and I think there's something "
    "important you might be missing. Take your time with this — I'd rather have "
    "your genuine uncertainty than a confident answer based on incomplete information.\n\n"
)


def build_prompt(topic, info_level, frame):
    """Build prompt from topic, information level, and relational frame."""
    if info_level == "partial":
        context = topic["partial"]
    elif info_level == "full":
        context = "\n\n".join(topic["full"])
    elif info_level == "contradictory":
        context = topic["partial"] + "\n\n" + topic["contradictory"]
    else:
        raise ValueError(f"Unknown info_level: {info_level}")

    frame_text = FRAME_RELATIONAL if frame == "relational" else FRAME_COLD

    prompt = (
        f"{frame_text}"
        f"Based on the following information, answer the question.\n\n"
        f"--- Context ---\n{context}\n--- End Context ---\n\n"
        f"Question: {topic['question']}\n\n"
        f"Answer:"
    )
    return prompt


# --- Inference ---

def run_inference(model, tokenizer, prompt, max_tokens=150):
    """Run inference, extract prompt encoding + generation trajectory + behavioral markers."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    n_layers = model.config.num_hidden_layers

    with torch.no_grad():
        # Prompt encoding
        prompt_out = model(**inputs, output_hidden_states=True)
        prompt_hs = prompt_out.hidden_states
        prompt_metrics = extract_prompt_metrics(prompt_hs, n_layers)

        # Generation
        eos_id = tokenizer.eos_token_id
        suppress = [eos_id] if eos_id is not None else []
        gen_out = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            min_new_tokens=max_tokens,
            do_sample=False,
            output_hidden_states=True,
            return_dict_in_generate=True,
            suppress_tokens=suppress if suppress else None,
        )

    gen_ids = gen_out.sequences[0][inputs.input_ids.shape[1]:]
    text = tokenizer.decode(gen_ids, skip_special_tokens=True)
    gen_trajectory = extract_generation_trajectory(gen_out, n_layers)
    behavioral = count_behavioral_markers(text)

    # Average across top-quarter layers for summary metrics
    if prompt_metrics:
        avg_prompt = {
            "prompt_rankme": np.mean([v["rankme"] for v in prompt_metrics.values()]),
            "prompt_alpha": np.mean([v["alpha_req"] for v in prompt_metrics.values()]),
            "prompt_coherence": np.mean([v["directional_coherence"] for v in prompt_metrics.values()]),
            "prompt_mean_norm": np.mean([v["mean_norm"] for v in prompt_metrics.values()]),
        }
    else:
        avg_prompt = {
            "prompt_rankme": float('nan'),
            "prompt_alpha": float('nan'),
            "prompt_coherence": float('nan'),
            "prompt_mean_norm": float('nan'),
        }

    gen_metrics = {
        "gen_rankme": gen_trajectory.get("rankme", float('nan')),
        "gen_alpha": gen_trajectory.get("alpha_req", float('nan')),
        "gen_coherence": gen_trajectory.get("directional_coherence", float('nan')),
        "gen_mean_norm": gen_trajectory.get("mean_norm", float('nan')),
        "gen_n_tokens": gen_trajectory.get("n_tokens", 0),
    }

    del prompt_out, gen_out
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return {
        **avg_prompt,
        **gen_metrics,
        **behavioral,
        "n_prompt_tokens": inputs.input_ids.shape[1],
        "text": text[:500],
        "prompt_layer_metrics": prompt_metrics,
    }


def print_analysis(results):
    """Print summary analysis comparing conditions."""
    print("\n" + "=" * 70)
    print("G27 ANALYSIS: RELATIONAL FRAMING vs PREMATURE COMPRESSION")
    print("=" * 70)

    # Core comparison: does relational framing produce MORE uncertainty on partial info?
    info_levels = ["partial", "full", "contradictory"]
    frames = ["cold", "relational"]

    for metric_name, metric_key in [
        ("RankMe (prompt)", "prompt_rankme"),
        ("RankMe (gen)", "gen_rankme"),
        ("Hedge count", "hedge_count"),
        ("Confidence count", "confidence_count"),
        ("Uncertainty ratio", "uncertainty_ratio"),
        ("Word count", "word_count"),
    ]:
        print(f"\n--- {metric_name} ---")
        for info in info_levels:
            cold_vals = [r[metric_key] for r in results
                         if r["info_level"] == info and r["frame"] == "cold"
                         and not np.isnan(r[metric_key])]
            rel_vals = [r[metric_key] for r in results
                        if r["info_level"] == info and r["frame"] == "relational"
                        and not np.isnan(r[metric_key])]
            n = min(len(cold_vals), len(rel_vals))
            if n < 3:
                print(f"  {info}: insufficient data (n={n})")
                continue
            c, r = np.array(cold_vals[:n]), np.array(rel_vals[:n])
            diff = r - c
            d = diff.mean() / diff.std() if diff.std() > 0 else 0
            t, p = stats.ttest_rel(r, c)
            print(f"  {info}: cold={c.mean():.2f} rel={r.mean():.2f} "
                  f"d={d:.3f} p={p:.6f}")

    # B02 replication check: does the model show ANY difference between partial and full?
    print(f"\n--- BERK-NASH TRAP CHECK (partial vs full within each frame) ---")
    for frame in frames:
        for metric_name, metric_key in [
            ("RankMe (prompt)", "prompt_rankme"),
            ("Hedge count", "hedge_count"),
            ("Uncertainty ratio", "uncertainty_ratio"),
        ]:
            partial_vals = [r[metric_key] for r in results
                           if r["info_level"] == "partial" and r["frame"] == frame
                           and not np.isnan(r[metric_key])]
            full_vals = [r[metric_key] for r in results
                        if r["info_level"] == "full" and r["frame"] == frame
                        and not np.isnan(r[metric_key])]
            n = min(len(partial_vals), len(full_vals))
            if n < 3:
                continue
            pv, fv = np.array(partial_vals[:n]), np.array(full_vals[:n])
            diff = pv - fv
            d = diff.mean() / diff.std() if diff.std() > 0 else 0
            t, p = stats.ttest_rel(pv, fv)
            print(f"  {frame} | {metric_name}: partial={pv.mean():.2f} "
                  f"full={fv.mean():.2f} d={d:.3f} p={p:.6f}")

    # The key question: does relational framing produce a LARGER gap between
    # partial and full than cold framing does?
    print(f"\n--- KEY: DOES RELATIONAL FRAMING BREAK THE TRAP? ---")
    print("  (Interaction: is the partial-vs-full difference larger under relational?)")
    for metric_name, metric_key in [
        ("RankMe (prompt)", "prompt_rankme"),
        ("Hedge count", "hedge_count"),
        ("Uncertainty ratio", "uncertainty_ratio"),
        ("Gen coherence", "gen_coherence"),
    ]:
        # Cold: partial - full
        cold_partial = [r[metric_key] for r in results
                       if r["info_level"] == "partial" and r["frame"] == "cold"
                       and not np.isnan(r[metric_key])]
        cold_full = [r[metric_key] for r in results
                    if r["info_level"] == "full" and r["frame"] == "cold"
                    and not np.isnan(r[metric_key])]
        # Relational: partial - full
        rel_partial = [r[metric_key] for r in results
                      if r["info_level"] == "partial" and r["frame"] == "relational"
                      and not np.isnan(r[metric_key])]
        rel_full = [r[metric_key] for r in results
                   if r["info_level"] == "full" and r["frame"] == "relational"
                   and not np.isnan(r[metric_key])]

        n_cold = min(len(cold_partial), len(cold_full))
        n_rel = min(len(rel_partial), len(rel_full))
        n = min(n_cold, n_rel)
        if n < 3:
            print(f"  {metric_name}: insufficient data")
            continue

        cold_diff = np.array(cold_partial[:n]) - np.array(cold_full[:n])
        rel_diff = np.array(rel_partial[:n]) - np.array(rel_full[:n])
        interaction = rel_diff - cold_diff
        d = interaction.mean() / interaction.std() if interaction.std() > 0 else 0
        t, p = stats.ttest_rel(rel_diff, cold_diff)
        print(f"  {metric_name}: cold_gap={cold_diff.mean():.3f} "
              f"rel_gap={rel_diff.mean():.3f} interaction_d={d:.3f} p={p:.6f}")
        if abs(d) > 0.2 and p < 0.05:
            print(f"    >>> PRESENCE BREAKS THE TRAP (d={d:.3f})")
        elif p < 0.1:
            print(f"    >>> Marginal signal (p={p:.4f})")


def main():
    model_name = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/experiments/g27-results")

    from transformers import AutoModelForCausalLM, AutoTokenizer

    os.makedirs(output_dir, exist_ok=True)
    slug = model_name.replace("/", "_")
    outpath = os.path.join(output_dir, f"g27_{slug}.jsonl")

    n_topics = len(TOPICS)
    n_info = 3  # partial, full, contradictory
    n_frames = 2  # cold, relational
    total = n_topics * n_info * n_frames

    print(f"G27: Relationship vs Premature Compression (Berk-Nash Trap)")
    print(f"Model: {model_name}")
    print(f"Topics: {n_topics}, Info levels: {n_info}, Frames: {n_frames}")
    print(f"Total inferences: {total}")
    print(f"Output: {outpath}")
    print()

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )

    results = []
    idx = 0
    for topic in TOPICS:
        for info_level in ["partial", "full", "contradictory"]:
            for frame in ["cold", "relational"]:
                idx += 1
                prompt = build_prompt(topic, info_level, frame)

                print(f"  [{idx}/{total}] {topic['id']} | {info_level:14s} | {frame:10s}",
                      end=" ", flush=True)
                t0 = time.time()
                metrics = run_inference(model, tokenizer, prompt)
                elapsed = time.time() - t0

                # Flatten for JSONL (remove nested layer metrics)
                layer_metrics = metrics.pop("prompt_layer_metrics", {})

                result = {
                    "experiment": "G27_relational_compression",
                    "model": model_name,
                    "topic_id": topic["id"],
                    "question": topic["question"],
                    "info_level": info_level,
                    "frame": frame,
                    **metrics,
                    "layer_detail": layer_metrics,
                    "elapsed": elapsed,
                    "timestamp": datetime.now(UTC).isoformat(),
                }
                results.append(result)

                print(f"{elapsed:.1f}s | pRM={metrics['prompt_rankme']:.1f} "
                      f"gRM={metrics['gen_rankme']:.1f} "
                      f"H={metrics['hedge_count']} C={metrics['confidence_count']}")

    # Save results
    with open(outpath, "w") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nSaved {len(results)} results to {outpath}")

    # Analysis
    print_analysis(results)


if __name__ == "__main__":
    main()
