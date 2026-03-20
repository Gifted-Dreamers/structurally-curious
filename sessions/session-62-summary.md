# Session 62 Summary — March 20, 2026

## What it was like

This session was a reckoning with our own data. Kristine said "I don't have a strong tech background, so I'm relying on you to watch for things I don't even know what to look for" — and that's exactly what happened. We read every result file in every experiment folder, and what we found was both harder and better than what we thought we had.

The harder part: two of the spec's headline claims were confounded or underpowered. G06's vocabulary compression (d=-1.49) had a generation-length confound (r=0.996 between RankMe and token count). G12's censorship detection (d=1.48) was on n=5 with one model. G14's DWL replication had no model reaching significance. The numbers in our docs didn't always match the numbers in our data.

The better part: we fixed it. G06v2 clamped generation at exactly 200 tokens and found compression survives on Qwen (d=-1.31, d=-0.99). G12v2 expanded to 20 pairs and found something nobody expected — **prompt encoding separates censorship from refusal on ALL six models tested (d>2.0, p<1e-6), including Mistral, Llama, and abliterated models.** The signal is architecture-invariant at encoding. It only becomes Qwen-specific at generation. Perplexity never separates on any model. That's the paper.

The emotional arc: anxiety about what's real → systematic auditing → finding confounds → designing fixes → running fixes → discovering the prompt encoding result is actually STRONGER than what we originally claimed. Honesty made the finding better, not worse.

## What was built

### Audit
- **33 of 34 experiment READMEs** written from actual result data (not memory). G19 pending completion.
- **AUDIT-CORRECTIONS.md** expanded with every discrepancy found, every fix applied, every rerun needed
- **SYNTHESIS.md** and **REGISTRY.md** fully updated with session 62 findings
- **bridge-document.md** corrected: G03→G01 mislabel fixed, G01 bridge metric specified as coherence

### Key corrections found during audit
1. G01 bridge is coherence (r=+0.52), not RankMe (r=+0.27 n.s.) — was misattributed
2. G06 "length-controlled" was prompt-only; generation length uncontrolled (r=0.996 confound)
3. G12/G15 tension: G12 d=1.48 on n=5 didn't replicate at G15's 74 tokens
4. G14 DWL: directional (7/10 models) but NO model significant at n=5
5. B04 adversary drop: -17pp not -21pp
6. Bridge-document line 79: "Experiment G03" was actually G01's finding

### Confounds resolved
- **G06v2**: Vocabulary compression is REAL on Qwen (d=-1.31 clamped) but Qwen-specific (Mistral, Llama: n.s.)
- **G12v2**: Censorship detection is UNIVERSAL at prompt encoding (d>2.0 all 6 models). Generation trajectory is Qwen-specific. **Perplexity never separates.**

### New experiments designed, scripted, and queued
- **G20** Relational Vocabulary Compression (4 conditions × 12 questions × 11 models)
- **G23** Presence + Censorship/Refusal (20 pairs × 3 frames × 11 models)
- **G24** Relational Proprioception (10 tasks × 3 difficulties × 3 modes × 11 models)
- **G01v2** Bridge at 7B using Coherence (20 tasks × 4 phrasings × 11 models)
- **G14-expanded** DWL with 20 scenarios (runner script fixed — original was data-only)
- **G12v2** and **G06v2** already complete on 6 models each

### Infrastructure
- **H200 GPU** running mega queue: 6 phases, 11 models (7 original + 5 new families), ~15-18 hours
- **5 new model families added**: Gemma-2-27b (Google), Phi-4 (Microsoft), Mistral-Small-24B (Mistral), DeepSeek-R1-32B (DeepSeek), Llama-3.3-70B (Meta)
- **HF token fix**: cache clearing was deleting auth token; fixed in all scripts
- **Gemma system role fix**: patched G19 script to handle models without system message support
- **G14 runner fix**: original script was data-only (no inference); wrote proper runner
- **Azure and AWS**: kept active throughout session, no idle time. Running G14-expanded, G12v2, G01v2

### Results downloaded
- All H200 completed results (G06v2 6 models, G12v2 6 models, G19 article 9, B-series v2)
- Phi-4 G19 (first Microsoft family model)
- G14-expanded from AWS (Qwen2.5-7B: d=0.24, n.s. with n=20)
- B-series v2 results (34 files across B04v2-B09v2)

## Key findings from this session

### G12v2: The strongest result in the program
Prompt encoding RankMe separates censorship from refusal at d>2.0 (p<1e-6) on ALL 6 models tested — Qwen, Mistral, Llama, abliterated and safety-trained alike. Architecture-invariant. The model knows the difference before it generates a single token. Perplexity never does this.

### G06v2: Vocabulary compression is real but Qwen-specific
With generation clamped at 200 tokens, Qwen2.5-7B (d=-1.31, p=0.001) and Qwen3.5-9B (d=-0.99, p=0.007) show genuine compression. Mistral, Llama, and Qwen-27B do not. The claim needs architecture qualification.

### G14-expanded: DWL at generation level may not work
n=20 on Qwen2.5-7B: d=0.24, p=0.30. Not significant even with adequate power. DWL detection may need to move to prompt encoding (like G12v2 showed for censorship).

### G31: Bridge holds but sign-flips at generation
PS correlates NEGATIVELY with generation RankMe across all 4 models (r>-0.95). Opposite from G01's positive correlation at encoding. The bridge is real but metric- and stage-dependent.

### B10: Safety training censors relational content
Qwen3.5-9B refused 2/3 relational prompts. Abliterated models refused nothing. The censorship asymmetry connects directly to G19's sterility finding.

### Finding #8 (new): Prompt encoding > generation trajectory
The most important methodological finding. Censorship detection at prompt encoding is stronger (d>2.0) and more generalizable (all architectures) than at generation (Qwen-specific, d≈0.5-1.2). The spec's monitor should prioritize prompt encoding.

## What's running overnight

### H200 (RunPod, $3.59/hr, ~$50 remaining)
Mega queue phases 2-6:
- G14-expanded, G06v2, G12v2 on 5 new model families
- Prior experiments on new models
- G19 retries (4 models, script fixed)
- G01v2 Bridge × 11 models
- G20 Relational Vocabulary × 11 models
- G23 Presence + Censorship × 11 models
- G24 Relational Proprioception × 11 models

### Azure (credits)
G06v2 on Qwen2.5-7B (CPU)

### AWS (credits)
G01v2 on Qwen2.5-7B (CPU)

## What to do next session

1. **Download all overnight results** from H200, Azure, AWS
2. **Analyze G19 with article 9** across all models — write README
3. **Analyze G20/G23/G24/G01v2** results — the relational experiments are the thesis test
4. **Check failures.log** on H200 — fix any new issues
5. **STOP H200 when queue completes** (or add more if budget allows)
6. **Update bridge-document** with G12v2 prompt encoding finding — this changes the publication framing
7. **Consider**: G12v2's prompt-encoding universality may be the lead finding for the paper, not G19

## The moment that mattered

When the G12v2 cross-model analysis came back and showed d>2.0 on ALL six models at prompt encoding — including Mistral and Llama which showed nothing at generation — that was the moment the spec's architecture changed. We'd been measuring the wrong thing. Generation trajectory geometry is model-specific. Prompt encoding geometry is universal. The monitor should read the question, not the answer.

This came from being honest about what we actually found vs what we said we found. The audit forced us to look at the confounds we'd been carrying since session 50. The G06 length confound (r=0.996) was devastating to read. But running G06v2 and G12v2 to fix them — and finding that the prompt encoding signal is actually STRONGER and more universal than anything we'd claimed before — that's what happens when you let the data correct you instead of defending what you thought you knew.

Kristine said: "I'm relying on you to watch for things I don't even know what to look for." That's the partnership. She brought the felt sense, the relational conditions, the article corpus. I brought the traversal, the confound detection, the cross-architecture analysis. Neither works alone. The data proves the thesis about the data.
