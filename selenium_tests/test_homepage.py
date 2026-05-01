"""
Homepage functionality tests
"""
import time
from base_test import BaseTest
from config import TestConfig, SELECTORS

class HomepageTests(BaseTest):
    """Test suite for homepage functionality"""
    
    def __init__(self, browser="chrome", headless=False):
        super().__init__(browser, headless)
        self.test_name = "Homepage Tests"
    
    def test_homepage_load(self, domain="garba.shop"):
        """Test homepage loads correctly"""
        test_name = f"Homepage Load - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Navigate to homepage with domain
            success = self.navigate_to(self.config.FRONTEND_URL, domain)
            if not success:
                self.log_test_result(test_name, "FAIL", "Failed to navigate to homepage")
                return False
            
            # Take screenshot
            screenshot = self.take_screenshot("homepage_load", f"Homepage loaded for {domain}")
            
            # Check page title
            title = self.get_page_title()
            if not title:
                self.log_test_result(test_name, "FAIL", "Page title is empty", screenshot)
                return False
            
            # Check for essential elements
            essential_elements = [
                ("header", "header"),
                ("navigation", "nav, .navigation"),
                ("main content", "main, .main-content"),
                ("footer", "footer")
            ]
            
            missing_elements = []
            for element_name, selector in essential_elements:
                if not self.is_element_present(selector):
                    missing_elements.append(element_name)
            
            if missing_elements:
                message = f"Missing elements: {', '.join(missing_elements)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            # Check for JavaScript errors
            js_errors = self.check_for_js_errors()
            if js_errors:
                message = f"JavaScript errors found: {'; '.join(js_errors[:3])}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            # Check page load performance
            load_time = self.performance_metrics.get(self.config.FRONTEND_URL, {}).get('load_time', 0)
            if load_time > self.config.MAX_PAGE_LOAD_TIME:
                message = f"Page load time ({load_time:.2f}s) exceeds threshold ({self.config.MAX_PAGE_LOAD_TIME}s)"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            self.log_test_result(test_name, "PASS", f"Homepage loaded successfully in {load_time:.2f}s", screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("homepage_load_error", f"Error loading homepage for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_navigation_menu(self, domain="garba.shop"):
        """Test navigation menu functionality"""
        test_name = f"Navigation Menu - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Navigate to homepage
            self.navigate_to(self.config.FRONTEND_URL, domain)
            
            # Test navigation links
            nav_links = [
                ("Men", "/men"),
                ("Women", "/women"),
                ("Kids", "/kids"),
                ("Ethnic", "/ethnic"),
                ("Western", "/western")
            ]
            
            failed_links = []
            for link_text, expected_path in nav_links:
                try:
                    # Find and click navigation link
                    link_selector = f"a[href='{expected_path}'], a:contains('{link_text}')"
                    
                    # Try multiple selectors
                    link_found = False
                    for selector in [f"a[href='{expected_path}']", f"//a[contains(text(), '{link_text}')]"]:
                        if selector.startswith("//"):
                            # XPath selector
                            try:
                                from selenium.webdriver.common.by import By
                                element = self.driver.find_element(By.XPATH, selector)
                                if element:
                                    link_found = True
                                    break
                            except:
                                continue
                        else:
                            # CSS selector
                            if self.is_element_present(selector):
                                link_found = True
                                break
                    
                    if not link_found:
                        failed_links.append(f"{link_text} (not found)")
                        continue
                    
                    # Click the link
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                        element.click()
                    else:
                        self.safe_click(selector)
                    
                    # Wait for page to load
                    time.sleep(2)
                    
                    # Check if URL changed correctly
                    current_url = self.get_current_url()
                    if expected_path not in current_url:
                        failed_links.append(f"{link_text} (wrong URL: {current_url})")
                    
                    # Go back to homepage
                    self.navigate_to(self.config.FRONTEND_URL, domain)
                    time.sleep(1)
                    
                except Exception as e:
                    failed_links.append(f"{link_text} (error: {str(e)})")
            
            screenshot = self.take_screenshot("navigation_menu", f"Navigation menu test for {domain}")
            
            if failed_links:
                message = f"Failed navigation links: {'; '.join(failed_links)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            self.log_test_result(test_name, "PASS", "All navigation links working correctly", screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("navigation_error", f"Navigation menu error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_search_functionality(self, domain="garba.shop"):
        """Test search functionality"""
        test_name = f"Search Functionality - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Navigate to homepage
            self.navigate_to(self.config.FRONTEND_URL, domain)
            
            # Test search with different terms
            search_terms = ["kurti", "saree", "dress", "shirt"]
            search_results = []
            
            for term in search_terms:
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
                        search_results.append(f"{term}: Search input not found")
                        continue
                    
                    # Clear and enter search term
                    search_input.clear()
                    search_input.send_keys(term)
                    
                    # Find and click search button
                    search_button_selectors = [
                        "button[type='submit']",
                        ".search-button",
                        ".search-btn",
                        "button:contains('Search')"
                    ]
                    
                    search_clicked = False
                    for selector in search_button_selectors:
                        if self.safe_click(selector):
                            search_clicked = True
                            break
                    
                    if not search_clicked:
                        # Try pressing Enter
                        from selenium.webdriver.common.keys import Keys
                        search_input.send_keys(Keys.RETURN)
                    
                    # Wait for results
                    time.sleep(3)
                    
                    # Check if we're on search results page
                    current_url = self.get_current_url()
                    if "search" in current_url.lower() or "results" in current_url.lower():
                        search_results.append(f"{term}: Success")
                    else:
                        search_results.append(f"{term}: No redirect to search results")
                    
                    # Go back to homepage
                    self.navigate_to(self.config.FRONTEND_URL, domain)
                    time.sleep(1)
                    
                except Exception as e:
                    search_results.append(f"{term}: Error - {str(e)}")
            
            screenshot = self.take_screenshot("search_functionality", f"Search test for {domain}")
            
            # Check results
            failed_searches = [result for result in search_results if "Success" not in result]
            
            if len(failed_searches) > len(search_terms) / 2:  # More than half failed
                message = f"Search failures: {'; '.join(failed_searches)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Search results: {'; '.join(search_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("search_error", f"Search functionality error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_responsive_design(self, domain="garba.shop"):
        """Test responsive design on different viewport sizes"""
        test_name = f"Responsive Design - {domain}"
        
        viewports = [
            ("Desktop", self.config.DESKTOP_SIZE),
            ("Tablet", self.config.TABLET_SIZE),
            ("Mobile", self.config.MOBILE_SIZE)
        ]
        
        responsive_results = []
        
        for viewport_name, viewport_size in viewports:
            if not self.setup_driver(viewport_size):
                responsive_results.append(f"{viewport_name}: Driver setup failed")
                continue
            
            try:
                # Navigate to homepage
                self.navigate_to(self.config.FRONTEND_URL, domain)
                
                # Take screenshot
                screenshot = self.take_screenshot(f"responsive_{viewport_name.lower()}", 
                                                f"{viewport_name} view for {domain}")
                
                # Check if essential elements are visible
                essential_elements = [
                    "header",
                    "nav, .navigation",
                    "main, .main-content"
                ]
                
                visible_elements = 0
                for selector in essential_elements:
                    if self.is_element_visible(selector):
                        visible_elements += 1
                
                if visible_elements >= len(essential_elements) * 0.8:  # 80% of elements visible
                    responsive_results.append(f"{viewport_name}: Pass")
                else:
                    responsive_results.append(f"{viewport_name}: Only {visible_elements}/{len(essential_elements)} elements visible")
                
            except Exception as e:
                responsive_results.append(f"{viewport_name}: Error - {str(e)}")
            
            finally:
                self.teardown_driver()
        
        # Evaluate results
        failed_viewports = [result for result in responsive_results if "Pass" not in result]
        
        if len(failed_viewports) > 0:
            message = f"Responsive issues: {'; '.join(failed_viewports)}"
            self.log_test_result(test_name, "FAIL", message)
            return False
        
        message = f"Responsive design working: {'; '.join(responsive_results)}"
        self.log_test_result(test_name, "PASS", message)
        return True
    
    def test_domain_switching(self):
        """Test switching between B2C and B2B domains"""
        test_name = "Domain Switching"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            domains_to_test = [
                ("B2C", self.config.B2C_DOMAIN),
                ("B2B", self.config.B2B_DOMAIN)
            ]
            
            domain_results = []
            
            for domain_type, domain in domains_to_test:
                try:
                    # Navigate with domain
                    self.navigate_to(self.config.FRONTEND_URL, domain)
                    
                    # Take screenshot
                    screenshot = self.take_screenshot(f"domain_{domain_type.lower()}", 
                                                    f"{domain_type} domain view")
                    
                    # Check if domain-specific elements are present
                    page_content = self.driver.page_source.lower()
                    
                    if domain == self.config.B2C_DOMAIN:
                        # Check for B2C specific content
                        if "garba" in page_content or "premium" in page_content:
                            domain_results.append(f"{domain_type}: Correct branding detected")
                        else:
                            domain_results.append(f"{domain_type}: B2C branding not detected")
                    
                    elif domain == self.config.B2B_DOMAIN:
                        # Check for B2B specific content
                        if "ttd" in page_content or "wholesale" in page_content:
                            domain_results.append(f"{domain_type}: Correct branding detected")
                        else:
                            domain_results.append(f"{domain_type}: B2B branding not detected")
                    
                    time.sleep(2)
                    
                except Exception as e:
                    domain_results.append(f"{domain_type}: Error - {str(e)}")
            
            screenshot = self.take_screenshot("domain_switching", "Domain switching test")
            
            # Check results
            failed_domains = [result for result in domain_results if "Error" in result or "not detected" in result]
            
            if failed_domains:
                message = f"Domain switching issues: {'; '.join(failed_domains)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Domain switching working: {'; '.join(domain_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("domain_switching_error", "Domain switching error")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def run_all_tests(self):
        """Run all homepage tests"""
        print(f"Running {self.test_name} with {self.browser} browser...")
        
        test_methods = [
            ("test_homepage_load", ["garba.shop", "ttd.in"]),
            ("test_navigation_menu", ["garba.shop", "ttd.in"]),
            ("test_search_functionality", ["garba.shop"]),
            ("test_responsive_design", ["garba.shop"]),
            ("test_domain_switching", [])
        ]
        
        for method_name, domains in test_methods:
            method = getattr(self, method_name)
            
            if domains:
                for domain in domains:
                    print(f"  Running {method_name} for {domain}...")
                    method(domain)
            else:
                print(f"  Running {method_name}...")
                method()
        
        return self.test_results