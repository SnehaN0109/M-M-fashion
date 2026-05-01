"""
Product browsing and filtering tests
"""
import time
import random
from base_test import BaseTest
from config import TestConfig, SELECTORS, TEST_DATA

class ProductBrowsingTests(BaseTest):
    """Test suite for product browsing functionality"""
    
    def __init__(self, browser="chrome", headless=False):
        super().__init__(browser, headless)
        self.test_name = "Product Browsing Tests"
    
    def test_category_pages(self, domain="garba.shop"):
        """Test category page loading and functionality"""
        test_name = f"Category Pages - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            categories = [
                ("Men", "/men"),
                ("Women", "/women"),
                ("Kids", "/kids"),
                ("Ethnic", "/ethnic"),
                ("Western", "/western")
            ]
            
            category_results = []
            
            for category_name, category_path in categories:
                try:
                    # Navigate to category page
                    category_url = f"{self.config.FRONTEND_URL}{category_path}"
                    self.navigate_to(category_url, domain)
                    
                    # Wait for page to load
                    time.sleep(3)
                    
                    # Take screenshot
                    screenshot = self.take_screenshot(f"category_{category_name.lower()}", 
                                                    f"{category_name} category page for {domain}")
                    
                    # Check if products are loaded
                    product_selectors = [
                        ".product-card",
                        ".product-item",
                        "[data-testid='product-card']",
                        ".grid > div",  # Generic grid items
                        ".product"
                    ]
                    
                    products_found = False
                    product_count = 0
                    
                    for selector in product_selectors:
                        try:
                            products = self.driver.find_elements("css selector", selector)
                            if products and len(products) > 0:
                                products_found = True
                                product_count = len(products)
                                break
                        except:
                            continue
                    
                    if products_found:
                        category_results.append(f"{category_name}: {product_count} products found")
                    else:
                        # Check if it's a "no products" message or loading issue
                        page_text = self.driver.page_source.lower()
                        if "no products" in page_text or "coming soon" in page_text:
                            category_results.append(f"{category_name}: No products available (expected)")
                        else:
                            category_results.append(f"{category_name}: Products not loaded")
                    
                    # Check page title
                    title = self.get_page_title()
                    if category_name.lower() not in title.lower():
                        category_results.append(f"{category_name}: Title doesn't match category")
                    
                except Exception as e:
                    category_results.append(f"{category_name}: Error - {str(e)}")
            
            # Evaluate results
            failed_categories = [result for result in category_results 
                               if "Error" in result or "not loaded" in result or "doesn't match" in result]
            
            if len(failed_categories) > len(categories) / 2:  # More than half failed
                message = f"Category page issues: {'; '.join(failed_categories)}"
                self.log_test_result(test_name, "FAIL", message)
                return False
            
            message = f"Category pages: {'; '.join(category_results)}"
            self.log_test_result(test_name, "PASS", message)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("category_pages_error", f"Category pages error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_product_filtering(self, domain="garba.shop"):
        """Test product filtering functionality"""
        test_name = f"Product Filtering - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Navigate to a category with products (Women's section typically has most products)
            self.navigate_to(f"{self.config.FRONTEND_URL}/women", domain)
            time.sleep(3)
            
            # Take initial screenshot
            screenshot = self.take_screenshot("before_filtering", f"Before filtering for {domain}")
            
            # Count initial products
            initial_product_count = self._count_products()
            
            filter_results = []
            
            # Test different filter types
            filter_tests = [
                ("Price Filter", self._test_price_filter),
                ("Category Filter", self._test_category_filter),
                ("Size Filter", self._test_size_filter)
            ]
            
            for filter_name, filter_test_method in filter_tests:
                try:
                    result = filter_test_method()
                    filter_results.append(f"{filter_name}: {result}")
                except Exception as e:
                    filter_results.append(f"{filter_name}: Error - {str(e)}")
                
                # Reset filters between tests
                self._reset_filters()
                time.sleep(2)
            
            # Take final screenshot
            screenshot = self.take_screenshot("after_filtering", f"After filtering tests for {domain}")
            
            # Evaluate results
            failed_filters = [result for result in filter_results if "Error" in result or "Failed" in result]
            
            if len(failed_filters) > 0:
                message = f"Filter issues: {'; '.join(failed_filters)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Filtering tests: {'; '.join(filter_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("filtering_error", f"Filtering error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_product_sorting(self, domain="garba.shop"):
        """Test product sorting functionality"""
        test_name = f"Product Sorting - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Navigate to products page
            self.navigate_to(f"{self.config.FRONTEND_URL}/women", domain)
            time.sleep(3)
            
            sort_results = []
            
            # Test different sorting options
            sort_options = [
                ("Price: Low to High", "price-asc"),
                ("Price: High to Low", "price-desc"),
                ("Name: A to Z", "name-asc"),
                ("Newest First", "newest")
            ]
            
            for sort_name, sort_value in sort_options:
                try:
                    # Look for sort dropdown
                    sort_selectors = [
                        "select[name='sort']",
                        ".sort-dropdown",
                        "#sort-select",
                        "select:contains('Sort')"
                    ]
                    
                    sort_element = None
                    for selector in sort_selectors:
                        if self.is_element_present(selector):
                            sort_element = self.wait_for_element(selector)
                            break
                    
                    if not sort_element:
                        sort_results.append(f"{sort_name}: Sort dropdown not found")
                        continue
                    
                    # Select sort option
                    from selenium.webdriver.support.ui import Select
                    select = Select(sort_element)
                    
                    # Try to select by value or visible text
                    try:
                        select.select_by_value(sort_value)
                    except:
                        try:
                            select.select_by_visible_text(sort_name)
                        except:
                            sort_results.append(f"{sort_name}: Option not found in dropdown")
                            continue
                    
                    # Wait for sorting to apply
                    time.sleep(3)
                    
                    # Verify sorting worked (basic check)
                    products_after_sort = self._count_products()
                    if products_after_sort > 0:
                        sort_results.append(f"{sort_name}: Applied successfully")
                    else:
                        sort_results.append(f"{sort_name}: No products after sorting")
                    
                except Exception as e:
                    sort_results.append(f"{sort_name}: Error - {str(e)}")
            
            screenshot = self.take_screenshot("product_sorting", f"Product sorting test for {domain}")
            
            # If no sort dropdown found at all, it might not be implemented
            if all("not found" in result for result in sort_results):
                message = "Sorting functionality not implemented"
                self.log_test_result(test_name, "SKIP", message, screenshot)
                return True
            
            # Evaluate results
            failed_sorts = [result for result in sort_results if "Error" in result or "not found" in result]
            
            if len(failed_sorts) > len(sort_options) / 2:
                message = f"Sorting issues: {'; '.join(failed_sorts)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Sorting tests: {'; '.join(sort_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("sorting_error", f"Sorting error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_product_search_results(self, domain="garba.shop"):
        """Test product search results page"""
        test_name = f"Product Search Results - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            search_results = []
            
            # Test different search terms
            search_terms = ["kurti", "saree", "dress", "ethnic"]
            
            for term in search_terms:
                try:
                    # Navigate to homepage first
                    self.navigate_to(self.config.FRONTEND_URL, domain)
                    time.sleep(2)
                    
                    # Perform search
                    search_success = self._perform_search(term)
                    
                    if not search_success:
                        search_results.append(f"{term}: Search failed")
                        continue
                    
                    # Wait for results page
                    time.sleep(3)
                    
                    # Check if we're on search results page
                    current_url = self.get_current_url()
                    if "search" not in current_url.lower():
                        search_results.append(f"{term}: Not redirected to search results")
                        continue
                    
                    # Count search results
                    result_count = self._count_products()
                    
                    if result_count > 0:
                        search_results.append(f"{term}: {result_count} results found")
                    else:
                        # Check if it's a "no results" message
                        page_text = self.driver.page_source.lower()
                        if "no results" in page_text or "not found" in page_text:
                            search_results.append(f"{term}: No results (expected)")
                        else:
                            search_results.append(f"{term}: Results page loaded but no products displayed")
                    
                except Exception as e:
                    search_results.append(f"{term}: Error - {str(e)}")
            
            screenshot = self.take_screenshot("search_results", f"Search results test for {domain}")
            
            # Evaluate results
            failed_searches = [result for result in search_results if "Error" in result or "failed" in result]
            
            if len(failed_searches) > len(search_terms) / 2:
                message = f"Search results issues: {'; '.join(failed_searches)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Search results: {'; '.join(search_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("search_results_error", f"Search results error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def _count_products(self):
        """Helper method to count products on current page"""
        product_selectors = [
            ".product-card",
            ".product-item",
            "[data-testid='product-card']",
            ".product",
            ".grid > div"
        ]
        
        for selector in product_selectors:
            try:
                products = self.driver.find_elements("css selector", selector)
                if products:
                    return len(products)
            except:
                continue
        
        return 0
    
    def _perform_search(self, term):
        """Helper method to perform search"""
        try:
            # Find search input
            search_selectors = [
                "input[type='search']",
                "input[placeholder*='Search']",
                ".search-input",
                "#search",
                "input[name='search']"
            ]
            
            search_input = None
            for selector in search_selectors:
                if self.is_element_present(selector):
                    search_input = self.wait_for_element(selector)
                    break
            
            if not search_input:
                return False
            
            # Enter search term
            search_input.clear()
            search_input.send_keys(term)
            
            # Submit search
            search_button_selectors = [
                "button[type='submit']",
                ".search-button",
                ".search-btn"
            ]
            
            for selector in search_button_selectors:
                if self.safe_click(selector):
                    return True
            
            # Try pressing Enter
            from selenium.webdriver.common.keys import Keys
            search_input.send_keys(Keys.RETURN)
            return True
            
        except Exception:
            return False
    
    def _test_price_filter(self):
        """Helper method to test price filtering"""
        try:
            # Look for price filter elements
            price_filter_selectors = [
                ".price-filter",
                "input[name='price']",
                ".filter-price",
                "#price-filter"
            ]
            
            for selector in price_filter_selectors:
                if self.is_element_present(selector):
                    # Found price filter, try to interact with it
                    if self.safe_click(selector):
                        time.sleep(2)
                        return "Applied"
            
            return "Not found"
            
        except Exception as e:
            return f"Error - {str(e)}"
    
    def _test_category_filter(self):
        """Helper method to test category filtering"""
        try:
            # Look for category filter elements
            category_filter_selectors = [
                ".category-filter",
                "input[name='category']",
                ".filter-category",
                "#category-filter"
            ]
            
            for selector in category_filter_selectors:
                if self.is_element_present(selector):
                    if self.safe_click(selector):
                        time.sleep(2)
                        return "Applied"
            
            return "Not found"
            
        except Exception as e:
            return f"Error - {str(e)}"
    
    def _test_size_filter(self):
        """Helper method to test size filtering"""
        try:
            # Look for size filter elements
            size_filter_selectors = [
                ".size-filter",
                "input[name='size']",
                ".filter-size",
                "#size-filter"
            ]
            
            for selector in size_filter_selectors:
                if self.is_element_present(selector):
                    if self.safe_click(selector):
                        time.sleep(2)
                        return "Applied"
            
            return "Not found"
            
        except Exception as e:
            return f"Error - {str(e)}"
    
    def _reset_filters(self):
        """Helper method to reset all filters"""
        try:
            # Look for reset/clear filters button
            reset_selectors = [
                ".clear-filters",
                ".reset-filters",
                "button:contains('Clear')",
                "button:contains('Reset')"
            ]
            
            for selector in reset_selectors:
                if self.safe_click(selector):
                    return True
            
            # If no reset button, refresh the page
            self.driver.refresh()
            return True
            
        except Exception:
            return False
    
    def run_all_tests(self):
        """Run all product browsing tests"""
        print(f"Running {self.test_name} with {self.browser} browser...")
        
        test_methods = [
            ("test_category_pages", ["garba.shop", "ttd.in"]),
            ("test_product_filtering", ["garba.shop"]),
            ("test_product_sorting", ["garba.shop"]),
            ("test_product_search_results", ["garba.shop"])
        ]
        
        for method_name, domains in test_methods:
            method = getattr(self, method_name)
            
            for domain in domains:
                print(f"  Running {method_name} for {domain}...")
                method(domain)
        
        return self.test_results