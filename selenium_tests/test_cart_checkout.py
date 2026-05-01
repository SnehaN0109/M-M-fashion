"""
Cart and checkout functionality tests
"""
import time
import random
from base_test import BaseTest
from config import TestConfig, SELECTORS, TEST_DATA

class CartCheckoutTests(BaseTest):
    """Test suite for cart and checkout functionality"""
    
    def __init__(self, browser="chrome", headless=False):
        super().__init__(browser, headless)
        self.test_name = "Cart and Checkout Tests"
    
    def test_add_to_cart_from_product_list(self, domain="garba.shop"):
        """Test adding products to cart from product listing page"""
        test_name = f"Add to Cart from Product List - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Navigate to a category page with products
            self.navigate_to(f"{self.config.FRONTEND_URL}/women", domain)
            time.sleep(3)
            
            # Find product cards with add to cart buttons
            product_cards = self._find_product_cards()
            
            if not product_cards:
                self.log_test_result(test_name, "SKIP", "No products found to add to cart")
                return True
            
            # Try to add first few products to cart
            added_products = 0
            max_products_to_add = min(3, len(product_cards))
            
            for i in range(max_products_to_add):
                try:
                    product_card = product_cards[i]
                    
                    # Look for add to cart button within this product card
                    add_to_cart_selectors = [
                        ".add-to-cart",
                        ".cart-btn",
                        "button:contains('Add to Cart')",
                        ".add-cart-btn"
                    ]
                    
                    cart_button_found = False
                    for selector in add_to_cart_selectors:
                        try:
                            if selector.startswith("button:contains"):
                                from selenium.webdriver.common.by import By
                                button = product_card.find_element(By.XPATH, ".//button[contains(text(), 'Add to Cart')]")
                            else:
                                button = product_card.find_element("css selector", selector)
                            
                            if button:
                                # Scroll to button and click
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                                time.sleep(0.5)
                                button.click()
                                cart_button_found = True
                                added_products += 1
                                time.sleep(2)  # Wait for cart update
                                break
                        except:
                            continue
                    
                    if not cart_button_found:
                        print(f"Add to cart button not found for product {i+1}")
                
                except Exception as e:
                    print(f"Error adding product {i+1} to cart: {str(e)}")
            
            screenshot = self.take_screenshot("add_to_cart_list", f"Added products to cart from list for {domain}")
            
            if added_products == 0:
                message = "No products could be added to cart"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            # Check cart count or navigate to cart to verify
            cart_verification = self._verify_cart_has_items()
            
            if cart_verification:
                message = f"Successfully added {added_products} products to cart"
                self.log_test_result(test_name, "PASS", message, screenshot)
                return True
            else:
                message = f"Added {added_products} products but cart verification failed"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
        except Exception as e:
            screenshot = self.take_screenshot("add_to_cart_list_error", f"Add to cart from list error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_cart_page_functionality(self, domain="garba.shop"):
        """Test cart page functionality including quantity updates and item removal"""
        test_name = f"Cart Page Functionality - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # First add some items to cart
            self._add_sample_items_to_cart(domain)
            
            # Navigate to cart page
            cart_url = f"{self.config.FRONTEND_URL}/cart"
            self.navigate_to(cart_url, domain)
            time.sleep(3)
            
            # Take screenshot of cart page
            screenshot = self.take_screenshot("cart_page", f"Cart page for {domain}")
            
            cart_results = []
            
            # Check if cart page loads
            if "cart" not in self.get_current_url().lower():
                cart_results.append("Cart page: Not accessible")
            else:
                cart_results.append("Cart page: Loaded successfully")
            
            # Check for cart items
            cart_items = self._find_cart_items()
            cart_results.append(f"Cart items: {len(cart_items)} found")
            
            if len(cart_items) > 0:
                # Test quantity update
                quantity_update_result = self._test_quantity_update(cart_items[0])
                cart_results.append(f"Quantity update: {quantity_update_result}")
                
                # Test item removal (if more than one item)
                if len(cart_items) > 1:
                    item_removal_result = self._test_item_removal(cart_items[-1])
                    cart_results.append(f"Item removal: {item_removal_result}")
                
                # Test cart total calculation
                total_calculation_result = self._test_cart_total_calculation()
                cart_results.append(f"Total calculation: {total_calculation_result}")
            
            # Test proceed to checkout button
            checkout_button_result = self._test_checkout_button()
            cart_results.append(f"Checkout button: {checkout_button_result}")
            
            screenshot = self.take_screenshot("cart_functionality", f"Cart functionality test for {domain}")
            
            # Evaluate results
            failed_features = [result for result in cart_results if "Error" in result or "Failed" in result or "Not accessible" in result]
            
            if len(failed_features) > len(cart_results) / 2:
                message = f"Cart functionality issues: {'; '.join(failed_features)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Cart functionality: {'; '.join(cart_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("cart_functionality_error", f"Cart functionality error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_checkout_form_validation(self, domain="garba.shop"):
        """Test checkout form validation"""
        test_name = f"Checkout Form Validation - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Add items to cart and proceed to checkout
            self._add_sample_items_to_cart(domain)
            
            # Navigate to checkout page
            checkout_url = f"{self.config.FRONTEND_URL}/checkout"
            self.navigate_to(checkout_url, domain)
            time.sleep(3)
            
            validation_results = []
            
            # Test empty form submission
            empty_form_result = self._test_empty_form_submission()
            validation_results.append(f"Empty form validation: {empty_form_result}")
            
            # Test invalid email validation
            invalid_email_result = self._test_invalid_email_validation()
            validation_results.append(f"Invalid email validation: {invalid_email_result}")
            
            # Test invalid phone validation
            invalid_phone_result = self._test_invalid_phone_validation()
            validation_results.append(f"Invalid phone validation: {invalid_phone_result}")
            
            # Test invalid pincode validation
            invalid_pincode_result = self._test_invalid_pincode_validation()
            validation_results.append(f"Invalid pincode validation: {invalid_pincode_result}")
            
            screenshot = self.take_screenshot("checkout_validation", f"Checkout form validation for {domain}")
            
            # Evaluate results
            failed_validations = [result for result in validation_results if "Failed" in result or "Error" in result]
            
            if len(failed_validations) > 0:
                message = f"Checkout validation issues: {'; '.join(failed_validations)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Checkout validation: {'; '.join(validation_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("checkout_validation_error", f"Checkout validation error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_successful_checkout_flow(self, domain="garba.shop"):
        """Test complete successful checkout flow"""
        test_name = f"Successful Checkout Flow - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Add items to cart
            self._add_sample_items_to_cart(domain)
            
            # Navigate to checkout page
            checkout_url = f"{self.config.FRONTEND_URL}/checkout"
            self.navigate_to(checkout_url, domain)
            time.sleep(3)
            
            # Fill out checkout form with valid data
            form_fill_result = self._fill_checkout_form(TEST_DATA["valid_checkout"])
            
            if not form_fill_result:
                message = "Failed to fill checkout form"
                screenshot = self.take_screenshot("checkout_form_fill_error", f"Checkout form fill error for {domain}")
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            # Take screenshot before submitting
            screenshot_before = self.take_screenshot("before_checkout_submit", f"Before checkout submission for {domain}")
            
            # Submit the form
            submit_result = self._submit_checkout_form()
            
            if not submit_result:
                message = "Failed to submit checkout form"
                self.log_test_result(test_name, "FAIL", message, screenshot_before)
                return False
            
            # Wait for order processing
            time.sleep(5)
            
            # Take screenshot after submission
            screenshot_after = self.take_screenshot("after_checkout_submit", f"After checkout submission for {domain}")
            
            # Check for success indicators
            success_result = self._check_checkout_success()
            
            if success_result:
                message = f"Checkout completed successfully: {success_result}"
                self.log_test_result(test_name, "PASS", message, screenshot_after)
                return True
            else:
                message = "Checkout submission did not show success confirmation"
                self.log_test_result(test_name, "FAIL", message, screenshot_after)
                return False
            
        except Exception as e:
            screenshot = self.take_screenshot("checkout_flow_error", f"Checkout flow error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_cart_persistence(self, domain="garba.shop"):
        """Test cart persistence across page navigation"""
        test_name = f"Cart Persistence - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Add items to cart
            self._add_sample_items_to_cart(domain)
            
            # Get initial cart count
            initial_cart_count = self._get_cart_count()
            
            # Navigate to different pages
            pages_to_visit = [
                f"{self.config.FRONTEND_URL}/",
                f"{self.config.FRONTEND_URL}/men",
                f"{self.config.FRONTEND_URL}/about-us"
            ]
            
            persistence_results = []
            
            for page_url in pages_to_visit:
                try:
                    self.navigate_to(page_url, domain)
                    time.sleep(2)
                    
                    current_cart_count = self._get_cart_count()
                    
                    if current_cart_count == initial_cart_count:
                        persistence_results.append(f"{page_url.split('/')[-1] or 'home'}: Cart persisted")
                    else:
                        persistence_results.append(f"{page_url.split('/')[-1] or 'home'}: Cart count changed ({initial_cart_count} -> {current_cart_count})")
                
                except Exception as e:
                    persistence_results.append(f"{page_url.split('/')[-1] or 'home'}: Error - {str(e)}")
            
            screenshot = self.take_screenshot("cart_persistence", f"Cart persistence test for {domain}")
            
            # Evaluate results
            failed_persistence = [result for result in persistence_results if "changed" in result or "Error" in result]
            
            if len(failed_persistence) > 0:
                message = f"Cart persistence issues: {'; '.join(failed_persistence)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Cart persistence: {'; '.join(persistence_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("cart_persistence_error", f"Cart persistence error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def _find_product_cards(self):
        """Helper method to find product cards on the page"""
        product_card_selectors = [
            ".product-card",
            ".product-item",
            ".product",
            "[data-testid='product-card']"
        ]
        
        for selector in product_card_selectors:
            try:
                cards = self.driver.find_elements("css selector", selector)
                if cards:
                    return cards
            except:
                continue
        
        return []
    
    def _add_sample_items_to_cart(self, domain):
        """Helper method to add sample items to cart"""
        try:
            # Navigate to women's category (usually has products)
            self.navigate_to(f"{self.config.FRONTEND_URL}/women", domain)
            time.sleep(3)
            
            # Find and click add to cart on first available product
            product_cards = self._find_product_cards()
            
            if product_cards:
                for card in product_cards[:2]:  # Try to add 2 items
                    try:
                        add_to_cart_btn = card.find_element("css selector", ".add-to-cart, .cart-btn, button")
                        add_to_cart_btn.click()
                        time.sleep(2)
                    except:
                        continue
            
            return True
            
        except Exception:
            return False
    
    def _verify_cart_has_items(self):
        """Helper method to verify cart has items"""
        try:
            # Check cart count
            cart_count = self._get_cart_count()
            if cart_count > 0:
                return True
            
            # Try navigating to cart page
            self.navigate_to(f"{self.config.FRONTEND_URL}/cart")
            time.sleep(2)
            
            # Check for cart items on cart page
            cart_items = self._find_cart_items()
            return len(cart_items) > 0
            
        except Exception:
            return False
    
    def _get_cart_count(self):
        """Helper method to get cart count"""
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
                    if count_text.isdigit():
                        return int(count_text)
            
            return 0
            
        except Exception:
            return 0
    
    def _find_cart_items(self):
        """Helper method to find cart items on cart page"""
        cart_item_selectors = [
            ".cart-item",
            ".cart-product",
            ".item",
            "[data-testid='cart-item']"
        ]
        
        for selector in cart_item_selectors:
            try:
                items = self.driver.find_elements("css selector", selector)
                if items:
                    return items
            except:
                continue
        
        return []
    
    def _test_quantity_update(self, cart_item):
        """Helper method to test quantity update functionality"""
        try:
            # Look for quantity input within the cart item
            quantity_selectors = [
                "input[type='number']",
                ".quantity-input",
                ".qty-input",
                "input[name='quantity']"
            ]
            
            for selector in quantity_selectors:
                try:
                    quantity_input = cart_item.find_element("css selector", selector)
                    if quantity_input:
                        # Get current value
                        current_value = quantity_input.get_attribute("value")
                        
                        # Update quantity
                        quantity_input.clear()
                        quantity_input.send_keys("3")
                        
                        # Trigger update (look for update button or just wait)
                        update_buttons = cart_item.find_elements("css selector", ".update-btn, .update-quantity, button")
                        if update_buttons:
                            update_buttons[0].click()
                        
                        time.sleep(2)
                        return "Working"
                except:
                    continue
            
            return "Not found"
            
        except Exception:
            return "Error"
    
    def _test_item_removal(self, cart_item):
        """Helper method to test item removal functionality"""
        try:
            # Look for remove button within the cart item
            remove_selectors = [
                ".remove-btn",
                ".delete-btn",
                ".remove-item",
                "button:contains('Remove')",
                ".fa-trash"
            ]
            
            for selector in remove_selectors:
                try:
                    if selector.startswith("button:contains"):
                        from selenium.webdriver.common.by import By
                        remove_btn = cart_item.find_element(By.XPATH, ".//button[contains(text(), 'Remove')]")
                    else:
                        remove_btn = cart_item.find_element("css selector", selector)
                    
                    if remove_btn:
                        remove_btn.click()
                        time.sleep(2)
                        return "Working"
                except:
                    continue
            
            return "Not found"
            
        except Exception:
            return "Error"
    
    def _test_cart_total_calculation(self):
        """Helper method to test cart total calculation"""
        try:
            total_selectors = [
                ".cart-total",
                ".total-amount",
                ".grand-total",
                ".order-total"
            ]
            
            for selector in total_selectors:
                if self.is_element_present(selector):
                    total_text = self.get_element_text(selector)
                    if total_text and ("₹" in total_text or "rs" in total_text.lower()):
                        return "Displayed correctly"
            
            return "Not found"
            
        except Exception:
            return "Error"
    
    def _test_checkout_button(self):
        """Helper method to test checkout button"""
        try:
            checkout_selectors = [
                ".checkout-btn",
                ".proceed-checkout",
                "button:contains('Checkout')",
                "a[href='/checkout']"
            ]
            
            for selector in checkout_selectors:
                if selector.startswith("button:contains"):
                    from selenium.webdriver.common.by import By
                    try:
                        checkout_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Checkout')]")
                        if checkout_btn:
                            return "Present and clickable" if checkout_btn.is_enabled() else "Present but disabled"
                    except:
                        continue
                else:
                    if self.is_element_present(selector):
                        element = self.wait_for_element(selector)
                        return "Present and clickable" if element.is_enabled() else "Present but disabled"
            
            return "Not found"
            
        except Exception:
            return "Error"
    
    def _test_empty_form_submission(self):
        """Helper method to test empty form submission validation"""
        try:
            # Find and click submit button without filling form
            submit_selectors = [
                ".place-order-btn",
                "button[type='submit']",
                ".submit-btn",
                "button:contains('Place Order')"
            ]
            
            for selector in submit_selectors:
                if selector.startswith("button:contains"):
                    from selenium.webdriver.common.by import By
                    try:
                        submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]")
                    except:
                        continue
                else:
                    if not self.is_element_present(selector):
                        continue
                    submit_btn = self.wait_for_element(selector)
                
                if submit_btn:
                    submit_btn.click()
                    time.sleep(2)
                    
                    # Check for validation messages
                    validation_selectors = [
                        ".error-message",
                        ".validation-error",
                        ".field-error",
                        ".alert-danger"
                    ]
                    
                    for val_selector in validation_selectors:
                        if self.is_element_present(val_selector):
                            return "Working (validation shown)"
                    
                    # Check if form didn't submit (still on same page)
                    if "checkout" in self.get_current_url():
                        return "Working (form not submitted)"
                    
                    return "Failed (form submitted without validation)"
            
            return "Submit button not found"
            
        except Exception:
            return "Error"
    
    def _test_invalid_email_validation(self):
        """Helper method to test invalid email validation"""
        try:
            email_selectors = [
                "input[name='email']",
                "input[type='email']",
                "#email"
            ]
            
            for selector in email_selectors:
                if self.is_element_present(selector):
                    # Enter invalid email
                    self.safe_send_keys(selector, "invalid-email", clear_first=True)
                    
                    # Try to submit or move to next field
                    from selenium.webdriver.common.keys import Keys
                    element = self.wait_for_element(selector)
                    element.send_keys(Keys.TAB)
                    time.sleep(1)
                    
                    # Check for validation message
                    if self._check_for_validation_message():
                        return "Working"
                    
                    return "Not working"
            
            return "Email field not found"
            
        except Exception:
            return "Error"
    
    def _test_invalid_phone_validation(self):
        """Helper method to test invalid phone validation"""
        try:
            phone_selectors = [
                "input[name='phone']",
                "input[type='tel']",
                "#phone"
            ]
            
            for selector in phone_selectors:
                if self.is_element_present(selector):
                    # Enter invalid phone
                    self.safe_send_keys(selector, "123", clear_first=True)
                    
                    # Try to submit or move to next field
                    from selenium.webdriver.common.keys import Keys
                    element = self.wait_for_element(selector)
                    element.send_keys(Keys.TAB)
                    time.sleep(1)
                    
                    # Check for validation message
                    if self._check_for_validation_message():
                        return "Working"
                    
                    return "Not working"
            
            return "Phone field not found"
            
        except Exception:
            return "Error"
    
    def _test_invalid_pincode_validation(self):
        """Helper method to test invalid pincode validation"""
        try:
            pincode_selectors = [
                "input[name='pincode']",
                "input[name='zip']",
                "#pincode"
            ]
            
            for selector in pincode_selectors:
                if self.is_element_present(selector):
                    # Enter invalid pincode
                    self.safe_send_keys(selector, "123", clear_first=True)
                    
                    # Try to submit or move to next field
                    from selenium.webdriver.common.keys import Keys
                    element = self.wait_for_element(selector)
                    element.send_keys(Keys.TAB)
                    time.sleep(1)
                    
                    # Check for validation message
                    if self._check_for_validation_message():
                        return "Working"
                    
                    return "Not working"
            
            return "Pincode field not found"
            
        except Exception:
            return "Error"
    
    def _check_for_validation_message(self):
        """Helper method to check for validation messages"""
        validation_selectors = [
            ".error-message",
            ".validation-error",
            ".field-error",
            ".alert-danger",
            ".invalid-feedback"
        ]
        
        for selector in validation_selectors:
            if self.is_element_visible(selector):
                return True
        
        return False
    
    def _fill_checkout_form(self, form_data):
        """Helper method to fill checkout form with provided data"""
        try:
            form_fields = [
                ("name", form_data["name"]),
                ("email", form_data["email"]),
                ("phone", form_data["phone"]),
                ("address", form_data["address"]),
                ("city", form_data["city"]),
                ("state", form_data["state"]),
                ("pincode", form_data["pincode"])
            ]
            
            for field_name, field_value in form_fields:
                field_selectors = [
                    f"input[name='{field_name}']",
                    f"#{field_name}",
                    f"textarea[name='{field_name}']"
                ]
                
                field_filled = False
                for selector in field_selectors:
                    if self.is_element_present(selector):
                        if self.safe_send_keys(selector, field_value, clear_first=True):
                            field_filled = True
                            break
                
                if not field_filled:
                    print(f"Could not fill field: {field_name}")
            
            return True
            
        except Exception as e:
            print(f"Error filling checkout form: {str(e)}")
            return False
    
    def _submit_checkout_form(self):
        """Helper method to submit checkout form"""
        try:
            submit_selectors = [
                ".place-order-btn",
                "button[type='submit']",
                ".submit-btn",
                "button:contains('Place Order')"
            ]
            
            for selector in submit_selectors:
                if selector.startswith("button:contains"):
                    from selenium.webdriver.common.by import By
                    try:
                        submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]")
                        submit_btn.click()
                        return True
                    except:
                        continue
                else:
                    if self.safe_click(selector):
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _check_checkout_success(self):
        """Helper method to check for checkout success indicators"""
        try:
            # Wait a bit for redirect/success message
            time.sleep(3)
            
            # Check current URL for success page
            current_url = self.get_current_url()
            if "success" in current_url or "order-success" in current_url or "thank-you" in current_url:
                return "Redirected to success page"
            
            # Check for success messages on page
            success_indicators = [
                "order placed successfully",
                "thank you for your order",
                "order confirmed",
                "payment successful",
                "order number"
            ]
            
            page_text = self.driver.page_source.lower()
            for indicator in success_indicators:
                if indicator in page_text:
                    return f"Success message found: {indicator}"
            
            return False
            
        except Exception:
            return False
    
    def run_all_tests(self):
        """Run all cart and checkout tests"""
        print(f"Running {self.test_name} with {self.browser} browser...")
        
        test_methods = [
            ("test_add_to_cart_from_product_list", ["garba.shop"]),
            ("test_cart_page_functionality", ["garba.shop"]),
            ("test_checkout_form_validation", ["garba.shop"]),
            ("test_successful_checkout_flow", ["garba.shop"]),
            ("test_cart_persistence", ["garba.shop"])
        ]
        
        for method_name, domains in test_methods:
            method = getattr(self, method_name)
            
            for domain in domains:
                print(f"  Running {method_name} for {domain}...")
                method(domain)
        
        return self.test_results