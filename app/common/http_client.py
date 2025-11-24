"""
Common HTTP client utilities for making requests to MCP services.
"""

import httpx
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class MCPClient:
    """Base HTTP client for communicating with MCP microservices."""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize the MCP client.
        
        Args:
            base_url: Base URL of the MCP service
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a POST request to the MCP service.
        
        Args:
            endpoint: API endpoint path
            data: Request payload
            
        Returns:
            Response data as dictionary
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        
        try:
            response = self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling {url}: {e}")
            raise
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the MCP service.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        
        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling {url}: {e}")
            raise
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
