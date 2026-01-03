#!/usr/bin/env python3
"""
Basic API tests for OCR Khai Sinh application
"""

import requests
import sys
import time

# Configuration
API_BASE_URL = "http://localhost:8128"
TIMEOUT = 30

def test_health_check():
    """Test if the API is running"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=TIMEOUT)
        if response.status_code == 200:
            print("✓ Health check passed")
            return True
        else:
            print(f"✗ Health check failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_api_docs():
    """Test if API documentation is accessible"""
    print("Testing API documentation...")
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=TIMEOUT)
        if response.status_code == 200 and "swagger" in response.text.lower():
            print("✓ API documentation accessible")
            return True
        else:
            print("✗ API documentation not accessible")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ API documentation test failed: {e}")
        return False

def test_openapi_schema():
    """Test if OpenAPI schema is available"""
    print("Testing OpenAPI schema...")
    try:
        response = requests.get(f"{API_BASE_URL}/openapi.json", timeout=TIMEOUT)
        if response.status_code == 200:
            schema = response.json()
            if "openapi" in schema and "paths" in schema:
                print("✓ OpenAPI schema valid")
                return True
            else:
                print("✗ OpenAPI schema invalid")
                return False
        else:
            print(f"✗ OpenAPI schema request failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ OpenAPI schema test failed: {e}")
        return False

def wait_for_api(max_retries=10, delay=3):
    """Wait for API to be ready"""
    print(f"Waiting for API to be ready (max {max_retries} retries)...")
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
            if response.status_code == 200:
                print(f"✓ API is ready after {i+1} attempt(s)")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_retries - 1:
            print(f"  Attempt {i+1}/{max_retries} failed, retrying in {delay}s...")
            time.sleep(delay)
    
    print("✗ API did not become ready in time")
    return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("OCR Khai Sinh API Tests")
    print("=" * 50)
    print()
    
    # Wait for API to be ready
    if not wait_for_api():
        print("\n❌ Tests failed: API not ready")
        sys.exit(1)
    
    print()
    
    # Run tests
    tests = [
        test_health_check,
        test_api_docs,
        test_openapi_schema,
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # Summary
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    print("=" * 50)
    
    if passed == total:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
