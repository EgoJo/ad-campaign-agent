"""
Client for interacting with the Schema Validator Service.
"""

from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.http_client import MCPClient
from common.config import settings


class ValidatorClient:
    """Client for the Schema Validator Service MCP."""
    
    def __init__(self):
        """Initialize the validator service client."""
        self.client = MCPClient(settings.SCHEMA_VALIDATOR_SERVICE_URL)
    
    def validate(
        self,
        schema_name: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate data against a schema.
        
        Args:
            schema_name: Name of the schema to validate against
            data: Data to validate
            
        Returns:
            Validation result with any errors
        """
        request_data = {
            "schema_name": schema_name,
            "data": data
        }
        
        return self.client.post("/validate", request_data)
    
    def close(self):
        """Close the client connection."""
        self.client.close()


if __name__ == "__main__":
    # Example usage
    client = ValidatorClient()
    try:
        result = client.validate(
            schema_name="campaign",
            data={"name": "Test Campaign", "budget": 1000}
        )
        print("Validation result:", result)
    finally:
        client.close()
