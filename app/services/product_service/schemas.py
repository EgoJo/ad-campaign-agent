"""
Pydantic schemas for the product service.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class PriorityLevel(str, Enum):
    """Product priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Product(BaseModel):
    """Individual product model."""
    product_id: str = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Product description")
    price: float = Field(..., description="Product price")
    category: str = Field(..., description="Product category")
    image_url: Optional[str] = Field(None, description="Product image URL")
    stock_quantity: int = Field(..., description="Available stock quantity")


class ProductGroup(BaseModel):
    """Group of products by priority level."""
    priority: PriorityLevel = Field(..., description="Priority level of this group")
    products: List[Product] = Field(..., description="List of products in this group")


class SelectProductsRequest(BaseModel):
    """Request to select products for ad campaign."""
    campaign_objective: str = Field(..., description="Campaign objective (e.g., 'increase sales', 'brand awareness')")
    target_audience: str = Field(..., description="Target audience description")
    budget: float = Field(..., description="Campaign budget")
    max_products: int = Field(default=10, description="Maximum number of products to select")


class SelectProductsResponse(BaseModel):
    """Response containing selected products grouped by priority."""
    product_groups: List[ProductGroup] = Field(..., description="Products grouped by priority level")
    total_products: int = Field(..., description="Total number of products selected")
