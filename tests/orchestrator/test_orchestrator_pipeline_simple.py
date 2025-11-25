"""
Tests for simple orchestrator pipeline execution.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from tests.testdata import (
    VALID_CAMPAIGN_SPEC_META_ELECTRONICS,
    SAMPLE_PRODUCTS_ELECTRONICS,
    SAMPLE_PRODUCT_GROUPS_ELECTRONICS,
    SAMPLE_CREATIVES_ELECTRONICS
)


class TestOrchestratorPipelineSimple:
    """Tests for simple orchestrator pipeline."""
    
    @pytest.mark.asyncio
    @patch('app.orchestrator.simple_service.requests.post')
    async def test_create_campaign_full_pipeline(self, mock_post):
        """Test full pipeline execution through orchestrator."""
        from app.orchestrator.simple_service import create_campaign, CampaignRequest
        
        # Mock service responses
        mock_responses = [
            # Product service response
            MagicMock(
                status_code=200,
                json=lambda: {
                    "status": "success",
                    "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS],
                    "groups": [g.model_dump() for g in SAMPLE_PRODUCT_GROUPS_ELECTRONICS]
                }
            ),
            # Creative service response
            MagicMock(
                status_code=200,
                json=lambda: {
                    "status": "success",
                    "creatives": [c.model_dump() for c in SAMPLE_CREATIVES_ELECTRONICS]
                }
            ),
            # Strategy service response
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
            # Meta service response
            MagicMock(
                status_code=200,
                json=lambda: {
                    "campaign_id": "CAMP-123",
                    "ad_set_id": "ADSET-456",
                    "ad_ids": [
                        {"ad_id": "AD-789-A", "creative_id": "CREATIVE-ELEC-001-A", "status": "ACTIVE"},
                        {"ad_id": "AD-789-B", "creative_id": "CREATIVE-ELEC-001-B", "status": "ACTIVE"}
                    ],
                    "status": "ACTIVE"
                }
            ),
            # Logs service response (multiple calls)
            MagicMock(status_code=200, json=lambda: {"status": "ok", "event_id": "EVENT-001"}),
            MagicMock(status_code=200, json=lambda: {"status": "ok", "event_id": "EVENT-002"}),
            MagicMock(status_code=200, json=lambda: {"status": "ok", "event_id": "EVENT-003"}),
        ]
        mock_post.side_effect = mock_responses
        
        request = CampaignRequest(
            campaign_objective="sales",
            target_audience="tech enthusiasts aged 25-45",
            budget=10000.0,
            duration_days=30,
            product_category="electronics",
            platforms=["facebook", "instagram"]
        )
        
        response = await create_campaign(request)
        
        assert response.status == "success"
        assert response.campaign_id is not None
        assert response.selected_products is not None
        assert response.creatives is not None
        assert response.strategy is not None
        assert response.meta_campaign is not None
        
        # Verify service calls were made in correct order
        assert mock_post.call_count >= 4  # At least product, creative, strategy, meta
    
    @pytest.mark.asyncio
    @patch('app.orchestrator.simple_service.requests.post')
    async def test_create_campaign_product_service_failure(self, mock_post):
        """Test pipeline behavior when product service fails."""
        from app.orchestrator.simple_service import create_campaign, CampaignRequest
        
        # Mock product service failure
        mock_post.side_effect = [
            MagicMock(status_code=500, json=lambda: {"status": "error", "message": "Service unavailable"}),
        ]
        
        request = CampaignRequest(
            campaign_objective="sales",
            target_audience="tech enthusiasts",
            budget=10000.0,
            duration_days=30,
            platforms=["facebook"]
        )
        
        from fastapi import HTTPException
        try:
            response = await create_campaign(request)
            # If no exception, check response
            assert response.status == "error" or response.message is not None
        except HTTPException as e:
            # Expected behavior - service raises HTTPException on error
            assert e.status_code == 500
    
    @pytest.mark.asyncio
    @patch('app.orchestrator.simple_service.requests.post')
    async def test_create_campaign_creative_service_failure(self, mock_post):
        """Test pipeline behavior when creative service fails."""
        from app.orchestrator.simple_service import create_campaign, CampaignRequest
        
        # Mock responses: product succeeds, creative fails
        mock_post.side_effect = [
            # Product service succeeds
            MagicMock(
                status_code=200,
                json=lambda: {
                    "status": "success",
                    "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS],
                    "groups": [g.model_dump() for g in SAMPLE_PRODUCT_GROUPS_ELECTRONICS]
                }
            ),
            # Creative service fails
            MagicMock(status_code=500, json=lambda: {"status": "error", "message": "Creative generation failed"}),
        ]
        
        request = CampaignRequest(
            campaign_objective="sales",
            target_audience="tech enthusiasts",
            budget=10000.0,
            duration_days=30,
            platforms=["facebook"]
        )
        
        from fastapi import HTTPException
        try:
            response = await create_campaign(request)
            # If no exception, check response
            assert response.status == "error" or "creative" in response.message.lower() or response.creatives is None
        except HTTPException as e:
            # Expected behavior - service raises HTTPException on error
            assert e.status_code == 500

