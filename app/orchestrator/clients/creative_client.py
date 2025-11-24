"""
Client for interacting with the Creative Service.
"""

from typing import Dict, Any, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.http_client import MCPClient
from common.config import settings


class CreativeClient:
    """Client for the Creative Service MCP."""
    
    def __init__(self):
        """Initialize the creative service client."""
        self.client = MCPClient(settings.CREATIVE_SERVICE_URL)
    
    def generate_creatives(
        self,
        product_ids: List[str],
        campaign_objective: str,
        target_audience: str,
        brand_voice: str = "professional",
        creative_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate creative content for ad campaigns.
        
        Args:
            product_ids: List of product IDs to create ads for
            campaign_objective: Campaign objective
            target_audience: Target audience description
            brand_voice: Brand voice/tone
            creative_types: Types of creatives to generate
            
        Returns:
            Generated creative assets
        """
        request_data = {
            "product_ids": product_ids,
            "campaign_objective": campaign_objective,
            "target_audience": target_audience,
            "brand_voice": brand_voice
        }
        
        if creative_types:
            request_data["creative_types"] = creative_types
        
        return self.client.post("/generate_creatives", request_data)
    
    def close(self):
        """Close the client connection."""
        self.client.close()


if __name__ == "__main__":
    # Example usage
    client = CreativeClient()
    try:
        result = client.generate_creatives(
            product_ids=["PROD-001", "PROD-002"],
            campaign_objective="increase sales",
            target_audience="tech enthusiasts"
        )
        print("Generated creatives:", result)
    finally:
        client.close()
