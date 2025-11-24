"""
Mock data generator for creative service.
"""

from .schemas import Creative, CreativeType, GenerateCreativesResponse


def get_mock_creatives_response(product_ids: list) -> GenerateCreativesResponse:
    """
    Generate mock creative content response.
    
    TODO: Replace with real creative generation logic:
    - Integrate with Gemini API for text generation
    - Use image generation APIs for visual assets
    - Implement A/B testing variants
    - Apply brand guidelines and style consistency
    """
    creatives = []
    
    for idx, product_id in enumerate(product_ids[:3]):  # Limit to first 3 products for mock
        creatives.append(
            Creative(
                creative_id=f"CREATIVE-{idx+1:03d}",
                creative_type=CreativeType.IMAGE,
                headline=f"Discover Amazing {product_id}!",
                body_text=f"Get the best deals on premium products. Limited time offer!",
                call_to_action="Shop Now",
                asset_url=f"https://example.com/creatives/ad_{idx+1}.jpg",
                product_id=product_id
            )
        )
        
        # Add a text variant
        creatives.append(
            Creative(
                creative_id=f"CREATIVE-{idx+1:03d}-TEXT",
                creative_type=CreativeType.TEXT,
                headline=f"Don't Miss Out on {product_id}",
                body_text=f"Premium quality at unbeatable prices. Order today and save!",
                call_to_action="Learn More",
                asset_url=None,
                product_id=product_id
            )
        )
    
    return GenerateCreativesResponse(
        creatives=creatives,
        total_creatives=len(creatives)
    )
