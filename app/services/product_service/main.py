"""
Product Service - MCP microservice for product selection.

This service is responsible for selecting products for ad campaigns
based on campaign objectives, target audience, and budget.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from .schemas import SelectProductsRequest, SelectProductsResponse
from .mock_data import get_mock_products_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Product Service",
    description="MCP microservice for product selection in ad campaigns",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "product_service"}


@app.post("/select_products", response_model=SelectProductsResponse)
async def select_products(request: SelectProductsRequest):
    """
    Select products for an ad campaign based on objectives and constraints.
    
    Args:
        request: Product selection request with campaign details
        
    Returns:
        Selected products grouped by priority level
        
    TODO: Implement real product selection logic:
    - Query product database based on campaign_objective and target_audience
    - Apply ML-based ranking algorithm
    - Filter by budget and stock availability
    - Return dynamically selected products instead of mock data
    """
    logger.info(f"Selecting products for campaign: objective={request.campaign_objective}, "
                f"audience={request.target_audience}, budget={request.budget}")
    
    # Return mock data for now
    response = get_mock_products_response()
    
    logger.info(f"Selected {response.total_products} products across "
                f"{len(response.product_groups)} priority groups")
    
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
