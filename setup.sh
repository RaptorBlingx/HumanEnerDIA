#!/bin/bash
# ============================================================================
# EnMS - Zero-Touch Setup Script
# ============================================================================
set -e

echo "============================================================================"
echo "  EnMS - Energy Management System Setup"
echo "============================================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Review .env and update passwords if needed"
    echo "   Default passwords are set for development use"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Build and start services
echo "🐳 Building Docker images (this may take a few minutes)..."
docker compose build

echo ""
echo "🚀 Starting services..."
docker compose up -d

echo ""
echo "⏳ Waiting for services to be healthy (30 seconds)..."
sleep 30

echo ""
echo "============================================================================"
echo "  ✅ EnMS Setup Complete!"
echo "============================================================================"
echo ""
echo "Access the system at:"
echo ""
echo "  🌐 Portal:        http://localhost:8080 or http://$(hostname -I | awk '{print $1}'):8080"
echo "  📊 Grafana:       http://localhost:8080/grafana"
echo "  🔴 Node-RED:      http://localhost:1880"
echo "  📈 Analytics UI:  http://localhost:8080/analytics/ui/"
echo "  📄 API Docs:      http://localhost:8080/api/analytics/docs"
echo ""
echo "Default credentials (from .env):"
echo "  • Grafana: Check GRAFANA_ADMIN_USER/GRAFANA_ADMIN_PASSWORD in .env"
echo ""
echo "Useful commands:"
echo "  • View logs:         docker compose logs -f"
echo "  • Stop services:     docker compose down"
echo "  • Restart services:  docker compose restart"
echo "  • Check status:      docker compose ps"
echo ""
echo "For more information, see README.md"
echo "============================================================================"
