# Subscription System & Payment Gateway Implementation Plan

## Document Information

- **Created**: December 8, 2025
- **Status**: Implementation Ready
- **Priority**: CRITICAL (PRD Section 7.1.F9 & 7.2.F5)
- **Timeline**: 2-3 Weeks

---

## 📋 Executive Summary

This document outlines the complete implementation plan for adding a subscription system with payment gateway integration to the Exam Platform, as required by the PRD.

### Current Status

- ✅ Database schema for subscriptions and payments (already implemented in `database.py`)
- ❌ Payment gateway integration (NOT implemented)
- ❌ Subscription management APIs (NOT implemented)
- ❌ Subscription UI/UX (NOT implemented)
- ❌ Auto-renewal logic (NOT implemented)
- ❌ Invoice generation (NOT implemented)

---

## 🎯 Implementation Goals

### Phase 1: Payment Gateway Integration (Week 1)

1. Choose and integrate payment gateway (Razorpay recommended for India)
2. Set up payment gateway credentials
3. Implement payment initiation API
4. Implement payment verification/webhook handling
5. Test payment flow in sandbox mode

### Phase 2: Subscription Management Backend (Week 2)

1. Create subscription plan configuration
2. Implement subscription creation API
3. Implement subscription status check API
4. Implement subscription cancellation API
5. Implement auto-renewal logic
6. Implement invoice generation
7. Add payment reminders system

### Phase 3: Frontend Integration (Week 3)

1. Create subscription plans page
2. Create payment checkout page
3. Create subscription management dashboard
4. Add subscription status indicators
5. Implement payment success/failure pages
6. Add invoice download functionality

---

## 🏗️ Technical Architecture

### Payment Gateway Options

#### Option 1: Razorpay (Recommended for India)

- **Pros**:
  - India-focused, supports UPI, cards, wallets
  - Easy integration, good documentation
  - Competitive pricing (2% + GST)
  - Automatic payment links
  - Subscription management built-in
- **Cons**:
  - Primarily India-focused
  - Requires KYC for activation

#### Option 2: Stripe (International)

- **Pros**:
  - Global coverage
  - Excellent developer experience
  - Advanced features (invoicing, billing portal)
  - Strong security
- **Cons**:
  - Higher fees for Indian cards
  - Complex setup for Indian businesses

#### Option 3: PayPal

- **Pros**:
  - Widely recognized
  - Global coverage
- **Cons**:
  - Higher fees
  - Complex integration
  - Not popular in India

**Decision**: Use **Razorpay** for primary implementation with architecture that allows switching to Stripe later.

---

## 📦 Subscription Plans (PRD Section 7.1.F9)

### Plan Structure

```python
SUBSCRIPTION_PLANS = {
    "monthly": {
        "name": "Monthly Plan",
        "duration_days": 30,
        "price": 499,  # INR
        "discount": 0,
        "features": [
            "Full access to all exams",
            "Unlimited practice tests",
            "Performance analytics",
            "Download reports (PDF)",
            "AI-powered question generation"
        ]
    },
    "quarterly": {
        "name": "Quarterly Plan",
        "duration_days": 90,
        "price": 1347,  # INR (10% discount)
        "discount": 10,
        "original_price": 1497,
        "features": [
            "All Monthly Plan features",
            "10% discount",
            "Priority support",
            "Advanced analytics"
        ]
    },
    "annual": {
        "name": "Annual Plan",
        "duration_days": 365,
        "price": 4788,  # INR (20% discount)
        "discount": 20,
        "original_price": 5988,
        "features": [
            "All Quarterly Plan features",
            "20% discount",
            "Dedicated support",
            "Early access to new features",
            "Interview preparation module"
        ]
    }
}
```

---

## 🔧 Backend Implementation

### 1. Environment Variables

Add to `.env`:

```env
# Payment Gateway Configuration
RAZORPAY_KEY_ID=your_key_id_here
RAZORPAY_KEY_SECRET=your_key_secret_here
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret_here

# Subscription Configuration
MONTHLY_PLAN_PRICE=499
QUARTERLY_PLAN_PRICE=1347
ANNUAL_PLAN_PRICE=4788

# Frontend URL for redirects
FRONTEND_URL=http://localhost:3000
```

### 2. Install Dependencies

Add to `requirements.txt`:

```
razorpay==1.4.1
python-dateutil==2.8.2
```

### 3. Create Payment Service (`payment_service.py`)

```python
"""
Payment Gateway Service
Handles Razorpay integration for subscription payments
"""

import razorpay
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class PaymentService:
    def __init__(self):
        self.client = razorpay.Client(
            auth=(
                os.getenv("RAZORPAY_KEY_ID"),
                os.getenv("RAZORPAY_KEY_SECRET")
            )
        )

    def create_order(self, amount, currency="INR", receipt=None):
        """Create a Razorpay order"""
        pass

    def verify_payment(self, payment_id, order_id, signature):
        """Verify payment signature"""
        pass

    def create_subscription(self, plan_id, customer_id):
        """Create a subscription"""
        pass

    def cancel_subscription(self, subscription_id):
        """Cancel a subscription"""
        pass
```

### 4. Create Subscription Service (`subscription_service.py`)

```python
"""
Subscription Management Service
Handles subscription lifecycle and business logic
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import Subscription, Payment, User

class SubscriptionService:

    PLANS = {
        "monthly": {"days": 30, "price": 499},
        "quarterly": {"days": 90, "price": 1347},
        "annual": {"days": 365, "price": 4788}
    }

    def create_subscription(self, db: Session, user_id: int, plan_type: str):
        """Create a new subscription"""
        pass

    def check_subscription_status(self, db: Session, user_id: int):
        """Check if user has active subscription"""
        pass

    def cancel_subscription(self, db: Session, subscription_id: int):
        """Cancel a subscription"""
        pass

    def renew_subscription(self, db: Session, subscription_id: int):
        """Renew a subscription (for auto-renewal)"""
        pass

    def get_user_subscriptions(self, db: Session, user_id: int):
        """Get all subscriptions for a user"""
        pass
```

### 5. API Endpoints (Add to `main.py`)

```python
# Subscription Plans
@app.get("/api/subscription/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    pass

# Create Payment Order
@app.post("/api/payment/create-order")
async def create_payment_order(plan_type: str, user_id: int):
    """Create a Razorpay order for subscription payment"""
    pass

# Verify Payment
@app.post("/api/payment/verify")
async def verify_payment(payment_data: dict):
    """Verify payment and activate subscription"""
    pass

# Get User Subscription Status
@app.get("/api/subscription/status/{user_id}")
async def get_subscription_status(user_id: int):
    """Get current subscription status for user"""
    pass

# Cancel Subscription
@app.post("/api/subscription/cancel/{subscription_id}")
async def cancel_subscription(subscription_id: int):
    """Cancel a subscription"""
    pass

# Razorpay Webhook
@app.post("/api/payment/webhook")
async def payment_webhook(request: Request):
    """Handle Razorpay webhooks for payment events"""
    pass

# Get Payment History
@app.get("/api/payment/history/{user_id}")
async def get_payment_history(user_id: int):
    """Get payment history for a user"""
    pass

# Download Invoice
@app.get("/api/payment/invoice/{payment_id}")
async def download_invoice(payment_id: int):
    """Generate and download invoice PDF"""
    pass
```

---

## 🎨 Frontend Implementation

### 1. Create Subscription Plans Page

**File**: `exam-app/src/app/subscription/page.tsx`

Features:

- Display all three plans (Monthly, Quarterly, Annual)
- Highlight recommended plan (Annual)
- Show discount badges
- Feature comparison table
- "Choose Plan" buttons
- Current subscription status indicator

### 2. Create Payment Checkout Page

**File**: `exam-app/src/app/checkout/page.tsx`

Features:

- Order summary
- Razorpay payment integration
- Payment method selection
- Terms and conditions checkbox
- Secure payment badge
- Loading states

### 3. Create Subscription Dashboard

**File**: `exam-app/src/app/dashboard/subscription/page.tsx`

Features:

- Current plan details
- Expiry date countdown
- Usage statistics
- Payment history table
- Invoice download buttons
- Upgrade/downgrade options
- Cancel subscription button

### 4. Add Subscription Status Indicator

**Component**: `exam-app/src/components/SubscriptionBadge.tsx`

Features:

- Show subscription status (Active/Expired/Trial)
- Display days remaining
- Quick upgrade button for expired users
- Premium badge for active subscribers

---

## 🔐 Security Considerations

### 1. Payment Security

- ✅ Use HTTPS for all payment-related requests
- ✅ Never store card details on server
- ✅ Verify payment signatures server-side
- ✅ Use webhook secrets for webhook verification
- ✅ Implement rate limiting on payment endpoints

### 2. Subscription Security

- ✅ Verify user authentication before showing payment page
- ✅ Check subscription status on every protected route
- ✅ Implement middleware to block expired users
- ✅ Log all subscription changes for audit trail
- ✅ Encrypt sensitive payment data in database

### 3. Webhook Security

- ✅ Verify webhook signatures
- ✅ Implement idempotency for webhook processing
- ✅ Use separate endpoint for webhooks
- ✅ Log all webhook events

---

## 📊 Database Migrations

### Migration 1: Add Subscription Plan Details

```sql
-- Add plan_details column to subscriptions table
ALTER TABLE subscriptions ADD COLUMN plan_details JSON;

-- Add discount_applied column
ALTER TABLE subscriptions ADD COLUMN discount_applied FLOAT DEFAULT 0;

-- Add original_amount column
ALTER TABLE subscriptions ADD COLUMN original_amount FLOAT;
```

### Migration 2: Add Payment Gateway Fields

```sql
-- Add gateway-specific fields to payments table
ALTER TABLE payments ADD COLUMN razorpay_order_id VARCHAR(255);
ALTER TABLE payments ADD COLUMN razorpay_payment_id VARCHAR(255);
ALTER TABLE payments ADD COLUMN razorpay_signature VARCHAR(500);
ALTER TABLE payments ADD COLUMN invoice_url VARCHAR(500);
```

---

## 🧪 Testing Strategy

### 1. Unit Tests

- Test subscription creation logic
- Test payment verification logic
- Test auto-renewal logic
- Test subscription expiry logic
- Test invoice generation

### 2. Integration Tests

- Test Razorpay sandbox integration
- Test webhook handling
- Test payment flow end-to-end
- Test subscription activation after payment
- Test subscription cancellation

### 3. Manual Testing Checklist

- [ ] Create subscription with each plan type
- [ ] Complete payment in Razorpay sandbox
- [ ] Verify subscription activation
- [ ] Test payment failure scenarios
- [ ] Test webhook delivery
- [ ] Test subscription expiry
- [ ] Test auto-renewal
- [ ] Test subscription cancellation
- [ ] Download invoice PDF
- [ ] Test payment history display

---

## 📈 Monitoring & Analytics

### Metrics to Track

1. **Conversion Metrics**

   - Subscription plan views
   - Checkout initiations
   - Payment success rate
   - Payment failure rate
   - Plan-wise conversion rates

2. **Revenue Metrics**

   - Monthly Recurring Revenue (MRR)
   - Annual Recurring Revenue (ARR)
   - Average Revenue Per User (ARPU)
   - Churn rate
   - Lifetime Value (LTV)

3. **Operational Metrics**
   - Active subscriptions count
   - Expired subscriptions count
   - Cancelled subscriptions count
   - Auto-renewal success rate
   - Payment gateway uptime

---

## 🚀 Deployment Checklist

### Pre-Production

- [ ] Set up Razorpay production account
- [ ] Complete KYC verification
- [ ] Configure production API keys
- [ ] Set up webhook URL
- [ ] Test in Razorpay sandbox
- [ ] Review pricing and plans
- [ ] Prepare terms and conditions
- [ ] Prepare refund policy

### Production

- [ ] Deploy backend with payment endpoints
- [ ] Deploy frontend with subscription pages
- [ ] Configure environment variables
- [ ] Set up SSL certificate
- [ ] Enable webhook endpoint
- [ ] Test production payment flow
- [ ] Set up monitoring alerts
- [ ] Prepare customer support documentation

---

## 📝 User Flow Diagrams

### Subscription Purchase Flow

```
User Dashboard
    ↓
View Subscription Plans
    ↓
Select Plan (Monthly/Quarterly/Annual)
    ↓
Review Order Summary
    ↓
Click "Proceed to Payment"
    ↓
Razorpay Checkout Opens
    ↓
User Completes Payment
    ↓
Payment Verification (Backend)
    ↓
Subscription Activated
    ↓
Redirect to Success Page
    ↓
Send Confirmation Email
```

### Auto-Renewal Flow

```
Cron Job (Daily at 2 AM)
    ↓
Check Subscriptions Expiring in 3 Days
    ↓
Filter Auto-Renew Enabled
    ↓
For Each Subscription:
    ↓
    Create Razorpay Order
    ↓
    Charge Saved Payment Method
    ↓
    If Success:
        ↓
        Extend Subscription
        ↓
        Send Renewal Confirmation
    ↓
    If Failure:
        ↓
        Send Payment Failure Email
        ↓
        Retry After 24 Hours
```

---

## 💰 Pricing Strategy

### Current Pricing (India Market)

- **Monthly**: ₹499/month
- **Quarterly**: ₹1,347/quarter (10% discount = ₹449/month)
- **Annual**: ₹4,788/year (20% discount = ₹399/month)

### Competitive Analysis

- Unacademy: ₹999-1,999/month
- BYJU'S: ₹1,500-3,000/month
- Vedantu: ₹800-1,500/month

**Our Positioning**: Affordable premium platform (₹399-499/month range)

---

## 🎁 Promotional Features

### Launch Offers

1. **Early Bird Discount**: 30% off for first 100 subscribers
2. **Referral Program**: Get 1 month free for every 3 referrals
3. **Student Discount**: 15% off with valid student ID
4. **Trial Period**: 7-day free trial for new users

### Implementation

- Add `promo_code` field to subscriptions table
- Create promo codes management in admin panel
- Implement promo code validation API
- Add promo code input in checkout page

---

## 📧 Email Notifications

### Required Email Templates

1. **Subscription Confirmation**

   - Subject: "Welcome to [Platform Name] Premium! 🎉"
   - Content: Plan details, features, invoice link

2. **Payment Success**

   - Subject: "Payment Successful - Invoice Attached"
   - Content: Payment details, invoice PDF

3. **Payment Failure**

   - Subject: "Payment Failed - Action Required"
   - Content: Retry link, support contact

4. **Subscription Expiring Soon**

   - Subject: "Your subscription expires in 3 days"
   - Content: Renewal link, plan benefits

5. **Subscription Expired**

   - Subject: "Your subscription has expired"
   - Content: Renewal link, limited access notice

6. **Subscription Cancelled**

   - Subject: "Subscription Cancelled Successfully"
   - Content: Cancellation confirmation, feedback request

7. **Auto-Renewal Success**
   - Subject: "Subscription Renewed Successfully"
   - Content: New expiry date, invoice

---

## 🔄 Migration from Free to Paid

### Handling Existing Users

1. **Grandfather Clause**: Existing users get 30-day grace period
2. **Limited Free Tier**: After grace period, limit to 5 exams/month
3. **Upgrade Prompts**: Show subscription benefits throughout app
4. **Trial Extension**: Offer 7-day trial to existing users

---

## 📊 Admin Dashboard Features

### Subscription Management Panel

1. **Overview Dashboard**

   - Total active subscriptions
   - Revenue this month
   - Churn rate
   - Conversion rate

2. **Subscription List**

   - Filter by plan type
   - Filter by status
   - Search by user email
   - Export to CSV

3. **Payment Transactions**

   - All payment history
   - Filter by status
   - Filter by date range
   - Refund management

4. **Analytics**
   - Revenue charts
   - Plan distribution pie chart
   - Subscription growth trend
   - Churn analysis

---

## 🛠️ Implementation Timeline

### Week 1: Payment Gateway Integration

- **Day 1-2**: Set up Razorpay account, create payment service
- **Day 3-4**: Implement payment APIs, webhook handling
- **Day 5**: Testing in sandbox mode

### Week 2: Subscription Management

- **Day 1-2**: Implement subscription service, APIs
- **Day 3-4**: Implement auto-renewal logic, invoice generation
- **Day 5**: Backend testing, API documentation

### Week 3: Frontend Integration

- **Day 1-2**: Create subscription plans page, checkout page
- **Day 3-4**: Create subscription dashboard, payment history
- **Day 5**: End-to-end testing, bug fixes

---

## ✅ Success Criteria

### Technical Success

- [ ] Payment success rate > 95%
- [ ] Webhook processing time < 2 seconds
- [ ] Zero payment data breaches
- [ ] API response time < 500ms
- [ ] 100% payment verification accuracy

### Business Success

- [ ] 10% conversion rate from free to paid
- [ ] 70% annual plan selection rate
- [ ] < 5% monthly churn rate
- [ ] 90% auto-renewal success rate
- [ ] 4.5+ star rating for payment experience

---

## 🐛 Common Issues & Solutions

### Issue 1: Payment Verification Fails

**Solution**: Check signature verification logic, ensure correct secret key

### Issue 2: Webhook Not Received

**Solution**: Verify webhook URL is publicly accessible, check firewall rules

### Issue 3: Subscription Not Activated After Payment

**Solution**: Check database transaction handling, ensure atomic operations

### Issue 4: Auto-Renewal Fails

**Solution**: Implement retry logic, send payment failure notifications

---

## 📚 Resources & Documentation

### Razorpay Documentation

- [Payment Gateway Integration](https://razorpay.com/docs/payments/)
- [Subscriptions API](https://razorpay.com/docs/subscriptions/)
- [Webhooks](https://razorpay.com/docs/webhooks/)
- [Testing Guide](https://razorpay.com/docs/payments/payments/test-card-details/)

### Internal Documentation

- Database Schema: `database.py`
- API Documentation: Generate with Swagger
- Frontend Components: Storybook (to be set up)

---

## 🎯 Next Steps

1. **Review this plan** with stakeholders
2. **Set up Razorpay account** and complete KYC
3. **Create feature branch**: `feature/subscription-system`
4. **Start with Week 1 tasks**: Payment gateway integration
5. **Daily standups** to track progress
6. **Weekly demos** to stakeholders

---

**Document Version**: 1.0  
**Last Updated**: December 8, 2025  
**Status**: Ready for Implementation  
**Estimated Effort**: 120-150 hours (2-3 weeks with 1 developer)
