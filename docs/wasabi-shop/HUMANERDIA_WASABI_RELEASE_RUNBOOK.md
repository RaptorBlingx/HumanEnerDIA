# HumanEnerDIA WASABI Shop Release Runbook

This runbook turns the WASABI plan into an operational checklist for publishing
the HumanEnerDIA OVOS skill as a WASABI White Label Shop product.

## 1. Release Artifact

Build the shop upload ZIP from the OVOS repository:

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

## 3. Shop Product

Create a free virtual product:

- Name: `HumanEnerDIA OVOS Skill for Industrial Energy Management`
- Category/tags: digital assistant, OVOS skill, energy management, ISO 50001,
  manufacturing, AI assistant.
- Download: `HumanEnerDIA-OVOS-skill-v1.0.0.zip`
- Additional attachment: release notes and SHA256 checksum.
- Optional model note: the Qwen GGUF model is distributed separately.

Use the product copy in `HUMANERDIA_WASABI_SHOP_PRODUCT.md`.

## 4. Verification

Run these checks before publishing or re-publishing the product:

```bash
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

## 6. Current Release State

As of 2026-05-20, the local WASABI deployment is running on:

- Front office: `http://10.33.10.104:18080/`
- Shop category: `http://10.33.10.104:18080/wasabiSHOP/`
- Product page: `http://10.33.10.104:18080/skills/38-humanenerdia-ovos-skill-for-industrial-energy-management.html`

The HumanEnerDIA product is product id `38`, configured as a free virtual
download, and the order/download flow was verified with order id `14`.

Release backup:

- `/home/ubuntu/release-backups/humanerdia-wasabi-20260520T133402Z`

Before external/public exposure, rotate the GitLab access token that was used
during cloning and add DNS/TLS routing for the final shop domain.
