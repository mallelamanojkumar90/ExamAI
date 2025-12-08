"""
Database configuration and models for PostgreSQL
Following PRD Section 9.1 - Database Design (ORM)
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///exam_app.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# ============================================================================
# PRD Section 9.1 - Core Entities
# ============================================================================

class User(Base):
    """Users Table - PRD Section 9.1"""
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="student")  # student/admin
    phone_number = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    exam_attempts = relationship("ExamAttempt", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    reports = relationship("Report", back_populates="user")


class Exam(Base):
    """Exams Table - PRD Section 9.1"""
    __tablename__ = "exams"
    
    exam_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exam_name = Column(String(255), nullable=False)
    exam_type = Column(String(100))  # IIT/JEE, NEET, EAMCET, etc.
    duration = Column(Integer)  # in minutes
    total_marks = Column(Integer)
    passing_marks = Column(Integer)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    syllabi = relationship("Syllabus", back_populates="exam")
    questions = relationship("Question", back_populates="exam")
    exam_attempts = relationship("ExamAttempt", back_populates="exam")
    study_materials = relationship("StudyMaterial", back_populates="exam")
    reports = relationship("Report", back_populates="exam")


class Syllabus(Base):
    """Syllabus Table - PRD Section 9.1"""
    __tablename__ = "syllabus"
    
    syllabus_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.exam_id"))
    subject_name = Column(String(255), nullable=False)
    topics = Column(JSON)  # Store topics as JSON array
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    exam = relationship("Exam", back_populates="syllabi")


class Question(Base):
    """Questions Table - PRD Section 9.1"""
    __tablename__ = "questions"
    
    question_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.exam_id"))
    subject = Column(String(255))
    topic = Column(String(255))
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50))  # MCQ, numerical, descriptive
    difficulty_level = Column(String(50))  # easy, medium, hard
    options = Column(JSON)  # Store options as JSON array
    correct_answer = Column(String(255))
    marks = Column(Integer)
    negative_marks = Column(Float, default=0.0)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    exam = relationship("Exam", back_populates="questions")
    answers = relationship("Answer", back_populates="question")


class ExamAttempt(Base):
    """Exam_Attempts Table - PRD Section 9.1"""
    __tablename__ = "exam_attempts"
    
    attempt_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    exam_id = Column(Integer, ForeignKey("exams.exam_id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    score = Column(Float)
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    incorrect_answers = Column(Integer)
    unanswered = Column(Integer)
    status = Column(String(50), default="in_progress")  # completed/in_progress
    
    # Relationships
    user = relationship("User", back_populates="exam_attempts")
    exam = relationship("Exam", back_populates="exam_attempts")
    answers = relationship("Answer", back_populates="attempt")
    reports = relationship("Report", back_populates="attempt")


class Answer(Base):
    """Answers Table - PRD Section 9.1"""
    __tablename__ = "answers"
    
    answer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    attempt_id = Column(Integer, ForeignKey("exam_attempts.attempt_id"))
    question_id = Column(Integer, ForeignKey("questions.question_id"))
    user_answer = Column(String(255))
    is_correct = Column(Boolean)
    time_taken = Column(Integer)  # in seconds
    marked_for_review = Column(Boolean, default=False)
    
    # Relationships
    attempt = relationship("ExamAttempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")


class StudyMaterial(Base):
    """Study_Materials Table - PRD Section 9.1"""
    __tablename__ = "study_materials"
    
    material_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    file_url = Column(String(500))
    material_type = Column(String(50))  # PDF, video, etc.
    subject = Column(String(255))
    topic = Column(String(255))
    exam_id = Column(Integer, ForeignKey("exams.exam_id"))
    uploaded_by = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    exam = relationship("Exam", back_populates="study_materials")


class Subscription(Base):
    """Subscriptions Table - PRD Section 9.1"""
    __tablename__ = "subscriptions"
    
    subscription_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    plan_type = Column(String(50))  # monthly/quarterly/annual
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    amount = Column(Float)
    payment_status = Column(String(50))  # active/expired/cancelled
    auto_renew = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription")


class Payment(Base):
    """Payments Table - PRD Section 9.1"""
    __tablename__ = "payments"
    
    payment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.subscription_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(Float)
    payment_method = Column(String(50))
    transaction_id = Column(String(255), unique=True)
    status = Column(String(50))  # success/failed/pending
    payment_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    subscription = relationship("Subscription", back_populates="payments")
    user = relationship("User", back_populates="payments")


class Report(Base):
    """Reports Table - PRD Section 9.1"""
    __tablename__ = "reports"
    
    report_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    exam_id = Column(Integer, ForeignKey("exams.exam_id"))
    attempt_id = Column(Integer, ForeignKey("exam_attempts.attempt_id"))
    report_url = Column(String(500))  # PDF URL
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reports")
    exam = relationship("Exam", back_populates="reports")
    attempt = relationship("ExamAttempt", back_populates="reports")


# ============================================================================
# Database Initialization
# ============================================================================

def init_db():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
