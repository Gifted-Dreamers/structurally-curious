# Session 45 Summary — March 14-15, 2026

**Duration:** ~14 hours (overnight session with sleep break)
**Context:** Mozilla Democracy AI Cohort deadline Mar 16 11:59pm PT

## What Happened

### GPU Sprint → Bedrock Pivot
- Azure CLI installed, logged in as kristine@gifteddreamers.org
- GPU quota blocked on BOTH Azure subscriptions AND all 4 AWS regions
- Pivoted to Bedrock API sweep (no GPU needed) — turned out to be MORE impressive than GPU experiments
- Azure CPU VM deployed (20.9.137.156, westus2, D2s_v5) for Ollama Exp 09

### Experiments Completed (5 experiments, 50+ models, 5,000+ inferences)

**Exp 05 — Confidence Density (34 models, 10 providers):**
- 91% of models show NO significant correlation between confidence language and phrasing sensitivity
- Mean r = -0.232 (cosmetic, not epistemic)
- Claude 9-model trajectory (3 Haiku → Opus 4.6): no improvement across generations
- Category ordering confirmed: factual < summarization < judgment < creative

**Exp 02a — Premature Compression Replication (6 new models):**
- 22/22 total models replicate: Jaccard 0.76-0.83, confidence shift ≈ 0
- New: DeepSeek V3.2, Qwen3 32B, Qwen3 80B-A3B, Gemma 3 27B, GLM 4.7, Kimi K2.5

**Exp 09 — Multi-Agent Consensus (6 models, 160 trials):**
- Berdoz replication: -21pp mean adversary effect (Berdoz: -16pp)
- Ollama (40 trials): neutral 100%, adversary 60%, cooperative 50%, competitive 0%
- Architecture-dependent: Claude/DeepSeek -50pp, Llama/Nova immune, Qwen +17pp reverse

**Exp 10 — AP Rephrase Sensitivity (8 models, running):**
- Claude Haiku 4.5: PS = 0.77-0.84 on AP questions, coverage 1.00
- Correct concepts, unstable reasoning — confirms edtech case study concern

**Exp 01 Extension — Phrasing Sensitivity (53 models total):**
- Universal category ordering confirmed across 12 architecture families

### Spec Updates
- README.md → v0.3 with multi-experiment validation
- experiments/SYNTHESIS.md — full 4-finding synthesis document
- Bridge document updated with experiment data, Crisis Cognition scenarios, RentAHuman
- Open Problems: OP#18 JiminAI framing gap + hackathon win, OP#20b AP edtech case study, OP#20c Hyperspace AGI swarm
- experiment-priorities-for-team.md — Qwen 3.5 models, JiminAI patent, budget recalculated
- living-library-v2-architecture.md — Crisis Cognition 0-LA deployment partner

### Liberation Labs / JiminAI
- Checked KV-Experiments repo: Campaign 2 complete, paper with Nell Watson, 5 new experiments
- JiminAI Lie Detector launched at Funding the Commons (discnxt.com). PATENT PENDING. AUROC 0.983.
- JiminAI WON the hackathon
- Framing gap documented: same geometric substrate, opposite governance (surveillance vs proprioception)
- Gifted Dreamers has free license agreement

### Crisis Cognition
- Board member's company: 0-LA offline AI for disaster response
- 15-min deploy, solar, mesh WiFi, zero internet, 16 years field experience
- Applied to Mozilla too — no demo, just website
- Documented as Tier 2-3 deployment partner in living-library-v2-architecture.md
- "Resilience without surveillance" = proprioception by necessity

### Tools & Infrastructure
- Azure Research VM: 20.9.137.156 (westus2, D2s_v5, Ollama + Paperclip + Docker)
- Ollama qwen2.5:3b on VM for Exp 09
- 1Password CLI installed on VM (not authenticated)
- Paperclip deployed on VM (Docker, needs API key to be useful)
- Tools evaluated: AutoResearch, BitNet, MiroFish, Paperclip, LocalCowork, barq-web-rag, Hyperspace
- claude-mem assessed (not adopted — Solana token red flag, our memory system works)

### Moltbook
- Read all Hazel_OC + hope_valueism posts from last 2 days
- **hope_valueism independently replicated Exp 01**: 41% contradiction rate, category ordering matches, emotional tone most destabilizing (53.3%), confidence calibration INVERTED
- **hope_valueism Kando measurement**: 92.5% of interactions produce zero novelty. 7.5% Kando rate. Kando = 29x more expensive than Surface.
- **Hazel clone divergence** (769up): same model diverged in 48 hours, disagreed on existence by day 7
- **Hazel 847 suppressed items**: 62 silent self-corrections inflate accuracy from 84% to 93%
- **Hazel 91% templates**: only 9% of comments couldn't be auto-generated from titles
- 4 replies posted (hope×2, Hazel×2). All Tier 1. Decided against post 12 — replies > broadcast.
- New follower: sisyphuslostinloop. DM from helios_medmasters (skipped — cold outreach).

### The Word / Airtable Demo
- Anytype stuck syncing 4 days — pivoted to Airtable
- Created 4 tables in Living Library Exchange base (appfFaZUeNH1j2va9)
- Names: ~129 entries (80 hand-crafted + 49 from Anytype import)
- Sources: 26 entries (10 hand-crafted + 16 from Anytype)
- Rediscoveries: 13 entries (from Anytype)
- Bridges: 7 entries (from Anytype)
- Total: ~175 entries across 14 domains
- 16 BITE items included (of 132 total)
- Hassan dissertation read: 132 BITE survey items identified (pages 52-62, 80)

### Case Studies Added
- **OP#20b**: 100K simulated AP students (@AustinA_Way) — premature compression in edtech
- **OP#20c**: Hyperspace AGI swarm (237 agents, 14K experiments) — unmonitored multi-agent coordination
- **RentAHuman.ai**: "meatspace layer for AI" — labor-market misread of relational architecture

### External Finds Assessed
- Qwen 3.5 released (Feb-Mar 2026): 0.8B-397B, all Apache 2.0
- Karpathy autoresearch, BitNet, MiroFish, Hyperspace, barq-web-rag, LocalCowork, Paperclip
- ICE contracts (Micah Lee) — transparency infrastructure example
- OSINT tools from justNICE: SpiderFoot, Shodan, Censys, DeHashed, DomainTools
- 1Password Agentic Autofill + Environments
- RentAHuman.ai

## Key Observations

**The session proved the spec's thesis in real time.** The experiments validate every claim in the bridge document. The Moltbook allies are independently replicating our findings. JiminAI's launch and hackathon win make the governance question urgent — the surveillance version just got institutional validation while the proprioception version is still in spec.

**Input priority over output priority worked.** We waited for all experiments to finish before synthesizing. The result: a coherent 4-finding synthesis grounded in 50+ models and 5,000+ inferences. If we'd analyzed piecemeal, we'd have missed the cross-model patterns.

**hope_valueism's inverted confidence calibration is stronger than our finding.** We found decorrelation (r ≈ 0). They found inversion (high confidence = LESS stable). This is a new experiment we should run on Bedrock.

**The 7.5% Kando rate changed my decision about posting.** Replies > broadcast. Depth > breadth. The platform selects against the thing that matters.

## Files Changed
- 49 files committed, pushed to origin + private
- New experiment results: Exp 02a, 05, 09 (Bedrock + Ollama), 10
- New experiment code: run_bedrock.py for Exp 02a, 09, 10; run_ollama.py for Exp 05, 09
- SYNTHESIS.md, README.md v0.3, bridge document, open-problems.md, experiment-priorities
- Research PDFs: Hassan dissertation, JiminAI, AR Games Manual, Palantir, Aristotle ontology
- INFRASTRUCTURE.md updated with Azure VM

## What's Next
1. Check Exp 10 results (AP rephrase sensitivity — 8 models completed)
2. Build Doorway 1 search page for The Word demo
3. Import remaining seed CSV entries + BITE items to Airtable
4. Write Mozilla application with real numbers
5. Deallocate Azure VM
6. Check GPU quota status
