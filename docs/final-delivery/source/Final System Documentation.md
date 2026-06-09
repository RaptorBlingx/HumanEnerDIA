# Final System Documentation

Project: WASABI / HumanEnerDIA / OVOS-EnMS
Version: 1.1
Date: 2026-06-09
Status: Final stakeholder-ready documentation package

Purpose: Provide a stakeholder-ready end-to-end overview, installation/operation guide, workflows, and final delivery notes.
Audience: Managers, reviewers, operators, users, integrators, and external WASABI partners.

Source basis: This document summarizes the evidence-backed content of the technical documents and points readers to implemented local sources.

## Project Overview

![Figure 1. Relationship between HumanEnerDIA, OVOS-EnMS, data services, dashboards, and users.](../assets/system-context.png)

HumanEnerDIA is an open-source industrial energy management system developed for the WASABI project delivery context. It monitors and analyzes simulated or ingested factory energy data, provides dashboards and APIs, supports ISO 50001-oriented concepts, and integrates with an OVOS assistant layer for natural-language operational queries.

This final delivery package presents the system as a Docker Compose deployable HumanEnerDIA stack with a companion OVOS-EnMS assistant repository/runtime. It includes implemented backend services, dashboards, reports, simulator, ingestion flow, authentication, text chatbot, and OVOS voice/natural-language paths, with limitations kept visible for review.

## Handover Summary

The six-document package is intended to let managers, reviewers, operators, and external partners understand what has been delivered, how the parts fit together, how to deploy and verify the stack, and which items still require runtime validation or production hardening.

| Document | Primary use |
| --- | --- |
| System Architecture Report | Architecture, service responsibilities, boundaries, data/message flow, security/network posture, and operational risks. |
| Software Design Documentation | Module design, API/database/service/auth design, configuration, logging, error handling, and design limitations. |
| Skill Documentation | OVOS-EnMS query lifecycle, intents, parser/validator/client/formatter behavior, configuration, mappings, and failure behavior. |
| Energy Management System Reports and KPI Reports | Energy data model, KPI catalog, formulas, dashboards, report workflow, data-quality assumptions, and audit cautions. |
| Docker Deployment Report | Compose topology, setup, environment groups, health checks, backup/recovery, redeployment, troubleshooting, and hardening. |
| Final System Documentation | End-to-end reader guide, workflows, operations, acceptance/demo checklists, and final delivery notes. |

## Delivery Artifact List

The formal deliverables are the six DOCX files. Source Markdown, the evidence map, diagrams, and generator script are included for maintainability and reproducibility.

| Artifact | Purpose |
| --- | --- |
| Final DOCX reports | Six stakeholder deliverables in docs/final-delivery/. |
| Source Markdown | docs/final-delivery/source/*.md mirrors the generated DOCX content for maintainability. |
| Evidence map | docs/final-delivery/source/evidence-map.md maps recurring claims to source files and validation output. |
| Generation script | docs/final-delivery/source/generate_delivery_docs.py regenerates DOCX, Markdown, and diagrams. |
| Diagram assets | docs/final-delivery/assets/*.png contains architecture, data-flow, deployment, topology, and OVOS lifecycle diagrams. |
| Application source | HumanEnerDIA production source tree plus separate OVOS-EnMS repository remain the authoritative technical sources. |

## Reader Guide

- Managers should start with Final System Documentation, then System Architecture Report, then the limitations sections.
- Technical reviewers should read Software Design Documentation, Energy Management System Reports and KPI Reports, and Docker Deployment Report.
- Assistant/voice reviewers should read Skill Documentation and the OVOS integration sections in the architecture report.
- Operators should use Docker Deployment Report together with setup.sh, verify.sh, docker-compose.yml, and .env.example.
- External partners should treat evidence references as the traceability map for major technical claims.

## Quick-Start Summary

This quick-start summarizes the handover path. It does not replace the deployment report or the live verification scripts.

| Step | Action | Outcome |
| --- | --- | --- |
| 1 | Review .env.example and run ./setup.sh with the target server host/IP if needed. | .env is created locally and first-run secrets are generated. |
| 2 | Run or confirm docker compose config --quiet. | Compose syntax and interpolation are valid. |
| 3 | Start the stack through setup.sh or docker compose up -d. | HumanEnerDIA services start on the configured network and ports. |
| 4 | Run docker compose ps and health checks. | Container status and basic service health are visible. |
| 5 | Run verify.sh when services are running. | Gateway, analytics, and optional OVOS live checks are performed. |
| 6 | Open portal, Grafana, analytics UI/API docs, and assistant endpoints as needed. | Stakeholder/demo access points are ready for review. |

## Installation And Access

For a local or evaluation deployment, use the guided setup script from the production repository checkout or approved delivery bundle. For remote browser access, pass a server host or IP so generated URLs match the expected access path. Generated credentials are stored in .env and must be kept private.

| Access point | Default URL | Notes |
| --- | --- | --- |
| Unified portal | http://<host>:8080 | Served by Nginx from portal/public |
| Grafana | http://<host>:8080/grafana | Sub-path proxy to Grafana with provisioned dashboards |
| Analytics UI | http://<host>:8080/analytics/ui/ | FastAPI-rendered analytics templates |
| Analytics API docs | http://<host>:8080/api/analytics/docs | Nginx proxy to analytics OpenAPI docs |
| Simulator docs | http://<host>:8080/api/simulator/docs | Nginx proxy to simulator OpenAPI docs |
| Node-RED | http://<host>:1881 or http://<host>:8080/nodered/ | Admin UI protected by Node-RED credentials |
| OVOS bridge | http://<host>:5000/health | Available when the separate OVOS-EnMS runtime is deployed |

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

- The documentation package relies on the GitHub production source tree and the separate OVOS-EnMS repository, not on untracked local release artifacts.
- .env is not shipped and must not be disclosed.
- The optional Qwen GGUF model path and LLM fallback controls are documented from the OVOS-EnMS code/config; model availability must be verified in the deployed OVOS-EnMS runtime.
- Runtime health must be verified on the actual target deployment before stakeholder demonstration or handover.

## Acceptance Checklist

The following checks define the final documentation package acceptance state for stakeholder review.

| Check | Expected result |
| --- | --- |
| Documentation files exist | All six required DOCX files are present under docs/final-delivery/. |
| Source alignment | No references to untracked release artifacts, missing release scripts, absent Compose services, or local absolute paths. |
| Compose validation | docker compose config --quiet passes for HumanEnerDIA production; OVOS-EnMS Compose validates separately. |
| DOCX integrity | All DOCX files open as valid ZIP/DOCX packages and contain embedded media where expected. |
| Secrets hygiene | Generated docs and sources are scanned for sensitive placeholders and private values. |
| Stakeholder limitations | Runtime, audit, OVOS boundary, and production-hardening limitations remain visible. |

## Demo-Readiness Checklist

Before a live stakeholder demonstration, use this checklist alongside the deployment report and verify.sh. These checks are operational and must be performed on the actual target deployment.

| Area | Readiness action |
| --- | --- |
| Before demo | Run docker compose ps, verify.sh, Nginx/analytics health checks, and OVOS /health if assistant demo is planned. |
| Data freshness | Confirm simulator or real ingestion is producing recent records before showing dashboards/KPIs. |
| Credentials | Use prepared demo/operator credentials without displaying .env or secrets. |
| Dashboards | Open Grafana dashboards and confirm panels load with current data. |
| Assistant | Run at least one machine status query and one KPI/report-style query through the OVOS bridge if OVOS is in scope. |
| Known cautions | Be ready to explain demo data, partial V2 report semantics, and production hardening steps. |

## Limitations And Assumptions

The following items should be reviewed before stakeholder distribution. They are documented to avoid overstating the current implementation.

| Item | Status |
| --- | --- |
| Runtime verification | This documentation package records compose validation. Live health checks require a running deployment and are not implied unless run separately. |
| OVOS deployment boundary | The GitHub production base docker-compose.yml does not define an OVOS service. OVOS-EnMS is documented as a separate source repository and companion assistant runtime. |
| OVOS optional LLM fallback | The OVOS-EnMS Dockerfile installs LLM fallback dependencies only when INSTALL_LLM_FALLBACK=true. Model availability must be verified in the OVOS-EnMS repository/runtime. |
| Third-party EnMS support | OVOS portability is through a HumanEnerDIA-compatible API or adapter/proxy, not zero-code support for arbitrary vendor APIs. |
| Reports V2 | V2 report code is implemented, but some service calculations use derived/proportional or placeholder values; final stakeholders should review report semantics before audit use. |
| Simulator inventory | The simulator code supports boiler in addition to compressor, HVAC, motor, pump, and injection molding. One simulator info response still lists five machine types. |
| Security posture | The codebase provides secret placeholders, generated first-run credentials, JWT/bcrypt auth, health checks, and hardening guidance. Public production exposure still requires operator DNS/TLS/firewall/credential work. |

## Source References

The table below lists the main source material used for this document. It is not a full file inventory; it identifies the sources behind the material claims.

| Topic | Source material |
| --- | --- |
| Overview/docs | README.md; docs/final-delivery/ |
| Deployment | docker-compose.yml; setup.sh; verify.sh |
| Analytics/database | analytics/main.py; database/init/02-schema.sql; database/init/03-timescaledb-setup.sql; database/init/04-functions.sql |
| Dashboards and reports | grafana/provisioning/; grafana/dashboards/; analytics/api/routes/reports.py; analytics/reports/; analytics/reports_v2/ |
| OVOS-EnMS | OVOS-EnMS repository: README.md; enms-ovos-skill/README.md; enms-ovos-skill/bridge/ovos_rest_bridge.py; enms-ovos-skill/enms_ovos_skill/__init__.py |
| Delivery package sources | docs/final-delivery/source/; docs/final-delivery/assets/ |
