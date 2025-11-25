"""
Basic tests for strategy generation endpoint.

Tests the fundamental functionality of the /generate_strategy endpoint
with valid inputs.
"""

import pytest
from fastapi.testclient import TestClient
from app.services.strategy_service.main import app
from app.common.schemas import CampaignSpec, ProductGroup, Creative, Product


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)


def test_basic_strategy_generation(client, campaign_spec_valid, product_group_high, creatives_ab):
    """
    Test basic strategy generation with valid inputs.
    
    Verifies:
    - Successful response (status 200)
    - Response structure matches expected format
    - Abstract strategy is present
    - Platform strategies are present
    - Debug information is included
    """
    request_payload = {
        "campaign_spec": campaign_spec_valid.model_dump(),
        "product_groups": [product_group_high.model_dump()],
        "creatives": [c.model_dump() for c in creatives_ab]
    }
    
    response = client.post("/generate_strategy", json=request_payload)
    
    # Assert HTTP status
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    
    # Assert response status
    assert data["status"] == "success", f"Expected 'success', got '{data.get('status')}'"
    
    # Assert abstract_strategy exists
    assert "abstract_strategy" in data, "abstract_strategy missing from response"
    assert data["abstract_strategy"] is not None, "abstract_strategy is None"
    
    abstract_strategy = data["abstract_strategy"]
    assert "objective" in abstract_strategy, "abstract_strategy missing 'objective' field"
    assert "budget_split" in abstract_strategy, "abstract_strategy missing 'budget_split' field"
    assert "bidding_strategy" in abstract_strategy, "abstract_strategy missing 'bidding_strategy' field"
    
    # Assert platform_strategies exists and is non-empty
    assert "platform_strategies" in data, "platform_strategies missing from response"
    assert isinstance(data["platform_strategies"], list), "platform_strategies should be a list"
    assert len(data["platform_strategies"]) > 0, "platform_strategies list is empty"
    
    platform_strategy = data["platform_strategies"][0]
    assert "platform" in platform_strategy, "platform_strategy missing 'platform' field"
    assert "campaign_structure" in platform_strategy, "platform_strategy missing 'campaign_structure' field"
    assert "optimization_goal" in platform_strategy, "platform_strategy missing 'optimization_goal' field"
    
    # Assert debug information exists
    assert "debug" in data, "debug information missing from response"
    debug = data["debug"]
    
    # Assert budget allocation fields
    assert "budget_plan" in debug, "debug missing 'budget_plan'"
    budget_plan = debug["budget_plan"]
    assert "total_budget" in budget_plan, "budget_plan missing 'total_budget'"
    assert "group_allocation" in budget_plan, "budget_plan missing 'group_allocation'"
    assert "creative_allocation" in budget_plan, "budget_plan missing 'creative_allocation'"
    
    # Assert targeting_plan exists
    assert "targeting_plan" in debug, "debug missing 'targeting_plan'"
    targeting_plan = debug["targeting_plan"]
    assert isinstance(targeting_plan, dict), "targeting_plan should be a dictionary"
    
    # Assert rules_applied exists
    assert "rules_applied" in debug, "debug missing 'rules_applied'"
    rules_applied = debug["rules_applied"]
    assert isinstance(rules_applied, list), "rules_applied should be a list"
    assert len(rules_applied) > 0, "rules_applied list is empty"


def test_strategy_generation_with_multiple_product_groups(
    client, campaign_spec_valid, product_group_high, product_group_medium, creatives_ab
):
    """Test strategy generation with multiple product groups."""
    request_payload = {
        "campaign_spec": campaign_spec_valid.model_dump(),
        "product_groups": [
            product_group_high.model_dump(),
            product_group_medium.model_dump()
        ],
        "creatives": [c.model_dump() for c in creatives_ab]
    }
    
    response = client.post("/generate_strategy", json=request_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    
    # Verify budget allocation includes both groups
    debug = data["debug"]
    budget_plan = debug["budget_plan"]
    group_allocation = budget_plan["group_allocation"]
    
    assert "high" in group_allocation, "High priority group allocation missing"
    assert "medium" in group_allocation, "Medium priority group allocation missing"
    assert group_allocation["high"] > group_allocation["medium"], "High group should get more budget than medium"


def test_strategy_generation_platform_meta(client, campaign_spec_valid, product_group_high, creatives_ab):
    """Test strategy generation specifically for Meta platform."""
    request_payload = {
        "campaign_spec": campaign_spec_valid.model_dump(),
        "product_groups": [product_group_high.model_dump()],
        "creatives": [c.model_dump() for c in creatives_ab]
    }
    
    response = client.post("/generate_strategy", json=request_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    
    # Verify platform strategy is for Meta
    platform_strategy = data["platform_strategies"][0]
    assert platform_strategy["platform"] == "meta", "Platform should be 'meta'"
    
    # Verify targeting is present for Meta
    assert "targeting" in platform_strategy, "Platform strategy missing 'targeting'"
    targeting = platform_strategy["targeting"]
    assert "age_min" in targeting, "Targeting missing 'age_min'"
    assert "age_max" in targeting, "Targeting missing 'age_max'"
    assert "interests" in targeting, "Targeting missing 'interests'"


def test_strategy_generation_objective_conversions(client, product_group_high, creatives_ab):
    """Test strategy generation for conversions objective."""
    campaign_spec = CampaignSpec(
        user_query="Create a conversions campaign",
        platform="meta",
        budget=2000.0,
        objective="conversions",
        category="electronics",
        metadata={}
    )
    
    request_payload = {
        "campaign_spec": campaign_spec.model_dump(),
        "product_groups": [product_group_high.model_dump()],
        "creatives": [c.model_dump() for c in creatives_ab]
    }
    
    response = client.post("/generate_strategy", json=request_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    
    # Verify bidding strategy is appropriate for conversions
    abstract_strategy = data["abstract_strategy"]
    bidding_strategy = abstract_strategy["bidding_strategy"]
    assert "LOWEST_COST_WITH_CAP" in bidding_strategy or "LOWEST_COST" in bidding_strategy, \
        f"Bidding strategy '{bidding_strategy}' should be appropriate for conversions"

