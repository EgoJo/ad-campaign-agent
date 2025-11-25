"""
Basic tests for meta_service create_campaign endpoint.
"""

import pytest
from unittest.mock import patch
from app.services.meta_service.schemas import CreateCampaignResponse, AdResult


class TestCreateCampaignBasic:
    """Basic tests for create_campaign endpoint."""
    
    def test_create_campaign_success(self, meta_client):
        """Test successful campaign creation."""
        request = {
            "campaign_name": "Test Electronics Campaign",
            "objective": "CONVERSIONS",
            "daily_budget": 100.0,
            "targeting": {
                "age_min": 25,
                "age_max": 45,
                "genders": [1, 2],
                "locations": ["US"],
                "interests": ["technology", "electronics"]
            },
            "creatives": [
                {
                    "creative_id": "CREATIVE-001-A",
                    "headline": "Amazing Headphones",
                    "body_text": "Experience premium sound quality",
                    "call_to_action": "SHOP_NOW",
                    "image_url": "https://example.com/image1.jpg"
                },
                {
                    "creative_id": "CREATIVE-001-B",
                    "headline": "Premium Audio",
                    "body_text": "Wireless freedom for your music",
                    "call_to_action": "LEARN_MORE",
                    "image_url": "https://example.com/image2.jpg"
                }
            ],
            "start_date": "2025-01-01T00:00:00Z"
        }
        
        response = meta_client.post("/create_campaign", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert "campaign_id" in data
        assert "ad_set_id" in data
        assert "ad_ids" in data
        assert len(data["ad_ids"]) == 2  # One ad per creative
        assert data["status"] in ["ACTIVE", "PENDING_REVIEW"]
        
        # Verify ad structure
        for ad in data["ad_ids"]:
            assert "ad_id" in ad
            assert "creative_id" in ad
            assert "status" in ad
    
    def test_create_campaign_with_end_date(self, meta_client):
        """Test campaign creation with end date."""
        request = {
            "campaign_name": "Test Campaign with End Date",
            "objective": "REACH",
            "daily_budget": 50.0,
            "targeting": {
                "age_min": 18,
                "age_max": 65,
                "genders": [1, 2],
                "locations": ["US"]
            },
            "creatives": [
                {
                    "creative_id": "CREATIVE-001",
                    "headline": "Test Headline",
                    "body_text": "Test body",
                    "call_to_action": "SHOP_NOW",
                    "image_url": "https://example.com/image.jpg"
                }
            ],
            "start_date": "2025-01-01T00:00:00Z",
            "end_date": "2025-01-31T23:59:59Z"
        }
        
        response = meta_client.post("/create_campaign", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert "campaign_id" in data
    
    def test_create_campaign_single_creative(self, meta_client):
        """Test campaign creation with single creative."""
        request = {
            "campaign_name": "Single Creative Campaign",
            "objective": "TRAFFIC",
            "daily_budget": 25.0,
            "targeting": {
                "age_min": 25,
                "age_max": 45,
                "genders": [1, 2],
                "locations": ["US"]
            },
            "creatives": [
                {
                    "creative_id": "CREATIVE-SINGLE",
                    "headline": "Single Creative",
                    "body_text": "Test content",
                    "call_to_action": "SHOP_NOW",
                    "image_url": "https://example.com/image.jpg"
                }
            ],
            "start_date": "2025-01-01T00:00:00Z"
        }
        
        response = meta_client.post("/create_campaign", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["ad_ids"]) == 1
    
    def test_create_campaign_empty_creatives(self, meta_client):
        """Test campaign creation with empty creatives list."""
        request = {
            "campaign_name": "Empty Creatives Campaign",
            "objective": "CONVERSIONS",
            "daily_budget": 100.0,
            "targeting": {
                "age_min": 25,
                "age_max": 45,
                "genders": [1, 2],
                "locations": ["US"]
            },
            "creatives": [],
            "start_date": "2025-01-01T00:00:00Z"
        }
        
        response = meta_client.post("/create_campaign", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert "campaign_id" in data
        assert len(data["ad_ids"]) == 0  # No ads if no creatives

