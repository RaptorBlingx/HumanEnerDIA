# Software Design Documentation

Project: WASABI / HumanEnerDIA / OVOS-EnMS
Version: 1.1
Date: 2026-06-09
Status: Final stakeholder-ready documentation package

Purpose: Document the implemented software modules, interfaces, data model, and design constraints.
Audience: Developers, maintainers, technical reviewers, and integration engineers.

Source basis: Claims prefer route registration, service code, SQL schema, compose files, and tests over README-level descriptions.

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

## API Design Details

The API design is organized by domain routers rather than by a single generic endpoint. The production tree exposes both operational APIs and UI-serving routes, and some compatibility routes remain mounted for OVOS-oriented integrations.

| Design aspect | Observed implementation | Source basis |
| --- | --- | --- |
| Route organization | analytics/main.py mounts route modules under settings.API_PREFIX, normally /api/v1. | FastAPI routers keep domain areas separate and expose OpenAPI docs. |
| Request/response models | Several routes use Pydantic response models, especially forecast, heatmap, ISO 50001, performance, model-performance, voice proxy, and reports. | Validation and schema visibility are strongest in typed routes. |
| Database access | Routes and services use the analytics database module and async connection pool where implemented. | Data-heavy routes prefer SQL queries and database functions over in-memory mock state. |
| Legacy/deprecated routes | OVOS and OVOS training routes remain mounted with comments noting newer factory/analytics/baseline paths. | Document as compatibility surface, not a separate service. |
| UI route surface | analytics/api/routes/ui_routes.py serves analytics UI pages for dashboard/baseline/anomaly/KPI/forecast/Sankey/heatmap/comparison/model-performance paths. | These are FastAPI-rendered pages, distinct from Grafana dashboards. |

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

## Database Object Catalog

The following catalog is intended as a stakeholder-level data-design view. It avoids column-by-column schema reproduction while identifying the functional database groups that support the application.

| Object group | Representative objects | Design role |
| --- | --- | --- |
| Core dimensions | factories, machines | Facility and machine metadata, including machine type, factory association, active flag, rated power, and topic-related context. |
| Telemetry facts | energy_readings, production_data, environmental_data, machine_status | High-frequency operational data and current machine state. |
| Time-series acceleration | Timescale hypertables and continuous aggregate views | 1 minute, 15 minute, 1 hour, and 1 day views support KPI/report/dashboard queries. |
| Analytics metadata | energy_baselines, anomalies, energy_tariffs, carbon_factors, audit_log | Model, anomaly, cost, carbon, and audit support tables. |
| ISO 50001 structures | energy_sources, seus, seu_energy_performance, enpi_baselines, enpi_performance, energy_targets, action_plans | Energy-source, significant-energy-use, EnPI, target, and action-plan concepts. |
| Model/forecast tracking | model_performance tables, energy_forecasts, model_training_history, model_alerts | Forecast output and model lifecycle/performance observations. |

## Service-Layer Design

The analytics service layer centralizes most non-trivial domain logic. KPIService wraps SQL KPI functions; baseline and forecast services coordinate model training/prediction and storage; anomaly services detect and record anomalies; report services assemble data and output files; event publisher/subscriber modules integrate Redis Pub/Sub where enabled.

This design keeps route handlers closer to request/response orchestration while delegating calculation, modeling, report assembly, and event behavior to domain services. Some older routes still contain direct SQL or route-level calculations, so the design is pragmatic rather than fully uniform.

| Service area | Implementation responsibility | Source basis |
| --- | --- | --- |
| KPI service | Calls SQL functions for SEC, peak demand, load factor, cost, carbon, and combined KPI responses. | analytics/services/kpi_service.py; database/init/04-functions.sql |
| Baseline services | Train/predict baseline models, store model metadata, explain drivers, and support SEU baseline training. | analytics/services/baseline_service.py; seu_baseline_service.py; analytics/models/baseline.py |
| Forecast service | Train ARIMA/Prophet models, create predictions, and support short-term/peak/demand routes. | analytics/services/forecast_service.py; analytics/models/*forecast*.py |
| Anomaly service | Create/detect/search/resolve anomalies and support anomaly-oriented routes. | analytics/services/anomaly_service.py; analytics/api/routes/anomaly.py |
| Report services | Generate legacy monthly EnPI PDFs and V2 report outputs through report components and generators. | analytics/reports/; analytics/reports_v2/ |
| Event services | Publish and subscribe to Redis channels for anomaly, metric, training, and system alert events when enabled. | analytics/services/event_publisher.py; event_subscriber.py; redis_manager.py |

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

## Authentication And Authorization Design

Authentication is implemented in a separate Flask service rather than inside the analytics FastAPI application. The service stores users, sessions, and audit records in PostgreSQL auth tables and exposes login/registration/admin/contact workflows through Nginx-routed endpoints.

Authorization is strongest on the auth-service admin endpoints, where a decorator verifies bearer JWTs, checks the configured admin email allowlist, and confirms the active/verified admin role in the database. Analytics middleware includes JWT support, but the final documentation should not imply a complete cross-service enterprise IAM layer.

| Auth feature | Observed implementation | Source basis |
| --- | --- | --- |
| Password storage | bcrypt with 12 rounds. | auth-service/auth_service.py |
| Session token | JWT signed with HS256 and stored in demo_sessions with expiry metadata. | auth-service/auth_service.py; database/init/05-auth-schema.sql |
| Email verification | Verification tokens and verified_at fields; email can be disabled, which auto-verifies users on registration. | auth-service/auth_service.py |
| Password reset | Reset token and timestamp fields with one-hour expiry logic. | auth-service/auth_service.py; database/init/05-auth-schema.sql |
| Admin controls | Admin allowlist from ADMIN_EMAILS plus database role/is_active/email_verified checks. | auth-service/auth_service.py |
| Audit trail | REGISTER, LOGIN, EMAIL_VERIFY and related actions are inserted into demo_audit_log. | auth-service/auth_service.py; database/init/05-auth-schema.sql |

## Configuration, Validation, Logging, And Error Handling

- Configuration is primarily environment-driven through .env.example, docker-compose.yml, analytics/config.py, simulator/config.py, Node-RED settings, and OVOS settings/config files.
- The setup helper preserves existing non-placeholder .env values, generates missing first-run secrets, validates Compose, builds images, and starts services.
- FastAPI services use health endpoints, request logging, validation exception handlers, and generic exception handlers.
- OVOS skill validation uses Pydantic schemas, confidence thresholding, machine whitelists, fuzzy matching, metric validation, time-range parsing, and entity normalization.
- auth-service uses bcrypt password hashing, JWT sessions, email verification gates, admin decorators, and parameterized SQL queries.

## Configuration Reference

Configuration is intentionally environment-driven. Stakeholder documentation should discuss configuration groups and operational responsibility, not disclose actual .env values.

| Configuration group | Representative variables | Source basis |
| --- | --- | --- |
| Database | POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT | .env.example; docker-compose.yml; analytics/config.py |
| Service ports | NGINX_HTTP_PORT, ANALYTICS_PORT, SIMULATOR_PORT, GRAFANA_PORT, NODERED_PORT, RASA_PORT, CHATBOT_PORT, REDIS_EXTERNAL_PORT | .env.example; docker-compose.yml |
| Security and auth | JWT_SECRET, API_KEY, ADMIN_EMAILS, JWT expiration settings, Node-RED password hash/credential secret | .env.example; auth-service/auth_service.py; nodered/settings.js |
| Telemetry | MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, simulator intervals and anomaly settings | .env.example; simulator/config.py |
| Analytics behavior | LOG_LEVEL, scheduler settings, model storage, anomaly thresholds, cost/carbon defaults | analytics/config.py; .env.example |
| OVOS proxy/runtime | OVOS_BRIDGE_HOST, OVOS_BRIDGE_PORT, OVOS_BRIDGE_TIMEOUT, OVOS external ports | .env.example; analytics/api/routes/ovos_voice.py; OVOS-EnMS repository compose |

## Error Handling And Logging

The codebase includes explicit error handling in key services, but behavior is not completely uniform across every route. This should be represented as implemented service-level error handling rather than a single formal enterprise error contract.

| Area | Observed behavior |
| --- | --- |
| Analytics request handling | Request logging middleware, validation exception handling, timeout middleware, and generic exception handling are present in analytics/main.py and middleware modules. |
| Analytics route behavior | Routes generally return structured JSON errors or raise HTTPException when validation, lookup, or database work fails. |
| Auth service | Endpoints catch exceptions, log errors, and return success/error JSON while auth_service.py performs bcrypt/JWT verification and audit logging. |
| Simulator | Lifecycle startup/shutdown, MQTT/database connection handling, and route-level start/stop/status errors are implemented. |
| OVOS bridge/client | Bridge returns structured failure responses on messagebus/query errors; ENMSClient avoids retrying ordinary 4xx errors and retries transient/timeouts/5xx. |

## Known Design Gaps And Placeholders

| Gap or caution | Source-backed status |
| --- | --- |
| Report V2 semantics | V2 routes and generator exist, but some service values are proportional or placeholder-derived, such as efficiency sparkline and estimated baseline cost. |
| Simulator machine list inconsistency | Code supports boiler; simulator info endpoint text still lists five machine types. |
| Direct public exposure | Several internal service ports are externally mapped for development/ops; production hardening requires operator firewall/TLS review. |
| README claims | Root README contains high-level feature claims; final documents use code/config evidence where details differ. |

## Source References

The table below lists the main source material used for this document. It is not a full file inventory; it identifies the sources behind the material claims.

| Topic | Source material |
| --- | --- |
| Analytics app and routers | analytics/main.py; analytics/api/routes/ |
| SQL schema/functions | database/init/02-schema.sql; database/init/03-timescaledb-setup.sql; database/init/04-functions.sql |
| Simulator | simulator/main.py; simulator/api/routes.py; simulator/simulator_manager.py; simulator/mqtt_publisher.py |
| Node-RED | nodered/data/flows.json; nodered/settings.js; nodered/package.json |
| Auth | auth-service/app.py; auth-service/auth_service.py; database/init/05-auth-schema.sql |
| Chatbot/Rasa | chatbot/server/index.js; chatbot/rasa/actions/actions.py; chatbot/rasa/qa_data.json |
| Validation performed | docker compose config --quiet for HumanEnerDIA production; docker compose -f <OVOS-EnMS repository>/docker-compose.yml config --quiet |
