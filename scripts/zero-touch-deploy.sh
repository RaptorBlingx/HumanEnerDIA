#!/bin/bash
set -e

echo "=============================================="
echo "  EnMS Zero-Touch Deployment"
echo "=============================================="
echo ""

# Configuration
SERVER_IP="${1:-10.33.10.103}"

echo "[1/5] Creating .env from template..."
cp .env.example .env
sed -i "s/SERVER_IP=localhost/SERVER_IP=$SERVER_IP/" .env

echo "[2/5] Building Docker images (this may take 5-10 minutes)..."
docker compose build

echo "[3/5] Starting all services..."
docker compose up -d

echo "[4/5] Waiting for services to become healthy..."
sleep 30

echo "[5/5] Ensuring all services are running..."
docker compose up -d  # Second run ensures dependent services start

echo ""
echo "=============================================="
echo "  ✓ Deployment Complete!"
echo "=============================================="
echo ""
echo "Services:"
echo "  Portal:    http://$SERVER_IP:8080"
echo "  Analytics: http://$SERVER_IP:8001/docs"
echo "  Grafana:   http://$SERVER_IP:8080/grafana"
echo "  Node-RED:  http://$SERVER_IP:8080/nodered"
echo ""
echo "Check status: docker compose ps"
echo "View logs:    docker compose logs -f"
