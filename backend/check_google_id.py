"""
Quick test to verify google_id column exists
"""

import os
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///exam_app.db")

def check_google_id_column():
    """Check if google_id column exists in users table"""
    engine = create_engine(DATABASE_URL, echo=False)
    
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns('users')
        
        print("Current columns in 'users' table:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
        
        # Check if google_id exists
        column_names = [col['name'] for col in columns]
        if 'google_id' in column_names:
            print("\n✅ google_id column EXISTS")
        else:
            print("\n❌ google_id column DOES NOT EXIST")
            print("Run: python migrate_add_google_oauth.py")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    check_google_id_column()
