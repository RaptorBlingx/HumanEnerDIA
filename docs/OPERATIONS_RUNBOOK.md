# HumanEnerDIA Operations Runbook

This runbook is for operators and maintainers responsible for running
HumanEnerDIA after deployment.

## Operational Baseline

Default deployment:

- Compose file: `docker-compose.yml`
- Optional full-stack OVOS file in release bundles: `docker-compose.ovos.yml`
- Network: `${ENMS_NETWORK_NAME:-enms-network}`
- Container prefix: `${CONTAINER_PREFIX:-enms}`
- Main gateway: `http://<host>:8080`

The `query-service` container is a placeholder. It is expected to run, but it
does not provide a production query API and is intentionally excluded from
release readiness checks.

## Daily Checks

Run from the repository or extracted release bundle directory.

```bash
docker compose ps
curl -fsS http://localhost:8080/health
curl -fsS http://localhost:8001/api/v1/health
curl -fsS http://localhost:5500/api/auth/health
curl -fsS http://localhost:5006/health
```

Confirm:

- `enms-nginx`, `enms-postgres`, `enms-mqtt`, `enms-redis`,
  `enms-analytics`, `enms-auth-service`, `enms-grafana`, `enms-nodered`,
  `enms-rasa-actions`, `enms-rasa`, and `enms-chatbot` are running.
- Portal loads at `http://localhost:8080`.
- Grafana loads through `http://localhost:8080/grafana`.
- Analytics UI loads through `http://localhost:8080/analytics/ui/`.
- Simulator is producing data when `SIMULATOR_AUTO_START=true`.

Screenshot placeholder:

![Container health placeholder](./images/operations/containers-healthy.png)

## Startup Procedure

1. Run the setup helper, which creates `.env` and generates first-run secrets
   when needed:

   ```bash
   ./setup.sh
   ```

2. For manual starts, confirm `.env` exists and has no `<CHANGE_ME...>`
   placeholders.
3. Validate Compose:

   ```bash
   docker compose --env-file .env -f docker-compose.yml config
   ```

4. Build and start manually only when bypassing `setup.sh`:

   ```bash
   docker compose build
   docker compose up -d
   ```

5. Verify health endpoints:

   ```bash
   curl -fsS http://localhost:8080/health
   curl -fsS http://localhost:8001/api/v1/health
   curl -fsS http://localhost:5500/api/auth/health
   ```

5. Open the portal and Grafana in a browser.

## Restart Procedure

Restart one service:

```bash
docker compose restart analytics
docker compose logs -f --tail=100 analytics
```

Restart the full stack:

```bash
docker compose restart
docker compose ps
```

Stop and start without deleting volumes:

```bash
docker compose down
docker compose up -d
```

Do not use `docker compose down -v` unless the goal is to remove persistent
data volumes.

## Logs

Common log commands:

```bash
docker compose logs -f --tail=200 nginx
docker compose logs -f --tail=200 analytics
docker compose logs -f --tail=200 auth-service
docker compose logs -f --tail=200 nodered
docker compose logs -f --tail=200 simulator
```

For data ingestion issues, inspect `mqtt`, `nodered`, `simulator`, and
`postgres` together.

## Incident Severity

| Severity | Meaning | Examples |
|---|---|---|
| SEV-1 | Platform unavailable or data-loss risk | PostgreSQL down, Nginx inaccessible, corrupt volume |
| SEV-2 | Core function degraded | Analytics API down, Grafana inaccessible, ingestion stopped |
| SEV-3 | Workaround available | Single dashboard broken, report export issue, delayed simulator data |

## Incident Triage

1. Record UTC time, user-facing symptom, and affected URLs.
2. Check Nginx first:

   ```bash
   curl -v http://localhost:8080/health
   docker compose logs --tail=100 nginx
   ```

3. Check service status:

   ```bash
   docker compose ps
   ```

4. Check the service that owns the failing route:

   - Portal/static routes: `nginx`, `portal/public`
   - Analytics routes: `analytics`, `postgres`, `redis`
   - Grafana: `grafana`, `postgres`
   - Node-RED ingestion: `nodered`, `mqtt`, `postgres`
   - Authentication: `auth-service`, `postgres`, SMTP settings if email is used
   - Chatbot: `chatbot`, `rasa`, `rasa-actions`
   - OVOS voice path: companion OVOS stack plus analytics `/api/v1/ovos/voice/*`

5. Avoid deployments, migrations, or secret changes until the incident is
   stable or clearly understood.

Screenshot placeholder:

![Grafana alert placeholder](./images/operations/grafana-alerts.png)

## Backup and Recovery

### PostgreSQL backup

There is no tracked generic `scripts/backup.sh` in this repository. Use
`pg_dump` or your platform backup tooling.

Manual logical backup example:

```bash
set -a
source .env
set +a
mkdir -p backups
docker exec enms-postgres pg_dump \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  -Fc \
  -f /tmp/humanerdia.dump
docker cp enms-postgres:/tmp/humanerdia.dump backups/humanerdia-$(date -u +%Y%m%dT%H%M%SZ).dump
```

Restore into a controlled environment first:

```bash
set -a
source .env
set +a
docker cp backups/humanerdia.dump enms-postgres:/tmp/humanerdia.dump
docker exec enms-postgres pg_restore \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  --clean \
  --if-exists \
  /tmp/humanerdia.dump
```

### Grafana dashboard backup

Tracked helper:

```bash
./scripts/backup-grafana-dashboards.sh
```

Optional timer installation:

```bash
sudo ./scripts/setup-grafana-auto-backup.sh
```

### Runtime volumes

Important named volumes:

- `${VOLUME_PREFIX:-enms}-postgres-data`
- `${VOLUME_PREFIX:-enms}-grafana-data`
- `${VOLUME_PREFIX:-enms}-redis-data`
- `${VOLUME_PREFIX:-enms}-mqtt-data`
- `${VOLUME_PREFIX:-enms}-mqtt-logs`

Back up volumes before host moves, Docker upgrades, and destructive maintenance.

## Common Failure Modes

| Symptom | Likely area | First checks |
|---|---|---|
| Portal does not load | Nginx or static files | `curl /health`, `docker compose logs nginx` |
| Analytics API returns 500 | Analytics, database, Redis | `docker compose logs analytics postgres redis` |
| Grafana login fails | Grafana credentials or volume | `.env`, `docker compose logs grafana` |
| No new telemetry | Simulator, MQTT, Node-RED | `docker compose logs simulator mqtt nodered` |
| Auth errors | Auth service or database | `curl :5500/api/auth/health`, logs |
| Voice widget unavailable | OVOS bridge path | analytics voice health route, OVOS container health |
| Query service has no API | Expected current state | Do not use it as a readiness blocker |

## Maintenance Checklist

Weekly:

- Verify backup creation and test restore process.
- Review disk usage:

  ```bash
  docker system df
  df -h
  ```

- Review service restart counts and recent errors:

  ```bash
  docker compose ps
  docker compose logs --since=24h
  ```

Monthly:

- Rotate credentials according to the deployment security policy.
- Review exposed host ports and firewall rules.
- Rebuild images after dependency and base-image review.
- Export or commit Grafana dashboard changes when intended.

## Post-Incident Review Template

```text
Incident:
UTC start:
UTC end:
Severity:
User impact:
Root cause:
Detection method:
What worked:
What failed:
Corrective actions:
Preventive actions:
Owner:
Due date:
```

## Screenshot Placeholders

- `docs/images/operations/containers-healthy.png`
- `docs/images/operations/grafana-alerts.png`
- `docs/images/operations/recovery-checklist.png`
