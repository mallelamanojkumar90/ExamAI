"""
Agentic Pre-Generation Service
Intelligently predicts and pre-generates questions based on user patterns
"""

import asyncio
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import Counter
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from database import get_db, ExamAttempt, User
from rag_service import RAGAgent
from question_cache_service import get_cache_service
from model_service import ModelService


class AgenticPreGenerationAgent:
    """
    Intelligent agent that analyzes user behavior and pre-generates
    questions to minimize cache misses
    """
    
    def __init__(self):
        self.rag_agent = RAGAgent()
        self.cache_service = get_cache_service()
        self.model_service = ModelService()
        
        # Common exam configurations to always keep cached
        self.priority_configs = [
            # IIT JEE - Most popular
            ("Mathematics", "Medium", 30, "IIT_JEE"),
            ("Physics", "Medium", 30, "IIT_JEE"),
            ("Chemistry", "Medium", 30, "IIT_JEE"),
            ("Mathematics", "Hard", 30, "IIT_JEE"),
            ("Physics", "Hard", 30, "IIT_JEE"),
            
            # NEET - Second most popular
            ("Physics", "Medium", 45, "NEET"),
            ("Chemistry", "Medium", 45, "NEET"),
            ("Biology", "Medium", 45, "NEET"),
            
            # Practice sets
            ("Mathematics", "Easy", 10, "IIT_JEE"),
            ("Physics", "Easy", 10, "IIT_JEE"),
        ]
    
    async def analyze_user_patterns(self, db: Session, days: int = 7) -> List[Tuple]:
        """
        Analyze exam attempts from last N days to find popular patterns
        Returns list of (subject, difficulty, count, exam_type) tuples
        """
        try:
            # Get date threshold
            threshold = datetime.utcnow() - timedelta(days=days)
            
            # Query exam attempts (simplified - you'll need to add subject/difficulty tracking)
            # For now, return priority configs
            print(f"📊 Analyzing user patterns from last {days} days...")
            
            # TODO: When you add subject/difficulty to ExamAttempt table, use this:
            # attempts = db.query(
            #     ExamAttempt.subject,
            #     ExamAttempt.difficulty,
            #     ExamAttempt.total_questions,
            #     func.count(ExamAttempt.attempt_id).label('count')
            # ).filter(
            #     ExamAttempt.start_time >= threshold
            # ).group_by(
            #     ExamAttempt.subject,
            #     ExamAttempt.difficulty,
            #     ExamAttempt.total_questions
            # ).order_by(desc('count')).limit(20).all()
            
            # For now, return priority configs
            return self.priority_configs
            
        except Exception as e:
            print(f"⚠️  Pattern analysis error: {e}")
            return self.priority_configs
    
    async def predict_next_requests(self, current_hour: int, current_day: int) -> List[Tuple]:
        """
        Predict likely requests based on time patterns
        
        Args:
            current_hour: Hour of day (0-23)
            current_day: Day of week (0=Monday, 6=Sunday)
        
        Returns:
            List of predicted (subject, difficulty, count, exam_type) tuples
        """
        predictions = []
        
        # Peak study hours: 6-9 AM, 2-5 PM, 7-11 PM
        is_peak_hour = (6 <= current_hour <= 9) or (14 <= current_hour <= 17) or (19 <= current_hour <= 23)
        
        # Weekday vs Weekend patterns
        is_weekend = current_day >= 5
        
        if is_peak_hour:
            # During peak hours, prioritize all difficulty levels
            predictions.extend(self.priority_configs)
        else:
            # Off-peak: focus on medium difficulty
            predictions.extend([
                config for config in self.priority_configs 
                if config[1] == "Medium"
            ])
        
        if is_weekend:
            # Weekends: more practice tests
            predictions.extend([
                ("Mathematics", "Easy", 10, "IIT_JEE"),
                ("Physics", "Easy", 10, "IIT_JEE"),
                ("Chemistry", "Easy", 10, "IIT_JEE"),
            ])
        
        return predictions
    
    async def schedule_pregeneration(
        self, 
        configs: List[Tuple],
        batch_size: int = 3
    ):
        """
        Schedule background pre-generation for given configurations
        
        Args:
            configs: List of (subject, difficulty, count, exam_type) tuples
            batch_size: Number of configs to process in parallel
        """
        print(f"\n🤖 AGENTIC PRE-GENERATION STARTED")
        print(f"   Configurations to generate: {len(configs)}")
        print(f"   Batch size: {batch_size}")
        
        # Process in batches to avoid overloading
        for i in range(0, len(configs), batch_size):
            batch = configs[i:i+batch_size]
            tasks = [self._generate_and_cache(*config) for config in batch]
            
            try:
                await asyncio.gather(*tasks)
                print(f"   ✅ Batch {i//batch_size + 1} completed")
            except Exception as e:
                print(f"   ⚠️  Batch {i//batch_size + 1} error: {e}")
            
            # Small delay between batches
            await asyncio.sleep(2)
        
        print(f"🤖 AGENTIC PRE-GENERATION COMPLETED\n")
    
    async def _generate_and_cache(
        self, 
        subject: str, 
        difficulty: str, 
        count: int, 
        exam_type: str
    ):
        """
        Generate questions and store in cache
        """
        try:
            # Check if already cached
            cache_key = self.cache_service.generate_cache_key(
                subject, difficulty, count, exam_type
            )
            
            if self.cache_service.get_cached_questions(cache_key):
                print(f"   ⏭️  Skipping {subject}/{difficulty}/{count} - already cached")
                return
            
            # Generate questions
            print(f"   🔄 Generating {subject}/{difficulty}/{count}...")
            questions = await self.rag_agent.generate_questions(
                subject=subject,
                difficulty=difficulty,
                count=count,
                exam_type=exam_type
            )
            
            # Cache the results
            success = self.cache_service.set_cached_questions(cache_key, questions)
            
            if success:
                print(f"   ✅ Cached {subject}/{difficulty}/{count}")
            else:
                print(f"   ⚠️  Failed to cache {subject}/{difficulty}/{count}")
                
        except Exception as e:
            print(f"   ❌ Error generating {subject}/{difficulty}/{count}: {e}")
    
    async def monitor_and_adapt(self, db: Session):
        """
        Monitor cache performance and adapt strategy
        """
        try:
            stats = self.cache_service.get_cache_stats()
            
            if not stats.get("enabled"):
                return
            
            hit_rate = stats.get("hit_rate_percentage", 0)
            
            print(f"\n📈 CACHE PERFORMANCE MONITORING")
            print(f"   Hit Rate: {hit_rate}%")
            print(f"   Total Hits: {stats.get('total_hits', 0)}")
            print(f"   Total Misses: {stats.get('total_misses', 0)}")
            print(f"   Cached Sets: {stats.get('total_cached_sets', 0)}")
            
            # Adapt strategy based on hit rate
            if hit_rate < 70:
                print(f"   ⚠️  Hit rate below 70% - increasing pre-generation")
                # Analyze patterns and pre-generate more
                patterns = await self.analyze_user_patterns(db, days=3)
                await self.schedule_pregeneration(patterns, batch_size=5)
            elif hit_rate > 90:
                print(f"   ✅ Hit rate excellent - maintaining current strategy")
            
            print()
            
        except Exception as e:
            print(f"⚠️  Monitoring error: {e}")
    
    async def warm_cache_on_startup(self):
        """
        Warm cache with priority configurations on application startup
        """
        print(f"\n🔥 WARMING CACHE ON STARTUP...")
        await self.schedule_pregeneration(self.priority_configs[:5], batch_size=2)
        print(f"🔥 CACHE WARMING COMPLETED\n")
    
    async def run_periodic_pregeneration(self, interval_minutes: int = 30):
        """
        Run periodic pre-generation in background
        
        Args:
            interval_minutes: How often to run (default: 30 minutes)
        """
        while True:
            try:
                # Get current time context
                now = datetime.now()
                current_hour = now.hour
                current_day = now.weekday()
                
                # Predict and pre-generate
                predictions = await self.predict_next_requests(current_hour, current_day)
                await self.schedule_pregeneration(predictions, batch_size=3)
                
                # Monitor performance
                db = next(get_db())
                await self.monitor_and_adapt(db)
                
            except Exception as e:
                print(f"⚠️  Periodic pre-generation error: {e}")
            
            # Wait for next interval
            await asyncio.sleep(interval_minutes * 60)


# Global instance
_pregeneration_agent = None

def get_pregeneration_agent() -> AgenticPreGenerationAgent:
    """Get or create pre-generation agent singleton"""
    global _pregeneration_agent
    if _pregeneration_agent is None:
        _pregeneration_agent = AgenticPreGenerationAgent()
    return _pregeneration_agent
