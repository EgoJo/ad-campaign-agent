"""
Meta Service - MCP microservice for Meta (Facebook/Instagram) platform integration.

This service handles campaign creation and management on Meta platforms.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from .schemas import CreateCampaignRequest, CreateCampaignResponse
from .mock_data import get_mock_campaign_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Meta Service",
    description="MCP microservice for Meta platform integration",
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
    return {"status": "healthy", "service": "meta_service"}


@app.post("/create_campaign", response_model=CreateCampaignResponse)
async def create_campaign(request: CreateCampaignRequest):
    """
    Create a campaign on Meta platforms (Facebook/Instagram).
    
    Args:
        request: Campaign creation request with targeting and creatives
        
    Returns:
        Created campaign, ad set, and ad IDs
        
    TODO: Implement real Meta API integration:
    - Authenticate with Facebook Marketing API
    - Create campaign with proper objectives
    - Create ad sets with targeting
    - Upload creatives and create ads
    - Handle API rate limits and errors
    - Implement campaign status monitoring
    """
    logger.info(f"Creating Meta campaign: {request.campaign_name}, "
                f"budget=${request.daily_budget}, creatives={len(request.creatives)}")
    
    # Return mock data for now
    response = get_mock_campaign_response(request.creatives)
    
    logger.info(f"Created campaign {response.campaign_id} with {len(response.ad_ids)} ads")
    
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
