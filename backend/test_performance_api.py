"""
Quick test script for Performance Dashboard API
Tests all endpoints to ensure they're working correctly
"""

import requests
import json

BASE_URL = "http://localhost:8000"
USER_ID = 1  # Test user ID

def test_endpoint(name, url):
    """Test a single endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS")
            print(f"Response Preview:")
            print(json.dumps(data, indent=2)[:500] + "...")
        else:
            print(f"❌ FAILED")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def main():
    print("\n" + "="*60)
    print("PERFORMANCE DASHBOARD API TESTS")
    print("="*60)
    
    # Test all endpoints
    endpoints = [
        ("Performance Summary", f"{BASE_URL}/api/performance/summary/{USER_ID}"),
        ("Performance Timeline (30 days)", f"{BASE_URL}/api/performance/timeline/{USER_ID}?days=30"),
        ("Peer Comparison", f"{BASE_URL}/api/performance/peer-comparison/{USER_ID}"),
        ("Strengths & Weaknesses", f"{BASE_URL}/api/performance/analysis/{USER_ID}"),
        ("Recent Activity", f"{BASE_URL}/api/performance/recent-activity/{USER_ID}?limit=5"),
        ("Subject Performance", f"{BASE_URL}/api/performance/subjects/{USER_ID}"),
        ("Difficulty Performance", f"{BASE_URL}/api/performance/difficulty/{USER_ID}"),
        ("Full Dashboard", f"{BASE_URL}/api/performance/dashboard/{USER_ID}"),
    ]
    
    for name, url in endpoints:
        test_endpoint(name, url)
    
    print("\n" + "="*60)
    print("TESTS COMPLETE")
    print("="*60)
    print("\nNote: If you see 404 errors, make sure:")
    print("1. Backend server is running (python main.py)")
    print("2. Performance routes are integrated in main.py")
    print("3. Database has some exam attempt data")

if __name__ == "__main__":
    main()
