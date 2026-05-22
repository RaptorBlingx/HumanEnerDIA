# HumanEnerDIA Database Schema Reference

This reference summarizes the database objects created by the tracked SQL files
under `database/init/` and `database/migrations/`.

The runtime database is PostgreSQL with the TimescaleDB extension.

## Initialization Files

The first-start database setup is driven by files mounted into
`/docker-entrypoint-initdb.d` from `database/init/`.

Important files:

- `01-extensions.sql`: PostgreSQL and TimescaleDB extensions.
- `02-schema.sql`: core factories, machines, telemetry, baseline, anomaly,
  tariff, carbon, and audit tables.
- `03-timescaledb-setup.sql`: hypertables and continuous aggregates.
- `05-auth-schema.sql`: auth and session tables.
- `07-iso50001-schema.sql`: energy sources, SEUs, and SEU performance.
- `09-production-enhancements.sql`: baseline adjustments and data quality log.
- `10a-energy-source-features.sql`: energy-source feature mapping.
- `11-model-performance.sql`: legacy model performance history.
- `12-forecast-predictions.sql`: forecast output table.
- `13-model-performance-tracking.sql`: model metrics, training history, A/B
  tests, and alerts.
- `15-enpi-tracking-tables.sql`: EnPI baselines, performance, and targets.
- `16-action-plans-table.sql`: ISO/action-plan workflow table.

Migration files in `database/migrations/` mirror or extend parts of the init
schema for already-running databases. Confirm the target environment before
applying migrations manually.

## Core Tables

| Table | Purpose |
|---|---|
| `factories` | Factory/site records |
| `machines` | Machine/asset records linked to factories |
| `energy_readings` | High-frequency machine energy and power readings |
| `production_data` | Production output readings for normalization and SEC |
| `environmental_data` | Temperature, humidity, pressure, and related context |
| `machine_status` | Current or recent machine operating state |
| `energy_baselines` | Baseline model metadata and serialized model details |
| `anomalies` | Detected anomalies and resolution status |
| `energy_tariffs` | Tariff definitions for cost calculations |
| `carbon_factors` | Emission factors for carbon estimates |
| `audit_log` | Generic audit/event history |

## Time-Series Design

TimescaleDB hypertables are created for:

- `energy_readings`
- `production_data`
- `environmental_data`
- `energy_forecasts`

Continuous aggregates include:

- `energy_readings_1min`
- `energy_readings_15min`
- `energy_readings_1hour`
- `energy_readings_1day`
- `production_data_1min`
- `production_data_15min`
- `production_data_1hour`
- `production_data_1day`
- `environmental_data_1min`
- `environmental_data_15min`
- `environmental_data_1hour`
- `environmental_degree_days_daily`

The analytics service reads from both raw hypertables and aggregate views
depending on endpoint and time range.

## ISO 50001 and Energy Performance Tables

| Table | Purpose |
|---|---|
| `energy_sources` | Energy source types such as electricity or other configured sources |
| `seus` | Significant Energy Uses |
| `seu_energy_performance` | SEU performance periods and compliance status |
| `baseline_adjustments` | Adjustments to baseline assumptions |
| `data_quality_log` | Data quality checks and scores |
| `energy_source_features` | Regression feature mapping for energy sources |
| `enpi_baselines` | EnPI baseline definitions |
| `enpi_performance` | EnPI performance results |
| `energy_targets` | Energy target records |
| `action_plans` | Improvement action plans |

## Authentication and Portal Tables

| Table | Purpose |
|---|---|
| `demo_users` | User account records |
| `demo_sessions` | Active session records |
| `demo_audit_log` | Authentication and admin audit events |
| `pilot_factory_applications` | Pilot/application form submissions |

## Model and Forecast Tracking

| Table | Purpose |
|---|---|
| `model_performance_history` | Legacy model performance records |
| `energy_forecasts` | Forecasted energy outputs |
| `model_performance_metrics` | Model evaluation metrics and drift flags |
| `model_training_history` | Training job metadata and status |
| `model_ab_tests` | Model A/B test definitions |
| `model_alerts` | Model-related alerts |

## Operational Queries

Open a PostgreSQL shell:

```bash
set -a
source .env
set +a
docker exec -it enms-postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

List key tables:

```sql
\dt
```

Check recent energy readings:

```sql
SELECT machine_id, time, power_kw, energy_kwh
FROM energy_readings
ORDER BY time DESC
LIMIT 10;
```

Check aggregate freshness:

```sql
SELECT max(bucket) FROM energy_readings_1hour;
SELECT max(bucket) FROM energy_readings_1day;
```

Check unresolved anomalies:

```sql
SELECT machine_id, severity, detected_at, description
FROM anomalies
WHERE is_resolved = false
ORDER BY detected_at DESC
LIMIT 20;
```

## Schema Change Guidance

- Add new first-install objects under `database/init/`.
- Add migrations under `database/migrations/` for existing deployments.
- Test changes on a copy of production data before applying them to a live
  system.
- Update this reference whenever tables, views, or materialized views are
  added, renamed, or removed.

## Diagram Placeholder

- `docs/images/architecture/database-erd.png`
