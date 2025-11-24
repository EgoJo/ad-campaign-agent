"""
Mock data generator for product service.
"""

from .schemas import Product, ProductGroup, PriorityLevel, SelectProductsResponse


def get_mock_products_response() -> SelectProductsResponse:
    """
    Generate mock product selection response.
    
    TODO: Replace with real product database queries and ML-based selection logic.
    """
    high_priority_products = [
        Product(
            product_id="PROD-001",
            name="Premium Wireless Headphones",
            description="High-quality noise-canceling wireless headphones",
            price=299.99,
            category="Electronics",
            image_url="https://example.com/images/headphones.jpg",
            stock_quantity=150
        ),
        Product(
            product_id="PROD-002",
            name="Smart Watch Pro",
            description="Advanced fitness tracking smartwatch",
            price=399.99,
            category="Electronics",
            image_url="https://example.com/images/smartwatch.jpg",
            stock_quantity=200
        )
    ]
    
    medium_priority_products = [
        Product(
            product_id="PROD-003",
            name="Bluetooth Speaker",
            description="Portable waterproof Bluetooth speaker",
            price=79.99,
            category="Electronics",
            image_url="https://example.com/images/speaker.jpg",
            stock_quantity=300
        ),
        Product(
            product_id="PROD-004",
            name="Wireless Charger",
            description="Fast wireless charging pad",
            price=39.99,
            category="Accessories",
            image_url="https://example.com/images/charger.jpg",
            stock_quantity=500
        )
    ]
    
    low_priority_products = [
        Product(
            product_id="PROD-005",
            name="USB-C Cable",
            description="Durable USB-C charging cable",
            price=14.99,
            category="Accessories",
            image_url="https://example.com/images/cable.jpg",
            stock_quantity=1000
        )
    ]
    
    product_groups = [
        ProductGroup(priority=PriorityLevel.HIGH, products=high_priority_products),
        ProductGroup(priority=PriorityLevel.MEDIUM, products=medium_priority_products),
        ProductGroup(priority=PriorityLevel.LOW, products=low_priority_products)
    ]
    
    total_products = sum(len(group.products) for group in product_groups)
    
    return SelectProductsResponse(
        product_groups=product_groups,
        total_products=total_products
    )
