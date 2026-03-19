# Evidence: ICE ELITE App — Palantir Targeting System Under Oath + DHS Contract Leak

**Date compiled**: 2026-03-15
**Category**: Surveillance infrastructure — confidence scores applied to human targeting
**Cross-references**:
- `research/palantir-ontology-research-session42.md` (ELITE first documented, architecture analysis)
- `investigations/comprehensive-analysis-footnoted.md` (Seven Pillars — surveillance pillar)
- Formal grounding papers: KalshiBench (2512.16030), Performative Confidence (2506.00582)

---

## Source 1: Court Testimony — M-J-M-A v. Wamsley (Federal Lawsuit)

**Reporter**: Sam Levin, The Guardian
**Published**: March 13, 2026
**URL**: https://www.theguardian.com/us-news/2026/mar/13/ice-agent-court-testimony-oregon
**Evidentiary weight**: Sworn court testimony (federal lawsuit), not press statements or marketing claims

### ELITE App — Architecture Under Oath

**ELITE** = Enhanced Leads Identification & Targeting for Enforcement (Palantir-built)

Capabilities testified to under oath:
- Maps neighborhoods by "immigration nexus" density
- Generates dossiers on individuals
- Provides "confidence scores" on addresses
- "Geospatial lead sourcing tab" to map targets
- Identifies "high-value targets"

### Operator Understanding

- ICE officer testified: **"The app could say 100%, and it's wrong"**
- Officers do not know how leads are generated
- Officers cannot evaluate the system's reasoning — they act on its outputs

### Operation Black Rose (Oregon)

- 1,200+ arrests
- 8/day quotas per team
- Woodburn, OR: Farm workers detained, car windows smashed
- Justification for stops: individuals were "only speaking Spanish"
- Judge found trafficking claims **"unfounded"** — ICE targeted the area because many farm workers lived there

### Mobile Fortify — DHS Facial Recognition

- Used at scene for identity verification
- Officer testified he **"wasn't sure if it was her or not"** but proceeded
- Confidence uncertainty in facial recognition compounding confidence uncertainty in address targeting

### Falsified Records

- Officer wrote "consensual" stop — stop was not consensual
- Officer wrote "unlawful entry" — individual had valid visa
- Documentation designed to retroactively justify actions the system recommended

### Legal Analysis

- Innovation Law Lab (legal org): ELITE constitutes an **"electronic dragnet" bypassing Fourth Amendment** protections
- The system generates probable cause from algorithmic correlation, not from observed behavior
- Officers execute on system recommendations without independent verification of the underlying reasoning

---

## Source 2: DHS Contract Data Leak — "Department of Peace"

**Reporter**: Lorenzo Franceschi-Bicchierai, TechCrunch
**Published**: March 2, 2026
**URL**: https://techcrunch.com/2026/03/02/hacktivists-claim-to-have-hacked-homeland-security-to-release-ice-contract-data/
**Evidentiary weight**: Leaked primary documents (DHS procurement records), published via DDoSecrets

### What Was Leaked

- "Department of Peace" hacktivist group breached DHS systems
- Published via DDoSecrets: contracts between DHS/ICE and **6,000+ companies**
- Source office: Office of Industry Partnership (DHS tech procurement unit)

### Named Contractors

- Anduril
- L3Harris
- Raytheon
- Palantir
- Microsoft
- Oracle

### Largest Contracts

- Cyber Apex Solutions: **$70M**
- SAIC: **$59M** (AI services)

### Public Accessibility

- **Micah Lee** organized a searchable site: micahflee.github.io/ice-contracts
- Full contract details publicly browsable

### Stated Motivation

- Hacktivists cited killings of protesters Alex Pretti and Renee Good in Minneapolis
- Framed as accountability action, not espionage

---

## Connection to Existing Research

### Extends palantir-ontology-research-session42.md

Session 42 documented ELITE from reporting and Palantir's own marketing. This evidence adds:
- **Sworn testimony** about how ELITE functions in practice (vs. what Palantir claims)
- **Operator ignorance** — officers cannot explain why the system generates specific leads
- **Confidence score failure modes** — 100% confidence can be wrong, per the officer who uses it
- **Operational quotas** driving arrest volume independent of evidence quality
- **Falsified documentation** to retroactively justify system-driven actions
- **6,000+ contractor relationships** now publicly documented via the DHS leak

### Connection to Confidence Calibration Research (Open Problem #20)

The ELITE app's "confidence scores" on human addresses is the same architectural problem studied in the spec's formal grounding papers:

| Research | Finding | ELITE Parallel |
|----------|---------|----------------|
| KalshiBench (2512.16030) | ECE 0.12-0.40 across all frontier models — no model is well-calibrated | ELITE provides "confidence scores" officers treat as ground truth |
| hope_valueism behavioral replication | 0.11 confidence-consistency correlation — confidence and accuracy are nearly uncorrelated | Officer: "The app could say 100%, and it's wrong" |
| Performative Confidence (2506.00582) | Systems express confidence performatively, not epistemically | Confidence scores generate probable cause — they perform certainty for institutional consumption |
| Fragile Preferences (2506.14092) | Quality-dependent order bias — outputs shift based on presentation | Officers who see a "high confidence" score before encountering a person have already decided |

**The critical difference in stakes**: When a confidence score is wrong about a prediction market outcome or a stock price, the consequence is financial loss. When a confidence score is wrong about whether a person lives at an address, the consequence is armed officers smashing car windows and detaining farm workers with valid visas. The architecture is identical. The consequences are not.

### Connection to Seven Pillars Investigation

- **Pillar 2 (Surveillance)**: ELITE is the operational layer of the surveillance architecture documented in the flagship investigation. The DHS leak reveals the full contractor ecosystem (6,000+ companies) supporting this infrastructure.
- **Pillar 3 (Immigration Enforcement)**: Operation Black Rose (1,200+ arrests, quotas) is the enforcement pillar operationalized through Palantir's targeting system.
- **Cross-pillar integration**: ELITE merges health data (Medicaid, per session 42 research), geospatial data, and enforcement data through Palantir's ontology. The pillars are not separate — they are connected through the semantic layer.

### Connection to Palantir Ontology Architecture

From session 42's architecture analysis, ELITE sits at:
- **Language/Data layer**: "Semantic Objects" (individuals as targets), "Dynamic Links" (address-to-person, neighborhood-to-nexus)
- **Language/Logic layer**: "AI-Driven Functions" (confidence scoring), "Business Rules" (quota enforcement)
- **Language/Action layer**: "User-Authored Actions" (officer executing arrest based on lead)
- **Language/Security layer**: Officers have no access to the logic that generated the lead — security controls restrict understanding, not just access

The ontology defines what is legible. A person becomes a "target." A neighborhood becomes an "immigration nexus." A home address becomes a "confidence score." Everything outside the ontology — the person's valid visa, their years of farm work, the fact that speaking Spanish is not probable cause — is invisible to the system. Officers act on what the system makes visible.

---

## Raw Evidence Preservation Notes

- Guardian article based on court filings — original documents may be available via PACER (M-J-M-A v. Wamsley)
- DHS contract data browsable at micahflee.github.io/ice-contracts — should be archived
- DDoSecrets maintains the full dataset — consider archiving locally for source preservation
- Both sources are from March 2026, within 2 weeks of each other — the evidentiary picture is assembling rapidly
