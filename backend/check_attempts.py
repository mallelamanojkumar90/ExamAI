"""
Debug script to check exam attempts in database
"""
from database import get_db, ExamAttempt, User
from sqlalchemy import func

def check_exam_attempts():
    db = next(get_db())
    
    print("\n" + "="*60)
    print("CHECKING EXAM ATTEMPTS IN DATABASE")
    print("="*60)
    
    # Get all users
    users = db.query(User).all()
    print(f"\nTotal Users: {len(users)}")
    
    for user in users:
        print(f"\n--- User: {user.email} (ID: {user.user_id}) ---")
        
        # Get exam attempts for this user
        attempts = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == user.user_id
        ).all()
        
        print(f"  Exam Attempts: {len(attempts)}")
        
        if attempts:
            for attempt in attempts:
                print(f"    - Attempt ID: {attempt.attempt_id}")
                print(f"      Score: {attempt.score}/{attempt.total_questions}")
                print(f"      Started: {attempt.start_time}")
                print(f"      Completed: {attempt.end_time}")
                print(f"      Status: {attempt.status}")
    
    # Check all exam attempts regardless of user
    print("\n" + "="*60)
    print("ALL EXAM ATTEMPTS")
    print("="*60)
    
    all_attempts = db.query(ExamAttempt).all()
    print(f"\nTotal Exam Attempts: {len(all_attempts)}")
    
    for attempt in all_attempts:
        print(f"\n  Attempt ID: {attempt.attempt_id}")
        print(f"  User ID: {attempt.user_id}")
        print(f"  Score: {attempt.score}/{attempt.total_questions}")
        print(f"  Started: {attempt.start_time}")
        print(f"  Status: {attempt.status}")
    
    db.close()

if __name__ == "__main__":
    check_exam_attempts()
