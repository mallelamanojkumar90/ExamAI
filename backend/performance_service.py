"""
Performance Analytics Service
Provides performance tracking, analytics, and insights for students
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database import ExamAttempt, Answer, User, Question
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import statistics


class PerformanceService:
    """Service for calculating and analyzing student performance metrics"""
    
    @staticmethod
    def get_user_performance_summary(user_id: int, db: Session) -> Dict:
        """
        Get comprehensive performance summary for a user
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Dictionary containing performance metrics
        """
        # Get all exam attempts for the user
        attempts = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == user_id
        ).order_by(desc(ExamAttempt.start_time)).all()
        
        if not attempts:
            return {
                "total_exams": 0,
                "average_score": 0,
                "total_questions": 0,
                "correct_answers": 0,
                "accuracy": 0,
                "recent_trend": "neutral",
                "subjects_performance": {},
                "difficulty_performance": {},
                "time_spent_minutes": 0
            }
        
        # Calculate basic metrics
        total_exams = len(attempts)
        total_questions = sum(a.total_questions for a in attempts if a.total_questions)
        correct_answers = sum(a.score for a in attempts if a.score)
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        average_score = correct_answers / total_exams if total_exams > 0 else 0
        
        # Calculate time spent
        time_spent = sum(
            (a.end_time - a.start_time).total_seconds() / 60 
            for a in attempts 
            if a.end_time and a.start_time
        )
        
        # Analyze recent trend (last 5 vs previous 5 exams)
        recent_trend = PerformanceService._calculate_trend(attempts)
        
        # Subject-wise performance
        subjects_performance = PerformanceService._calculate_subject_performance(attempts)
        
        # Difficulty-wise performance
        difficulty_performance = PerformanceService._calculate_difficulty_performance(attempts)
        
        return {
            "total_exams": total_exams,
            "average_score": round(average_score, 2),
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy": round(accuracy, 2),
            "recent_trend": recent_trend,
            "subjects_performance": subjects_performance,
            "difficulty_performance": difficulty_performance,
            "time_spent_minutes": round(time_spent, 2)
        }
    
    @staticmethod
    def _calculate_trend(attempts: List[ExamAttempt]) -> str:
        """Calculate performance trend based on recent attempts"""
        if len(attempts) < 2:
            return "neutral"
        
        # Get last 5 and previous 5 attempts
        recent = attempts[:5]
        previous = attempts[5:10] if len(attempts) > 5 else []
        
        if not previous:
            return "neutral"
        
        recent_avg = statistics.mean([
            (a.score / a.total_questions * 100) if a.total_questions > 0 else 0 
            for a in recent
        ])
        previous_avg = statistics.mean([
            (a.score / a.total_questions * 100) if a.total_questions > 0 else 0 
            for a in previous
        ])
        
        if recent_avg > previous_avg + 5:
            return "improving"
        elif recent_avg < previous_avg - 5:
            return "declining"
        else:
            return "stable"
    
    @staticmethod
    def _calculate_subject_performance(attempts: List[ExamAttempt]) -> Dict:
        """Calculate performance by subject"""
        subject_data = {}
        
        for attempt in attempts:
            # Get exam details to find subject
            if hasattr(attempt, 'exam') and attempt.exam:
                subject = attempt.exam.exam_type  # Using exam_type as subject
            else:
                subject = "Unknown"
            
            if subject not in subject_data:
                subject_data[subject] = {
                    "attempts": 0,
                    "total_questions": 0,
                    "correct_answers": 0,
                    "accuracy": 0
                }
            
            subject_data[subject]["attempts"] += 1
            subject_data[subject]["total_questions"] += attempt.total_questions or 0
            subject_data[subject]["correct_answers"] += attempt.score or 0
        
        # Calculate accuracy for each subject
        for subject in subject_data:
            total_q = subject_data[subject]["total_questions"]
            correct = subject_data[subject]["correct_answers"]
            subject_data[subject]["accuracy"] = round(
                (correct / total_q * 100) if total_q > 0 else 0, 
                2
            )
        
        return subject_data
    
    @staticmethod
    def _calculate_difficulty_performance(attempts: List[ExamAttempt]) -> Dict:
        """Calculate performance by difficulty level"""
        difficulty_data = {
            "easy": {"attempts": 0, "total_questions": 0, "correct_answers": 0, "accuracy": 0},
            "medium": {"attempts": 0, "total_questions": 0, "correct_answers": 0, "accuracy": 0},
            "hard": {"attempts": 0, "total_questions": 0, "correct_answers": 0, "accuracy": 0}
        }
        
        for attempt in attempts:
            # Get exam details to find difficulty
            if hasattr(attempt, 'exam') and attempt.exam:
                # Assuming difficulty is stored in exam metadata or we can infer from score
                difficulty = "medium"  # Default
            else:
                difficulty = "medium"
            
            if difficulty in difficulty_data:
                difficulty_data[difficulty]["attempts"] += 1
                difficulty_data[difficulty]["total_questions"] += attempt.total_questions or 0
                difficulty_data[difficulty]["correct_answers"] += attempt.score or 0
        
        # Calculate accuracy for each difficulty
        for difficulty in difficulty_data:
            total_q = difficulty_data[difficulty]["total_questions"]
            correct = difficulty_data[difficulty]["correct_answers"]
            difficulty_data[difficulty]["accuracy"] = round(
                (correct / total_q * 100) if total_q > 0 else 0, 
                2
            )
        
        return difficulty_data
    
    @staticmethod
    def get_performance_over_time(user_id: int, days: int, db: Session) -> List[Dict]:
        """
        Get performance data over time for charts
        
        Args:
            user_id: User ID
            days: Number of days to look back
            db: Database session
            
        Returns:
            List of daily performance data
        """
        start_date = datetime.now() - timedelta(days=days)
        
        attempts = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == user_id,
            ExamAttempt.start_time >= start_date
        ).order_by(ExamAttempt.start_time).all()
        
        # Group by date
        daily_data = {}
        for attempt in attempts:
            date_key = attempt.start_time.date().isoformat()
            
            if date_key not in daily_data:
                daily_data[date_key] = {
                    "date": date_key,
                    "exams": 0,
                    "total_questions": 0,
                    "correct_answers": 0,
                    "accuracy": 0
                }
            
            daily_data[date_key]["exams"] += 1
            daily_data[date_key]["total_questions"] += attempt.total_questions or 0
            daily_data[date_key]["correct_answers"] += attempt.score or 0
        
        # Calculate accuracy for each day
        for date_key in daily_data:
            total_q = daily_data[date_key]["total_questions"]
            correct = daily_data[date_key]["correct_answers"]
            daily_data[date_key]["accuracy"] = round(
                (correct / total_q * 100) if total_q > 0 else 0, 
                2
            )
        
        return list(daily_data.values())
    
    @staticmethod
    def get_peer_comparison(user_id: int, db: Session) -> Dict:
        """
        Compare user's performance with peers
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Peer comparison data
        """
        # Get user's average score
        user_attempts = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == user_id
        ).all()
        
        if not user_attempts:
            return {
                "user_accuracy": 0,
                "peer_average": 0,
                "percentile": 0,
                "rank": 0,
                "total_users": 0
            }
        
        user_total_q = sum(a.total_questions for a in user_attempts if a.total_questions)
        user_correct = sum(a.score for a in user_attempts if a.score)
        user_accuracy = (user_correct / user_total_q * 100) if user_total_q > 0 else 0
        
        # Get all users' performance
        all_users_performance = db.query(
            ExamAttempt.user_id,
            func.sum(ExamAttempt.score).label('total_correct'),
            func.sum(ExamAttempt.total_questions).label('total_questions')
        ).group_by(ExamAttempt.user_id).all()
        
        # Calculate accuracy for all users
        user_accuracies = []
        for user_perf in all_users_performance:
            if user_perf.total_questions and user_perf.total_questions > 0:
                accuracy = (user_perf.total_correct / user_perf.total_questions * 100)
                user_accuracies.append({
                    "user_id": user_perf.user_id,
                    "accuracy": accuracy
                })
        
        # Sort by accuracy
        user_accuracies.sort(key=lambda x: x["accuracy"], reverse=True)
        
        # Find user's rank
        rank = 0
        for i, user_perf in enumerate(user_accuracies):
            if user_perf["user_id"] == user_id:
                rank = i + 1
                break
        
        # Calculate percentile
        total_users = len(user_accuracies)
        percentile = ((total_users - rank) / total_users * 100) if total_users > 0 else 0
        
        # Calculate peer average (excluding the user)
        peer_accuracies = [u["accuracy"] for u in user_accuracies if u["user_id"] != user_id]
        peer_average = statistics.mean(peer_accuracies) if peer_accuracies else 0
        
        return {
            "user_accuracy": round(user_accuracy, 2),
            "peer_average": round(peer_average, 2),
            "percentile": round(percentile, 2),
            "rank": rank,
            "total_users": total_users
        }
    
    @staticmethod
    def get_strengths_and_weaknesses(user_id: int, db: Session) -> Dict:
        """
        Identify user's strengths and weaknesses
        
        Args:
            user_id: User ID
            db: Database session
            
        Returns:
            Strengths and weaknesses analysis
        """
        # Get subject performance
        attempts = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == user_id
        ).all()
        
        subject_performance = PerformanceService._calculate_subject_performance(attempts)
        
        # Sort subjects by accuracy
        subjects_sorted = sorted(
            subject_performance.items(), 
            key=lambda x: x[1]["accuracy"], 
            reverse=True
        )
        
        # Identify strengths (top 3) and weaknesses (bottom 3)
        strengths = []
        weaknesses = []
        
        for subject, data in subjects_sorted[:3]:
            if data["accuracy"] >= 70:
                strengths.append({
                    "subject": subject,
                    "accuracy": data["accuracy"],
                    "attempts": data["attempts"]
                })
        
        for subject, data in reversed(subjects_sorted[-3:]):
            if data["accuracy"] < 70:
                weaknesses.append({
                    "subject": subject,
                    "accuracy": data["accuracy"],
                    "attempts": data["attempts"]
                })
        
        # Generate recommendations
        recommendations = []
        for weakness in weaknesses:
            recommendations.append(
                f"Focus more on {weakness['subject']} - current accuracy is {weakness['accuracy']}%"
            )
        
        if not recommendations:
            recommendations.append("Great job! Keep practicing to maintain your performance.")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations
        }
    
    @staticmethod
    def get_recent_activity(user_id: int, limit: int, db: Session) -> List[Dict]:
        """
        Get recent exam activity
        
        Args:
            user_id: User ID
            limit: Number of recent activities to fetch
            db: Database session
            
        Returns:
            List of recent activities
        """
        attempts = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == user_id
        ).order_by(desc(ExamAttempt.start_time)).limit(limit).all()
        
        activities = []
        for attempt in attempts:
            accuracy = (attempt.score / attempt.total_questions * 100) if attempt.total_questions > 0 else 0
            
            activities.append({
                "attempt_id": attempt.attempt_id,
                "exam_name": attempt.exam.exam_name if hasattr(attempt, 'exam') and attempt.exam else "Unknown",
                "subject": attempt.exam.exam_type if hasattr(attempt, 'exam') and attempt.exam else "Unknown",
                "score": attempt.score,
                "total_questions": attempt.total_questions,
                "accuracy": round(accuracy, 2),
                "started_at": attempt.start_time.isoformat() if attempt.start_time else None,
                "completed_at": attempt.end_time.isoformat() if attempt.end_time else None,
                "time_taken_minutes": round(
                    (attempt.end_time - attempt.start_time).total_seconds() / 60, 2
                ) if attempt.end_time and attempt.start_time else 0
            })
        
        return activities
