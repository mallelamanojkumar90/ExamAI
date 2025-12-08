from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
import sqlite3
import bcrypt
from rag_service import RAGAgent

app = FastAPI(title="ExamAI RAG Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
def verify_password(plain_password, hashed_password):
    password_byte = plain_password.encode('utf-8')
    hashed_password_byte = hashed_password.encode('utf-8')
    print(f"Verifying: plain={plain_password}, hash={hashed_password}")
    try:
        result = bcrypt.checkpw(password_byte, hashed_password_byte)
        print(f"Verification result: {result}")
        return result
    except Exception as e:
        print(f"Verification error: {e}")
        return False

def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

# Database Setup
DB_NAME = "exam_app.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            full_name TEXT
        )
    ''')
    # Documents table
    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            subject TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Exam Results table
    c.execute('''
        CREATE TABLE IF NOT EXISTS exam_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            subject TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Initialize RAG Agent
rag_agent = RAGAgent()

# Data Models
class QuestionRequest(BaseModel):
    subject: str
    difficulty: str
    count: int

class Question(BaseModel):
    id: str
    text: str
    options: List[str]
    correctAnswer: int
    explanation: Optional[str] = None

class ExamResult(BaseModel):
    username: str
    subject: str
    difficulty: str
    score: int
    total_questions: int

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

# ... (existing endpoints) ...

@app.post("/submit-exam")
def submit_exam(result: ExamResult):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO exam_results (username, subject, difficulty, score, total_questions)
            VALUES (?, ?, ?, ?, ?)
        ''', (result.username, result.subject, result.difficulty, result.score, result.total_questions))
        conn.commit()
        conn.close()
        return {"message": "Exam result saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/users")
def get_users():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        # Get users and their latest activity time
        c.execute('''
            SELECT u.username, u.full_name, 
                   MAX(e.timestamp) as last_active,
                   COUNT(e.id) as exams_taken
            FROM users u
            LEFT JOIN exam_results e ON u.username = e.username
            GROUP BY u.username
        ''')
        users = [dict(row) for row in c.fetchall()]
        conn.close()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/user/{username}/activity")
def get_user_activity(username: str):
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''
            SELECT * FROM exam_results 
            WHERE username = ? 
            ORDER BY timestamp DESC
        ''', (username,))
        activity = [dict(row) for row in c.fetchall()]
        conn.close()
        return activity
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "online", "message": "ExamAI RAG Backend is running"}

@app.post("/auth/signup")
def signup(user: UserCreate):
    print(f"Signup attempt: {user.username}")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        hashed_password = get_password_hash(user.password)
        print(f"Generated hash: {hashed_password}")
        c.execute("INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)",
                  (user.username, hashed_password, user.full_name))
        conn.commit()
        print("User created successfully")
        return {"message": "User created successfully"}
    except sqlite3.IntegrityError:
        print("Username already registered")
        raise HTTPException(status_code=400, detail="Username already registered")
    finally:
        conn.close()

@app.post("/auth/login")
def login(user: UserLogin):
    print(f"Login attempt: {user.username}")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (user.username,))
    result = c.fetchone()
    conn.close()

    if not result:
        print("User not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"Found hash in DB: {result[0]}")
    if not verify_password(user.password, result[0]):
        print("Password verification failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print("Login successful")
    return {"message": "Login successful", "username": user.username}

@app.post("/generate-questions", response_model=List[Question])
def generate_questions(request: QuestionRequest):
    try:
        questions = rag_agent.generate_questions(
            subject=request.subject,
            difficulty=request.difficulty,
            count=request.count
        )
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def get_documents():
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM documents ORDER BY upload_date DESC")
        documents = [dict(row) for row in c.fetchall()]
        conn.close()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...), subject: str = Form("mixed")):
    try:
        # Save file temporarily
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Trigger RAG ingestion
        success = rag_agent.ingest_document(file_path, subject)
        
        if not success:
            return {
                "filename": file.filename, 
                "subject": subject, 
                "status": "warning", 
                "message": "File uploaded but no text extracted. This appears to be a scanned PDF. Please use a searchable PDF."
            }
        
        # Record in database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO documents (filename, subject) VALUES (?, ?)", (file.filename, subject))
        conn.commit()
        conn.close()
        
        return {"filename": file.filename, "subject": subject, "status": "indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug/index-stats")
def get_index_stats():
    """Debug endpoint to check Pinecone index statistics"""
    try:
        stats = rag_agent.index.describe_index_stats()
        # Convert to dict to avoid recursion error in FastAPI/Pydantic on Py3.14
        stats_dict = {
            "total_vector_count": stats.total_vector_count,
            "dimension": getattr(stats, "dimension", 0),
            "index_fullness": getattr(stats, "index_fullness", 0.0),
            "namespaces": {
                k: {"vector_count": v.vector_count} 
                for k, v in stats.namespaces.items()
            }
        }
        return {
            "status": "success",
            "stats": stats_dict,
            "message": "Check the namespaces and total_vector_count to see what's in your index"
        }
    except Exception as e:
        print(f"Error fetching index stats: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Use PORT environment variable if set, otherwise default to 8000
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
