"""
Exam Type Management Service
Handles IIT/JEE, NEET, EAMCET exam configurations
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from database import Exam, Syllabus
from datetime import datetime

# Exam Type Configurations
EXAM_TYPES = {
    "IIT_JEE": {
        "name": "IIT/JEE",
        "full_name": "Joint Entrance Examination",
        "subjects": ["Physics", "Chemistry", "Mathematics"],
        "duration": 180,  # 3 hours
        "total_marks": 300,
        "passing_marks": 90,
        "description": "Engineering entrance exam for IITs, NITs, and other technical institutes",
        "pattern": {
            "total_questions": 75,
            "physics": 25,
            "chemistry": 25,
            "mathematics": 25,
            "marking_scheme": {
                "correct": 4,
                "incorrect": -1,
                "unanswered": 0
            }
        }
    },
    "NEET": {
        "name": "NEET",
        "full_name": "National Eligibility cum Entrance Test",
        "subjects": ["Physics", "Chemistry", "Biology"],
        "duration": 180,  # 3 hours
        "total_marks": 720,
        "passing_marks": 138,
        "description": "Medical entrance exam for MBBS, BDS, and other medical courses",
        "pattern": {
            "total_questions": 180,
            "physics": 45,
            "chemistry": 45,
            "biology": 90,
            "marking_scheme": {
                "correct": 4,
                "incorrect": -1,
                "unanswered": 0
            }
        }
    },
    "EAMCET": {
        "name": "EAMCET",
        "full_name": "Engineering, Agriculture and Medical Common Entrance Test",
        "subjects": ["Physics", "Chemistry", "Mathematics", "Biology"],
        "duration": 180,  # 3 hours
        "total_marks": 160,
        "passing_marks": 40,
        "description": "State-level entrance exam for engineering and medical courses",
        "pattern": {
            "total_questions": 160,
            "physics": 40,
            "chemistry": 40,
            "mathematics": 40,
            "biology": 40,
            "marking_scheme": {
                "correct": 1,
                "incorrect": 0,
                "unanswered": 0
            }
        }
    }
}

# Subject-wise syllabus topics
SYLLABUS_TOPICS = {
    "IIT_JEE": {
        "Physics": [
            "Mechanics",
            "Thermodynamics",
            "Electromagnetism",
            "Optics",
            "Modern Physics",
            "Waves and Sound"
        ],
        "Chemistry": [
            "Physical Chemistry",
            "Organic Chemistry",
            "Inorganic Chemistry",
            "Chemical Bonding",
            "Thermodynamics",
            "Electrochemistry"
        ],
        "Mathematics": [
            "Algebra",
            "Calculus",
            "Trigonometry",
            "Coordinate Geometry",
            "Vectors and 3D Geometry",
            "Probability and Statistics"
        ]
    },
    "NEET": {
        "Physics": [
            "Mechanics",
            "Thermodynamics",
            "Electrodynamics",
            "Optics",
            "Modern Physics",
            "Oscillations and Waves"
        ],
        "Chemistry": [
            "Physical Chemistry",
            "Organic Chemistry",
            "Inorganic Chemistry",
            "Biomolecules",
            "Environmental Chemistry"
        ],
        "Biology": [
            "Cell Biology",
            "Genetics",
            "Ecology",
            "Human Physiology",
            "Plant Physiology",
            "Evolution",
            "Biotechnology"
        ]
    },
    "EAMCET": {
        "Physics": [
            "Mechanics",
            "Heat and Thermodynamics",
            "Electricity and Magnetism",
            "Optics",
            "Modern Physics"
        ],
        "Chemistry": [
            "Atomic Structure",
            "Chemical Bonding",
            "States of Matter",
            "Thermodynamics",
            "Organic Chemistry",
            "Inorganic Chemistry"
        ],
        "Mathematics": [
            "Algebra",
            "Calculus",
            "Trigonometry",
            "Vectors",
            "Probability",
            "Coordinate Geometry"
        ],
        "Biology": [
            "Cell Biology",
            "Genetics",
            "Ecology",
            "Human Anatomy",
            "Plant Biology"
        ]
    }
}


class ExamTypeService:
    """Service for managing exam types and their configurations"""
    
    @staticmethod
    def get_all_exam_types() -> List[Dict]:
        """Get all available exam types"""
        return [
            {
                "id": exam_id,
                "name": config["name"],
                "full_name": config["full_name"],
                "subjects": config["subjects"],
                "description": config["description"],
                "duration": config["duration"],
                "total_marks": config["total_marks"],
                "pattern": config["pattern"]
            }
            for exam_id, config in EXAM_TYPES.items()
        ]
    
    @staticmethod
    def get_exam_type(exam_type_id: str) -> Optional[Dict]:
        """Get specific exam type configuration"""
        if exam_type_id not in EXAM_TYPES:
            return None
        
        config = EXAM_TYPES[exam_type_id]
        return {
            "id": exam_type_id,
            "name": config["name"],
            "full_name": config["full_name"],
            "subjects": config["subjects"],
            "description": config["description"],
            "duration": config["duration"],
            "total_marks": config["total_marks"],
            "passing_marks": config["passing_marks"],
            "pattern": config["pattern"]
        }
    
    @staticmethod
    def get_subjects_for_exam_type(exam_type_id: str) -> List[str]:
        """Get subjects for a specific exam type"""
        if exam_type_id not in EXAM_TYPES:
            return []
        return EXAM_TYPES[exam_type_id]["subjects"]
    
    @staticmethod
    def get_syllabus_for_exam_type(exam_type_id: str, subject: Optional[str] = None) -> Dict:
        """Get syllabus topics for exam type and subject"""
        if exam_type_id not in SYLLABUS_TOPICS:
            return {}
        
        syllabus = SYLLABUS_TOPICS[exam_type_id]
        
        if subject:
            return {subject: syllabus.get(subject, [])}
        
        return syllabus
    
    @staticmethod
    def create_exam_in_db(
        db: Session,
        exam_type_id: str,
        created_by: int
    ) -> Optional[Exam]:
        """Create exam record in database"""
        if exam_type_id not in EXAM_TYPES:
            return None
        
        config = EXAM_TYPES[exam_type_id]
        
        exam = Exam(
            exam_name=config["full_name"],
            exam_type=exam_type_id,
            duration=config["duration"],
            total_marks=config["total_marks"],
            passing_marks=config["passing_marks"],
            created_by=created_by,
            created_at=datetime.utcnow(),
            is_active=True
        )
        
        db.add(exam)
        db.commit()
        db.refresh(exam)
        
        # Create syllabus entries
        syllabus_data = SYLLABUS_TOPICS.get(exam_type_id, {})
        for subject, topics in syllabus_data.items():
            syllabus = Syllabus(
                exam_id=exam.exam_id,
                subject_name=subject,
                topics=topics,
                description=f"{subject} syllabus for {config['name']}",
                created_at=datetime.utcnow()
            )
            db.add(syllabus)
        
        db.commit()
        
        return exam
    
    @staticmethod
    def get_exam_pattern(exam_type_id: str) -> Optional[Dict]:
        """Get exam pattern details"""
        if exam_type_id not in EXAM_TYPES:
            return None
        
        return EXAM_TYPES[exam_type_id]["pattern"]
    
    @staticmethod
    def validate_exam_type(exam_type_id: str) -> bool:
        """Validate if exam type exists"""
        return exam_type_id in EXAM_TYPES
    
    @staticmethod
    def get_marking_scheme(exam_type_id: str) -> Optional[Dict]:
        """Get marking scheme for exam type"""
        if exam_type_id not in EXAM_TYPES:
            return None
        
        return EXAM_TYPES[exam_type_id]["pattern"]["marking_scheme"]
