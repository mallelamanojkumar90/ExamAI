"""
Subscription Management Service
Handles subscription lifecycle and business logic
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from database import Subscription, Payment, User
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class SubscriptionService:
    """Service class for managing subscriptions"""
    
    # Subscription plan configuration
    PLANS = {
        "monthly": {
            "id": "monthly",
            "name": "Monthly Plan",
            "duration_days": 30,
            "price": float(os.getenv("MONTHLY_PLAN_PRICE", "499")),
            "discount": 0,
            "original_price": float(os.getenv("MONTHLY_PLAN_PRICE", "499")),
            "features": [
                "Full access to all exams",
                "Unlimited practice tests",
                "Performance analytics",
                "Download reports (PDF)",
                "AI-powered question generation",
                "24/7 support"
            ]
        },
        "quarterly": {
            "id": "quarterly",
            "name": "Quarterly Plan",
            "duration_days": 90,
            "price": float(os.getenv("QUARTERLY_PLAN_PRICE", "1347")),
            "discount": 10,
            "original_price": 1497,
            "features": [
                "All Monthly Plan features",
                "10% discount (₹449/month)",
                "Priority support",
                "Advanced analytics",
                "Study material downloads"
            ]
        },
        "annual": {
            "id": "annual",
            "name": "Annual Plan",
            "duration_days": 365,
            "price": float(os.getenv("ANNUAL_PLAN_PRICE", "4788")),
            "discount": 20,
            "original_price": 5988,
            "features": [
                "All Quarterly Plan features",
                "20% discount (₹399/month)",
                "Dedicated support",
                "Early access to new features",
                "Interview preparation module",
                "Personalized learning path"
            ],
            "recommended": True
        }
    }
    
    @staticmethod
    def get_all_plans() -> List[Dict]:
        """
        Get all available subscription plans
        
        Returns:
            List of subscription plan dictionaries
        """
        return list(SubscriptionService.PLANS.values())
    
    @staticmethod
    def get_plan(plan_type: str) -> Optional[Dict]:
        """
        Get a specific subscription plan
        
        Args:
            plan_type: Plan type (monthly/quarterly/annual)
            
        Returns:
            Plan dictionary or None if not found
        """
        return SubscriptionService.PLANS.get(plan_type)
    
    @staticmethod
    def create_subscription(db: Session, user_id: int, plan_type: str, 
                           payment_id: int) -> Dict:
        """
        Create a new subscription for a user
        
        Args:
            db: Database session
            user_id: User ID
            plan_type: Plan type (monthly/quarterly/annual)
            payment_id: Payment ID
            
        Returns:
            Dictionary with subscription details
        """
        try:
            # Get plan details
            plan = SubscriptionService.get_plan(plan_type)
            if not plan:
                return {"success": False, "error": "Invalid plan type"}
            
            # Calculate dates
            start_date = datetime.utcnow()
            end_date = start_date + timedelta(days=plan["duration_days"])
            
            # Create subscription
            subscription = Subscription(
                user_id=user_id,
                plan_type=plan_type,
                start_date=start_date,
                end_date=end_date,
                amount=plan["price"],
                payment_status="active",
                auto_renew=False,  # Default to false, user can enable later
                plan_details=plan,
                discount_applied=plan["discount"],
                original_amount=plan["original_price"]
            )
            
            db.add(subscription)
            db.commit()
            db.refresh(subscription)
            
            return {
                "success": True,
                "subscription": {
                    "subscription_id": subscription.subscription_id,
                    "plan_type": subscription.plan_type,
                    "start_date": subscription.start_date.isoformat(),
                    "end_date": subscription.end_date.isoformat(),
                    "amount": subscription.amount,
                    "status": subscription.payment_status
                }
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def check_subscription_status(db: Session, user_id: int) -> Dict:
        """
        Check if user has an active subscription
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dictionary with subscription status
        """
        try:
            # Get active subscription
            subscription = db.query(Subscription).filter(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.payment_status == "active",
                    Subscription.end_date > datetime.utcnow()
                )
            ).order_by(Subscription.end_date.desc()).first()
            
            if subscription:
                days_remaining = (subscription.end_date - datetime.utcnow()).days
                return {
                    "success": True,
                    "has_active_subscription": True,
                    "subscription": {
                        "subscription_id": subscription.subscription_id,
                        "plan_type": subscription.plan_type,
                        "start_date": subscription.start_date.isoformat(),
                        "end_date": subscription.end_date.isoformat(),
                        "days_remaining": days_remaining,
                        "amount": subscription.amount,
                        "auto_renew": subscription.auto_renew
                    }
                }
            else:
                return {
                    "success": True,
                    "has_active_subscription": False,
                    "subscription": None
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_user_subscriptions(db: Session, user_id: int) -> Dict:
        """
        Get all subscriptions for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dictionary with list of subscriptions
        """
        try:
            subscriptions = db.query(Subscription).filter(
                Subscription.user_id == user_id
            ).order_by(Subscription.created_at.desc()).all()
            
            subscription_list = []
            for sub in subscriptions:
                subscription_list.append({
                    "subscription_id": sub.subscription_id,
                    "plan_type": sub.plan_type,
                    "start_date": sub.start_date.isoformat(),
                    "end_date": sub.end_date.isoformat(),
                    "amount": sub.amount,
                    "status": sub.payment_status,
                    "auto_renew": sub.auto_renew,
                    "created_at": sub.created_at.isoformat()
                })
            
            return {
                "success": True,
                "subscriptions": subscription_list,
                "count": len(subscription_list)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def cancel_subscription(db: Session, subscription_id: int, user_id: int) -> Dict:
        """
        Cancel a subscription
        
        Args:
            db: Database session
            subscription_id: Subscription ID
            user_id: User ID (for verification)
            
        Returns:
            Dictionary with cancellation status
        """
        try:
            subscription = db.query(Subscription).filter(
                and_(
                    Subscription.subscription_id == subscription_id,
                    Subscription.user_id == user_id
                )
            ).first()
            
            if not subscription:
                return {"success": False, "error": "Subscription not found"}
            
            # Update subscription status
            subscription.payment_status = "cancelled"
            subscription.auto_renew = False
            
            db.commit()
            
            return {
                "success": True,
                "message": "Subscription cancelled successfully",
                "subscription_id": subscription_id
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def toggle_auto_renew(db: Session, subscription_id: int, user_id: int, 
                         auto_renew: bool) -> Dict:
        """
        Enable or disable auto-renewal for a subscription
        
        Args:
            db: Database session
            subscription_id: Subscription ID
            user_id: User ID (for verification)
            auto_renew: True to enable, False to disable
            
        Returns:
            Dictionary with update status
        """
        try:
            subscription = db.query(Subscription).filter(
                and_(
                    Subscription.subscription_id == subscription_id,
                    Subscription.user_id == user_id
                )
            ).first()
            
            if not subscription:
                return {"success": False, "error": "Subscription not found"}
            
            subscription.auto_renew = auto_renew
            db.commit()
            
            return {
                "success": True,
                "message": f"Auto-renewal {'enabled' if auto_renew else 'disabled'}",
                "auto_renew": auto_renew
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_expiring_subscriptions(db: Session, days: int = 3) -> List[Subscription]:
        """
        Get subscriptions expiring in the next N days (for auto-renewal)
        
        Args:
            db: Database session
            days: Number of days to look ahead
            
        Returns:
            List of expiring subscriptions
        """
        try:
            expiry_date = datetime.utcnow() + timedelta(days=days)
            
            subscriptions = db.query(Subscription).filter(
                and_(
                    Subscription.payment_status == "active",
                    Subscription.auto_renew == True,
                    Subscription.end_date <= expiry_date,
                    Subscription.end_date > datetime.utcnow()
                )
            ).all()
            
            return subscriptions
        except Exception as e:
            print(f"Error fetching expiring subscriptions: {e}")
            return []
    
    @staticmethod
    def renew_subscription(db: Session, subscription_id: int) -> Dict:
        """
        Renew a subscription (extends end date)
        
        Args:
            db: Database session
            subscription_id: Subscription ID
            
        Returns:
            Dictionary with renewal status
        """
        try:
            subscription = db.query(Subscription).filter(
                Subscription.subscription_id == subscription_id
            ).first()
            
            if not subscription:
                return {"success": False, "error": "Subscription not found"}
            
            # Get plan details
            plan = SubscriptionService.get_plan(subscription.plan_type)
            if not plan:
                return {"success": False, "error": "Invalid plan type"}
            
            # Extend subscription
            new_end_date = subscription.end_date + timedelta(days=plan["duration_days"])
            subscription.end_date = new_end_date
            subscription.payment_status = "active"
            
            db.commit()
            
            return {
                "success": True,
                "message": "Subscription renewed successfully",
                "new_end_date": new_end_date.isoformat()
            }
        except Exception as e:
            db.rollback()
            return {"success": False, "error": str(e)}


# Create singleton instance
subscription_service = SubscriptionService()
