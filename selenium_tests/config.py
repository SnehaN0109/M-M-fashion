"""
Configuration settings for Selenium tests
"""
import os
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class TestConfig:
    # Application URLs
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:5000"
    
    # Test domains
    B2C_DOMAIN: str = "garba.shop"
    B2B_DOMAIN: str = "ttd.in"
    
    # Browser settings
    BROWSERS: List[str] = field(default_factory=lambda: ["chrome", "firefox"])
    HEADLESS: bool = False
    
    # Viewport sizes
    DESKTOP_SIZE: tuple = (1920, 1080)
    MOBILE_SIZE: tuple = (375, 667)
    TABLET_SIZE: tuple = (768, 1024)
    
    # Test data
    TEST_USER_PHONE: str = "+919876543210"
    TEST_USER_NAME: str = "Test User"
    TEST_USER_EMAIL: str = "test@example.com"
    
    # Admin credentials
    ADMIN_PASSWORD: str = "admin123"
    
    # Timeouts (seconds)
    IMPLICIT_WAIT: int = 10
    EXPLICIT_WAIT: int = 20
    PAGE_LOAD_TIMEOUT: int = 30
    
    # Screenshot settings
    SCREENSHOT_DIR: str = "test_screenshots"
    REPORT_DIR: str = "test_reports"
    
    # Performance thresholds
    MAX_PAGE_LOAD_TIME: float = 5.0  # seconds
    MAX_API_RESPONSE_TIME: float = 2.0  # seconds

# Test data for various scenarios
TEST_DATA = {
    "valid_checkout": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+919876543210",
        "address": "123 Test Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001"
    },
    "invalid_checkout": {
        "name": "",
        "email": "invalid-email",
        "phone": "123",
        "address": "",
        "city": "",
        "state": "",
        "pincode": "invalid"
    },
    "search_terms": [
        "kurti",
        "saree",
        "lehenga",
        "shirt",
        "dress",
        "ethnic wear",
        "western wear"
    ],
    "filter_options": {
        "categories": ["Men", "Women", "Kids", "Ethnic", "Western"],
        "price_ranges": ["0-500", "500-1000", "1000-2000", "2000+"],
        "sizes": ["S", "M", "L", "XL", "XXL"]
    }
}

# Expected elements and their selectors
SELECTORS = {
    "header": {
        "logo": "[data-testid='logo']",
        "search_bar": "[data-testid='search-input']",
        "search_button": "[data-testid='search-button']",
        "cart_icon": "[data-testid='cart-icon']",
        "wishlist_icon": "[data-testid='wishlist-icon']",
        "login_button": "[data-testid='login-button']",
        "menu_toggle": "[data-testid='menu-toggle']"
    },
    "navigation": {
        "men_link": "a[href='/men']",
        "women_link": "a[href='/women']",
        "kids_link": "a[href='/kids']",
        "ethnic_link": "a[href='/ethnic']",
        "western_link": "a[href='/western']"
    },
    "product_card": {
        "container": ".product-card",
        "image": ".product-image",
        "title": ".product-title",
        "price": ".product-price",
        "add_to_cart": ".add-to-cart-btn",
        "add_to_wishlist": ".add-to-wishlist-btn"
    },
    "product_detail": {
        "main_image": ".product-main-image",
        "title": ".product-detail-title",
        "price": ".product-detail-price",
        "size_selector": ".size-selector",
        "quantity_input": ".quantity-input",
        "add_to_cart": ".add-to-cart-detail",
        "buy_now": ".buy-now-btn"
    },
    "cart": {
        "item_container": ".cart-item",
        "quantity_input": ".cart-quantity-input",
        "remove_button": ".remove-item-btn",
        "total_price": ".cart-total",
        "checkout_button": ".checkout-btn"
    },
    "checkout": {
        "name_input": "input[name='name']",
        "email_input": "input[name='email']",
        "phone_input": "input[name='phone']",
        "address_input": "textarea[name='address']",
        "city_input": "input[name='city']",
        "state_input": "input[name='state']",
        "pincode_input": "input[name='pincode']",
        "place_order_button": ".place-order-btn"
    },
    "filters": {
        "category_filter": ".category-filter",
        "price_filter": ".price-filter",
        "size_filter": ".size-filter",
        "apply_filters": ".apply-filters-btn",
        "clear_filters": ".clear-filters-btn"
    }
}