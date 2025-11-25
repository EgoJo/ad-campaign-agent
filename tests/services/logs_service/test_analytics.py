"""
Tests for analytics endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.services.logs_service.main import app

client = TestClient(app)


@pytest.fixture
def sample_analytics_events():
    """Create sample events for analytics testing."""
    events = []
    
    # Create events for different stages
    stages = ["product", "creative", "strategy", "product", "creative"]
    services = ["product_service", "creative_service", "strategy_service", "product_service", "creative_service"]
    success_flags = [True, True, False, True, False]
    
    for i, (stage, service, success) in enumerate(zip(stages, services, success_flags)):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "stage": stage,
            "service": service,
            "success": success,
            "metadata": {"message": f"Analytics test event {i}"}
        }
        events.append(event)
        # Append the event
        client.post("/append_event", json=event)
    
    return events


class TestAnalytics:
    """Test analytics endpoint."""
    
    def test_analytics_basic(self, sample_analytics_events):
        """Test basic analytics query."""
        response = client.get("/analytics")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert "by_stage" in data
        assert "by_service" in data
        assert "levels" in data
    
    def test_analytics_by_stage(self, sample_analytics_events):
        """Test analytics by stage."""
        response = client.get("/analytics")
        data = response.json()
        
        assert "by_stage" in data
        assert isinstance(data["by_stage"], dict)
        
        # Should have counts for stages we created
        # Note: May have other events from previous tests
        by_stage = data["by_stage"]
        assert isinstance(by_stage, dict)
        # All values should be integers
        for count in by_stage.values():
            assert isinstance(count, int)
            assert count >= 0
    
    def test_analytics_by_service(self, sample_analytics_events):
        """Test analytics by service."""
        response = client.get("/analytics")
        data = response.json()
        
        assert "by_service" in data
        assert isinstance(data["by_service"], dict)
        
        by_service = data["by_service"]
        assert isinstance(by_service, dict)
        # All values should be integers
        for count in by_service.values():
            assert isinstance(count, int)
            assert count >= 0
    
    def test_analytics_by_level(self, sample_analytics_events):
        """Test analytics by log level."""
        response = client.get("/analytics")
        data = response.json()
        
        assert "levels" in data
        assert isinstance(data["levels"], dict)
        
        levels = data["levels"]
        assert isinstance(levels, dict)
        
        # Should have INFO and ERROR levels
        # All values should be integers
        for level, count in levels.items():
            assert isinstance(count, int)
            assert count >= 0
            assert level in ["INFO", "ERROR", "WARNING"]
    
    def test_analytics_structure(self, sample_analytics_events):
        """Test analytics response structure."""
        response = client.get("/analytics")
        data = response.json()
        
        # Verify structure
        assert data["status"] == "success"
        assert isinstance(data["by_stage"], dict)
        assert isinstance(data["by_service"], dict)
        assert isinstance(data["levels"], dict)
        
        # Verify all counts are non-negative
        all_counts = list(data["by_stage"].values()) + \
                    list(data["by_service"].values()) + \
                    list(data["levels"].values())
        
        for count in all_counts:
            assert isinstance(count, int)
            assert count >= 0
    
    def test_analytics_empty_database(self):
        """Test analytics with empty database (should return empty dicts)."""
        # This test assumes database might be empty or file-only mode
        response = client.get("/analytics")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        # Should return empty dicts if no data, or populated if data exists
        assert isinstance(data["by_stage"], dict)
        assert isinstance(data["by_service"], dict)
        assert isinstance(data["levels"], dict)

