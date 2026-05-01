"""
Main test runner for M&M Fashion Selenium test suite
"""
import os
import sys
import time
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import test classes
from test_homepage import HomepageTests
from test_product_browsing import ProductBrowsingTests
from test_product_detail import ProductDetailTests
from test_cart_checkout import CartCheckoutTests
from test_performance import PerformanceTests
from config import TestConfig

class TestRunner:
    """Main test runner class"""
    
    def __init__(self):
        self.config = TestConfig()
        self.all_results = []
        self.test_summary = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'skipped_tests': 0,
            'start_time': None,
            'end_time': None,
            'duration': 0,
            'browsers_tested': [],
            'domains_tested': []
        }
        
        # Create output directories
        os.makedirs(self.config.SCREENSHOT_DIR, exist_ok=True)
        os.makedirs(self.config.REPORT_DIR, exist_ok=True)
    
    def run_single_browser_tests(self, browser, headless=False):
        """Run all tests for a single browser"""
        print(f"\n{'='*60}")
        print(f"Running tests for {browser.upper()} browser")
        print(f"{'='*60}")
        
        # Test classes to run
        test_classes = [
            HomepageTests,
            ProductBrowsingTests,
            ProductDetailTests,
            CartCheckoutTests,
            PerformanceTests
        ]
        
        browser_results = []
        
        for test_class in test_classes:
            try:
                print(f"\nRunning {test_class.__name__}...")
                test_instance = test_class(browser=browser, headless=headless)
                results = test_instance.run_all_tests()
                browser_results.extend(results)
                
                # Add browser info to results
                for result in results:
                    result['browser'] = browser
                
            except Exception as e:
                print(f"Error running {test_class.__name__}: {str(e)}")
                error_result = {
                    'test_name': f"{test_class.__name__} - Setup Error",
                    'status': 'FAIL',
                    'message': f"Failed to initialize test class: {str(e)}",
                    'browser': browser,
                    'timestamp': datetime.now().isoformat()
                }
                browser_results.append(error_result)
        
        return browser_results
    
    def run_cross_browser_tests(self, browsers=None, headless=False):
        """Run tests across multiple browsers"""
        browsers = browsers or self.config.BROWSERS
        
        print(f"Starting cross-browser testing with browsers: {', '.join(browsers)}")
        print(f"Headless mode: {headless}")
        
        self.test_summary['start_time'] = datetime.now()
        self.test_summary['browsers_tested'] = browsers
        
        all_browser_results = []
        
        # Run tests for each browser sequentially (to avoid resource conflicts)
        for browser in browsers:
            try:
                browser_results = self.run_single_browser_tests(browser, headless)
                all_browser_results.extend(browser_results)
            except Exception as e:
                print(f"Critical error testing {browser}: {str(e)}")
        
        self.all_results = all_browser_results
        self.test_summary['end_time'] = datetime.now()
        self.test_summary['duration'] = (self.test_summary['end_time'] - self.test_summary['start_time']).total_seconds()
        
        # Calculate summary statistics
        self._calculate_test_summary()
        
        return all_browser_results
    
    def run_smoke_tests(self, browser="chrome", headless=True):
        """Run a quick smoke test suite"""
        print(f"\n{'='*60}")
        print(f"Running SMOKE TESTS for {browser.upper()} browser")
        print(f"{'='*60}")
        
        self.test_summary['start_time'] = datetime.now()
        self.test_summary['browsers_tested'] = [browser]
        
        smoke_results = []
        
        # Run essential tests only
        essential_tests = [
            (HomepageTests, "test_homepage_load"),
            (ProductBrowsingTests, "test_category_pages"),
            (ProductDetailTests, "test_product_detail_page_load"),
            (CartCheckoutTests, "test_add_to_cart_from_product_list"),
            (PerformanceTests, "test_page_load_performance")
        ]
        
        for test_class, test_method in essential_tests:
            try:
                print(f"Running {test_class.__name__}.{test_method}...")
                test_instance = test_class(browser=browser, headless=headless)
                
                # Run specific test method
                method = getattr(test_instance, test_method)
                result = method("garba.shop")  # Test with B2C domain
                
                # Create result entry
                test_result = {
                    'test_name': f"{test_class.__name__}.{test_method}",
                    'status': 'PASS' if result else 'FAIL',
                    'message': 'Smoke test completed',
                    'browser': browser,
                    'timestamp': datetime.now().isoformat()
                }
                smoke_results.append(test_result)
                
            except Exception as e:
                print(f"Error in smoke test {test_class.__name__}.{test_method}: {str(e)}")
                error_result = {
                    'test_name': f"{test_class.__name__}.{test_method}",
                    'status': 'FAIL',
                    'message': f"Smoke test error: {str(e)}",
                    'browser': browser,
                    'timestamp': datetime.now().isoformat()
                }
                smoke_results.append(error_result)
        
        self.all_results = smoke_results
        self.test_summary['end_time'] = datetime.now()
        self.test_summary['duration'] = (self.test_summary['end_time'] - self.test_summary['start_time']).total_seconds()
        
        self._calculate_test_summary()
        
        return smoke_results
    
    def _calculate_test_summary(self):
        """Calculate test summary statistics"""
        self.test_summary['total_tests'] = len(self.all_results)
        self.test_summary['passed_tests'] = len([r for r in self.all_results if r['status'] == 'PASS'])
        self.test_summary['failed_tests'] = len([r for r in self.all_results if r['status'] == 'FAIL'])
        self.test_summary['skipped_tests'] = len([r for r in self.all_results if r['status'] == 'SKIP'])
        
        # Extract domains tested
        domains = set()
        for result in self.all_results:
            if 'garba.shop' in result.get('test_name', ''):
                domains.add('garba.shop')
            if 'ttd.in' in result.get('test_name', ''):
                domains.add('ttd.in')
        
        self.test_summary['domains_tested'] = list(domains)
    
    def generate_json_report(self):
        """Generate JSON test report"""
        report_data = {
            'summary': self.test_summary,
            'results': self.all_results,
            'config': {
                'frontend_url': self.config.FRONTEND_URL,
                'backend_url': self.config.BACKEND_URL,
                'max_page_load_time': self.config.MAX_PAGE_LOAD_TIME,
                'max_api_response_time': self.config.MAX_API_RESPONSE_TIME
            }
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.config.REPORT_DIR, f"test_report_{timestamp}.json")
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"JSON report generated: {report_file}")
        return report_file
    
    def generate_html_report(self):
        """Generate HTML test report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.config.REPORT_DIR, f"test_report_{timestamp}.html")
        
        # Calculate pass rate
        pass_rate = (self.test_summary['passed_tests'] / max(self.test_summary['total_tests'], 1)) * 100
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>M&M Fashion - Selenium Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .summary {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .summary-item {{ text-align: center; padding: 10px; background-color: #e9e9e9; border-radius: 5px; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        .skip {{ color: orange; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .status-PASS {{ background-color: #d4edda; }}
        .status-FAIL {{ background-color: #f8d7da; }}
        .status-SKIP {{ background-color: #fff3cd; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>M&M Fashion - Selenium Test Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p><strong>Duration:</strong> {self.test_summary['duration']:.2f} seconds</p>
        <p><strong>Browsers:</strong> {', '.join(self.test_summary['browsers_tested'])}</p>
        <p><strong>Domains:</strong> {', '.join(self.test_summary['domains_tested'])}</p>
    </div>
    
    <div class="summary">
        <div class="summary-item">
            <h3>Total Tests</h3>
            <p style="font-size: 24px; font-weight: bold;">{self.test_summary['total_tests']}</p>
        </div>
        <div class="summary-item">
            <h3 class="pass">Passed</h3>
            <p style="font-size: 24px; font-weight: bold;" class="pass">{self.test_summary['passed_tests']}</p>
        </div>
        <div class="summary-item">
            <h3 class="fail">Failed</h3>
            <p style="font-size: 24px; font-weight: bold;" class="fail">{self.test_summary['failed_tests']}</p>
        </div>
        <div class="summary-item">
            <h3 class="skip">Skipped</h3>
            <p style="font-size: 24px; font-weight: bold;" class="skip">{self.test_summary['skipped_tests']}</p>
        </div>
        <div class="summary-item">
            <h3>Pass Rate</h3>
            <p style="font-size: 24px; font-weight: bold;">{pass_rate:.1f}%</p>
        </div>
    </div>
    
    <h2>Test Results</h2>
    <table>
        <thead>
            <tr>
                <th>Test Name</th>
                <th>Status</th>
                <th>Browser</th>
                <th>Message</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for result in self.all_results:
            html_content += f"""
            <tr class="status-{result['status']}">
                <td>{result['test_name']}</td>
                <td>{result['status']}</td>
                <td>{result.get('browser', 'N/A')}</td>
                <td>{result.get('message', '')}</td>
                <td>{result['timestamp']}</td>
            </tr>
"""
        
        html_content += """
        </tbody>
    </table>
</body>
</html>
"""
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        print(f"HTML report generated: {report_file}")
        return report_file
    
    def print_summary(self):
        """Print test summary to console"""
        print(f"\n{'='*60}")
        print("TEST EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {self.test_summary['total_tests']}")
        print(f"Passed: {self.test_summary['passed_tests']} ✓")
        print(f"Failed: {self.test_summary['failed_tests']} ✗")
        print(f"Skipped: {self.test_summary['skipped_tests']} ⚠")
        print(f"Duration: {self.test_summary['duration']:.2f} seconds")
        print(f"Browsers: {', '.join(self.test_summary['browsers_tested'])}")
        print(f"Domains: {', '.join(self.test_summary['domains_tested'])}")
        
        if self.test_summary['total_tests'] > 0:
            pass_rate = (self.test_summary['passed_tests'] / self.test_summary['total_tests']) * 100
            print(f"Pass Rate: {pass_rate:.1f}%")
        
        # Show failed tests
        if self.test_summary['failed_tests'] > 0:
            print(f"\nFAILED TESTS:")
            for result in self.all_results:
                if result['status'] == 'FAIL':
                    print(f"  ✗ {result['test_name']}: {result.get('message', 'No message')}")

def main():
    """Main function to run tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='M&M Fashion Selenium Test Suite')
    parser.add_argument('--browser', choices=['chrome', 'firefox', 'both'], default='chrome',
                       help='Browser to test with')
    parser.add_argument('--headless', action='store_true',
                       help='Run tests in headless mode')
    parser.add_argument('--smoke', action='store_true',
                       help='Run smoke tests only')
    parser.add_argument('--generate-word-doc', action='store_true',
                       help='Generate Word document report')
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = TestRunner()
    
    try:
        if args.smoke:
            # Run smoke tests
            results = runner.run_smoke_tests(browser=args.browser, headless=args.headless)
        else:
            # Run full test suite
            browsers = ['chrome', 'firefox'] if args.browser == 'both' else [args.browser]
            results = runner.run_cross_browser_tests(browsers=browsers, headless=args.headless)
        
        # Generate reports
        runner.generate_json_report()
        runner.generate_html_report()
        
        # Print summary
        runner.print_summary()
        
        # Generate Word document if requested
        if args.generate_word_doc:
            try:
                from document_generator import DocumentGenerator
                doc_generator = DocumentGenerator(runner.all_results, runner.test_summary)
                doc_file = doc_generator.generate_word_document()
                print(f"Word document generated: {doc_file}")
            except ImportError:
                print("Word document generation requires python-docx. Install with: pip install python-docx")
            except Exception as e:
                print(f"Error generating Word document: {str(e)}")
        
        # Exit with appropriate code
        if runner.test_summary['failed_tests'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
    
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Critical error during test execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()