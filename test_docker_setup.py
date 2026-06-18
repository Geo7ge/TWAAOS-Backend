#!/usr/bin/env python3
"""
Test script to verify Docker setup is working correctly
Run this after: docker-compose up -d
"""

import requests
import sys
import time

def test_api_health():
    """Test if API is responding"""
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✓ API is responding (root endpoint)")
            return True
    except Exception as e:
        print(f"✗ API not responding: {e}")
        return False

def test_api_docs():
    """Test if API docs are available"""
    try:
        response = requests.get('http://localhost:8000/docs', timeout=5)
        if response.status_code == 200:
            print("✓ API documentation (Swagger UI) is available")
            return True
    except Exception as e:
        print(f"✗ API docs not available: {e}")
        return False

def test_api_openapi():
    """Test if OpenAPI schema is available"""
    try:
        response = requests.get('http://localhost:8000/openapi.json', timeout=5)
        if response.status_code == 200:
            print("✓ OpenAPI schema is available")
            return True
    except Exception as e:
        print(f"✗ OpenAPI schema not available: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Docker Setup Verification Tests")
    print("=" * 60)
    print("")
    
    print("⏳ Waiting for API to be ready (timeout: 60s)...")
    print("")
    
    # Wait up to 60 seconds for API to be ready
    start_time = time.time()
    timeout = 60
    api_ready = False
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get('http://localhost:8000/', timeout=2)
            if response.status_code == 200:
                api_ready = True
                break
        except:
            pass
        
        elapsed = int(time.time() - start_time)
        print(f"\r⏳ Waiting... {elapsed}s", end="", flush=True)
        time.sleep(1)
    
    print("\r" + " " * 30 + "\r", end="")  # Clear line
    
    if not api_ready:
        print("✗ API failed to start within timeout")
        print("")
        print("Debug steps:")
        print("  1. Check if Docker containers are running:")
        print("     docker-compose ps")
        print("  2. View API logs:")
        print("     docker-compose logs api")
        print("  3. View database logs:")
        print("     docker-compose logs db")
        return False
    
    print("✓ API is ready!")
    print("")
    
    # Run tests
    tests = [
        ("API Health", test_api_health),
        ("API Documentation", test_api_docs),
        ("OpenAPI Schema", test_api_openapi),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append(result)
    
    print("")
    print("=" * 60)
    
    if all(results):
        print("✅ All tests passed!")
        print("")
        print("Your Docker setup is working correctly!")
        print("")
        print("📖 Next steps:")
        print("  - API Docs: http://localhost:8000/docs")
        print("  - API: http://localhost:8000")
        print("  - Database: localhost:5432")
        print("")
        print("🛑 To stop containers:")
        print("  docker-compose down")
        print("")
        return True
    else:
        print("❌ Some tests failed!")
        print("")
        print("Try these steps to debug:")
        print("  1. Check container status:")
        print("     docker-compose ps")
        print("  2. View detailed logs:")
        print("     docker-compose logs -f")
        print("  3. Rebuild containers:")
        print("     docker-compose down -v")
        print("     docker-compose build --no-cache")
        print("     docker-compose up -d")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
