# Evidence Map

Project: WASABI / HumanEnerDIA / OVOS-EnMS
Generated: 2026-06-08

This file maps recurring documentation claims to local evidence. It intentionally avoids .env values and credential-bearing runtime files.

| Key | Evidence |
| --- | --- |
| analytics_main | analytics/main.py |
| analytics_models | analytics/models/ |
| analytics_routes | analytics/api/routes/ |
| analytics_services | analytics/services/ |
| auth | auth-service/app.py; auth-service/auth_service.py; database/init/05-auth-schema.sql |
| chatbot | chatbot/server/index.js; chatbot/rasa/actions/actions.py; chatbot/rasa/qa_data.json |
| compose | docker-compose.yml |
| compose_ovos_overlay | scripts/release/docker-compose.ovos.yml |
| database_schema | database/init/02-schema.sql; database/init/03-timescaledb-setup.sql; database/init/04-functions.sql |
| grafana | grafana/provisioning/; grafana/dashboards/ |
| nginx | nginx/nginx.conf; nginx/conf.d/default.conf |
| nodered | nodered/data/flows.json; nodered/settings.js; nodered/package.json |
| ovos_bridge | /home/ubuntu/ovos-llm/enms-ovos-skill/bridge/ovos_rest_bridge.py |
| ovos_client | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/api_client.py |
| ovos_config | /home/ubuntu/ovos-llm/docker-compose.yml; Dockerfile; enms-ovos-skill/config.yaml.template; settings.docker.json; settingsmeta.yaml |
| ovos_formatter | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/response_formatter.py |
| ovos_parser | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/intent_parser.py; lib/adapt_parser.py; lib/llm_parser.py |
| ovos_readme | /home/ubuntu/ovos-llm/README.md; /home/ubuntu/ovos-llm/enms-ovos-skill/README.md |
| ovos_skill | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/__init__.py |
| ovos_validator | /home/ubuntu/ovos-llm/enms-ovos-skill/enms_ovos_skill/lib/validator.py |
| reports | analytics/api/routes/reports.py; analytics/reports/; analytics/reports_v2/ |
| seed_data | database/init/06-seed-data.sql |
| setup | setup.sh |
| simulator | simulator/main.py; simulator/api/routes.py; simulator/simulator_manager.py; simulator/mqtt_publisher.py |
| verify_release | scripts/verify-wasabi-release.sh |

## Validation Performed

- `docker compose config --quiet` in `/home/ubuntu/humanergy`: passed.
- `docker compose -f /home/ubuntu/ovos-llm/docker-compose.yml config --quiet`: passed.
- Runtime health checks were not run by this generator; they require a running deployment.
