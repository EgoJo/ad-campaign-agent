"""
Pydantic schemas for the schema validator service.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ValidationError(BaseModel):
    """Individual validation error."""
    field: str = Field(..., description="Field that failed validation")
    error: str = Field(..., description="Error message")
    value: Optional[Any] = Field(None, description="Invalid value")


class ValidateRequest(BaseModel):
    """Request to validate data against a schema."""
    schema_name: str = Field(..., description="Name of the schema to validate against")
    data: Dict[str, Any] = Field(..., description="Data to validate")


class ValidateResponse(BaseModel):
    """Response after validation."""
    valid: bool = Field(..., description="Whether the data is valid")
    errors: List[ValidationError] = Field(default=[], description="List of validation errors")
