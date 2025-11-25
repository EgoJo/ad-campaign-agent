"""
Reusable test data for all test suites.

This module provides standardized test data that aligns with app/common/schemas.py
definitions, ensuring consistency across all tests.
"""

from app.common.schemas import (
    CampaignSpec,
    Product,
    ProductGroup,
    Creative,
    AbstractStrategy,
    PlatformStrategy
)

# ============================================================================
# Campaign Specifications
# ============================================================================

VALID_CAMPAIGN_SPEC_META_TOYS = CampaignSpec(
    user_query="Create a campaign for children's toys on Meta",
    platform="meta",
    budget=5000.0,
    objective="conversions",
    category="toys",
    time_range={"start": "2025-01-01", "end": "2025-01-31"},
    metadata={"locale": "en_US", "target_audience": "parents with children aged 3-8"}
)

VALID_CAMPAIGN_SPEC_META_ELECTRONICS = CampaignSpec(
    user_query="Create a campaign for electronics on Meta",
    platform="meta",
    budget=10000.0,
    objective="sales",
    category="electronics",
    time_range={"start": "2025-01-01", "end": "2025-01-31"},
    metadata={"locale": "en_US", "target_audience": "tech enthusiasts aged 25-45"}
)

VALID_CAMPAIGN_SPEC_TIKTOK_FASHION = CampaignSpec(
    user_query="Create a fashion campaign on TikTok",
    platform="tiktok",
    budget=3000.0,
    objective="traffic",
    category="fashion",
    time_range={"start": "2025-01-01", "end": "2025-01-31"},
    metadata={"locale": "en_US", "target_audience": "fashion-forward millennials"}
)

VALID_CAMPAIGN_SPEC_GOOGLE_HEALTH = CampaignSpec(
    user_query="Create a health products campaign on Google",
    platform="google",
    budget=8000.0,
    objective="leads",
    category="health",
    time_range={"start": "2025-01-01", "end": "2025-01-31"},
    metadata={"locale": "en_US", "target_audience": "health-conscious adults"}
)

# ============================================================================
# Products
# ============================================================================

SAMPLE_PRODUCTS_TOYS = [
    Product(
        product_id="TOY-001",
        title="Creative Building Blocks 150pcs",
        description="Educational building blocks for children aged 3-8. Safe, colorful, and promotes creativity.",
        price=49.99,
        category="toys",
        image_url="https://example.com/images/toy-blocks.jpg",
        metadata={"age_range": "3-8", "brand": "KidsBuild", "material": "plastic"}
    ),
    Product(
        product_id="TOY-002",
        title="Remote Control Car",
        description="Fast and fun remote control car with LED lights. Perfect for outdoor play.",
        price=79.99,
        category="toys",
        image_url="https://example.com/images/rc-car.jpg",
        metadata={"age_range": "5-12", "brand": "SpeedToys", "battery": "included"}
    ),
    Product(
        product_id="TOY-003",
        title="Art Supplies Set",
        description="Complete art set with crayons, markers, and coloring books. Encourages artistic expression.",
        price=29.99,
        category="toys",
        image_url="https://example.com/images/art-set.jpg",
        metadata={"age_range": "4-10", "brand": "ArtKids", "pieces": 50}
    )
]

SAMPLE_PRODUCTS_ELECTRONICS = [
    Product(
        product_id="ELEC-001",
        title="Premium Wireless Headphones",
        description="High-quality noise-canceling wireless headphones with premium sound quality and long battery life.",
        price=299.99,
        category="electronics",
        image_url="https://example.com/images/headphones.jpg",
        metadata={"brand": "AudioTech", "warranty": "2 years", "features": ["noise_canceling", "wireless"]}
    ),
    Product(
        product_id="ELEC-002",
        title="Smart Watch Pro",
        description="Advanced fitness tracking smartwatch with heart rate monitor, GPS, and 7-day battery life.",
        price=399.99,
        category="electronics",
        image_url="https://example.com/images/smartwatch.jpg",
        metadata={"brand": "TechWear", "features": ["GPS", "heart_rate", "waterproof"]}
    ),
    Product(
        product_id="ELEC-003",
        title="Bluetooth Speaker",
        description="Portable waterproof Bluetooth speaker with 360-degree sound and 12-hour battery.",
        price=79.99,
        category="electronics",
        image_url="https://example.com/images/speaker.jpg",
        metadata={"waterproof": True, "battery_hours": 12, "brand": "SoundMax"}
    )
]

SAMPLE_PRODUCTS_FASHION = [
    Product(
        product_id="FASH-001",
        title="Designer Sunglasses",
        description="Stylish UV-protection sunglasses with premium frame and polarized lenses.",
        price=129.99,
        category="fashion",
        image_url="https://example.com/images/sunglasses.jpg",
        metadata={"brand": "StyleCo", "uv_protection": True, "frame_material": "acetate"}
    ),
    Product(
        product_id="FASH-002",
        title="Leather Handbag",
        description="Elegant leather handbag with multiple compartments. Perfect for everyday use.",
        price=199.99,
        category="fashion",
        image_url="https://example.com/images/handbag.jpg",
        metadata={"brand": "LuxuryBags", "material": "genuine_leather", "color": "black"}
    )
]

# ============================================================================
# Product Groups
# ============================================================================

SAMPLE_PRODUCT_GROUPS_TOYS = [
    ProductGroup(
        group="high",
        products=[SAMPLE_PRODUCTS_TOYS[0], SAMPLE_PRODUCTS_TOYS[1]],
        score_range=(0.8, 1.0),
        reasoning="High conversion potential based on category match and product quality"
    ),
    ProductGroup(
        group="medium",
        products=[SAMPLE_PRODUCTS_TOYS[2]],
        score_range=(0.5, 0.8),
        reasoning="Medium conversion potential"
    )
]

SAMPLE_PRODUCT_GROUPS_ELECTRONICS = [
    ProductGroup(
        group="high",
        products=[SAMPLE_PRODUCTS_ELECTRONICS[0], SAMPLE_PRODUCTS_ELECTRONICS[1]],
        score_range=(0.85, 1.0),
        reasoning="High-value electronics with strong market demand"
    ),
    ProductGroup(
        group="medium",
        products=[SAMPLE_PRODUCTS_ELECTRONICS[2]],
        score_range=(0.6, 0.85),
        reasoning="Good product with competitive pricing"
    )
]

# ============================================================================
# Creatives
# ============================================================================

SAMPLE_CREATIVES_TOYS = [
    Creative(
        creative_id="CREATIVE-TOY-001-A",
        product_id="TOY-001",
        platform="meta",
        variant_id="A",
        primary_text="Spark your child's creativity with our 150-piece building blocks set! Safe, colorful, and educational. Perfect for ages 3-8.",
        headline="Build, Create, Learn!",
        image_url="https://example.com/generated/toy-blocks-a.jpg",
        style_profile={"copy_style": "playful", "tone": "energetic"},
        ab_group="control"
    ),
    Creative(
        creative_id="CREATIVE-TOY-001-B",
        product_id="TOY-001",
        platform="meta",
        variant_id="B",
        primary_text="Watch your child's imagination come to life! Our building blocks encourage hours of creative play and learning.",
        headline="Unlock Creativity",
        image_url="https://example.com/generated/toy-blocks-b.jpg",
        style_profile={"copy_style": "playful", "tone": "warm"},
        ab_group="variant"
    )
]

SAMPLE_CREATIVES_ELECTRONICS = [
    Creative(
        creative_id="CREATIVE-ELEC-001-A",
        product_id="ELEC-001",
        platform="meta",
        variant_id="A",
        primary_text="Experience premium sound quality with noise-canceling technology. Perfect for music lovers and professionals.",
        headline="Premium Audio Experience",
        image_url="https://example.com/generated/headphones-a.jpg",
        style_profile={"copy_style": "technical_benefit", "tone": "authoritative"},
        ab_group="control"
    ),
    Creative(
        creative_id="CREATIVE-ELEC-001-B",
        product_id="ELEC-001",
        platform="meta",
        variant_id="B",
        primary_text="Immerse yourself in crystal-clear audio. Wireless freedom meets professional-grade sound quality.",
        headline="Wireless Freedom",
        image_url="https://example.com/generated/headphones-b.jpg",
        style_profile={"copy_style": "technical_benefit", "tone": "professional"},
        ab_group="variant"
    )
]

# ============================================================================
# Strategies
# ============================================================================

SAMPLE_ABSTRACT_STRATEGY = AbstractStrategy(
    objective="conversions",
    budget_split={"A": 0.4, "B": 0.35, "C": 0.25},
    bidding_strategy="lowest_cost",
    constraints={"max_daily_budget": 500.0, "min_age": 25, "max_age": 45},
    metadata={"optimization_goal": "conversions", "target_cpa": 15.0}
)

SAMPLE_PLATFORM_STRATEGY_META = PlatformStrategy(
    platform="meta",
    campaign_structure={
        "campaign": {"name": "Electronics Campaign", "objective": "CONVERSIONS"},
        "adset": {"name": "High Priority Products", "daily_budget": 333.33},
        "ad": {"format": "single_image", "creative_count": 6}
    },
    optimization_goal="CONVERSIONS",
    targeting={
        "age_min": 25,
        "age_max": 45,
        "genders": [1, 2],
        "interests": ["technology", "electronics"],
        "locations": ["US"]
    },
    placements=["facebook_feed", "instagram_feed"],
    metadata={"billing_event": "IMPRESSIONS", "bid_strategy": "LOWEST_COST"}
)

# ============================================================================
# Helper Functions
# ============================================================================

def get_sample_products_for_category(category: str) -> list[Product]:
    """Get sample products for a specific category."""
    category_map = {
        "toys": SAMPLE_PRODUCTS_TOYS,
        "electronics": SAMPLE_PRODUCTS_ELECTRONICS,
        "fashion": SAMPLE_PRODUCTS_FASHION
    }
    return category_map.get(category.lower(), SAMPLE_PRODUCTS_ELECTRONICS)

def get_sample_product_groups_for_category(category: str) -> list[ProductGroup]:
    """Get sample product groups for a specific category."""
    category_map = {
        "toys": SAMPLE_PRODUCT_GROUPS_TOYS,
        "electronics": SAMPLE_PRODUCT_GROUPS_ELECTRONICS
    }
    return category_map.get(category.lower(), SAMPLE_PRODUCT_GROUPS_ELECTRONICS)

def get_sample_creatives_for_product(product_id: str, platform: str = "meta") -> list[Creative]:
    """Get sample creatives for a specific product."""
    # Map product IDs to creatives
    creative_map = {
        "TOY-001": SAMPLE_CREATIVES_TOYS,
        "ELEC-001": SAMPLE_CREATIVES_ELECTRONICS
    }
    creatives = creative_map.get(product_id, SAMPLE_CREATIVES_ELECTRONICS)
    # Update platform if needed
    if platform != "meta":
        return [
            Creative(**{**c.model_dump(), "platform": platform})
            for c in creatives
        ]
    return creatives

