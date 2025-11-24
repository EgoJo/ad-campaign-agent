"""
Mock data generator for strategy service.
"""

from .schemas import (
    GenerateStrategyResponse, 
    PlatformStrategy, 
    Platform, 
    BidStrategy
)


def get_mock_strategy_response(total_budget: float, platforms: list) -> GenerateStrategyResponse:
    """
    Generate mock campaign strategy response.
    
    TODO: Replace with real strategy generation logic:
    - Implement ML-based budget allocation
    - Use historical performance data for predictions
    - Optimize bidding strategies based on objectives
    - Calculate realistic reach and conversion estimates
    """
    
    # Simple budget split for mock
    budget_per_platform = 100.0 / len(platforms) if platforms else 0
    daily_budget_per_platform = total_budget / len(platforms) / 30 if platforms else 0
    
    platform_strategies = []
    
    for platform in platforms:
        strategy = PlatformStrategy(
            platform=platform,
            budget_allocation=budget_per_platform,
            bid_strategy=BidStrategy.LOWEST_COST,
            target_cpa=15.0,
            daily_budget=daily_budget_per_platform,
            targeting_criteria={
                "age_range": "25-45",
                "interests": "technology, shopping",
                "location": "United States"
            }
        )
        platform_strategies.append(strategy)
    
    abstract_strategy = (
        f"Multi-platform campaign targeting tech-savvy consumers aged 25-45. "
        f"Budget of ${total_budget:.2f} allocated across {len(platforms)} platforms "
        f"with focus on conversion optimization and brand awareness."
    )
    
    return GenerateStrategyResponse(
        abstract_strategy=abstract_strategy,
        platform_strategies=platform_strategies,
        estimated_reach=500000,
        estimated_conversions=2500
    )
