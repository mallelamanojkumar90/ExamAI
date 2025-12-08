"""
Updated FastAPI backend with PostgreSQL support
Following PRD requirements for database structure
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import shutil
import os
import bcrypt
from rag_service import RAGAgent
from database import (
    get_db, init_db, User, Exam, Question, ExamAttempt, 
    Answer, StudyMaterial, Subscription, Payment, Report
)

app = FastAPI(title="ExamAI RAG Backend - PostgreSQL")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    print("🚀 Starting ExamAI Backend...")
    init_db()
    print("✅ Database initialized!")

# Security functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        password_byte = plain_password.encode('utf-8')
        hashed_password_byte = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_byte, hashed_password_byte)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt"""
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

# Initialize RAG Agent
rag_agent = RAGAgent()

# ============================================================================
# Pydantic Models (Request/Response)
# ============================================================================

class QuestionRequest(BaseModel):
    subject: str
    difficulty: str
    count: int

class QuestionResponse(BaseModel):
    id: str
    text: str
    options: List[str]
    correctAnswer: int
    explanation: Optional[str] = None

class ExamResultSubmit(BaseModel):
    username: str
    subject: str
    difficulty: str
    score: int
    total_questions: int

class UserCreate(BaseModel):
    username: str  # Will be used as email
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str  # Will be used as email
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.post("/auth/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    print(f"Signup attempt: {user.username}")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.username,
        password_hash=hashed_password,
        full_name=user.full_name,
        role="student",
        created_at=datetime.utcnow(),
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"✅ User created: {user.username}")
    return {"message": "User created successfully"}

@app.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    print(f"Login attempt: {user.username}")
    
    # Find user
    db_user = db.query(User).filter(User.email == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    db_user.last_login = datetime.utcnow()
    db.commit()
    
    print(f"✅ Login successful: {user.username}")
    return {"message": "Login successful", "username": user.username, "role": db_user.role}

# ============================================================================
# Question Generation Endpoints
# ============================================================================

@app.post("/generate-questions", response_model=List[QuestionResponse])
def generate_questions(request: QuestionRequest):
    """Generate questions using RAG"""
    try:
        questions = rag_agent.generate_questions(
            subject=request.subject,
            difficulty=request.difficulty,
            count=request.count
        )
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Exam Management Endpoints
# ============================================================================

@app.post("/submit-exam")
def submit_exam(result: ExamResultSubmit, db: Session = Depends(get_db)):
    """Submit exam results"""
    try:
        # Find user
        user = db.query(User).filter(User.email == result.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # For now, create a basic exam attempt record
        # TODO: Link to actual exam_id when exam management is implemented
        exam_attempt = ExamAttempt(
            user_id=user.user_id,
            exam_id=None,  # Will be set when exam management is implemented
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow(),
            score=result.score,
            total_questions=result.total_questions,
            correct_answers=result.score,
            incorrect_answers=result.total_questions - result.score,
            unanswered=0,
            status="completed"
        )
        
        db.add(exam_attempt)
        db.commit()
        
        return {"message": "Exam result saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Document Management Endpoints
# ============================================================================

@app.get("/documents")
async def get_documents(db: Session = Depends(get_db)):
    """Get all uploaded documents"""
    try:
        materials = db.query(StudyMaterial).order_by(StudyMaterial.created_at.desc()).all()
        return [{
            "id": m.material_id,
            "filename": m.title,
            "subject": m.subject,
            "upload_date": m.created_at.isoformat() if m.created_at else None
        } for m in materials]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...), 
    subject: str = Form("mixed"),
    db: Session = Depends(get_db)
):
    """Upload and process document"""
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
                "message": "File uploaded but no text extracted. This appears to be a scanned PDF."
            }
        
        # Record in database
        study_material = StudyMaterial(
            title=file.filename,
            description=f"Uploaded document for {subject}",
            file_url=file_path,
            material_type="PDF",
            subject=subject,
            topic=None,
            exam_id=None,  # Will be set when exam management is implemented
            uploaded_by=None,  # TODO: Get from authenticated user
            created_at=datetime.utcnow()
        )
        
        db.add(study_material)
        db.commit()
        
        return {"filename": file.filename, "subject": subject, "status": "indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Admin Endpoints
# ============================================================================

@app.get("/admin/users")
def get_users(db: Session = Depends(get_db)):
    """Get all users with activity stats"""
    try:
        users = db.query(User).filter(User.role == "student").all()
        
        result = []
        for user in users:
            # Get exam count
            exam_count = db.query(ExamAttempt).filter(ExamAttempt.user_id == user.user_id).count()
            
            # Get last activity
            last_attempt = db.query(ExamAttempt).filter(
                ExamAttempt.user_id == user.user_id
            ).order_by(ExamAttempt.end_time.desc()).first()
            
            result.append({
                "username": user.email,
                "full_name": user.full_name,
                "last_active": last_attempt.end_time.isoformat() if last_attempt and last_attempt.end_time else None,
                "exams_taken": exam_count
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/user/{username}/activity")
def get_user_activity(username: str, db: Session = Depends(get_db)):
    """Get user activity history"""
    try:
        user = db.query(User).filter(User.email == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        attempts = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == user.user_id
        ).order_by(ExamAttempt.end_time.desc()).all()
        
        return [{
            "id": a.attempt_id,
            "subject": "N/A",  # TODO: Get from exam when implemented
            "difficulty": "N/A",
            "score": a.score,
            "total_questions": a.total_questions,
            "timestamp": a.end_time.isoformat() if a.end_time else None
        } for a in attempts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Debug Endpoints
# ============================================================================

@app.get("/debug/index-stats")
def get_index_stats():
    """Debug endpoint to check Pinecone index statistics"""
    try:
        stats = rag_agent.index.describe_index_stats()
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
            "message": "Check the namespaces and total_vector_count"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "ExamAI RAG Backend is running",
        "database": "PostgreSQL"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
