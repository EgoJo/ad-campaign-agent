FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (including curl for health checks)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Set Python path
ENV PYTHONPATH=/app

# Default command (will be overridden by docker-compose)
CMD ["python", "-m", "uvicorn", "app.services.product_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
