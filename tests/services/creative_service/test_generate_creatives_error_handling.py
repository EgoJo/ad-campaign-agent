"""
Error handling tests for creative_service.
"""

import pytest
from unittest.mock import patch
from tests.testdata import VALID_CAMPAIGN_SPEC_META_ELECTRONICS, SAMPLE_PRODUCTS_ELECTRONICS


class TestGenerateCreativesErrorHandling:
    """Tests for error handling in creative generation."""
    
    def test_generate_creatives_invalid_campaign_spec(self, creative_client):
        """Test error when campaign_spec is invalid."""
        request = {
            "campaign_spec": {
                "user_query": "Test",
                "platform": "invalid_platform",  # Invalid
                "budget": 1000.0,
                "objective": "conversions",
                "category": "electronics"
            },
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS[:1]]
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        # Should return 422 validation error
        assert response.status_code == 422
    
    def test_generate_creatives_missing_campaign_spec(self, creative_client):
        """Test error when campaign_spec is missing."""
        request = {
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS[:1]]
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        # Should return 422 validation error
        assert response.status_code == 422
    
    def test_generate_creatives_llm_failure_fallback(self, creative_client, mock_gemini_failure):
        """Test that LLM failure triggers fallback."""
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
        
        # Should still generate creatives using fallback
        assert len(data["creatives"]) >= 2
        
        # Check that fallback was used
        debug = data["debug"]
        assert "raw_llm_responses" in debug
        # At least some LLM calls should have failed
        llm_responses = [r for r in debug["raw_llm_responses"] if r.get("type") == "copy"]
        if llm_responses:
            # Check if any used fallback
            assert any(not r.get("llm_call_success", False) for r in llm_responses) or \
                   any("fallback" in str(r.get("response", "")).lower() for r in llm_responses)
    
    def test_generate_creatives_empty_products(self, creative_client):
        """Test error when products list is empty."""
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": []
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        assert response.status_code == 200  # Service returns 200 with error status
        data = response.json()
        assert data["status"] == "error"
        assert "error_code" in data
        assert "No products provided" in data.get("message", "") or "products" in data.get("message", "").lower()
    
    def test_generate_creatives_invalid_ab_config(self, creative_client):
        """Test error when ab_config has invalid values."""
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": [p.model_dump() for p in SAMPLE_PRODUCTS_ELECTRONICS[:1]],
            "ab_config": {
                "variants_per_product": 10,  # Exceeds max (5)
                "max_creatives": 100,  # Exceeds max (50)
                "enable_image_generation": True
            }
        }
        
        response = creative_client.post("/generate_creatives", json=request)
        
        # Should return 422 validation error
        assert response.status_code == 422
    
    def test_generate_creatives_all_products_fail(self, creative_client):
        """Test error when all products fail to generate creatives."""
        # Mock all LLM calls to fail - fallback should still work
        with patch('app.services.creative_service.creative_utils.call_gemini_text', return_value=None), \
             patch('app.services.creative_service.creative_utils.call_gemini_image', return_value=None):
            
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
            
            # Service should use fallback and still return creatives
            assert response.status_code == 200
            data = response.json()
            # Fallback should generate creatives even when LLM fails
            assert data.get("status") == "success"
            assert len(data.get("creatives", [])) >= 2  # Fallback should generate at least 2 variants

