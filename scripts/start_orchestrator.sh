#!/bin/bash
# Startup script to run the orchestrator agent locally

echo "Starting Ad Campaign Orchestrator Agent..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if MCP services are running
echo "Checking MCP services status..."
services_ok=true
for port in 8001 8002 8003 8004 8005 8006 8007; do
    if ! curl -s http://localhost:$port/health > /dev/null 2>&1; then
        echo "⚠️  Warning: Service on port $port is not responding"
        services_ok=false
    fi
done

if [ "$services_ok" = false ]; then
    echo ""
    echo "⚠️  Some MCP services are not running!"
    echo "Please start all MCP services first: make start-services (or ./scripts/start_services.sh)"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create logs directory
mkdir -p logs

# Set environment variables for local services
export PRODUCT_SERVICE_URL="http://localhost:8001"
export CREATIVE_SERVICE_URL="http://localhost:8002"
export STRATEGY_SERVICE_URL="http://localhost:8003"
export META_SERVICE_URL="http://localhost:8004"
export LOGS_SERVICE_URL="http://localhost:8005"
export VALIDATOR_SERVICE_URL="http://localhost:8006"
export OPTIMIZER_SERVICE_URL="http://localhost:8007"

# Load GEMINI_API_KEY from .env if exists
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Start orchestrator agent
echo ""
echo "Starting Orchestrator Agent on port 8000..."
echo "Using orchestrator service: simple_service.py"
echo ""

# Check if port 8000 is already in use
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "⚠️  Port 8000 is already in use!"
    echo "Please stop the existing orchestrator first: ./stop_orchestrator.sh"
    exit 1
fi

# Run orchestrator agent in background
cd "$(dirname "$0")"
python -m app.orchestrator.simple_service > logs/orchestrator.log 2>&1 &
ORCHESTRATOR_PID=$!

# Save PID
echo $ORCHESTRATOR_PID > logs/orchestrator.pid

# Wait a moment for service to start
sleep 3

# Check if orchestrator started successfully
if ps -p $ORCHESTRATOR_PID > /dev/null 2>&1; then
    echo "✅ Orchestrator Agent started successfully!"
    echo ""
    echo "Orchestrator Agent Information:"
    echo "  PID: $ORCHESTRATOR_PID"
    echo "  Port: 8000"
    echo "  URL: http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
    echo "  Health Check: http://localhost:8000/health"
    echo ""
    echo "Service URLs:"
    echo "  Product Service:    $PRODUCT_SERVICE_URL"
    echo "  Creative Service:   $CREATIVE_SERVICE_URL"
    echo "  Strategy Service:   $STRATEGY_SERVICE_URL"
    echo "  Meta Service:       $META_SERVICE_URL"
    echo "  Logs Service:       $LOGS_SERVICE_URL"
    echo "  Validator Service:  $VALIDATOR_SERVICE_URL"
    echo "  Optimizer Service:  $OPTIMIZER_SERVICE_URL"
    echo ""
    echo "To stop the orchestrator, run: ./stop_orchestrator.sh"
    echo "Or manually: kill $ORCHESTRATOR_PID"
    echo "Logs are available in: logs/orchestrator.log"
else
    echo "❌ Failed to start Orchestrator Agent"
    echo "Check logs/orchestrator.log for details"
    exit 1
fi

