#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_ROOT="${APP_ROOT:-/home/ubuntu/HumanEnerDIA-Prod-staging}"
OVOS_ROOT="${OVOS_ROOT:-/home/ubuntu/ovos-llm}"
VERSION="${1:-1.0.0}"
RELEASE_DIR="$ROOT_DIR/releases"
ARTIFACT_BASE="HumanEnerDIA-full-stack-v${VERSION}"
ARTIFACT_PATH="$RELEASE_DIR/${ARTIFACT_BASE}.tar.gz"
CHECKSUM_PATH="${ARTIFACT_PATH}.sha256"
NOTES_PATH="$RELEASE_DIR/${ARTIFACT_BASE}-release-notes.md"
STAGE_ROOT="$(mktemp -d)"
BUNDLE_DIR="$STAGE_ROOT/${ARTIFACT_BASE}"

cleanup() {
  rm -rf "$STAGE_ROOT"
}
trap cleanup EXIT

if [[ ! -d "$OVOS_ROOT/enms-ovos-skill" ]]; then
  echo "OVOS source directory not found: $OVOS_ROOT" >&2
  exit 1
fi

if [[ ! -f "$APP_ROOT/docker-compose.yml" ]]; then
  APP_ROOT="$ROOT_DIR"
fi

mkdir -p "$RELEASE_DIR" "$BUNDLE_DIR"

copy_humanergy_dir() {
  local src="$1"
  local dest="$2"
  shift 2
  rsync -a \
    --exclude '.git/' \
    --exclude '.gitignore' \
    --exclude '.gitkeep' \
    --exclude '.env' \
    --exclude '__pycache__/' \
    --exclude '.pytest_cache/' \
    --exclude 'tests/' \
    --exclude 'test_*.py' \
    --exclude '*_test.py' \
    --exclude '*test*.html' \
    --exclude 'htmlcov/' \
    --exclude 'node_modules/' \
    --exclude 'dist/' \
    --exclude 'logs/' \
    --exclude 'cache/' \
    --exclude 'backup/' \
    --exclude 'dashboards-backup/' \
    --exclude 'postgres-data/' \
    --exclude 'README.md' \
    --exclude '*.log' \
    --exclude '*.pyc' \
    --exclude '*.pyo' \
    --exclude '*.dump' \
    --exclude '*.bak' \
    --exclude '*.bak_*' \
    --exclude '*.old' \
    --exclude 'releases/' \
    --exclude 'models/saved/' \
    "$@" \
    "$src" "$dest"
}

copy_ovos_dir() {
  local src="$1"
  local dest="$2"
  rsync -a \
    --exclude '.git/' \
    --exclude '.gitignore' \
    --exclude '.gitkeep' \
    --exclude '.env' \
    --exclude 'docs/' \
    --exclude 'scripts/' \
    --exclude 'tests/' \
    --exclude 'enms_ovos_skill/tests/' \
    --exclude '__pycache__/' \
    --exclude '.pytest_cache/' \
    --exclude 'pytest.ini' \
    --exclude 'test_*.py' \
    --exclude '*_test.py' \
    --exclude '*.phase*' \
    --exclude '*.pre-*' \
    --exclude 'run_gui.sh' \
    --exclude 'bridge/README.md' \
    --exclude 'bridge/pdf_download_example.html' \
    --exclude 'bridge/test_*' \
    --exclude 'bridge/*windows*' \
    --exclude 'bridge/*wsl*' \
    --exclude 'bridge/*.bat' \
    --exclude 'bridge/hey_mycroft.tflite' \
    --exclude 'htmlcov/' \
    --exclude 'logs/' \
    --exclude 'releases/' \
    --exclude 'models/' \
    --exclude '*.log' \
    --exclude '*.pyc' \
    "$src" "$dest"
}

install -m 644 "$APP_ROOT/LICENSE" "$BUNDLE_DIR/LICENSE"
install -m 755 "$APP_ROOT/setup.sh" "$BUNDLE_DIR/setup.sh"
install -m 644 "$APP_ROOT/docker-compose.yml" "$BUNDLE_DIR/docker-compose.yml"
install -m 644 "$ROOT_DIR/scripts/release/docker-compose.ovos.yml" "$BUNDLE_DIR/docker-compose.ovos.yml"
install -m 644 "$ROOT_DIR/docs/wasabi-shop/HUMANERDIA_FULL_STACK_INSTALLATION.md" "$BUNDLE_DIR/INSTALL.md"
install -m 644 "$ROOT_DIR/docs/wasabi-shop/HUMANERDIA_FULL_STACK_WASABI_SHOP_PRODUCT.md" "$BUNDLE_DIR/PRODUCT.md"
install -m 755 "$ROOT_DIR/scripts/verify-wasabi-release.sh" "$BUNDLE_DIR/verify-release.sh"

cat > "$BUNDLE_DIR/README.md" <<EOF
# HumanEnerDIA Full Stack v${VERSION}

Production evaluation bundle for the HumanEnerDIA industrial energy-management
stack with an embedded OVOS runtime and skill.

## Start

\`\`\`bash
./setup.sh
./verify-release.sh
\`\`\`

For remote browser access:

\`\`\`bash
./setup.sh --server-ip <host-or-ip>
\`\`\`

Read \`INSTALL.md\` for the complete end-user deployment guide. Generated
first-run credentials are stored in \`.env\`; rotate them before production
exposure.
EOF

cp "$APP_ROOT/.env.example" "$BUNDLE_DIR/.env.example"
sed -i \
  -e 's/^OVOS_BRIDGE_HOST=.*/OVOS_BRIDGE_HOST=ovos/' \
  -e 's|^FRONTEND_URL=.*|FRONTEND_URL=https://your-humanerdia-domain.example|' \
  "$BUNDLE_DIR/.env.example"

copy_humanergy_dir "$APP_ROOT/analytics/" "$BUNDLE_DIR/analytics/"
copy_humanergy_dir "$APP_ROOT/auth-service/" "$BUNDLE_DIR/auth-service/"
copy_humanergy_dir "$APP_ROOT/chatbot/" "$BUNDLE_DIR/chatbot/" \
  --exclude '/rasa/models/components/' \
  --exclude '/rasa/models/metadata.json' \
  --exclude '/rasa/tests/' \
  --exclude '/models/' \
  --exclude 'dist/'

mkdir -p "$BUNDLE_DIR/database"
copy_humanergy_dir "$APP_ROOT/database/init/" "$BUNDLE_DIR/database/init/"
install -m 644 "$APP_ROOT/database/postgresql.conf" "$BUNDLE_DIR/database/postgresql.conf"

copy_humanergy_dir "$APP_ROOT/grafana/" "$BUNDLE_DIR/grafana/"
copy_humanergy_dir "$APP_ROOT/mqtt/" "$BUNDLE_DIR/mqtt/"
copy_humanergy_dir "$APP_ROOT/nginx/" "$BUNDLE_DIR/nginx/"
copy_humanergy_dir "$APP_ROOT/nodered/" "$BUNDLE_DIR/nodered/" \
  --exclude 'data/.npm/' \
  --exclude 'data/projects/.sshkeys/' \
  --exclude 'data/*.backup'
copy_humanergy_dir "$APP_ROOT/portal/" "$BUNDLE_DIR/portal/" \
  --exclude 'public/pilot-*' \
  --exclude 'public/admin/pilot-*' \
  --exclude 'public/js/*pilot*'
copy_humanergy_dir "$APP_ROOT/simulator/" "$BUNDLE_DIR/simulator/"

mkdir -p "$BUNDLE_DIR/ovos-stack"
for file in Dockerfile docker-compose.yml ovos.conf requirements.txt requirements-llm.txt setup.sh supervisord.conf README.md; do
  install -m 644 "$OVOS_ROOT/$file" "$BUNDLE_DIR/ovos-stack/$file"
done
chmod 755 "$BUNDLE_DIR/ovos-stack/setup.sh"
copy_ovos_dir "$OVOS_ROOT/enms-ovos-skill/" "$BUNDLE_DIR/ovos-stack/enms-ovos-skill/"

rm -f "$ARTIFACT_PATH" "$CHECKSUM_PATH" "$NOTES_PATH"
tar -C "$STAGE_ROOT" -czf "$ARTIFACT_PATH" "$ARTIFACT_BASE"
sha256sum "$ARTIFACT_PATH" > "$CHECKSUM_PATH"

{
  echo "# HumanEnerDIA Full Stack v${VERSION} Release Notes"
  echo
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "## WASABI Shop Artifact"
  echo
  echo "- Upload file: \`${ARTIFACT_BASE}.tar.gz\`"
  echo "- SHA256: \`$(cut -d ' ' -f1 "$CHECKSUM_PATH")\`"
  echo "- Product name: HumanEnerDIA Full Stack for Industrial Energy Management"
  echo "- Core license: MIT for HumanEnerDIA backend/full-stack repository"
  echo "- Included OVOS component license: Apache-2.0 OR GPL-3.0-or-later"
  echo
  echo "## Bundle Contents"
  echo
  echo "The archive contains the EnMS backend stack, portal, analytics services,"
  echo "database initialization, dashboards, MQTT pipeline, authentication service,"
  echo "a production verifier, and an embedded OVOS runtime/skill directory under"
  echo "\`ovos-stack/\`."
  echo
  echo "## Exclusions"
  echo
  echo "- Live .env files"
  echo "- Docker runtime volumes and local data"
  echo "- Internal docs, pilot/proposal materials, crawl data, reports, and TODO files"
  echo "- Development, test, backfill, package, release, and maintenance scripts"
  echo "- Unit/integration tests and test fixtures"
  echo "- Grafana dashboard backups and transient backup files"
  echo "- Trained analytics baseline/anomaly models"
  echo "- OVOS GGUF models and caches"
  echo "- node_modules, __pycache__, logs, Git metadata, and release artifacts"
  echo "- The required Rasa runtime model under \`chatbot/rasa/models/\` is retained because the repository does not include a rebuildable training set."
  echo
  echo "## Guided Install"
  echo
  echo "1. Extract the archive"
  echo "2. Run \`./setup.sh\`"
  echo "3. Run \`./verify-release.sh\`"
  echo "4. Optional Qwen fallback: set \`INSTALL_LLM_FALLBACK=true\`, place the GGUF in"
  echo "   \`ovos-stack/enms-ovos-skill/models/\`, and rebuild the OVOS image"
  echo
  echo "\`setup.sh\` creates \`.env\` when needed, generates local first-run secrets,"
  echo "validates Docker Compose, builds the images, and starts the stack. For"
  echo "production, rotate generated secrets and configure DNS/TLS before exposure."
  echo
  echo "## Smoke Checks"
  echo
  echo "\`\`\`bash"
  echo "curl -fsS http://localhost:8080/health"
  echo "curl -fsS http://localhost:8001/api/v1/health"
  echo "curl -fsS http://localhost:5000/health"
  echo "curl -sS -X POST http://localhost:5000/query \\"
  echo "  -H 'Content-Type: application/json' \\"
  echo "  -d '{\"text\":\"what is the power of compressor one\",\"session_id\":\"full-stack-release\"}'"
  echo "\`\`\`"
} > "$NOTES_PATH"

echo "Created $ARTIFACT_PATH"
echo "Created $CHECKSUM_PATH"
echo "Created $NOTES_PATH"
