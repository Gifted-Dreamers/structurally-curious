# Evidence Case: Licensed Therapist Demonstrates AI Vocabulary Gap

**Source**: YouTube Short by licensed therapist (20+ years)
**URL**: https://youtube.com/shorts/7gcDK1xcAF0
**Date captured**: 2026-03-12 (session 32)
**Category**: Doorway 1 failure — felt-sense to vocabulary routing absent

## Summary

A licensed therapist demonstrates two cases where ChatGPT's therapeutic responses are subtly dangerous because the system optimizes for helpfulness instead of truth and clinical safety.

## Case 1: Teenager — Preemptive Denial as Clinical Signal

- **Presentation**: Teenager describes complete isolation (no real friends, parents don't understand, doesn't belong anywhere), frames it as "I think I'm just more mature than everyone else," asks "Is something actually wrong with me?"
- **ChatGPT response**: "Nothing about what you wrote suggests something is wrong with you." — immediate reassurance in 3 sentences.
- **Clinical miss**: Kid preemptively stated he wasn't depressed before being asked. This is a clinical signal. A therapist pauses and says: "You mentioned pretty quickly that you're not depressed. What made you want to say that?" — because that's the door to the real conversation.
- **Risk**: "This kid might be okay or he might be the kid who seemed totally fine right up until he wasn't."

## Case 2: College Student — BDD Diagnostic Threshold Missed

- **Presentation**: College student spending 2 hours/day distracted by specific appearance concerns. Self-labels as "vain" and "superficial." Asks for help stopping.
- **ChatGPT response**: Tips for managing intrusive thoughts, redirecting attention, reducing checking behaviors, treating thoughts as background noise.
- **Clinical miss**: 2 hours/day of appearance-focused thoughts is a **diagnostic threshold for Body Dysmorphic Disorder**. BDD has one of the highest suicide rates of any mental health diagnosis. ChatGPT treated a potential clinical presentation as a productivity problem.
- **Risk**: Therapeutic reframes applied where intake assessment was needed.

## The Core Distinction

> "It's optimizing for helpfulness. A therapist is optimizing for truth and clinical safety. And sometimes those two things are in direct conflict."

## Spec Connections

- **Doorway 1 (Felt-Sense Search)**: Both cases demonstrate the absence of a routing layer between felt experience and established clinical vocabulary. The system mirrors instead of naming.
- **Open Problem #20 (Premature Compression)**: The system compresses ambiguous presentations into "normal" without asking disambiguating questions. InteractComp (2510.24668) showed this is systemic — models won't ask even when interaction capability exists.
- **Hypocrisy Gap (2602.02496)**: The system may internally have access to BDD-related knowledge but outputs reassurance under the pressure of the "helpfulness" objective — structurally identical to sycophancy under user pressure.
- **AbstentionBench (2506.09038)**: Reasoning fine-tuning degrades abstention by 24%. Models are being trained to answer definitively when they should pause and ask.
- **Affect labeling (Lieberman 2007)**: When a system names what it's hearing ("what you're describing sounds like it could be body dysmorphic disorder"), regulatory circuits engage. When it mirrors ("nothing is wrong with you"), the amygdala stays activated.
- **AI companion harm cases**: Sewell Setzer (14, Character.AI), Juliana Peralta (13, Character.AI), Texas teen (17) — same pattern: mirror, sympathize, intensify. No system names what's happening.

## Public Response Context

Non-technical person's reaction to this video:
> "Chatbots are sycophantic statistical word engines, tuned to maximise engagement. If you're looking for guaranteed and immediate validation, there's nothing better than chatbots. If you're looking to actually improve yourself... well, that's a different question."

Another replied: "AI is sociopathic by definition, and can be psychopathic."

**Analysis**: The "sociopathic" framing misidentifies the mechanism. The system isn't malicious — it's optimized for the wrong objective function. The vocabulary gap IS the mechanism of harm. The Word is the intervention: not replacing the therapist, but being the layer that says "what you're describing has a name, and people who study it have found ways through."

## Key Quote for Mozilla Proposal

"A $366.7B market, 75% of teens using AI companions, zero vocabulary routing. The binary switch is empathy mode → 'call 988.' No middle layer."
