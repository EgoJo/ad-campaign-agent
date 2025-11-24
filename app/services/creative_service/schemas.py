"""
Pydantic schemas for the creative service.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class CreativeType(str, Enum):
    """Types of creative content."""
    IMAGE = "image"
    VIDEO = "video"
    TEXT = "text"
    CAROUSEL = "carousel"


class Creative(BaseModel):
    """Individual creative asset."""
    creative_id: str = Field(..., description="Unique creative identifier")
    creative_type: CreativeType = Field(..., description="Type of creative")
    headline: str = Field(..., description="Creative headline")
    body_text: str = Field(..., description="Creative body text")
    call_to_action: str = Field(..., description="Call to action text")
    asset_url: Optional[str] = Field(None, description="URL to the creative asset (image/video)")
    product_id: Optional[str] = Field(None, description="Associated product ID")


class GenerateCreativesRequest(BaseModel):
    """Request to generate creative content."""
    product_ids: List[str] = Field(..., description="List of product IDs to create ads for")
    campaign_objective: str = Field(..., description="Campaign objective")
    target_audience: str = Field(..., description="Target audience description")
    brand_voice: str = Field(default="professional", description="Brand voice/tone")
    creative_types: List[CreativeType] = Field(default=[CreativeType.IMAGE], description="Types of creatives to generate")


class GenerateCreativesResponse(BaseModel):
    """Response containing generated creatives."""
    creatives: List[Creative] = Field(..., description="List of generated creative assets")
    total_creatives: int = Field(..., description="Total number of creatives generated")
