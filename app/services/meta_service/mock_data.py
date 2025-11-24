"""
Mock data generator for Meta service.
"""

import uuid
from .schemas import CreateCampaignResponse, AdResult


def get_mock_campaign_response(creatives: list) -> CreateCampaignResponse:
    """
    Generate mock campaign creation response.
    
    TODO: Replace with real Meta API integration:
    - Use Facebook Marketing API
    - Create actual campaigns, ad sets, and ads
    - Handle authentication and permissions
    - Implement error handling and retries
    - Add campaign status monitoring
    """
    
    campaign_id = f"CAMP-{uuid.uuid4().hex[:12].upper()}"
    ad_set_id = f"ADSET-{uuid.uuid4().hex[:12].upper()}"
    
    ad_results = []
    for creative in creatives:
        ad_result = AdResult(
            ad_id=f"AD-{uuid.uuid4().hex[:12].upper()}",
            creative_id=creative.creative_id,
            status="PENDING_REVIEW"
        )
        ad_results.append(ad_result)
    
    return CreateCampaignResponse(
        campaign_id=campaign_id,
        ad_set_id=ad_set_id,
        ad_ids=ad_results,
        status="ACTIVE"
    )
