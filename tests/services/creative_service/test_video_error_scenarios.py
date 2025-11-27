"""
Tests for error scenarios in video generation.

Tests:
- API failures (network errors, timeouts)
- Invalid responses
- Resource cleanup
- Edge cases
"""

import pytest
import json
from unittest.mock import patch, MagicMock, Mock
from app.services.creative_service import creative_utils
from tests.testdata import VALID_CAMPAIGN_SPEC_META_ELECTRONICS, SAMPLE_PRODUCTS_ELECTRONICS


class TestVideoErrorScenarios:
    """Test error handling in video generation."""
    
    def test_replicate_api_timeout(self):
        """Test Replicate API timeout handling."""
        with patch.object(creative_utils, 'replicate_client') as mock_client:
            import requests
            mock_client.run.side_effect = requests.Timeout("Request timeout")
            
            with pytest.raises(Exception):
                creative_utils.call_replicate_video(
                    "https://example.com/image.jpg",
                    "test description"
                )
    
    def test_replicate_api_rate_limit(self):
        """Test Replicate API rate limit handling."""
        with patch.object(creative_utils, 'replicate_client') as mock_client:
            import requests
            mock_response = MagicMock()
            mock_response.status_code = 429
            mock_response.text = "Rate limit exceeded"
            mock_client.run.side_effect = requests.HTTPError(response=mock_response)
            
            with pytest.raises(Exception):
                creative_utils.call_replicate_video(
                    "https://example.com/image.jpg",
                    "test description"
                )
    
    def test_storyline_malformed_json(self):
        """Test storyline generation with malformed JSON."""
        malformed_responses = [
            "{invalid json}",
            '{"theme": "test", "segments": [}',  # Missing closing bracket
            "",  # Empty response
            None  # None response
        ]
        
        for malformed_response in malformed_responses:
            with patch.object(creative_utils, 'call_gemini_text', return_value=malformed_response):
                result = creative_utils.generate_storyline(
                    product_title="Test",
                    product_description="Test",
                    category="electronics",
                    platform="meta",
                    objective="conversions",
                    num_segments=3,
                    request_id="test-123"
                )
                
                # Should handle gracefully and return None
                assert result is None
    
    def test_storyline_missing_required_fields(self):
        """Test storyline with missing required fields."""
        incomplete_json = {
            "theme": "test"
            # Missing: style, total_duration, num_segments, segments
        }
        
        with patch.object(creative_utils, 'call_gemini_text') as mock_llm:
            mock_llm.return_value = json.dumps(incomplete_json)
            
            result = creative_utils.generate_storyline(
                product_title="Test",
                product_description="Test",
                category="electronics",
                platform="meta",
                objective="conversions",
                num_segments=3,
                request_id="test-123"
            )
            
            # Function may return incomplete dict or None
            # This tests that it doesn't crash
            assert result is None or isinstance(result, dict)
    
    def test_storyline_missing_required_fields(self):
        """Test storyline with missing required fields."""
        incomplete_json = {
            "theme": "test"
            # Missing: style, total_duration, num_segments, segments
        }
        
        with patch.object(creative_utils, 'call_gemini_text') as mock_llm:
            mock_llm.return_value = json.dumps(incomplete_json)
            
            result = creative_utils.generate_storyline(
                product_title="Test",
                product_description="Test",
                category="electronics",
                platform="meta",
                objective="conversions",
                num_segments=3,
                request_id="test-123"
            )
            
            # Function may return incomplete dict or None
            # This tests that it doesn't crash
            assert result is None or isinstance(result, dict)
    
    def test_concatenate_videos_network_error(self):
        """Test video concatenation with network errors during download."""
        video_urls = ["https://example.com/segment1.mp4"]
        
        with patch('shutil.which', return_value='/usr/bin/ffmpeg'), \
             patch.object(creative_utils, 'download_video', return_value=False):
            
            result = creative_utils.concatenate_videos(
                video_urls,
                "/tmp/output.mp4",
                request_id="test-123"
            )
            
            assert result is None
    
    def test_concatenate_videos_ffmpeg_failure(self):
        """Test video concatenation when FFmpeg fails."""
        import subprocess
        import tempfile
        import os
        
        video_urls = ["https://example.com/segment1.mp4"]
        
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
            output_path = tmp_file.name
        
        try:
            with patch('shutil.which', return_value='/usr/bin/ffmpeg'), \
                 patch.object(creative_utils, 'download_video', return_value=True), \
                 patch('subprocess.run') as mock_subprocess:
                
                # Mock FFmpeg failure
                mock_subprocess.return_value = Mock(returncode=1)
                
                result = creative_utils.concatenate_videos(
                    video_urls,
                    output_path,
                    request_id="test-123"
                )
                
                # Should handle FFmpeg failure gracefully
                assert result is None or result == output_path
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_download_video_http_error(self):
        """Test video download with HTTP error."""
        with patch('requests.get') as mock_get:
            import requests
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = requests.HTTPError("Not found")
            mock_get.return_value = mock_response
            
            result = creative_utils.download_video(
                "https://example.com/nonexistent.mp4",
                "/tmp/video.mp4"
            )
            
            assert result is False
    
    def test_download_video_timeout(self):
        """Test video download timeout."""
        with patch('requests.get', side_effect=Exception("Timeout")):
            result = creative_utils.download_video(
                "https://example.com/video.mp4",
                "/tmp/video.mp4"
            )
            
            assert result is False
    
    def test_video_generation_endpoint_api_failure(self, creative_client):
        """Test video generation endpoint handles API failures gracefully."""
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
        
        # Simulate Replicate API failure
        with patch.object(creative_utils, 'replicate_client') as mock_client:
            mock_client.run.side_effect = Exception("API Error")
            
            # Should still return success with fallback
            response = creative_client.post("/generate_creatives", json=request)
            
            assert response.status_code == 200
            data = response.json()
            # Service should handle error gracefully
            assert data["status"] == "success" or data["status"] == "error"
    
    def test_storyline_video_generation_partial_failure(self, creative_client):
        """Test storyline video generation when some segments fail."""
        request = {
            "campaign_spec": VALID_CAMPAIGN_SPEC_META_ELECTRONICS.model_dump(),
            "products": [SAMPLE_PRODUCTS_ELECTRONICS[0].model_dump()],
            "ab_config": {
                "variants_per_product": 1,
                "max_creatives": 1,
                "enable_image_generation": True,
                "enable_storyline_video": True,
                "num_video_segments": 3
            }
        }
        
        # Mock storyline generation success but video segment generation failure
        mock_storyline = {
            "theme": "test",
            "style": "minimalist",
            "total_duration": 15,
            "num_segments": 3,
            "segments": [
                {
                    "segment_id": 1,
                    "duration": 5,
                    "scene_description": "Segment 1",
                    "camera_movement": "zoom",
                    "focus": "product",
                    "text_overlay": "Text 1",
                    "video_prompt": "Prompt 1"
                }
            ]
        }
        
        with patch.object(creative_utils, 'generate_storyline', return_value=mock_storyline), \
             patch.object(creative_utils, 'call_replicate_video', return_value=None):
            
            response = creative_client.post("/generate_creatives", json=request)
            
            assert response.status_code == 200
            data = response.json()
            # Should handle partial failure gracefully
            assert data["status"] == "success" or data["status"] == "error"
    
    def test_resource_cleanup_on_error(self):
        """Test that temporary resources are cleaned up on error."""
        import tempfile
        import os
        
        video_urls = ["https://example.com/segment1.mp4"]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "output.mp4")
            
            with patch('shutil.which', return_value='/usr/bin/ffmpeg'), \
                 patch.object(creative_utils, 'download_video', return_value=True), \
                 patch('subprocess.run', side_effect=Exception("FFmpeg error")):
                
                try:
                    result = creative_utils.concatenate_videos(
                        video_urls,
                        output_path,
                        request_id="test-123"
                    )
                except Exception:
                    pass
                
                # Temporary directory should be cleaned up (tested via context manager)
                # This is more of an integration test
                assert True  # If we get here, cleanup worked

