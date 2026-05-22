# HumanEnerDIA Technical Architecture Guide

This guide is the system-level reference for engineers, maintainers, and
integrators working with HumanEnerDIA.

## Scope

HumanEnerDIA is a Docker Compose based industrial energy management platform.
It combines a web portal, reverse proxy, analytics APIs, time-series storage,
Grafana dashboards, MQTT ingestion, Node-RED flows, simulator data generation,
authentication, chatbot services, and an optional companion OVOS voice bridge.

The current deployment target is a Linux server running Docker Engine and
Docker Compose v2.

## System Context

Screenshot placeholder:

![System context diagram placeholder](./images/architecture/system-context.png)

```text
Users / Operators / Integrators
        |
        v
Nginx gateway (:8080 / :8443)
        |
        +-- Portal static UI
        +-- Analytics UI and API
        +-- Grafana
        +-- Node-RED
        +-- Auth API
        +-- Chatbot API
        +-- OVOS voice proxy route

Core services
        |
        +-- analytics       FastAPI, ML/KPI/reporting APIs
        +-- auth-service    Flask authentication and portal account flows
        +-- simulator       synthetic factory telemetry generator
        +-- nodered         MQTT-to-database ingestion and automation
        +-- chatbot/rasa    conversational web chatbot path
        +-- query-service   reserved placeholder, not a release-ready API

Data and messaging
        |
        +-- postgres        TimescaleDB-backed operational and analytics data
        +-- mqtt            Mosquitto telemetry broker
        +-- redis           cache and transient coordination
```

## Runtime Services

| Compose service | Container name by default | External port | Role |
|---|---:|---:|---|
| `nginx` | `enms-nginx` | `8080`, `8443` | Public gateway, portal, and reverse proxy |
| `postgres` | `enms-postgres` | `5433` | PostgreSQL with TimescaleDB |
| `mqtt` | `enms-mqtt` | `1883`, `9001` | MQTT telemetry broker |
| `redis` | `enms-redis` | `6380` | Redis cache |
| `simulator` | `enms-simulator` | internal `8003` | Synthetic factory data generator |
| `nodered` | `enms-nodered` | `1881` | Ingestion and automation flows |
| `grafana` | `enms-grafana` | `3001` | Dashboards and visualization |
| `analytics` | `enms-analytics` | `8001` | Analytics, KPI, baseline, forecast, reporting APIs |
| `query-service` | `enms-query-service` | `8002` | Placeholder container; excluded from release health |
| `auth-service` | `enms-auth-service` | `5500` | User auth, admin, and form APIs |
| `rasa-actions` | `enms-rasa-actions` | `5055` | Rasa custom action server |
| `rasa` | `enms-rasa` | `5005` | Rasa NLU server |
| `chatbot` | `enms-chatbot` | `5006` | Express chatbot backend |

When the full-stack release includes OVOS, it is started through the additional
Compose file generated into the release bundle, not directly from the base
`docker-compose.yml`.

## Network Model

All core containers join the Docker network named by `ENMS_NETWORK_NAME`, which
defaults to `enms-network`. Internal service-to-service calls use Compose service
names such as `postgres`, `redis`, `mqtt`, `analytics`, and `auth-service`.

External access should normally enter through Nginx on `NGINX_HTTP_PORT` or
`NGINX_HTTPS_PORT`. Direct service ports are exposed for development,
operations, or integration testing and should be restricted in production.

## Data Flow

Screenshot placeholder:

![Data flow diagram placeholder](./images/architecture/data-flow.png)

1. The simulator or external devices publish telemetry to MQTT.
2. Node-RED consumes MQTT messages and writes normalized records to PostgreSQL.
3. TimescaleDB hypertables store high-frequency time-series data.
4. Continuous aggregates provide 1-minute, 15-minute, 1-hour, and 1-day views.
5. The analytics service calculates KPIs, baselines, forecasts, anomalies,
   reports, and OVOS-facing responses.
6. The portal, Grafana, chatbot, and OVOS bridge consume API or dashboard data.

## Primary Data Stores

The base schema is initialized from `database/init/*.sql`.

Core tables include:

- `factories`
- `machines`
- `energy_readings`
- `production_data`
- `environmental_data`
- `machine_status`
- `energy_baselines`
- `anomalies`
- `energy_tariffs`
- `carbon_factors`
- `audit_log`

ISO 50001 and energy-performance tables include:

- `energy_sources`
- `seus`
- `seu_energy_performance`
- `baseline_adjustments`
- `data_quality_log`
- `energy_source_features`
- `enpi_baselines`
- `enpi_performance`
- `energy_targets`
- `action_plans`

Authentication and portal workflow tables include:

- `demo_users`
- `demo_sessions`
- `demo_audit_log`
- `pilot_factory_applications`

See [DATABASE_SCHEMA_REFERENCE.md](./DATABASE_SCHEMA_REFERENCE.md) for the
database reference.

## API Surface

Primary public API paths:

- Nginx health: `GET /health`
- Analytics health: `GET /api/analytics/api/v1/health` through Nginx or
  `GET :8001/api/v1/health` directly
- Analytics OpenAPI docs: `GET /api/analytics/docs` through Nginx
- Auth health: `GET /api/auth/health`
- Chatbot API: `/api/chatbot/*`
- OVOS voice proxy: `/api/ovos/voice/*`

The analytics service mounts routers under `/api/v1`, including baseline,
anomaly, KPI, machines, forecast, timeseries, stats, production, comparison,
SEU, energy-source, reports, and OVOS-related routes.

## Configuration Sources

- `.env.example`: public template for required deployment values.
- `.env`: local deployment values; never commit it.
- `docker-compose.yml`: service orchestration.
- `nginx/conf.d/default.conf`: public route mapping.
- `database/init/`: first-start database initialization.
- `grafana/provisioning/` and `grafana/dashboards/`: dashboard provisioning.
- `nodered/data/`: Node-RED flow and credential material.

Required production values include strong database, Redis, MQTT, Grafana,
Node-RED, JWT, and API credentials. SMTP values are optional; if SMTP is not
configured, email features are disabled and the auth service follows its
configured no-email behavior.

## Reliability Notes

- `query-service` is intentionally a placeholder and must not be used as a
  readiness signal.
- PostgreSQL, Redis, MQTT, analytics, simulator, Grafana, Node-RED, auth,
  Rasa, chatbot, and Nginx have health checks in Compose.
- Grafana dashboard JSON can be backed up with
  `scripts/backup-grafana-dashboards.sh`.
- PostgreSQL volume data is persistent in the Docker volume named
  `${VOLUME_PREFIX:-enms}-postgres-data`.

## Security Notes

- Do not commit `.env`, generated secrets, database dumps, service logs, model
  caches, or runtime volumes.
- Restrict direct exposure of database, Redis, MQTT, Grafana, Node-RED, and
  service debug ports in production.
- Terminate TLS at Nginx or an upstream reverse proxy before public exposure.
- Rotate any credential that has appeared in screenshots, documentation, shell
  history, tracked files, or uploaded artifacts.
- Review CORS and public route exposure before internet-facing deployment.

## Screenshot Placeholders

Replace these placeholders when final screenshots or diagrams are available:

- `docs/images/architecture/system-context.png`
- `docs/images/architecture/data-flow.png`
- `docs/images/architecture/service-map.png`
