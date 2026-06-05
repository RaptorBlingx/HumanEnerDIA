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
- Zero-touch setup helper and release verifier

## Requirements

- Linux server or workstation
- Docker Engine and Docker Compose
- Enough RAM and disk for a multi-service stack
- Optional Qwen GGUF model only when local Tier-3 LLM fallback is enabled

## Installation Summary

1. Extract `HumanEnerDIA-full-stack-v1.0.0.tar.gz`
2. Run `./setup.sh`
3. Verify portal, Grafana, analytics, and OVOS health endpoints
4. Run a smoke query through the OVOS bridge

`setup.sh` creates `.env` when needed and generates first-run secrets for local
evaluation. For production, rotate those generated values, configure DNS/TLS,
and review exposed ports before public use.

The base bundle keeps `INSTALL_LLM_FALLBACK=false` so the install remains
lighter. Buyers who want local Qwen fallback can provide
`Qwen3.5-2B-Q4_K_M.gguf`, set `INSTALL_LLM_FALLBACK=true`, and rebuild the
OVOS image.

## License/IPR

The HumanEnerDIA backend/full-stack repository is distributed under the MIT
License. The bundled OVOS component remains `Apache-2.0 OR GPL-3.0-or-later`.
Third-party services keep their own upstream licenses.

## Production Notes

This artifact is designed as a zero-touch evaluation bundle and a guided
production starting point. Production hardening still requires buyer-specific
DNS, TLS, backup policy, secret rotation, and infrastructure review.
