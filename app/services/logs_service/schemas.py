"""
Pydantic schemas for the logs service.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """Types of events to log."""
    CAMPAIGN_CREATED = "campaign_created"
    CAMPAIGN_UPDATED = "campaign_updated"
    AD_CREATED = "ad_created"
    PRODUCT_SELECTED = "product_selected"
    CREATIVE_GENERATED = "creative_generated"
    STRATEGY_GENERATED = "strategy_generated"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class AppendEventRequest(BaseModel):
    """Request to append an event to logs."""
    event_type: EventType = Field(..., description="Type of event")
    message: str = Field(..., description="Event message")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional event metadata")
    campaign_id: Optional[str] = Field(None, description="Associated campaign ID")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Event timestamp")


class AppendEventResponse(BaseModel):
    """Response after appending an event."""
    status: str = Field(..., description="Operation status")
    event_id: str = Field(..., description="Unique event ID")
