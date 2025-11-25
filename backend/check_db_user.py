import sqlite3
from main import verify_password

def check_db():
    conn = sqlite3.connect('exam_app.db')
    c = conn.cursor()
    c.execute("SELECT username, password_hash FROM users WHERE username='debugstudent'")
    row = c.fetchone()
    conn.close()
    
    if row:
        username, password_hash = row
        print(f"User: {username}")
        print(f"Hash in DB: {password_hash}")
        
        password = "password123"
        print(f"Testing against password: {password}")
        result = verify_password(password, password_hash)
        print(f"Verification result: {result}")
    else:
        print("User 'debugstudent' not found in DB.")

if __name__ == "__main__":
    check_db()
