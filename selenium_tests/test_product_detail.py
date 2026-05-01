"""
Product detail page tests
"""
import time
import random
from base_test import BaseTest
from config import TestConfig, SELECTORS, TEST_DATA

class ProductDetailTests(BaseTest):
    """Test suite for product detail page functionality"""
    
    def __init__(self, browser="chrome", headless=False):
        super().__init__(browser, headless)
        self.test_name = "Product Detail Tests"
    
    def test_product_detail_page_load(self, domain="garba.shop"):
        """Test product detail page loading"""
        test_name = f"Product Detail Page Load - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # First, get a product ID by visiting a category page
            product_id = self._get_sample_product_id(domain)
            
            if not product_id:
                self.log_test_result(test_name, "SKIP", "No products found to test")
                return True
            
            # Navigate to product detail page
            product_url = f"{self.config.FRONTEND_URL}/product/{product_id}"
            self.navigate_to(product_url, domain)
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot
            screenshot = self.take_screenshot("product_detail_load", f"Product detail page for {domain}")
            
            # Check essential elements
            essential_elements = [
                ("Product Image", [".product-image", ".product-main-image", "img"]),
                ("Product Title", [".product-title", ".product-name", "h1", "h2"]),
                ("Product Price", [".product-price", ".price", ".cost"]),
                ("Add to Cart Button", [".add-to-cart", "button:contains('Add to Cart')", ".cart-btn"])
            ]
            
            missing_elements = []
            for element_name, selectors in essential_elements:
                element_found = False
                for selector in selectors:
                    if self.is_element_present(selector):
                        element_found = True
                        break
                
                if not element_found:
                    missing_elements.append(element_name)
            
            if missing_elements:
                message = f"Missing elements: {', '.join(missing_elements)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            # Check for JavaScript errors
            js_errors = self.check_for_js_errors()
            if js_errors:
                message = f"JavaScript errors: {'; '.join(js_errors[:2])}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            # Check page load performance
            load_time = self.performance_metrics.get(product_url, {}).get('load_time', 0)
            if load_time > self.config.MAX_PAGE_LOAD_TIME:
                message = f"Page load time ({load_time:.2f}s) exceeds threshold"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            self.log_test_result(test_name, "PASS", f"Product detail page loaded successfully", screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("product_detail_error", f"Product detail error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_product_image_gallery(self, domain="garba.shop"):
        """Test product image gallery functionality"""
        test_name = f"Product Image Gallery - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Get a product and navigate to its detail page
            product_id = self._get_sample_product_id(domain)
            if not product_id:
                self.log_test_result(test_name, "SKIP", "No products found to test")
                return True
            
            product_url = f"{self.config.FRONTEND_URL}/product/{product_id}"
            self.navigate_to(product_url, domain)
            time.sleep(3)
            
            gallery_results = []
            
            # Check main product image
            main_image_selectors = [
                ".product-main-image img",
                ".product-image img",
                ".main-image img",
                "img[alt*='product']"
            ]
            
            main_image_found = False
            for selector in main_image_selectors:
                if self.is_element_present(selector):
                    main_image_found = True
                    break
            
            if main_image_found:
                gallery_results.append("Main image: Present")
            else:
                gallery_results.append("Main image: Missing")
            
            # Check for thumbnail images
            thumbnail_selectors = [
                ".product-thumbnails img",
                ".image-thumbnails img",
                ".gallery-thumbs img"
            ]
            
            thumbnail_count = 0
            for selector in thumbnail_selectors:
                try:
                    thumbnails = self.driver.find_elements("css selector", selector)
                    thumbnail_count += len(thumbnails)
                except:
                    continue
            
            gallery_results.append(f"Thumbnails: {thumbnail_count} found")
            
            # Test image click functionality (if thumbnails exist)
            if thumbnail_count > 0:
                try:
                    # Click on first thumbnail
                    first_thumbnail = self.driver.find_element("css selector", thumbnail_selectors[0])
                    first_thumbnail.click()
                    time.sleep(1)
                    gallery_results.append("Thumbnail click: Working")
                except:
                    gallery_results.append("Thumbnail click: Failed")
            
            # Test image zoom functionality
            zoom_test_result = self._test_image_zoom()
            gallery_results.append(f"Image zoom: {zoom_test_result}")
            
            screenshot = self.take_screenshot("product_image_gallery", f"Product image gallery for {domain}")
            
            # Evaluate results
            failed_features = [result for result in gallery_results if "Missing" in result or "Failed" in result]
            
            if len(failed_features) > len(gallery_results) / 2:
                message = f"Image gallery issues: {'; '.join(failed_features)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Image gallery: {'; '.join(gallery_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("image_gallery_error", f"Image gallery error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_product_options_selection(self, domain="garba.shop"):
        """Test product options (size, color, etc.) selection"""
        test_name = f"Product Options Selection - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Get a product and navigate to its detail page
            product_id = self._get_sample_product_id(domain)
            if not product_id:
                self.log_test_result(test_name, "SKIP", "No products found to test")
                return True
            
            product_url = f"{self.config.FRONTEND_URL}/product/{product_id}"
            self.navigate_to(product_url, domain)
            time.sleep(3)
            
            options_results = []
            
            # Test size selection
            size_result = self._test_size_selection()
            options_results.append(f"Size selection: {size_result}")
            
            # Test color selection
            color_result = self._test_color_selection()
            options_results.append(f"Color selection: {color_result}")
            
            # Test quantity selection
            quantity_result = self._test_quantity_selection()
            options_results.append(f"Quantity selection: {quantity_result}")
            
            screenshot = self.take_screenshot("product_options", f"Product options for {domain}")
            
            # If no options are available, it's not necessarily a failure
            if all("Not available" in result for result in options_results):
                message = "No product options available (may be expected)"
                self.log_test_result(test_name, "SKIP", message, screenshot)
                return True
            
            # Evaluate results
            failed_options = [result for result in options_results if "Error" in result or "Failed" in result]
            
            if len(failed_options) > 0:
                message = f"Product options issues: {'; '.join(failed_options)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Product options: {'; '.join(options_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("product_options_error", f"Product options error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_add_to_cart_functionality(self, domain="garba.shop"):
        """Test add to cart functionality from product detail page"""
        test_name = f"Add to Cart Functionality - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Get a product and navigate to its detail page
            product_id = self._get_sample_product_id(domain)
            if not product_id:
                self.log_test_result(test_name, "SKIP", "No products found to test")
                return True
            
            product_url = f"{self.config.FRONTEND_URL}/product/{product_id}"
            self.navigate_to(product_url, domain)
            time.sleep(3)
            
            # Take screenshot before adding to cart
            screenshot_before = self.take_screenshot("before_add_to_cart", f"Before adding to cart for {domain}")
            
            # Find and click add to cart button
            add_to_cart_selectors = [
                ".add-to-cart",
                "button:contains('Add to Cart')",
                ".cart-btn",
                ".add-cart-btn",
                "[data-testid='add-to-cart']"
            ]
            
            cart_button_found = False
            for selector in add_to_cart_selectors:
                if selector.startswith("button:contains"):
                    # Handle text-based selector
                    try:
                        from selenium.webdriver.common.by import By
                        button = self.driver.find_element(By.XPATH, f"//button[contains(text(), 'Add to Cart')]")
                        if button:
                            button.click()
                            cart_button_found = True
                            break
                    except:
                        continue
                else:
                    if self.safe_click(selector):
                        cart_button_found = True
                        break
            
            if not cart_button_found:
                message = "Add to cart button not found"
                self.log_test_result(test_name, "FAIL", message, screenshot_before)
                return False
            
            # Wait for cart action to complete
            time.sleep(3)
            
            # Take screenshot after adding to cart
            screenshot_after = self.take_screenshot("after_add_to_cart", f"After adding to cart for {domain}")
            
            # Check for success indicators
            success_indicators = [
                "Added to cart",
                "Item added",
                "Success",
                "Cart updated"
            ]
            
            page_text = self.driver.page_source
            success_found = any(indicator.lower() in page_text.lower() for indicator in success_indicators)
            
            # Check if cart icon shows updated count
            cart_count_updated = self._check_cart_count_update()
            
            # Check if we can navigate to cart page
            cart_navigation_works = self._test_cart_navigation()
            
            # Evaluate results
            if success_found or cart_count_updated or cart_navigation_works:
                message = f"Add to cart successful (success_msg: {success_found}, count_updated: {cart_count_updated}, nav_works: {cart_navigation_works})"
                self.log_test_result(test_name, "PASS", message, screenshot_after)
                return True
            else:
                message = "No confirmation of successful cart addition"
                self.log_test_result(test_name, "FAIL", message, screenshot_after)
                return False
            
        except Exception as e:
            screenshot = self.take_screenshot("add_to_cart_error", f"Add to cart error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_product_information_display(self, domain="garba.shop"):
        """Test product information display"""
        test_name = f"Product Information Display - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Get a product and navigate to its detail page
            product_id = self._get_sample_product_id(domain)
            if not product_id:
                self.log_test_result(test_name, "SKIP", "No products found to test")
                return True
            
            product_url = f"{self.config.FRONTEND_URL}/product/{product_id}"
            self.navigate_to(product_url, domain)
            time.sleep(3)
            
            info_results = []
            
            # Check product information elements
            info_elements = [
                ("Title", [".product-title", ".product-name", "h1", "h2"]),
                ("Price", [".product-price", ".price", ".cost"]),
                ("Description", [".product-description", ".description", ".product-details"]),
                ("SKU/Code", [".product-sku", ".product-code", ".sku"]),
                ("Availability", [".availability", ".stock-status", ".in-stock"])
            ]
            
            for element_name, selectors in info_elements:
                element_found = False
                element_text = ""
                
                for selector in selectors:
                    if self.is_element_present(selector):
                        element_found = True
                        element_text = self.get_element_text(selector)
                        break
                
                if element_found:
                    if element_text.strip():
                        info_results.append(f"{element_name}: Present with content")
                    else:
                        info_results.append(f"{element_name}: Present but empty")
                else:
                    info_results.append(f"{element_name}: Missing")
            
            # Check for domain-specific pricing (B2B vs B2C)
            price_display_result = self._check_domain_specific_pricing(domain)
            info_results.append(f"Domain-specific pricing: {price_display_result}")
            
            screenshot = self.take_screenshot("product_information", f"Product information for {domain}")
            
            # Evaluate results
            missing_info = [result for result in info_results if "Missing" in result]
            empty_info = [result for result in info_results if "empty" in result]
            
            if len(missing_info) > 2:  # More than 2 missing elements is concerning
                message = f"Too much missing information: {'; '.join(missing_info)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            if len(empty_info) > 1:  # More than 1 empty element is concerning
                message = f"Empty information fields: {'; '.join(empty_info)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Product information: {'; '.join(info_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("product_info_error", f"Product information error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def _get_sample_product_id(self, domain):
        """Helper method to get a sample product ID"""
        try:
            # Navigate to a category page to find products
            self.navigate_to(f"{self.config.FRONTEND_URL}/women", domain)
            time.sleep(3)
            
            # Look for product links
            product_link_selectors = [
                "a[href*='/product/']",
                ".product-card a",
                ".product-item a"
            ]
            
            for selector in product_link_selectors:
                try:
                    product_links = self.driver.find_elements("css selector", selector)
                    if product_links:
                        # Get href from first product link
                        href = product_links[0].get_attribute("href")
                        if href and "/product/" in href:
                            # Extract product ID from URL
                            product_id = href.split("/product/")[-1].split("?")[0].split("#")[0]
                            return product_id
                except:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def _test_image_zoom(self):
        """Helper method to test image zoom functionality"""
        try:
            # Look for zoom functionality
            zoom_selectors = [
                ".zoom-image",
                ".product-image.zoomable",
                "[data-zoom]"
            ]
            
            for selector in zoom_selectors:
                if self.is_element_present(selector):
                    # Try to hover over image to trigger zoom
                    if self.hover_over_element(selector):
                        return "Available"
            
            return "Not available"
            
        except Exception:
            return "Error testing zoom"
    
    def _test_size_selection(self):
        """Helper method to test size selection"""
        try:
            size_selectors = [
                ".size-selector",
                ".product-sizes",
                "select[name='size']",
                ".size-options"
            ]
            
            for selector in size_selectors:
                if self.is_element_present(selector):
                    if self.safe_click(selector):
                        return "Available and working"
                    else:
                        return "Available but not clickable"
            
            return "Not available"
            
        except Exception:
            return "Error testing size selection"
    
    def _test_color_selection(self):
        """Helper method to test color selection"""
        try:
            color_selectors = [
                ".color-selector",
                ".product-colors",
                "select[name='color']",
                ".color-options"
            ]
            
            for selector in color_selectors:
                if self.is_element_present(selector):
                    if self.safe_click(selector):
                        return "Available and working"
                    else:
                        return "Available but not clickable"
            
            return "Not available"
            
        except Exception:
            return "Error testing color selection"
    
    def _test_quantity_selection(self):
        """Helper method to test quantity selection"""
        try:
            quantity_selectors = [
                ".quantity-selector input",
                "input[name='quantity']",
                ".qty-input",
                ".quantity-input"
            ]
            
            for selector in quantity_selectors:
                if self.is_element_present(selector):
                    # Try to change quantity
                    if self.safe_send_keys(selector, "2", clear_first=True):
                        return "Available and working"
                    else:
                        return "Available but not editable"
            
            return "Not available"
            
        except Exception:
            return "Error testing quantity selection"
    
    def _check_cart_count_update(self):
        """Helper method to check if cart count is updated"""
        try:
            cart_count_selectors = [
                ".cart-count",
                ".cart-badge",
                ".cart-items-count",
                "[data-testid='cart-count']"
            ]
            
            for selector in cart_count_selectors:
                if self.is_element_present(selector):
                    count_text = self.get_element_text(selector)
                    if count_text and count_text.strip() != "0":
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _test_cart_navigation(self):
        """Helper method to test navigation to cart page"""
        try:
            cart_link_selectors = [
                ".cart-link",
                "a[href='/cart']",
                ".cart-icon",
                "[data-testid='cart-link']"
            ]
            
            for selector in cart_link_selectors:
                if self.safe_click(selector):
                    time.sleep(2)
                    current_url = self.get_current_url()
                    return "/cart" in current_url
            
            return False
            
        except Exception:
            return False
    
    def _check_domain_specific_pricing(self, domain):
        """Helper method to check domain-specific pricing display"""
        try:
            # Get price text
            price_selectors = [
                ".product-price",
                ".price",
                ".cost"
            ]
            
            price_text = ""
            for selector in price_selectors:
                if self.is_element_present(selector):
                    price_text = self.get_element_text(selector).lower()
                    break
            
            if not price_text:
                return "No price displayed"
            
            # Check for currency symbols or pricing indicators
            if "₹" in price_text or "rs" in price_text or "inr" in price_text:
                return "Currency displayed correctly"
            
            # For B2B domains, check for wholesale indicators
            if domain == self.config.B2B_DOMAIN:
                if "wholesale" in price_text or "bulk" in price_text:
                    return "B2B pricing indicators present"
            
            return "Basic pricing displayed"
            
        except Exception:
            return "Error checking pricing"
    
    def run_all_tests(self):
        """Run all product detail tests"""
        print(f"Running {self.test_name} with {self.browser} browser...")
        
        test_methods = [
            ("test_product_detail_page_load", ["garba.shop", "ttd.in"]),
            ("test_product_image_gallery", ["garba.shop"]),
            ("test_product_options_selection", ["garba.shop"]),
            ("test_add_to_cart_functionality", ["garba.shop"]),
            ("test_product_information_display", ["garba.shop", "ttd.in"])
        ]
        
        for method_name, domains in test_methods:
            method = getattr(self, method_name)
            
            for domain in domains:
                print(f"  Running {method_name} for {domain}...")
                method(domain)
        
        return self.test_results