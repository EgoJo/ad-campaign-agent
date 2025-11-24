"""
Mock data generator for optimizer service.
"""

from .schemas import SummarizeRecentRunsResponse, OptimizationSuggestion


def get_mock_optimization_response() -> SummarizeRecentRunsResponse:
    """
    Generate mock optimization summary and suggestions.
    
    TODO: Replace with real optimization logic:
    - Analyze campaign performance metrics
    - Use ML models to identify optimization opportunities
    - Compare against benchmarks and best practices
    - Provide actionable, data-driven recommendations
    - Calculate expected ROI for each suggestion
    """
    
    suggestions = [
        OptimizationSuggestion(
            category="budget",
            suggestion="Increase budget for high-performing ad sets by 20%",
            expected_impact="Estimated 15% increase in conversions",
            priority="high"
        ),
        OptimizationSuggestion(
            category="targeting",
            suggestion="Narrow age range to 25-35 based on conversion data",
            expected_impact="Reduce CPA by approximately 12%",
            priority="high"
        ),
        OptimizationSuggestion(
            category="creative",
            suggestion="Test video creatives for products with high engagement",
            expected_impact="Potential 25% increase in click-through rate",
            priority="medium"
        ),
        OptimizationSuggestion(
            category="bidding",
            suggestion="Switch to target CPA bidding for mature campaigns",
            expected_impact="More consistent cost per conversion",
            priority="medium"
        ),
        OptimizationSuggestion(
            category="schedule",
            suggestion="Increase bids during peak hours (6-9 PM)",
            expected_impact="Capture 10% more high-intent traffic",
            priority="low"
        )
    ]
    
    summary = (
        "Recent campaigns show strong performance with an average CPA of $12.50. "
        "Top-performing campaigns are in the electronics category with 2.5x ROAS. "
        "Opportunities exist for budget reallocation and creative optimization."
    )
    
    return SummarizeRecentRunsResponse(
        summary=summary,
        total_campaigns=15,
        total_spend=25000.00,
        total_conversions=2000,
        average_cpa=12.50,
        suggestions=suggestions
    )
