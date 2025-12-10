"""
Payment Gateway Service
Handles Razorpay integration for subscription payments
"""

import razorpay
import os
import hmac
import hashlib
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()


class PaymentService:
    """Service class for handling Razorpay payment operations"""
    
    def __init__(self):
        """Initialize Razorpay client with credentials from environment"""
        self.key_id = os.getenv("RAZORPAY_KEY_ID")
        self.key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        self.webhook_secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")
        
        if not self.key_id or not self.key_secret:
            raise ValueError("Razorpay credentials not found in environment variables")
        
        self.client = razorpay.Client(auth=(self.key_id, self.key_secret))
    
    def create_order(self, amount: float, currency: str = "INR", receipt: Optional[str] = None, 
                     notes: Optional[Dict] = None) -> Dict:
        """
        Create a Razorpay order for payment
        
        Args:
            amount: Amount in rupees (will be converted to paise)
            currency: Currency code (default: INR)
            receipt: Optional receipt ID for reference
            notes: Optional dictionary of notes
            
        Returns:
            Dictionary containing order details including order_id
        """
        try:
            # Convert amount to paise (Razorpay expects amount in smallest currency unit)
            amount_paise = int(amount * 100)
            
            order_data = {
                "amount": amount_paise,
                "currency": currency,
                "payment_capture": 1  # Auto capture payment
            }
            
            if receipt:
                order_data["receipt"] = receipt
            
            if notes:
                order_data["notes"] = notes
            
            order = self.client.order.create(data=order_data)
            return {
                "success": True,
                "order_id": order["id"],
                "amount": amount,
                "currency": currency,
                "order_data": order
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def verify_payment_signature(self, razorpay_order_id: str, razorpay_payment_id: str, 
                                 razorpay_signature: str) -> bool:
        """
        Verify payment signature to ensure payment authenticity
        
        Args:
            razorpay_order_id: Order ID from Razorpay
            razorpay_payment_id: Payment ID from Razorpay
            razorpay_signature: Signature from Razorpay
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Create signature verification string
            message = f"{razorpay_order_id}|{razorpay_payment_id}"
            
            # Generate expected signature
            generated_signature = hmac.new(
                self.key_secret.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures
            return hmac.compare_digest(generated_signature, razorpay_signature)
        except Exception as e:
            print(f"Signature verification error: {e}")
            return False
    
    def verify_webhook_signature(self, webhook_body: str, webhook_signature: str) -> bool:
        """
        Verify webhook signature to ensure webhook authenticity
        
        Args:
            webhook_body: Raw webhook body as string
            webhook_signature: Signature from webhook header
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            if not self.webhook_secret:
                print("Warning: Webhook secret not configured")
                return False
            
            # Generate expected signature
            generated_signature = hmac.new(
                self.webhook_secret.encode(),
                webhook_body.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures
            return hmac.compare_digest(generated_signature, webhook_signature)
        except Exception as e:
            print(f"Webhook signature verification error: {e}")
            return False
    
    def fetch_payment(self, payment_id: str) -> Dict:
        """
        Fetch payment details from Razorpay
        
        Args:
            payment_id: Razorpay payment ID
            
        Returns:
            Dictionary containing payment details
        """
        try:
            payment = self.client.payment.fetch(payment_id)
            return {
                "success": True,
                "payment": payment
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def fetch_order(self, order_id: str) -> Dict:
        """
        Fetch order details from Razorpay
        
        Args:
            order_id: Razorpay order ID
            
        Returns:
            Dictionary containing order details
        """
        try:
            order = self.client.order.fetch(order_id)
            return {
                "success": True,
                "order": order
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def refund_payment(self, payment_id: str, amount: Optional[float] = None, 
                       notes: Optional[Dict] = None) -> Dict:
        """
        Initiate a refund for a payment
        
        Args:
            payment_id: Razorpay payment ID
            amount: Optional partial refund amount (full refund if not specified)
            notes: Optional notes for the refund
            
        Returns:
            Dictionary containing refund details
        """
        try:
            refund_data = {}
            
            if amount:
                # Convert to paise for partial refund
                refund_data["amount"] = int(amount * 100)
            
            if notes:
                refund_data["notes"] = notes
            
            refund = self.client.payment.refund(payment_id, refund_data)
            return {
                "success": True,
                "refund": refund
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_razorpay_key_id(self) -> str:
        """
        Get Razorpay key ID for frontend integration
        
        Returns:
            Razorpay key ID
        """
        return self.key_id


# Create singleton instance
payment_service = PaymentService()
