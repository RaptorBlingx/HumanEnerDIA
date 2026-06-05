# HumanEnerDIA Clean Machine E2E Runbook

This runbook validates the two HumanEnerDIA WASABI shop products from the
perspective of a new end user:

- Product 38: `HumanEnerDIA OVOS Skill for Industrial Energy Management`
- Product 39: `HumanEnerDIA Full Stack for Industrial Energy Management`

Use it for release acceptance, buyer support, and clean-machine smoke testing.

## Preconditions

- A Linux host or VM with Docker Engine 20.10+ and Docker Compose v2.
- Network access to pull Docker images.
- The downloaded product artifact and its `.sha256` file from the WASABI shop.
- For the OVOS-skill-only experiment, a reachable HumanEnerDIA/EnMS analytics
  API endpoint.

## Product 39: Full Stack

This is the zero-touch path. After Docker is available, the buyer should not
need to manually edit `.env` for a local evaluation deployment.

1. Verify the downloaded archive:

   ```bash
   sha256sum -c HumanEnerDIA-full-stack-v1.0.0.tar.gz.sha256
   ```

2. Extract and start:

   ```bash
   tar -xzf HumanEnerDIA-full-stack-v1.0.0.tar.gz
   cd HumanEnerDIA-full-stack-v1.0.0
   ./setup.sh
   ```

   For remote browser access, pass the public host name or IP:

   ```bash
   ./setup.sh --server-ip energy-demo.local
   ```

3. Run the bundled verifier:

   ```bash
   ./scripts/verify-wasabi-release.sh --skip-shop
   ```

4. Open the main endpoints:

   - Portal: `http://localhost:8080`
   - Grafana: `http://localhost:8080/grafana`
   - Analytics health: `http://localhost:8001/api/v1/health`
   - OVOS bridge health: `http://localhost:5000/health`
   - Simulator docs: `http://localhost:8080/api/simulator/docs`

5. Run a direct OVOS query:

   ```bash
   curl -sS -X POST http://localhost:5000/query \
     -H 'Content-Type: application/json' \
     -d '{"text":"what is the power of compressor one","session_id":"full-stack-e2e"}'
   ```

Expected outcome:

- `./setup.sh` creates `.env`, generates secrets, validates Compose, builds,
  and starts the HumanEnerDIA and OVOS services.
- Nginx returns `healthy`.
- Analytics returns JSON with `"status":"healthy"`.
- OVOS health reports `messagebus_connected: true`.
- The query returns `success: true` and a response about `Compressor-1`.

## Product 38: OVOS Skill Only

The OVOS skill ZIP is intentionally smaller than the full-stack product. It
contains the skill artifact, not the HumanEnerDIA backend and not a complete
OVOS runtime. A clean-machine test therefore needs one of these contexts:

- an existing OVOS runtime plus a reachable HumanEnerDIA backend, or
- the companion OVOS Docker repository, pointed at a reachable backend.

### Option A: Companion OVOS Docker Runtime

Use this when the tester wants a clean-machine container experiment for the
OVOS layer only.

1. Start or identify a HumanEnerDIA backend. For a local full-stack backend, the
   analytics endpoint is normally `http://localhost:8001/api/v1`.

2. Clone and configure the OVOS runtime:

   ```bash
   git clone https://github.com/RaptorBlingx/ovos-llm.git
   cd ovos-llm
   cp .env.example .env
   sed -i 's|^ENMS_API_URL=.*|ENMS_API_URL=http://host.docker.internal:8001/api/v1|' .env
   docker network create enms-network || true
   docker compose build
   docker compose up -d
   ```

   If the backend is on the same Docker network, use:

   ```bash
   sed -i 's|^ENMS_API_URL=.*|ENMS_API_URL=http://enms-analytics:8001/api/v1|' .env
   ```

3. Verify:

   ```bash
   curl -fsS http://localhost:5000/health
   curl -sS -X POST http://localhost:5000/query \
     -H 'Content-Type: application/json' \
     -d '{"text":"what is the power of compressor one","session_id":"ovos-docker-e2e"}'
   ```

### Option B: Existing OVOS Runtime

Use this when the buyer already runs OVOS and only needs to install the
HumanEnerDIA skill from the WASABI ZIP.

1. Verify and extract the downloaded ZIP:

   ```bash
   sha256sum -c HumanEnerDIA-OVOS-skill-v1.0.0.zip.sha256
   unzip HumanEnerDIA-OVOS-skill-v1.0.0.zip -d HumanEnerDIA-OVOS-skill-v1.0.0
   cd HumanEnerDIA-OVOS-skill-v1.0.0
   ```

2. Install the skill:

   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   python -m pip install -U pip
   python -m pip install -e .
   ```

3. Configure the backend URL in the OVOS skill settings for the runtime:

   ```json
   {
     "enms_api_base_url": "http://YOUR_ENMS_HOST:8001/api/v1",
     "api_timeout_seconds": 30
   }
   ```

4. Start the OVOS runtime and REST bridge used by that installation.

5. Verify:

   ```bash
   curl -fsS http://localhost:5000/health
   curl -sS -X POST http://localhost:5000/query \
     -H 'Content-Type: application/json' \
     -d '{"text":"what is the power of compressor one","session_id":"ovos-skill-e2e"}'
   ```

Expected outcome:

- The REST bridge reports healthy with the messagebus connected.
- The query returns `success: true`.
- The response references `Compressor-1` or a matching machine-status result.

## WASABI Shop Acceptance

Run this from the HumanEnerDIA repository on the maintainer host:

```bash
cd /home/ubuntu/humanergy
./scripts/verify-wasabi-release.sh --shop-url http://10.33.10.104:18080
```

The verifier checks:

- Docker Compose config for the current full-stack bundle.
- Portal, analytics, and OVOS health endpoints.
- A live OVOS smoke query.
- The WASABI home page, skills category, and both product pages.
- Published product license text and SHA256 checksums.
- Basic checkout/download signals.
- A stale-text scan for old placeholder shop content.

## Maintainer Rebuild And Republish

Use this when the source tree changes and product 39 needs to be refreshed in
the WASABI shop.

```bash
cd /home/ubuntu/humanergy
./scripts/package_wasabi_full_stack.sh 1.0.0

cd /home/ubuntu/wasabi
./tools/publish_humanerdia_catalog.sh full-stack

cd /home/ubuntu/humanergy
./scripts/verify-wasabi-release.sh --shop-url http://10.33.10.104:18080
```

For product 38, rebuild from the OVOS repository:

```bash
cd /home/ubuntu/ovos-llm
./scripts/package_wasabi_release.sh 1.0.0

cd /home/ubuntu/wasabi
./tools/publish_humanerdia_catalog.sh ovos-skill
```

## Troubleshooting

Useful commands:

```bash
docker compose ps
docker compose logs -f --tail=100 analytics
docker compose logs -f --tail=100 ovos
docker compose logs -f --tail=100 nginx
```

Common causes:

- Docker is not running.
- A required port is already in use.
- The OVOS-only experiment points `ENMS_API_URL` at an unreachable backend.
- A production host still needs DNS/TLS and firewall rules after the local
  zero-touch install succeeds.

## Remote Branch Note

During the 2026-06-05 release-readiness pass, `main` was already aligned with
`forgejo/main` and `github/main`. The remote branch
`feat/simulated-pilot-identity-alignment` had newer pilot-work commits, but it
diverged from the WASABI release path and would remove release/shop docs if
merged directly. Keep that branch separate unless a dedicated pilot merge is
reviewed.
