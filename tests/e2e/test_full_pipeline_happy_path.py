"""
End-to-end test for the complete happy path pipeline.

Tests the full flow:
product_service → creative_service → strategy_service → meta_service → logs_service
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from tests.testdata import (
    VALID_CAMPAIGN_SPEC_META_ELECTRONICS,
    SAMPLE_PRODUCTS_ELECTRONICS,
    SAMPLE_PRODUCT_GROUPS_ELECTRONICS,
    SAMPLE_CREATIVES_ELECTRONICS
)


class TestFullPipelineHappyPath:
    """End-to-end tests for complete pipeline execution."""
    
    @pytest.fixture
    def mock_all_services(self):
        """Mock all external service calls."""
        with patch('app.services.creative_service.creative_utils.call_gemini_text') as mock_gemini_text, \
             patch('app.services.creative_service.creative_utils.call_gemini_image') as mock_gemini_image:
            
            # Mock Gemini responses
            mock_gemini_text.return_value = '{"headline": "Test Headline", "primary_text": "Test primary text content for the ad campaign."}'
            mock_gemini_image.return_value = "https://example.com/generated-image.jpg"
            
            yield {
                "gemini_text": mock_gemini_text,
                "gemini_image": mock_gemini_image
            }
    
    def test_full_pipeline_e2e(self, mock_all_services):
        """Test complete E2E pipeline execution."""
        from app.services.product_service.main import app as product_app
        from app.services.creative_service.main import app as creative_app
        from app.services.strategy_service.main import app as strategy_app
        from app.services.meta_service.main import app as meta_app
        from app.services.logs_service.main import app as logs_app
        
        product_client = TestClient(product_app)
        creative_client = TestClient(creative_app)
        strategy_client = TestClient(strategy_app)
        meta_client = TestClient(meta_app)
        logs_client = TestClient(logs_app)
        
        # Step 1: Select products
        product_request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "limit": 3
        }
        product_response = product_client.post("/select_products", json=product_request)
        assert product_response.status_code == 200
        product_data = product_response.json()
        assert product_data["status"] == "success"
        assert "products" in product_data or "groups" in product_data
        
        # Extract products for next step
        if "products" in product_data:
            products = product_data["products"]
        else:
            # Extract from groups
            products = []
            for group in product_data.get("groups", []):
                products.extend(group.get("products", []))
        
        assert len(products) > 0
        
        # Step 2: Generate creatives
        creative_request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": products[:2],  # Use first 2 products
            "ab_config": {
                "variants_per_product": 2,
                "max_creatives": 10,
                "enable_image_generation": True
            }
        }
        creative_response = creative_client.post("/generate_creatives", json=creative_request)
        assert creative_response.status_code == 200
        creative_data = creative_response.json()
        assert creative_data["status"] == "success"
        assert len(creative_data["creatives"]) >= 4  # 2 products * 2 variants
        
        creatives = creative_data["creatives"]
        
        # Step 3: Generate strategy
        # Get product groups from product service response
        product_groups = product_data.get("groups", [])
        if not product_groups:
            # Create groups from products
            product_groups = [{
                "group": "high",
                "products": products,
                "score_range": [0.8, 1.0]
            }]
        
        strategy_request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "product_groups": product_groups,
            "creatives": creatives
        }
        strategy_response = strategy_client.post("/generate_strategy", json=strategy_request)
        assert strategy_response.status_code == 200
        strategy_data = strategy_response.json()
        assert strategy_data["status"] == "success"
        assert "abstract_strategy" in strategy_data or "platform_strategies" in strategy_data
        
        # Step 4: Create campaign on Meta
        # Convert creatives to Meta format
        meta_creatives = [
            {
                "creative_id": c["creative_id"],
                "headline": c.get("headline", ""),
                "body_text": c["primary_text"],
                "call_to_action": "SHOP_NOW",
                "image_url": c.get("image_url")
            }
            for c in creatives[:2]  # Use first 2 creatives
        ]
        
        meta_request = {
            "campaign_name": "E2E Test Campaign",
            "objective": "CONVERSIONS",
            "daily_budget": 100.0,
            "targeting": {
                "age_min": 25,
                "age_max": 45,
                "genders": [1, 2],
                "locations": ["US"],
                "interests": ["technology", "electronics"]
            },
            "creatives": meta_creatives,
            "start_date": "2025-01-01T00:00:00Z"
        }
        meta_response = meta_client.post("/create_campaign", json=meta_request)
        assert meta_response.status_code == 200
        meta_data = meta_response.json()
        assert "campaign_id" in meta_data
        assert "ad_set_id" in meta_data
        assert "ad_ids" in meta_data
        
        # Step 5: Log events
        log_request = {
            "timestamp": "2025-01-01T00:00:00Z",
            "stage": "orchestrator",
            "service": "orchestrator_agent",
            "success": True,
            "metadata": {
                "message": "E2E test campaign created",
                "campaign_id": meta_data["campaign_id"]
            }
        }
        log_response = logs_client.post("/append_event", json=log_request)
        assert log_response.status_code == 200
        log_data = log_response.json()
        assert log_data["status"] == "success"
        assert "event_id" in log_data
        
        # Verify complete pipeline executed successfully
        assert product_data["status"] == "success"
        assert creative_data["status"] == "success"
        assert strategy_data["status"] == "success"
        assert "campaign_id" in meta_data
        assert log_data["status"] == "success"
    
    def test_full_pipeline_with_orchestrator(self, mock_all_services):
        """Test E2E pipeline through orchestrator."""
        from app.orchestrator.simple_service import app as orchestrator_app
        from unittest.mock import patch
        
        orchestrator_client = TestClient(orchestrator_app)
        
        # Mock all service HTTP calls
        with patch('app.orchestrator.simple_service.requests.post') as mock_post:
            # Setup mock responses
            mock_responses = [
                # Product service
                MagicMock(
                    status_code=200,
                    json=lambda: {
                        "status": "success",
                        "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS],
                        "groups": [g.model_dump() for g in SAMPLE_PRODUCT_GROUPS_ELECTRONICS]
                    }
                ),
                # Creative service
                MagicMock(
                    status_code=200,
                    json=lambda: {
                        "status": "success",
                        "creatives": [c.model_dump() for c in SAMPLE_CREATIVES_ELECTRONICS]
                    }
                ),
                # Strategy service
                MagicMock(
                    status_code=200,
                    json=lambda: {
                        "status": "success",
                        "abstract_strategy": {
                            "objective": "conversions",
                            "budget_split": {"A": 0.5, "B": 0.5},
                            "bidding_strategy": "lowest_cost"
                        },
                        "platform_strategies": []
                    }
                ),
                # Meta service
                MagicMock(
                    status_code=200,
                    json=lambda: {
                        "campaign_id": "CAMP-E2E-123",
                        "ad_set_id": "ADSET-E2E-456",
                        "ad_ids": [
                            {"ad_id": "AD-E2E-789", "creative_id": "CREATIVE-ELEC-001-A", "status": "ACTIVE"}
                        ],
                        "status": "ACTIVE"
                    }
                ),
                # Logs service (multiple calls)
                MagicMock(status_code=200, json=lambda: {"status": "ok", "event_id": "EVENT-E2E-001"}),
                MagicMock(status_code=200, json=lambda: {"status": "ok", "event_id": "EVENT-E2E-002"}),
            ]
            mock_post.side_effect = mock_responses
            
            request = {
                "campaign_objective": "sales",
                "target_audience": "tech enthusiasts aged 25-45",
                "budget": 10000.0,
                "duration_days": 30,
                "product_category": "electronics",
                "platforms": ["facebook", "instagram"]
            }
            
            response = orchestrator_client.post("/create_campaign", json=request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["campaign_id"] is not None
            assert data["selected_products"] is not None
            assert data["creatives"] is not None
            assert data["strategy"] is not None
            assert data["meta_campaign"] is not None
            
            # Verify all services were called
            assert mock_post.call_count >= 4

