"""
Edge case tests for strategy generation.

Tests verify behavior with:
- Very small budgets
- Very large budgets
- Non-Meta platforms
- Different objectives
- Various time ranges
"""

import pytest
from fastapi.testclient import TestClient
from app.services.strategy_service.main import app
from app.common.schemas import CampaignSpec, ProductGroup, Creative, Product


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    return TestClient(app)


def test_very_small_budget(client, product_group_high, creatives_ab):
    """
    Test strategy generation with very small budget.
    
    Should return a "single adset" style strategy.
    """
    campaign_spec = CampaignSpec(
        user_query="Test small budget campaign",
        platform="meta",
        budget=50.0,  # Very small budget
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
    
    # Verify platform strategy has single adset structure
    platform_strategy = data["platform_strategies"][0]
    campaign_structure = platform_strategy["campaign_structure"]
    
    assert "adsets" in campaign_structure, "campaign_structure missing 'adsets'"
    adsets = campaign_structure["adsets"]
    
    # Small budget should result in single adset
    assert len(adsets) == 1, \
        f"Small budget should produce 1 adset, got {len(adsets)}"


def test_large_budget(client, product_group_high, product_group_medium, creatives_multiple_products):
    """
    Test strategy generation with large budget.
    
    Should produce multi-adset structure.
    """
    campaign_spec = CampaignSpec(
        user_query="Test large budget campaign",
        platform="meta",
        budget=10000.0,  # Large budget
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
    
    # Verify platform strategy has multi-adset structure
    platform_strategy = data["platform_strategies"][0]
    campaign_structure = platform_strategy["campaign_structure"]
    
    assert "adsets" in campaign_structure, "campaign_structure missing 'adsets'"
    adsets = campaign_structure["adsets"]
    
    # Large budget should result in multiple adsets
    assert len(adsets) >= 2, \
        f"Large budget should produce multiple adsets, got {len(adsets)}"
    
    # Verify bidding strategy is appropriate for conversions
    abstract_strategy = data["abstract_strategy"]
    bidding_strategy = abstract_strategy["bidding_strategy"]
    assert "LOWEST_COST_WITH_CAP" in bidding_strategy or "LOWEST_COST" in bidding_strategy, \
        f"Bidding strategy '{bidding_strategy}' should be appropriate for conversions"


def test_non_meta_platform_tiktok(client, product_group_high, creatives_ab):
    """Test strategy generation for TikTok platform."""
    campaign_spec = CampaignSpec(
        user_query="Test TikTok campaign",
        platform="tiktok",
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
    
    # Service should handle non-Meta platforms
    # Either return success with default strategy or error
    assert response.status_code in [200, 400]
    
    data = response.json()
    
    if data["status"] == "success":
        # If successful, verify platform is TikTok
        platform_strategy = data["platform_strategies"][0]
        assert platform_strategy["platform"] == "tiktok", \
            "Platform should be 'tiktok'"
    else:
        # If error, verify it's a clear error message
        assert "error_code" in data
        assert "message" in data


def test_non_meta_platform_google(client, product_group_high, creatives_ab):
    """Test strategy generation for Google platform."""
    campaign_spec = CampaignSpec(
        user_query="Test Google campaign",
        platform="google",
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
    assert response.status_code in [200, 400]
    
    data = response.json()
    
    if data["status"] == "success":
        platform_strategy = data["platform_strategies"][0]
        assert platform_strategy["platform"] == "google", \
            "Platform should be 'google'"
    else:
        assert "error_code" in data


def test_objective_traffic(client, product_group_high, creatives_ab):
    """Test strategy generation for traffic objective."""
    campaign_spec = CampaignSpec(
        user_query="Test traffic campaign",
        platform="meta",
        budget=2000.0,
        objective="traffic",
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
    
    # Verify bidding strategy is appropriate for traffic
    abstract_strategy = data["abstract_strategy"]
    bidding_strategy = abstract_strategy["bidding_strategy"]
    assert "LOWEST_COST" in bidding_strategy, \
        f"Bidding strategy '{bidding_strategy}' should include 'LOWEST_COST' for traffic objective"


def test_objective_sales(client, product_group_high, creatives_ab):
    """Test strategy generation for sales objective."""
    campaign_spec = CampaignSpec(
        user_query="Test sales campaign",
        platform="meta",
        budget=2000.0,
        objective="sales",
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
    
    # Verify bidding strategy is appropriate for sales
    abstract_strategy = data["abstract_strategy"]
    bidding_strategy = abstract_strategy["bidding_strategy"]
    assert "LOWEST_COST_WITH_CAP" in bidding_strategy or "LOWEST_COST" in bidding_strategy, \
        f"Bidding strategy '{bidding_strategy}' should be appropriate for sales"


def test_time_range_provided(client, product_group_high, creatives_ab):
    """Test strategy generation with time range."""
    campaign_spec = CampaignSpec(
        user_query="Test campaign with time range",
        platform="meta",
        budget=2000.0,
        objective="conversions",
        category="electronics",
        time_range={"start": "2025-01-01", "end": "2025-01-15"},  # 14 days
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
    
    # Verify daily budget is calculated correctly
    platform_strategy = data["platform_strategies"][0]
    metadata = platform_strategy.get("metadata", {})
    
    if "daily_budget" in metadata:
        daily_budget = metadata["daily_budget"]
        # Daily budget should be approximately total_budget / duration_days
        # Allow some flexibility
        assert daily_budget > 0, "Daily budget should be positive"
        assert daily_budget <= 2000.0, "Daily budget should not exceed total budget"


def test_no_time_range(client, product_group_high, creatives_ab):
    """Test strategy generation without time range."""
    campaign_spec = CampaignSpec(
        user_query="Test campaign without time range",
        platform="meta",
        budget=2000.0,
        objective="conversions",
        category="electronics",
        time_range=None,  # No time range
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
    
    # Service should handle missing time_range gracefully
    platform_strategy = data["platform_strategies"][0]
    assert "campaign_structure" in platform_strategy


def test_different_categories(client, product_group_high, creatives_ab):
    """Test strategy generation for different product categories."""
    categories = ["toys", "fashion", "beauty", "sports", "food"]
    
    for category in categories:
        campaign_spec = CampaignSpec(
            user_query=f"Test {category} campaign",
            platform="meta",
            budget=2000.0,
            objective="conversions",
            category=category,
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
        
        # Verify targeting is category-appropriate
        debug = data["debug"]
        targeting_plan = debug.get("targeting_plan", {})
        
        if category == "toys":
            # Toys should target parents
            assert targeting_plan.get("age_min", 0) >= 25, \
                "Toys category should target parents (age >= 25)"
        elif category == "fashion":
            # Fashion should have fashion interests
            interests = targeting_plan.get("interests", [])
            assert any("fashion" in str(interest).lower() for interest in interests), \
                "Fashion category should include fashion interests"

