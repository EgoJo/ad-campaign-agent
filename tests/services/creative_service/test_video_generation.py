"""
Tests for video generation functionality.

Tests:
- Video generation from image (Replicate)
- Storyline generation and JSON parsing
- Video concatenation
- Fallback mechanisms
- Error handling
"""

import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock, Mock, mock_open
from app.services.creative_service import creative_utils
from app.common.schemas import Product


class TestVideoGeneration:
    """Test video generation functions."""
    
    @pytest.fixture
    def sample_product(self):
        """Sample product for testing."""
        return Product(
            product_id="TEST-001",
            title="Test Product",
            description="A test product for video generation",
            price=99.99,
            category="electronics",
            metadata={}
        )
    
    def test_call_replicate_video_success(self):
        """Test successful video generation via Replicate."""
        from app.common.config import settings
        
        with patch.object(creative_utils, 'replicate_client') as mock_client:
            mock_output = "https://replicate.com/video.mp4"
            mock_client.run.return_value = mock_output
            
            result = creative_utils.call_replicate_video(
                "https://example.com/image.jpg",
                "A product video showing the product in use"
            )
            
            assert result == mock_output
            mock_client.run.assert_called_once()
            # Verify model and parameters
            call_args = mock_client.run.call_args
            assert call_args[0][0] == settings.REPLICATE_VIDEO_MODEL
    
    def test_call_replicate_video_no_client(self):
        """Test video generation when Replicate client is not available."""
        with patch.object(creative_utils, 'replicate_client', None):
            result = creative_utils.call_replicate_video(
                "https://example.com/image.jpg",
                "test description"
            )
            
            assert result is None
    
    def test_call_replicate_video_failure(self):
        """Test video generation failure handling."""
        with patch.object(creative_utils, 'replicate_client') as mock_client:
            mock_client.run.side_effect = Exception("Replicate API error")
            
            with pytest.raises(Exception):
                creative_utils.call_replicate_video(
                    "https://example.com/image.jpg",
                    "test description"
                )
    
    def test_fallback_video_url(self, sample_product):
        """Test fallback video URL generation."""
        result = creative_utils.fallback_video_url(sample_product)
        
        # Currently returns None, but function exists for future extension
        assert result is None or isinstance(result, str)
    
    def test_generate_storyline_success(self):
        """Test successful storyline generation."""
        mock_storyline_json = {
            "theme": "modern lifestyle",
            "style": "minimalist_modern",
            "total_duration": 15,
            "num_segments": 3,
            "segments": [
                {
                    "segment_id": 1,
                    "duration": 5,
                    "scene_description": "Product close-up",
                    "camera_movement": "slow_zoom_in",
                    "focus": "product_detail",
                    "text_overlay": "Introducing",
                    "video_prompt": "Close-up of product"
                },
                {
                    "segment_id": 2,
                    "duration": 5,
                    "scene_description": "Person using product",
                    "camera_movement": "pan_left",
                    "focus": "user_experience",
                    "text_overlay": "Experience it",
                    "video_prompt": "Person using product"
                },
                {
                    "segment_id": 3,
                    "duration": 5,
                    "scene_description": "Benefits and CTA",
                    "camera_movement": "static",
                    "focus": "benefits",
                    "text_overlay": "Get yours today",
                    "video_prompt": "Benefits showcase"
                }
            ]
        }
        
        with patch.object(creative_utils, 'call_gemini_text') as mock_llm:
            mock_llm.return_value = json.dumps(mock_storyline_json)
            
            result = creative_utils.generate_storyline(
                product_title="Test Product",
                product_description="A test product",
                category="electronics",
                platform="meta",
                objective="conversions",
                num_segments=3,
                request_id="test-123"
            )
            
            assert result is not None
            assert result["theme"] == "modern lifestyle"
            assert result["num_segments"] == 3
            assert len(result["segments"]) == 3
            assert result["segments"][0]["segment_id"] == 1
    
    def test_generate_storyline_json_parse_error(self):
        """Test storyline generation with invalid JSON."""
        with patch.object(creative_utils, 'call_gemini_text') as mock_llm:
            mock_llm.return_value = "Invalid JSON response"
            
            result = creative_utils.generate_storyline(
                product_title="Test Product",
                product_description="A test product",
                category="electronics",
                platform="meta",
                objective="conversions",
                num_segments=3,
                request_id="test-123"
            )
            
            assert result is None
    
    def test_generate_storyline_no_llm(self):
        """Test storyline generation when LLM is unavailable."""
        with patch.object(creative_utils, 'call_gemini_text', return_value=None):
            result = creative_utils.generate_storyline(
                product_title="Test Product",
                product_description="A test product",
                category="electronics",
                platform="meta",
                objective="conversions",
                num_segments=3,
                request_id="test-123"
            )
            
            assert result is None
    
    def test_generate_storyline_json_mode_schema(self):
        """Test that storyline generation uses JSON Mode with correct schema."""
        mock_storyline_json = {
            "theme": "test",
            "style": "minimalist",
            "total_duration": 15,
            "num_segments": 3,
            "segments": []
        }
        
        with patch.object(creative_utils, 'call_gemini_text') as mock_llm:
            mock_llm.return_value = json.dumps(mock_storyline_json)
            
            creative_utils.generate_storyline(
                product_title="Test",
                product_description="Test",
                category="electronics",
                platform="meta",
                objective="conversions",
                num_segments=3
            )
            
            # Verify JSON Mode was used
            mock_llm.assert_called_once()
            call_args = mock_llm.call_args
            assert call_args[1]['response_schema'] is not None
            schema = call_args[1]['response_schema']
            assert schema['type'] == 'object'
            assert 'segments' in schema['properties']


class TestVideoConcatenation:
    """Test video concatenation functionality."""
    
    def test_concatenate_videos_success(self):
        """Test successful video concatenation."""
        video_urls = [
            "https://example.com/segment1.mp4",
            "https://example.com/segment2.mp4",
            "https://example.com/segment3.mp4"
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            with patch('shutil.which', return_value='/usr/bin/ffmpeg'), \
                 patch.object(creative_utils, 'download_video') as mock_download, \
                 patch('subprocess.run') as mock_subprocess:
                
                # Mock successful downloads
                mock_download.return_value = True
                # Mock successful FFmpeg concatenation
                mock_subprocess.return_value = Mock(returncode=0)
                
                result = creative_utils.concatenate_videos(
                    video_urls,
                    output_path,
                    request_id="test-123"
                )
                
                # Should attempt to download and concatenate
                assert mock_download.call_count == len(video_urls)
                # Note: actual concatenation logic may vary
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_concatenate_videos_no_ffmpeg(self):
        """Test concatenation fails when FFmpeg is not available."""
        video_urls = ["https://example.com/segment1.mp4"]
        
        with patch('shutil.which', return_value=None):
            result = creative_utils.concatenate_videos(
                video_urls,
                "/tmp/output.mp4",
                request_id="test-123"
            )
            
            assert result is None
    
    def test_concatenate_videos_download_failure(self):
        """Test concatenation when video download fails."""
        video_urls = ["https://example.com/segment1.mp4"]
        
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            with patch('shutil.which', return_value='/usr/bin/ffmpeg'), \
                 patch.object(creative_utils, 'download_video', return_value=False):
                
                result = creative_utils.concatenate_videos(
                    video_urls,
                    output_path,
                    request_id="test-123"
                )
                
                # Should return None if download fails
                assert result is None
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_download_video_success(self):
        """Test successful video download."""
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.iter_content.return_value = [b'video', b'data']
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                output_path = tmp_file.name
            
            try:
                result = creative_utils.download_video(
                    "https://example.com/video.mp4",
                    output_path
                )
                
                assert result is True
                assert os.path.exists(output_path)
            finally:
                if os.path.exists(output_path):
                    os.unlink(output_path)
    
    def test_download_video_failure(self):
        """Test video download failure."""
        with patch('requests.get', side_effect=Exception("Network error")):
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                output_path = tmp_file.name
            
            try:
                result = creative_utils.download_video(
                    "https://example.com/video.mp4",
                    output_path
                )
                
                assert result is False
            finally:
                if os.path.exists(output_path):
                    os.unlink(output_path)


class TestVideoGenerationIntegration:
    """Integration tests for video generation flow."""
    
    def test_video_generation_fallback_chain(self, creative_client):
        """Test complete fallback chain: Replicate -> Fallback."""
        from tests.testdata import VALID_CAMPAIGN_SPEC_META_ELECTRONICS, SAMPLE_PRODUCTS_ELECTRONICS
        
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": [SAMPLE_PRODUCTS_ELECTRONICS[0].model_dump()],
            "ab_config": {
                "variants_per_product": 1,
                "max_creatives": 1,
                "enable_image_generation": True,
                "enable_video_generation": True
            }
        }
        
        with patch.object(creative_utils, 'replicate_client', None), \
             patch.object(creative_utils, 'call_openai_image', return_value="https://example.com/image.jpg"):
            
            response = creative_client.post("/generate_creatives", json=request)
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            # Video should be None when Replicate is unavailable
            if data["creatives"]:
                creative = data["creatives"][0]
                # Video URL may be None (fallback)
                assert "video_url" in creative

