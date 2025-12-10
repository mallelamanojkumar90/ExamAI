"""
Performance Analytics API Routes
Provides endpoints for student performance tracking and analytics
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, User
from performance_service import PerformanceService
from typing import Optional

router = APIRouter(prefix="/api/performance", tags=["performance"])


# ============================================================================
# Performance Summary Endpoints
# ============================================================================

@router.get("/summary/{user_id}")
async def get_performance_summary(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive performance summary for a user
    
    Args:
        user_id: User ID
        
    Returns:
        Performance summary with metrics
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        summary = PerformanceService.get_user_performance_summary(user_id, db)
        
        return {
            "success": True,
            "user_id": user_id,
            "username": user.email,
            "summary": summary
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching performance summary: {str(e)}")


@router.get("/timeline/{user_id}")
async def get_performance_timeline(
    user_id: int,
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """
    Get performance data over time for charts
    
    Args:
        user_id: User ID
        days: Number of days to look back (1-365)
        
    Returns:
        Daily performance data
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        timeline_data = PerformanceService.get_performance_over_time(user_id, days, db)
        
        return {
            "success": True,
            "user_id": user_id,
            "days": days,
            "data": timeline_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching performance timeline: {str(e)}")


# ============================================================================
# Peer Comparison Endpoints
# ============================================================================

@router.get("/peer-comparison/{user_id}")
async def get_peer_comparison(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Compare user's performance with peers
    
    Args:
        user_id: User ID
        
    Returns:
        Peer comparison data including rank and percentile
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        comparison = PerformanceService.get_peer_comparison(user_id, db)
        
        return {
            "success": True,
            "user_id": user_id,
            "comparison": comparison
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching peer comparison: {str(e)}")


# ============================================================================
# Strengths & Weaknesses Endpoints
# ============================================================================

@router.get("/analysis/{user_id}")
async def get_strengths_weaknesses(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get strengths and weaknesses analysis
    
    Args:
        user_id: User ID
        
    Returns:
        Strengths, weaknesses, and recommendations
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        analysis = PerformanceService.get_strengths_and_weaknesses(user_id, db)
        
        return {
            "success": True,
            "user_id": user_id,
            "analysis": analysis
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analysis: {str(e)}")


# ============================================================================
# Recent Activity Endpoints
# ============================================================================

@router.get("/recent-activity/{user_id}")
async def get_recent_activity(
    user_id: int,
    limit: int = Query(default=10, ge=1, le=50, description="Number of recent activities"),
    db: Session = Depends(get_db)
):
    """
    Get recent exam activity
    
    Args:
        user_id: User ID
        limit: Number of recent activities (1-50)
        
    Returns:
        List of recent exam attempts
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        activities = PerformanceService.get_recent_activity(user_id, limit, db)
        
        return {
            "success": True,
            "user_id": user_id,
            "activities": activities
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent activity: {str(e)}")


# ============================================================================
# Subject Performance Endpoints
# ============================================================================

@router.get("/subjects/{user_id}")
async def get_subject_performance(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed subject-wise performance
    
    Args:
        user_id: User ID
        
    Returns:
        Subject-wise performance data
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        summary = PerformanceService.get_user_performance_summary(user_id, db)
        
        return {
            "success": True,
            "user_id": user_id,
            "subjects": summary.get("subjects_performance", {})
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subject performance: {str(e)}")


# ============================================================================
# Difficulty Performance Endpoints
# ============================================================================

@router.get("/difficulty/{user_id}")
async def get_difficulty_performance(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get performance by difficulty level
    
    Args:
        user_id: User ID
        
    Returns:
        Difficulty-wise performance data
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        summary = PerformanceService.get_user_performance_summary(user_id, db)
        
        return {
            "success": True,
            "user_id": user_id,
            "difficulty": summary.get("difficulty_performance", {})
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching difficulty performance: {str(e)}")


# ============================================================================
# Dashboard Stats Endpoint
# ============================================================================

@router.get("/dashboard/{user_id}")
async def get_dashboard_stats(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all stats needed for performance dashboard
    
    Args:
        user_id: User ID
        
    Returns:
        Complete dashboard data
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Fetch all data
        summary = PerformanceService.get_user_performance_summary(user_id, db)
        timeline = PerformanceService.get_performance_over_time(user_id, 30, db)
        peer_comparison = PerformanceService.get_peer_comparison(user_id, db)
        analysis = PerformanceService.get_strengths_and_weaknesses(user_id, db)
        recent_activity = PerformanceService.get_recent_activity(user_id, 5, db)
        
        return {
            "success": True,
            "user_id": user_id,
            "username": user.email,
            "full_name": user.full_name,
            "dashboard": {
                "summary": summary,
                "timeline": timeline,
                "peer_comparison": peer_comparison,
                "analysis": analysis,
                "recent_activity": recent_activity
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard stats: {str(e)}")
