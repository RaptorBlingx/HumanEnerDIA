# HumanEnerDIA

HumanEnerDIA is a Docker Compose stack for industrial energy management. It
includes the web portal, analytics service, authentication service, Grafana
dashboards, Node-RED ingestion, MQTT, Redis, PostgreSQL/TimescaleDB, a demo
factory simulator, and optional integration with a separately running OVOS
assistant.

## WASABI Products

The release is split into three downloadable products:

- `HumanEnerDIA-EnMS-v1.0.0`: the EnMS platform only.
- `HumanEnerDIA-OVOS-skill-v1.0.0`: the OVOS runtime and HumanEnerDIA skill only.
- `HumanEnerDIA-full-stack-v1.0.0`: EnMS plus embedded OVOS in one bundle.

For separate EnMS and OVOS deployments, start the EnMS package first, then
start the OVOS package with:

```bash
./setup.sh --enms-api-url http://<enms-host>:8001/api/v1
```

To let the EnMS portal call the separate OVOS bridge, configure EnMS with:

```bash
./setup.sh --ovos-bridge-host <ovos-host> --ovos-bridge-port 5000
```

## Requirements

- Docker Engine 20.10+
- Docker Compose v2
- Linux, macOS, or Windows with WSL2
- 8 GB RAM recommended
- 15 GB free disk space recommended

## Start

```bash
git clone https://github.com/RaptorBlingx/HumanEnerDIA-Prod.git
cd HumanEnerDIA-Prod
./setup.sh
```

For browser access from another machine, pass the host name or IP that users
will open:

```bash
./setup.sh --server-ip energy-demo.local
```

To configure the optional separate OVOS bridge during EnMS setup:

```bash
./setup.sh --server-ip energy-demo.local --ovos-bridge-host ovos-demo.local --ovos-bridge-port 5000
```

`setup.sh` creates `.env` when needed, generates local first-run secrets,
validates Docker Compose, builds the images, and starts the stack. Generated
credentials are stored in `.env`; keep that file private and rotate the values
before public exposure.

## Open

- Portal: `http://localhost:8080`
- Grafana: `http://localhost:8080/grafana`
- Analytics UI: `http://localhost:8080/analytics/ui/`
- Analytics API health: `http://localhost:8001/api/v1/health`
- API URL for a separate OVOS package: `http://localhost:8001/api/v1`

## Verify

```bash
./verify.sh
```

The verifier checks Docker Compose configuration, the Nginx health endpoint,
and the analytics health endpoint. If an OVOS bridge is available at
`http://localhost:5000`, it also runs the OVOS health and smoke-query checks.

## Stop

```bash
docker compose down
```

To remove runtime volumes as well:

```bash
docker compose down -v
```

## Clean Reinstall

Use this before retesting on a machine that already ran HumanEnerDIA:

```bash
docker compose down -v --remove-orphans || true
docker rm -f enms-nginx enms-postgres enms-mqtt enms-redis enms-simulator enms-nodered enms-grafana enms-analytics enms-auth-service enms-rasa-actions enms-rasa enms-chatbot enms-ovos ovos-enms enms-query-service 2>/dev/null || true
docker volume rm enms-postgres-data enms-grafana-data enms-mqtt-data enms-mqtt-logs enms-redis-data enms-nodered-data enms-ovos-logs enms-ovos-supervisor-logs postgres-data grafana-data mqtt-data mqtt-logs redis-data nodered-data ovos-logs supervisor-logs 2>/dev/null || true
docker network rm enms-network 2>/dev/null || true
docker builder prune -af
```

On a dedicated test laptop where it is acceptable to remove all unused Docker
state for every project:

```bash
docker system prune -af --volumes
docker builder prune -af
```

## Production Notes

- Rotate generated `.env` secrets before production exposure.
- Configure DNS, TLS, firewall rules, backups, and host monitoring.
- Do not commit or publish `.env`, Docker volumes, logs, caches, or local model
  outputs.

## License

HumanEnerDIA is released under the MIT License. See `LICENSE`.
