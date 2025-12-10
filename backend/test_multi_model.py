"""
Test script for multi-model configuration
Tests model availability and question generation
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_models_endpoint():
    """Test the /models endpoint"""
    print("\n" + "="*60)
    print("Testing /models endpoint...")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/models")
        if response.status_code == 200:
            data = response.json()
            print("✅ Models endpoint working!")
            print(f"\nDefault Configuration:")
            print(f"  Provider: {data['default']['provider']}")
            print(f"  Model: {data['default']['model_name']}")
            print(f"  Temperature: {data['default']['temperature']}")
            
            print(f"\nAvailable Providers:")
            for provider, info in data['models'].items():
                status = "✅ Configured" if info['available'] else "❌ Not Configured"
                print(f"  {provider}: {status}")
                if info['available']:
                    print(f"    Models: {len(info['models'])} available")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_question_generation(provider="openai", model_name="gpt-4o-mini"):
    """Test question generation with specific model"""
    print("\n" + "="*60)
    print(f"Testing question generation with {provider}/{model_name}...")
    print("="*60)
    
    payload = {
        "subject": "Physics",
        "difficulty": "medium",
        "count": 2,
        "exam_type": "IIT_JEE",
        "model_provider": provider,
        "model_name": model_name,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-questions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            questions = response.json()
            print(f"✅ Generated {len(questions)} questions successfully!")
            print(f"\nSample Question:")
            if questions:
                q = questions[0]
                print(f"  Text: {q['text'][:100]}...")
                print(f"  Options: {len(q['options'])} choices")
                print(f"  Has Explanation: {'Yes' if q.get('explanation') else 'No'}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_default_generation():
    """Test question generation with default model"""
    print("\n" + "="*60)
    print("Testing question generation with default model...")
    print("="*60)
    
    payload = {
        "subject": "Chemistry",
        "difficulty": "easy",
        "count": 2,
        "exam_type": "NEET"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-questions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            questions = response.json()
            print(f"✅ Generated {len(questions)} questions with default model!")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 Multi-Model Configuration Test Suite")
    print("="*60)
    
    # Test 1: Check models endpoint
    models_ok = test_models_endpoint()
    
    # Test 2: Test default generation
    default_ok = test_default_generation()
    
    # Test 3: Test OpenAI generation
    openai_ok = test_question_generation("openai", "gpt-4o-mini")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Models Endpoint: {'✅ PASS' if models_ok else '❌ FAIL'}")
    print(f"Default Generation: {'✅ PASS' if default_ok else '❌ FAIL'}")
    print(f"OpenAI Generation: {'✅ PASS' if openai_ok else '❌ FAIL'}")
    
    all_passed = models_ok and default_ok and openai_ok
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    print("\n💡 To test other providers (Google, Anthropic):")
    print("   1. Add API keys to .env file")
    print("   2. Restart the backend server")
    print("   3. Run this test again")
