"""
Pydantic schemas for the Meta (Facebook/Instagram) service.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class AdCreative(BaseModel):
    """Ad creative for Meta platform."""
    creative_id: str = Field(..., description="Creative ID from creative service")
    headline: str = Field(..., description="Ad headline")
    body_text: str = Field(..., description="Ad body text")
    call_to_action: str = Field(..., description="Call to action")
    image_url: Optional[str] = Field(None, description="Image URL")


class CreateCampaignRequest(BaseModel):
    """Request to create a campaign on Meta platforms."""
    campaign_name: str = Field(..., description="Campaign name")
    objective: str = Field(..., description="Campaign objective")
    daily_budget: float = Field(..., description="Daily budget")
    targeting: Dict[str, Any] = Field(..., description="Targeting criteria")
    creatives: List[AdCreative] = Field(..., description="Ad creatives to use")
    start_date: str = Field(..., description="Campaign start date (ISO format)")
    end_date: Optional[str] = Field(None, description="Campaign end date (ISO format)")


class AdResult(BaseModel):
    """Result of creating an ad."""
    ad_id: str = Field(..., description="Created ad ID")
    creative_id: str = Field(..., description="Associated creative ID")
    status: str = Field(..., description="Ad status")


class CreateCampaignResponse(BaseModel):
    """Response after creating a campaign."""
    campaign_id: str = Field(..., description="Created campaign ID")
    ad_set_id: str = Field(..., description="Created ad set ID")
    ad_ids: List[AdResult] = Field(..., description="Created ad IDs")
    status: str = Field(..., description="Campaign status")
