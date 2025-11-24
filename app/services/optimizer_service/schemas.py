"""
Pydantic schemas for the optimizer service.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class OptimizationSuggestion(BaseModel):
    """Individual optimization suggestion."""
    category: str = Field(..., description="Category of optimization (e.g., 'budget', 'targeting', 'creative')")
    suggestion: str = Field(..., description="Optimization suggestion")
    expected_impact: str = Field(..., description="Expected impact description")
    priority: str = Field(..., description="Priority level (high, medium, low)")


class SummarizeRecentRunsRequest(BaseModel):
    """Request to summarize recent campaign runs."""
    campaign_ids: Optional[List[str]] = Field(default=None, description="Specific campaign IDs to analyze")
    days: int = Field(default=7, description="Number of days to look back")


class SummarizeRecentRunsResponse(BaseModel):
    """Response with campaign performance summary and optimization suggestions."""
    summary: str = Field(..., description="High-level performance summary")
    total_campaigns: int = Field(..., description="Total campaigns analyzed")
    total_spend: float = Field(..., description="Total spend across campaigns")
    total_conversions: int = Field(..., description="Total conversions")
    average_cpa: float = Field(..., description="Average cost per acquisition")
    suggestions: List[OptimizationSuggestion] = Field(..., description="Optimization suggestions")
