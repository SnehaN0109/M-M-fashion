"""
Performance and cross-browser testing
"""
import time
import statistics
from base_test import BaseTest
from config import TestConfig

class PerformanceTests(BaseTest):
    """Test suite for performance and cross-browser testing"""
    
    def __init__(self, browser="chrome", headless=False):
        super().__init__(browser, headless)
        self.test_name = "Performance Tests"
    
    def test_page_load_performance(self, domain="garba.shop"):
        """Test page load performance across different pages"""
        test_name = f"Page Load Performance - {domain} - {self.browser}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Pages to test
            pages_to_test = [
                ("Homepage", f"{self.config.FRONTEND_URL}/"),
                ("Men Category", f"{self.config.FRONTEND_URL}/men"),
                ("Women Category", f"{self.config.FRONTEND_URL}/women"),
                ("Cart Page", f"{self.config.FRONTEND_URL}/cart"),
                ("Checkout Page", f"{self.config.FRONTEND_URL}/checkout")
            ]
            
            performance_results = []
            all_load_times = []
            
            for page_name, page_url in pages_to_test:
                try:
                    # Measure load time multiple times for accuracy
                    load_times = []
                    
                    for i in range(3):  # Test each page 3 times
                        load_time = self.measure_page_load_time(page_url)
                        load_times.append(load_time)
                        time.sleep(1)  # Brief pause between tests
                    
                    avg_load_time = statistics.mean(load_times)
                    all_load_times.extend(load_times)
                    
                    if avg_load_time <= self.config.MAX_PAGE_LOAD_TIME:
                        performance_results.append(f"{page_name}: {avg_load_time:.2f}s (PASS)")
                    else:
                        performance_results.append(f"{page_name}: {avg_load_time:.2f}s (SLOW)")
                
                except Exception as e:
                    performance_results.append(f"{page_name}: Error - {str(e)}")
            
            # Calculate overall statistics
            if all_load_times:
                avg_overall = statistics.mean(all_load_times)
                max_load_time = max(all_load_times)
                min_load_time = min(all_load_times)
            else:
                avg_overall = max_load_time = min_load_time = 0
            
            screenshot = self.take_screenshot("performance_test", f"Performance test for {domain} on {self.browser}")
            
            # Evaluate results
            slow_pages = [result for result in performance_results if "SLOW" in result]
            error_pages = [result for result in performance_results if "Error" in result]
            
            if len(slow_pages) > len(pages_to_test) / 2 or len(error_pages) > 0:
                message = f"Performance issues - Avg: {avg_overall:.2f}s, Max: {max_load_time:.2f}s. Issues: {'; '.join(slow_pages + error_pages)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Performance good - Avg: {avg_overall:.2f}s, Max: {max_load_time:.2f}s, Min: {min_load_time:.2f}s. Results: {'; '.join(performance_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("performance_error", f"Performance test error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_api_response_times(self, domain="garba.shop"):
        """Test API response times"""
        test_name = f"API Response Times - {domain}"
        
        # API endpoints to test
        api_endpoints = [
            "/api/products",
            "/api/categories",
            "/api/cart",
            "/health"
        ]
        
        api_results = []
        
        for endpoint in api_endpoints:
            try:
                response_time = self.check_api_response_time(endpoint)
                
                if response_time == -1:
                    api_results.append(f"{endpoint}: Error/Not Found")
                elif response_time <= self.config.MAX_API_RESPONSE_TIME:
                    api_results.append(f"{endpoint}: {response_time:.3f}s (PASS)")
                else:
                    api_results.append(f"{endpoint}: {response_time:.3f}s (SLOW)")
            
            except Exception as e:
                api_results.append(f"{endpoint}: Exception - {str(e)}")
        
        # Evaluate results
        slow_apis = [result for result in api_results if "SLOW" in result]
        error_apis = [result for result in api_results if "Error" in result or "Exception" in result]
        
        if len(slow_apis) > 0 or len(error_apis) > len(api_endpoints) / 2:
            message = f"API performance issues: {'; '.join(slow_apis + error_apis)}"
            self.log_test_result(test_name, "FAIL", message)
            return False
        
        message = f"API performance good: {'; '.join(api_results)}"
        self.log_test_result(test_name, "PASS", message)
        return True
    
    def test_memory_usage(self, domain="garba.shop"):
        """Test memory usage during browsing session"""
        test_name = f"Memory Usage - {domain} - {self.browser}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Navigate through multiple pages to test memory usage
            pages_to_visit = [
                f"{self.config.FRONTEND_URL}/",
                f"{self.config.FRONTEND_URL}/men",
                f"{self.config.FRONTEND_URL}/women",
                f"{self.config.FRONTEND_URL}/kids",
                f"{self.config.FRONTEND_URL}/ethnic"
            ]
            
            memory_results = []
            
            for page_url in pages_to_visit:
                try:
                    self.navigate_to(page_url, domain)
                    time.sleep(3)
                    
                    # Get memory usage (if available)
                    try:
                        memory_info = self.driver.execute_script("""
                            if (performance.memory) {
                                return {
                                    used: performance.memory.usedJSHeapSize,
                                    total: performance.memory.totalJSHeapSize,
                                    limit: performance.memory.jsHeapSizeLimit
                                };
                            }
                            return null;
                        """)
                        
                        if memory_info:
                            used_mb = memory_info['used'] / (1024 * 1024)
                            total_mb = memory_info['total'] / (1024 * 1024)
                            memory_results.append(f"{page_url.split('/')[-1] or 'home'}: {used_mb:.1f}MB used, {total_mb:.1f}MB total")
                        else:
                            memory_results.append(f"{page_url.split('/')[-1] or 'home'}: Memory info not available")
                    
                    except Exception:
                        memory_results.append(f"{page_url.split('/')[-1] or 'home'}: Memory check failed")
                
                except Exception as e:
                    memory_results.append(f"{page_url.split('/')[-1] or 'home'}: Navigation error - {str(e)}")
            
            screenshot = self.take_screenshot("memory_usage", f"Memory usage test for {domain}")
            
            # Check for memory leaks (basic check)
            memory_leak_detected = False
            if len(memory_results) > 2:
                # Simple heuristic: if memory usage increases significantly
                try:
                    first_memory = float(memory_results[0].split(': ')[1].split('MB')[0])
                    last_memory = float(memory_results[-1].split(': ')[1].split('MB')[0])
                    
                    if last_memory > first_memory * 2:  # Memory doubled
                        memory_leak_detected = True
                except:
                    pass
            
            if memory_leak_detected:
                message = f"Potential memory leak detected: {'; '.join(memory_results)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Memory usage normal: {'; '.join(memory_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("memory_usage_error", f"Memory usage error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_javascript_errors(self, domain="garba.shop"):
        """Test for JavaScript errors across different pages"""
        test_name = f"JavaScript Errors - {domain} - {self.browser}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            pages_to_test = [
                ("Homepage", f"{self.config.FRONTEND_URL}/"),
                ("Category Page", f"{self.config.FRONTEND_URL}/women"),
                ("Cart Page", f"{self.config.FRONTEND_URL}/cart")
            ]
            
            js_error_results = []
            total_errors = 0
            
            for page_name, page_url in pages_to_test:
                try:
                    self.navigate_to(page_url, domain)
                    time.sleep(3)
                    
                    # Check for JavaScript errors
                    js_errors = self.check_for_js_errors()
                    
                    if js_errors:
                        error_count = len(js_errors)
                        total_errors += error_count
                        js_error_results.append(f"{page_name}: {error_count} errors")
                    else:
                        js_error_results.append(f"{page_name}: No errors")
                
                except Exception as e:
                    js_error_results.append(f"{page_name}: Check failed - {str(e)}")
            
            screenshot = self.take_screenshot("js_errors", f"JavaScript errors test for {domain}")
            
            # Evaluate results
            if total_errors > 5:  # More than 5 total errors is concerning
                message = f"Too many JavaScript errors ({total_errors} total): {'; '.join(js_error_results)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            if total_errors > 0:
                message = f"Some JavaScript errors found ({total_errors} total): {'; '.join(js_error_results)}"
                self.log_test_result(test_name, "PASS", message, screenshot)
            else:
                message = f"No JavaScript errors found: {'; '.join(js_error_results)}"
                self.log_test_result(test_name, "PASS", message, screenshot)
            
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("js_errors_test_error", f"JS errors test error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def test_responsive_performance(self, domain="garba.shop"):
        """Test performance across different viewport sizes"""
        test_name = f"Responsive Performance - {domain} - {self.browser}"
        
        viewports = [
            ("Desktop", self.config.DESKTOP_SIZE),
            ("Tablet", self.config.TABLET_SIZE),
            ("Mobile", self.config.MOBILE_SIZE)
        ]
        
        responsive_perf_results = []
        
        for viewport_name, viewport_size in viewports:
            if not self.setup_driver(viewport_size):
                responsive_perf_results.append(f"{viewport_name}: Driver setup failed")
                continue
            
            try:
                # Test homepage load time on this viewport
                load_time = self.measure_page_load_time(f"{self.config.FRONTEND_URL}/")
                
                if load_time <= self.config.MAX_PAGE_LOAD_TIME:
                    responsive_perf_results.append(f"{viewport_name}: {load_time:.2f}s (PASS)")
                else:
                    responsive_perf_results.append(f"{viewport_name}: {load_time:.2f}s (SLOW)")
                
                # Take screenshot
                screenshot = self.take_screenshot(f"responsive_perf_{viewport_name.lower()}", 
                                                f"Responsive performance {viewport_name} for {domain}")
            
            except Exception as e:
                responsive_perf_results.append(f"{viewport_name}: Error - {str(e)}")
            
            finally:
                self.teardown_driver()
        
        # Evaluate results
        slow_viewports = [result for result in responsive_perf_results if "SLOW" in result]
        error_viewports = [result for result in responsive_perf_results if "Error" in result or "failed" in result]
        
        if len(slow_viewports) > 0 or len(error_viewports) > 0:
            message = f"Responsive performance issues: {'; '.join(slow_viewports + error_viewports)}"
            self.log_test_result(test_name, "FAIL", message)
            return False
        
        message = f"Responsive performance good: {'; '.join(responsive_perf_results)}"
        self.log_test_result(test_name, "PASS", message)
        return True
    
    def test_concurrent_user_simulation(self, domain="garba.shop"):
        """Simulate concurrent user actions"""
        test_name = f"Concurrent User Simulation - {domain}"
        
        # This is a simplified simulation since we're using a single browser instance
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Failed to setup driver")
            return False
        
        try:
            # Simulate rapid navigation and actions
            actions = [
                ("Navigate to homepage", lambda: self.navigate_to(f"{self.config.FRONTEND_URL}/", domain)),
                ("Search for products", lambda: self._simulate_search("kurti")),
                ("Navigate to category", lambda: self.navigate_to(f"{self.config.FRONTEND_URL}/women", domain)),
                ("Navigate to cart", lambda: self.navigate_to(f"{self.config.FRONTEND_URL}/cart", domain)),
                ("Navigate back to homepage", lambda: self.navigate_to(f"{self.config.FRONTEND_URL}/", domain))
            ]
            
            concurrent_results = []
            start_time = time.time()
            
            for action_name, action_func in actions:
                try:
                    action_start = time.time()
                    action_func()
                    action_time = time.time() - action_start
                    
                    if action_time <= 5.0:  # Each action should complete within 5 seconds
                        concurrent_results.append(f"{action_name}: {action_time:.2f}s (PASS)")
                    else:
                        concurrent_results.append(f"{action_name}: {action_time:.2f}s (SLOW)")
                
                except Exception as e:
                    concurrent_results.append(f"{action_name}: Error - {str(e)}")
            
            total_time = time.time() - start_time
            
            screenshot = self.take_screenshot("concurrent_simulation", f"Concurrent user simulation for {domain}")
            
            # Evaluate results
            slow_actions = [result for result in concurrent_results if "SLOW" in result]
            error_actions = [result for result in concurrent_results if "Error" in result]
            
            if len(slow_actions) > 0 or len(error_actions) > 0:
                message = f"Concurrent user issues (Total: {total_time:.2f}s): {'; '.join(slow_actions + error_actions)}"
                self.log_test_result(test_name, "FAIL", message, screenshot)
                return False
            
            message = f"Concurrent user simulation successful (Total: {total_time:.2f}s): {'; '.join(concurrent_results)}"
            self.log_test_result(test_name, "PASS", message, screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("concurrent_simulation_error", f"Concurrent simulation error for {domain}")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
    
    def _simulate_search(self, term):
        """Helper method to simulate search action"""
        try:
            # Find search input
            search_selectors = [
                "input[type='search']",
                "input[placeholder*='Search']",
                ".search-input"
            ]
            
            for selector in search_selectors:
                if self.is_element_present(selector):
                    self.safe_send_keys(selector, term)
                    
                    # Try to submit
                    from selenium.webdriver.common.keys import Keys
                    element = self.wait_for_element(selector)
                    element.send_keys(Keys.RETURN)
                    time.sleep(2)
                    return True
            
            return False
            
        except Exception:
            return False
    
    def run_all_tests(self):
        """Run all performance tests"""
        print(f"Running {self.test_name} with {self.browser} browser...")
        
        test_methods = [
            ("test_page_load_performance", ["garba.shop"]),
            ("test_api_response_times", ["garba.shop"]),
            ("test_memory_usage", ["garba.shop"]),
            ("test_javascript_errors", ["garba.shop"]),
            ("test_responsive_performance", ["garba.shop"]),
            ("test_concurrent_user_simulation", ["garba.shop"])
        ]
        
        for method_name, domains in test_methods:
            method = getattr(self, method_name)
            
            if method_name == "test_api_response_times":
                # API tests don't need domain parameter
                print(f"  Running {method_name}...")
                method(domains[0])
            else:
                for domain in domains:
                    print(f"  Running {method_name} for {domain}...")
                    method(domain)
        
        return self.test_results