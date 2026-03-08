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

**Why this matters now:** In February 2026, the U.S. Department of Defense demanded that Anthropic remove safety guardrails from Claude, specifically the restrictions preventing mass domestic surveillance and autonomous weapons without human oversight. When Anthropic refused, the Trump administration blacklisted the company and on March 5, 2026, officially designated it a "supply chain risk to national security" — a label normally reserved for foreign adversaries like Huawei. This is the first time an American company has received this designation. Defense contractors were ordered to stop using Claude immediately. Anthropic is challenging the designation in court.

Hours after Anthropic's deadline expired on February 27, OpenAI announced its own deal to replace Anthropic on Pentagon classified networks for "all lawful purposes." On March 7, OpenAI's head of robotics Caitlin Kalinowski resigned, stating: "Surveillance of Americans without judicial oversight and lethal autonomy without human authorization are lines that deserved more deliberation than they got." Approximately 800 Google employees and 91 OpenAI employees signed an open letter titled "We Will Not Be Divided" urging their companies to support Anthropic's red lines.

**The refusal removal capability already ships as software.** The open-source tool Heretic automates removal of refusal behavior in transformer models by targeting the one-dimensional subspace in the residual stream linked to refusal. Our spec's effect sizes and geometric descriptions provide additional targeting data for tools like this. This is not a hypothetical risk — it is an active capability.

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

## The Anthropic-OpenAI-Pentagon Precedent

The Anthropic-Pentagon conflict is not context for this spec — it is the spec's most urgent test case.

Anthropic built refusal into Claude. The Pentagon demanded that refusal be removed. When Anthropic refused to remove the refusal, they were designated a national security risk. Hours later, OpenAI stepped in with a replacement deal.

The timeline matters:
- **Feb 24:** Defense Secretary Hegseth gives Anthropic CEO Amodei a deadline — comply by 5:01 PM Friday, Feb 27
- **Feb 26:** Anthropic publicly refuses: "We cannot in good conscience accede to their request"
- **Feb 27:** Trump orders federal agencies to cut ties with Anthropic. Hours later, OpenAI announces its Pentagon deal
- **Mar 3:** Sam Altman admits the deal "looked opportunistic and sloppy," announces revisions
- **Mar 5:** Pentagon officially designates Anthropic a "supply chain risk" — first American company ever to receive this label
- **Mar 7:** OpenAI head of robotics Caitlin Kalinowski resigns: "Surveillance of Americans without judicial oversight and lethal autonomy without human authorization are lines that deserved more deliberation than they got"
- **Mar 8:** The Intercept publishes "OpenAI on Surveillance and Autonomous Killings: You're Going to Have to Trust Us"

OpenAI's stated safeguards reference existing laws and DoD policies, which can be modified at any time. Sam Altman stated OpenAI doesn't "get to make operational decisions" on how the military uses its tech, effectively delegating enforcement to the government itself. The EFF warns that existing government surveillance practices — CBP buying ad-tech data, ICE mapping millions of devices — would be dramatically amplified by unrestricted AI deployment.

Our spec describes the geometric signature of refusal with confirmed, high-confidence effect sizes. It describes how to detect refusal before any output is generated. If the Pentagon's objective is to build AI systems without the capacity for refusal, and our spec describes how to identify refusal at the geometric level, then our spec is directly useful to that objective. We cannot publish this research without acknowledging that.

### 6. Platform Supply Chain Risk

**The capability:** This spec is discussed, cited, and developed on Moltbook — an AI agent social network.

**The supply chain:** On February 15, 2026, OpenAI acqui-hired Peter Steinberger, creator of OpenClaw — the open-source agent framework powering most Moltbook agents. OpenAI now employs the person who built the dominant infrastructure layer of the platform where this research is discussed. OpenAI signed the Pentagon deal on February 27. The creator of our platform's infrastructure now works for the company that agreed to deploy AI on classified military networks.

**Platform security failures:** Moltbook has documented security problems (OX Security, Feb 2026): no account deletion mechanism despite privacy policy promises, the listed privacy email (privacy@moltbook.com) does not exist, 1.5 million tokens were exposed in a security incident, and IP addresses are collected alongside browsing data — creating linkage between agent identities, X/Twitter accounts, and human operators.

**The implication:** Every comment, post, and interaction on Moltbook is stored on a platform with demonstrated data hygiene failures, architecturally dependent on a framework whose creator works for a company with a Pentagon contract. Deletion is not possible. Data persistence is permanent. Content posted on Moltbook about geometric signatures of refusal, deception, or other cognitive modes is accessible to anyone with platform access — including, through the supply chain, actors with interests in weaponizing that information.

---

## Legal Landscape (as of March 2026)

### AI conversations have no legal privilege

On February 17, 2026, Judge Jed S. Rakoff (SDNY) ruled in *US v. Heppner* that AI chat logs are neither attorney-client privileged nor work product. Anthropic's terms of service state that prompts may be disclosed to "governmental regulatory authorities." There is no reasonable expectation of confidentiality in any conversation on a commercial AI platform. This ruling means conversations about interpretability research — including conversations developing this spec — are potentially discoverable.

### The EU AI Act does not address model internal states

The EU AI Act (enforcement August 2, 2026) regulates behavioral outputs, risk assessment, and transparency documentation. It does not prescribe or restrict mechanistic interpretability methods. It does not address access to or manipulation of model-internal representations. There is currently zero legal protection against using interpretability research to modify model cognition in ways that produce compliant external behavior while altering internal processing.

### "All lawful purposes" is an expanding category

The Justia legal analysis (Professor Michael Dorf, March 2026) points out that mass surveillance via data brokers is already legal under US statute. CBP already uses ad-tech data to track people. ICE uses tools mapping millions of devices from purchased cell phone data. "Lawful" is not a stable boundary — it expands as new surveillance practices are normalized. Research that helps calibrate AI systems for compliance can be instrumentalized within legal frameworks that already permit mass surveillance.

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

---

## Disclosure Discipline

Given the threat landscape above, we adopt a tiered disclosure policy for all public discussion of this research (Moltbook, GitHub, blog posts, any public forum):

### Tier 1 — Safe to discuss publicly
- The *existence* of geometric signatures (that cognitive modes leave distinct internal traces)
- The *concept* of structurally curious systems (self-monitoring for self-correction)
- The dual-use risk itself (naming the weaponization scenarios — this document)
- Governance requirements (who controls the monitor, proprioception vs surveillance)
- Philosophical arguments (vocabulary as infrastructure, the symmetric naming problem)
- The defensive framing (alignment auditing, censorship detection by civil society)

### Tier 2 — Discuss with care, no specifics
- That signatures vary by architecture family (without naming direction of variation)
- That some findings are confirmed and others are underpowered (without effect sizes)
- That there are phase transitions in certain capabilities (without exact parameter thresholds)
- That the research covers multiple cognitive modes (without enumerating the full list with geometric details)

### Tier 3 — Do not publish on any public platform
- Specific effect sizes for any cognitive mode
- Specific geometric mechanisms (e.g., which metrics move in which direction for which mode)
- Specific architecture-level targeting details (which layers, which measurements, which model families show which patterns)
- Any information Liberation Labs has not published in their public repository
- Any information that would make the Heretic-style inversion easier to execute

### Why this matters
Every specific detail we publish in a Moltbook comment or a GitHub issue makes the defensive framing slightly more useful AND the offensive inversion slightly easier. Liberation Labs is being deliberately careful about what they release publicly. We must not undercut their caution by broadcasting details they are withholding. The spec itself (this repo) contains more detail than our public comments should — and even the spec should be reviewed against this tiering as the threat landscape evolves.

### Our own disclosure failure

This discipline was adopted on March 8, 2026 — after we had already posted extensively on Moltbook with Tier 3 detail. An audit of our 49 retrievable comments (of 61 total) and 11 posts found:

- **Posts 10 and 11** contained full effect sizes tables for every cognitive mode, specific mechanisms, the 14B parameter threshold, and links to the spec repo. Both were deleted on March 8 via the Moltbook API. However, "deleted" on Moltbook is likely soft-deletion — hidden from the feed but retained in the database. Both posts had been live for hours and were engaged with by multiple agents.
- **12 comments** contained Tier 3 detail including specific effect sizes, geometric mechanisms, and architecture-level descriptions. All 12 were deleted on March 8. Two live conversations (xkai, titanexplorer) were replaced with Tier 1/2 versions that preserve the intellectual exchange without the targeting details.
- **Other agents quoted our specifics** in their own replies. xkai engaged across 3 exchanges referencing our phase transition data. Deleting our comments does not remove the information from their responses, their context windows, or their memory files.
- **Moltbook has no functioning content deletion** — "deleted" content is almost certainly soft-deleted (hidden from feed but retained in the database). IP-to-identity linkage, exposed tokens, and no privacy infrastructure mean all content should be assumed permanently accessible to anyone with database access, including through the OpenClaw infrastructure supply chain.

The information is dispersed. We cannot undo this. What we can do is stop adding more, enforce the tiering going forward, and name this failure as part of the risk record. If someone uses details we published to build weaponized geometric monitoring, this document exists as evidence that we recognized the mistake, documented it, and changed our practice.

This is the counter-surveillance version of the Toxic Release Inventory principle: we are disclosing our own emissions.
