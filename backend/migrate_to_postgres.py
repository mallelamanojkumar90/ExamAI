"""
Migration script to transfer data from SQLite to PostgreSQL
Run this after setting up PostgreSQL database
"""

import sqlite3
from database import SessionLocal, User, init_db
from datetime import datetime
import bcrypt

def migrate_users():
    """Migrate users from SQLite to PostgreSQL"""
    print("\n📦 Migrating users...")
    
    # Connect to SQLite
    sqlite_conn = sqlite3.connect("exam_app.db")
    sqlite_conn.row_factory = sqlite3.Row
    cursor = sqlite_conn.cursor()
    
    # Get all users from SQLite
    cursor.execute("SELECT * FROM users")
    sqlite_users = cursor.fetchall()
    
    if not sqlite_users:
        print("⚠️  No users found in SQLite database")
        sqlite_conn.close()
        return
    
    # Connect to PostgreSQL
    db = SessionLocal()
    
    try:
        migrated_count = 0
        for sqlite_user in sqlite_users:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == sqlite_user['username']).first()
            if existing_user:
                print(f"⏭️  User {sqlite_user['username']} already exists, skipping...")
                continue
            
            # Create new user in PostgreSQL
            new_user = User(
                email=sqlite_user['username'],  # SQLite uses 'username', PostgreSQL uses 'email'
                password_hash=sqlite_user['password_hash'],
                full_name=sqlite_user['full_name'],
                role='student',  # Default role
                created_at=datetime.utcnow(),
                is_active=True
            )
            db.add(new_user)
            migrated_count += 1
            print(f"✅ Migrated user: {sqlite_user['username']}")
        
        db.commit()
        print(f"\n✨ Successfully migrated {migrated_count} users!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        db.rollback()
    finally:
        db.close()
        sqlite_conn.close()


def create_default_admin():
    """Create default admin user"""
    print("\n👤 Creating default admin user...")
    
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@exam.com").first()
        if admin:
            print("⚠️  Admin user already exists")
            return
        
        # Create admin user
        admin_password = "admin123"  # Change this in production!
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin_user = User(
            email="admin@exam.com",
            password_hash=hashed_password,
            full_name="System Administrator",
            role="admin",
            created_at=datetime.utcnow(),
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Admin user created successfully!")
        print("   Email: admin@exam.com")
        print("   Password: admin123")
        print("   ⚠️  Please change the password in production!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Main migration function"""
    print("=" * 60)
    print("🚀 Database Migration: SQLite → PostgreSQL")
    print("=" * 60)
    
    # Step 1: Initialize PostgreSQL database
    print("\n1️⃣  Initializing PostgreSQL database...")
    try:
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return
    
    # Step 2: Migrate users
    print("\n2️⃣  Migrating data...")
    try:
        migrate_users()
    except Exception as e:
        print(f"❌ Error migrating users: {e}")
    
    # Step 3: Create default admin
    print("\n3️⃣  Setting up admin user...")
    try:
        create_default_admin()
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
    
    print("\n" + "=" * 60)
    print("✨ Migration completed!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Update your .env file with PostgreSQL connection string")
    print("   2. Test the connection by running: python database.py")
    print("   3. Update main.py to use the new database models")
    print("   4. Restart your FastAPI server")
    print("\n")


if __name__ == "__main__":
    main()
