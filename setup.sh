#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

compose_files=(-f docker-compose.yml)
if [[ -f docker-compose.ovos.yml ]]; then
  compose_files+=(-f docker-compose.ovos.yml)
fi

if [[ ! -f .env && -f .env.example ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

if [[ ! -f .env ]]; then
  echo ".env is required. Copy .env.example and fill the required values first." >&2
  exit 1
fi

if grep -Eq '^[[:space:]]*[^#].*<CHANGE_ME' .env; then
  echo "Placeholder values are still present in .env. Update them before running setup." >&2
  exit 1
fi

docker compose "${compose_files[@]}" build
docker compose "${compose_files[@]}" up -d

echo "Started stack with compose files: ${compose_files[*]}"
