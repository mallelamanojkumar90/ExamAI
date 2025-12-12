"""
Direct database test for performance data
"""
from database import get_db, ExamAttempt, User
from performance_service import PerformanceService

def test_direct_query():
    db = next(get_db())
    
    print("\n" + "="*60)
    print("DIRECT DATABASE QUERY TEST")
    print("="*60)
    
    # Get user
    user = db.query(User).first()
    if not user:
        print("❌ No users found in database")
        return
    
    print(f"\n✅ Found user: {user.email} (ID: {user.user_id})")
    
    # Get exam attempts
    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == user.user_id
    ).all()
    
    print(f"✅ Found {len(attempts)} exam attempts")
    
    if attempts:
        print("\nAttempt details:")
        for attempt in attempts:
            print(f"  - ID: {attempt.attempt_id}")
            print(f"    Score: {attempt.score}/{attempt.total_questions}")
            print(f"    Start: {attempt.start_time}")
            print(f"    End: {attempt.end_time}")
    
    # Test performance service
    print("\n" + "="*60)
    print("TESTING PERFORMANCE SERVICE")
    print("="*60)
    
    try:
        summary = PerformanceService.get_user_performance_summary(user.user_id, db)
        print(f"\n✅ Performance Summary Retrieved!")
        print(f"  Total Exams: {summary['total_exams']}")
        print(f"  Accuracy: {summary['accuracy']}%")
        print(f"  Subjects: {list(summary['subjects_performance'].keys())}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    db.close()

if __name__ == "__main__":
    test_direct_query()
