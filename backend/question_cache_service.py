"""
Question Cache Service using Redis
Provides instant question delivery by caching pre-generated questions
"""

import redis
import json
import hashlib
import os
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class QuestionCacheService:
    def __init__(self):
        """Initialize Redis connection"""
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", "6379"))
        self.redis_db = int(os.getenv("REDIS_DB", "0"))
        self.redis_password = os.getenv("REDIS_PASSWORD", None)
        self.cache_ttl = int(os.getenv("CACHE_TTL_SECONDS", "1800"))  # 30 minutes default
        
        try:
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                password=self.redis_password,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            print(f"✅ Redis connected: {self.redis_host}:{self.redis_port}")
        except redis.ConnectionError as e:
            print(f"⚠️  Redis connection failed: {e}")
            print("   Cache will be disabled. Questions will be generated in real-time.")
            self.redis_client = None
        except Exception as e:
            print(f"⚠️  Redis initialization error: {e}")
            self.redis_client = None
    
    def generate_cache_key(
        self, 
        subject: str, 
        difficulty: str, 
        count: int, 
        exam_type: Optional[str] = None,
        model_provider: Optional[str] = None,
        model_name: Optional[str] = None
    ) -> str:
        """
        Generate a unique cache key for question set
        Format: questions:{hash}
        """
        # Create a deterministic key from parameters
        key_parts = [
            subject.lower().strip(),
            difficulty.lower().strip(),
            str(count),
            exam_type.lower().strip() if exam_type else "general",
            model_provider.lower().strip() if model_provider else "default",
            model_name.lower().strip() if model_name else "default"
        ]
        
        # Create hash for shorter key
        key_string = ":".join(key_parts)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()[:12]
        
        return f"questions:{key_hash}:{key_string}"
    
    def get_cached_questions(self, cache_key: str) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve questions from cache
        Returns None if not found or cache disabled
        """
        if not self.redis_client:
            return None
        
        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                # Update access metadata
                self._update_access_metadata(cache_key, hit=True)
                print(f"✅ CACHE HIT: {cache_key}")
                return json.loads(cached_data)
            else:
                self._update_access_metadata(cache_key, hit=False)
                print(f"❌ CACHE MISS: {cache_key}")
                return None
        except Exception as e:
            print(f"⚠️  Cache retrieval error: {e}")
            return None
    
    def set_cached_questions(
        self, 
        cache_key: str, 
        questions: List[Dict[str, Any]], 
        ttl: Optional[int] = None
    ) -> bool:
        """
        Store questions in cache with TTL
        Returns True if successful
        """
        if not self.redis_client:
            return False
        
        try:
            ttl = ttl or self.cache_ttl
            serialized = json.dumps(questions)
            self.redis_client.setex(cache_key, ttl, serialized)
            
            # Store metadata
            self._store_metadata(cache_key, len(questions))
            
            print(f"💾 CACHED: {cache_key} ({len(questions)} questions, TTL: {ttl}s)")
            return True
        except Exception as e:
            print(f"⚠️  Cache storage error: {e}")
            return False
    
    def invalidate_cache(self, pattern: str = "questions:*") -> int:
        """
        Invalidate cache entries matching pattern
        Returns number of keys deleted
        """
        if not self.redis_client:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                deleted = self.redis_client.delete(*keys)
                print(f"🗑️  Invalidated {deleted} cache entries")
                return deleted
            return 0
        except Exception as e:
            print(f"⚠️  Cache invalidation error: {e}")
            return 0
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache performance statistics
        """
        if not self.redis_client:
            return {
                "enabled": False,
                "message": "Redis cache is disabled"
            }
        
        try:
            # Get all question keys
            question_keys = self.redis_client.keys("questions:*")
            metadata_keys = self.redis_client.keys("metadata:*")
            
            # Calculate total hits and misses
            total_hits = 0
            total_misses = 0
            total_questions = 0
            
            for meta_key in metadata_keys:
                metadata = self.redis_client.hgetall(meta_key)
                total_hits += int(metadata.get("hit_count", 0))
                total_misses += int(metadata.get("miss_count", 0))
            
            # Count total cached questions
            for q_key in question_keys:
                data = self.redis_client.get(q_key)
                if data:
                    questions = json.loads(data)
                    total_questions += len(questions)
            
            hit_rate = (total_hits / (total_hits + total_misses) * 100) if (total_hits + total_misses) > 0 else 0
            
            return {
                "enabled": True,
                "total_cached_sets": len(question_keys),
                "total_cached_questions": total_questions,
                "total_hits": total_hits,
                "total_misses": total_misses,
                "hit_rate_percentage": round(hit_rate, 2),
                "redis_info": {
                    "host": self.redis_host,
                    "port": self.redis_port,
                    "db": self.redis_db
                }
            }
        except Exception as e:
            return {
                "enabled": True,
                "error": str(e)
            }
    
    def _store_metadata(self, cache_key: str, question_count: int):
        """Store metadata about cached questions"""
        if not self.redis_client:
            return
        
        try:
            metadata_key = f"metadata:{cache_key}"
            self.redis_client.hset(metadata_key, mapping={
                "question_count": question_count,
                "created_at": datetime.utcnow().isoformat(),
                "hit_count": 0,
                "miss_count": 0
            })
            # Metadata expires with the questions
            self.redis_client.expire(metadata_key, self.cache_ttl)
        except Exception as e:
            print(f"⚠️  Metadata storage error: {e}")
    
    def _update_access_metadata(self, cache_key: str, hit: bool):
        """Update access statistics"""
        if not self.redis_client:
            return
        
        try:
            metadata_key = f"metadata:{cache_key}"
            field = "hit_count" if hit else "miss_count"
            self.redis_client.hincrby(metadata_key, field, 1)
            self.redis_client.hset(metadata_key, "last_accessed", datetime.utcnow().isoformat())
        except Exception as e:
            print(f"⚠️  Metadata update error: {e}")
    
    def warm_cache(
        self, 
        subject: str, 
        difficulty: str, 
        count: int, 
        questions: List[Dict[str, Any]],
        exam_type: Optional[str] = None
    ) -> bool:
        """
        Manually warm cache with pre-generated questions
        Used by admin or background workers
        """
        cache_key = self.generate_cache_key(subject, difficulty, count, exam_type)
        return self.set_cached_questions(cache_key, questions)
    
    def is_enabled(self) -> bool:
        """Check if cache is enabled and connected"""
        return self.redis_client is not None


# Global instance
_cache_service = None

def get_cache_service() -> QuestionCacheService:
    """Get or create cache service singleton"""
    global _cache_service
    if _cache_service is None:
        _cache_service = QuestionCacheService()
    return _cache_service
