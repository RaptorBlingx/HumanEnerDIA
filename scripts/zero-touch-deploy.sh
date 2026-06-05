#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SERVER_IP="${1:-${SERVER_IP:-localhost}}"

env_value() {
  local key="$1"
  local default="$2"
  local value

  value="$(grep -E "^${key}=" .env 2>/dev/null | tail -n 1 | cut -d= -f2- || true)"
  printf '%s' "${value:-$default}"
}

echo "=============================================="
echo "  HumanEnerDIA Zero-Touch Deployment"
echo "=============================================="
echo

./setup.sh --server-ip "$SERVER_IP"

if [[ -x ./scripts/verify-wasabi-release.sh ]]; then
  HUMANERDIA_BASE_URL="http://${SERVER_IP}:$(env_value NGINX_HTTP_PORT 8080)" \
  ANALYTICS_BASE_URL="http://${SERVER_IP}:$(env_value ANALYTICS_PORT 8001)" \
  OVOS_BASE_URL="http://${SERVER_IP}:$(env_value OVOS_BRIDGE_EXTERNAL_PORT 5000)" \
    ./scripts/verify-wasabi-release.sh --skip-shop
fi

echo
echo "Deployment complete."
