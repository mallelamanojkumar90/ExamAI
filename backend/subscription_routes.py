"""
Subscription API Routes
Handles all subscription and payment related endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from database import get_db, User, Subscription, Payment
from payment_service import payment_service
from subscription_service import subscription_service
from invoice_service import invoice_service
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api", tags=["subscription"])


# Pydantic models for request validation
class CreateOrderRequest(BaseModel):
    user_id: int
    plan_type: str


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    user_id: int
    plan_type: str


class ToggleAutoRenewRequest(BaseModel):
    subscription_id: int
    user_id: int
    auto_renew: bool


class CancelSubscriptionRequest(BaseModel):
    subscription_id: int
    user_id: int


# ============================================================================
# Subscription Plans Endpoints
# ============================================================================

@router.get("/subscription/plans")
async def get_subscription_plans():
    """
    Get all available subscription plans
    
    Returns:
        List of subscription plans with pricing and features
    """
    try:
        plans = subscription_service.get_all_plans()
        return {
            "success": True,
            "plans": plans
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/subscription/plan/{plan_type}")
async def get_subscription_plan(plan_type: str):
    """
    Get details of a specific subscription plan
    
    Args:
        plan_type: Plan type (monthly/quarterly/annual)
        
    Returns:
        Plan details
    """
    try:
        plan = subscription_service.get_plan(plan_type)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        return {
            "success": True,
            "plan": plan
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Payment Endpoints
# ============================================================================

@router.post("/payment/create-order")
async def create_payment_order(request: CreateOrderRequest, db: Session = Depends(get_db)):
    """
    Create a Razorpay order for subscription payment
    
    Args:
        request: Order creation request with user_id and plan_type
        
    Returns:
        Razorpay order details including order_id
    """
    try:
        # Validate user exists
        user = db.query(User).filter(User.user_id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get plan details
        plan = subscription_service.get_plan(request.plan_type)
        if not plan:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        # Create Razorpay order
        receipt = f"sub_{request.user_id}_{request.plan_type}_{int(datetime.now().timestamp())}"
        notes = {
            "user_id": request.user_id,
            "plan_type": request.plan_type,
            "user_email": user.email
        }
        
        order_result = payment_service.create_order(
            amount=plan["price"],
            receipt=receipt,
            notes=notes
        )
        
        if not order_result["success"]:
            raise HTTPException(status_code=500, detail=order_result.get("error", "Failed to create order"))
        
        return {
            "success": True,
            "order_id": order_result["order_id"],
            "amount": order_result["amount"],
            "currency": order_result["currency"],
            "key_id": payment_service.get_razorpay_key_id(),
            "plan": plan
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/payment/verify")
async def verify_payment(request: VerifyPaymentRequest, db: Session = Depends(get_db)):
    """
    Verify payment and activate subscription
    
    Args:
        request: Payment verification request with Razorpay details
        
    Returns:
        Subscription activation status
    """
    try:
        # Verify payment signature
        is_valid = payment_service.verify_payment_signature(
            request.razorpay_order_id,
            request.razorpay_payment_id,
            request.razorpay_signature
        )
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid payment signature")
        
        # Fetch payment details from Razorpay
        payment_details = payment_service.fetch_payment(request.razorpay_payment_id)
        if not payment_details["success"]:
            raise HTTPException(status_code=500, detail="Failed to fetch payment details")
        
        payment_data = payment_details["payment"]
        
        # Get plan details
        plan = subscription_service.get_plan(request.plan_type)
        if not plan:
            raise HTTPException(status_code=400, detail="Invalid plan type")
        
        # Create payment record
        payment = Payment(
            user_id=request.user_id,
            amount=plan["price"],
            payment_method=payment_data.get("method", "card"),
            transaction_id=request.razorpay_payment_id,
            status="success",
            payment_date=datetime.utcnow(),
            razorpay_order_id=request.razorpay_order_id,
            razorpay_payment_id=request.razorpay_payment_id,
            razorpay_signature=request.razorpay_signature
        )
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        # Create subscription
        subscription_result = subscription_service.create_subscription(
            db=db,
            user_id=request.user_id,
            plan_type=request.plan_type,
            payment_id=payment.payment_id
        )
        
        if not subscription_result["success"]:
            raise HTTPException(status_code=500, detail=subscription_result.get("error"))
        
        # Link payment to subscription
        payment.subscription_id = subscription_result["subscription"]["subscription_id"]
        db.commit()
        
        # Generate invoice
        user = db.query(User).filter(User.user_id == request.user_id).first()
        invoice_result = invoice_service.generate_invoice(
            payment_data={
                "payment_id": payment.payment_id,
                "transaction_id": payment.transaction_id,
                "amount": payment.amount,
                "status": payment.status
            },
            user_data={
                "full_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number
            },
            subscription_data={
                "plan_type": request.plan_type,
                "duration": f"{plan['duration_days']} days",
                "discount_applied": plan["discount"],
                "original_amount": plan["original_price"]
            }
        )
        
        if invoice_result["success"]:
            payment.invoice_url = invoice_result["invoice_path"]
            db.commit()
        
        return {
            "success": True,
            "message": "Payment verified and subscription activated",
            "subscription": subscription_result["subscription"],
            "payment_id": payment.payment_id,
            "invoice_available": invoice_result["success"]
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/payment/webhook")
async def payment_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Razorpay webhook events
    
    Args:
        request: Webhook request from Razorpay
        
    Returns:
        Acknowledgment response
    """
    try:
        # Get webhook body and signature
        body = await request.body()
        signature = request.headers.get("X-Razorpay-Signature", "")
        
        # Verify webhook signature
        is_valid = payment_service.verify_webhook_signature(body.decode(), signature)
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid webhook signature")
        
        # Parse webhook data
        webhook_data = json.loads(body)
        event = webhook_data.get("event")
        payload = webhook_data.get("payload", {}).get("payment", {}).get("entity", {})
        
        # Handle different webhook events
        if event == "payment.captured":
            # Payment successful - already handled in verify endpoint
            pass
        elif event == "payment.failed":
            # Payment failed - update payment record if exists
            payment_id = payload.get("id")
            if payment_id:
                payment = db.query(Payment).filter(
                    Payment.razorpay_payment_id == payment_id
                ).first()
                if payment:
                    payment.status = "failed"
                    db.commit()
        
        return {"success": True, "message": "Webhook processed"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Subscription Management Endpoints
# ============================================================================

@router.get("/subscription/status/{user_id}")
async def get_subscription_status(user_id: int, db: Session = Depends(get_db)):
    """
    Get current subscription status for a user
    
    Args:
        user_id: User ID
        
    Returns:
        Subscription status and details
    """
    try:
        result = subscription_service.check_subscription_status(db, user_id)
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/subscription/history/{user_id}")
async def get_subscription_history(user_id: int, db: Session = Depends(get_db)):
    """
    Get all subscriptions for a user
    
    Args:
        user_id: User ID
        
    Returns:
        List of user's subscriptions
    """
    try:
        result = subscription_service.get_user_subscriptions(db, user_id)
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subscription/cancel")
async def cancel_subscription(request: CancelSubscriptionRequest, db: Session = Depends(get_db)):
    """
    Cancel a subscription
    
    Args:
        request: Cancellation request with subscription_id and user_id
        
    Returns:
        Cancellation status
    """
    try:
        result = subscription_service.cancel_subscription(
            db,
            request.subscription_id,
            request.user_id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subscription/auto-renew")
async def toggle_auto_renew(request: ToggleAutoRenewRequest, db: Session = Depends(get_db)):
    """
    Enable or disable auto-renewal for a subscription
    
    Args:
        request: Auto-renewal toggle request
        
    Returns:
        Update status
    """
    try:
        result = subscription_service.toggle_auto_renew(
            db,
            request.subscription_id,
            request.user_id,
            request.auto_renew
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Payment History Endpoints
# ============================================================================

@router.get("/payment/history/{user_id}")
async def get_payment_history(user_id: int, db: Session = Depends(get_db)):
    """
    Get payment history for a user
    
    Args:
        user_id: User ID
        
    Returns:
        List of user's payments
    """
    try:
        payments = db.query(Payment).filter(
            Payment.user_id == user_id
        ).order_by(Payment.payment_date.desc()).all()
        
        payment_list = []
        for payment in payments:
            payment_list.append({
                "payment_id": payment.payment_id,
                "amount": payment.amount,
                "payment_method": payment.payment_method,
                "transaction_id": payment.transaction_id,
                "status": payment.status,
                "payment_date": payment.payment_date.isoformat(),
                "invoice_available": payment.invoice_url is not None
            })
        
        return {
            "success": True,
            "payments": payment_list,
            "count": len(payment_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/payment/invoice/{payment_id}")
async def download_invoice(payment_id: int, db: Session = Depends(get_db)):
    """
    Download invoice PDF for a payment
    
    Args:
        payment_id: Payment ID
        
    Returns:
        PDF file
    """
    try:
        payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        if not payment.invoice_url:
            raise HTTPException(status_code=404, detail="Invoice not available")
        
        if not os.path.exists(payment.invoice_url):
            raise HTTPException(status_code=404, detail="Invoice file not found")
        
        return FileResponse(
            payment.invoice_url,
            media_type="application/pdf",
            filename=f"invoice_{payment_id}.pdf"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Import os for file operations
import os
