#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

HUMANERDIA_BASE_URL="${HUMANERDIA_BASE_URL:-http://localhost:8080}"
ANALYTICS_BASE_URL="${ANALYTICS_BASE_URL:-http://localhost:8001}"
OVOS_BASE_URL="${OVOS_BASE_URL:-http://localhost:5000}"
WASABI_BASE_URL="${WASABI_BASE_URL:-http://10.33.10.104:18080}"
SKIP_SHOP=false

checksum_or_default() {
  local checksum_file="$1"
  local default="$2"

  if [[ -r "$checksum_file" ]]; then
    awk '{print $1; exit}' "$checksum_file"
  else
    printf '%s\n' "$default"
  fi
}

OVOS_ARTIFACT_SHA256="${OVOS_ARTIFACT_SHA256:-$(checksum_or_default "/home/ubuntu/ovos-llm/releases/HumanEnerDIA-OVOS-skill-v1.0.0.zip.sha256" "27ae856288e594e095bf83ac916ddcd6a07ec11161605cf04824b980f0815711")}"
FULL_STACK_ARTIFACT_SHA256="${FULL_STACK_ARTIFACT_SHA256:-$(checksum_or_default "$ROOT_DIR/releases/HumanEnerDIA-full-stack-v1.0.0.tar.gz.sha256" "5d3a2ba1689ab34c61b9045fdf44db7aeb29c0359134ed311829a39d7db67bfd")}"

usage() {
  cat <<'EOF'
Usage: scripts/verify-wasabi-release.sh [--skip-shop] [--shop-url URL]

Environment overrides:
  HUMANERDIA_BASE_URL  default http://localhost:8080
  ANALYTICS_BASE_URL   default http://localhost:8001
  OVOS_BASE_URL        default http://localhost:5000
  WASABI_BASE_URL      default http://10.33.10.104:18080
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-shop)
      SKIP_SHOP=true
      shift
      ;;
    --shop-url)
      WASABI_BASE_URL="${2:?--shop-url requires a URL}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

require_command() {
  local command_name="$1"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing required command: $command_name" >&2
    exit 1
  fi
}

pass() {
  printf '[OK] %s\n' "$1"
}

fetch() {
  local url="$1"
  local out="$2"
  curl -fsSL --max-time 30 "$url" -o "$out"
}

assert_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if grep -Eiq "$pattern" "$file"; then
    pass "$label"
  else
    echo "[FAIL] $label" >&2
    echo "Missing pattern: $pattern" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if grep -Eiq "$pattern" "$file"; then
    echo "[FAIL] $label" >&2
    grep -Ein "$pattern" "$file" >&2 || true
    exit 1
  fi
  pass "$label"
}

require_command curl
require_command grep

echo "HumanEnerDIA release verification"
echo "HumanEnerDIA: $HUMANERDIA_BASE_URL"
echo "Analytics:    $ANALYTICS_BASE_URL"
echo "OVOS:         $OVOS_BASE_URL"
echo

if command -v docker >/dev/null 2>&1 && [[ -f docker-compose.yml ]]; then
  compose_files=(-f docker-compose.yml)
  if [[ -f docker-compose.ovos.yml ]]; then
    compose_files+=(-f docker-compose.ovos.yml)
  elif [[ -f scripts/release/docker-compose.ovos.yml && -d ovos-stack ]]; then
    compose_files+=(-f scripts/release/docker-compose.ovos.yml)
  fi
  docker compose "${compose_files[@]}" config --quiet
  pass "Docker Compose config validates"
fi

tmpdir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmpdir"
}
trap cleanup EXIT

fetch "$HUMANERDIA_BASE_URL/health" "$tmpdir/humanerdia-health.txt"
assert_contains "$tmpdir/humanerdia-health.txt" '^healthy$' "Nginx health endpoint"

fetch "$ANALYTICS_BASE_URL/api/v1/health" "$tmpdir/analytics-health.json"
assert_contains "$tmpdir/analytics-health.json" '"status"[[:space:]]*:[[:space:]]*"healthy"' "Analytics health endpoint"

fetch "$OVOS_BASE_URL/health" "$tmpdir/ovos-health.json"
assert_contains "$tmpdir/ovos-health.json" '"status"[[:space:]]*:[[:space:]]*"healthy"' "OVOS bridge health endpoint"
assert_contains "$tmpdir/ovos-health.json" '"messagebus_connected"[[:space:]]*:[[:space:]]*true' "OVOS messagebus connection"

curl -fsS --max-time 95 \
  -X POST "$OVOS_BASE_URL/query" \
  -H 'Content-Type: application/json' \
  -d '{"text":"what is the power of compressor one","session_id":"wasabi-release-verify"}' \
  -o "$tmpdir/ovos-query.json"
assert_contains "$tmpdir/ovos-query.json" '"success"[[:space:]]*:[[:space:]]*true' "OVOS smoke query"
assert_contains "$tmpdir/ovos-query.json" 'Compressor-1|compressor one|machine_status' "OVOS smoke query content"

if [[ "$SKIP_SHOP" != "true" ]]; then
  echo
  echo "WASABI shop: $WASABI_BASE_URL"

  fetch "$WASABI_BASE_URL/" "$tmpdir/shop-home.html"
  fetch "$WASABI_BASE_URL/12-skills" "$tmpdir/shop-skills.html"
  fetch "$WASABI_BASE_URL/skills/38-humanenerdia-ovos-skill-for-industrial-energy-management.html" "$tmpdir/shop-ovos.html"
  fetch "$WASABI_BASE_URL/skills/39-humanenerdia-full-stack-for-industrial-energy-management.html" "$tmpdir/shop-fullstack.html"

  assert_contains "$tmpdir/shop-home.html" 'HumanEnerDIA Full Stack|HumanEnerDIA OVOS Skill' "Shop homepage HumanEnerDIA signals"
  assert_contains "$tmpdir/shop-skills.html" 'There are 2 products|HumanEnerDIA OVOS Skill' "Skills category has products"
  assert_contains "$tmpdir/shop-skills.html" 'HumanEnerDIA Full Stack for Industrial Energy Management' "Full-stack product listed"
  assert_contains "$tmpdir/shop-skills.html" 'HumanEnerDIA OVOS Skill for Industrial Energy Management' "OVOS product listed"
  assert_contains "$tmpdir/shop-ovos.html" 'Apache-2.0 OR GPL-3.0-or-later' "OVOS product license copy"
  assert_contains "$tmpdir/shop-ovos.html" "$OVOS_ARTIFACT_SHA256" "OVOS product checksum"
  assert_contains "$tmpdir/shop-fullstack.html" 'MIT License' "Full-stack product license copy"
  assert_contains "$tmpdir/shop-fullstack.html" "$FULL_STACK_ARTIFACT_SHA256" "Full-stack product checksum"
  assert_contains "$tmpdir/shop-ovos.html" 'Add to cart|Available as digital download' "OVOS product checkout signals"
  assert_contains "$tmpdir/shop-fullstack.html" 'Add to cart|Available as full stack digital download' "Full-stack product checkout signals"

  cat "$tmpdir"/shop-*.html > "$tmpdir/shop-all.html"
  assert_not_contains "$tmpdir/shop-all.html" 'Lorem ipsum|info@sizeyou|Via Corradino|seller@wasabi\.test|Mohamad Jarad|value="Array"' "Shop stale-text scan"
fi

echo
echo "Verification passed."
