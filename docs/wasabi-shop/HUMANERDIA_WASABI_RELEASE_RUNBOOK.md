# HumanEnerDIA WASABI Shop Release Runbook

This runbook turns the WASABI plan into an operational checklist for publishing
two HumanEnerDIA WASABI White Label Shop products:

- the standalone OVOS skill
- the full stack deployment bundle

For overall production delivery criteria, see
[`../DELIVERY_READINESS.md`](../DELIVERY_READINESS.md).

## 1. Release Artifacts

Build the standalone OVOS skill ZIP from the OVOS repository:

```bash
cd /home/ubuntu/ovos-llm
./scripts/package_wasabi_release.sh 1.0.0
```

Upload:

- `/home/ubuntu/ovos-llm/releases/HumanEnerDIA-OVOS-skill-v1.0.0.zip`
- `/home/ubuntu/ovos-llm/releases/HumanEnerDIA-OVOS-skill-v1.0.0.zip.sha256`

Keep the optional Qwen model outside the main ZIP:

- `Qwen3.5-2B-Q4_K_M.gguf`
- `/home/ubuntu/ovos-llm/releases/Qwen3.5-2B-Q4_K_M.gguf.sha256`

Build the full stack deployment bundle from the HumanEnerDIA repository:

```bash
cd /home/ubuntu/humanergy
./scripts/package_wasabi_full_stack.sh 1.0.0
```

Upload:

- `/home/ubuntu/humanergy/releases/HumanEnerDIA-full-stack-v1.0.0.tar.gz`
- `/home/ubuntu/humanergy/releases/HumanEnerDIA-full-stack-v1.0.0.tar.gz.sha256`

Publish both products to WASABI with one command:

```bash
cd /home/ubuntu/wasabi
./tools/publish_humanerdia_catalog.sh all
```

Or publish just one artifact:

```bash
./tools/publish_humanerdia_catalog.sh ovos-skill
./tools/publish_humanerdia_catalog.sh full-stack
```

## 2. WASABI Shop Install

The current server already uses ports `8080`, `8443`, `5000`, `8001`, `8002`,
and related service ports. Run WASABI under a distinct compose project and map
its web port to a temporary non-conflicting port such as `18080`.

```bash
sudo mkdir -p /opt/wasabi-shop
sudo chown "$USER":"$USER" /opt/wasabi-shop
cd /opt/wasabi-shop

# Use an interactive prompt or temporary credential helper. Do not commit tokens.
git clone https://gitlab.com/wasabimarketplace/wasabi.git .

docker compose -p wasabi-shop -f ./Docker/docker-compose.yml up --build -d
docker exec -it wasabi-db sh -c "mysql -u root -proot wasabi < PS-Wasabi-Default.sql"
```

After first login:

- Change the default back-office admin email and password.
- Go to Advanced Parameters -> Performance and enable Apache optimization.
- Verify front office and back office load before adding products.

If the WASABI compose file binds port `80`, adjust the compose override or
reverse proxy so the local test URL is `http://SERVER_IP:18080`.

## 3. Shop Products

Create two free virtual products:

- `HumanEnerDIA OVOS Skill for Industrial Energy Management`
- `HumanEnerDIA Full Stack for Industrial Energy Management`

Recommended category for both current listings: `Skills` (category `12`).

Use these product copy sources:

- `HUMANERDIA_WASABI_SHOP_PRODUCT.md` for the standalone skill
- `HUMANERDIA_FULL_STACK_WASABI_SHOP_PRODUCT.md` for the full stack

## 4. Verification

Run these checks before publishing or re-publishing either product:

```bash
docker compose config
curl -fsS http://localhost:8080/health
curl -fsS http://localhost:8001/api/v1/health
curl -fsS http://localhost:5000/health
curl -sS -X POST http://localhost:5000/query \
  -H 'Content-Type: application/json' \
  -d '{"text":"what is the power of compressor one","session_id":"wasabi-release"}'
```

Known local service notes from the release preparation:

- `ovos-enms`, `enms-nginx`, and `enms-analytics` were healthy.
- `enms-query-service` is a placeholder and is disabled from Docker health
  expectations; do not list it as required for the WASABI skill product.
- `enms-auth-service` uses a Python-based Docker healthcheck. Recreate the
  container after pulling the release-prep compose change, then confirm it is
  healthy before a public web demo that depends on login, admin, or email flows.

## 5. Security

Before upload, confirm the ZIP does not contain:

- `.env`
- SMTP passwords
- GitLab tokens
- private server-only IPs
- cache directories
- model files
- `node_modules`

Rotate any credential that previously appeared in docs or tracked examples.

For the full-stack tarball, run the same exclusion check against the archive and
confirm it does not include `.env`, Git metadata, Docker volumes, `node_modules`,
model caches, analytics saved models, or OVOS GGUF files.

## 6. Current Release State

As of 2026-05-21, the local WASABI deployment is running on:

- Front office: `http://10.33.10.104:18080/`
- Shop category: `http://10.33.10.104:18080/wasabiSHOP/`
- OVOS skill product page: `http://10.33.10.104:18080/skills/38-humanenerdia-ovos-skill-for-industrial-energy-management.html`
- Full stack product page: `http://10.33.10.104:18080/skills/39-humanenerdia-full-stack-for-industrial-energy-management.html`

Current HumanEnerDIA product ids:

- `38` for the OVOS skill bundle
- `39` for the full stack deployment bundle

Both are configured as free virtual downloads.

Release backup:

- `/home/ubuntu/release-backups/humanerdia-wasabi-20260520T133402Z`

Before external/public exposure, rotate the GitLab access token that was used
during cloning and add DNS/TLS routing for the final shop domain.
