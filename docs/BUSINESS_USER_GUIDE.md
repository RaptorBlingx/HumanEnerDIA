# HumanEnerDIA Business User Guide

This guide is for plant managers, energy managers, operators, auditors, and
other non-technical users who need to understand and use HumanEnerDIA outputs.

## What HumanEnerDIA Provides

HumanEnerDIA helps teams monitor industrial energy performance and review
ISO 50001-oriented information in one place.

Typical tasks:

- review factory and machine energy use
- identify high-consumption equipment
- track energy performance indicators such as SEC and peak demand
- review anomalies and unusual operating patterns
- open Grafana dashboards for detailed visualization
- generate or review reports where reporting features are enabled
- use the assistant/voice integration when the OVOS companion stack is deployed

## Accessing the Portal

1. Open the HumanEnerDIA URL provided by your administrator.
2. Log in if the page requires authentication.
3. Use the portal navigation to open dashboards, reports, ISO 50001 pages, or
   assistant features.

Default local development URL:

```text
http://localhost:8080
```

On a server, replace `localhost` with the server host name or IP address.

Screenshot placeholder:

![Portal home placeholder](./images/user-guide/portal-home.png)

## Key Pages and Tools

| Area | What it is used for |
|---|---|
| Portal home | Entry point for HumanEnerDIA pages and status panels |
| Analytics UI | Service status, analytics views, and API-backed operational data |
| Grafana | Detailed dashboards for energy, production, machine health, ML performance, ISO 50001, and cost analytics |
| Reports page | Report-oriented user workflows where enabled |
| ISO 50001 page | Energy-performance and EnPI-oriented views |
| Chatbot/assistant | Text assistant path through the Rasa chatbot |
| OVOS voice widget | Voice/assistant path when the OVOS bridge is deployed |

## Reviewing Energy Performance

1. Open the portal or Grafana dashboard.
2. Select the factory, machine, or SEU where dashboard filters are available.
3. Review the selected time period.
4. Compare energy use, power, production, and anomaly indicators.
5. Record operational explanations for unusual peaks or drops.

Screenshot placeholder:

![Energy dashboard placeholder](./images/user-guide/energy-dashboard.png)

## Understanding Core KPIs

| KPI | Meaning | How to interpret it |
|---|---|---|
| SEC | Specific Energy Consumption, usually energy per production unit | Lower is often better, but compare only similar products, periods, and operating conditions |
| Peak demand | Highest power draw in a period | High peaks can increase cost and may indicate simultaneous loads |
| Load factor | Average load divided by peak load | Higher values often mean steadier energy use |
| Energy cost | Estimated cost from tariffs and energy use | Depends on configured tariffs and peak/off-peak assumptions |
| Carbon indicator | Estimated emissions from energy use | Depends on the configured emission factor |
| Baseline deviation | Difference between actual energy use and expected baseline | Positive deviation may indicate worse-than-expected energy performance |
| Anomaly | Unusual pattern detected from monitored data | Requires operational review before assigning cause |

See [KPI_REFERENCE.md](./KPI_REFERENCE.md) for more detailed definitions.

## Reviewing Anomalies

An anomaly means HumanEnerDIA detected behavior that differs from expected
patterns. It does not automatically prove a fault.

When reviewing an anomaly:

1. Check the affected machine and time period.
2. Compare the anomaly with production, maintenance, shift, and weather context.
3. Confirm whether the event is explainable.
4. Escalate unexplained anomalies to the technical or energy team.

## Reports

Report availability depends on the deployed features and data quality.

Recommended practice:

1. Select the correct reporting period.
2. Confirm the underlying data period is complete.
3. Generate or export the report.
4. Review values before sending to management or external stakeholders.
5. Store the final report with a clear filename, such as
   `site-report-type-period-version`.

Screenshot placeholder:

![Report workflow placeholder](./images/user-guide/report-export.png)

## Assistant and Voice Queries

If the companion OVOS stack is deployed, users can ask energy questions in
natural language.

Example questions:

- "What is the status of Compressor-1?"
- "How much energy did Boiler-1 use yesterday?"
- "Show the top three energy consumers."
- "Forecast energy for tomorrow."
- "Give me a factory overview."

If the assistant gives an unclear or incomplete answer, try a shorter question
with the machine name and time period included.

## When to Contact Technical Support

Contact support when:

- the portal or Grafana does not load
- login fails or your role does not have expected access
- dashboard values stop updating
- expected machines are missing
- a report cannot be generated
- KPI values appear inconsistent with known operations
- assistant answers repeatedly fail for simple supported questions

Include:

- page URL
- screenshot
- time and date in UTC if possible
- machine, factory, or report period involved
- what you expected and what happened instead

## Screenshot Placeholders

- `docs/images/user-guide/portal-home.png`
- `docs/images/user-guide/energy-dashboard.png`
- `docs/images/user-guide/report-export.png`
- `docs/images/user-guide/ovos-widget.png`
