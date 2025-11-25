"""
Pytest configuration and shared fixtures for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from app.common.schemas import (
    CampaignSpec,
    Product,
    ProductGroup,
    Creative
)


@pytest.fixture
def test_client():
    """FastAPI TestClient fixture."""
    from app.services.strategy_service.main import app
    return TestClient(app)


@pytest.fixture
def campaign_spec_valid():
    """Valid CampaignSpec fixture."""
    return CampaignSpec(
        user_query="Create a campaign for electronics",
        platform="meta",
        budget=2000.0,
        objective="conversions",
        category="electronics",
        time_range={"start": "2025-01-01", "end": "2025-01-31"},
        metadata={"locale": "en_US"}
    )


@pytest.fixture
def campaign_spec_small_budget():
    """CampaignSpec with small budget for edge case testing."""
    return CampaignSpec(
        user_query="Create a campaign with small budget",
        platform="meta",
        budget=50.0,
        objective="conversions",
        category="electronics",
        time_range={"start": "2025-01-01", "end": "2025-01-31"},
        metadata={}
    )


@pytest.fixture
def campaign_spec_large_budget():
    """CampaignSpec with large budget for edge case testing."""
    return CampaignSpec(
        user_query="Create a campaign with large budget",
        platform="meta",
        budget=10000.0,
        objective="conversions",
        category="electronics",
        time_range={"start": "2025-01-01", "end": "2025-01-31"},
        metadata={}
    )


@pytest.fixture
def product_group_high():
    """High priority ProductGroup fixture."""
    return ProductGroup(
        group="high",
        products=[
            Product(
                product_id="PROD-001",
                title="Wireless Headphones",
                description="Premium noise-canceling headphones",
                price=199.99,
                category="electronics",
                image_url="https://example.com/headphones.jpg",
                metadata={"age_range": "25-45"}
            )
        ],
        score_range=(0.8, 1.0),
        reasoning="High conversion potential"
    )


@pytest.fixture
def product_group_medium():
    """Medium priority ProductGroup fixture."""
    return ProductGroup(
        group="medium",
        products=[
            Product(
                product_id="PROD-002",
                title="Bluetooth Speaker",
                description="Portable wireless speaker",
                price=79.99,
                category="electronics",
                image_url="https://example.com/speaker.jpg",
                metadata={}
            )
        ],
        score_range=(0.5, 0.8),
        reasoning="Medium conversion potential"
    )


@pytest.fixture
def product_group_low():
    """Low priority ProductGroup fixture."""
    return ProductGroup(
        group="low",
        products=[
            Product(
                product_id="PROD-003",
                title="USB Cable",
                description="Standard USB charging cable",
                price=9.99,
                category="electronics",
                image_url="https://example.com/cable.jpg",
                metadata={}
            )
        ],
        score_range=(0.0, 0.5),
        reasoning="Low conversion potential"
    )


@pytest.fixture
def creatives_ab():
    """Creatives with A and B variants fixture."""
    return [
        Creative(
            creative_id="CREATIVE-001-A",
            product_id="PROD-001",
            platform="meta",
            variant_id="A",
            primary_text="Experience premium sound quality with our wireless headphones. Perfect for music lovers.",
            headline="Amazing Headphones",
            image_url="https://example.com/creative1a.jpg",
            style_profile={"copy_style": "direct_response"},
            ab_group="control"
        ),
        Creative(
            creative_id="CREATIVE-001-B",
            product_id="PROD-001",
            platform="meta",
            variant_id="B",
            primary_text="Wireless freedom for your music. Premium audio quality that you'll love.",
            headline="Premium Audio",
            image_url="https://example.com/creative1b.jpg",
            style_profile={"copy_style": "playful"},
            ab_group="variant"
        )
    ]


@pytest.fixture
def creatives_multiple_products():
    """Creatives for multiple products fixture."""
    return [
        Creative(
            creative_id="CREATIVE-001-A",
            product_id="PROD-001",
            platform="meta",
            variant_id="A",
            primary_text="Premium headphones",
            headline="Amazing Headphones",
            image_url="https://example.com/creative1a.jpg"
        ),
        Creative(
            creative_id="CREATIVE-001-B",
            product_id="PROD-001",
            platform="meta",
            variant_id="B",
            primary_text="Wireless headphones",
            headline="Premium Audio",
            image_url="https://example.com/creative1b.jpg"
        ),
        Creative(
            creative_id="CREATIVE-002-A",
            product_id="PROD-002",
            platform="meta",
            variant_id="A",
            primary_text="Portable speaker",
            headline="Bluetooth Speaker",
            image_url="https://example.com/creative2a.jpg"
        ),
        Creative(
            creative_id="CREATIVE-002-B",
            product_id="PROD-002",
            platform="meta",
            variant_id="B",
            primary_text="Wireless speaker",
            headline="Portable Audio",
            image_url="https://example.com/creative2b.jpg"
        )
    ]


@pytest.fixture
def minimal_valid_request(campaign_spec_valid, product_group_high, creatives_ab):
    """Minimal valid request payload fixture."""
    return {
        "campaign_spec": campaign_spec_valid.model_dump(),
        "product_groups": [product_group_high.model_dump()],
        "creatives": [c.model_dump() for c in creatives_ab]
    }

