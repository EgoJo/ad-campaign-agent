"""
Client for interacting with the Strategy Service.
"""

from typing import Dict, Any, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.http_client import MCPClient
from common.config import settings


class StrategyClient:
    """Client for the Strategy Service MCP."""
    
    def __init__(self):
        """Initialize the strategy service client."""
        self.client = MCPClient(settings.STRATEGY_SERVICE_URL)
    
    def generate_strategy(
        self,
        campaign_objective: str,
        total_budget: float,
        duration_days: int,
        target_audience: str,
        platforms: List[str]
    ) -> Dict[str, Any]:
        """
        Generate campaign strategy.
        
        Args:
            campaign_objective: Campaign objective
            total_budget: Total campaign budget
            duration_days: Campaign duration in days
            target_audience: Target audience description
            platforms: Platforms to advertise on
            
        Returns:
            Campaign strategy with platform-specific recommendations
        """
        request_data = {
            "campaign_objective": campaign_objective,
            "total_budget": total_budget,
            "duration_days": duration_days,
            "target_audience": target_audience,
            "platforms": platforms
        }
        
        return self.client.post("/generate_strategy", request_data)
    
    def close(self):
        """Close the client connection."""
        self.client.close()


if __name__ == "__main__":
    # Example usage
    client = StrategyClient()
    try:
        result = client.generate_strategy(
            campaign_objective="increase sales",
            total_budget=10000.0,
            duration_days=30,
            target_audience="tech enthusiasts",
            platforms=["facebook", "instagram"]
        )
        print("Generated strategy:", result)
    finally:
        client.close()
