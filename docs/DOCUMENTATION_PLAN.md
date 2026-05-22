# HumanEnerDIA Documentation Plan

This plan tracks the documentation set needed for delivery, support, and future
maintenance. It is not user guidance by itself; it is the map for keeping the
documentation complete.

## Audiences

| Audience | Needs |
|---|---|
| Business users | Understand dashboards, KPIs, reports, anomalies, and support paths |
| Operators | Start, stop, monitor, back up, restore, and troubleshoot the stack |
| Developers | Understand services, APIs, data model, configuration, and extension points |
| Integrators | Connect HumanEnerDIA to OVOS, external devices, MQTT, dashboards, and APIs |
| Delivery reviewers | Verify release readiness and packaging evidence |

## Current Documentation Set

| Document | Audience | Status |
|---|---|---|
| [Docs Index](./README.md) | All | Added |
| [Business User Guide](./BUSINESS_USER_GUIDE.md) | Non-technical | Added |
| [Technical Architecture Guide](./TECHNICAL_ARCHITECTURE_GUIDE.md) | Technical | Added |
| [Operations Runbook](./OPERATIONS_RUNBOOK.md) | Technical operators | Added |
| [KPI Reference](./KPI_REFERENCE.md) | Mixed | Added |
| [Database Schema Reference](./DATABASE_SCHEMA_REFERENCE.md) | Technical | Added |
| [Delivery Readiness](./DELIVERY_READINESS.md) | Delivery/release | Existing |
| [ENMS API Documentation for OVOS](./api-documentation/ENMS-API-DOCUMENTATION-FOR-OVOS.md) | Integrators | Existing |
| WASABI shop docs under `docs/wasabi-shop/` | Release/shop | Existing |

## Documentation Backlog

| Priority | Document | Audience | Notes |
|---|---|---|---|
| P0 | Screenshot completion pass | All | Replace placeholders after final UI screenshots are available |
| P0 | Public production README alignment | All | Keep root README and docs index consistent |
| P1 | API overview for general integrators | Technical | Summarize stable public routes and link to OpenAPI |
| P1 | Security hardening guide | Operators | TLS, firewall, secret rotation, CORS, public exposure |
| P1 | Backup and restore drill record | Operators | Document a tested restore, date, dataset, and owner |
| P2 | Troubleshooting by role | Mixed | Business-user and operator symptom lookup |
| P2 | Data quality guide | Mixed | Explain missing data, stale dashboards, and validation checks |
| P2 | Release artifact checklist | Delivery | Tie shop artifacts to checksums and clean repositories |

## Screenshot Placeholder Policy

Use stable relative paths under `docs/images/` so screenshots can be added later
without changing the Markdown links.

Recommended folders:

```text
docs/images/architecture/
docs/images/operations/
docs/images/user-guide/
docs/images/release/
```

Each screenshot should be captured from a clean deployment and should not show:

- real secrets
- personal emails unless intentionally public
- private tokens
- browser history or private tabs
- unrelated terminal output
- local paths that should not be public

## Accuracy Rules

- Do not document a script unless it exists in the repository.
- Do not mark `query-service` as production-ready until it has a real
  implementation and health contract.
- Prefer exact service names from `docker-compose.yml`.
- Prefer exact health endpoints from the running services.
- Keep `.env.example` aligned with installation and operations docs.
- Keep WASABI release docs separate from general product docs unless the reader
  is specifically installing or publishing the shop artifacts.
