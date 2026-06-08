# Software Design Documentation

Project: WASABI / HumanEnerDIA / OVOS-EnMS
Version: 1.0
Date: 2026-06-08
Status: Final delivery documentation package

Purpose: Document the implemented software modules, interfaces, data model, and design constraints.
Audience: Developers, maintainers, technical reviewers, and integration engineers.

Evidence rule: Claims prefer route registration, service code, SQL schema, compose files, and tests over README-level descriptions.

## Design Overview

HumanEnerDIA uses a service-oriented design. Nginx centralizes browser and API routing; analytics owns most domain APIs; PostgreSQL/TimescaleDB owns persistent operational and time-series data; MQTT and Node-RED connect telemetry ingestion; Grafana presents dashboards; simulator produces demo telemetry; auth-service owns user/account workflows; Rasa/chatbot provides a text help assistant; OVOS-EnMS provides a separate assistant layer.

The repository favors explicit route modules and service modules rather than a single monolithic backend. The analytics service mounts routers for baselines, anomalies, KPIs, machines, forecasts, time series, visualization data, model performance, production, SEU/ISO 50001 features, reports, and OVOS-facing integration.

## Module Responsibility Matrix

| Subsystem | Responsibilities | Primary evidence |
| --- | --- | --- |
| analytics/api/routes | FastAPI request handlers and route-specific request/response behavior | analytics/api/routes/ |
| analytics/services | Business logic for KPIs, baselines, forecasts, anomaly handling, performance, event publishing, reports, and Redis coordination | analytics/services/ |
| analytics/models | ML/statistical model implementations and model persistence helpers | analytics/models/ |
| database/init | First-start schema, hypertables, continuous aggregates, SQL functions, seed data, ISO 50001 and model-performance tables | database/init/02-schema.sql; database/init/03-timescaledb-setup.sql; database/init/04-functions.sql |
| simulator | FastAPI control endpoints, machine simulation classes, MQTT publisher, auto anomaly injection support | simulator/main.py; simulator/api/routes.py; simulator/simulator_manager.py; simulator/mqtt_publisher.py |
| nodered | MQTT topic parsing, data validation, and PostgreSQL write pipeline | nodered/data/flows.json; nodered/settings.js; nodered/package.json |
| auth-service | Registration, login, JWT verification, admin APIs, email verification/reset, pilot/contact forms | auth-service/app.py; auth-service/auth_service.py; database/init/05-auth-schema.sql |
| chatbot/rasa | Text help chatbot, QA retrieval actions, Rasa runtime, Express proxy backend | chatbot/server/index.js; chatbot/rasa/actions/actions.py; chatbot/rasa/qa_data.json |

## Analytics Service Design

The analytics service is a FastAPI application with lifespan-managed database connection, optional Redis event subscriber, scheduler startup, route registration, CORS middleware, request logging, timeout handling, and generic exception handling.

Router registration in analytics/main.py shows the implemented surface: baseline, anomaly, KPI, machines, forecast, time series, sankey, heatmap, comparison, model performance, stats, production, SEU/factory/performance/ISO 50001/multi-energy, OVOS, OVOS voice proxy, and reports.

| API area | Representative endpoints | Evidence |
| --- | --- | --- |
| Health and system | /api/v1/health, /api/v1/stats/system, /api/v1/stats/connections | analytics/main.py |
| Baselines | /api/v1/baseline/train, /deviation, /predict, /models, /train-seu | analytics/api/routes/baseline.py |
| KPIs | /api/v1/kpi/sec, /peak-demand, /load-factor, /energy-cost, /carbon, /all, /factory | analytics/api/routes/kpi.py |
| Forecasting | /api/v1/forecast/train/arima, /train/prophet, /predict, /demand, /peak, /short-term | analytics/api/routes/forecast.py |
| Anomalies | /api/v1/anomaly/create, /detect, /search, /recent, /active, /{id}/resolve | analytics/api/routes/anomaly.py |
| Machines and time series | /api/v1/machines, /machines/status/{name}, /timeseries/energy, /power, /latest/{id} | analytics/api/routes/machines.py; timeseries.py |
| ISO 50001 and SEUs | /api/v1/iso50001/*, /api/v1/seus, /api/v1/reports/seu-performance | analytics/api/routes/iso50001.py; seu.py; seus.py |
| Reports | /api/v1/reports/types, /generate, /preview, /v2/generate, /v2/download/{id}, /v2/status | analytics/api/routes/reports.py |
| OVOS integration | /api/v1/ovos/*, /api/v1/ovos/voice/query, /voice/health, /voice/config | analytics/api/routes/ovos.py; ovos_voice.py |
| Visualization data | /api/v1/sankey/data, /heatmap/hourly, /comparison/machines, /compare/machines | analytics/api/routes/sankey.py; heatmap.py; comparison.py; compare.py |

## Database And Schema Design

The database initialization files create core dimensions, time-series facts, current-state tables, baseline/anomaly/tariff/carbon/audit tables, auth tables, ISO 50001 tables, model-performance tables, forecast output tables, and action-plan workflow tables.

TimescaleDB is used for high-frequency time-series storage. The initialization scripts create hypertables for energy_readings, production_data, environmental_data, and energy_forecasts, plus continuous aggregates at 1 minute, 15 minutes, 1 hour, and 1 day where implemented.

| Database object group | Implemented objects | Evidence |
| --- | --- | --- |
| Core entities | factories, machines, energy_readings, production_data, environmental_data, machine_status | database/init/02-schema.sql |
| Analytics metadata | energy_baselines, anomalies, energy_tariffs, carbon_factors, model performance/training/alert tables | database/init/02-schema.sql; 11-13 model scripts |
| ISO 50001 | energy_sources, seus, seu_energy_performance, enpi_baselines, enpi_performance, energy_targets, action_plans | database/init/07-iso50001-schema.sql; 15-16 scripts |
| Aggregates | energy, production, and environmental aggregate materialized views | database/init/03-timescaledb-setup.sql |
| KPI functions | calculate_sec, calculate_peak_demand, calculate_load_factor, calculate_energy_cost, calculate_carbon_intensity, calculate_all_kpis | database/init/04-functions.sql |

## Simulator And Ingestion Design

The simulator is a FastAPI service with lifecycle initialization. It connects to PostgreSQL, connects to MQTT, loads active machines from the database, creates simulator instances by machine type, and can auto-start based on configuration.

Machine implementations generate energy, production, environmental, and status payloads. The boiler path supports multi-energy publication for electricity, natural gas, and steam style payloads. Node-RED processes subscribed MQTT traffic and writes normalized records into the database.

| Area | Design details | Evidence |
| --- | --- | --- |
| Control API | start, stop, runtime config, status, list machines, machine detail, inject/clear anomaly, info | simulator/api/routes.py |
| Machine loading | Loads active machines from database with type, rated_power_kw, interval, and MQTT topic | simulator/simulator_manager.py |
| MQTT publishing | Publishes energy, multi-energy, production, environmental, and retained status messages | simulator/mqtt_publisher.py |
| Node-RED flow | Subscribe: factory/#, Parse Topic, Route by Type, Process Energy/Production/Environmental/Status | nodered/data/flows.json |

## Authentication, Portal, And Chatbot Design

auth-service is a Flask application backed by demo_users, demo_sessions, demo_audit_log, and pilot_factory_applications tables. It implements registration, login, JWT verification, email verification, password reset, admin user management, CSV export, pilot factory application workflows, and contact form handling.

The portal is static HTML/CSS/JS served by Nginx. It includes general pages, authentication pages, admin pages, report pages, and an OVOS voice widget script. The chatbot backend is an Express service that serves the built frontend and proxies to Rasa and OVOS endpoints.

The Rasa custom action loads qa_data.json and retrieves knowledge/help answers using exact match, special cases, keyword routing, abbreviation expansion, misspelling correction, and fuzzy-style matching logic. This is a text help path; it should not be confused with live OVOS operational queries.

## Configuration, Validation, Logging, And Error Handling

- Configuration is primarily environment-driven through .env.example, docker-compose.yml, analytics/config.py, simulator/config.py, Node-RED settings, and OVOS settings/config files.
- The setup helper preserves existing non-placeholder .env values, generates missing first-run secrets, validates Compose, builds images, and starts services.
- FastAPI services use health endpoints, request logging, validation exception handlers, and generic exception handlers.
- OVOS skill validation uses Pydantic schemas, confidence thresholding, machine whitelists, fuzzy matching, metric validation, time-range parsing, and entity normalization.
- auth-service uses bcrypt password hashing, JWT sessions, email verification gates, admin decorators, and parameterized SQL queries.

## Known Design Gaps And Placeholders

| Gap or caution | Evidence-based status |
| --- | --- |
| query-service | Only Dockerfile and empty route/schema/service folders observed; compose healthcheck disabled. |
| Report V2 semantics | V2 routes and generator exist, but some service values are proportional or placeholder-derived, such as efficiency sparkline and estimated baseline cost. |
| Simulator machine list inconsistency | Code supports boiler; simulator info endpoint text still lists five machine types. |
| Direct public exposure | Several internal service ports are externally mapped for development/ops; production hardening requires operator firewall/TLS review. |
| README claims | Root README contains high-level feature claims; final documents use code/config evidence where details differ. |

## Evidence References

The table below lists the main local evidence used for this document. It is not a full file inventory; it identifies the sources behind the material claims.

| Topic | Evidence |
| --- | --- |
| Analytics app and routers | analytics/main.py; analytics/api/routes/ |
| SQL schema/functions | database/init/02-schema.sql; database/init/03-timescaledb-setup.sql; database/init/04-functions.sql |
| Simulator | simulator/main.py; simulator/api/routes.py; simulator/simulator_manager.py; simulator/mqtt_publisher.py |
| Node-RED | nodered/data/flows.json; nodered/settings.js; nodered/package.json |
| Auth | auth-service/app.py; auth-service/auth_service.py; database/init/05-auth-schema.sql |
| Chatbot/Rasa | chatbot/server/index.js; chatbot/rasa/actions/actions.py; chatbot/rasa/qa_data.json |
| Tests | analytics/tests/test_*.py; /home/ubuntu/ovos-llm/enms-ovos-skill/tests/test_*.py |
