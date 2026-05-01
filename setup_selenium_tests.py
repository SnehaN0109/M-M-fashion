"""
Setup script for M&M Fashion Selenium Test Suite
"""
import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        return False
    print(f"✓ Python {sys.version.split()[0]} detected")
    return True

def install_requirements():
    """Install required Python packages"""
    print("\nInstalling required packages...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "selenium_tests/test_screenshots",
        "selenium_tests/test_reports"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_browser_availability():
    """Check if browsers are available"""
    browsers = {
        'chrome': ['google-chrome', 'chrome', 'chromium'],
        'firefox': ['firefox', 'firefox-esr']
    }
    
    available_browsers = []
    
    for browser, commands in browsers.items():
        for cmd in commands:
            try:
                subprocess.run([cmd, '--version'], 
                             capture_output=True, 
                             check=True, 
                             timeout=5)
                available_browsers.append(browser)
                print(f"✓ {browser.title()} browser detected")
                break
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
    
    if not available_browsers:
        print("⚠ Warning: No browsers detected. Please install Chrome or Firefox.")
        return False
    
    return available_browsers

def create_run_scripts():
    """Create convenient run scripts"""
    
    # Windows batch script
    if platform.system() == "Windows":
        batch_script = """@echo off
echo M&M Fashion Selenium Test Suite
echo ================================

echo.
echo Available options:
echo 1. Run smoke tests (quick)
echo 2. Run full test suite
echo 3. Run tests with Word document generation
echo 4. Run headless tests
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    python selenium_tests/test_runner.py --smoke --headless
) else if "%choice%"=="2" (
    python selenium_tests/test_runner.py
) else if "%choice%"=="3" (
    python selenium_tests/test_runner.py --generate-word-doc
) else if "%choice%"=="4" (
    python selenium_tests/test_runner.py --headless
) else (
    echo Invalid choice
)

pause
"""
        with open("run_tests.bat", "w") as f:
            f.write(batch_script)
        print("✓ Created run_tests.bat for Windows")
    
    # Unix shell script
    shell_script = """#!/bin/bash
echo "M&M Fashion Selenium Test Suite"
echo "================================"
echo ""
echo "Available options:"
echo "1. Run smoke tests (quick)"
echo "2. Run full test suite"
echo "3. Run tests with Word document generation"
echo "4. Run headless tests"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        python3 selenium_tests/test_runner.py --smoke --headless
        ;;
    2)
        python3 selenium_tests/test_runner.py
        ;;
    3)
        python3 selenium_tests/test_runner.py --generate-word-doc
        ;;
    4)
        python3 selenium_tests/test_runner.py --headless
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
"""
    with open("run_tests.sh", "w") as f:
        f.write(shell_script)
    
    # Make shell script executable on Unix systems
    if platform.system() != "Windows":
        os.chmod("run_tests.sh", 0o755)
        print("✓ Created run_tests.sh for Unix/Linux/Mac")

def create_readme():
    """Create comprehensive README file"""
    readme_content = """# M&M Fashion Selenium Test Suite

## Overview
Comprehensive automated testing suite for the M&M Fashion e-commerce platform using Selenium WebDriver.

## Features
- ✅ Homepage functionality testing
- ✅ Product browsing and filtering
- ✅ Product detail page interactions
- ✅ Shopping cart management
- ✅ Checkout process validation
- ✅ Cross-browser compatibility (Chrome, Firefox)
- ✅ Mobile responsiveness testing
- ✅ B2C vs B2B domain testing
- ✅ Performance testing
- ✅ Professional Word document reporting

## Prerequisites
- Python 3.7 or higher
- Chrome and/or Firefox browser
- M&M Fashion application running locally:
  - Frontend: http://localhost:5173
  - Backend: http://localhost:5000

## Installation

1. **Clone or download the test suite**
2. **Run the setup script:**
   ```bash
   python setup_selenium_tests.py
   ```

3. **Manual installation (if setup script fails):**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
```bash
# Run smoke tests (quick validation)
python selenium_tests/test_runner.py --smoke --headless

# Run full test suite
python selenium_tests/test_runner.py

# Run with Word document generation
python selenium_tests/test_runner.py --generate-word-doc
```

### Using Convenience Scripts
- **Windows:** Double-click `run_tests.bat`
- **Unix/Linux/Mac:** Run `./run_tests.sh`

### Command Line Options
```bash
python selenium_tests/test_runner.py [OPTIONS]

Options:
  --browser {chrome,firefox,both}  Browser to test with (default: chrome)
  --headless                       Run tests in headless mode
  --smoke                         Run smoke tests only
  --generate-word-doc             Generate Word document report
```

### Examples
```bash
# Test with Firefox browser
python selenium_tests/test_runner.py --browser firefox

# Test both browsers
python selenium_tests/test_runner.py --browser both

# Run headless tests with Word report
python selenium_tests/test_runner.py --headless --generate-word-doc
```

## Test Categories

### 1. Homepage Tests
- Page loading and performance
- Navigation menu functionality
- Search functionality
- Responsive design
- Domain switching (B2C/B2B)

### 2. Product Browsing Tests
- Category page loading
- Product filtering
- Product sorting
- Search results

### 3. Product Detail Tests
- Product page loading
- Image gallery functionality
- Product options selection
- Add to cart functionality
- Product information display

### 4. Cart & Checkout Tests
- Add to cart from product list
- Cart page functionality
- Quantity updates and item removal
- Checkout form validation
- Successful checkout flow
- Cart persistence

### 5. Performance Tests
- Page load performance
- API response times
- Memory usage monitoring
- JavaScript error detection
- Cross-browser performance
- Concurrent user simulation

## Output Files

### Test Reports
- **HTML Report:** `selenium_tests/test_reports/test_report_YYYYMMDD_HHMMSS.html`
- **JSON Report:** `selenium_tests/test_reports/test_report_YYYYMMDD_HHMMSS.json`
- **Word Document:** `selenium_tests/test_reports/MM_Fashion_Selenium_Test_Report_YYYYMMDD_HHMMSS.docx`

### Screenshots
- Stored in: `selenium_tests/test_screenshots/`
- Automatically captured for both successful and failed tests
- Named with test name and timestamp

## Configuration

Edit `selenium_tests/config.py` to modify:
- Application URLs
- Test timeouts
- Browser settings
- Performance thresholds
- Test data

## Troubleshooting

### Common Issues

1. **Browser not found:**
   - Install Chrome or Firefox
   - Ensure browser is in system PATH

2. **WebDriver issues:**
   - WebDriver Manager automatically handles driver downloads
   - Check internet connection for driver downloads

3. **Application not running:**
   - Ensure frontend is running on http://localhost:5173
   - Ensure backend is running on http://localhost:5000

4. **Permission errors:**
   - Run with administrator/sudo privileges if needed
   - Check file permissions in test directories

### Debug Mode
Add `--headless` flag to run tests without opening browser windows for debugging.

## Test Data

The test suite uses predefined test data for:
- Valid/invalid checkout information
- Search terms
- Filter options
- User credentials

Modify `TEST_DATA` in `config.py` to customize test data.

## Extending Tests

To add new tests:
1. Create new test class inheriting from `BaseTest`
2. Add test methods following naming convention `test_*`
3. Register test class in `test_runner.py`
4. Update documentation

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review test logs and screenshots
3. Check browser console for JavaScript errors
4. Verify application is running correctly

## License

This test suite is part of the M&M Fashion project.
"""
    
    with open("SELENIUM_TESTING_README.md", "w", encoding='utf-8') as f:
        f.write(readme_content)
    print("✓ Created comprehensive README file")

def main():
    """Main setup function"""
    print("M&M Fashion Selenium Test Suite Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Create directories
    create_directories()
    
    # Check browser availability
    available_browsers = check_browser_availability()
    
    # Create run scripts
    create_run_scripts()
    
    # Create README
    create_readme()
    
    print("\n" + "=" * 40)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Ensure M&M Fashion app is running:")
    print("   - Frontend: http://localhost:5173")
    print("   - Backend: http://localhost:5000")
    print("2. Run tests using:")
    if platform.system() == "Windows":
        print("   - run_tests.bat (Windows)")
    print("   - ./run_tests.sh (Unix/Linux/Mac)")
    print("   - python selenium_tests/test_runner.py --smoke")
    print("\nFor detailed instructions, see SELENIUM_TESTING_README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)