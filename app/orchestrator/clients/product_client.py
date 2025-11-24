"""
Client for interacting with the Product Service.
"""

from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.http_client import MCPClient
from common.config import settings


class ProductClient:
    """Client for the Product Service MCP."""
    
    def __init__(self):
        """Initialize the product service client."""
        self.client = MCPClient(settings.PRODUCT_SERVICE_URL)
    
    def select_products(
        self,
        campaign_objective: str,
        target_audience: str,
        budget: float,
        max_products: int = 10
    ) -> Dict[str, Any]:
        """
        Select products for an ad campaign.
        
        Args:
            campaign_objective: Campaign objective (e.g., 'increase sales')
            target_audience: Target audience description
            budget: Campaign budget
            max_products: Maximum number of products to select
            
        Returns:
            Selected products grouped by priority level
        """
        request_data = {
            "campaign_objective": campaign_objective,
            "target_audience": target_audience,
            "budget": budget,
            "max_products": max_products
        }
        
        return self.client.post("/select_products", request_data)
    
    def close(self):
        """Close the client connection."""
        self.client.close()


if __name__ == "__main__":
    # Example usage
    client = ProductClient()
    try:
        result = client.select_products(
            campaign_objective="increase sales",
            target_audience="tech enthusiasts",
            budget=10000.0
        )
        print("Selected products:", result)
    finally:
        client.close()
