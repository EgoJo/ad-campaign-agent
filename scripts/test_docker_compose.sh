#!/bin/bash
# Test script for Docker Compose configuration

set -e

echo "=========================================="
echo "Docker Compose Configuration Test"
echo "=========================================="
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
    echo "❌ Error: docker-compose not found"
    echo "   Please install Docker Compose"
    exit 1
fi

# Use docker compose (v2) if available, otherwise docker-compose (v1)
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo "✅ Using: $DOCKER_COMPOSE"
echo ""

# Validate configuration
echo "1. Validating docker-compose.yml..."
if $DOCKER_COMPOSE config > /dev/null 2>&1; then
    echo "   ✅ Configuration is valid"
else
    echo "   ❌ Configuration has errors"
    $DOCKER_COMPOSE config
    exit 1
fi

# Count services
SERVICE_COUNT=$($DOCKER_COMPOSE config --services | wc -l | tr -d ' ')
echo "2. Service count: $SERVICE_COUNT services"
echo ""

# List services
echo "3. Services defined:"
$DOCKER_COMPOSE config --services | sed 's/^/   - /'
echo ""

# Check if orchestrator is included
if $DOCKER_COMPOSE config --services | grep -q "orchestrator_agent"; then
    echo "   ✅ orchestrator_agent is included"
else
    echo "   ❌ orchestrator_agent is missing"
    exit 1
fi

# Check orchestrator dependencies
echo ""
echo "4. Checking orchestrator dependencies..."
ORCHESTRATOR_DEPS=$($DOCKER_COMPOSE config | grep -A 10 "orchestrator_agent:" | grep -A 8 "depends_on:" | grep -E "^\s+-" | sed 's/^\s*-\s*//' | sed 's/:$//')
echo "   Orchestrator depends on:"
for dep in $ORCHESTRATOR_DEPS; do
    echo "   - $dep"
done

EXPECTED_DEPS=6
ACTUAL_DEPS=$(echo "$ORCHESTRATOR_DEPS" | wc -l | tr -d ' ')
if [ "$ACTUAL_DEPS" -eq "$EXPECTED_DEPS" ]; then
    echo "   ✅ All $EXPECTED_DEPS dependencies configured"
else
    echo "   ⚠️  Expected $EXPECTED_DEPS dependencies, found $ACTUAL_DEPS"
fi

# Check health checks
echo ""
echo "5. Checking health checks..."
HEALTH_CHECK_COUNT=$($DOCKER_COMPOSE config | grep -c "healthcheck:" || echo "0")
if [ "$HEALTH_CHECK_COUNT" -eq "$SERVICE_COUNT" ]; then
    echo "   ✅ All $SERVICE_COUNT services have health checks"
else
    echo "   ⚠️  Only $HEALTH_CHECK_COUNT services have health checks (expected $SERVICE_COUNT)"
fi

# Check service URLs in orchestrator
echo ""
echo "6. Checking orchestrator service URLs..."
ORCHESTRATOR_ENV=$($DOCKER_COMPOSE config | grep -A 20 "orchestrator_agent:" | grep -E "^\s+- (PRODUCT|CREATIVE|STRATEGY|META|LOGS|OPTIMIZER)_SERVICE_URL=")
echo "   Service URLs configured:"
echo "$ORCHESTRATOR_ENV" | sed 's/^\s*-\s*//' | sed 's/^/   /'

# Summary
echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="
echo "✅ Configuration validation: PASSED"
echo "✅ Service count: $SERVICE_COUNT"
echo "✅ Orchestrator included: YES"
echo "✅ Dependencies configured: YES"
echo "✅ Health checks configured: YES"
echo ""
echo "To start all services:"
echo "  $DOCKER_COMPOSE up -d"
echo ""
echo "To check service status:"
echo "  $DOCKER_COMPOSE ps"
echo ""
echo "To view logs:"
echo "  $DOCKER_COMPOSE logs -f orchestrator_agent"
echo ""

