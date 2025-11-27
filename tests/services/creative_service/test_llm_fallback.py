"""
Tests for LLM fallback logic (OpenAI -> Gemini -> Template).

Tests:
- OpenAI primary, Gemini fallback
- Gemini primary when OpenAI unavailable
- Template fallback when both unavailable
- JSON Mode parsing
"""

import pytest
from unittest.mock import patch, MagicMock, Mock
from app.services.creative_service import creative_utils


class TestLLMFallback:
    """Test LLM fallback logic."""
    
    def test_openai_primary_success(self):
        """Test OpenAI is used first when available."""
        with patch.object(creative_utils, 'openai_client', MagicMock()), \
             patch.object(creative_utils, '_call_openai_api_internal') as mock_call:
            
            mock_call.return_value = '{"headline": "Test", "primary_text": "Content"}'
            
            result = creative_utils.call_gemini_text("test prompt")
            
            assert result is not None
            assert "headline" in result
            mock_call.assert_called_once()
    
    def test_openai_failure_fallback_to_gemini(self):
        """Test fallback to Gemini when OpenAI fails."""
        with patch.object(creative_utils, 'openai_client', MagicMock()), \
             patch.object(creative_utils, '_call_openai_api_internal', side_effect=Exception("OpenAI error")), \
             patch.object(creative_utils, 'gemini_model', MagicMock()), \
             patch.object(creative_utils, '_call_gemini_api_internal') as mock_gemini:
            
            mock_gemini.return_value = '{"headline": "Gemini", "primary_text": "Content"}'
            
            result = creative_utils.call_gemini_text("test prompt")
            
            assert result is not None
            assert "headline" in result
            mock_gemini.assert_called_once()
    
    def test_both_fail_fallback_to_template(self):
        """Test template fallback when both OpenAI and Gemini fail."""
        with patch.object(creative_utils, 'openai_client', None), \
             patch.object(creative_utils, 'gemini_model', None):
            
            result = creative_utils.call_gemini_text("test prompt")
            
            # Should return None, which triggers template fallback in calling code
            assert result is None
    
    def test_json_mode_openai(self):
        """Test JSON Mode with OpenAI."""
        schema = {
            "type": "object",
            "properties": {
                "headline": {"type": "string"},
                "primary_text": {"type": "string"}
            }
        }
        
        with patch.object(creative_utils, 'openai_client', MagicMock()), \
             patch.object(creative_utils, '_call_openai_api_internal') as mock_call:
            
            mock_call.return_value = '{"headline": "Test", "primary_text": "Content"}'
            
            result = creative_utils.call_gemini_text("test prompt", response_schema=schema)
            
            assert result is not None
            # Verify JSON Mode was requested
            mock_call.assert_called_once()
            call_args, call_kwargs = mock_call.call_args
            assert call_kwargs['json_mode'] is True
    
    def test_json_mode_gemini(self):
        """Test JSON Mode with Gemini fallback."""
        schema = {
            "type": "object",
            "properties": {
                "headline": {"type": "string"},
                "primary_text": {"type": "string"}
            }
        }
        
        with patch.object(creative_utils, 'openai_client', None), \
             patch.object(creative_utils, 'gemini_model', MagicMock()), \
             patch.object(creative_utils, '_call_gemini_api_internal') as mock_gemini:
            
            mock_gemini.return_value = '{"headline": "Gemini", "primary_text": "Content"}'
            
            result = creative_utils.call_gemini_text("test prompt", response_schema=schema)
            
            assert result is not None
            # Verify JSON Mode was requested
            mock_gemini.assert_called_once()
            call_args, call_kwargs = mock_gemini.call_args
            assert call_kwargs['response_schema'] == schema
    
    def test_openai_retry_exhausted_fallback(self):
        """Test fallback when OpenAI retries are exhausted."""
        from tenacity import RetryError
        
        # Create a proper RetryError mock
        mock_last_attempt = MagicMock()
        mock_last_attempt.exception.return_value = Exception("Retries exhausted")
        mock_retry_error = RetryError("Retries exhausted")
        mock_retry_error.last_attempt = mock_last_attempt
        
        with patch.object(creative_utils, 'openai_client', MagicMock()), \
             patch.object(creative_utils, '_call_openai_api_internal', side_effect=mock_retry_error), \
             patch.object(creative_utils, 'gemini_model', MagicMock()), \
             patch.object(creative_utils, '_call_gemini_api_internal') as mock_gemini:
            
            mock_gemini.return_value = '{"headline": "Gemini", "primary_text": "Content"}'
            
            result = creative_utils.call_gemini_text("test prompt")
            
            assert result is not None
            mock_gemini.assert_called_once()
    
    def test_image_generation_openai_primary(self):
        """Test image generation uses OpenAI DALL-E first."""
        with patch.object(creative_utils, 'openai_image_client') as mock_client:
            mock_response = MagicMock()
            mock_response.data = [MagicMock(url="https://example.com/image.jpg")]
            mock_client.images.generate.return_value = mock_response
            
            result = creative_utils.call_openai_image("test image prompt")
            
            assert result == "https://example.com/image.jpg"
            mock_client.images.generate.assert_called_once()
    
    def test_image_generation_openai_failure_fallback_to_gemini(self):
        """Test image generation falls back to Gemini when DALL-E fails."""
        with patch.object(creative_utils, 'openai_image_client', None), \
             patch.object(creative_utils, 'call_gemini_image') as mock_gemini:
            
            mock_gemini.return_value = "https://example.com/gemini-image.jpg"
            
            # This is tested at the endpoint level, not in utils
            # But we can test the fallback logic
            result = creative_utils.call_openai_image("test prompt")
            
            assert result is None  # openai_image_client is None
            # Fallback to Gemini happens in main.py, not here

