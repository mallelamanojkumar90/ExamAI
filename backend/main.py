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
from model_service import ModelService
from database import (
    get_db, init_db, User, Exam, Question, ExamAttempt, 
    Answer, StudyMaterial, Subscription, Payment, Report
)
from subscription_routes import router as subscription_router
from performance_routes import router as performance_router

# Import caching and pre-generation services
from question_cache_service import get_cache_service
from agentic_pregeneration_service import get_pregeneration_agent

from exam_type_service import ExamTypeService

app = FastAPI(title="ExamAI RAG Backend - PostgreSQL")

# Include subscription routes
app.include_router(subscription_router)

# Include performance analytics routes
app.include_router(performance_router)



# Include exam pattern management routes


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
cache_service = get_cache_service()
pregeneration_agent = get_pregeneration_agent()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting ExamAI Backend...")
    init_db()
    print("✅ Database initialized!")
    
    # Warm cache with priority questions
    if cache_service.is_enabled():
        print("🔥 Warming question cache...")
        import asyncio
        asyncio.create_task(pregeneration_agent.warm_cache_on_startup())
        print("✅ Cache warming initiated!")
    else:
        print("⚠️  Redis cache disabled - questions will be generated in real-time")

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
    exam_type: Optional[str] = None
    model_provider: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[float] = None

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
    return {
        "message": "Login successful", 
        "username": user.username, 
        "full_name": db_user.full_name,
        "role": db_user.role, 
        "user_id": db_user.user_id
    }

class GoogleSignIn(BaseModel):
    email: str
    name: Optional[str] = None
    google_id: str

@app.post("/auth/google-signin")
def google_signin(google_user: GoogleSignIn, db: Session = Depends(get_db)):
    """Handle Google OAuth sign-in"""
    print(f"🔵 Google sign-in attempt: {google_user.email}")
    
    try:
        # Check if user exists
        db_user = db.query(User).filter(User.email == google_user.email).first()
        
        if db_user:
            # Update Google ID if not set
            if not db_user.google_id:
                db_user.google_id = google_user.google_id
            
            # Update last login
            db_user.last_login = datetime.utcnow()
            db.commit()
            
            print(f"✅ Existing user logged in via Google: {google_user.email}")
        else:
            # Create new user
            db_user = User(
                email=google_user.email,
                password_hash="",  # No password for OAuth users
                full_name=google_user.name,
                google_id=google_user.google_id,
                role="student",
                created_at=datetime.utcnow(),
                last_login=datetime.utcnow(),
                is_active=True
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            print(f"✅ New user created via Google: {google_user.email}")
        
        return {
            "message": "Google sign-in successful",
            "username": db_user.email,
            "full_name": db_user.full_name,
            "role": db_user.role,
            "user_id": db_user.user_id
        }
    except Exception as e:
        import traceback
        print(f"❌ Google sign-in error: {str(e)}")
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Google sign-in failed: {str(e)}")


# ============================================================================
# Exam Type Management Endpoints
# ============================================================================

@app.get("/exam-types")
def get_exam_types():
    """Get all available exam types (IIT/JEE, NEET, EAMCET)"""
    try:
        exam_types = ExamTypeService.get_all_exam_types()
        return {"exam_types": exam_types}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exam-types/{exam_type_id}")
def get_exam_type(exam_type_id: str):
    """Get specific exam type details"""
    try:
        exam_type = ExamTypeService.get_exam_type(exam_type_id)
        if not exam_type:
            raise HTTPException(status_code=404, detail="Exam type not found")
        return exam_type
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exam-types/{exam_type_id}/subjects")
def get_exam_subjects(exam_type_id: str):
    """Get subjects for a specific exam type"""
    try:
        subjects = ExamTypeService.get_subjects_for_exam_type(exam_type_id)
        if not subjects:
            raise HTTPException(status_code=404, detail="Exam type not found")
        return {"exam_type": exam_type_id, "subjects": subjects}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exam-types/{exam_type_id}/syllabus")
def get_exam_syllabus(exam_type_id: str, subject: Optional[str] = None):
    """Get syllabus for exam type and optional subject"""
    try:
        syllabus = ExamTypeService.get_syllabus_for_exam_type(exam_type_id, subject)
        if not syllabus:
            raise HTTPException(status_code=404, detail="Syllabus not found")
        return {"exam_type": exam_type_id, "syllabus": syllabus}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/exams/create")
def create_exam(exam_type_id: str, db: Session = Depends(get_db)):
    """Create an exam based on exam type"""
    try:
        # For now, use a default admin user ID (1)
        # TODO: Get from authenticated user
        exam = ExamTypeService.create_exam_in_db(db, exam_type_id, created_by=1)
        if not exam:
            raise HTTPException(status_code=400, detail="Invalid exam type")
        
        return {
            "message": "Exam created successfully",
            "exam_id": exam.exam_id,
            "exam_type": exam.exam_type,
            "exam_name": exam.exam_name
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Model Management Endpoints
# ============================================================================

@app.get("/models")
def get_available_models():
    """Get all available AI models"""
    try:
        models = ModelService.list_available_models()
        return {
            "models": models,
            "default": ModelService.get_default_config()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/{provider}")
def get_provider_models(provider: str):
    """Get models for a specific provider"""
    try:
        all_models = ModelService.list_available_models()
        if provider not in all_models:
            raise HTTPException(status_code=404, detail=f"Provider {provider} not found")
        return all_models[provider]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Question Generation Endpoints
# ============================================================================

@app.post("/generate-questions", response_model=List[QuestionResponse])
async def generate_questions(request: QuestionRequest):
    """Generate questions using RAG with optional model selection and caching"""
    try:
        # 1. Generate cache key
        cache_key = cache_service.generate_cache_key(
            subject=request.subject,
            difficulty=request.difficulty,
            count=request.count,
            exam_type=request.exam_type,
            model_provider=request.model_provider,
            model_name=request.model_name
        )
        
        # 2. Check cache first
        cached_questions = cache_service.get_cached_questions(cache_key)
        if cached_questions:
            print(f"⚡ INSTANT DELIVERY: Returning {len(cached_questions)} cached questions")
            return cached_questions
        
        # 3. Cache miss - generate in real-time
        print(f"🔄 Cache miss - generating questions in real-time...")
        questions = await rag_agent.generate_questions(
            subject=request.subject,
            difficulty=request.difficulty,
            count=request.count,
            exam_type=request.exam_type,
            model_provider=request.model_provider,
            model_name=request.model_name,
            temperature=request.temperature
        )
        
        # 4. Store in cache for future requests
        cache_service.set_cached_questions(cache_key, questions)
        
        # 5. Trigger background pre-generation for similar patterns
        # (This helps pre-generate related difficulty levels)
        if request.difficulty == "Medium":
            asyncio.create_task(pregeneration_agent._generate_and_cache(
                request.subject, "Easy", request.count, request.exam_type or "IIT_JEE"
            ))
            asyncio.create_task(pregeneration_agent._generate_and_cache(
                request.subject, "Hard", request.count, request.exam_type or "IIT_JEE"
            ))
        
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Exam Management Endpoints
# ============================================================================

@app.post("/submit-exam")
def submit_exam(result: ExamResultSubmit, db: Session = Depends(get_db)):
    """Submit exam results"""
    print(f"📥 Received exam submission for: {result.username}")
    try:
        # Find user
        user = db.query(User).filter(User.email == result.username).first()
        if not user:
            print(f"❌ User not found: {result.username}")
            raise HTTPException(status_code=404, detail=f"User {result.username} not found")
        
        print(f"👤 Found user: {user.user_id}, saving attempt...")
        
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
        print(f"✅ Exam result saved successfully for {result.username}")
        
        return {"message": "Exam result saved successfully"}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Error saving exam result: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

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
            "topic": m.topic,  # This stores the exam_type
            "upload_date": m.created_at.isoformat() if m.created_at else None
        } for m in materials]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...), 
    subject: str = Form("mixed"),
    exam_type: str = Form("IIT_JEE"),
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
            description=f"Uploaded document for {subject} - {exam_type}",
            file_url=file_path,
            material_type="PDF",
            subject=f"{exam_type}:{subject}",  # Store exam_type with subject
            topic=exam_type,  # Store exam_type in topic field
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
# Cache Management Endpoints
# ============================================================================

@app.get("/cache/stats")
def get_cache_stats():
    """Get cache performance statistics"""
    try:
        stats = cache_service.get_cache_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cache/warm")
async def warm_cache(
    subject: str,
    difficulty: str,
    count: int,
    exam_type: Optional[str] = "IIT_JEE"
):
    """Admin endpoint to manually warm cache with specific configuration"""
    try:
        # Generate questions
        questions = await rag_agent.generate_questions(
            subject=subject,
            difficulty=difficulty,
            count=count,
            exam_type=exam_type
        )
        
        # Cache them
        success = cache_service.warm_cache(subject, difficulty, count, questions, exam_type)
        
        if success:
            return {
                "status": "success",
                "message": f"Cached {len(questions)} questions for {subject}/{difficulty}/{count}",
                "cached_count": len(questions)
            }
        else:
            return {
                "status": "failed",
                "message": "Cache is disabled or error occurred"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cache/invalidate")
def invalidate_cache(pattern: str = "questions:*"):
    """Admin endpoint to invalidate cache entries"""
    try:
        deleted = cache_service.invalidate_cache(pattern)
        return {
            "status": "success",
            "message": f"Invalidated {deleted} cache entries",
            "deleted_count": deleted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cache/pregenerate")
async def trigger_pregeneration():
    """Admin endpoint to trigger background pre-generation"""
    try:
        import asyncio
        asyncio.create_task(pregeneration_agent.warm_cache_on_startup())
        return {
            "status": "success",
            "message": "Background pre-generation triggered"
        }
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
