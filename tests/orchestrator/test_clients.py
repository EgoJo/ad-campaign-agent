"""
Unit tests for orchestrator clients.
"""

import pytest
from unittest.mock import patch, MagicMock
from app.orchestrator.clients.product_client import ProductClient
from app.orchestrator.clients.creative_client import CreativeClient
from app.orchestrator.clients.strategy_client import StrategyClient
from app.orchestrator.clients.meta_client import MetaClient
from app.orchestrator.clients.logs_client import LogsClient
from app.orchestrator.clients.optimizer_client import OptimizerClient
from tests.testdata import VALID_CAMPAIGN_SPEC_META_ELECTRONICS, SAMPLE_PRODUCTS_ELECTRONICS


class TestProductClient:
    """Tests for ProductClient."""
    
    @patch('app.orchestrator.clients.product_client.MCPClient')
    def test_select_products_success(self, mock_mcp_client_class):
        """Test successful product selection."""
        mock_client_instance = MagicMock()
        mock_mcp_client_class.return_value = mock_client_instance
        
        mock_response = {
            "status": "success",
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS],
            "groups": []
        }
        mock_client_instance.post.return_value = mock_response
        
        client = ProductClient()
        # Replace the client's internal client with our mock
        client.client = mock_client_instance
        
        result = client.select_products(
            campaign_objective="sales",
            target_audience="tech enthusiasts",
            budget=10000.0,
            max_products=10
        )
        
        assert result["status"] == "success"
        assert "products" in result
        mock_client_instance.post.assert_called_once()
        call_args = mock_client_instance.post.call_args
        assert call_args[0][0] == "/select_products"
        client.close()
    
    @patch('app.orchestrator.clients.product_client.MCPClient')
    def test_select_products_error(self, mock_mcp_client_class):
        """Test product selection error handling."""
        mock_client_instance = MagicMock()
        mock_mcp_client_class.return_value = mock_client_instance
        mock_client_instance.post.side_effect = Exception("Service unavailable")
        
        client = ProductClient()
        client.client = mock_client_instance
        
        with pytest.raises(Exception):
            client.select_products(
                campaign_objective="sales",
                target_audience="tech enthusiasts",
                budget=10000.0
            )
        client.close()


class TestCreativeClient:
    """Tests for CreativeClient."""
    
    @patch('app.orchestrator.clients.creative_client.MCPClient')
    def test_generate_creatives_success(self, mock_mcp_client_class):
        """Test successful creative generation."""
        mock_client_instance = MagicMock()
        mock_mcp_client_class.return_value = mock_client_instance
        
        mock_response = {
            "status": "success",
            "creatives": [
                {
                    "creative_id": "CREATIVE-001-A",
                    "product_id": "PROD-001",
                    "platform": "meta",
                    "variant_id": "A",
                    "primary_text": "Test text",
                    "headline": "Test headline"
                }
            ]
        }
        mock_client_instance.post.return_value = mock_response
        
        client = CreativeClient()
        client.client = mock_client_instance
        
        result = client.generate_creatives(
            product_ids=["PROD-001"],
            campaign_objective="sales",
            target_audience="tech enthusiasts"
        )
        
        assert result["status"] == "success"
        assert "creatives" in result
        mock_client_instance.post.assert_called_once()
        client.close()


class TestStrategyClient:
    """Tests for StrategyClient."""
    
    @patch('app.orchestrator.clients.strategy_client.MCPClient')
    def test_generate_strategy_success(self, mock_mcp_client_class):
        """Test successful strategy generation."""
        mock_client_instance = MagicMock()
        mock_mcp_client_class.return_value = mock_client_instance
        
        mock_response = {
            "status": "success",
            "abstract_strategy": {
                "objective": "conversions",
                "budget_split": {"A": 0.4, "B": 0.6},
                "bidding_strategy": "lowest_cost"
            },
            "platform_strategies": []
        }
        mock_client_instance.post.return_value = mock_response
        
        client = StrategyClient()
        client.client = mock_client_instance
        
        result = client.generate_strategy(
            campaign_objective="sales",
            total_budget=10000.0,
            duration_days=30,
            target_audience="tech enthusiasts",
            platforms=["facebook", "instagram"]
        )
        
        assert result["status"] == "success"
        assert "abstract_strategy" in result
        mock_client_instance.post.assert_called_once()
        client.close()


class TestMetaClient:
    """Tests for MetaClient."""
    
    @patch('app.orchestrator.clients.meta_client.MCPClient')
    def test_create_campaign_success(self, mock_mcp_client_class):
        """Test successful campaign creation."""
        mock_client_instance = MagicMock()
        mock_mcp_client_class.return_value = mock_client_instance
        
        mock_response = {
            "campaign_id": "CAMP-123",
            "ad_set_id": "ADSET-456",
            "ad_ids": [
                {"ad_id": "AD-789", "creative_id": "CREATIVE-001", "status": "ACTIVE"}
            ],
            "status": "ACTIVE"
        }
        mock_client_instance.post.return_value = mock_response
        
        client = MetaClient()
        client.client = mock_client_instance
        
        result = client.create_campaign(
            campaign_name="Test Campaign",
            objective="CONVERSIONS",
            daily_budget=100.0,
            targeting={"age_min": 25, "age_max": 45},
            creatives=[{"creative_id": "CREATIVE-001", "headline": "Test", "body_text": "Test", "call_to_action": "SHOP_NOW"}],
            start_date="2025-01-01T00:00:00Z"
        )
        
        assert "campaign_id" in result
        assert result["campaign_id"] == "CAMP-123"
        mock_client_instance.post.assert_called_once()
        client.close()


class TestLogsClient:
    """Tests for LogsClient."""
    
    @patch('app.orchestrator.clients.logs_client.MCPClient')
    def test_append_event_success(self, mock_mcp_client_class):
        """Test successful event logging."""
        mock_client_instance = MagicMock()
        mock_mcp_client_class.return_value = mock_client_instance
        
        mock_response = {
            "status": "ok",
            "event_id": "EVENT-123"
        }
        mock_client_instance.post.return_value = mock_response
        
        client = LogsClient()
        client.client = mock_client_instance
        
        result = client.append_event(
            event_type="campaign_created",
            message="Campaign created successfully",
            campaign_id="CAMP-123"
        )
        
        assert result["status"] == "ok"
        assert "event_id" in result
        mock_client_instance.post.assert_called_once()
        client.close()


class TestOptimizerClient:
    """Tests for OptimizerClient."""
    
    @patch('app.orchestrator.clients.optimizer_client.MCPClient')
    def test_summarize_recent_runs_success(self, mock_mcp_client_class):
        """Test successful optimization summary."""
        mock_client_instance = MagicMock()
        mock_mcp_client_class.return_value = mock_client_instance
        
        mock_response = {
            "summary": "Campaign performance summary",
            "total_campaigns": 5,
            "total_spend": 5000.0,
            "total_conversions": 100,
            "average_cpa": 50.0,
            "suggestions": []
        }
        mock_client_instance.post.return_value = mock_response
        
        client = OptimizerClient()
        client.client = mock_client_instance
        
        result = client.summarize_recent_runs(
            campaign_ids=["CAMP-001", "CAMP-002"],
            days=7
        )
        
        assert "summary" in result
        assert result["total_campaigns"] == 5
        mock_client_instance.post.assert_called_once()
        client.close()

