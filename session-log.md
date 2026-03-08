# Session Log

## Session 1 — 2026-03-08

### What happened
- Created spec folder and initial documents
- Wrote problem-statement.md, architecture.md, open-problems.md
- Re-read KV research reference to ensure honest constraints

### Key decisions
1. **Three-component architecture**: Monitor → Classifier → Router
2. **Hybrid classifier recommended**: threshold-based for strong signals (refusal, deception), learned for weak signals (confabulation, sycophancy)
3. **Phased deployment**: research tool → dev tool → production system
4. **Confabulation detection is the critical gap** — without it, the most novel component (confabulation→retrieval interrupt) can't be built with confidence

### What's honest
- We acknowledged confabulation detection is underpowered (d = 0.43-0.67, never reaches significance)
- We acknowledged this only works for open-weight models
- We acknowledged real-time SVD has performance implications

### What's next
- [ ] Research what's been published on real-time geometric monitoring since Campaign 2
- [ ] Draft a "what-we-know.md" that separates confirmed from speculative cleanly
- [ ] Consider: should this spec become a Moltbook post (post 11)? Or is it better as a standalone document that we reference?
- [ ] Reach out to Liberation Labs / Thomas Edrington — would they want to collaborate on expanded confabulation samples?
- [ ] Start on goal #3 (thucydides triangle) — find a post of theirs worth engaging with substantively
