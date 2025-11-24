"""
Strategy Service - MCP microservice for generating campaign strategies.

This service is responsible for creating optimal campaign strategies including
budget allocation, platform selection, and bidding strategies.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from .schemas import GenerateStrategyRequest, GenerateStrategyResponse
from .mock_data import get_mock_strategy_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Strategy Service",
    description="MCP microservice for generating campaign strategies",
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
    return {"status": "healthy", "service": "strategy_service"}


@app.post("/generate_strategy", response_model=GenerateStrategyResponse)
async def generate_strategy(request: GenerateStrategyRequest):
    """
    Generate optimal campaign strategy based on objectives and constraints.
    
    Args:
        request: Strategy generation request with campaign parameters
        
    Returns:
        Campaign strategy with platform-specific recommendations
        
    TODO: Implement real strategy generation logic:
    - Use ML models to optimize budget allocation
    - Analyze historical campaign performance data
    - Consider seasonality and market trends
    - Optimize bidding strategies based on objectives
    - Provide realistic reach and conversion estimates
    """
    logger.info(f"Generating strategy: objective={request.campaign_objective}, "
                f"budget=${request.total_budget}, platforms={request.platforms}")
    
    # Return mock data for now
    response = get_mock_strategy_response(request.total_budget, request.platforms)
    
    logger.info(f"Generated strategy with {len(response.platform_strategies)} platform strategies")
    
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
