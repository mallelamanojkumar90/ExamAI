"""
Database migration script to add google_id column for OAuth support
Run this script to update your existing database schema
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///exam_app.db")

def migrate_add_google_id():
    """Add google_id column to users table"""
    engine = create_engine(DATABASE_URL, echo=True)
    
    try:
        with engine.connect() as conn:
            # Check if column already exists
            if 'postgresql' in DATABASE_URL:
                # PostgreSQL
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='users' AND column_name='google_id'
                """))
                
                if result.fetchone() is None:
                    print("Adding google_id column to users table...")
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN google_id VARCHAR(255) UNIQUE
                    """))
                    conn.commit()
                    print("✅ google_id column added successfully!")
                else:
                    print("ℹ️  google_id column already exists, skipping migration")
                    
            else:
                # SQLite
                result = conn.execute(text("PRAGMA table_info(users)"))
                columns = [row[1] for row in result.fetchall()]
                
                if 'google_id' not in columns:
                    print("Adding google_id column to users table...")
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN google_id VARCHAR(255) UNIQUE
                    """))
                    conn.commit()
                    print("✅ google_id column added successfully!")
                else:
                    print("ℹ️  google_id column already exists, skipping migration")
                    
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("🚀 Starting database migration...")
    print(f"Database: {DATABASE_URL}")
    migrate_add_google_id()
    print("✅ Migration completed!")
