"""
Demo script to test M&M Fashion Selenium Test Suite
This script runs a quick demonstration of the testing capabilities
"""
import os
import sys
import time
from datetime import datetime

# Add selenium_tests to path
sys.path.append('selenium_tests')

try:
    from test_runner import TestRunner
    from document_generator import DocumentGenerator
except ImportError as e:
    print(f"Error importing test modules: {e}")
    print("Please run 'python setup_selenium_tests.py' first")
    sys.exit(1)

def check_application_status():
    """Check if M&M Fashion application is running"""
    import requests
    
    print("Checking application status...")
    
    try:
        # Check frontend
        frontend_response = requests.get("http://localhost:5173", timeout=5)
        frontend_status = "✓ Running" if frontend_response.status_code == 200 else "✗ Error"
    except requests.exceptions.RequestException:
        frontend_status = "✗ Not running"
    
    try:
        # Check backend
        backend_response = requests.get("http://localhost:5000/health", timeout=5)
        backend_status = "✓ Running" if backend_response.status_code == 200 else "✗ Error"
    except requests.exceptions.RequestException:
        try:
            # Try alternative backend endpoint
            backend_response = requests.get("http://localhost:5000", timeout=5)
            backend_status = "✓ Running" if backend_response.status_code in [200, 404] else "✗ Error"
        except requests.exceptions.RequestException:
            backend_status = "✗ Not running"
    
    print(f"Frontend (http://localhost:5173): {frontend_status}")
    print(f"Backend (http://localhost:5000): {backend_status}")
    
    return "Running" in frontend_status

def run_demo_tests():
    """Run a demonstration of the test suite"""
    print("\n" + "="*60)
    print("M&M FASHION SELENIUM TEST SUITE DEMONSTRATION")
    print("="*60)
    
    # Check application status
    app_running = check_application_status()
    
    if not app_running:
        print("\n⚠️  WARNING: Frontend application doesn't appear to be running")
        print("   Please start the M&M Fashion application:")
        print("   - Frontend: npm run dev (should run on http://localhost:5173)")
        print("   - Backend: python backend/app.py (should run on http://localhost:5000)")
        print("\n   The demo will continue but tests may fail...")
        
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    
    print(f"\n🚀 Starting demo test run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize test runner
    runner = TestRunner()
    
    try:
        print("\n📋 Running smoke tests (quick validation)...")
        print("   This will test basic functionality across key areas")
        
        # Run smoke tests
        results = runner.run_smoke_tests(browser="chrome", headless=True)
        
        print(f"\n📊 Test Results Summary:")
        print(f"   Total Tests: {runner.test_summary['total_tests']}")
        print(f"   Passed: {runner.test_summary['passed_tests']} ✅")
        print(f"   Failed: {runner.test_summary['failed_tests']} ❌")
        print(f"   Skipped: {runner.test_summary['skipped_tests']} ⚠️")
        print(f"   Duration: {runner.test_summary['duration']:.2f} seconds")
        
        # Generate reports
        print(f"\n📄 Generating reports...")
        json_report = runner.generate_json_report()
        html_report = runner.generate_html_report()
        
        print(f"   JSON Report: {json_report}")
        print(f"   HTML Report: {html_report}")
        
        # Generate Word document if possible
        try:
            print(f"   Generating Word document...")
            doc_generator = DocumentGenerator(runner.all_results, runner.test_summary)
            word_doc = doc_generator.generate_word_document()
            print(f"   Word Document: {word_doc}")
        except Exception as e:
            print(f"   Word Document: Failed ({str(e)})")
        
        # Show sample test results
        print(f"\n🔍 Sample Test Results:")
        for i, result in enumerate(results[:5]):  # Show first 5 results
            status_icon = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "⚠️"
            print(f"   {status_icon} {result['test_name']}")
            if result.get('message'):
                print(f"      {result['message'][:80]}{'...' if len(result['message']) > 80 else ''}")
        
        if len(results) > 5:
            print(f"   ... and {len(results) - 5} more tests")
        
        # Show failed tests if any
        failed_tests = [r for r in results if r['status'] == 'FAIL']
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests[:3]:  # Show first 3 failed tests
                print(f"   • {test['test_name']}")
                print(f"     {test.get('message', 'No error message')}")
        
        # Performance summary
        perf_tests = [r for r in results if 'performance' in r['test_name'].lower()]
        if perf_tests:
            print(f"\n⚡ Performance Summary:")
            for test in perf_tests:
                print(f"   • {test['test_name']}: {test['status']}")
        
        print(f"\n🎯 Demo completed successfully!")
        
        # Calculate pass rate
        if runner.test_summary['total_tests'] > 0:
            pass_rate = (runner.test_summary['passed_tests'] / runner.test_summary['total_tests']) * 100
            print(f"   Overall Pass Rate: {pass_rate:.1f}%")
            
            if pass_rate >= 80:
                print("   🎉 Excellent! Most tests are passing.")
            elif pass_rate >= 60:
                print("   👍 Good! Some areas need attention.")
            else:
                print("   ⚠️  Several issues found. Review failed tests.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        print("   This might be due to:")
        print("   - Application not running")
        print("   - Browser not installed")
        print("   - Network connectivity issues")
        print("   - Missing dependencies")
        return False

def show_next_steps():
    """Show next steps after demo"""
    print(f"\n📚 Next Steps:")
    print("="*40)
    print("1. 🔧 Run Full Test Suite:")
    print("   python selenium_tests/test_runner.py")
    print("")
    print("2. 🌐 Test Multiple Browsers:")
    print("   python selenium_tests/test_runner.py --browser both")
    print("")
    print("3. 📄 Generate Word Report:")
    print("   python selenium_tests/test_runner.py --generate-word-doc")
    print("")
    print("4. 🎯 Run Specific Tests:")
    print("   python selenium_tests/test_runner.py --smoke")
    print("")
    print("5. 👁️ Run Headless (Background):")
    print("   python selenium_tests/test_runner.py --headless")
    print("")
    print("6. 📖 Read Documentation:")
    print("   Open SELENIUM_TESTING_README.md")
    print("")
    print("7. 🔍 View Test Reports:")
    print("   Check selenium_tests/test_reports/ folder")
    print("")
    print("8. 📸 View Screenshots:")
    print("   Check selenium_tests/test_screenshots/ folder")

def main():
    """Main demo function"""
    print("🧪 M&M Fashion Selenium Test Suite Demo")
    print("This demo will run a quick test to validate the setup")
    print("")
    
    # Check if setup was run
    if not os.path.exists("selenium_tests/config.py"):
        print("❌ Test suite not found!")
        print("Please run: python setup_selenium_tests.py")
        return False
    
    # Run demo
    success = run_demo_tests()
    
    if success:
        show_next_steps()
        print(f"\n✨ Demo completed! Check the generated reports.")
    else:
        print(f"\n💡 Troubleshooting Tips:")
        print("   - Ensure M&M Fashion app is running")
        print("   - Check browser installation")
        print("   - Run: python setup_selenium_tests.py")
        print("   - Check SELENIUM_TESTING_README.md")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)