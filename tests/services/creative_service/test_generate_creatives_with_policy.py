"""
Tests for creative_service with different policy configurations.
"""

import pytest
from unittest.mock import patch
from tests.testdata import VALID_CAMPAIGN_SPEC_META_TOYS, SAMPLE_PRODUCTS_TOYS


class TestGenerateCreativesWithPolicy:
    """Tests for policy-based creative generation."""
    
    def test_generate_creatives_toys_policy(self, creative_client, mock_gemini_text, mock_gemini_image):
        """Test that toys category uses playful policy."""
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_TOYS.model_dump(),
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_TOYS[:1]],
            "ab_config": {
                "variants_per_product": 2,
                "max_creatives": 10,
                "enable_image_generation": True
            }
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # Check policy was applied
        assert "policy_used" in data["debug"]
        policy_info = data["debug"]["policy_used"]
        assert "products_processed" in policy_info
        
        # Find the product in policy info
        product_policy = next(
            (p for p in policy_info["products_processed"] if p["product_id"] == SAMPLE_PRODUCTS_TOYS[0].product_id),
            None
        )
        assert product_policy is not None
        assert product_policy["category"] == "toys"
        # Policy should have playful style
        applied_policy = product_policy["policy_applied"]
        assert "copy_style" in applied_policy or "visual_style" in applied_policy
    
    def test_generate_creatives_electronics_policy(self, creative_client, mock_gemini_text, mock_gemini_image):
        """Test that electronics category uses technical policy."""
        from tests.testdata import VALID_CAMPAIGN_SPEC_META_ELECTRONICS, SAMPLE_PRODUCTS_ELECTRONICS
        
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS[:1]],
            "ab_config": {
                "variants_per_product": 2,
                "max_creatives": 10,
                "enable_image_generation": True
            }
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # Check policy was applied
        assert "policy_used" in data["debug"]
        policy_info = data["debug"]["policy_used"]
        product_policy = next(
            (p for p in policy_info["products_processed"] if p["category"] == "electronics"),
            None
        )
        assert product_policy is not None
        applied_policy = product_policy["policy_applied"]
        # Electronics should have technical style
        assert "copy_style" in applied_policy or "visual_style" in applied_policy
    
    def test_generate_creatives_default_policy_fallback(self, creative_client, mock_gemini_text, mock_gemini_image):
        """Test that unknown category falls back to default policy."""
        from app.common.schemas import CampaignSpec, Product
        
        unknown_category_spec = CampaignSpec(
            user_query="Test campaign",
            platform="meta",
            budget=1000.0,
            objective="conversions",
            category="unknown_category",
            metadata={}
        )
        
        unknown_product = Product(
            product_id="UNKNOWN-001",
            title="Unknown Product",
            description="Test product",
            price=50.0,
            category="unknown_category",
            metadata={}
        )
        
        request = {
            "campaign_spec": unknown_category_spec.model_dump(),
            "products": [unknown_product.model_dump()],
            "ab_config": {
                "variants_per_product": 2,
                "max_creatives": 10,
                "enable_image_generation": True
            }
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        
        # Should still generate creatives using default policy
        assert len(data["creatives"]) >= 2
        assert "policy_used" in data["debug"]
        assert "default_policy" in data["debug"]["policy_used"]

