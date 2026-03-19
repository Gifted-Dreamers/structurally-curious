# RSSHub Deployment Plan — Docker VM (cloudpublica.org)

**Status:** PREPARED (not deployed)
**Target:** rsshub.cloudpublica.org
**Server:** aws-docker (3.232.111.51)
**Created:** 2026-03-12

---

## Overview

RSSHub is a self-hosted RSS feed generator that creates RSS feeds from websites that don't natively support them (Threads, Instagram, Twitter/X, Reddit, etc.). Deploying our own instance means:
- No rate limits from public instances
- Privacy: feed requests stay on our infrastructure
- Feeds Miniflux (feeds.cloudpublica.org) with sources that lack native RSS
- Full control over caching, access, and routes

---

## 1. Docker Compose Service Block

Add this to `/home/admin/commoncloud/docker-compose.yml` after the Miniflux services:

```yaml
  # ===========================================
  # RSSHUB - Self-hosted RSS Feed Generator
  # rsshub.cloudpublica.org
  # Generates RSS from Threads, Instagram, etc.
  # ===========================================
  rsshub:
    image: diygod/rsshub:latest
    container_name: rsshub
    restart: unless-stopped
    depends_on:
      rsshub-redis:
        condition: service_healthy
    environment:
      - NODE_ENV=production
      - CACHE_TYPE=redis
      - REDIS_URL=redis://rsshub-redis:6379/
      # Access control — require key in query string: ?key=YOUR_KEY
      - ACCESS_KEY=${RSSHUB_ACCESS_KEY}
      # Rate limiting (requests per IP per 10 minutes)
      - REQUEST_TIMEOUT=10000
      # Cache duration in seconds (default 300 = 5min; 900 = 15min to match Miniflux polling)
      - CACHE_EXPIRE=900
      - CACHE_CONTENT_EXPIRE=3600
      # Disable Puppeteer/Browserless (saves ~500MB RAM; most routes don't need it)
      # If Threads route requires it later, switch image to diygod/rsshub:chromium-bundled
    networks:
      - commoncloud
    labels:
      - "com.datadoghq.tags.env=production"
      - "com.datadoghq.tags.service=rsshub"
      - "com.datadoghq.tags.team=commoncloud"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:1200/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
    # Security hardening
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 128M

  rsshub-redis:
    image: redis:alpine
    container_name: rsshub-redis
    restart: unless-stopped
    volumes:
      - rsshub_redis_data:/data
    networks:
      - commoncloud
    labels:
      - "com.datadoghq.tags.env=production"
      - "com.datadoghq.tags.service=rsshub-redis"
      - "com.datadoghq.tags.team=commoncloud"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 5s
    # Security hardening
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          memory: 128M
          cpus: '0.25'
        reservations:
          memory: 32M
```

Also add to the `volumes:` section at the bottom of docker-compose.yml:

```yaml
  # RSSHub volume
  rsshub_redis_data:
    driver: local
```

And add `rsshub` to the nginx `depends_on:` list.

---

## 2. Nginx Config

Create file: `/home/admin/commoncloud/nginx/conf.d/rsshub.conf`

```nginx
# ===========================================
# RSSHUB - rsshub.cloudpublica.org
# ===========================================
# Self-hosted RSS feed generator
# Generates feeds from Threads, Instagram, etc.
# Access controlled via ACCESS_KEY env var
# ===========================================

server {
    listen 80;
    server_name rsshub.cloudpublica.org;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        try_files $uri =404;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name rsshub.cloudpublica.org;

    ssl_certificate /etc/nginx/certs/cloudpublica-origin.crt;
    ssl_certificate_key /etc/nginx/certs/cloudpublica-origin.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Authenticated Origin Pulls — only accept connections from Cloudflare
    include /etc/nginx/conf.d/authenticated-origin-pull.conf.inc;

    # Health check — no rate limit needed (internal)
    location /healthz {
        proxy_pass http://rsshub:1200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        limit_req zone=api burst=30 nodelay;

        proxy_pass http://rsshub:1200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Security headers
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
        add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()" always;
    }
}
```

---

## 3. DNS Record (Cloudflare)

Add a CNAME or A record for the subdomain. Since `*.cloudpublica.org` uses CF Origin cert:

| Type | Name | Content | Proxy | TTL |
|------|------|---------|-------|-----|
| A | rsshub | 3.232.111.51 | Proxied (orange cloud) | Auto |

The wildcard Origin cert (`*.cloudpublica.org`, expires 2040) already covers this subdomain, so no new SSL cert is needed.

---

## 4. Environment Variable

Add to `/home/admin/commoncloud/.env`:

```bash
# RSSHub access key (prevents unauthorized use)
RSSHUB_ACCESS_KEY=<generate-a-random-key>
```

Generate with: `openssl rand -hex 32`

---

## 5. Miniflux Feed URLs

Once deployed, add these feeds to Miniflux (feeds.cloudpublica.org). The `key` parameter is the ACCESS_KEY value.

### Threads Profiles

RSSHub Threads route format: `/threads/<username>`

| Feed | Miniflux URL |
|------|-------------|
| kristinesocall (Threads) | `https://rsshub.cloudpublica.org/threads/kristinesocall?key=YOUR_ACCESS_KEY` |

### Adding Other Profiles Later

Replace the username in the URL pattern:

```
https://rsshub.cloudpublica.org/threads/{username}?key=YOUR_ACCESS_KEY
```

### Other Useful Routes (examples)

```
# Instagram user posts
https://rsshub.cloudpublica.org/instagram/user/{username}?key=YOUR_ACCESS_KEY

# Reddit subreddit
https://rsshub.cloudpublica.org/reddit/subreddit/{subreddit}?key=YOUR_ACCESS_KEY

# Twitter/X user timeline
https://rsshub.cloudpublica.org/twitter/user/{username}?key=YOUR_ACCESS_KEY

# GitHub repo releases
https://rsshub.cloudpublica.org/github/release/{owner}/{repo}?key=YOUR_ACCESS_KEY
```

Full route directory: https://docs.rsshub.app/routes/

---

## 6. Deployment Steps

```bash
# 1. SSH to server
ssh aws-docker

# 2. Backup
cp ~/commoncloud/docker-compose.yml ~/commoncloud/docker-compose.yml.bak

# 3. Edit docker-compose.yml — add rsshub + rsshub-redis services (section 1 above)
# 4. Edit docker-compose.yml — add rsshub_redis_data to volumes section
# 5. Edit docker-compose.yml — add rsshub to nginx depends_on list
# 6. Create nginx config
#    Copy rsshub.conf content (section 2 above) to:
#    ~/commoncloud/nginx/conf.d/rsshub.conf

# 7. Generate and set access key
RSSHUB_KEY=$(openssl rand -hex 32)
echo "RSSHUB_ACCESS_KEY=$RSSHUB_KEY" >> ~/commoncloud/.env

# 8. Deploy
cd ~/commoncloud
sudo docker compose up -d rsshub rsshub-redis
sudo docker compose restart nginx
sudo docker compose ps

# 9. Test health check
curl -f http://localhost:1200/healthz

# 10. Add DNS record in Cloudflare dashboard (section 3 above)

# 11. Test externally (after DNS propagates)
curl https://rsshub.cloudpublica.org/healthz

# 12. Test a feed
curl "https://rsshub.cloudpublica.org/threads/kristinesocall?key=$RSSHUB_KEY"

# 13. Add feed to Miniflux via API or web UI
```

---

## 7. Resource Impact

| Component | Memory Limit | CPU Limit | Notes |
|-----------|-------------|-----------|-------|
| rsshub | 512M | 0.5 | Node.js app; no Puppeteer |
| rsshub-redis | 128M | 0.25 | Cache only, small dataset |
| **Total** | **640M** | **0.75** | Lightweight addition |

If Threads or Instagram routes require JavaScript rendering, switch to the `chromium-bundled` image variant (will need ~1.5G memory instead of 512M).

---

## 8. Notes

- **Why separate Redis?** The existing Miniflux stack doesn't use Redis. The main `redis` container in docker-compose is used by Statamic/billing. Using a dedicated `rsshub-redis` avoids namespace collisions and keeps services isolated.
- **ACCESS_KEY is critical.** Without it, anyone can use our instance as a proxy to scrape social media, which would get our server IP blocked.
- **Cache TTL set to 900s (15min)** to match Miniflux's polling interval. No point fetching more often than Miniflux checks.
- **No Browserless/Puppeteer initially.** Most routes work without it. If specific routes fail, upgrade to `diygod/rsshub:chromium-bundled` and increase memory limit.
- **Some routes may require API keys** (Twitter, Instagram). Check RSSHub docs for route-specific env vars if feeds return errors.
