# Skill Documentation

Project: WASABI / HumanEnerDIA / OVOS-EnMS
Version: 1.0
Date: 2026-06-08
Status: Final delivery documentation package

Purpose: Document the OVOS-EnMS skill, REST bridge, parser, validation, API client, and response behavior.
Audience: OVOS integrators, WASABI technical reviewers, backend maintainers, and external partners.

Evidence rule: OVOS-EnMS evidence comes from /home/ubuntu/ovos-llm, with HumanEnerDIA API integration evidence from /home/ubuntu/humanergy.

## Purpose And Boundaries

The HumanEnerDIA OVOS skill is the natural-language assistant layer for industrial energy-management questions. It is not the HumanEnerDIA backend and does not own telemetry storage or KPI calculation. It connects to a reachable HumanEnerDIA-compatible analytics API.

The production integration boundary is the HumanEnerDIA-compatible REST API. The repository includes adapter abstractions, but v1.0.0 documentation states that arbitrary third-party EnMS APIs require an adapter or proxy that exposes the expected API contract.

## Deployment And Configuration

The OVOS repository provides a Docker Compose service that exposes the REST bridge on port 5000 and the OVOS messagebus on port 8181. The full-stack HumanEnerDIA release can include an OVOS overlay that builds from ./ovos-stack and joins the enms-network.

Key configuration includes ENMS_API_URL, OVOS_BRIDGE_PORT, STRUCTURED_RESPONSE_GRACE_SECONDS, OVOS_TTS_ENABLED, LOG_LEVEL, OVOS_CONFIG_PATH, and XDG_CONFIG_HOME. Skill-level settings include enms_api_base_url, llm_model_path, confidence_threshold, and progress feedback options.

| Configuration item | Observed default or behavior | Evidence |
| --- | --- | --- |
| ENMS_API_URL | Docker default points at a HumanEnerDIA-compatible /api/v1 backend | /home/ubuntu/ovos-llm/docker-compose.yml |
| enms_api_base_url | Skill setting for backend API URL | settings.docker.json; settingsmeta.yaml |
| confidence_threshold | Default 0.85 in settings and validator configuration | settings.docker.json; lib/validator.py |
| INSTALL_LLM_FALLBACK | Build argument for installing optional LLM dependencies in the Dockerfile | /home/ubuntu/ovos-llm/Dockerfile |

## Query Lifecycle

![Figure 1. REST bridge, messagebus, skill, API, and response lifecycle.](../assets/ovos-query-lifecycle.png)

The REST bridge exposes GET /health and POST /query. POST /query/voice is an alias used by the analytics proxy when audio-capable flows request the same bridge behavior.

For each query, the bridge creates or uses a session id, emits recognizer_loop:utterance to the OVOS messagebus, and waits for a speak message plus, when available, an enms.skill.response structured payload. The response returns success status, spoken response text, intent, confidence, data, insights, timestamp, and session id.

The EnMS skill receives the utterance through OVOS intent handlers or fallback handling. It parses the utterance, validates intent/entity output, calls the configured backend API, formats a deterministic response, speaks it, and emits structured response data for the bridge or portal widget.

## Supported Intent And Query Families

The active IntentType enum and skill handlers show the supported query families below. This table is not a guarantee that every phrasing is understood; it identifies implemented categories in the skill code.

| Intent family | Purpose |
| --- | --- |
| energy_query | Energy use questions by machine or factory scope |
| power_query | Current or historical power demand questions |
| machine_status | Machine running/offline/status checks |
| factory_overview | Factory/facility summaries, machine lists, aggregate status |
| comparison | Machine-to-machine comparisons |
| ranking | Top or lowest machines by energy, power, cost, efficiency, or alerts |
| anomaly_detection | Active/recent anomaly and alert queries |
| cost_analysis | Cost and spending questions |
| forecast | Forecasted demand and future energy usage |
| baseline, baseline_models, baseline_explanation | Baseline prediction, model inventory, and driver explanation |
| driver_analysis | Energy driver analysis for factory or SEU/machine context |
| seus | Significant Energy Use listing and context |
| kpi, performance, production | KPIs, performance analysis, production/OEE-related queries |
| report | Report type, preview, and generation workflows |
| help, health | Capability help and system health checks |

## Intent Parsing And Routing

The parser is hybrid. Tier 1 is regex-based heuristic routing for common operational queries. Tier 2 uses Adapt pattern matching and registered vocabulary. Tier 3 is an optional local Qwen GGUF LLM parser used as fallback when dependencies and model files are available.

The active parser code includes patterns for production, anomaly detection, forecasts, KPIs, performance, baselines, driver analysis, SEUs, rankings, factory overview, status, power, and related query types. Adapt vocabulary registers machine names, spoken number variants, energy/power/status/cost/KPI/factory/comparison/time/forecast/anomaly/help terms and more.

| Tier | Implementation | Important note |
| --- | --- | --- |
| Heuristic | Regex patterns in lib/intent_parser.py | Fast path for common operational wording. |
| Adapt | IntentDeterminationEngine in lib/adapt_parser.py | Pattern/vocabulary matching with registered machine and domain terms. |
| LLM | Qwen3Parser in lib/llm_parser.py | Optional fallback requiring llama-cpp-python and a GGUF model file. |

## Validation And Fuzzy Matching

Validation is deliberately conservative. The validator builds a Pydantic Intent model, checks confidence, rejects unknown intent types, validates machine names against a whitelist, supports fuzzy matching and number-word normalization, detects ambiguity, validates multi-machine comparisons, and performs soft metric validation.

Machine discovery can refresh the whitelist from the backend API during runtime; fallback machine names are configured for cases where API discovery fails. This helps prevent hallucinated machine names from becoming backend calls.

## Backend API Client And Adapter Behavior

The ENMSClient wraps async HTTP calls to the configured backend. It uses connection pooling, request timeout management, and tenacity retry behavior that retries connection/timeouts and server-side 5xx responses while avoiding retries on ordinary 4xx client errors.

Client methods cover health, stats, machines, time series, top consumers, anomalies, KPIs, performance opportunities, action plans, forecasts, baseline models/explanations, SEU/energy-source data, reports, and ISO 50001 EnPI/action-plan endpoints. The production path remains HumanEnerDIA-compatible API usage.

| Client area | Representative methods | Evidence |
| --- | --- | --- |
| System and machines | health_check, system_stats, factory_summary, list_machines, get_machine_status | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/api_client.py |
| Telemetry | get_energy_timeseries, get_power_timeseries, get_latest_reading, get_multi_machine_energy | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/api_client.py |
| Analytics | detect_anomalies, get_all_kpis, analyze_performance, forecast_demand, predict_baseline | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/api_client.py |
| Reports and ISO | get_enpi_report, list_action_plans, get_report_types, preview_report, generate_report | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/api_client.py |

## Response Formatting

The response formatter uses Jinja2 templates and custom number/unit/time filters. The formatter documentation and code explicitly state that final responses should come from API data and templates rather than free-form LLM generation.

Additional enrichment exists for anomaly responses, including severity grouping, resolved/unresolved counts, metric/anomaly label humanization, and concise spoken examples.

## Example Supported Queries

- What is the power of Compressor-1?
- Is HVAC-Main running?
- How much energy did Boiler-1 use yesterday?
- Show me the top three energy consumers.
- Any anomalies today?
- What is tomorrow's energy forecast?
- Give me a factory overview.
- List SEUs.
- Generate a monthly energy report.

## Optional LLM Fallback

The default release documentation states that fast heuristic and Adapt routing are the normal path and that large GGUF model files are not bundled by default. The local development tree contains model files, but release packaging excludes models. To enable local LLM fallback in the release path, the operator must provide the GGUF model under the skill models directory and build with INSTALL_LLM_FALLBACK=true.

The LLM parser uses llama-cpp-python when installed, loads a configured GGUF model, performs deterministic JSON intent classification, and returns None on missing dependencies, missing model, parse failures, or timeout. It should be documented as optional fallback, not as required normal operation.

## Limitations And Assumptions

The following items should be reviewed before stakeholder distribution. They are documented to avoid overstating the current implementation.

| Item | Status |
| --- | --- |
| query-service | Placeholder only; Docker service exists, healthcheck disabled, and it is excluded from release readiness expectations. |
| Runtime verification | This documentation package records compose validation. Live health checks require a running deployment and are not implied unless run separately. |
| OVOS release artifact | The OVOS source tree may contain local GGUF model files, but release notes state optional GGUF weights are not bundled by default. |
| Third-party EnMS support | OVOS portability is through a HumanEnerDIA-compatible API or adapter/proxy, not zero-code support for arbitrary vendor APIs. |
| Reports V2 | V2 report code is implemented, but some service calculations use derived/proportional or placeholder values; final stakeholders should review report semantics before audit use. |
| Simulator inventory | The simulator code supports boiler in addition to compressor, HVAC, motor, pump, and injection molding. One simulator info response still lists five machine types. |
| Security posture | The codebase provides secret placeholders, generated first-run credentials, JWT/bcrypt auth, health checks, and hardening guidance. Public production exposure still requires operator DNS/TLS/firewall/credential work. |

## Evidence References

The table below lists the main local evidence used for this document. It is not a full file inventory; it identifies the sources behind the material claims.

| Topic | Evidence |
| --- | --- |
| REST bridge | /home/ubuntu/ovos-llm/enms-ovos-skill/bridge/ovos_rest_bridge.py |
| Skill lifecycle and handlers | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/__init__.py |
| Intent parser tiers | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/intent_parser.py; lib/adapt_parser.py; lib/llm_parser.py |
| Validation | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/validator.py |
| API client | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/api_client.py |
| Response formatter | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/response_formatter.py |
| Configuration and deployment | /home/ubuntu/ovos-llm/docker-compose.yml; Dockerfile; enms-ovos-skill/config.yaml.template; settings.docker.json; settingsmeta.yaml |
