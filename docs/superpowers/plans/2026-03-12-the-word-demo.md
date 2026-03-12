# The Word Demo: MCP Server + JSON-LD REST API

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox syntax for tracking.

**Goal:** Deploy a working demo of The Word vocabulary infrastructure as a public JSON-LD REST API + MCP server on cloudpublica.org, with 90+ entries from Anytype, for the Mozilla Democracy AI Cohort application (deadline: March 16, 2026 11:59pm PT).

**Architecture:** Export Anytype's 90 objects (53 Names, 17 Sources, 13 Rediscoveries, 7 Bridges) to a SQLite database. Serve via a lightweight Node.js API that exposes JSON-LD endpoints for browsers and an MCP server for AI agents. Runs as a Docker container on the existing cloudpublica.org VM behind nginx-proxy. No ActivityPods, no PostgreSQL migration, no embedding search yet. This is Layer 1: make the data accessible.

**Tech Stack:** Node.js 22 (Alpine Docker), SQLite3 (better-sqlite3), Express.js, JSON-LD, MCP TypeScript SDK, nginx reverse proxy, Cloudflare DNS (already configured).

**Subdomain:** word.cloudpublica.org

**Related Plan:** `plans/cloudpublica-investigations-site.md` — ProPublica-style investigations site at cloudpublica.org root (same domain). The Word provides vocabulary infrastructure; the investigations site publishes the structural analysis that demonstrates why vocabulary matters. Both served via CF Pages under the Enterprise zone.

**Docker repo:** commoncloud.git/04-docker-server/ (docker-compose.yml, nginx/conf.d/)

**Anytype Word space ID:** bafyreidtuzkizdckcm7ofvjewtaq2agebgvszyqmmrmnghcblifwuoaa5a.9g641q4x5sey

**Anytype types:** name_entry, source_entry, rediscovery_entry, bridge_entry (skip page type)

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
```

Minimum viable demo (Tasks 1-5): ~300 lines TypeScript, working URL, 90+ entries searchable.
Full demo (Tasks 1-6): adds MCP so agents can use it natively.
Application (Task 7): narrative from existing architecture docs.
