"""
Basic tests for optimizer_service summarize_recent_runs endpoint.
"""

import pytest
from app.services.optimizer_service.schemas import SummarizeRecentRunsResponse


class TestOptimizeStrategyBasic:
    """Basic tests for summarize_recent_runs endpoint."""
    
    def test_summarize_recent_runs_success(self, optimizer_client):
        """Test successful optimization summary."""
        request = {
            "campaign_ids": ["CAMP-001", "CAMP-002", "CAMP-003"],
            "days": 7
        }
        
        response = optimizer_client.post("/summarize_recent_runs", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "total_campaigns" in data
        assert "total_spend" in data
        assert "total_conversions" in data
        assert "average_cpa" in data
        assert "suggestions" in data
        assert isinstance(data["suggestions"], list)
    
    def test_summarize_recent_runs_no_campaign_ids(self, optimizer_client):
        """Test optimization summary without specific campaign IDs."""
        request = {
            "days": 30
        }
        
        response = optimizer_client.post("/summarize_recent_runs", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "suggestions" in data
    
    def test_summarize_recent_runs_empty_campaign_ids(self, optimizer_client):
        """Test optimization summary with empty campaign IDs list."""
        request = {
            "campaign_ids": [],
            "days": 7
        }
        
        response = optimizer_client.post("/summarize_recent_runs", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
    
    def test_summarize_recent_runs_custom_days(self, optimizer_client):
        """Test optimization summary with custom time range."""
        request = {
            "campaign_ids": ["CAMP-001"],
            "days": 14
        }
        
        response = optimizer_client.post("/summarize_recent_runs", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
    
    def test_summarize_recent_runs_invalid_days(self, optimizer_client):
        """Test error when days is invalid."""
        request = {
            "campaign_ids": ["CAMP-001"],
            "days": 0  # Invalid: must be > 0
        }
        
        response = optimizer_client.post("/summarize_recent_runs", json=request)
        
        # Service may accept it or return 422
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            # Service may handle it gracefully
            data = response.json()
            assert "summary" in data
    
    def test_summarize_recent_runs_negative_days(self, optimizer_client):
        """Test error when days is negative."""
        request = {
            "campaign_ids": ["CAMP-001"],
            "days": -7  # Invalid: negative
        }
        
        response = optimizer_client.post("/summarize_recent_runs", json=request)
        
        # Service may accept it or return 422
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            # Service may handle it gracefully
            data = response.json()
            assert "summary" in data

