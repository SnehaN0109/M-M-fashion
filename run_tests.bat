@echo off
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
