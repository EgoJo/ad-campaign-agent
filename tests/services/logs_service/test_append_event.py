"""
Tests for append_event endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.services.logs_service.main import app

client = TestClient(app)


@pytest.fixture
def sample_log_event():
    """Sample log event for testing."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "stage": "product",
        "service": "product_service",
        "request": {"campaign_spec": {"category": "electronics"}},
        "response": {"status": "success", "products": []},
        "success": True,
        "metadata": {"message": "Products selected successfully"}
    }


class TestAppendEvent:
    """Test append_event endpoint."""
    
    def test_append_event_success(self, sample_log_event):
        """Test successful event logging."""
        response = client.post("/append_event", json=sample_log_event)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        # Event ID may be None if database not available
        assert "event_id" in data
    
    def test_append_event_error_level(self):
        """Test logging error-level event."""
        error_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "stage": "creative",
            "service": "creative_service",
            "request": {"product_id": "PROD-001"},
            "response": {"status": "error", "error_code": "LLM_FAILED"},
            "success": False,
            "metadata": {"message": "LLM call failed"}
        }
        
        response = client.post("/append_event", json=error_event)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
    
    def test_append_event_minimal(self):
        """Test logging with minimal required fields."""
        minimal_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "stage": "orchestrator",
            "service": "orchestrator_agent",
            "success": True
        }
        
        response = client.post("/append_event", json=minimal_event)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
    
    def test_append_event_with_correlation_id(self, sample_log_event):
        """Test logging with correlation ID."""
        sample_log_event["metadata"] = {
            "correlation_id": "test-correlation-123",
            "message": "Test event"
        }
        
        response = client.post("/append_event", json=sample_log_event)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
    
    def test_append_event_invalid_timestamp(self):
        """Test logging with invalid timestamp format."""
        invalid_event = {
            "timestamp": "invalid-timestamp",
            "stage": "product",
            "service": "product_service",
            "success": True
        }
        
        # Should still succeed, but use current time
        response = client.post("/append_event", json=invalid_event)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
    
    def test_append_event_missing_required_fields(self):
        """Test logging with missing required fields."""
        incomplete_event = {
            "timestamp": datetime.utcnow().isoformat(),
            # Missing stage, service, success
        }
        
        response = client.post("/append_event", json=incomplete_event)
        # Should return validation error
        assert response.status_code == 422
    
    def test_append_event_all_stages(self):
        """Test logging events for all workflow stages."""
        stages = ["intent", "product", "creative", "strategy", "meta", "optimizer", "orchestrator"]
        
        for stage in stages:
            event = {
                "timestamp": datetime.utcnow().isoformat(),
                "stage": stage,
                "service": f"{stage}_service",
                "success": True,
                "metadata": {"message": f"Test event for {stage} stage"}
            }
            
            response = client.post("/append_event", json=event)
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "success"

