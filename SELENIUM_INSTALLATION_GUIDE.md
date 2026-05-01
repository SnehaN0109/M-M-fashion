# M&M Fashion Selenium Test Suite - Installation & Usage Guide

## 🎯 Overview

This comprehensive Selenium testing suite provides automated testing for the M&M Fashion e-commerce platform, covering:

- ✅ **Homepage functionality** and navigation
- ✅ **Product browsing** and filtering
- ✅ **Product detail** page interactions  
- ✅ **Shopping cart** management
- ✅ **Checkout process** validation
- ✅ **Cross-browser compatibility** (Chrome, Firefox)
- ✅ **Mobile responsiveness** testing
- ✅ **B2C vs B2B domain** testing (garba.shop vs ttd.in)
- ✅ **Performance testing** and monitoring
- ✅ **Professional Word document** reporting

## 📋 Prerequisites

### System Requirements
- **Python 3.7+** (Python 3.8+ recommended)
- **Chrome and/or Firefox** browser installed
- **4GB RAM** minimum (8GB recommended)
- **Internet connection** (for WebDriver downloads)

### Application Requirements
- **M&M Fashion Frontend** running on `http://localhost:5173`
- **M&M Fashion Backend** running on `http://localhost:5000`

## 🚀 Quick Start (5 Minutes)

### Step 1: Download and Setup
```bash
# 1. Navigate to your M&M Fashion project directory
cd /path/to/mm-fashion-project

# 2. Run the automated setup
python setup_selenium_tests.py

# 3. Start your M&M Fashion application
# Frontend: npm run dev (or your start command)
# Backend: python backend/app.py (or your start command)
```

### Step 2: Run Demo Test
```bash
# Run quick demo to verify everything works
python demo_selenium_tests.py
```

### Step 3: Run Full Tests
```bash
# Run complete test suite with Word document
python selenium_tests/test_runner.py --generate-word-doc
```

## 📦 Detailed Installation

### Method 1: Automated Setup (Recommended)
```bash
# Run the setup script - it handles everything
python setup_selenium_tests.py
```

The setup script will:
- ✅ Check Python version compatibility
- ✅ Install all required packages
- ✅ Create necessary directories
- ✅ Check browser availability
- ✅ Create convenient run scripts
- ✅ Generate comprehensive documentation

### Method 2: Manual Installation
```bash
# 1. Install Python packages
pip install selenium==4.15.2
pip install webdriver-manager==4.0.1
pip install python-docx==1.1.0
pip install Pillow==10.1.0
pip install pytest==7.4.3
pip install pytest-html==4.1.1
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
pip install openpyxl==3.1.2

# 2. Create directories
mkdir -p selenium_tests/test_screenshots
mkdir -p selenium_tests/test_reports

# 3. Verify browser installation
google-chrome --version  # or chrome --version
firefox --version
```

## 🎮 Usage Guide

### Basic Commands

#### 1. Smoke Tests (Quick - 2-3 minutes)
```bash
# Fast validation of core functionality
python selenium_tests/test_runner.py --smoke --headless
```

#### 2. Full Test Suite (10-15 minutes)
```bash
# Complete testing across all areas
python selenium_tests/test_runner.py
```

#### 3. Cross-Browser Testing
```bash
# Test with Chrome only
python selenium_tests/test_runner.py --browser chrome

# Test with Firefox only  
python selenium_tests/test_runner.py --browser firefox

# Test with both browsers
python selenium_tests/test_runner.py --browser both
```

#### 4. Headless Testing (Background)
```bash
# Run without opening browser windows
python selenium_tests/test_runner.py --headless
```

#### 5. Generate Professional Reports
```bash
# Create Word document with complete analysis
python selenium_tests/test_runner.py --generate-word-doc

# Headless with Word document
python selenium_tests/test_runner.py --headless --generate-word-doc
```

### Convenience Scripts

#### Windows Users
```batch
# Double-click run_tests.bat for interactive menu
run_tests.bat
```

#### Mac/Linux Users
```bash
# Run interactive menu
./run_tests.sh
```

## 📊 Understanding Test Results

### Test Categories

#### 1. Homepage Tests
- **Page Loading**: Validates homepage loads within performance thresholds
- **Navigation**: Tests all menu links and navigation functionality
- **Search**: Validates search functionality and results
- **Responsive Design**: Tests mobile, tablet, and desktop layouts
- **Domain Switching**: Validates B2C (garba.shop) vs B2B (ttd.in) functionality

#### 2. Product Browsing Tests
- **Category Pages**: Tests Men, Women, Kids, Ethnic, Western categories
- **Product Filtering**: Validates price, category, and size filters
- **Product Sorting**: Tests sorting by price, name, date
- **Search Results**: Validates search functionality and result display

#### 3. Product Detail Tests
- **Page Loading**: Validates product detail pages load correctly
- **Image Gallery**: Tests product image display and zoom functionality
- **Product Options**: Tests size, color, and quantity selection
- **Add to Cart**: Validates add to cart functionality
- **Information Display**: Tests product information completeness

#### 4. Cart & Checkout Tests
- **Add to Cart**: Tests adding products from listing pages
- **Cart Management**: Validates quantity updates and item removal
- **Form Validation**: Tests checkout form validation (email, phone, address)
- **Checkout Flow**: Tests complete purchase process
- **Cart Persistence**: Validates cart maintains items across navigation

#### 5. Performance Tests
- **Page Load Times**: Measures and validates page loading performance
- **API Response Times**: Tests backend API response speeds
- **Memory Usage**: Monitors browser memory consumption
- **JavaScript Errors**: Detects and reports JavaScript errors
- **Cross-Browser Performance**: Compares performance across browsers

### Test Status Meanings

- **✅ PASS**: Test completed successfully, functionality works as expected
- **❌ FAIL**: Test failed, issue found that needs attention
- **⚠️ SKIP**: Test was skipped (usually due to prerequisites not met)

### Performance Thresholds

- **Page Load Time**: Maximum 5 seconds
- **API Response Time**: Maximum 2 seconds
- **Memory Usage**: Monitored for memory leaks
- **JavaScript Errors**: Zero tolerance for critical errors

## 📄 Generated Reports

### 1. HTML Report
- **Location**: `selenium_tests/test_reports/test_report_YYYYMMDD_HHMMSS.html`
- **Content**: Interactive web-based report with test results
- **Features**: Sortable tables, color-coded results, summary statistics

### 2. JSON Report
- **Location**: `selenium_tests/test_reports/test_report_YYYYMMDD_HHMMSS.json`
- **Content**: Machine-readable test data
- **Use**: Integration with CI/CD systems, custom reporting

### 3. Word Document Report
- **Location**: `selenium_tests/test_reports/MM_Fashion_Selenium_Test_Report_YYYYMMDD_HHMMSS.docx`
- **Content**: Professional comprehensive report including:
  - Executive Summary
  - Test Environment Setup
  - Test Coverage Matrix
  - Detailed Test Results with Screenshots
  - Performance Metrics
  - Bug Reports and Issues Found
  - Recommendations for Improvements
  - Technical Appendix

### 4. Screenshots
- **Location**: `selenium_tests/test_screenshots/`
- **Content**: Automatic screenshots for both successful and failed tests
- **Naming**: `test_name_YYYYMMDD_HHMMSS.png`

## 🔧 Configuration

### Customizing Test Settings

Edit `selenium_tests/config.py` to modify:

```python
# Application URLs
FRONTEND_URL = "http://localhost:5173"
BACKEND_URL = "http://localhost:5000"

# Performance thresholds
MAX_PAGE_LOAD_TIME = 5.0  # seconds
MAX_API_RESPONSE_TIME = 2.0  # seconds

# Browser settings
BROWSERS = ["chrome", "firefox"]
HEADLESS = False

# Viewport sizes
DESKTOP_SIZE = (1920, 1080)
MOBILE_SIZE = (375, 667)
TABLET_SIZE = (768, 1024)

# Test data
TEST_USER_PHONE = "+919876543210"
TEST_USER_EMAIL = "test@example.com"
```

### Domain Testing Configuration

The test suite automatically switches between domains:
- **B2C Domain**: `garba.shop` (Premium Garba & Ethnic Wear)
- **B2B Domain**: `ttd.in` (Wholesale Ethnic Wear)

Domain switching is handled via localStorage for local testing.

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. "Browser not found" Error
```bash
# Install Chrome
# Ubuntu/Debian: sudo apt install google-chrome-stable
# CentOS/RHEL: sudo yum install google-chrome-stable
# Windows: Download from https://chrome.google.com
# Mac: brew install --cask google-chrome

# Install Firefox
# Ubuntu/Debian: sudo apt install firefox
# CentOS/RHEL: sudo yum install firefox
# Windows: Download from https://firefox.com
# Mac: brew install --cask firefox
```

#### 2. "WebDriver not found" Error
The test suite uses WebDriver Manager for automatic driver management. If issues persist:
```bash
# Clear WebDriver cache
rm -rf ~/.wdm  # Linux/Mac
rmdir /s %USERPROFILE%\.wdm  # Windows

# Reinstall webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager==4.0.1
```

#### 3. "Application not running" Error
```bash
# Verify frontend is running
curl http://localhost:5173

# Verify backend is running  
curl http://localhost:5000

# Start M&M Fashion application
# Frontend: npm run dev
# Backend: python backend/app.py
```

#### 4. "Permission denied" Error
```bash
# Linux/Mac: Run with appropriate permissions
sudo python selenium_tests/test_runner.py

# Windows: Run Command Prompt as Administrator
```

#### 5. "Module not found" Error
```bash
# Reinstall requirements
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 6. Tests Failing Due to Element Not Found
- **Cause**: Application UI changes or slow loading
- **Solution**: 
  - Increase timeouts in `config.py`
  - Check if application is fully loaded
  - Verify element selectors are correct

#### 7. Performance Tests Failing
- **Cause**: System resources or network issues
- **Solution**:
  - Close other applications
  - Check internet connection
  - Adjust performance thresholds in `config.py`

### Debug Mode

For debugging test issues:
```bash
# Run with verbose output
python selenium_tests/test_runner.py --headless --smoke

# Check generated screenshots
ls selenium_tests/test_screenshots/

# Review HTML report for detailed error messages
open selenium_tests/test_reports/test_report_*.html
```

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Selenium Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run Selenium tests
      run: |
        python selenium_tests/test_runner.py --headless --smoke
```

### Jenkins Pipeline Example
```groovy
pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python selenium_tests/test_runner.py --headless'
            }
        }
        stage('Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'selenium_tests/test_reports',
                    reportFiles: '*.html',
                    reportName: 'Selenium Test Report'
                ])
            }
        }
    }
}
```

## 📈 Best Practices

### 1. Regular Testing Schedule
- **Daily**: Run smoke tests
- **Weekly**: Run full test suite
- **Before releases**: Run complete cross-browser tests

### 2. Test Data Management
- Use consistent test data
- Avoid hardcoded values
- Implement data-driven testing for scalability

### 3. Performance Monitoring
- Set realistic performance thresholds
- Monitor trends over time
- Alert on performance degradation

### 4. Error Handling
- Review failed tests immediately
- Maintain test stability above 90%
- Update tests when application changes

### 5. Reporting
- Generate Word documents for stakeholders
- Use HTML reports for development teams
- Archive test results for trend analysis

## 🆘 Support and Maintenance

### Getting Help
1. **Check this guide** for common solutions
2. **Review test logs** and screenshots
3. **Check browser console** for JavaScript errors
4. **Verify application status** before testing
5. **Update dependencies** regularly

### Maintenance Tasks
- **Weekly**: Update browser drivers (automatic with WebDriver Manager)
- **Monthly**: Update Python packages
- **Quarterly**: Review and update test cases
- **As needed**: Update selectors when UI changes

### Extending the Test Suite

To add new tests:
1. Create new test class inheriting from `BaseTest`
2. Follow naming convention: `test_*` methods
3. Add comprehensive error handling
4. Include screenshots for verification
5. Update documentation

Example:
```python
from base_test import BaseTest

class NewFeatureTests(BaseTest):
    def test_new_functionality(self, domain="garba.shop"):
        test_name = f"New Functionality - {domain}"
        
        if not self.setup_driver():
            self.log_test_result(test_name, "FAIL", "Driver setup failed")
            return False
        
        try:
            # Test implementation
            self.navigate_to(f"{self.config.FRONTEND_URL}/new-feature", domain)
            # ... test logic ...
            
            screenshot = self.take_screenshot("new_feature", "Testing new feature")
            self.log_test_result(test_name, "PASS", "Feature works correctly", screenshot)
            return True
            
        except Exception as e:
            screenshot = self.take_screenshot("new_feature_error", "Error in new feature")
            self.log_test_result(test_name, "FAIL", f"Exception: {str(e)}", screenshot)
            return False
        
        finally:
            self.teardown_driver()
```

## 📞 Contact and Support

For technical support or questions about the test suite:
- **Documentation**: Review this guide and `SELENIUM_TESTING_README.md`
- **Issues**: Check troubleshooting section
- **Updates**: Keep dependencies updated regularly

---

**Happy Testing! 🧪✨**

*This test suite helps ensure the M&M Fashion platform delivers a high-quality user experience across all browsers and devices.*