# HumanEnerDIA Full Stack Installation

This guide is for the WASABI full-stack product that bundles the HumanEnerDIA
platform together with the OVOS runtime and skill.

## Requirements

- Linux server or workstation
- Docker Engine 20.10+ and Docker Compose v2
- 8 GB RAM recommended
- 15 GB free disk space recommended
- Network access for pulling Docker images during first startup

No manual secret editing is required for a local evaluation install. The setup
helper creates `.env`, generates first-run secrets, validates Docker Compose,
builds the images, and starts the stack.

## Bundle Layout

After extraction, the bundle root contains:

- `docker-compose.yml` for the HumanEnerDIA stack
- `docker-compose.ovos.yml` for the embedded OVOS service
- `ovos-stack/` with the OVOS runtime and skill source
- `setup.sh`
- `scripts/verify-wasabi-release.sh`
- `INSTALL.md` and `PRODUCT.md`
- `.env.example`

## Zero-Touch Evaluation Deployment

1. Extract the archive:

   ```bash
   tar -xzf HumanEnerDIA-full-stack-v1.0.0.tar.gz
   cd HumanEnerDIA-full-stack-v1.0.0
   ```

2. Start the full stack:

   ```bash
   ./setup.sh
   ```

   For access from another machine, pass the host name or IP that users will
   type in the browser:

   ```bash
   ./setup.sh --server-ip energy-demo.local
   ```

3. Wait for Docker Compose to finish, then open:

   - Portal: `http://localhost:8080`
   - Grafana: `http://localhost:8080/grafana`
   - Analytics health: `http://localhost:8001/api/v1/health`
   - OVOS bridge health: `http://localhost:5000/health`

Generated first-run credentials are stored in `.env`. Keep that file private.

## Verification

Run the bundled verifier:

```bash
./scripts/verify-wasabi-release.sh --skip-shop
```

Manual checks:

```bash
curl -fsS http://localhost:8080/health
curl -fsS http://localhost:8001/api/v1/health
curl -fsS http://localhost:5000/health
curl -sS -X POST http://localhost:5000/query \
  -H 'Content-Type: application/json' \
  -d '{"text":"what is the power of compressor one","session_id":"bundle-smoke"}'
```

Expected result:

- the Nginx health endpoint returns `healthy`
- analytics returns JSON with `"status":"healthy"`
- the OVOS bridge reports `messagebus_connected: true`
- the smoke query returns `success: true` and a response about `Compressor-1`

## Manual Equivalent

Use this only when you intentionally want to bypass `setup.sh`:

```bash
cp .env.example .env
# Fill every <CHANGE_ME...> value before starting.
docker compose -f docker-compose.yml -f docker-compose.ovos.yml config
docker compose -f docker-compose.yml -f docker-compose.ovos.yml build
docker compose -f docker-compose.yml -f docker-compose.ovos.yml up -d
```

## Optional Qwen Fallback

The base bundle keeps `INSTALL_LLM_FALLBACK=false` so the install remains
lighter. If you want Tier-3 local LLM fallback:

1. Place `Qwen3.5-2B-Q4_K_M.gguf` under
   `ovos-stack/enms-ovos-skill/models/`.
2. Set `INSTALL_LLM_FALLBACK=true` in `.env`.
3. Rebuild the OVOS image:

   ```bash
   docker compose -f docker-compose.yml -f docker-compose.ovos.yml build ovos
   docker compose -f docker-compose.yml -f docker-compose.ovos.yml up -d ovos
   ```

## Production Notes

- Rotate the generated `.env` secrets before production exposure.
- Set DNS and TLS-specific URLs.
- Review exposed ports, firewall rules, backup policy, and host monitoring.
- The bundle excludes live `.env` files, Docker volumes, analytics saved
  models, OVOS GGUF model files, caches, and logs.
- The `query-service` container is a reserved placeholder and is not part of
  release health expectations.
