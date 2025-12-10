"""
Check Exam Attempts Script
Verifies if there is any data in the exam_attempts table
"""

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

from database import get_db, ExamAttempt, User
from sqlalchemy.orm import Session
import json

def check_attempts():
    db = next(get_db())
    try:
        # Get all users
        users = db.query(User).all()
        print(f"\n👥 Total Users: {len(users)}\n")
        
        for user in users:
            # Get attempts for this user
            attempts = db.query(ExamAttempt).filter(ExamAttempt.user_id == user.user_id).all()
            
            if attempts:
                print(f"✅ User: {user.email} (ID: {user.user_id}) has {len(attempts)} attempts")
                for attempt in attempts:
                    print(f"    - Attempt {attempt.attempt_id}: Score {attempt.score}/{attempt.total_questions}, Date: {attempt.end_time}")
            else:
                pass
                # print(f"❌ User: {user.email} (ID: {user.user_id}) has 0 attempts")
                
        # global count
        total_attempts = db.query(ExamAttempt).count()
        print(f"\n📊 Total attempts in database: {total_attempts}\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_attempts()
