"""
Base test class with common functionality for all Selenium tests
"""
import os
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image
import requests

from config import TestConfig, SELECTORS, TEST_DATA

class BaseTest:
    """Base class for all Selenium tests with common functionality"""
    
    def __init__(self, browser: str = "chrome", headless: bool = False):
        self.config = TestConfig()
        self.browser = browser
        self.headless = headless
        self.driver = None
        self.wait = None
        self.test_results = []
        self.screenshots = []
        self.performance_metrics = {}
        
        # Create directories
        os.makedirs(self.config.SCREENSHOT_DIR, exist_ok=True)
        os.makedirs(self.config.REPORT_DIR, exist_ok=True)
    
    def setup_driver(self, viewport_size: Tuple[int, int] = None):
        """Initialize WebDriver with specified browser and options"""
        viewport_size = viewport_size or self.config.DESKTOP_SIZE
        
        try:
            if self.browser.lower() == "chrome":
                options = ChromeOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument(f"--window-size={viewport_size[0]},{viewport_size[1]}")
                
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                
            elif self.browser.lower() == "firefox":
                options = FirefoxOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument(f"--width={viewport_size[0]}")
                options.add_argument(f"--height={viewport_size[1]}")
                
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
            
            # Set timeouts
            self.driver.implicitly_wait(self.config.IMPLICIT_WAIT)
            self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
            
            # Set window size
            self.driver.set_window_size(*viewport_size)
            
            # Initialize WebDriverWait
            self.wait = WebDriverWait(self.driver, self.config.EXPLICIT_WAIT)
            
            return True
            
        except Exception as e:
            print(f"Failed to setup {self.browser} driver: {str(e)}")
            return False
    
    def teardown_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def navigate_to(self, url: str, domain: str = None) -> bool:
        """Navigate to URL and optionally set domain for testing"""
        try:
            start_time = time.time()
            
            # Set domain in localStorage if specified
            if domain:
                self.driver.get(self.config.FRONTEND_URL)
                self.driver.execute_script(f"localStorage.setItem('test_domain', '{domain}');")
                self.driver.refresh()
            
            self.driver.get(url)
            
            # Record page load time
            load_time = time.time() - start_time
            self.performance_metrics[url] = {
                'load_time': load_time,
                'timestamp': datetime.now().isoformat()
            }
            
            # Wait for page to be ready
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            
            return True
            
        except Exception as e:
            print(f"Failed to navigate to {url}: {str(e)}")
            return False
    
    def take_screenshot(self, name: str, description: str = "") -> str:
        """Take screenshot and save with timestamp"""
        if not self.driver:
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.config.SCREENSHOT_DIR, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            
            # Store screenshot info
            screenshot_info = {
                'filename': filename,
                'filepath': filepath,
                'description': description,
                'timestamp': timestamp,
                'url': self.driver.current_url,
                'viewport_size': self.driver.get_window_size()
            }
            self.screenshots.append(screenshot_info)
            
            return filepath
            
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return ""
    
    def wait_for_element(self, selector: str, timeout: int = None) -> Optional[object]:
        """Wait for element to be present and return it"""
        timeout = timeout or self.config.EXPLICIT_WAIT
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            return None
    
    def wait_for_clickable(self, selector: str, timeout: int = None) -> Optional[object]:
        """Wait for element to be clickable and return it"""
        timeout = timeout or self.config.EXPLICIT_WAIT
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            return None
    
    def safe_click(self, selector: str, timeout: int = None) -> bool:
        """Safely click an element with error handling"""
        try:
            element = self.wait_for_clickable(selector, timeout)
            if element:
                # Scroll element into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)  # Brief pause for scroll
                element.click()
                return True
            return False
        except Exception as e:
            print(f"Failed to click element {selector}: {str(e)}")
            return False
    
    def safe_send_keys(self, selector: str, text: str, clear_first: bool = True) -> bool:
        """Safely send keys to an element"""
        try:
            element = self.wait_for_element(selector)
            if element:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                return True
            return False
        except Exception as e:
            print(f"Failed to send keys to {selector}: {str(e)}")
            return False
    
    def get_element_text(self, selector: str) -> str:
        """Get text content of an element"""
        try:
            element = self.wait_for_element(selector)
            return element.text if element else ""
        except Exception:
            return ""
    
    def is_element_present(self, selector: str) -> bool:
        """Check if element is present on the page"""
        try:
            self.driver.find_element(By.CSS_SELECTOR, selector)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible on the page"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def scroll_to_element(self, selector: str) -> bool:
        """Scroll to an element"""
        try:
            element = self.wait_for_element(selector)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                return True
            return False
        except Exception:
            return False
    
    def hover_over_element(self, selector: str) -> bool:
        """Hover over an element"""
        try:
            element = self.wait_for_element(selector)
            if element:
                ActionChains(self.driver).move_to_element(element).perform()
                return True
            return False
        except Exception:
            return False
    
    def switch_domain(self, domain: str) -> bool:
        """Switch to different domain for testing"""
        try:
            self.driver.execute_script(f"localStorage.setItem('test_domain', '{domain}');")
            self.driver.refresh()
            time.sleep(2)  # Wait for domain switch to take effect
            return True
        except Exception as e:
            print(f"Failed to switch domain to {domain}: {str(e)}")
            return False
    
    def measure_page_load_time(self, url: str) -> float:
        """Measure page load time"""
        start_time = time.time()
        self.driver.get(url)
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        return time.time() - start_time
    
    def check_api_response_time(self, endpoint: str) -> float:
        """Check API response time"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.config.BACKEND_URL}{endpoint}")
            response_time = time.time() - start_time
            return response_time
        except Exception:
            return -1
    
    def log_test_result(self, test_name: str, status: str, message: str = "", screenshot_path: str = ""):
        """Log test result"""
        result = {
            'test_name': test_name,
            'status': status,  # PASS, FAIL, SKIP
            'message': message,
            'screenshot': screenshot_path,
            'timestamp': datetime.now().isoformat(),
            'browser': self.browser,
            'url': self.driver.current_url if self.driver else ""
        }
        self.test_results.append(result)
    
    def get_console_logs(self) -> List[Dict]:
        """Get browser console logs"""
        try:
            logs = self.driver.get_log('browser')
            return logs
        except Exception:
            return []
    
    def check_for_js_errors(self) -> List[str]:
        """Check for JavaScript errors in console"""
        errors = []
        try:
            logs = self.get_console_logs()
            for log in logs:
                if log['level'] == 'SEVERE':
                    errors.append(log['message'])
        except Exception:
            pass
        return errors
    
    def wait_for_page_load(self, timeout: int = None) -> bool:
        """Wait for page to fully load"""
        timeout = timeout or self.config.PAGE_LOAD_TIMEOUT
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            return False
    
    def get_current_url(self) -> str:
        """Get current URL"""
        return self.driver.current_url if self.driver else ""
    
    def get_page_title(self) -> str:
        """Get page title"""
        return self.driver.title if self.driver else ""