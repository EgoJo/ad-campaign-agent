"""
Tests for Meta Service
"""

import pytest
from fastapi.testclient import TestClient
from app.services.meta_service.main import app

client = TestClient(app)


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test basic health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "meta_service"


class TestCreateCampaign:
    """Test campaign creation endpoint"""
    
    def test_create_campaign_success(self):
        """Test successful campaign creation"""
        payload = {
            "campaign_name": "Test Campaign",
            "objective": "conversions",
            "daily_budget": 100,
            "targeting": {
                "age_min": 25,
                "age_max": 45,
                "genders": [1, 2],
                "locations": ["US"]
            },
            "creatives": [
                {
                    "creative_id": "creative_1",
                    "headline": "Test Headline 1",
                    "body_text": "Test body text 1",
                    "call_to_action": "Learn More",
                    "image_url": "https://example.com/image1.jpg"
                },
                {
                    "creative_id": "creative_2",
                    "headline": "Test Headline 2",
                    "body_text": "Test body text 2",
                    "call_to_action": "Shop Now",
                    "image_url": "https://example.com/image2.jpg"
                }
            ],
            "start_date": "2025-01-01"
        }
        response = client.post("/create_campaign", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "campaign_id" in data
        assert "ad_set_id" in data
        assert "ad_ids" in data
        assert len(data["ad_ids"]) > 0
    
    def test_create_campaign_validation_error(self):
        """Test campaign creation with invalid payload"""
        payload = {
            "campaign_name": "",
            "daily_budget": -100  # Invalid budget
        }
        response = client.post("/create_campaign", json=payload)
        assert response.status_code == 422
    
    def test_create_campaign_missing_creatives(self):
        """Test campaign creation with missing creatives"""
        payload = {
            "campaign_name": "Test Campaign",
            "objective": "conversions",
            "daily_budget": 100,
            "targeting": {},
            "creatives": [],  # Empty creatives
            "start_date": "2025-01-01"
        }
        response = client.post("/create_campaign", json=payload)
        # Should still succeed but with empty ad_ids
        assert response.status_code == 200

