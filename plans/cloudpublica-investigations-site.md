# CloudPublica.org Investigations Site — Implementation Plan

> **For agentic workers:** Read this plan at the start of each session. Check boxes as you complete steps. This is the canonical reference for the cloudpublica.org investigations site build.

**Goal:** Build a ProPublica-style investigations site at cloudpublica.org, served via Cloudflare Pages (no origin server), under the Enterprise zone with WHOIS hidden via CF Registrar.

**Architecture:** Static HTML site deployed via CF Pages from GitHub (`Gifted-Dreamers/cloudpublica`). ProPublica-style structure: `/article/slug` for investigations, organized by Topics. No "blog" terminology. Dark, serious, investigative journalism aesthetic.

Additional Cloudflare services (covered by $250K Civil Society cohort credits):
- **R2 Storage** — Large assets (PDFs, high-res diagrams) that exceed the 25MB CF Pages limit, served from `assets.cloudpublica.org`
- **Cloudflare Stream** — Host the Mozilla 2-minute demo video and future video explainers about BITE patterns. No third-party video hosting needed.
- **Analytics Engine** — Privacy-first analytics (no cookies, no third-party JS). Track article reads, diagram views, Word API referrals. Data stays on CF edge.
- **Browser Rendering /crawl API** — Research tool for sourcing: crawl URLs cited in investigations to archive snapshots and detect changes over time. Evidence preservation.

**Tech Stack:** Static HTML + Tailwind CSS (CDN), Mermaid CLI for diagram rendering, CF Pages for hosting, GitHub Actions for CI/CD, R2 (asset storage), Stream (video), Analytics Engine (metrics), Browser Rendering (source archiving).

**Related Plan:** `plans/2026-03-12-the-word-demo.md` — The Word API + MCP server at word.cloudpublica.org (same domain, different subdomain). The Word provides vocabulary infrastructure; this site provides the investigations that demonstrate why that vocabulary matters. The Word is evolving toward CF edge-native architecture (Workers + D1 + Vectorize + Workers AI) — when that migration happens, the entire cloudpublica.org domain will run serverless on Cloudflare's edge with no origin server.

**Source Material:**
- `investigations/comprehensive-analysis-for-press.md` — flagship investigation (~540 lines, 110+ sources)
- `investigations/diagram-*.mmd` — 3 Mermaid diagrams (need regeneration)
- `justNICE.us/blog/5gw-research.html` — copy to cloudpublica
- `justNICE.us/blog/open-source-transparency-tools.html` — copy to cloudpublica
- `justNICE.us/blog/psychology-of-authoritarian-control.html` — copy to cloudpublica

**Security:**
- cloudpublica.org is on CF Enterprise with CF Registrar (WHOIS hidden)
- Site served entirely from CF edge — no origin server to attack
- DNSSEC, HSTS, min TLS 1.2, CAA records — all active
- justnice.us already migrated to CF Pages (session 29) — same pattern
- Cloudflare Civil Society cohort provides Enterprise-grade protection at no cost
- WAF managed rulesets (Cloudflare Managed + OWASP Core + Exposed Credentials Check) deployed
- DDoS L7 ruleset active
- Bot Fight Mode intentionally NOT enabled — investigations site must be crawlable by search engines and AI
- robots.txt allows all crawlers; sitemap.xml published
- **CF Access dev lock ACTIVE** — site behind login wall while iterating on design. Access app ID: `b230ce64-9fb6-48fd-b256-fc9b145c6260`. Only bee@justnice.us allowed. Delete app to go public.
- Zero Trust Access available for admin interfaces (50 users free) — use for any future CMS or editorial tools

---

## Phase 1: Infrastructure Setup

### Task 1.1: Create CF Pages Project for cloudpublica.org

- [x] Create CF Pages project `cloudpublica-site` via API (account `0d4b5eb6fd041bc97e6f0d2d32e0762a`)
- [x] Build command: `node build.js` (reuse justNICE pattern)
- [x] Output dir: `dist/`
- [x] Add custom domain: `cloudpublica.org` (root)
- [x] Add custom domain: `www.cloudpublica.org`
- [x] Update DNS: root A record → CNAME `cloudpublica-site.pages.dev` (proxied)
- [x] Update DNS: www A record → CNAME `cloudpublica-site.pages.dev` (proxied)
- [x] **DO NOT touch subdomains** — word, n8n, hq, feeds, etc. stay on Docker origin
- [x] Verify DNSSEC is enabled on cloudpublica.org zone — **active**
- [x] Verify HSTS, min TLS 1.2, CAA records on zone — HSTS enabled (max-age 31536000, preload, nosniff), TLS 1.2 min, CAA has pki.goog + letsencrypt.org
- [x] Enable WAF managed rulesets — Cloudflare Managed + OWASP Core + Exposed Credentials Check deployed to zone entrypoint
- [x] ~~Enable Bot Management~~ — **Skipped intentionally.** Bot Fight Mode blocks legitimate AI crawlers (GPTBot, ClaudeBot, etc.). Investigations site needs to be findable and citable. WAF managed rulesets handle real threats.
- [x] Security level set to "high", browser check enabled, challenge TTL 1800s
- [x] Test: `curl -I https://cloudpublica.org` returns CF Pages headers

### Task 1.2: Create Site Repository Structure

Decided: new repo `Gifted-Dreamers/cloudpublica` (private).

- [x] Create GitHub repo `Gifted-Dreamers/cloudpublica` (private)
- [x] Initialize with:
  ```
  cloudpublica.org/
  ├── _partials/          # nav, footer, scripts
  ├── article/            # investigations
  ├── research/           # shorter research pieces
  ├── about/              # about page
  ├── assets/
  │   ├── img/            # hero images (12 JPGs)
  │   └── diagrams/       # Mermaid .mmd source + rendered PNGs
  ├── build.js            # partial injection (adapted from justNICE)
  ├── index.html          # landing page
  ├── robots.txt          # allow all crawlers
  ├── sitemap.xml         # 16 pages
  ├── .github/workflows/deploy.yml  # GitHub Actions → CF Pages
  └── dist/               # build output (gitignored)
  ```
- [x] Connect CF Pages to GitHub repo via GitHub Actions (auto-deploy on push to main)
- [x] Verify: push triggers build + deploy — **confirmed working**

### Task 1.3: DNS Considerations

- [x] Document current DNS state before changes
- [x] Changed ONLY root + www to CF Pages CNAME; all subdomains unchanged
- [x] Verify all subdomains still resolve after root change

---

## Phase 2: Design & Content Structure

### Task 2.1: Site Design

Dark investigative journalism aesthetic with cp-teal (#206795), cp-cyan (#38c1e0), cp-dark (#1a3347), cp-muted (#5a7a8f). Tailwind CSS via CDN.

- [x] Design nav partial (`_partials/nav.html`) — sticky dark header, Investigations/Research/About links, mobile hamburger
- [x] Design footer partial (`_partials/footer.html`) — three-column dark footer
- [x] Design article template (hero, metadata, body, sources)
- [x] Design index page (featured investigation + recent articles + topics grid + about callout)
- [ ] Design topic landing pages — **deferred** (not blocking launch)
- [x] Mobile responsive breakpoints
- [x] Favicon + OpenGraph metadata

### Task 2.2: Build System

- [x] Copy and adapt `build.js` for cloudpublica structure (113 lines, zero dependencies)
- [x] Partial injection: `<!-- build:nav -->`, `<!-- build:footer -->`, `<!-- build:scripts -->`
- [x] Active link styling per page via `<!-- build:config {"nav":"key"} -->` + `{{ACTIVE:key}}`
- [x] Build verification (no leftover tokens)

---

## Phase 3: Diagram Regeneration

### Task 3.1: Update Seven Pillars Diagram

- [x] Existing `diagram-seven-pillars.mmd` copied to cloudpublica assets/diagrams/
- [x] Rendered to PNG via mermaid-cli
- [ ] Add "Pillar 8" or expand step 7/8 — **content update deferred**
- [ ] Update Pillar 1 nodes (Pen Link, Palantir, DOGE)
- [ ] Update Pillar 4 nodes (Haiti/Vectus, BlackRock, Shield of Americas)
- [ ] Update Pillar 6 nodes (CISA status)
- [ ] Update Pillar 7 nodes (Apollo-Epstein, Bessent/CFIUS, financial fragility)
- [ ] Update NG QRF: 23,500 → 23,000+

### Task 3.2: Update Assembled Profile Diagram

- [x] Existing `diagram-assembled-profile.mmd` copied and rendered to PNG
- [ ] Update "Webblock" → "Pen Link (Webloc/Tangles)"
- [ ] Add Palantir integration layer

### Task 3.3: Update Timeline Diagram

- [x] Existing `diagram-timeline.mmd` copied and rendered to PNG
- [ ] Fix CISA status, add Haiti, Apollo-Epstein, Shield of Americas, financial fragility

### Task 3.4: New Diagram — Financial Fragility Cascade

- [x] Created `diagram-financial-fragility.mmd`
- [x] Rendered to PNG

### Task 3.5: New Diagram — Apollo-Epstein-Board of Peace Network

- [x] Created `diagram-apollo-epstein-network.mmd`
- [x] Rendered to PNG

---

## Phase 4: Content Creation

### Task 4.1: Flagship Article — Comprehensive Analysis

- [x] Title chosen: "Seven Pillars, One System: The Architecture of Consolidation"
- [x] Structure as `/article/seven-pillars.html`
- [x] Convert markdown to HTML (~1000 lines) with proper semantic structure
- [x] Embed 5 diagrams with expand/collapse pattern (max-height 600px, gradient fade, click toggle)
- [x] Style source citations (inline links)
- [x] Add article metadata: date, source count
- [x] Add OpenGraph/Twitter card metadata
- [x] Mobile-responsive styling
- [x] Hero image generated via AWS Bedrock Titan Image Generator v2 (1280x768)
- [ ] Test all 110+ source links

### Task 4.2: Copy Research Articles from justNICE

Copied 11 articles total (not just 3 from the original plan — expanded scope):

**Investigations (6):**
- [x] `5gw-research.html` → `/article/5gw-research.html`
- [x] `open-source-transparency-tools.html` → `/article/open-source-transparency-tools.html`
- [x] `psychology-of-authoritarian-control.html` → `/article/psychology-of-authoritarian-control.html`
- [x] `ai-chat-legal-risks.html` → `/article/ai-chat-legal-risks.html`
- [x] `anti-surveillance-tech-market.html` → `/article/anti-surveillance-tech-market.html`
- [x] `data-privacy-sovereignty-best-practices.html` → `/article/data-privacy-sovereignty-best-practices.html`

**Research (5):**
- [x] `vocabulary-is-infrastructure.html` → `/research/vocabulary-is-infrastructure.html`
- [x] `naming-what-you-feel.html` → `/research/naming-what-you-feel.html`
- [x] `connecting-isolated-voices.html` → `/research/connecting-isolated-voices.html`
- [x] `rebuilding-resilience.html` → `/research/rebuilding-resilience.html`
- [x] `privacy-protection-nicholas-merrill.html` → `/research/privacy-protection-nicholas-merrill.html`

All restyled: maroon/gold → cp-teal/cp-cyan, dark theme, cloudpublica branding/favicon/og URLs, build markers.

- [x] Hero images: 11 copied from justNICE + 1 Bedrock-generated for flagship = 12 total
- [ ] Update internal cross-links between articles

### Task 4.3: Index Page

- [x] Featured investigation with hero image (Bedrock-generated)
- [x] Recent articles grid (3 cards)
- [x] Topics grid (4 categories)
- [x] "About this project" blurb with link to GD
- [ ] Link to The Word (word.cloudpublica.org) — **deferred until CF security plan complete**

---

## Phase 5: Deployment & Security

### Task 5.1: Deploy to CF Pages

- [x] Push to GitHub main branch
- [x] Verify CF Pages auto-build succeeds (GitHub Actions)
- [x] Verify custom domain resolves (cloudpublica-site.pages.dev confirmed; cloudpublica.org SSL was pending, now active)
- [ ] Verify subdomains (word, n8n, hq) still work
- [ ] Test on mobile

### Task 5.2: Security Hardening

- [x] WAF managed rulesets active (Cloudflare Managed + OWASP Core + Exposed Credentials Check)
- [x] DDoS L7 ruleset active
- [x] ~~Bot Fight Mode~~ — **Skipped.** Blocks AI crawlers. Using WAF + security level "high" + browser check instead.
- [x] Security level: high
- [x] Browser integrity check: on
- [x] HSTS: enabled (max-age 31536000, preload, include_subdomains, nosniff)
- [x] Min TLS: 1.2
- [x] DNSSEC: active
- [x] CAA records: pki.goog + letsencrypt.org
- [x] robots.txt: allow all crawlers
- [x] sitemap.xml: 16 pages
- [ ] Add rate limiting rules
- [ ] Set up CF notifications for DDoS alerts
- [ ] Test with `securityheaders.com`

### Task 5.3: Large File Handling

- [ ] No large assets needed yet — all hero images under 2MB, all within CF Pages 25MB limit

### Task 5.4: Set Up R2 Bucket for Large Assets

- [ ] Create R2 bucket `cloudpublica-assets` — **deferred until needed**
- [ ] Add custom domain `assets.cloudpublica.org`
- [ ] Upload any oversized assets
- [ ] Configure CORS headers
- [ ] Test access

### Task 5.5: Set Up Cloudflare Stream for Video

- [ ] Upload Mozilla 2-minute demo video to CF Stream
- [ ] Embed in investigations site
- [ ] Embed in Mozilla Democracy AI application materials
- [ ] Future: BITE pattern explainer videos
- [ ] Future: investigation companion videos

---

## Phase 6: Cleanup & Documentation

### Task 6.1: Update DNS Reference Doc

- [ ] Update `commoncloud.git/docs/reference/integrations/DNS.md`:
  - cloudpublica.org root/www → CF Pages (no longer Docker origin)
  - justnice.us root/www → CF Pages (completed session 29)
  - Note: subdomains unchanged

### Task 6.2: Remove Old Deployment Path

- [ ] Remove justnice.us from Docker nginx config (no longer serving from origin)
- [ ] Remove justnice.us Docker mount from docker-compose.yml
- [ ] Remove justnice.us LE certs from Docker (CF Pages handles SSL)
- [ ] Keep justnice.us GitHub Actions for now (can migrate to CF Pages auto-deploy later)

### Task 6.3: Update MEMORY.md

- [x] Add cloudpublica.org site structure and deploy path
- [x] Update infrastructure section
- [x] Update priorities

---

## Dependencies & Ordering

```
Phase 1 (infra) → Phase 2 (design) → Phase 3 (diagrams) + Phase 4.2 (copy articles)
                                    → Phase 4.1 (flagship, needs diagrams from Phase 3)
                                    → Phase 4.3 (index, needs articles)
Phase 4 complete → Phase 5 (deploy) → Phase 6 (cleanup)
```

Phases 3 and 4.2 can run in parallel. Phase 4.1 depends on Phase 3 (diagrams).

---

## Key Decisions — Resolved

1. **Title for flagship article** → "Seven Pillars, One System: The Architecture of Consolidation"
2. **Author attribution** → Cloud Publica (no individual name yet)
3. **Repo name** → `Gifted-Dreamers/cloudpublica` (private)
4. **Color scheme** → Dark theme: cp-teal (#206795), cp-cyan (#38c1e0), cp-dark (#1a3347), cp-muted (#5a7a8f)
5. **Diagram rendering** → Mermaid CLI (local `npx mmdc`) for .mmd → PNG, AWS Bedrock for hero images
6. **Video hosting** → CF Stream (deferred)
7. **Analytics** → CF Analytics Engine (deferred, not blocking launch)
8. **Bot policy** → No Bot Fight Mode. Allow all crawlers. WAF handles threats.

---

*Created: Session 29, March 12, 2026*
*Last Updated: Session 36, March 13, 2026*
