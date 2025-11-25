# Quick Start Guide

Get the ad campaign agent system up and running in 5 minutes!

## Prerequisites

- Python 3.11+
- pip
- Git (optional)

## Step 1: Install Dependencies

```bash
# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Gemini API key (optional for mock data)
# nano .env
```

## Step 3: Start All Services

### Option A: Using the startup script (Recommended)

```bash
./start_services.sh
```

This will start all 7 microservices in the background.

### Option B: Using Docker Compose

```bash
docker-compose up --build
```

### Option C: Manual (for debugging)

Open 7 terminal windows and run:

```bash
# Terminal 1
python -m app.services.product_service.main

# Terminal 2
python -m app.services.creative_service.main

# Terminal 3
python -m app.services.strategy_service.main

# Terminal 4
python -m app.services.meta_service.main

# Terminal 5
python -m app.services.logs_service.main

# Terminal 6
python -m app.services.schema_validator_service.main

# Terminal 7
python -m app.services.optimizer_service.main
```

## Step 4: Verify Services are Running

```bash
# Check all health endpoints
curl http://localhost:8001/health  # Product Service
curl http://localhost:8002/health  # Creative Service
curl http://localhost:8003/health  # Strategy Service
curl http://localhost:8004/health  # Meta Service
curl http://localhost:8005/health  # Logs Service
curl http://localhost:8006/health  # Schema Validator Service
curl http://localhost:8007/health  # Optimizer Service
```

All should return `{"status": "healthy", "service": "..."}`

## Step 5: Run Example Campaign

```bash
python example_usage.py
```

This will:
1. Select products for the campaign
2. Generate a campaign strategy
3. Create ad creatives
4. Validate the data
5. Deploy to Meta (mock)
6. Log the events
7. Get optimization suggestions

## Step 6: Explore the APIs

Visit the interactive API documentation:

- Product Service: http://localhost:8001/docs
- Creative Service: http://localhost:8002/docs
- Strategy Service: http://localhost:8003/docs
- Meta Service: http://localhost:8004/docs
- Logs Service: http://localhost:8005/docs
- Schema Validator: http://localhost:8006/docs
- Optimizer Service: http://localhost:8007/docs

## Stopping Services

```bash
./stop_services.sh
```

Or if using Docker:

```bash
docker-compose down
```

## Next Steps

1. **Review the code**: Start with `app/services/product_service/main.py`
2. **Read the TODO comments**: Each service has TODOs for real implementations
3. **Customize mock data**: Edit `mock_data.py` files to match your use case
4. **Add real integrations**: Replace mocks with actual APIs and databases
5. **Test the orchestrator**: Review `app/orchestrator/agent_prompt.md`

## Troubleshooting

### Port already in use

```bash
# Find and kill process on port 8001 (example)
lsof -ti:8001 | xargs kill
```

### Import errors

Make sure you're in the project root directory and have activated the virtual environment:

```bash
cd ad-campaign-agent
source venv/bin/activate
```

### Services not responding

Check the logs:

```bash
# If using startup script
tail -f logs/product_service.log

# If using Docker
docker-compose logs -f product_service
```

## Common Commands

```bash
# Start services
./start_services.sh

# Stop services
./stop_services.sh

# View logs
tail -f logs/*.log

# Run example
python example_usage.py

# Run tests (when implemented)
pytest

# Format code
black app/

# Type check
mypy app/
```

## Need Help?

- Check the main README.md for detailed documentation
- Review TODO comments in the code
- Check service logs for error messages
- Ensure all dependencies are installed
- Verify environment variables in .env

Happy building! 🚀
