# Subscription System - Implementation Roadmap

## 📅 3-Week Sprint Plan

```
Week 1: Payment Gateway Foundation
├── Day 1-2: Razorpay Setup & Payment Service
├── Day 3-4: Payment APIs & Webhook Handling
└── Day 5: Testing & Documentation

Week 2: Subscription Management
├── Day 1-2: Subscription Service & Business Logic
├── Day 3-4: Auto-Renewal & Invoice Generation
└── Day 5: Admin Dashboard Integration

Week 3: Frontend & Polish
├── Day 1-2: Subscription Plans & Checkout UI
├── Day 3-4: User Dashboard & Payment History
└── Day 5: End-to-End Testing & Bug Fixes
```

---

## 🎯 Implementation Phases

### Phase 1: Backend Foundation (Week 1)

#### Files to Create:

1. **`backend/payment_service.py`** (200 lines)

   - Razorpay client initialization
   - Order creation
   - Payment verification
   - Webhook signature validation

2. **`backend/subscription_service.py`** (300 lines)

   - Subscription CRUD operations
   - Plan configuration
   - Status checking
   - Auto-renewal logic

3. **`backend/invoice_service.py`** (150 lines)

   - PDF invoice generation
   - Invoice template
   - Email attachment

4. **`backend/routes/subscription_routes.py`** (250 lines)
   - GET /api/subscription/plans
   - POST /api/payment/create-order
   - POST /api/payment/verify
   - GET /api/subscription/status/{user_id}
   - POST /api/subscription/cancel/{subscription_id}
   - POST /api/payment/webhook
   - GET /api/payment/history/{user_id}
   - GET /api/payment/invoice/{payment_id}

#### Database Changes:

```sql
-- Add missing columns to subscriptions table
ALTER TABLE subscriptions ADD COLUMN IF NOT EXISTS plan_details JSON;
ALTER TABLE subscriptions ADD COLUMN IF NOT EXISTS discount_applied FLOAT DEFAULT 0;
ALTER TABLE subscriptions ADD COLUMN IF NOT EXISTS original_amount FLOAT;

-- Add missing columns to payments table
ALTER TABLE payments ADD COLUMN IF NOT EXISTS razorpay_order_id VARCHAR(255);
ALTER TABLE payments ADD COLUMN IF NOT EXISTS razorpay_payment_id VARCHAR(255);
ALTER TABLE payments ADD COLUMN IF NOT EXISTS razorpay_signature VARCHAR(500);
ALTER TABLE payments ADD COLUMN IF NOT EXISTS invoice_url VARCHAR(500);
```

---

### Phase 2: Frontend Integration (Week 2-3)

#### Pages to Create:

1. **Subscription Plans Page** (`exam-app/src/app/subscription/page.tsx`)

   - 3 pricing cards (Monthly, Quarterly, Annual)
   - Feature comparison
   - Discount badges
   - "Choose Plan" buttons
   - Current subscription indicator

2. **Checkout Page** (`exam-app/src/app/checkout/page.tsx`)

   - Order summary
   - Razorpay integration
   - Payment button
   - Loading states
   - Success/failure handling

3. **Subscription Dashboard** (`exam-app/src/app/dashboard/subscription/page.tsx`)

   - Current plan overview
   - Expiry countdown
   - Payment history table
   - Invoice download
   - Cancel/upgrade buttons

4. **Payment Success Page** (`exam-app/src/app/payment/success/page.tsx`)

   - Success animation
   - Subscription details
   - Next steps
   - Download invoice

5. **Payment Failure Page** (`exam-app/src/app/payment/failure/page.tsx`)
   - Error message
   - Retry button
   - Support contact

#### Components to Create:

1. **`SubscriptionBadge.tsx`**

   - Shows subscription status
   - Premium indicator
   - Days remaining

2. **`PricingCard.tsx`**

   - Reusable pricing card
   - Feature list
   - CTA button

3. **`PaymentHistoryTable.tsx`**
   - Transaction list
   - Status indicators
   - Invoice download

---

## 📋 Detailed Task Breakdown

### Week 1 Tasks

#### Day 1: Razorpay Setup

- [ ] Create Razorpay test account
- [ ] Get API keys (Key ID, Secret)
- [ ] Set up webhook endpoint
- [ ] Update .env file
- [ ] Install razorpay package
- [ ] Create payment_service.py skeleton

#### Day 2: Payment Service Implementation

- [ ] Implement create_order()
- [ ] Implement verify_payment()
- [ ] Implement verify_webhook_signature()
- [ ] Add error handling
- [ ] Write unit tests
- [ ] Test with Razorpay sandbox

#### Day 3: Subscription Service

- [ ] Create subscription_service.py
- [ ] Define PLANS configuration
- [ ] Implement create_subscription()
- [ ] Implement check_subscription_status()
- [ ] Implement get_user_subscriptions()
- [ ] Add business logic validation

#### Day 4: API Routes

- [ ] Create routes/subscription_routes.py
- [ ] Implement all 8 endpoints
- [ ] Add authentication middleware
- [ ] Add request validation
- [ ] Add error handling
- [ ] Test all endpoints with Postman

#### Day 5: Testing & Documentation

- [ ] Write API tests
- [ ] Test payment flow end-to-end
- [ ] Test webhook handling
- [ ] Generate API documentation
- [ ] Code review
- [ ] Fix bugs

---

### Week 2 Tasks

#### Day 1: Invoice Generation

- [ ] Create invoice_service.py
- [ ] Design invoice template
- [ ] Implement PDF generation
- [ ] Add company logo/branding
- [ ] Test invoice generation
- [ ] Store invoices in database

#### Day 2: Auto-Renewal Logic

- [ ] Implement check_expiring_subscriptions()
- [ ] Implement auto_renew_subscription()
- [ ] Create cron job script
- [ ] Add email notifications
- [ ] Test renewal flow
- [ ] Handle renewal failures

#### Day 3: Admin Dashboard Backend

- [ ] Add admin subscription stats endpoint
- [ ] Add revenue analytics endpoint
- [ ] Add subscription list endpoint
- [ ] Add refund processing endpoint
- [ ] Test admin endpoints

#### Day 4: Email Notifications

- [ ] Set up email service (SendGrid/Mailgun)
- [ ] Create email templates
- [ ] Implement send_subscription_confirmation()
- [ ] Implement send_payment_receipt()
- [ ] Implement send_expiry_reminder()
- [ ] Test email delivery

#### Day 5: Backend Polish

- [ ] Add logging
- [ ] Add monitoring
- [ ] Performance optimization
- [ ] Security audit
- [ ] Code cleanup

---

### Week 3 Tasks

#### Day 1: Subscription Plans Page

- [ ] Create page.tsx
- [ ] Design pricing cards
- [ ] Add animations
- [ ] Implement plan selection
- [ ] Add responsive design
- [ ] Test on mobile

#### Day 2: Checkout Page

- [ ] Create checkout page
- [ ] Integrate Razorpay SDK
- [ ] Implement payment flow
- [ ] Add loading states
- [ ] Handle success/failure
- [ ] Test payment

#### Day 3: Subscription Dashboard

- [ ] Create dashboard page
- [ ] Show current subscription
- [ ] Display payment history
- [ ] Add invoice download
- [ ] Implement cancel flow
- [ ] Add upgrade options

#### Day 4: Components & Polish

- [ ] Create SubscriptionBadge
- [ ] Create PricingCard
- [ ] Create PaymentHistoryTable
- [ ] Add success/failure pages
- [ ] Polish UI/UX
- [ ] Add animations

#### Day 5: Testing & Launch

- [ ] End-to-end testing
- [ ] Cross-browser testing
- [ ] Mobile testing
- [ ] Fix bugs
- [ ] Performance optimization
- [ ] Prepare for launch

---

## 🔧 Technical Dependencies

### Backend Dependencies

```txt
razorpay==1.4.1           # Payment gateway
python-dateutil==2.8.2    # Date calculations
reportlab==4.0.7          # PDF generation
celery==5.3.4             # Background tasks (optional)
redis==5.0.1              # Caching (optional)
```

### Frontend Dependencies

```json
{
  "dependencies": {
    "razorpay": "^2.9.2",
    "date-fns": "^2.30.0",
    "react-hot-toast": "^2.4.1"
  }
}
```

---

## 🎨 UI/UX Design Specifications

### Subscription Plans Page

**Layout**: 3-column grid (responsive to 1-column on mobile)

**Color Scheme**:

- Monthly: Blue (#3B82F6)
- Quarterly: Purple (#8B5CF6) - Recommended
- Annual: Green (#10B981)

**Features**:

- Glassmorphism cards
- Hover animations
- Discount badges (10%, 20%)
- Feature checkmarks
- "Most Popular" ribbon on Annual plan

### Checkout Page

**Layout**: 2-column (Order Summary + Payment Form)

**Elements**:

- Plan details card
- Price breakdown
- Razorpay payment button
- Secure payment badge
- Terms checkbox
- Loading spinner

### Subscription Dashboard

**Layout**: Grid layout with cards

**Sections**:

1. Current Plan Card (large)
2. Expiry Countdown (medium)
3. Quick Stats (small cards)
4. Payment History Table (full width)

---

## 🔐 Security Checklist

- [ ] Use HTTPS in production
- [ ] Validate webhook signatures
- [ ] Sanitize all user inputs
- [ ] Implement rate limiting
- [ ] Use environment variables for secrets
- [ ] Encrypt sensitive data
- [ ] Implement CSRF protection
- [ ] Add request logging
- [ ] Set up security headers
- [ ] Regular security audits

---

## 📊 Success Metrics

### Technical Metrics

- Payment success rate: > 95%
- API response time: < 500ms
- Webhook processing: < 2s
- Zero payment data breaches

### Business Metrics

- Conversion rate: > 10%
- Annual plan selection: > 70%
- Churn rate: < 5%
- Auto-renewal success: > 90%

---

## 🚀 Launch Checklist

### Pre-Launch

- [ ] Complete all development tasks
- [ ] Pass all tests
- [ ] Security audit completed
- [ ] Performance optimization done
- [ ] Documentation complete
- [ ] Razorpay production account ready
- [ ] KYC verification complete
- [ ] Terms & conditions finalized
- [ ] Refund policy finalized
- [ ] Customer support ready

### Launch Day

- [ ] Deploy backend to production
- [ ] Deploy frontend to production
- [ ] Switch to production API keys
- [ ] Configure production webhook
- [ ] Test production payment flow
- [ ] Monitor error logs
- [ ] Monitor payment success rate
- [ ] Announce to users

### Post-Launch

- [ ] Monitor metrics daily
- [ ] Collect user feedback
- [ ] Fix critical bugs immediately
- [ ] Optimize based on data
- [ ] Plan feature enhancements

---

## 📈 Future Enhancements

### Phase 2 Features (Month 2-3)

- [ ] Referral program
- [ ] Promo codes
- [ ] Gift subscriptions
- [ ] Family plans
- [ ] Student discounts
- [ ] Corporate plans

### Phase 3 Features (Month 4-6)

- [ ] Multiple payment methods
- [ ] International pricing
- [ ] Subscription pause/resume
- [ ] Upgrade/downgrade mid-cycle
- [ ] Loyalty rewards
- [ ] Subscription analytics dashboard

---

## 🎯 Current Status

**Overall Progress**: 0% (Ready to start)

**Phase 1 (Backend)**: Not started

- Payment Service: ⬜ 0%
- Subscription Service: ⬜ 0%
- API Routes: ⬜ 0%
- Testing: ⬜ 0%

**Phase 2 (Frontend)**: Not started

- Plans Page: ⬜ 0%
- Checkout Page: ⬜ 0%
- Dashboard: ⬜ 0%
- Components: ⬜ 0%

**Phase 3 (Launch)**: Not started

- Testing: ⬜ 0%
- Documentation: ⬜ 0%
- Deployment: ⬜ 0%

---

## 📝 Notes

- Start with Razorpay test mode
- Test thoroughly before production
- Keep security as top priority
- Monitor payment success rate closely
- Collect user feedback continuously
- Iterate based on data

---

**Next Action**: Review this roadmap and start with Week 1, Day 1 tasks!

**Document Version**: 1.0  
**Last Updated**: December 8, 2025  
**Status**: Ready for Implementation
