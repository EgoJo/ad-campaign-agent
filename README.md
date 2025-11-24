# Ad Campaign AI Agent System

A production-ready scaffold for an AI-powered ad campaign orchestration system built with Google ADK/Gemini and MCP-style microservices.

## Architecture Overview

This system uses a **microservices architecture** with an orchestrator agent that coordinates multiple specialized services:

- **Orchestrator Agent**: Built with Google ADK / Gemini, coordinates all services
- **MCP Microservices**: Independent FastAPI services handling specific domains

### Services

| Service | Port | Description |
|---------|------|-------------|
| **product_service** | 8001 | Selects optimal products for campaigns |
| **creative_service** | 8002 | Generates ad creatives (text, images) |
| **strategy_service** | 8003 | Creates campaign strategies and budget allocation |
| **meta_service** | 8004 | Deploys campaigns to Meta platforms |
| **logs_service** | 8005 | Logs events for auditing and monitoring |
| **schema_validator_service** | 8006 | Validates data structures |
| **optimizer_service** | 8007 | Analyzes performance and suggests optimizations |

## Project Structure

```
ad-campaign-agent/
├── app/
│   ├── orchestrator/           # Orchestrator agent configuration
│   │   ├── agent_prompt.md     # Agent system prompt
│   │   ├── agent_config.yaml   # ADK tool definitions
│   │   └── clients/            # HTTP clients for each MCP service
│   ├── services/               # MCP microservices
│   │   ├── product_service/
│   │   ├── creative_service/
│   │   ├── strategy_service/
│   │   ├── meta_service/
│   │   ├── logs_service/
│   │   ├── schema_validator_service/
│   │   └── optimizer_service/
│   └── common/                 # Shared utilities
│       ├── config.py           # Configuration management
│       └── http_client.py      # HTTP client base class
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container definition
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Tech Stack

- **Python 3.11+**
- **FastAPI** - Modern web framework for building APIs
- **Uvicorn/Gunicorn** - ASGI server
- **Pydantic** - Data validation using Python type annotations
- **google-generativeai** - Google Gemini API client
- **httpx** - Async HTTP client
- **Docker** - Containerization (optional)

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip
- (Optional) Docker and Docker Compose

### Installation

1. **Clone the repository** (or use this scaffold):
   ```bash
   cd ad-campaign-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

### Running Services

#### Option 1: Run Locally (Development)

Start each service in a separate terminal:

```bash
# Terminal 1 - Product Service
python -m app.services.product_service.main

# Terminal 2 - Creative Service
python -m app.services.creative_service.main

# Terminal 3 - Strategy Service
python -m app.services.strategy_service.main

# Terminal 4 - Meta Service
python -m app.services.meta_service.main

# Terminal 5 - Logs Service
python -m app.services.logs_service.main

# Terminal 6 - Schema Validator Service
python -m app.services.schema_validator_service.main

# Terminal 7 - Optimizer Service
python -m app.services.optimizer_service.main
```

#### Option 2: Run with Docker Compose

```bash
docker-compose up --build
```

This will start all services in containers.

### Testing Services

Each service exposes a health check endpoint:

```bash
# Test product service
curl http://localhost:8001/health

# Test creative service
curl http://localhost:8002/health

# ... and so on for other services
```

### Using the Orchestrator Clients

Example usage of the client libraries:

```python
from app.orchestrator.clients import ProductClient, CreativeClient

# Select products
product_client = ProductClient()
products = product_client.select_products(
    campaign_objective="increase sales",
    target_audience="tech enthusiasts",
    budget=10000.0
)
print(products)

# Generate creatives
creative_client = CreativeClient()
creatives = creative_client.generate_creatives(
    product_ids=["PROD-001", "PROD-002"],
    campaign_objective="increase sales",
    target_audience="tech enthusiasts"
)
print(creatives)
```

## Current Implementation Status

### ✅ Implemented

- Complete project structure
- All 7 MCP microservices with FastAPI
- Pydantic schemas for type safety
- Mock data generators for all services
- HTTP client utilities
- Configuration management
- Orchestrator agent prompt and configuration
- Client libraries for all services
- Docker support
- Health check endpoints

### 🚧 TODO (Next Steps)

Each service contains `TODO` comments indicating where to add real implementations:

1. **Product Service**:
   - Connect to product database
   - Implement ML-based product selection
   - Add inventory management

2. **Creative Service**:
   - Integrate Gemini API for copywriting
   - Add image generation (DALL-E, Stable Diffusion)
   - Implement A/B testing variants

3. **Strategy Service**:
   - Add ML-based budget optimization
   - Use historical performance data
   - Implement platform-specific strategies

4. **Meta Service**:
   - Integrate Facebook Marketing API
   - Handle authentication and permissions
   - Add campaign status monitoring

5. **Logs Service**:
   - Connect to database (PostgreSQL, MongoDB)
   - Integrate with logging platforms (ELK, Datadog)
   - Add search and filtering

6. **Schema Validator Service**:
   - Define schemas for all data types
   - Implement custom validation rules
   - Add detailed error reporting

7. **Optimizer Service**:
   - Query analytics database
   - Implement ML-based optimization models
   - Add performance benchmarking

8. **Orchestrator Agent**:
   - Integrate with Google ADK
   - Implement agent runtime
   - Add error handling and retries

## API Documentation

Each service provides interactive API documentation:

- Product Service: http://localhost:8001/docs
- Creative Service: http://localhost:8002/docs
- Strategy Service: http://localhost:8003/docs
- Meta Service: http://localhost:8004/docs
- Logs Service: http://localhost:8005/docs
- Schema Validator Service: http://localhost:8006/docs
- Optimizer Service: http://localhost:8007/docs

## Development Guidelines

### Adding New Services

1. Create a new directory under `app/services/`
2. Add `schemas.py` for Pydantic models
3. Add `main.py` with FastAPI app
4. (Optional) Add `mock_data.py` for testing
5. Create a client in `app/orchestrator/clients/`
6. Update `agent_config.yaml` with new tool definitions

### Code Style

- Use **type hints** for all function parameters and return values
- Add **docstrings** to all classes and functions
- Follow **PEP 8** style guidelines
- Use **Pydantic models** for request/response validation

### Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app tests/
```

## Deployment

### Environment Variables

Key environment variables to configure:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `PRODUCT_SERVICE_URL`: URL of the product service
- `CREATIVE_SERVICE_URL`: URL of the creative service
- (etc. for other services)

### Production Considerations

- Use **Gunicorn** with multiple workers for production
- Set up **reverse proxy** (nginx) for load balancing
- Implement **authentication and authorization**
- Add **rate limiting** and **request throttling**
- Set up **monitoring and alerting** (Prometheus, Grafana)
- Use **secrets management** (AWS Secrets Manager, HashiCorp Vault)
- Implement **circuit breakers** for service resilience

## License

This is a scaffold/template project. Add your own license as needed.

## Contributing

This is a starting scaffold. Customize it for your specific needs:

1. Replace mock data with real implementations
2. Add authentication and security
3. Implement error handling and retries
4. Add comprehensive testing
5. Set up CI/CD pipelines
6. Add monitoring and observability

## Support

For issues or questions about this scaffold, please refer to the TODO comments in the code for guidance on implementing real functionality.
