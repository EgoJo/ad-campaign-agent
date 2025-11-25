"""
Tests for query_logs endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.services.logs_service.main import app

client = TestClient(app)


@pytest.fixture
def sample_log_events():
    """Create sample log events for testing."""
    events = []
    base_time = datetime.utcnow()
    
    # Create events for different stages and services
    for i, stage in enumerate(["product", "creative", "strategy"]):
        event = {
            "timestamp": (base_time - timedelta(minutes=i)).isoformat(),
            "stage": stage,
            "service": f"{stage}_service",
            "success": i % 2 == 0,  # Alternate success/failure
            "metadata": {
                "message": f"Test event {i}",
                "correlation_id": f"test-correlation-{i}"
            }
        }
        events.append(event)
        # Append the event
        client.post("/append_event", json=event)
    
    return events


class TestQueryLogs:
    """Test query_logs endpoint."""
    
    def test_query_logs_all(self, sample_log_events):
        """Test querying all logs."""
        response = client.get("/logs")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert "logs" in data
        assert "pagination" in data
        assert isinstance(data["logs"], list)
    
    def test_query_logs_by_stage(self, sample_log_events):
        """Test filtering by stage."""
        response = client.get("/logs?stage=product")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        # All returned logs should have stage=product
        for log in data["logs"]:
            assert log["stage"] == "product"
    
    def test_query_logs_by_service(self, sample_log_events):
        """Test filtering by service."""
        response = client.get("/logs?service=creative_service")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        # All returned logs should have service=creative_service
        for log in data["logs"]:
            assert log["service"] == "creative_service"
    
    def test_query_logs_by_correlation_id(self, sample_log_events):
        """Test filtering by correlation ID."""
        correlation_id = "test-correlation-0"
        response = client.get(f"/logs?correlation_id={correlation_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        # All returned logs should have the same correlation_id
        for log in data["logs"]:
            assert log.get("correlation_id") == correlation_id
    
    def test_query_logs_by_level(self, sample_log_events):
        """Test filtering by log level."""
        response = client.get("/logs?level=ERROR")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        # All returned logs should be ERROR level
        for log in data["logs"]:
            assert log["level"] == "ERROR"
    
    def test_query_logs_with_pagination(self, sample_log_events):
        """Test pagination."""
        response = client.get("/logs?limit=2&offset=0")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert len(data["logs"]) <= 2
        assert data["pagination"]["limit"] == 2
        assert data["pagination"]["offset"] == 0
    
    def test_query_logs_time_range(self, sample_log_events):
        """Test filtering by time range."""
        now = datetime.utcnow()
        start_time = (now - timedelta(hours=1)).isoformat()
        end_time = (now + timedelta(hours=1)).isoformat()
        
        response = client.get(f"/logs?start_time={start_time}&end_time={end_time}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
    
    def test_query_logs_invalid_time_format(self):
        """Test query with invalid time format."""
        response = client.get("/logs?start_time=invalid-time")
        
        # Should return error response
        assert response.status_code == 200  # Returns 200 with ErrorResponse
        data = response.json()
        assert data["status"] == "error"
        assert data["error_code"] == "INVALID_START_TIME"
    
    def test_query_logs_combined_filters(self, sample_log_events):
        """Test query with multiple filters."""
        response = client.get("/logs?stage=product&service=product_service&level=INFO")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        # Verify all filters are applied
        for log in data["logs"]:
            assert log["stage"] == "product"
            assert log["service"] == "product_service"
            assert log["level"] == "INFO"
    
    def test_query_logs_pagination_metadata(self, sample_log_events):
        """Test pagination metadata is correct."""
        response = client.get("/logs?limit=10&offset=0")
        
        assert response.status_code == 200
        data = response.json()
        
        pagination = data["pagination"]
        assert "limit" in pagination
        assert "offset" in pagination
        assert "returned" in pagination
        assert "total" in pagination
        assert pagination["returned"] == len(data["logs"])

