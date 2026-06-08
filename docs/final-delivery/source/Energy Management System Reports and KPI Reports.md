# Energy Management System Reports and KPI Reports

Project: WASABI / HumanEnerDIA / OVOS-EnMS
Version: 1.0
Date: 2026-06-08
Status: Final delivery documentation package

Purpose: Document implemented energy data, KPI, dashboard, and report capabilities with formulas and evidence.
Audience: Energy managers, project reviewers, operators, analytics maintainers, and external partners.

Evidence rule: KPI formulas are included only where defined in SQL functions, code, dashboard queries, or existing local documentation.

## Energy Data Model

![Figure 1. Data path from telemetry to KPI/report consumers.](../assets/telemetry-data-flow.png)

HumanEnerDIA stores factory/site records, machines/SEUs, high-frequency energy readings, production data, environmental context, machine status, baseline metadata, anomaly records, tariffs, carbon factors, audit records, ISO 50001 entities, model tracking, forecast output, and action plans.

The first-start seed data defines two sample factories and eight sample machines across the demo and European facilities. The machine examples include Compressor-1, HVAC-Main, Conveyor-A, Hydraulic-Pump-1, Injection-Molding-1, Boiler-1, Compressor-EU-1, and HVAC-EU-North.

| Concept | Implemented representation | Evidence |
| --- | --- | --- |
| Factories | factories table and seed data for Demo Manufacturing Plant and European Production Facility | database/init/02-schema.sql; 06-seed-data.sql |
| Machines/SEUs | machines table plus ISO-oriented seus and SEU performance tables | database/init/02-schema.sql; 07-iso50001-schema.sql |
| Energy readings | energy_readings hypertable with energy_type, power, energy, electrical quality fields, metadata | database/init/02-schema.sql; 03-timescaledb-setup.sql |
| Production data | production_data hypertable for production count, quality, throughput, mode, downtime | database/init/02-schema.sql |
| Environmental data | environmental_data hypertable for temperature, humidity, pressure, flow, HVAC, vibration context | database/init/02-schema.sql |
| Energy sources | energy_sources and energy_source_features support multi-energy/source-aware modeling | database/init/07-iso50001-schema.sql; 10a-energy-source-features.sql |

## KPI Formula Evidence

The following KPI formulas are implemented as database functions and wrapped by analytics/services/kpi_service.py. Some additional API routes compute aggregate factory cost/carbon estimates with constants; those should be described as route-level estimates rather than tariff/factor driven SQL functions.

| KPI | Formula or calculation | Implementation | Evidence |
| --- | --- | --- | --- |
| Specific Energy Consumption | SEC = total energy kWh / total production units | calculate_sec() over energy_readings_1hour and production_data_1hour | database/init/04-functions.sql; /api/v1/kpi/sec |
| Peak demand | Maximum 15-minute peak_demand_kw in selected period | calculate_peak_demand() over energy_readings_15min | database/init/04-functions.sql; /api/v1/kpi/peak-demand |
| Load factor | Average power divided by maximum power | calculate_load_factor() over energy_readings_15min | database/init/04-functions.sql; /api/v1/kpi/load-factor |
| Energy cost | Energy multiplied by tariff rate; active time-of-use tariff selected when configured | calculate_energy_cost() queries energy_tariffs with default fallback rate | database/init/04-functions.sql; /api/v1/kpi/energy-cost |
| Carbon intensity/emissions | Energy multiplied by active carbon factor, with default factor fallback | calculate_carbon_intensity() queries carbon_factors | database/init/04-functions.sql; /api/v1/kpi/carbon |
| Combined KPI response | Aggregates SEC, peak demand, load factor, cost, and carbon | calculate_all_kpis() and KPIService.calculate_all_kpis() | database/init/04-functions.sql; analytics/services/kpi_service.py |

## Analytics Endpoints And Modules

| Capability area | Implemented routes/modules | Notes |
| --- | --- | --- |
| KPI | /api/v1/kpi/sec, /factory, /factories, /peak-demand, /load-factor, /energy-cost, /carbon, /all | Machine and factory KPI endpoints exist; formulas vary by endpoint. |
| Baselines | /baseline/train, /deviation, /predict, /models, /drivers, /train-seu | ML baseline model metadata and saved model files are present. |
| Forecasts | /forecast/train/arima, /train/prophet, /predict, /demand, /optimal-schedule, /models, /peak, /short-term | Uses forecasting model modules and forecast prediction tables. |
| Anomalies | /anomaly/create, /detect, /search, /recent, /active, /resolve | Anomaly detection and search APIs with anomaly table evidence. |
| Performance and ISO 50001 | /performance/analyze, /opportunities, /action-plan, /health; /iso50001/* | Performance engine and ISO 50001 action-plan/reporting workflows are implemented. |
| Production | /production/{machine_id} | Production metrics and related energy/cost/carbon estimates are exposed. |
| Reports | /reports/generate, /preview, /v2/generate, /v2/download/{id}, /v2/status | Legacy monthly EnPI PDF and newer V2 report system exist. |

## Grafana Dashboard Capabilities

Grafana provisioning and dashboard JSON files are present. The dashboard inventory below is based on the tracked JSON dashboard titles and panel names. Dashboard presence is evidence of configured reporting views, while exact metric correctness should be reviewed against each panel SQL query for audit-grade use.

| Dashboard | Panel themes |
| --- | --- |
| SOTA Factory Overview | Active machines, energy today, cost today, active anomalies, current power, machine status |
| SOTA Machine Health | Health score, current power, baseline variance, production, actual vs baseline, anomalies |
| SOTA ISO 50001 EnPI | EnPI score, energy savings, compliance rate, CUSUM, baseline vs actual, SEU performance |
| SOTA Energy Cost Analytics | Cost trend, time-of-use cost, top cost contributors, savings opportunities |
| SOTA Environmental Impact | Monthly carbon footprint, CO2 trend, emission intensity, emissions by machine |
| SOTA Predictive Analytics | Forecast metrics, forecast vs actual, accuracy trends, recent forecasts |
| SOTA Anomaly Detection | Active and critical anomalies, severity distribution, machine-hour heatmap, unresolved list |
| SOTA ML Model Performance | Active models, R2/RMSE, model performance trends, training history |
| SOTA Operational Efficiency | OEE, availability, performance rate, production vs energy efficiency |
| SOTA Real-Time Production | Live factory status, active machines, current power |
| SOTA Executive Summary | Operational concerns, 12-month energy trend, energy intensity, monthly summary |

## Node-RED Ingestion Pipeline

The tracked Node-RED flow subscribes to MQTT topic factory/# and includes function nodes for topic parsing, route selection, payload validation, database preparation, success counting, error catching, and a 30-second statistics dashboard update. Credential files are intentionally not inspected or reproduced in this package.

| Flow area | Observed nodes | Evidence |
| --- | --- | --- |
| Input | MQTT in node Subscribe: factory/# | nodered/data/flows.json |
| Routing | Parse Topic, Route by Type | nodered/data/flows.json |
| Processing | Process Energy, Process Production, Process Environmental, Process Status | nodered/data/flows.json |
| Storage | PostgreSQL nodes via node-red-contrib-postgresql | nodered/package.json; nodered/data/flows.json |
| Monitoring/errors | Count Success, Catch All Errors, Log Error, Stats Dashboard | nodered/data/flows.json |

## Report Generation Capabilities

The legacy report path exposes a monthly_enpi report type, generates report data, generates machine and daily trend charts, and returns a ReportLab PDF. The V2 report path creates a report id, writes a PDF under /tmp, and exposes a download endpoint. V2 components include cover page, executive dashboard, energy overview, machine analysis, cost analysis, and carbon analysis templates/components.

Important caution: the V2 generator is implemented, but some values are derived or placeholder-like in code. Examples include proportional cost/carbon trend assumptions and constant efficiency sparkline values. The final report should therefore be presented as implemented reporting capability, not as independently audited KPI methodology.

| Report path | Implemented behavior | Evidence |
| --- | --- | --- |
| Legacy monthly EnPI | GET /types, POST /generate, GET /preview for monthly_enpi | analytics/api/routes/reports.py; analytics/reports/monthly_enpi_report.py |
| V2 PDF report | POST /v2/generate, GET /v2/download/{report_id}, GET /v2/status | analytics/api/routes/reports.py; analytics/reports_v2/services/report_service.py |
| V2 templates | Base, header/footer, KPI cards, chart containers, cover, executive dashboard, energy overview, machine ranking/profile, cost, carbon sections | analytics/reports_v2/templates/ |

## Implemented, Configured, Partial, And Demo Data Distinctions

| Capability | Classification | Reason |
| --- | --- | --- |
| TimescaleDB energy/production/environmental storage | Supported by implementation | Tables, hypertables, and aggregate views are created by SQL init scripts. |
| SEC, peak demand, load factor, cost, carbon KPI functions | Supported by implementation | SQL functions and service wrappers exist. |
| Grafana dashboards | Configured | Dashboard JSON and provisioning are tracked. |
| Node-RED ingestion | Configured and implemented | Flow nodes and settings are tracked; runtime execution not verified in this pass. |
| Sample factories and machines | Demo/sample data | Seed SQL inserts named sample facilities and machines. |
| V2 report polish/semantic completeness | Partially implemented | Routes/templates exist, but some data calculations are placeholders or estimates. |
| Standalone query API service | Out of scope | No separate natural-language query API service is defined in the GitHub production docker-compose.yml. |

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
| KPI functions | database/init/04-functions.sql |
| KPI routes and service | analytics/api/routes/kpi.py; analytics/services/kpi_service.py |
| Report routes/services | analytics/api/routes/reports.py; analytics/reports/; analytics/reports_v2/ |
| Database schema | database/init/02-schema.sql; database/init/03-timescaledb-setup.sql; database/init/04-functions.sql |
| Node-RED | nodered/data/flows.json; nodered/settings.js; nodered/package.json |
| Grafana | grafana/provisioning/; grafana/dashboards/ |
| Simulator seed data | database/init/06-seed-data.sql |
