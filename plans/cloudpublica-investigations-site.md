# CloudPublica.org Investigations Site — Implementation Plan

> **For agentic workers:** Read this plan at the start of each session. Check boxes as you complete steps. This is the canonical reference for the cloudpublica.org investigations site build.

**Goal:** Build a ProPublica-style investigations site at cloudpublica.org, served via Cloudflare Pages (no origin server), under the Enterprise zone with WHOIS hidden via CF Registrar.

**Architecture:** Static HTML site deployed via CF Pages from GitHub (commoncloud.git or new repo). ProPublica-style structure: `/article/slug` for investigations, organized by Topics. No "blog" terminology. Dark, serious, investigative journalism aesthetic.

**Tech Stack:** Static HTML + Tailwind CSS (CDN), Mermaid.js for diagrams, CF Pages for hosting, GitHub Actions for CI/CD.

**Source Material:**
- `UnrigUSA/comprehensive-analysis-for-press.md` — flagship investigation (~540 lines, 110+ sources)
- `UnrigUSA/diagram-*.mmd` — 3 Mermaid diagrams (need regeneration)
- `justNICE.us/blog/5gw-research.html` — copy to cloudpublica
- `justNICE.us/blog/open-source-transparency-tools.html` — copy to cloudpublica
- `justNICE.us/blog/psychology-of-authoritarian-control.html` — copy to cloudpublica

**Security:**
- cloudpublica.org is on CF Enterprise with CF Registrar (WHOIS hidden)
- Site served entirely from CF edge — no origin server to attack
- DNSSEC, HSTS, min TLS 1.2, CAA records required
- justnice.us already migrated to CF Pages (session 29) — same pattern

---

## Phase 1: Infrastructure Setup

### Task 1.1: Create CF Pages Project for cloudpublica.org

- [ ] Create CF Pages project `cloudpublica-site` via API (account `0d4b5eb6fd041bc97e6f0d2d32e0762a`)
- [ ] Build command: `node build.js` (reuse justNICE pattern)
- [ ] Output dir: `dist/`
- [ ] Add custom domain: `cloudpublica.org` (root)
- [ ] Add custom domain: `www.cloudpublica.org`
- [ ] Update DNS: root A record → CNAME `cloudpublica-site.pages.dev` (proxied)
- [ ] Update DNS: www A record → CNAME `cloudpublica-site.pages.dev` (proxied)
- [ ] **DO NOT touch subdomains** — word, n8n, hq, feeds, etc. stay on Docker origin
- [ ] Verify DNSSEC is enabled on cloudpublica.org zone
- [ ] Verify HSTS, min TLS 1.2, CAA records on zone
- [ ] Test: `curl -I https://cloudpublica.org` returns CF Pages headers

### Task 1.2: Create Site Repository Structure

Decide: new repo OR subdirectory in commoncloud.git. **Recommendation: new repo `Gifted-Dreamers/cloudpublica.org`** — keeps it clean, CF Pages connects directly.

- [ ] Create GitHub repo `Gifted-Dreamers/cloudpublica.org` (private)
- [ ] Initialize with:
  ```
  cloudpublica.org/
  ├── _partials/          # nav, footer, scripts (like justNICE)
  ├── article/            # investigations (ProPublica-style)
  ├── research/           # shorter research pieces
  ├── assets/
  │   ├── css/
  │   ├── img/
  │   └── diagrams/       # rendered SVG/PNG from Mermaid
  ├── build.js            # partial injection (adapt from justNICE)
  ├── index.html           # landing page
  └── dist/               # build output (gitignored)
  ```
- [ ] Connect CF Pages to GitHub repo (auto-deploy on push to main)
- [ ] Verify: push triggers build + deploy

### Task 1.3: DNS Considerations

**CRITICAL:** cloudpublica.org root currently points to Docker VM (3.232.111.51) via A record. Subdomains (word, n8n, hq, feeds, etc.) also point there.

**Strategy:** Change ONLY the root (`cloudpublica.org`) and `www` to CF Pages. All subdomains keep their A records to the Docker VM.

- [ ] Document current DNS state before changes
- [ ] Verify all subdomains still resolve after root change
- [ ] The existing nginx `00-default.conf` serves the landing page — it will stop receiving traffic for root domain but subdomains unaffected

---

## Phase 2: Design & Content Structure

### Task 2.1: Site Design

ProPublica-inspired, not ProPublica-copied. Key attributes:
- Clean, high-contrast, readable typography
- Dark header/nav, light article body
- Source citations prominently displayed (not hidden in footnotes)
- Mobile-first responsive
- No ads, no tracking, no cookies
- Tailwind CSS via CDN (same as justNICE)

Navigation structure:
```
Cloud Publica
├── Investigations          → /article/
├── Research                → /research/
├── Topics                  → topic-based filtering
│   ├── Surveillance
│   ├── Elections
│   ├── AI & Security
│   ├── Financial Architecture
│   └── Military & Foreign Policy
├── About                   → /about/
└── The Word                → word.cloudpublica.org (external link)
```

- [ ] Design nav partial (`_partials/nav.html`)
- [ ] Design footer partial (`_partials/footer.html`)
- [ ] Design article template (hero, metadata, body, sources)
- [ ] Design index page (featured investigation + recent articles)
- [ ] Design topic landing pages
- [ ] Mobile responsive breakpoints
- [ ] Favicon + OpenGraph metadata

### Task 2.2: Build System

Adapt justNICE `build.js` pattern:
- [ ] Copy and adapt `build.js` for cloudpublica structure
- [ ] Partial injection: `<!-- build:nav -->`, `<!-- build:footer -->`, `<!-- build:scripts -->`
- [ ] Active link styling per page
- [ ] Build verification (no leftover tokens)

---

## Phase 3: Diagram Regeneration

### Task 3.1: Update Seven Pillars Diagram

Current `diagram-seven-pillars.mmd` is outdated. Needs:

- [ ] Add "Pillar 8" or expand step 7/8 in "What Connects Them":
  - Step 7: Privatize state functions (Haiti template, BlackRock ports)
  - Step 8: Enforce via leverage (Epstein files, Apollo-Board of Peace, database consolidation)
- [ ] Update Pillar 1 nodes:
  - "Webblock" → "Pen Link (Webloc/Tangles)"
  - Add Palantir HHS contracts (~$300M), denials AI
  - Add DOGE-Palantir pipeline
- [ ] Update Pillar 4 nodes:
  - Add Haiti/Vectus privatization
  - Add BlackRock Panama Canal
  - Add Shield of Americas
- [ ] Update Pillar 6 nodes:
  - Fix "Cyber Info Sharing Act EXPIRED during shutdown" → "expired Sept 30, 2025; re-extended through Sept 30, 2026"
- [ ] Update Pillar 7 nodes:
  - Add Apollo-Epstein-Board of Peace connection
  - Add Bessent/CFIUS conflict
  - Add financial fragility data
- [ ] Update NG QRF: 23,500 → 23,000+
- [ ] Render to SVG/PNG using Mermaid CLI or Mermaid Chart MCP

### Task 3.2: Update Assembled Profile Diagram

Current `diagram-assembled-profile.mmd` needs:
- [ ] Update "Webblock ($5M)" → "Pen Link (Webloc/Tangles) ($5M)"
- [ ] Add Palantir as integration layer connecting all databases
- [ ] Render to SVG/PNG

### Task 3.3: Update Timeline Diagram

Current `diagram-timeline.mmd` needs:
- [ ] Fix "Cyber Info Sharing Act expires in shutdown" → correct status
- [ ] Add Haiti privatization events
- [ ] Add Apollo-Epstein lawsuit (March 2, 2026)
- [ ] Add Shield of Americas (March 7, 2026)
- [ ] Add financial fragility markers
- [ ] Render to SVG/PNG

### Task 3.4: New Diagram — Financial Fragility Cascade

- [ ] Create new Mermaid diagram showing:
  - $38.88T debt → $1T/yr interest → $5T corporate rollover
  - Private credit stress (Blue Owl) → zombie firms (1 in 5) → BBB cliff (50% of IG)
  - Iran war trigger → oil $100 → Hormuz insurance 12x → rare earths vaporized → Qatar offline
- [ ] Render to SVG/PNG

### Task 3.5: New Diagram — Apollo-Epstein-Board of Peace Network

- [ ] Create relationship diagram:
  - Rowan (Apollo CEO) → Board of Peace + Gaza Board + SDNY lawsuit
  - Black (Apollo co-founder) → $158M to Epstein → Senate found $170M
  - Kushner → 666 Fifth Ave ($300M Apollo) → $55B Saudi EA deal
  - Bessent (Treasury) → blocking Epstein records + chairing CFIUS
  - Deutsche Bank → flagged both Epstein + Kushner → same supervisor suppressed
  - Kahn (Epstein accountant) → tracked Rowan trades + Kushner vulnerabilities
- [ ] Render to SVG/PNG

---

## Phase 4: Content Creation

### Task 4.1: Flagship Article — Comprehensive Analysis

Convert `comprehensive-analysis-for-press.md` to HTML article:

- [ ] Choose title from the 8 options in the markdown (or create new)
- [ ] Structure as `/article/seven-pillars-consolidation` (or chosen slug)
- [ ] Convert markdown to HTML with proper semantic structure
- [ ] Embed regenerated diagrams (SVG inline or img tags)
- [ ] Style source citations (ProPublica uses inline links + expandable source lists)
- [ ] Add article metadata: author, date, last updated, source count
- [ ] Add OpenGraph/Twitter card metadata
- [ ] Mobile-responsive table styling (the data tables)
- [ ] Test all 110+ source links

### Task 4.2: Copy Research Articles from justNICE

Copy (not move — leave originals on justNICE):

- [ ] `5gw-research.html` → `/research/fifth-generation-warfare`
  - Restyle to match cloudpublica design
  - Update nav/footer to cloudpublica partials
- [ ] `open-source-transparency-tools.html` → `/research/transparency-tools`
  - Restyle to match cloudpublica design
- [ ] `psychology-of-authoritarian-control.html` → `/research/psychology-authoritarian-control`
  - Restyle to match cloudpublica design
- [ ] Update internal cross-links between articles

### Task 4.3: Index Page

- [ ] Featured investigation (comprehensive analysis) with hero image/diagram
- [ ] Recent articles grid
- [ ] Topic tags
- [ ] "About this project" blurb
- [ ] Link to The Word (word.cloudpublica.org)

---

## Phase 5: Deployment & Security

### Task 5.1: Deploy to CF Pages

- [ ] Push to GitHub main branch
- [ ] Verify CF Pages auto-build succeeds
- [ ] Verify custom domain resolves
- [ ] Verify subdomains (word, n8n, hq) still work
- [ ] Test on mobile

### Task 5.2: Security Hardening

- [ ] Verify Enterprise WAF is active on cloudpublica.org zone
- [ ] Enable Bot Fight Mode
- [ ] Add rate limiting rules (Enterprise allows unlimited)
- [ ] Set up CF notifications for DDoS alerts
- [ ] Verify CAA records include `pki.goog` (for Pages SSL)
- [ ] Test with `securityheaders.com`

### Task 5.3: Large File Handling

3 PDFs from justNICE exceeded CF Pages 25MB limit. For cloudpublica:
- [ ] If any large assets needed, upload to CF R2
- [ ] Serve from `assets.cloudpublica.org` subdomain

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

- [ ] Add cloudpublica.org site structure and deploy path
- [ ] Update infrastructure section
- [ ] Update priorities

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

## Key Decisions Still Needed

1. **Title for flagship article** — 8 options in the markdown, or new
2. **Author attribution** — "[TBD]" in current doc. Cloud Publica editorial? Individual name? Pseudonym?
3. **Repo name** — `cloudpublica.org` or `cloudpublica-site` or subdirectory of commoncloud.git?
4. **Color scheme** — dark teal/cyan from current landing page? Or new palette?
5. **Diagram rendering** — Mermaid CLI (local), Mermaid Chart MCP, or client-side Mermaid.js?

---

*Created: Session 29, March 12, 2026*
*Last Updated: March 12, 2026*
