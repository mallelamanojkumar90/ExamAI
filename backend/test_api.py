"""
Test script to check backend API
"""
import requests
import json

try:
    print("Testing backend API...")
    response = requests.post(
        "http://localhost:8000/generate-questions",
        json={
            "subject": "Physics",
            "difficulty": "Easy",
            "count": 2
        },
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    
    if response.ok:
        data = response.json()
        print(f"\n✅ Success! Generated {len(data)} questions")
    else:
        print(f"\n❌ Error: {response.status_text}")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")
    import traceback
    traceback.print_exc()
