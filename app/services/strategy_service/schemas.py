"""
Pydantic schemas for the strategy service.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class Platform(str, Enum):
    """Advertising platforms."""
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    GOOGLE_ADS = "google_ads"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"


class BidStrategy(str, Enum):
    """Bidding strategies."""
    LOWEST_COST = "lowest_cost"
    COST_CAP = "cost_cap"
    BID_CAP = "bid_cap"
    TARGET_COST = "target_cost"


class PlatformStrategy(BaseModel):
    """Strategy for a specific platform."""
    platform: Platform = Field(..., description="Advertising platform")
    budget_allocation: float = Field(..., description="Budget allocated to this platform (percentage)")
    bid_strategy: BidStrategy = Field(..., description="Bidding strategy")
    target_cpa: Optional[float] = Field(None, description="Target cost per acquisition")
    daily_budget: float = Field(..., description="Daily budget for this platform")
    targeting_criteria: Dict[str, str] = Field(..., description="Platform-specific targeting criteria")


class GenerateStrategyRequest(BaseModel):
    """Request to generate campaign strategy."""
    campaign_objective: str = Field(..., description="Campaign objective")
    total_budget: float = Field(..., description="Total campaign budget")
    duration_days: int = Field(..., description="Campaign duration in days")
    target_audience: str = Field(..., description="Target audience description")
    platforms: List[Platform] = Field(..., description="Platforms to advertise on")


class GenerateStrategyResponse(BaseModel):
    """Response containing campaign strategy."""
    abstract_strategy: str = Field(..., description="High-level strategy description")
    platform_strategies: List[PlatformStrategy] = Field(..., description="Platform-specific strategies")
    estimated_reach: int = Field(..., description="Estimated total reach")
    estimated_conversions: int = Field(..., description="Estimated conversions")
