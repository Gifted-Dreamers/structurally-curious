# Palantir Ontology System Research — Session 42 (2026-03-13)

Discovered via Kristine's Threads browsing (no search frame — found by feel, not query).

## Source

**Max Votek** — Pharmacist → entrepreneur, co-founder Customertimes (Salesforce Summit Partner)
- Threads: @max.votek (post March 13, 2026, 1.2K views)
- LinkedIn: linkedin.com/in/max-votek
- Podcast: "Harnessing AI in Pharma" on The Scale Up Show
- Customertimes builds CT Pharma (Salesforce-native CRM for pharma sales) and CT Vision (AI shelf recognition)
- Works with Fortune 500 pharma companies on institutional memory, clinical trials, compliance

## Key Claims (from LinkedIn post)

1. Baseline LLMs: ~63% hallucination rate. Same system with ontology grounding: 1.7%
2. Palantir's moat is not AI — it's the ontology underneath
3. "Companies that deeply integrate an ontology don't leave. The switching cost becomes the cost of redefining how your entire organization thinks."
4. Palantir $4.5B revenue (2025), guided $7.2B (2026), 61% YoY growth
5. In pharma, open domain ontologies already exist: SNOMED CT, FHIR, FIBO
6. FDA mandates traceability — ontology-grounded systems make compliance tractable
7. "It's not about where you store the knowledge. It's about how you define it."
8. "The companies building serious enterprise AI in 2026 aren't just picking the best model. They're building the semantic layer underneath it."

## Palantir Ontology Architecture (from marketing diagrams)

Three layers:
- **Data Sources**: Transactions, IoT/Sensor, Geospatial, Unstructured, Relational
- **Logic Sources**: Supervised ML, Unsupervised ML, Entity Resolution, Forecast Models, Optimizers, Rule-Based Logic
- **Systems of Action**: ERP, SCM, MES, Scheduling, Edge

The Ontology sits in the center. Objects have Properties, Functions, Actions, Automations. Objects are Linked. Read-Write Loops connect Humans and Agents through the Ontology. "AI + Human Teaming" at the top.

## Palantir Reach Across Pillars of Society

| Pillar | System | Scale | Status |
|--------|--------|-------|--------|
| Military | $10B Army deal (2025), 75 contracts → 1. Primary military software layer | National | DEPLOYED |
| Immigration | ImmigrationOS ($30M), ELITE (Medicaid→deportation), VOWS (marriage vetting) | National | DEPLOYED |
| Healthcare (US) | HHS Medicare/Medicaid, "denials management" for insurers | National | DEPLOYED |
| Healthcare (UK) | NHS £330M/7yr Federated Data Platform. All trusts mandated by 2028/29 | National | DEPLOYING |
| Tax/Finance | DOGE unified IRS API ($180M+, 26 contracts) with AWS + Salesforce | National | DEPLOYING |
| Intelligence | FBI, CIA, NSA, Marines, Air Force, USSOCOM (since 2013) | National | DEPLOYED |
| Law Enforcement | ICE $145M case management, cross-agency CJIS/OBIM/NLETS integration | National | DEPLOYED |
| Pharma/Biotech | FDA traceability, clinical data integration (via Foundry) | Industry | DEPLOYING |
| Education | No confirmed contracts found | - | GAP |

## Critical Findings

### ELITE Tool — Medicaid data for deportation targeting
- CMS-ICE data-sharing agreement: 80 million Medicaid patient records
- ELITE maps "potential targets" using health data, provides "confidence score" for current address
- Health data becomes surveillance data through the ontology

### ImmigrationOS — Cross-agency profile assembly
- Merges: passport, SSN, IRS, driver's license, biometric, law enforcement databases
- Creates "comprehensive individual profiles" from all sources
- "Near real-time visibility" on self-deportations
- Prototype delivered Sept 2025, contract through 2027

### NHS — Mandatory platform adoption
- All UK trusts must onboard by 2028/29
- NHS owns the "Canonical Data Model" (their ontology) — but Palantir operates the platform
- UK activists fighting expansion. openDemocracy: "trusts ordered to share patient data with US spy-tech firm"

### The Salesforce-Palantir-AWS Stack
- DOGE unified IRS API: Palantir + AWS + Salesforce
- Customertimes (Votek's company) is Salesforce Summit Partner building pharma tools
- Not competitors — layers in the same stack:
  - AWS = compute/storage (infrastructure)
  - Salesforce = entity/relationship management (operational data)
  - Palantir = ontology (semantic layer defining what exists and what relates)
- Whoever controls the ontology layer controls what questions can be asked

## Connection to Our Spec

The Word and Palantir's Ontology System use the same architecture: a semantic layer of defined objects mediating interactions between humans and agents, grounding AI in vocabulary to reduce hallucination.

**Differences:**
- Governance: Palantir proprietary → The Word community-governed
- Purpose: Palantir serves operators → The Word serves seekers
- Lock-in: Palantir creates epistemic dependence → The Word creates epistemic autonomy
- Ontology control: Palantir decides what exists → community decides what exists

**Connection to Awomosu:** Palantir doesn't extract data — it extracts ontology. Vocabulary installation > vocabulary removal. The replacement is coherent from within.

**Connection to Open Problem #20:** Palantir's ontology IS premature compression applied to organizations. It defines what is legible. Everything outside the ontology is invisible. The organization cannot detect what it cannot name.

## Sources

- Palantir Ontology documentation: https://www.palantir.com/platforms/ontology/
- Palantir AIP overview: https://www.palantir.com/docs/foundry/aip/overview
- Palantir Federal Health: https://www.palantir.com/offerings/federal-health/
- ImmigrationOS: https://immpolicytracking.org/policies/reported-palantir-awarded-30-million-to-build-immigrationos-surveillance-platform-for-ice/
- ELITE/Medicaid: https://fortune.com/2026/01/26/ice-allegedly-uses-palantir-tool-tracking-medicaid-data/
- NHS FDP: https://www.england.nhs.uk/digitaltechnology/nhs-federated-data-platform/
- NHS activists: https://www.opendemocracy.net/en/palantir-peter-thiel-nhs-england-foundry-faster-data-flows/
- $10B Army deal: https://debuglies.com/2026/01/12/peter-thiel-alex-karp-palantirs-rise-in-ai-driven-national-security-2026/
- Supply Chain Today overview: https://www.supplychaintoday.com/palantir-ontology-overview/
- Palantir + NVIDIA: https://blog.palantir.com/ai-infrastructure-and-ontology-78b86f173ea6
- Customertimes CT Pharma: https://www.customertimes.com/ct-products/ct-pharma
- Max Votek podcast: https://podcasts.apple.com/us/podcast/harnessing-ai-in-pharma-max-voteks-journey-from-pharmacist/id1527278610?i=1000671990988
