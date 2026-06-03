# Production deployment

Target: a single small VPS running everything for **~$20–40/month**.

## Recommended VPS

For Cambodia, latency matters. Cheapest good options:

- **Hetzner CCX13** (Singapore) — $13/mo, 2 vCPU, 8 GB RAM
- **Vultr Cloud Compute** (Singapore) — $12/mo, 2 vCPU, 4 GB RAM
- **DigitalOcean Premium AMD** (Singapore) — $14/mo, 2 vCPU, 4 GB RAM

LLM costs are separate. DeepSeek at the planned volume (1k searches/day, 100 CVs/day) is ~$5–10/month.

## One-time setup

```bash
# On a fresh Ubuntu 24.04 VPS:
ssh root@<your-vps>

# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone the repo
git clone https://github.com/YOUR-ORG/srokwork-core.git /opt/srokwork-core
cd /opt/srokwork-core

# Configure
cp .env.example .env
nano .env
# Set: APP_ENV=production
#      TELEGRAM_BOT_TOKEN, LLM_API_KEY
#      TELEGRAM_WEBHOOK_URL=https://<your-domain>
#      TELEGRAM_WEBHOOK_SECRET=<random hex>
#      SECRET_KEY=$(openssl rand -hex 32)

# Start
docker compose up -d
docker compose exec api alembic upgrade head
```

## Reverse proxy + TLS

Use Caddy — it handles Let's Encrypt automatically.

```bash
# /etc/caddy/Caddyfile
api.srokwork.org {
    reverse_proxy localhost:8000
}
```

Then `systemctl reload caddy`. Telegram will POST to `https://api.srokwork.org/telegram/webhook`.

## Confirming the webhook is live

```bash
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

Should show your URL with `pending_update_count: 0`.

## Backups

```bash
# Daily Postgres dump
docker compose exec -T postgres pg_dump -U srokwork srokwork | gzip > backup-$(date +%F).sql.gz
```

Put this in cron. Ship to off-host storage (Backblaze B2, Cloudflare R2, or your homelab).

## Monitoring

Minimum viable: a `cron` job that hits `/health` every minute and pages you if it fails. UptimeRobot is free for this. For real metrics, add Prometheus + Grafana in v0.2.

## Scaling notes (when you outgrow one VPS)

- **First bottleneck** is LLM latency, not the VPS. Hosting matters less than picking a fast model.
- **Second** is Postgres. Move it to a managed service (Neon, Supabase) when you exceed ~10k profiles.
- **Third** is the worker — split `arq` into its own container/host when alerts get heavy.

You will not hit any of these in year one.
