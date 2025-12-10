"""
Create Admin User Script
Run this script to create an admin user for ExamAI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, User
from datetime import datetime
import bcrypt

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt"""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def create_admin():
    """Create an admin user"""
    db = SessionLocal()
    
    try:
        # Admin credentials
        admin_email = input("Enter admin email: ")
        admin_password = input("Enter admin password: ")
        admin_name = input("Enter admin full name: ")
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == admin_email).first()
        if existing_user:
            print(f"\n⚠️  User with email {admin_email} already exists!")
            update = input("Do you want to update this user to admin role? (yes/no): ")
            if update.lower() == 'yes':
                existing_user.role = "admin"
                db.commit()
                print(f"✅ User {admin_email} updated to admin role!")
                return
            else:
                print("❌ Operation cancelled.")
                return
        
        # Create new admin user
        hashed_password = get_password_hash(admin_password)
        admin_user = User(
            email=admin_email,
            password_hash=hashed_password,
            full_name=admin_name,
            role="admin",  # Set role as admin
            created_at=datetime.utcnow(),
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"\n✅ Admin user created successfully!")
        print(f"Email: {admin_email}")
        print(f"Role: admin")
        print(f"\nYou can now login at: http://localhost:3000/auth/login")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("ExamAI - Create Admin User")
    print("=" * 50)
    create_admin()
