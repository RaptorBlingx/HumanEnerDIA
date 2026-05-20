# HumanEnerDIA OVOS Skill for Industrial Energy Management

## Short Description

HumanEnerDIA is an OVOS-based Digital Intelligent Assistant for manufacturing
energy management. It lets operators query ISO 50001 energy performance,
machine status, anomalies, forecasts, KPIs, and action-plan context through
natural language.

## Product Type

Digital download, free/open distribution.

## Requirements

- Linux server or workstation with Docker.
- Open Voice OS compatible runtime.
- HumanEnerDIA/EnMS analytics API endpoint.
- Optional: `Qwen3.5-2B-Q4_K_M.gguf` for Tier-3 local LLM fallback.

## Installation Summary

1. Download and extract `HumanEnerDIA-OVOS-skill-v1.0.0.zip`.
2. Configure the backend API:

   ```bash
   export ENMS_API_URL=http://YOUR_ENMS_HOST:8001/api/v1
   ```

3. Install the skill:

   ```bash
   cd enms-ovos-skill
   python3 -m pip install -e .
   ```

4. Start the OVOS stack and REST bridge.
5. Run a smoke query:

   ```bash
   curl -sS -X POST http://localhost:5000/query \
     -H 'Content-Type: application/json' \
     -d '{"text":"what is the power of compressor one","session_id":"shop-smoke"}'
   ```

## License/IPR

The WASABI release artifact is offered under `Apache-2.0 OR GPL-3.0-or-later`.
The permissive Apache-2.0 option is provided for WASABI skill distribution.
Backend services and optional model weights may have separate licenses.

## Known Limitations

Fast-path operational queries are suitable for demonstration and shop release.
The optional local LLM fallback is slower and should be described as improving
robustness for difficult phrasing rather than solving every open-ended query.
