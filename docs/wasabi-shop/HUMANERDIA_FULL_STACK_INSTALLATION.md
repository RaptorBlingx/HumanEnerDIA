# HumanEnerDIA Full Stack Installation

This guide is for the WASABI full-stack product that bundles the HumanEnerDIA
platform together with the OVOS runtime and skill.

## Requirements

- Linux server with Docker Engine 20.10+ and Docker Compose v2
- 8 GB RAM recommended
- 15 GB free disk space recommended
- Open ports for the web UI, Grafana, Node-RED, OVOS bridge, and any optional
  external services you want to expose

## Bundle Layout

After extraction, the bundle root contains:

- `docker-compose.yml` for the HumanEnerDIA stack
- `docker-compose.ovos.yml` for the embedded OVOS service
- `ovos-stack/` with the OVOS runtime and skill source
- `INSTALL.md` and `PRODUCT.md`
- `.env.example`

## Guided Deployment

1. Extract the archive:

   ```bash
   tar -xzf HumanEnerDIA-full-stack-v1.0.0.tar.gz
   cd HumanEnerDIA-full-stack-v1.0.0
   ```

2. Create your environment file:

   ```bash
   cp .env.example .env
   ```

3. Update at least these values in `.env`:

   - `POSTGRES_PASSWORD`
   - `GRAFANA_ADMIN_PASSWORD`
   - `NODE_RED_CREDENTIAL_SECRET`
   - `NODE_RED_PASSWORD_HASH`
   - `REDIS_PASSWORD`
   - `MQTT_PASSWORD`
   - `JWT_SECRET`
   - `API_KEY`
   - `FRONTEND_URL`

4. Optional for side-by-side deployments on one host:

   - `CONTAINER_PREFIX`
   - `VOLUME_PREFIX`
   - `ENMS_NETWORK_NAME`
   - all host port variables such as `NGINX_HTTP_PORT`, `AUTH_SERVICE_EXTERNAL_PORT`,
     `MQTT_EXTERNAL_PORT`, `OVOS_BRIDGE_EXTERNAL_PORT`, and `OVOS_MESSAGEBUS_PORT`
   - `INSTALL_LLM_FALLBACK=true` only if you will also provide the optional Qwen GGUF model

5. Start the stack:

   ```bash
   ./setup.sh
   ```

   Manual equivalent:

   ```bash
   docker compose -f docker-compose.yml -f docker-compose.ovos.yml build
   docker compose -f docker-compose.yml -f docker-compose.ovos.yml up -d
   ```

6. Optional Qwen fallback:

   - keep the default `INSTALL_LLM_FALLBACK=false` for the leanest base install
   - if you want Tier-3 local LLM fallback, place `Qwen3.5-2B-Q4_K_M.gguf` under
     `ovos-stack/enms-ovos-skill/models/`
   - set `INSTALL_LLM_FALLBACK=true`
   - rebuild the OVOS image:

   ```bash
   docker compose -f docker-compose.yml -f docker-compose.ovos.yml build ovos
   docker compose -f docker-compose.yml -f docker-compose.ovos.yml up -d ovos
   ```

## Verification

Check the main services:

```bash
curl -fsS http://localhost:8080/health
curl -fsS http://localhost:8001/api/v1/health
curl -fsS http://localhost:5000/health
```

Run one live OVOS smoke query:

```bash
curl -sS -X POST http://localhost:5000/query \
  -H 'Content-Type: application/json' \
  -d '{"text":"what is the power of compressor one","session_id":"bundle-smoke"}'
```

## Notes

- This is a guided deployment bundle, not a one-click appliance.
- The bundle excludes trained analytics models, OVOS GGUF model files, caches,
  live credentials, and Docker volumes.
- The OVOS image skips `llama-cpp-python` by default. That keeps the base install
  lighter, and the local Qwen fallback can be enabled later if needed.
- For production exposure, add DNS, TLS, backup policy, and host-level
  monitoring after the initial deployment works locally.
