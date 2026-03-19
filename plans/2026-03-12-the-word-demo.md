# The Word Demo: MCP Server + JSON-LD REST API

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox syntax for tracking.

**Goal:** Deploy a working demo of The Word vocabulary infrastructure as a public JSON-LD REST API + MCP server on cloudpublica.org, with 90+ entries from Anytype, for the Mozilla Democracy AI Cohort application (deadline: March 16, 2026 11:59pm PT). The Docker deployment is the MVP; the architecture is designed for edge-native evolution via Cloudflare Workers/D1/Vectorize/Workers AI, adding global distribution, multilingual semantic search, and ethical web scanning without replacing the origin.

**Architecture:**

- **Layer 1 (deployed — Docker origin):** Export Anytype's 90 objects (53 Names, 17 Sources, 13 Rediscoveries, 7 Bridges) to a SQLite database. Serve via a lightweight Node.js API that exposes JSON-LD endpoints for browsers and an MCP server for AI agents. Runs as a Docker container on the existing cloudpublica.org VM behind nginx-proxy. This is the MVP and remains the origin server.

- **Layer 1.5 (edge-native — new):** Cloudflare Workers as API gateway fronting D1 (serverless SQLite at edge, globally distributed). Workers AI provides multilingual embeddings for felt-sense search. Vectorize stores and queries vocabulary entry vectors for semantic similarity. Browser Rendering /crawl API enables BITE pattern scanning of external content. Analytics Engine tracks search-to-name conversion and felt-sense coverage gaps. The Docker origin becomes the fallback; D1 becomes the primary data store at edge.

- **Layer 2 (future):** ActivityPub federation — vocabulary entries federate across instances.

- **Layer 3 (future):** ActivityPods/Solid — decentralized identity and data sovereignty.

**Tech Stack:** Node.js 22 (Alpine Docker), SQLite3 (better-sqlite3), Express.js, JSON-LD, MCP TypeScript SDK, nginx reverse proxy, Cloudflare DNS (already configured), Cloudflare Workers, D1 (serverless SQLite), Workers AI ($50K cap for ML at edge), Vectorize (vector DB), Browser Rendering API (/crawl endpoint for ethical web scanning), R2 (object storage, zero egress), Analytics Engine.

**Subdomain:** word.cloudpublica.org

**Related Plan:** `plans/cloudpublica-investigations-site.md` — ProPublica-style investigations site at cloudpublica.org root (same domain). The Word provides vocabulary infrastructure; the investigations site publishes the structural analysis that demonstrates why vocabulary matters. Both served via CF Pages + R2 under the Enterprise zone.

**Docker repo:** commoncloud.git/04-docker-server/ (docker-compose.yml, nginx/conf.d/)

**Anytype Word space ID:** bafyreidtuzkizdckcm7ofvjewtaq2agebgvszyqmmrmnghcblifwuoaa5a.9g641q4x5sey

**Anytype types:** name_entry, source_entry, rediscovery_entry, bridge_entry (skip page type)

**Cloudflare credits:** $250K via Civil Society cohort (including $50K Workers AI cap). All infrastructure costs covered by CF credits, so Mozilla's $50K goes entirely to development — research, content creation, community building, and contributor stipends.

**Credibility signal:** Acceptance into the Cloudflare Civil Society cohort validates the project's public-interest mission and provides enterprise-grade infrastructure at zero cost. This is not a startup discount; it is a cohort for organizations doing work Cloudflare considers essential to civil society.

---

## Chunk 1: Data Export Pipeline (Anytype to SQLite)

### Task 1: Create project directory and scaffold

**Files:**
- Create: the-word/package.json
- Create: the-word/tsconfig.json
- Create: the-word/.gitignore
- Create: the-word/Dockerfile

Location: commoncloud.git/04-docker-server/the-word/

- [ ] Step 1: Create project directory structure (the-word/src, the-word/scripts, the-word/data)
- [ ] Step 2: Create package.json with dependencies: @modelcontextprotocol/sdk, better-sqlite3, express. Dev deps: @types/better-sqlite3, @types/express, @types/node, tsx, typescript
- [ ] Step 3: Create tsconfig.json (target ES2022, module ESNext, moduleResolution bundler, outDir dist, rootDir src)
- [ ] Step 4: Create .gitignore (node_modules, dist, data/*.db, .env)
- [ ] Step 5: Create Dockerfile (node:22-alpine, copy dist and data, expose 3456, CMD node dist/server.js)
- [ ] Step 6: Commit scaffold

### Task 2: Write database schema and import script

**Files:**
- Create: the-word/src/db.ts (schema + helpers)
- Create: the-word/src/scripts/import-json.ts (reads data/export.json, populates SQLite)

**Schema tables:** names (id, name, felt_sense, definition, why_it_matters, source_year, source_author, domain, human_search_terms, agent_search_terms), sources (id, name, author, year, source_type, url, description), rediscoveries (id, name, observed_by, platform, description, maps_to_id, date_observed, evidence_url, notes), bridges (id, name, from_name, to_name, relationship, description), metadata (key, value). Plus FTS5 virtual table on names for full-text search.

**Import script:** Reads data/export.json (array of {type, id, name, properties}), inserts into appropriate table based on type field, runs in a transaction.

- [ ] Step 1: Create src/db.ts with openDb() and initSchema() functions
- [ ] Step 2: Create src/scripts/import-json.ts that reads export.json and populates all tables
- [ ] Step 3: Commit

### Task 3: Extract data from Anytype via MCP

This task is performed by Claude Code using Anytype MCP tools directly.

- [ ] Step 1: Call mcp__anytype__API-list-objects for the Word space (limit=100)
- [ ] Step 2: For each object, map type.key to table (name_entry->names, source_entry->sources, rediscovery_entry->rediscoveries, bridge_entry->bridges, page->skip)
- [ ] Step 3: Extract all property values, mapping Anytype property keys to schema columns
- [ ] Step 4: Write the-word/data/export.json
- [ ] Step 5: Run import script locally: npx tsx src/scripts/import-json.ts
- [ ] Step 6: Verify with sqlite3: SELECT count from each table
- [ ] Step 7: Commit export.json (word.db is gitignored, regenerated from export.json)

---

## Chunk 2: REST API + JSON-LD

### Task 4: Build the REST API server

**Files:**
- Create: the-word/src/jsonld.ts (JSON-LD context and wrappers)
- Create: the-word/src/routes.ts (Express routes)
- Create: the-word/src/server.ts (Express app with landing page)

**JSON-LD context:** Uses schema.org, SKOS, and custom vocab namespace at word.cloudpublica.org/vocab/. Each response is a valid JSON-LD document.

**Endpoints:**
- GET /api/stats - library overview (counts per table)
- GET /api/names - all names
- GET /api/names/:id - single name
- GET /api/search?q=... - full-text search (FTS5)
- GET /api/felt-sense?q=... - Doorway 1 felt-sense search (alias for search, signals intent)
- GET /api/sources - all sources
- GET /api/sources/:id - single source
- GET /api/rediscoveries - all rediscoveries
- GET /api/rediscoveries/:id - single rediscovery
- GET /api/bridges - all bridges
- GET /api/bridges/:id - single bridge
- GET / - HTML landing page explaining what The Word is, with clickable API links

**Landing page content:** Brief explanation of The Word, list of API endpoints with links, link to GitHub repo, "Built by Gifted Dreamers 501(c)(3)"

**Server config:** Port 3456 (from PORT env var), CORS enabled, Content-Type application/ld+json, FTS index rebuilt on startup.

- [ ] Step 1: Create src/jsonld.ts with context object and wrapper functions (wrapName, wrapSource, wrapRediscovery, wrapBridge, wrapCollection)
- [ ] Step 2: Create src/routes.ts with all route handlers
- [ ] Step 3: Create src/server.ts with Express app, CORS, landing page HTML
- [ ] Step 4: Test locally: npm run build && npm start, then curl localhost:3456/api/stats
- [ ] Step 5: Commit

---

## Chunk 3: Docker + nginx + Deploy

### Task 5: Add to docker-compose and nginx, deploy to server

**Files:**
- Modify: docker-compose.yml (add the-word service on port 3456, proxy network, healthcheck via wget on /api/stats)
- Create: nginx/conf.d/the-word.conf (server_name word.cloudpublica.org, proxy_pass to the-word:3456)

**Deploy steps:**
1. Build TypeScript locally (npm run build)
2. scp the-word/ directory to aws-docker:/home/admin/commoncloud/the-word/
3. scp nginx config to server
4. docker compose build the-word && docker compose up -d the-word
5. nginx -s reload
6. Add DNS: word.cloudpublica.org CNAME to cloudpublica.org (Cloudflare, proxied/orange)

- [ ] Step 1: Add the-word service to docker-compose.yml
- [ ] Step 2: Create nginx/conf.d/the-word.conf
- [ ] Step 3: Add Cloudflare DNS record
- [ ] Step 4: Build locally and scp to server
- [ ] Step 5: Build container and start on server
- [ ] Step 6: Verify: curl https://word.cloudpublica.org/api/stats
- [ ] Step 7: Verify: curl "https://word.cloudpublica.org/api/felt-sense?q=helping+people+when+it+hurts"
- [ ] Step 8: Commit infrastructure changes

---

## Chunk 4: MCP Server (stretch goal)

### Task 6: Add MCP server for AI agents

**Files:**
- Create: the-word/src/mcp.ts (MCP tool definitions using @modelcontextprotocol/sdk)
- Create: the-word/src/mcp-stdio.ts (stdio entry point for local MCP use)

**MCP Tools:**
- search_names(query) - keyword/concept search
- felt_sense_search(description) - natural language experience description search (Doorway 1)
- get_bridges(name) - find bridges for a concept
- list_rediscoveries(limit?) - list independent rediscoveries

The MCP server runs via stdio transport so anyone can add it to their Claude Code or other MCP client config. The REST API is the primary demo; MCP is the unique value prop showing agent accessibility.

- [ ] Step 1: Create src/mcp.ts with tools/list and tools/call handlers
- [ ] Step 2: Create src/mcp-stdio.ts entry point
- [ ] Step 3: Test locally by adding to Claude Code MCP config and calling search_names
- [ ] Step 4: Commit

---

## Chunk 4.5: Edge-Native Migration

> **Phase:** Post-MVP. After Docker deploy is live and verified (Chunks 1-4), migrate the API to Cloudflare's edge-native stack. Docker origin stays as fallback. All infrastructure costs covered by $250K Cloudflare Civil Society cohort credits.

### Task 6.5: Deploy The Word API as a Cloudflare Worker fronting D1

**Files:**
- Create: the-word/worker/wrangler.toml (D1 binding, routes, compatibility flags)
- Create: the-word/worker/src/index.ts (Worker fetch handler mirroring Express routes)
- Create: the-word/worker/migrations/0001_initial_schema.sql (D1 migration from SQLite schema)

**Steps:**

- [ ] Step 1: Migrate SQLite schema to D1 migration format (D1 is SQLite-compatible but uses Cloudflare's migration system)
- [ ] Step 2: Rewrite Express route handlers as a Worker fetch handler (same JSON-LD responses, same endpoints)
- [ ] Step 3: Configure wrangler.toml with D1 database binding, route to word.cloudpublica.org
- [ ] Step 4: Import export.json data into D1 via wrangler d1 execute
- [ ] Step 5: Deploy via `npx wrangler deploy`
- [ ] Step 6: Verify: curl https://word.cloudpublica.org/api/stats returns same data as Docker origin
- [ ] Step 7: Keep Docker container running as fallback origin (CF failover rule if Worker errors)
- [ ] Step 8: Commit worker code

### Task 6.6: Add Workers AI + Vectorize for multilingual felt-sense search

**Files:**
- Modify: the-word/worker/src/index.ts (add /api/felt-sense-semantic endpoint)
- Create: the-word/worker/src/vectorize.ts (embedding + search logic)

Workers AI model: `@cf/baai/bge-base-en-v1.5` (or multilingual-e5 when available) for embedding generation. Vectorize index stores vocabulary entries as vectors. Felt-sense search queries Vectorize for semantic similarity, returning names ranked by conceptual closeness to the query.

**Steps:**

- [ ] Step 1: Create Vectorize index via wrangler (`wrangler vectorize create the-word-vectors --dimensions 768 --metric cosine`)
- [ ] Step 2: Generate embeddings for all vocabulary entries (name + felt_sense + definition concatenated) using Workers AI
- [ ] Step 3: Insert vectors into Vectorize index with entry IDs as metadata
- [ ] Step 4: Add /api/felt-sense-semantic?q=... endpoint: embed the query via Workers AI, search Vectorize, return top-N matches with similarity scores
- [ ] Step 5: Supports queries in English, Spanish, Portuguese, French, Arabic (multilingual embedding model handles cross-lingual similarity)
- [ ] Step 6: Test: curl "https://word.cloudpublica.org/api/felt-sense-semantic?q=when+someone+helps+you+but+it+hurts" should rank "Rubber-banding" or similar high
- [ ] Step 7: Commit

### Task 6.7: Add Browser Rendering /crawl for BITE pattern scanning

**Files:**
- Create: the-word/worker/src/crawl.ts (Browser Rendering integration for BITE scanning)
- Modify: the-word/worker/src/index.ts (add /api/crawl endpoint)

Browser Rendering API renders pages headlessly at edge. The /crawl endpoint accepts target URLs, renders them, extracts text content, and pipes it through BITE (Behavior, Information, Thought, Emotional control) pattern matching against The Word's vocabulary.

**Steps:**

- [ ] Step 1: Add Browser Rendering binding to wrangler.toml
- [ ] Step 2: Create POST /api/crawl endpoint: accepts `{ url: string }`, renders via Browser Rendering, extracts text
- [ ] Step 3: Create GET /api/crawl/:id endpoint: returns crawl results with BITE domain activation scores
- [ ] Step 4: Pipe extracted text through BITE matching engine (pattern match against domain tags and vocabulary definitions)
- [ ] Step 5: Respect robots.txt by default (ethical scanning — check before rendering)
- [ ] Step 6: Rate limit: 1 crawl/minute per IP (abuse prevention)
- [ ] Step 7: Test with known BITE-heavy content, verify domain activation scores
- [ ] Step 8: Commit

### Task 6.8: Add Analytics Engine for Word metrics

**Files:**
- Modify: the-word/worker/src/index.ts (add analytics event logging)
- Create: the-word/worker/src/analytics.ts (Analytics Engine event definitions)

Track usage patterns to understand how vocabulary infrastructure gets used, without cookies or PII.

**Steps:**

- [ ] Step 1: Add Analytics Engine binding to wrangler.toml
- [ ] Step 2: Log events: search queries (hashed, not raw text), endpoint hit counts, felt-sense vs keyword search ratio
- [ ] Step 3: Track search-to-name conversion (did a search lead to a specific name being viewed?)
- [ ] Step 4: Track BITE domain activation frequency (which domains appear most in crawl results?)
- [ ] Step 5: Track felt-sense coverage gaps (searches that return zero or low-similarity results — these are vocabulary the library needs)
- [ ] Step 6: No cookies, no PII, no IP logging — privacy-first (follows CF Web Analytics model)
- [ ] Step 7: Commit

---

## Chunk 5: Mozilla Application

### Task 7: Write project proposal

**Files:**
- Create: docs/mozilla-democracy-ai-proposal.md

Pull from existing docs: contribution-architecture-draft.md, living-library-v2-architecture.md (five unmet needs), affect labeling research (Lieberman 2007), AI chatbot harm cases, experiment results, the working demo URL.

**Narrative:** Problem (closed-loop AI companions harming teens, no vocabulary routing) -> Solution (The Word breaks closed loops via naming + citation + exit ramps) -> Evidence (3 experiments, 90+ entries, 13 rediscoveries, neuroscience) -> Democracy angle (vocabulary access as democratic infrastructure, offline-capable, open source, no paywall) -> Team and 12-month plan.

**Must address all 6 evaluation criteria:** technical viability, problem/community clarity, impact potential, values alignment, sustainability, theme fit.

- [ ] Step 1: Draft proposal
- [ ] Step 2: Review against 6 Mozilla criteria
- [ ] Step 3: Submit by March 16 11:59pm PT

---

## Critical Path

```
Day 1 (Mar 12): Tasks 1-3 -- scaffold, schema, export from Anytype
Day 2 (Mar 13): Task 4 -- REST API + JSON-LD
Day 3 (Mar 14): Task 5 -- Docker + nginx + deploy + verify live
Day 3 (Mar 14): Task 6 -- MCP server (stretch)
Day 4 (Mar 15-16): Task 7 -- Write and submit Mozilla proposal
Post-MVP:     Tasks 6.5-6.8 -- Edge-native migration (after Docker is live, before or alongside Mozilla submission if time permits)
```

Minimum viable demo (Tasks 1-5): ~300 lines TypeScript, working URL, 90+ entries searchable.
Full demo (Tasks 1-6): adds MCP so agents can use it natively.
Edge evolution (Tasks 6.5-6.8): global distribution, multilingual semantic search, BITE scanning, privacy-first analytics.
Application (Task 7): narrative from existing architecture docs. Note: Cloudflare credits cover all infra, so Mozilla's $50K is 100% development spend.
