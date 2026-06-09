# Docker Deployment Report

Project: WASABI / HumanEnerDIA / OVOS-EnMS
Version: 1.1
Date: 2026-06-09
Status: Final stakeholder-ready documentation package

Purpose: Document Docker Compose deployment, configuration, startup, verification, health checks, and operational troubleshooting.
Audience: Operators, deployment engineers, technical reviewers, and external partner infrastructure teams.

Source basis: Deployment claims are based on compose files, Dockerfiles, setup and verification scripts, and local compose validation.

## Deployment Overview

![Figure 1. Deployment preparation, setup, validation, build, start, and verification flow.](../assets/deployment-startup-flow.png)

The deployment target described by the repository is a Linux host running Docker Engine and Docker Compose v2. The GitHub production base stack is defined by docker-compose.yml. The separate OVOS-EnMS repository provides its own Compose file and should be deployed/validated separately when the assistant runtime is in scope.

The setup helper is the intended guided path. It creates .env from .env.example when needed, generates first-run secrets for placeholders, validates Docker Compose, builds images, and starts the stack. It also adjusts OVOS_BRIDGE_HOST when an optional OVOS compose file is present.

## Deployment Prerequisites

The repository does not install host Docker itself. Operators should prepare the host and confirm prerequisite tooling before running setup or Compose commands.

| Prerequisite | Source basis / action |
| --- | --- |
| Linux host or compatible container host | Deployment scripts assume a shell environment with Docker available. |
| Docker Engine and Docker Compose v2 | setup.sh requires docker and verifies docker compose version. |
| Outbound image/build access | Compose builds local images and pulls base images such as nginx, TimescaleDB, Redis, and Grafana. |
| curl and grep for verification | verify.sh requires curl and grep. |
| Optional openssl or /dev/urandom | setup.sh uses openssl rand when available for generated secrets, otherwise /dev/urandom. |
| Optional python3-bcrypt or Docker | setup.sh needs one path to generate the Node-RED bcrypt password hash. |
| Ports available | Default external ports include 8080, 8443, 5433, 1883, 9001, 3001, 1881, 8001, 8003, 5500, 5005, 5006, 5055, 6380, 5000, and 8181. |

## Compose Service Topology

![Figure 2. Docker Compose service topology and optional OVOS attachment.](../assets/docker-service-topology.png)

The base deployment uses one Docker bridge network for HumanEnerDIA services. Nginx is the browser/API gateway; analytics, auth-service, chatbot/Rasa, simulator, Node-RED, Grafana, PostgreSQL/TimescaleDB, MQTT, and Redis communicate on the internal network. OVOS-EnMS remains a separate assistant runtime in the GitHub production evidence and connects through the HumanEnerDIA-compatible API.

## Docker Compose Services

| Service | Image or build context | External port/path | Responsibility | Healthcheck |
| --- | --- | --- | --- | --- |
| nginx | nginx:1.25-alpine | 8080; 8443 mapped but HTTPS server block is optional/commented until certificates are configured | Public gateway, portal/static hosting, reverse proxy | Yes |
| postgres | timescale/timescaledb:latest-pg16 | 5433 | PostgreSQL with TimescaleDB extension and persistent data volume | Yes |
| mqtt | build ./mqtt | 1883, 9001 | Mosquitto telemetry broker with configured credentials | Yes |
| redis | redis:7-alpine | 6380 | Redis cache and Pub/Sub support for analytics event paths | Yes |
| simulator | build ./simulator | internal 8003 | FastAPI synthetic telemetry generator loaded from database machines | Yes |
| nodered | build ./nodered | 1881 | MQTT-to-database ingestion and automation flow runtime | Yes |
| grafana | grafana/grafana:10.2.0 | 3001, /grafana | Provisioned dashboards backed by PostgreSQL/TimescaleDB | Yes |
| analytics | build ./analytics | 8001, /api/analytics | FastAPI analytics, KPI, reports, ISO 50001, and OVOS proxy APIs | Yes |
| auth-service | build ./auth-service | 5500 | Flask auth, admin, contact, pilot/application APIs | Yes |
| rasa-actions | build ./chatbot/rasa | 5055 | Rasa custom action server | Yes |
| rasa | build ./chatbot/rasa | 5005 | Rasa NLU text chatbot server | Yes |
| chatbot | build ./chatbot | 5006 | Express backend and built chatbot frontend proxying to Rasa and OVOS | Yes |

## Networks, Volumes, And Ports

All HumanEnerDIA production Compose services join the Docker bridge network named by ENMS_NETWORK_NAME, defaulting to enms-network. OVOS-EnMS is documented as a separate assistant runtime rather than a service in the GitHub production base docker-compose.yml.

Persistent named volumes in the production Compose file include PostgreSQL data, MQTT data/logs, Redis data, Node-RED data, and Grafana data.

| Resource | Configured name/default | Purpose |
| --- | --- | --- |
| Network | ${ENMS_NETWORK_NAME:-enms-network} | Service-to-service communication |
| postgres-data | ${VOLUME_PREFIX:-enms}-postgres-data | PostgreSQL/TimescaleDB persistent data |
| grafana-data | ${VOLUME_PREFIX:-enms}-grafana-data | Grafana runtime data |
| redis-data | ${VOLUME_PREFIX:-enms}-redis-data | Redis append-only persistence |
| mqtt-data/logs | ${VOLUME_PREFIX:-enms}-mqtt-data and -mqtt-logs | Mosquitto runtime data and logs |

## Environment Variables And Configuration

.env.example is the safe public configuration template. The real .env file is intentionally not included and must not be committed or copied into documentation. The setup helper generates first-run values for placeholders and preserves existing non-placeholder values.

Important configuration groups include database credentials, Redis password, MQTT credentials, Grafana admin credentials, Node-RED credential secret and password hash, JWT secret, API key, server IP/frontend URL, Grafana root URL, simulator controls, OVOS bridge host/port/timeout, and SMTP/admin settings.

- Use .env.example in documentation, not .env.
- Rotate generated first-run credentials before production exposure.
- Set DNS, TLS, firewall rules, and public URLs explicitly for production.

## Environment Variable Groups

The table below summarizes configuration groups without reproducing private runtime values. Use .env.example and setup.sh as the source for expected keys.

| Group | Representative variables | Source basis |
| --- | --- | --- |
| Database | POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT | .env.example; docker-compose.yml; analytics/config.py |
| Service ports | NGINX_HTTP_PORT, ANALYTICS_PORT, SIMULATOR_PORT, GRAFANA_PORT, NODERED_PORT, RASA_PORT, CHATBOT_PORT, REDIS_EXTERNAL_PORT | .env.example; docker-compose.yml |
| Security and auth | JWT_SECRET, API_KEY, ADMIN_EMAILS, JWT expiration settings, Node-RED password hash/credential secret | .env.example; auth-service/auth_service.py; nodered/settings.js |
| Telemetry | MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, simulator intervals and anomaly settings | .env.example; simulator/config.py |
| Analytics behavior | LOG_LEVEL, scheduler settings, model storage, anomaly thresholds, cost/carbon defaults | analytics/config.py; .env.example |
| OVOS proxy/runtime | OVOS_BRIDGE_HOST, OVOS_BRIDGE_PORT, OVOS_BRIDGE_TIMEOUT, OVOS external ports | .env.example; analytics/api/routes/ovos_voice.py; OVOS-EnMS repository compose |

## Step-By-Step Deployment

The guided setup path should be used for normal evaluation deployment. Manual commands are appropriate when operators have already prepared .env and want explicit control over build/start timing.

| Step | Command / action | Expected result |
| --- | --- | --- |
| 1. Review source | Confirm current commit and inspect README.md, docker-compose.yml, .env.example. | Operator understands delivery scope and exposed services. |
| 2. Prepare .env | ./setup.sh or copy .env.example to .env and replace placeholders. | Private runtime configuration exists locally and is not committed. |
| 3. Validate Compose | docker compose config --quiet | Compose interpolation and syntax pass. |
| 4. Build images | docker compose build | Local service images are built. |
| 5. Start stack | docker compose up -d or setup.sh default start path. | Containers start on the configured network and volumes. |
| 6. Verify | docker compose ps, health endpoints, verify.sh when services are running. | Operator confirms live readiness before demo/handover. |

## Startup, Shutdown, And Clean Reinstall Procedures

Supported startup paths are ./setup.sh or manual Docker Compose commands after .env is prepared. Supported stop/start procedures use docker compose down/up or docker compose restart without deleting volumes. Destructive volume deletion is not part of routine operations.

| Procedure | Command or source | Notes |
| --- | --- | --- |
| Guided setup | ./setup.sh [--server-ip HOST] [--no-build] [--no-start] | Creates/updates .env, validates compose, builds and starts by default. |
| Manual validation | docker compose config | Base validation succeeded in this documentation pass. |
| Manual start | docker compose build; docker compose up -d | Use after .env has no placeholders. |
| Restart service | docker compose restart analytics | Use service-specific logs to confirm recovery. |
| Stop without deleting data | docker compose down | Keeps persistent volumes. |
| Clean reinstall | Only when data removal is intended; do not use down -v casually | Back up data first. |

## Verification Scripts And Health Checks

The repository provides verification scripts. These scripts are source material for intended operational checks, but their success depends on a running stack and reachable services. In this documentation run, compose validation was executed; live health checks were not implied.

| Check | Purpose | Source/status |
| --- | --- | --- |
| docker compose config --quiet | Validate Compose syntax/resolution | Ran successfully for base HumanEnerDIA stack. |
| OVOS-EnMS repository docker-compose.yml | Validate OVOS assistant Compose configuration separately | Ran successfully during documentation review. |
| verify.sh | Checks Compose config and live Nginx, analytics, and optional OVOS endpoints when a stack is running | Script exists in production repository; live checks were not run in this pass. |
| Chatbot/Rasa live checks | Use Compose healthchecks, service logs, and chatbot/Rasa endpoints when services are running | No production-tracked standalone chatbot verification script is cited. |
| Service healthchecks | Container-level checks for all production Compose services | Configured in docker-compose.yml. |

## Healthcheck Details

Compose healthchecks are present for the production service inventory. A healthy container does not prove business data quality, but it is the first operational signal for deployment readiness.

| Service | Healthcheck focus | Interpretation |
| --- | --- | --- |
| nginx | wget/curl style check to /health | Confirms gateway process responds, not full upstream health. |
| postgres | pg_isready | Confirms database accepts connections. |
| mqtt | mosquitto_pub/sub or broker health command | Confirms broker is reachable with configured credentials. |
| redis | redis-cli ping with password | Confirms Redis responds. |
| simulator | HTTP /health | Confirms simulator API process health. |
| nodered | HTTP admin/API health check | Confirms Node-RED runtime responds. |
| grafana | HTTP /api/health | Confirms Grafana process health. |
| analytics | HTTP /api/v1/health | Confirms analytics service and database checks exposed by route. |
| auth-service | HTTP /api/auth/health | Confirms Flask auth service responds. |
| rasa/rasa-actions/chatbot | HTTP health or root checks from Compose healthcheck | Confirms chatbot components respond. |

## Backup And Recovery

The production tree provides persistent volumes and tracked dashboard/flow configuration, but it does not provide a complete universal backup/restore automation. Operators should implement tested backup procedures before production data is at risk.

| Area | Recommended handling | Caution |
| --- | --- | --- |
| PostgreSQL/TimescaleDB | Use pg_dump/pg_restore or platform database backups before upgrades and before docker compose down -v. | No tracked generic database backup script exists in production. |
| Grafana dashboards | Keep intended dashboard JSON under grafana/dashboards and provisioning under grafana/provisioning. | Back up runtime edits before replacing Grafana volumes. |
| Node-RED flows | nodered/data/flows.json is tracked; credential-bearing runtime files should not be published. | Credential files are excluded from documentation. |
| Docker volumes | postgres-data, grafana-data, mqtt data/logs, redis-data, Node-RED data | Volume deletion is destructive. |
| Documentation package | Regenerate DOCX from docs/final-delivery/source/generate_delivery_docs.py and source Markdown/assets. | Keeps source and deliverables reproducible. |

## Upgrade And Redeployment

Redeployment should be treated as a controlled change. Take backups, rebuild images, restart services, and run smoke checks. If schema/data changes are introduced in future versions, rollback must include database/volume strategy, not only Git checkout.

| Phase | Action |
| --- | --- |
| Pre-upgrade | Confirm current commit, back up database/volumes, export dashboard changes, record .env keys without exposing values. |
| Build | docker compose build after pulling source changes or switching approved delivery bundles. |
| Redeploy | docker compose up -d; use --wait when supported by Docker Compose. |
| Smoke test | Run docker compose ps, service logs, /health endpoints, analytics /api/v1/health, and verify.sh when services are running. |
| Rollback | Return to the previous commit or approved delivery version and restore volumes/database backup if schema/data changed. |

## Troubleshooting Commands

These commands are safe static/live inspection commands when run by an operator with Docker access. They should not delete volumes or modify runtime state.

| Purpose | Command | Use |
| --- | --- | --- |
| List service state | docker compose ps | Shows container state, health, and exposed ports. |
| Inspect logs | docker compose logs <service> --tail=100 | Use owning service first: nginx, analytics, postgres, mqtt, nodered, grafana, auth-service, chatbot, rasa. |
| Validate configuration | docker compose config --quiet | Catches Compose syntax/interpolation errors. |
| Gateway health | curl -fsS http://localhost:8080/health | Expected healthy response from Nginx when stack is running. |
| Analytics health | curl -fsS http://localhost:8001/api/v1/health | Checks analytics service directly. |
| Verification script | HUMANERDIA_BASE_URL=... ANALYTICS_BASE_URL=... OVOS_BASE_URL=... ./verify.sh | Runs live checks; skips OVOS if bridge is unreachable. |

## Production Hardening Checklist

The checklist below is intentionally phrased as operator action. The repository provides hooks and configuration, but production hardening is not complete until these actions are performed in the target environment.

| Area | Required action |
| --- | --- |
| Credentials | Rotate generated setup secrets; use strong admin, database, Redis, MQTT, JWT, API, and Node-RED values. |
| Network exposure | Restrict direct service ports; expose only intended Nginx/TLS routes to external users. |
| TLS | Configure certificates in Nginx or an upstream reverse proxy before internet-facing use. |
| Runtime users | Review container users and file permissions; OVOS Dockerfile creates a non-root ovos user. |
| Backups | Implement tested backup/restore for database, dashboard changes, and operational volumes. |
| Monitoring | Add external monitoring/log collection for health endpoints, disk usage, restart counts, and data freshness. |
| Secrets hygiene | Never publish .env, runtime credential files, tokens, database dumps, or logs containing credentials. |

## Troubleshooting Scenarios

The repository provides deployment-oriented defaults, placeholders, health checks, and hardening notes, but it should not be represented as automatically production-hardened. Operator action is required for DNS, TLS, firewall restrictions, credential rotation, backups, and monitoring policy.

| Symptom | Likely area | First checks |
| --- | --- | --- |
| Portal does not load | Nginx or portal static files | curl /health; docker compose logs nginx |
| Analytics API returns 500 | Analytics, PostgreSQL, Redis | logs for analytics/postgres/redis; /api/v1/health |
| No new telemetry | Simulator, MQTT, Node-RED | logs for simulator/mqtt/nodered; Node-RED flow status |
| Grafana unavailable | Grafana or database | Grafana health endpoint; credentials and volume status |
| Auth errors | auth-service, database, SMTP | /api/auth/health; auth-service logs |
| OVOS voice path unavailable | OVOS bridge/messagebus or analytics proxy | OVOS /health; analytics /api/v1/ovos/voice/health |

## Limitations And Assumptions

The following items should be reviewed before stakeholder distribution. They are documented to avoid overstating the current implementation.

| Item | Status |
| --- | --- |
| Runtime verification | This documentation package records compose validation. Live health checks require a running deployment and are not implied unless run separately. |
| OVOS deployment boundary | The GitHub production base docker-compose.yml does not define an OVOS service. OVOS-EnMS is documented as a separate source repository and companion assistant runtime. |
| OVOS optional LLM fallback | The OVOS-EnMS Dockerfile installs LLM fallback dependencies only when INSTALL_LLM_FALLBACK=true. Model availability must be verified in the OVOS-EnMS repository/runtime. |
| Third-party EnMS support | OVOS portability is through a HumanEnerDIA-compatible API or adapter/proxy, not zero-code support for arbitrary vendor APIs. |
| Reports V2 | V2 report code is implemented, but some service calculations use derived/proportional or placeholder values; final stakeholders should review report semantics before audit use. |
| Simulator inventory | The simulator code supports boiler in addition to compressor, HVAC, motor, pump, and injection molding. One simulator info response still lists five machine types. |
| Security posture | The codebase provides secret placeholders, generated first-run credentials, JWT/bcrypt auth, health checks, and hardening guidance. Public production exposure still requires operator DNS/TLS/firewall/credential work. |

## Source References

The table below lists the main source material used for this document. It is not a full file inventory; it identifies the sources behind the material claims.

| Topic | Source material |
| --- | --- |
| Base compose | docker-compose.yml |
| Setup helper | setup.sh |
| Verifier | verify.sh |
| OVOS Docker | OVOS-EnMS repository: docker-compose.yml; Dockerfile; enms-ovos-skill/config.yaml.template; enms-ovos-skill/settings.docker.json; enms-ovos-skill/settingsmeta.yaml |
