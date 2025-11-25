"""
Basic tests for creative_service generate_creatives endpoint.
"""

import pytest
from unittest.mock import patch
from app.common.schemas import Creative, ErrorResponse
from tests.testdata import VALID_CAMPAIGN_SPEC_META_ELECTRONICS, SAMPLE_PRODUCTS_ELECTRONICS


class TestGenerateCreativesBasic:
    """Basic tests for generate_creatives endpoint."""
    
    def test_generate_creatives_success(self, creative_client, mock_gemini_text, mock_gemini_image):
        """Test successful creative generation."""
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
        assert "creatives" in data
        assert len(data["creatives"]) >= 2  # At least A and B variants
        
        # Verify creative structure
        creative = data["creatives"][0]
        assert "creative_id" in creative
        assert "product_id" in creative
        assert "platform" in creative
        assert "variant_id" in creative
        assert "primary_text" in creative
        assert creative["platform"] == "meta"
        assert creative["variant_id"] in ["A", "B"]
        
        # Verify debug info
        assert "debug" in data
        assert "copy_prompts" in data["debug"]
        assert "image_prompts" in data["debug"]
        assert "policy_used" in data["debug"]
    
    def test_generate_creatives_multiple_products(self, creative_client, mock_gemini_text, mock_gemini_image):
        """Test generating creatives for multiple products."""
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS[:2]],
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
        assert len(data["creatives"]) >= 4  # 2 products * 2 variants
    
    def test_generate_creatives_with_custom_variants(self, creative_client, mock_gemini_text, mock_gemini_image):
        """Test generating creatives with custom variant count."""
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS[:1]],
            "ab_config": {
                "variants_per_product": 3,
                "max_creatives": 10,
                "enable_image_generation": True
            }
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["creatives"]) >= 3  # 3 variants
        
        # Check variant IDs
        variant_ids = {c["variant_id"] for c in data["creatives"]}
        assert "A" in variant_ids
        assert "B" in variant_ids
        assert "C" in variant_ids
    
    def test_generate_creatives_max_limit(self, creative_client, mock_gemini_text, mock_gemini_image):
        """Test max_creatives limit is respected."""
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS * 3],  # 9 products
            "ab_config": {
                "variants_per_product": 2,
                "max_creatives": 5,  # Limit to 5
                "enable_image_generation": True
            }
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["creatives"]) <= 5  # Should not exceed max
    
    def test_generate_creatives_no_products(self, creative_client):
        """Test error when no products provided."""
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": []
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        assert response.status_code == 200  # Service returns 200 with error status
        data = response.json()
        assert data["status"] == "error"
        assert "error_code" in data
    
    def test_generate_creatives_image_generation_disabled(self, creative_client, mock_gemini_text):
        """Test creative generation with image generation disabled."""
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS[:1]],
            "ab_config": {
                "variants_per_product": 2,
                "max_creatives": 10,
                "enable_image_generation": False
            }
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        # All creatives should have image_url (from fallback)
        for creative in data["creatives"]:
            assert "image_url" in creative
            assert creative["image_url"] is not None

