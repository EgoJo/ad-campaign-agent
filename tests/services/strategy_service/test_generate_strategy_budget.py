"""
Tests for budget allocation logic in strategy generation.

Tests verify that budget is correctly allocated across:
- Product groups (high, medium, low priority)
- Individual creatives
"""

import pytest
from fastapi.testclient import TestClient
from app.services.strategy_service.main import app
from app.common.schemas import CampaignSpec, ProductGroup, Creative, Product


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)


def test_budget_allocation_correctness(
    client, product_group_high, product_group_medium, creatives_multiple_products
):
    """
    Test budget allocation correctness with multiple groups and creatives.
    
    Verifies:
    - High priority group gets more budget than medium
    - Creative-level allocation is not zero
    - Sum of allocated budget equals total budget (within epsilon)
    """
    campaign_spec = CampaignSpec(
        user_query="Test budget allocation",
        platform="meta",
        budget=3000.0,
        objective="conversions",
        category="electronics",
        metadata={}
    )
    
    request_payload = {
        "campaign_spec": campaign_spec.model_dump(),
        "product_groups": [
            product_group_high.model_dump(),
            product_group_medium.model_dump()
        ],
        "creatives": [c.model_dump() for c in creatives_multiple_products]
    }
    
    response = client.post("/generate_strategy", json=request_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    
    # Extract budget plan from debug
    debug = data["debug"]
    assert "budget_plan" in debug, "budget_plan missing from debug"
    budget_plan = debug["budget_plan"]
    
    # Verify group-level allocation
    assert "group_allocation" in budget_plan, "group_allocation missing"
    group_allocation = budget_plan["group_allocation"]
    
    assert "high" in group_allocation, "High priority group allocation missing"
    assert "medium" in group_allocation, "Medium priority group allocation missing"
    
    high_budget = group_allocation["high"]
    medium_budget = group_allocation["medium"]
    
    # High group should get more budget than medium
    assert high_budget > medium_budget, \
        f"High priority group ({high_budget}) should get more budget than medium ({medium_budget})"
    
    # Verify creative-level allocation
    assert "creative_allocation" in budget_plan, "creative_allocation missing"
    creative_allocation = budget_plan["creative_allocation"]
    
    # All creatives should have non-zero allocation
    assert len(creative_allocation) > 0, "No creatives have budget allocation"
    for creative_id, budget in creative_allocation.items():
        assert budget > 0, f"Creative {creative_id} has zero or negative budget: {budget}"
    
    # Verify sum of allocated budget equals total budget (within epsilon)
    total_allocated = sum(creative_allocation.values())
    total_budget = budget_plan["total_budget"]
    
    # Allow small floating point differences (epsilon = 0.01)
    epsilon = 0.01
    assert abs(total_allocated - total_budget) <= epsilon, \
        f"Sum of creative allocations ({total_allocated}) should equal total budget ({total_budget}) within {epsilon}"


def test_budget_allocation_high_medium_low(client, product_group_high, product_group_medium, product_group_low, creatives_ab):
    """Test budget allocation across all three priority levels."""
    campaign_spec = CampaignSpec(
        user_query="Test three-tier budget allocation",
        platform="meta",
        budget=5000.0,
        objective="conversions",
        category="electronics",
        metadata={}
    )
    
    request_payload = {
        "campaign_spec": campaign_spec.model_dump(),
        "product_groups": [
            product_group_high.model_dump(),
            product_group_medium.model_dump(),
            product_group_low.model_dump()
        ],
        "creatives": [c.model_dump() for c in creatives_ab]
    }
    
    response = client.post("/generate_strategy", json=request_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    
    budget_plan = data["debug"]["budget_plan"]
    group_allocation = budget_plan["group_allocation"]
    
    # Verify all three groups are present
    assert "high" in group_allocation
    assert "medium" in group_allocation
    assert "low" in group_allocation
    
    # Verify allocation order: high > medium > low
    assert group_allocation["high"] > group_allocation["medium"], \
        "High should get more than medium"
    assert group_allocation["medium"] > group_allocation["low"], \
        "Medium should get more than low"
    
    # Verify total allocation matches budget
    total_allocated = sum(group_allocation.values())
    total_budget = budget_plan["total_budget"]
    epsilon = 0.01
    assert abs(total_allocated - total_budget) <= epsilon, \
        f"Group allocation sum ({total_allocated}) should equal total budget ({total_budget})"


def test_budget_allocation_variant_split(client, campaign_spec_valid, product_group_high, creatives_ab):
    """Test that budget is split correctly between variants (A and B)."""
    request_payload = {
        "campaign_spec": campaign_spec_valid.model_dump(),
        "product_groups": [product_group_high.model_dump()],
        "creatives": [c.model_dump() for c in creatives_ab]
    }
    
    response = client.post("/generate_strategy", json=request_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    
    # Verify variant split in abstract strategy
    abstract_strategy = data["abstract_strategy"]
    budget_split = abstract_strategy["budget_split"]
    
    # Should have both A and B variants
    assert "A" in budget_split, "Variant A missing from budget_split"
    assert "B" in budget_split, "Variant B missing from budget_split"
    
    # Variants should sum to approximately 1.0
    total_split = sum(budget_split.values())
    epsilon = 0.01
    assert abs(total_split - 1.0) <= epsilon, \
        f"Budget split should sum to 1.0, got {total_split}"
    
    # Variant A typically gets more budget than B
    assert budget_split["A"] > 0, "Variant A should have positive budget"
    assert budget_split["B"] > 0, "Variant B should have positive budget"


def test_budget_allocation_single_creative(client, campaign_spec_valid, product_group_high):
    """Test budget allocation with a single creative."""
    single_creative = Creative(
        creative_id="CREATIVE-001-A",
        product_id="PROD-001",
        platform="meta",
        variant_id="A",
        primary_text="Test creative",
        headline="Test Headline",
        image_url="https://example.com/image.jpg"
    )
    
    request_payload = {
        "campaign_spec": campaign_spec_valid.model_dump(),
        "product_groups": [product_group_high.model_dump()],
        "creatives": [single_creative.model_dump()]
    }
    
    response = client.post("/generate_strategy", json=request_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    
    # Verify single creative gets all allocated budget
    budget_plan = data["debug"]["budget_plan"]
    creative_allocation = budget_plan["creative_allocation"]
    
    assert len(creative_allocation) == 1, "Should have exactly one creative allocation"
    assert "CREATIVE-001-A" in creative_allocation, "Creative ID should be in allocation"
    
    # Single creative should get the full group budget
    group_allocation = budget_plan["group_allocation"]
    high_budget = group_allocation.get("high", 0)
    creative_budget = creative_allocation["CREATIVE-001-A"]
    
    epsilon = 0.01
    assert abs(creative_budget - high_budget) <= epsilon, \
        f"Single creative budget ({creative_budget}) should equal group budget ({high_budget})"

