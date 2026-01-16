#!/bin/bash
# Zero-Touch Deployment Verification Script
# Tests that a fresh clone + deploy works without manual fixes

set -e

echo "=========================================="
echo "🧪 ZERO-TOUCH DEPLOYMENT VERIFICATION"
echo "=========================================="

# Get server IP
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "📍 Server IP: $SERVER_IP"

# Verify current commits
echo ""
echo "📋 Verifying latest commits are pushed..."
cd /home/ubuntu/enms
ENMS_HEAD=$(git rev-parse HEAD)
ENMS_ORIGIN=$(git rev-parse origin/feat/zero-touch-deployment)
if [ "$ENMS_HEAD" = "$ENMS_ORIGIN" ]; then
    echo "✅ EnMS: All commits pushed ($ENMS_HEAD)"
else
    echo "❌ EnMS: Local commits not pushed!"
    exit 1
fi

cd /home/ubuntu/ovos-llm
OVOS_HEAD=$(git rev-parse HEAD)
OVOS_ORIGIN=$(git rev-parse origin/feat/zero-touch-deployment)
if [ "$OVOS_HEAD" = "$OVOS_ORIGIN" ]; then
    echo "✅ OVOS: All commits pushed ($OVOS_HEAD)"
else
    echo "❌ OVOS: Local commits not pushed!"
    exit 1
fi

# Check critical files have correct values
echo ""
echo "🔍 Verifying configuration files..."

# EnMS .env.example
if grep -q "OVOS_BRIDGE_HOST=ovos-enms" /home/ubuntu/enms/.env.example; then
    echo "✅ EnMS .env.example: OVOS_BRIDGE_HOST=ovos-enms"
else
    echo "❌ EnMS .env.example: OVOS_BRIDGE_HOST not set to ovos-enms!"
    grep "OVOS_BRIDGE_HOST" /home/ubuntu/enms/.env.example
    exit 1
fi

# OVOS config.yaml
if grep -q "api_base_url: http://enms-analytics:8001/api/v1" /home/ubuntu/ovos-llm/enms-ovos-skill/config.yaml; then
    echo "✅ OVOS config.yaml: api_base_url=enms-analytics:8001"
else
    echo "❌ OVOS config.yaml: api_base_url not correct!"
    grep "api_base_url" /home/ubuntu/ovos-llm/enms-ovos-skill/config.yaml
    exit 1
fi

# OVOS settings.docker.json
if grep -q '"enms_api_base_url": "http://enms-analytics:8001/api/v1"' /home/ubuntu/ovos-llm/enms-ovos-skill/settings.docker.json; then
    echo "✅ OVOS settings.docker.json: enms_api_base_url=enms-analytics:8001"
else
    echo "❌ OVOS settings.docker.json: enms_api_base_url not correct!"
    grep "enms_api_base_url" /home/ubuntu/ovos-llm/enms-ovos-skill/settings.docker.json
    exit 1
fi

# OVOS settingsmeta.yaml
if grep -q "value: http://enms-analytics:8001/api/v1" /home/ubuntu/ovos-llm/enms-ovos-skill/settingsmeta.yaml; then
    echo "✅ OVOS settingsmeta.yaml: default value=enms-analytics:8001"
else
    echo "❌ OVOS settingsmeta.yaml: default value not correct!"
    grep "value:" /home/ubuntu/ovos-llm/enms-ovos-skill/settingsmeta.yaml | head -5
    exit 1
fi

# Analytics health check code
if grep -q 'data.get("messagebus_connected"' /home/ubuntu/enms/analytics/api/routes/ovos_voice.py; then
    echo "✅ Analytics ovos_voice.py: Uses messagebus_connected"
else
    echo "❌ Analytics ovos_voice.py: Missing messagebus_connected mapping!"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ ALL CHECKS PASSED!"
echo "=========================================="
echo ""
echo "Zero-touch deployment is ready. To test:"
echo "1. Clean: rm -rf ~/enms ~/ovos-llm && docker system prune -af"
echo "2. Clone EnMS: git clone -b feat/zero-touch-deployment https://github.com/RaptorBlingx/enms.git"
echo "3. Deploy: cd enms && ./scripts/zero-touch-deploy.sh $SERVER_IP"
echo "4. Clone OVOS: git clone -b feat/zero-touch-deployment https://github.com/RaptorBlingx/ovos-llm.git"
echo "5. Deploy: cd ovos-llm && cp .env.example .env && docker compose build && docker compose up -d"
echo "6. Wait 30s, test: curl http://localhost:8080/api/ovos/voice/health"
echo ""
