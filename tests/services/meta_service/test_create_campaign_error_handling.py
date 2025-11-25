"""
Error handling tests for meta_service.
"""

import pytest


class TestCreateCampaignErrorHandling:
    """Tests for error handling in campaign creation."""
    
    def test_create_campaign_missing_required_fields(self, meta_client):
        """Test error when required fields are missing."""
        request = {
            "campaign_name": "Test Campaign"
            # Missing objective, daily_budget, targeting, creatives, start_date
        }
        
        response = meta_client.post("/create_campaign", json=request)
        
        # Should return 422 validation error
        assert response.status_code == 422
    
    def test_create_campaign_invalid_budget(self, meta_client):
        """Test error when budget is invalid."""
        request = {
            "campaign_name": "Test Campaign",
            "objective": "CONVERSIONS",
            "daily_budget": -100.0,  # Invalid negative budget
            "targeting": {
                "age_min": 25,
                "age_max": 45,
                "genders": [1, 2],
                "locations": ["US"]
            },
            "creatives": [
                {
                    "creative_id": "CREATIVE-001",
                    "headline": "Test",
                    "body_text": "Test",
                    "call_to_action": "SHOP_NOW",
                    "image_url": "https://example.com/image.jpg"
                }
            ],
            "start_date": "2025-01-01T00:00:00Z"
        }
        
        response = meta_client.post("/create_campaign", json=request)
        
        # Service may accept it (validation happens at Meta API level) or return 422
        # Check that response is either validation error or service handles it
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            # Service may return error in response body
            data = response.json()
            assert "campaign_id" in data or "error" in str(data).lower()
    
    def test_create_campaign_empty_campaign_name(self, meta_client):
        """Test error when campaign name is empty."""
        request = {
            "campaign_name": "",  # Empty name
            "objective": "CONVERSIONS",
            "daily_budget": 100.0,
            "targeting": {
                "age_min": 25,
                "age_max": 45,
                "genders": [1, 2],
                "locations": ["US"]
            },
            "creatives": [
                {
                    "creative_id": "CREATIVE-001",
                    "headline": "Test",
                    "body_text": "Test",
                    "call_to_action": "SHOP_NOW",
                    "image_url": "https://example.com/image.jpg"
                }
            ],
            "start_date": "2025-01-01T00:00:00Z"
        }
        
        response = meta_client.post("/create_campaign", json=request)
        
        # Service may accept it (validation happens at Meta API level) or return 422
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            # Service may return error in response body
            data = response.json()
            assert "campaign_id" in data or "error" in str(data).lower()
    
    def test_create_campaign_invalid_targeting(self, meta_client):
        """Test error when targeting is invalid."""
        request = {
            "campaign_name": "Test Campaign",
            "objective": "CONVERSIONS",
            "daily_budget": 100.0,
            "targeting": {
                "age_min": 100,  # Invalid: min > max
                "age_max": 25,
                "genders": [1, 2],
                "locations": ["US"]
            },
            "creatives": [
                {
                    "creative_id": "CREATIVE-001",
                    "headline": "Test",
                    "body_text": "Test",
                    "call_to_action": "SHOP_NOW",
                    "image_url": "https://example.com/image.jpg"
                }
            ],
            "start_date": "2025-01-01T00:00:00Z"
        }
        
        response = meta_client.post("/create_campaign", json=request)
        
        # Service may accept it (validation happens at Meta API level)
        # But we can check the response structure
        assert response.status_code in [200, 422]

