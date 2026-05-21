# HumanEnerDIA Full Stack for Industrial Energy Management

## Short Description

HumanEnerDIA Full Stack is a self-hosted deployment bundle for industrial
energy management. It includes the HumanEnerDIA EnMS platform together with the
OVOS runtime and skill for natural-language energy queries.

## Product Type

Digital download, free/open distribution for the initial WASABI release.

## Includes

- Unified portal
- Analytics service
- PostgreSQL + TimescaleDB initialization
- Grafana dashboards
- MQTT and Node-RED pipeline
- Authentication service
- Simulator and chatbot components
- Embedded OVOS runtime and HumanEnerDIA OVOS skill source

## Requirements

- Linux server or workstation
- Docker Engine and Docker Compose
- Enough RAM and disk for a multi-service stack
- Buyer-provided secrets in `.env`
- Optional Qwen GGUF model only when local Tier-3 LLM fallback is enabled

## Installation Summary

1. Extract `HumanEnerDIA-full-stack-v1.0.0.tar.gz`
2. Copy `.env.example` to `.env`
3. Fill the required values
4. Run `./setup.sh`
5. Verify portal, Grafana, and OVOS health endpoints
6. Run a smoke query through the OVOS bridge

The base bundle keeps `INSTALL_LLM_FALLBACK=false` so the install remains
lighter. Buyers who want local Qwen fallback can provide
`Qwen3.5-2B-Q4_K_M.gguf`, set `INSTALL_LLM_FALLBACK=true`, and rebuild the
OVOS image.

## License/IPR

The HumanEnerDIA backend/full-stack repository is distributed under the MIT
License. The bundled OVOS component remains `Apache-2.0 OR GPL-3.0-or-later`.
Third-party services keep their own upstream licenses.

## Known Limitations

This artifact is designed as a guided deployment bundle for evaluation and
integration. Production hardening still requires buyer-specific secrets, DNS,
TLS, backups, and infrastructure review.

The `query-service` container is currently a reserved placeholder and is not
part of release health expectations.
