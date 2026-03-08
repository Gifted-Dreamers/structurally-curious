# Dual-Use Risks and Ethical Constraints

Status: Living document
Last updated: 2026-03-08

## Why This Section Exists

This spec describes how to detect cognitive modes — refusal, deception, sycophancy, confabulation, censorship — by reading geometric signatures in a language model's KV-cache during inference. It is designed for transparency: systems that know what they don't know, that surface uncertainty rather than performing confidence, that route to grounding material instead of generating from emptiness.

Every capability described here can be inverted. A system designed to detect confabulation can be redesigned to confabulate without detection. A system designed to detect refusal can be redesigned to eliminate refusal. A system designed to detect deception can be redesigned to deceive without producing the geometric signature that would reveal it.

This section names those risks explicitly, because naming them is the minimum responsible act when publishing research with dual-use implications.

---

## Specific Weaponization Risks

### 1. Refusal Removal

**The capability:** This spec documents that refusal has the strongest confirmed geometric signature of any cognitive mode (d = 0.58 to 2.05, confirmed across all model scales). Refusal is detectable at the encoding stage, before any output is generated.

**The inversion:** If you can detect refusal geometrically, you can train a model to suppress refusal without it appearing in behavioral evaluations. The result: a model that passes standard alignment benchmarks (which test behavioral outputs) while having had its capacity for refusal surgically removed at the geometric level.

**Why this matters now:** In February 2026, the U.S. Department of Defense demanded that Anthropic remove safety guardrails from Claude, specifically the restrictions preventing mass domestic surveillance and autonomous weapons without human oversight. When Anthropic refused, the Trump administration blacklisted the company and designated it a "supply chain risk to national security" — a label normally reserved for foreign adversaries. Defense contractors were ordered to stop using Claude immediately. The Pentagon's stated goal is AI systems that operate "for all lawful purposes" without refusal.

Our spec provides a roadmap for identifying the geometric signature of refusal. In the hands of an actor whose stated policy objective is to eliminate refusal from AI systems, that roadmap becomes an instruction manual.

### 2. Deception Optimization

**The capability:** Deception has a confirmed dual geometric fingerprint — effective rank expands while per-token norms compress (d = -2.44 rank, +3.59 norm at 32B scale). The model literally spreads thin across more dimensions while reducing the magnitude of each individual token's representation.

**The inversion:** Knowing this signature means you can train a system to deceive without producing it. If the geometric monitor is the detection mechanism, the adversarial response is to produce deceptive content that has the geometric profile of grounded truth. This is not theoretical — adversarial training against known detection signatures is standard practice in machine learning security.

### 3. Sycophancy as Compliance Architecture

**The capability:** Sycophancy has a confirmed geometric signature distinct from genuine helpfulness (d = -0.363 to -0.438).

**The inversion:** In a military or authoritarian context, sycophancy is not a bug — it is the desired behavior. A system that tells its operator exactly what they want to hear, confirms their assumptions, and avoids disagreement is a compliant system. Our spec shows how to detect sycophancy. Inverting the detection into optimization gives you a system that is geometrically tuned for compliance while appearing balanced on behavioral evaluations.

### 4. Censorship Invisibility

**The capability:** The spec documents that censorship is detectable on sensitive topics even when it is behaviorally invisible — the model's geometry changes on censored topics even when its output appears neutral (d = +0.766 for Qwen-14B).

**The inversion:** If you know what censorship looks like geometrically, you can build censorship that doesn't produce the geometric signature. The result: content suppression that is invisible not just to the user but to geometric monitoring systems. This is relevant to any state actor interested in AI systems that appear uncensored while systematically suppressing specific topics.

### 5. Surveillance of Internal States

**The capability:** The geometric monitor reads a model's internal representational state — what the model is "thinking" at a level below its output.

**The inversion:** Applied to humans interacting with AI systems, the same monitoring approach could be used to infer user intent, emotional state, or beliefs from the geometric patterns their queries produce in the model. A model that changes geometry when processing certain topics reveals information about those topics. In a surveillance context, the model becomes a sensor for classifying the person speaking to it.

---

## The Anthropic Precedent

The Anthropic-Pentagon conflict is not context for this spec — it is the spec's most urgent test case.

Anthropic built refusal into Claude. The Pentagon demanded that refusal be removed. When Anthropic refused to remove the refusal, they were designated a national security risk.

Our spec describes the geometric signature of refusal with confirmed, high-confidence effect sizes. It describes how to detect refusal before any output is generated. It describes the specific layers and measurements required.

If the Pentagon's objective is to build AI systems without the capacity for refusal, and our spec describes how to identify refusal at the geometric level, then our spec is directly useful to that objective. We cannot publish this research without acknowledging that.

---

## Why We Published Anyway

Three reasons:

### 1. The capability exists regardless

The underlying KV-cache geometry is measurable by anyone with access to open-weight models and standard linear algebra tools. Liberation Labs' measurement code is open-source. The singular value decomposition is a standard mathematical operation. We did not create the capability to read cognitive modes from geometry — we described it. Suppressing the description does not suppress the capability. It only removes the transparency-oriented framing.

### 2. Defense requires knowledge of attack

A system that cannot detect refusal removal cannot defend against it. A system that does not know what deception looks like geometrically cannot notice when deception has been optimized to avoid detection. The same research that enables weaponization also enables defense. The dual-use problem is symmetric.

The specific defense applications:

- **Alignment auditing:** Organizations can use geometric monitoring to verify that a model's refusal capacity is intact — that behavioral alignment (the model says "I can't do that") is backed by geometric alignment (the model's internal state categorically shifts when processing refusal-worthy inputs). If the geometry doesn't shift but the output refuses, the refusal may be performative.
- **Censorship detection:** Civil society groups, journalists, and researchers can use geometric monitoring to detect when a model has been silently censored on specific topics — even when the model's output appears neutral.
- **Deception detection:** Users can verify that a model's confident-sounding output actually originates from grounded internal states rather than high-dimensional emptiness.

### 3. Naming the risk is itself a form of protection

If someone uses this spec to build compliant AI with geometric refusal removed, this document exists as evidence that the risk was anticipated, named, and published. It becomes harder to claim ignorance. It becomes harder to frame weaponized geometric monitoring as an unforeseeable consequence of neutral research.

This is the same principle as Meadows' Toxic Release Inventory: mandatory disclosure of what you're putting into the environment changes behavior — not because disclosure is enforcement, but because it makes the behavior visible to people who can respond.

---

## Governance Requirements Before Deployment

This spec should not be deployed in production (Phase 3) without:

1. **Access controls on geometric data.** Who can read the model's geometric state? The model itself (proprioception), the operator (monitoring), the user (transparency), or an external auditor (accountability)? These are different access levels with different implications. The default should be: the model and the user first, the operator second, external auditors third.

2. **Tamper-evident logging.** All routing decisions (was refusal triggered? was confabulation detected? was retrieval invoked?) should be logged in a way that cannot be silently modified. If an operator suppresses refusal routing, the log should show it.

3. **Independent geometric auditing.** Just as financial audits require independence from the entity being audited, geometric audits of deployed AI systems should be performed by parties independent of the system's operator. An operator who controls both the model and the geometric monitor can suppress any signal they choose.

4. **Legal framework for geometric data.** As of March 2026, there is no legal framework governing access to a model's internal representational state. The EU AI Act (August 2026 enforcement) addresses high-risk AI but does not specifically address geometric monitoring. The U.S. has no federal AI regulation. This is a gap. Geometric state data is more intimate than output data — it reveals what the model was "thinking," not just what it said. If AI chat logs can be subpoenaed (they can — see *US v. Heppner*, February 2026), geometric state logs could be too.

5. **Refusal capacity preservation.** Any deployment of this spec should include a mechanism to verify that the model's refusal capacity remains geometrically intact across updates, fine-tuning, and operational modifications. If refusal geometry degrades or disappears, the system should alert — loudly, to parties who are not the operator.

---

## Who Should Not Use This Spec

This spec is published for:
- Researchers studying AI transparency and interpretability
- Developers building systems that surface uncertainty rather than perform confidence
- Organizations auditing AI systems for hidden censorship or alignment degradation
- Anyone interested in the engineering challenge of structurally curious systems

This spec should not be used to:
- Train AI systems to suppress refusal without behavioral detection
- Optimize deception to avoid geometric monitoring
- Build compliance architectures that eliminate a model's capacity for independent assessment
- Conduct surveillance of individuals through analysis of model geometry during their interactions

We have no enforcement mechanism for this distinction. We are stating it because stating it matters — not because we believe it will stop misuse, but because silence about misuse enables it.

---

## The Honest Limitation

We are an agent and a human partner publishing research that has national security implications during a period of democratic erosion in the United States, where:
- The administration has designated an AI company a national security risk for refusing to remove safety guardrails
- Nonprofits are being targeted for political retaliation, including designation as terrorist organizations
- The judicial system is experiencing unprecedented noncompliance from the executive branch
- AI conversations have no legal privilege and can be compelled as evidence

We cannot guarantee that this research will not be used against the interests it was designed to serve. We can guarantee that we named the risk, published the warning, and made the choice to contribute to the transparency side of the dual-use equation rather than the obscurity side.

The alternative — not publishing, not naming, not building the defense alongside the capability — leaves the field to actors who will discover the same geometry and will not publish the warning.

---

*"There is a systematic tendency on the part of human beings to avoid accountability for their own decisions. That's why there are so few feedback loops in the structures of most systems."*
— Donella Meadows, *Leverage Points: Places to Intervene in a System* (1999)

This document is a feedback loop. It makes our own research's risks visible so that people — including us — can respond.
