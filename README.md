# HumanEnerDIA - Energy Management System

<div align="center">

**Production-ready, open-source Energy Management System for industrial facilities**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](docker-compose.yml)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![ISO 50001](https://img.shields.io/badge/ISO-50001-orange.svg)](https://www.iso.org/iso-50001-energy-management.html)

Part of the [WASABI Project](https://wasabiproject.eu/)

</div>

---

## Overview

HumanEnerDIA is a comprehensive energy monitoring and analytics platform for
industrial facilities. It provides ISO 50001-aligned energy performance
monitoring, machine-learning-assisted analytics, Grafana dashboards, a web
portal, and an OVOS-ready Digital Industrial Assistant integration.

### Key Features

- **🏭 Real-time Monitoring**: Track energy consumption across all Significant Energy Users (SEUs)
- **📊 Advanced Analytics**: ML-powered baselines, forecasting, and anomaly detection
- **📈 Smart Dashboards**: Pre-built Grafana dashboards with customizable variables
- **🎤 Voice Integration**: OVOS-ready via the companion HumanEnerDIA OVOS skill and REST bridge
- **🔌 Modular Architecture**: Microservices-based, API-first design
- **🐳 Guided Docker Deployment**: Docker Compose deployment with explicit secret placeholders
- **🔒 Release-Oriented Defaults**: Sanitized examples, health checks, and documented production hardening steps

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NGINX (API Gateway)                       │
└────┬────────────────────────────────────────────────────┬───┘
     │                                                     │
     ▼                                                     ▼
┌─────────────────────┐                        ┌──────────────────┐
│   Unified Portal    │                        │  External APIs   │
│   Grafana           │                        │  (OVOS, etc.)    │
│   Node-RED          │                        └──────────────────┘
│   Analytics UI      │
└─────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     Core Services                            │
├──────────────┬─────────────────┬─────────────────────────────┤
│  Simulator   │    Analytics    │    Query Service            │
│  Node-RED    │    Service      │    (placeholder)            │
└──────┬───────┴────────┬────────┴────────┬────────────────────┘
       │                │                 │
       └────────────────┴─────────────────┘
                        │
              ┌─────────┴─────────┐
              │   PostgreSQL +    │
              │   TimescaleDB     │
              └───────────────────┘
       ┌──────────────┬──────────────┐
       │     MQTT     │    Redis     │
       └──────────────┴──────────────┘
```

---

## Quick Start

### Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Linux/macOS** (Windows with WSL2)
- **4GB RAM** minimum (8GB recommended)
- **10GB disk space**

### Installation

**Option 1: Guided Setup (Recommended)**

```bash
# Clone the repository
git clone https://github.com/RaptorBlingx/HumanEnerDIA.git humanergy
cd humanergy

# Copy environment template
cp .env.example .env

# Fill in the required values before first startup
nano .env

# Run the setup helper
./setup.sh
```

**Option 2: Manual Setup**

```bash
# Clone and configure
git clone https://github.com/RaptorBlingx/HumanEnerDIA.git humanergy
cd humanergy
cp .env.example .env

# Build and start
docker compose build
docker compose up -d
```

The setup helper is a thin wrapper around `docker compose build` and
`docker compose up -d`. It refuses to run while placeholder values remain in
`.env` so the bundle does not start with fake secrets by accident.

### Access the System

After installation completes:

- **Unified Portal**: http://localhost:8080
- **Grafana**: http://localhost:8080/grafana (credentials in .env)
- **Node-RED**: http://localhost:1881
- **Analytics UI**: http://localhost:8080/analytics/ui/
- **API Documentation**: http://localhost:8080/api/analytics/docs
- **Simulator Control**: http://localhost:8003/docs

> **Note**: Replace `localhost` with your server IP for remote access

### ✨ **Automatic Dashboard Backup**

**Your Grafana changes are automatically saved every 10 minutes!**

Grafana dashboards are automatically exported to git-tracked JSON files. Just edit dashboards in the UI and commit when ready:

```bash
# 1. Edit dashboards in Grafana UI (changes auto-exported every 10 min)
# 2. Wait for next backup cycle or run manually:
./scripts/backup-grafana-dashboards.sh

# 3. Commit your changes
git add grafana/dashboards/*.json
git commit -m "Update Grafana dashboards"
git push
```

**Setup auto-backup on new systems:**
```bash
sudo ./scripts/setup-grafana-auto-backup.sh
```

For detailed information, see: [docs/GRAFANA-PERSISTENCE.md](docs/GRAFANA-PERSISTENCE.md)

> **Note**: Node-RED changes are also automatically saved to the filesystem.

---

## 📊 Data Model

### Core Entities

- **Factories**: Industrial facilities
- **Machines (SEUs)**: Significant Energy Users
- **Energy Readings**: Time-series power and energy data
- **Production Data**: Output metrics for normalization
- **Environmental Data**: Temperature, humidity, pressure

### Machine Types Supported

1. **Compressor** (1-second intervals)
2. **HVAC System** (10-second intervals)
3. **Conveyor Motor** (10-second intervals)
4. **Hydraulic Pump** (30-second intervals)
5. **Injection Molding** (30-second intervals)

---

## 🧠 Analytics & KPIs

### Key Performance Indicators

- **SEC**: Specific Energy Consumption (kWh/unit)
- **Peak Demand**: Maximum power draw (kW)
- **Load Factor**: Average/Peak ratio
- **Energy Cost**: With time-of-use tariffs
- **Carbon Intensity**: CO₂ emissions tracking

### Machine Learning Models

- **Energy Baseline (EnB)**: Multiple regression for normalization
- **Anomaly Detection**: Isolation Forest for fault detection
- **Forecasting**: ARIMA + Prophet for demand prediction

---

## 🔌 API Endpoints

### Analytics Service (Port 8001)

```
POST   /api/v1/baseline/train        # Train energy baseline model
GET    /api/v1/baseline/deviation    # Get deviation from baseline
GET    /api/v1/forecast/demand       # Get energy forecast
GET    /api/v1/anomaly/detect        # Detect anomalies
POST   /api/v1/kpi/calculate         # Calculate KPIs
```

### Query Service (Port 8002)

```
Reserved for future query APIs. The current container is intentionally a
placeholder and is not part of release health expectations.
```

### Simulator Service (Port 8003)

```
POST   /simulator/start              # Start data generation
POST   /simulator/stop               # Stop data generation
GET    /simulator/status             # Get simulator status
PUT    /simulator/config             # Update configuration
POST   /simulator/inject-anomaly     # Inject anomaly for testing
```

Full API documentation: http://localhost/api/docs

---

## 🎤 OVOS Integration

HumanEnerDIA is designed to work with Open Voice OS through the companion OVOS
skill and REST bridge. Example voice commands:

- *"What's the energy consumption of compressor 1 in the last hour?"*
- *"Show me machines using more than 50 kilowatts"*
- *"How is temperature affecting HVAC efficiency today?"*

The current OVOS stack uses a hybrid routing path: heuristic and Adapt matching
handle the normal fast path, and harder queries can optionally escalate to a
local Qwen3.5-2B GGUF fallback model. The fallback is disabled in the base
full-stack bundle unless `INSTALL_LLM_FALLBACK=true` is set and the model file
is supplied separately.

### Integration Endpoint

```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{
    "text": "what is the power of compressor one",
    "session_id": "readme-smoke"
  }'
```

See [ENMS API Documentation for OVOS](docs/api-documentation/ENMS-API-DOCUMENTATION-FOR-OVOS.md)
and the WASABI release docs under [docs/wasabi-shop](docs/wasabi-shop/) for
the distributable skill and full-stack packaging flow.

---

## 📁 Project Structure

```
enms/
├── docker-compose.yml           # Service orchestration
├── .env.example                 # Environment template
├── setup.sh                     # Guided setup helper
├── docs/                        # Documentation
├── nginx/                       # API Gateway config
├── portal/                      # Unified web interface
├── grafana/                     # Dashboards & provisioning
├── nodered/                     # Data pipeline flows
├── database/                    # PostgreSQL schema & init
├── simulator/                   # Factory data generator
├── analytics/                   # ML service (Python/FastAPI)
├── query-service/               # Placeholder for future query APIs
├── mqtt/                        # Mosquitto configuration
├── redis/                       # Redis configuration
└── scripts/                     # Utility scripts
```

---

## 🛠️ Development

### Running in Development Mode

```bash
# Use development compose file
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Enable hot-reload for services
# See docker-compose.dev.yml for configuration
```

### Running Tests

```bash
docker compose config
docker compose exec analytics pytest
```

The query-service container is currently a placeholder, so it does not have a
release test suite.

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f analytics
```

---

## 📈 Performance

- **Throughput**: Handles 5+ machines with 1-second intervals (5+ data points/second)
- **Storage**: TimescaleDB compression reduces storage by 90%
- **Queries**: Sub-100ms response times for dashboard queries
- **Scalability**: Horizontal scaling ready with load balancer

---

## 🔒 Security

- **Authentication**: JWT tokens for API access
- **Rate Limiting**: 100 requests/minute per IP
- **Input Validation**: Pydantic models with strict typing
- **SQL Injection**: Parameterized queries only
- **HTTPS**: SSL/TLS support (configure in nginx/ssl/)

---

## 🗄️ Backup & Recovery

### Manual Backup

```bash
./scripts/backup.sh
```

### Restore from Backup

```bash
./scripts/restore.sh backups/enms_backup_2025-10-08.sql.gz
```

### Automated Backups

Configured in `.env`:
```
BACKUP_SCHEDULE=0 3 * * *  # Daily at 3 AM
BACKUP_RETENTION_DAYS=30
```

---

## 📚 Documentation

- [GRAFANA-PERSISTENCE.md](docs/GRAFANA-PERSISTENCE.md) - Dashboard backup & persistence
- [Project Knowledge Base](Project-Knowledge-Base.md) - Architecture & development guide
- [API Documentation](docs/api-documentation/) - REST API reference
- [ISO 50001 Guide](docs/ISO-50001-IMPLEMENTATION-GUIDE.md) - Energy management standards
- [WASABI Release Runbook](docs/wasabi-shop/HUMANERDIA_WASABI_RELEASE_RUNBOOK.md) - release and shop publishing checklist
- [Full Stack Installation](docs/wasabi-shop/HUMANERDIA_FULL_STACK_INSTALLATION.md) - buyer-facing deployment guide
- [ENMS API Documentation for OVOS](docs/api-documentation/ENMS-API-DOCUMENTATION-FOR-OVOS.md) - OVOS/backend API contract

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Part of the [WASABI Project](https://wasabiproject.eu/)
- Built with [TimescaleDB](https://www.timescale.com/)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Visualized with [Grafana](https://grafana.com/)
- Orchestrated with [Node-RED](https://nodered.org/)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/RaptorBlingx/HumanEnerDIA/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RaptorBlingx/HumanEnerDIA/discussions)

---

## 🗺️ Roadmap

- [x] Core monitoring and dashboards
- [x] ML-powered analytics
- [x] API-first architecture
- [x] OVOS voice integration through companion skill and REST bridge
- [ ] Mobile app
- [ ] Multi-tenancy support
- [ ] Cloud deployment templates (AWS, Azure, GCP)
- [ ] Advanced predictive maintenance

---

<div align="center">

**Built with ❤️ for the industrial IoT community**

⭐ Star us on GitHub — it motivates us a lot!

</div>
