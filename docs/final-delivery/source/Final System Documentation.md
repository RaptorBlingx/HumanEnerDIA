# Final System Documentation

Project: WASABI / HumanEnerDIA / OVOS-EnMS
Version: 1.0
Date: 2026-06-08
Status: Final delivery documentation package

Purpose: Provide a stakeholder-ready end-to-end overview, installation/operation guide, workflows, and final delivery notes.
Audience: Managers, reviewers, operators, users, integrators, and external WASABI partners.

Evidence rule: This document summarizes the evidence-backed content of the technical documents and points readers to implemented local sources.

## Project Overview

![Figure 1. Relationship between HumanEnerDIA, OVOS-EnMS, data services, dashboards, and users.](../assets/system-context.png)

HumanEnerDIA is an open-source industrial energy management system developed for the WASABI project delivery context. It monitors and analyzes simulated or ingested factory energy data, provides dashboards and APIs, supports ISO 50001-oriented concepts, and integrates with an OVOS assistant layer for natural-language operational queries.

The final package should be described as a Docker Compose deployable system with a companion OVOS-EnMS assistant. It includes implemented backend services, dashboards, reports, simulator, ingestion flow, authentication, text chatbot, and OVOS voice/natural-language paths. It also includes documented limitations that must remain visible for review.

## Installation And Access

For a local or evaluation deployment, use the guided setup script from the repository or extracted release bundle. For remote browser access, pass a server host or IP so generated URLs match the expected access path. Generated credentials are stored in .env and must be kept private.

| Access point | Default URL | Notes |
| --- | --- | --- |
| Unified portal | http://<host>:8080 | Served by Nginx from portal/public |
| Grafana | http://<host>:8080/grafana | Sub-path proxy to Grafana with provisioned dashboards |
| Analytics UI | http://<host>:8080/analytics/ui/ | FastAPI-rendered analytics templates |
| Analytics API docs | http://<host>:8080/api/analytics/docs | Nginx proxy to analytics OpenAPI docs |
| Simulator docs | http://<host>:8080/api/simulator/docs | Nginx proxy to simulator OpenAPI docs |
| Node-RED | http://<host>:1881 or http://<host>:8080/nodered/ | Admin UI protected by Node-RED credentials |
| OVOS bridge | http://<host>:5000/health | Available when the separate OVOS-EnMS stack or release-bundle component is deployed |

## Main Workflows

| Workflow | Implementation path | Result |
| --- | --- | --- |
| Start system | ./setup.sh or docker compose build/up | Services start with generated or configured environment values. |
| Generate telemetry | simulator -> MQTT -> Node-RED -> PostgreSQL | Energy, production, environmental, status, and selected multi-energy data are stored. |
| View dashboards | Grafana through Nginx or direct port | Configured SOTA dashboard JSON views are available. |
| Use analytics APIs | FastAPI analytics service under /api/v1 | KPIs, baselines, forecasts, anomalies, reports, and related data are exposed. |
| Authenticate/admin | auth-service through portal and /api/auth, /api/admin | Registration/login/admin/session flows use JWT and database tables. |
| Ask text help questions | chatbot Express proxy -> Rasa -> custom action QA retrieval | Knowledge/help answers from qa_data.json categories. |
| Ask operational assistant questions | OVOS REST bridge -> messagebus -> EnMS skill -> analytics API | Voice/text operational responses with structured data. |
| Generate reports | analytics report endpoints | Legacy monthly EnPI PDF and V2 PDF paths are available. |

## Operator Guide

- Use docker compose ps and service health endpoints for daily status checks.
- Check Nginx first for browser routing issues, then the owning upstream service.
- Inspect simulator, MQTT, Node-RED, and PostgreSQL together for data-ingestion issues.
- Use the tracked JSON files under grafana/dashboards and Grafana provisioning files for dashboard review and controlled updates.
- Use pg_dump or platform backup tooling for PostgreSQL; no generic tracked database backup script exists.
- Avoid docker compose down -v unless the purpose is deliberate persistent data deletion.

## Analytics, Dashboards, Reports, And Assistants

Analytics capabilities include baseline training/prediction/deviation, KPI functions, forecasting, anomaly detection/search, machine status and time series, comparison/visualization data, model performance, production metrics, performance analysis, ISO 50001/SEU endpoints, and report generation.

Dashboards are configured in Grafana JSON and provisioned through the Grafana provisioning directory. The Rasa chatbot is a text help/knowledge assistant, while OVOS-EnMS is the operational natural-language assistant integrated with live backend APIs.

| Dashboard or assistant | Purpose |
| --- | --- |
| Grafana dashboards | Operational, executive, cost, carbon, ISO 50001, anomaly, model, production, and predictive views. |
| Analytics UI | FastAPI-rendered pages for dashboards, baselines, anomalies, KPIs, forecasts, Sankey, heatmap, comparison, and model performance. |
| Rasa chatbot | Text knowledge/help assistant using QA categories and custom retrieval action. |
| OVOS-EnMS | Operational assistant for energy, power, machine status, rankings, anomalies, forecasts, baselines, KPIs, reports, help, and health checks. |

## Maintenance And Troubleshooting

Maintenance should focus on credential rotation, backup verification, dashboard export/commit policy, disk usage, restart counts, recent errors, image/base dependency review, and firewall/public route review. Production hardening requires operator policy beyond the repository defaults.

| Maintenance area | Recommended review |
| --- | --- |
| Credentials | Rotate generated first-run values and any exposed credentials. |
| Backups | Test PostgreSQL restore; back up Grafana dashboards and Docker volumes. |
| Dashboards | Commit intended Grafana JSON changes after backup/export. |
| Telemetry | Confirm simulator/MQTT/Node-RED/PostgreSQL are all healthy when data appears stale. |
| OVOS | Confirm /health messagebus_connected and smoke query when assistant is required. |
| Docs | Update final documents when route, schema, compose, or packaging behavior changes. |

## Final Delivery Notes

- The full-stack release notes identify the HumanEnerDIA archive, SHA256 checksum, licensing notes, and embedded OVOS runtime/skill directory under ovos-stack.
- .env is not shipped and must not be disclosed.
- The optional Qwen GGUF model is not bundled in the main release artifacts according to the release notes.
- Runtime health must be verified on the actual target deployment before stakeholder demonstration or handover.

## Limitations And Assumptions

The following items should be reviewed before stakeholder distribution. They are documented to avoid overstating the current implementation.

| Item | Status |
| --- | --- |
| Runtime verification | This documentation package records compose validation. Live health checks require a running deployment and are not implied unless run separately. |
| OVOS deployment boundary | The GitHub production base docker-compose.yml does not define an OVOS service. OVOS-EnMS is documented as a separate source repository and as an embedded component in the full-stack release archive. |
| OVOS release artifact | Release notes state optional GGUF model weights are not bundled by default. |
| Third-party EnMS support | OVOS portability is through a HumanEnerDIA-compatible API or adapter/proxy, not zero-code support for arbitrary vendor APIs. |
| Reports V2 | V2 report code is implemented, but some service calculations use derived/proportional or placeholder values; final stakeholders should review report semantics before audit use. |
| Simulator inventory | The simulator code supports boiler in addition to compressor, HVAC, motor, pump, and injection molding. One simulator info response still lists five machine types. |
| Security posture | The codebase provides secret placeholders, generated first-run credentials, JWT/bcrypt auth, health checks, and hardening guidance. Public production exposure still requires operator DNS/TLS/firewall/credential work. |

## Evidence References

The table below lists the main local evidence used for this document. It is not a full file inventory; it identifies the sources behind the material claims.

| Topic | Evidence |
| --- | --- |
| Overview/docs | README.md; releases/HumanEnerDIA-full-stack-v1.0.0-release-notes.md |
| Deployment | docker-compose.yml; setup.sh; verify.sh |
| Analytics/database | analytics/main.py; database/init/02-schema.sql; database/init/03-timescaledb-setup.sql; database/init/04-functions.sql |
| Dashboards and reports | grafana/provisioning/; grafana/dashboards/; analytics/api/routes/reports.py; analytics/reports/; analytics/reports_v2/ |
| OVOS-EnMS | OVOS-EnMS repository: README.md; enms-ovos-skill/README.md; enms-ovos-skill/bridge/ovos_rest_bridge.py; enms-ovos-skill/enms_ovos_skill/__init__.py |
| Release artifact notes | releases/HumanEnerDIA-full-stack-v1.0.0-release-notes.md |
