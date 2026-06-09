#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RELEASE_DIR="$ROOT_DIR/releases"
VERSION="${1:-1.0.0}"
ARTIFACT_BASE="HumanEnerDIA-EnMS-v${VERSION}"
ARTIFACT_NAME="${ARTIFACT_BASE}.tar.gz"
ARTIFACT_PATH="$RELEASE_DIR/$ARTIFACT_NAME"
NOTES_PATH="$RELEASE_DIR/${ARTIFACT_BASE}-release-notes.md"
STAGE_ROOT="$(mktemp -d)"
BUNDLE_DIR="$STAGE_ROOT/$ARTIFACT_BASE"

cleanup() {
  rm -rf "$STAGE_ROOT"
}
trap cleanup EXIT

mkdir -p "$RELEASE_DIR" "$BUNDLE_DIR"
rm -f "$ARTIFACT_PATH" "$ARTIFACT_PATH.sha256" "$NOTES_PATH"

runtime_paths=(
  .env.example
  LICENSE
  docker-compose.yml
  setup.sh
  analytics
  auth-service
  chatbot
  database
  grafana
  mqtt
  nginx
  nodered
  portal
  simulator
)

(
  cd "$ROOT_DIR"
  git ls-files -z "${runtime_paths[@]}" |
    tar --null -T - -cf - |
    tar -C "$BUNDLE_DIR" -xf -
)

cp "$ROOT_DIR/scripts/release/enms/README.md" "$BUNDLE_DIR/README.md"
cp "$ROOT_DIR/scripts/release/enms/INSTALL.md" "$BUNDLE_DIR/INSTALL.md"
cp "$ROOT_DIR/scripts/release/enms/PRODUCT.md" "$BUNDLE_DIR/PRODUCT.md"
cp "$ROOT_DIR/scripts/release/enms/OVOS_INTEGRATION.md" "$BUNDLE_DIR/OVOS_INTEGRATION.md"
cp "$ROOT_DIR/verify.sh" "$BUNDLE_DIR/verify-release.sh"
chmod 755 "$BUNDLE_DIR/setup.sh" "$BUNDLE_DIR/verify-release.sh"
find "$BUNDLE_DIR" -name '.gitignore' -delete

(
  cd "$STAGE_ROOT"
  tar -czf "$ARTIFACT_PATH" "$ARTIFACT_BASE"
)

sha256sum "$ARTIFACT_PATH" > "$ARTIFACT_PATH.sha256"

{
  echo "# HumanEnerDIA EnMS v${VERSION} Release Notes"
  echo
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "## WASABI Shop Artifact"
  echo
  echo "- Upload file: \`$ARTIFACT_NAME\`"
  echo "- SHA256: \`$(cut -d ' ' -f1 "$ARTIFACT_PATH.sha256")\`"
  echo "- License: MIT"
  echo "- Product name: HumanEnerDIA EnMS for Industrial Energy Management"
  echo
  echo "## Artifact Contents"
  echo
  echo "The archive contains the HumanEnerDIA EnMS platform: portal, analytics API,"
  echo "PostgreSQL/TimescaleDB initialization, Grafana dashboards, MQTT, Node-RED,"
  echo "Redis, authentication service, simulator, Rasa/web chatbot components,"
  echo "setup helper, verifier, and EnMS/OVOS integration documentation."
  echo
  echo "It intentionally excludes the OVOS runtime, OVOS skill source,"
  echo "\`docker-compose.ovos.yml\`, \`ovos-stack/\`, optional GGUF model weights,"
  echo "live environments, Docker volumes, logs, caches, tests, and internal"
  echo "delivery documents."
  echo
  echo "## Guided Install"
  echo
  echo "\`\`\`bash"
  echo "tar -xzf $ARTIFACT_NAME"
  echo "cd $ARTIFACT_BASE"
  echo "./setup.sh"
  echo "./verify-release.sh"
  echo "\`\`\`"
  echo
  echo "## Pair With OVOS"
  echo
  echo "Run the OVOS product separately and point it at:"
  echo
  echo "\`\`\`text"
  echo "http://<enms-host>:8001/api/v1"
  echo "\`\`\`"
  echo
  echo "For same-host OVOS integration, configure EnMS with:"
  echo
  echo "\`\`\`bash"
  echo "./setup.sh --ovos-bridge-host host.docker.internal --ovos-bridge-port 5000"
  echo "\`\`\`"
} > "$NOTES_PATH"

echo "Created $ARTIFACT_PATH"
echo "Created $ARTIFACT_PATH.sha256"
echo "Created $NOTES_PATH"
