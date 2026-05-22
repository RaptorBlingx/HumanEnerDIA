# HumanEnerDIA KPI Reference

This reference explains the main energy-performance terms used by HumanEnerDIA.
It is written for both technical and non-technical readers.

## Important Interpretation Rule

Energy KPIs are decision-support indicators. They should be interpreted with
production volume, operating schedule, maintenance events, weather, tariffs,
and data quality in mind. A single KPI change should not be treated as root
cause proof without operational review.

## Core KPIs

| KPI | Typical unit | Meaning |
|---|---:|---|
| Energy consumption | kWh | Total energy used over a selected period |
| Power demand | kW | Instantaneous or aggregated power draw |
| Peak demand | kW | Highest power draw in a selected period |
| Specific Energy Consumption (SEC) | kWh/unit | Energy used per unit of production |
| Load factor | ratio or percent | Average demand divided by peak demand |
| Energy cost | currency | Estimated cost from configured tariffs |
| Carbon indicator | kg CO2e | Estimated emissions from configured emission factor |
| Baseline deviation | kWh or percent | Difference between actual and expected baseline energy |
| Anomaly severity | category | Relative seriousness of unusual behavior |

## Specific Energy Consumption

SEC shows how much energy is used per production unit.

```text
SEC = energy consumption / production quantity
```

Interpretation:

- lower SEC usually indicates better energy efficiency
- compare SEC only across similar products, lines, or operating modes
- low production volume can make SEC unstable
- missing production data makes SEC unreliable

## Peak Demand

Peak demand is the highest power draw during a selected time period.

Use it to:

- find demand spikes
- review simultaneous high-load operations
- understand demand-related cost risk
- identify opportunities for load scheduling

Peak demand should be reviewed with shift schedules, startup events, and
maintenance activity.

## Load Factor

Load factor compares average demand to peak demand.

```text
Load factor = average demand / peak demand
```

Interpretation:

- higher load factor usually means steadier energy use
- lower load factor can indicate spikes or irregular operating patterns
- the "best" value depends on the plant process and production schedule

## Baselines and Deviations

An energy baseline estimates expected energy use for a given operating context.
HumanEnerDIA stores baseline model metadata in `energy_baselines` and related
model-performance tables.

Baseline deviation compares actual energy use with expected energy use.

```text
Deviation = actual energy - baseline energy
```

Interpretation:

- positive deviation usually means actual energy is higher than expected
- negative deviation usually means actual energy is lower than expected
- deviations require context such as production, weather, pressure, load, or
  maintenance conditions

## Anomalies

Anomaly records are stored in the `anomalies` table. They identify unusual
patterns in energy or machine behavior.

An anomaly should trigger investigation, not automatic blame. Confirm:

- whether the affected machine was operating normally
- whether production volume changed
- whether maintenance or downtime occurred
- whether sensor or ingestion data was missing
- whether weather or process conditions changed

## ISO 50001 Terms

| Term | Meaning |
|---|---|
| SEU | Significant Energy Use; equipment, process, or area with material energy impact |
| EnPI | Energy Performance Indicator; metric used to track energy performance |
| EnB | Energy Baseline; reference used to compare energy performance |
| Action plan | Structured improvement action with owner, priority, dates, and status |

HumanEnerDIA stores ISO-oriented information in tables such as `seus`,
`seu_energy_performance`, `enpi_baselines`, `enpi_performance`,
`energy_targets`, and `action_plans`.

## Data Quality Considerations

Treat KPIs cautiously when:

- telemetry ingestion stopped
- production data is missing
- selected period is too short
- machines were offline or under maintenance
- baselines were recently retrained
- sensor calibration changed
- simulator data is being used instead of real sensor data

## Screenshot Placeholders

- `docs/images/user-guide/kpi-dashboard.png`
- `docs/images/user-guide/anomaly-detail.png`
- `docs/images/user-guide/baseline-deviation.png`
