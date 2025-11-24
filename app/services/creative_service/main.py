"""
Creative Service - MCP microservice for generating ad creatives.

This service is responsible for generating creative content (text, images, videos)
for ad campaigns using AI models.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from .schemas import GenerateCreativesRequest, GenerateCreativesResponse
from .mock_data import get_mock_creatives_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Creative Service",
    description="MCP microservice for generating ad creatives",
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
    return {"status": "healthy", "service": "creative_service"}


@app.post("/generate_creatives", response_model=GenerateCreativesResponse)
async def generate_creatives(request: GenerateCreativesRequest):
    """
    Generate creative content for ad campaigns.
    
    Args:
        request: Creative generation request with product and campaign details
        
    Returns:
        Generated creative assets (headlines, body text, images, etc.)
        
    TODO: Implement real creative generation logic:
    - Integrate with Gemini API for copywriting
    - Use DALL-E or similar for image generation
    - Apply brand voice and style guidelines
    - Generate multiple variants for A/B testing
    - Ensure compliance with platform-specific requirements
    """
    logger.info(f"Generating creatives for {len(request.product_ids)} products, "
                f"objective={request.campaign_objective}, types={request.creative_types}")
    
    # Return mock data for now
    response = get_mock_creatives_response(request.product_ids)
    
    logger.info(f"Generated {response.total_creatives} creatives")
    
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
