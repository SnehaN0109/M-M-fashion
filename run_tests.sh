#!/bin/bash
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
