"""
Test the performance dashboard endpoint
"""
import requests

def test_performance_dashboard():
    # Assuming user_id = 1 (adjust based on your user)
    user_id = 1
    
    print("\n" + "="*60)
    print(f"Testing Performance Dashboard for User ID: {user_id}")
    print("="*60)
    
    try:
        url = f"http://localhost:8000/api/performance/dashboard/{user_id}"
        print(f"\nCalling: {url}")
        
        response = requests.get(url)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                print("\n✅ SUCCESS! Dashboard data retrieved")
                
                summary = data["dashboard"]["summary"]
                print(f"\n📊 Performance Summary:")
                print(f"  Total Exams: {summary['total_exams']}")
                print(f"  Total Questions: {summary['total_questions']}")
                print(f"  Correct Answers: {summary['correct_answers']}")
                print(f"  Accuracy: {summary['accuracy']}%")
                print(f"  Recent Trend: {summary['recent_trend']}")
                print(f"  Time Spent: {summary['time_spent_minutes']} minutes")
                
                print(f"\n📚 Subject Performance:")
                for subject, perf in summary['subjects_performance'].items():
                    print(f"  {subject}: {perf['accuracy']}% ({perf['attempts']} exams)")
                
                recent = data["dashboard"]["recent_activity"]
                print(f"\n🕒 Recent Activity: {len(recent)} exams")
                for activity in recent[:3]:
                    print(f"  - {activity['subject']}: {activity['score']}/{activity['total_questions']}")
                
            else:
                print("\n❌ Response not successful")
                print(data)
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_performance_dashboard()
