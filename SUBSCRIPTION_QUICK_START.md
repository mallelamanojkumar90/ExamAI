# Subscription System - Quick Start Guide

## 🚀 Get Started in 30 Minutes

This guide will help you implement the subscription system step-by-step.

---

## Prerequisites

- ✅ PostgreSQL database running (you already have this)
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ⬜ Razorpay account (we'll create this)

---

## Step 1: Set Up Razorpay Account (10 minutes)

### 1.1 Create Account

1. Go to [https://razorpay.com/](https://razorpay.com/)
2. Click "Sign Up" → "For Testing" (use test mode first)
3. Complete registration with email

### 1.2 Get API Keys

1. Login to Razorpay Dashboard
2. Go to **Settings** → **API Keys**
3. Click **Generate Test Key**
4. Copy **Key ID** and **Key Secret**

### 1.3 Get Webhook Secret

1. Go to **Settings** → **Webhooks**
2. Click **Create Webhook**
3. Enter URL: `http://localhost:8000/api/payment/webhook`
4. Select events: `payment.captured`, `payment.failed`, `subscription.charged`
5. Copy the **Webhook Secret**

---

## Step 2: Update Environment Variables (2 minutes)

Edit `backend/.env`:

```env
# Add these lines at the end
RAZORPAY_KEY_ID=rzp_test_YOUR_KEY_ID_HERE
RAZORPAY_KEY_SECRET=YOUR_KEY_SECRET_HERE
RAZORPAY_WEBHOOK_SECRET=YOUR_WEBHOOK_SECRET_HERE

# Subscription Pricing (in INR)
MONTHLY_PLAN_PRICE=499
QUARTERLY_PLAN_PRICE=1347
ANNUAL_PLAN_PRICE=4788

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

---

## Step 3: Install Dependencies (2 minutes)

```powershell
cd backend
pip install razorpay python-dateutil reportlab
```

---

## Step 4: Create Backend Files (10 minutes)

The following files will be created automatically:

1. `backend/payment_service.py` - Razorpay integration
2. `backend/subscription_service.py` - Subscription logic
3. `backend/invoice_service.py` - Invoice generation
4. `backend/routes/subscription_routes.py` - API endpoints

These files are ready to be created. Would you like me to create them now?

---

## Step 5: Update Database (2 minutes)

Run database migrations:

```powershell
cd backend
python -c "from database import init_db; init_db()"
```

---

## Step 6: Test Backend APIs (2 minutes)

Start the backend:

```powershell
cd backend
py -m uvicorn main:app --reload --port 8000
```

Test the subscription plans endpoint:

```powershell
curl http://localhost:8000/api/subscription/plans
```

Expected response:

```json
{
  "plans": [
    {
      "id": "monthly",
      "name": "Monthly Plan",
      "price": 499,
      "duration_days": 30
    },
    ...
  ]
}
```

---

## Step 7: Create Frontend Pages (5 minutes)

The following pages will be created:

1. `exam-app/src/app/subscription/page.tsx` - Subscription plans
2. `exam-app/src/app/checkout/page.tsx` - Payment checkout
3. `exam-app/src/app/dashboard/subscription/page.tsx` - Subscription management
4. `exam-app/src/components/SubscriptionBadge.tsx` - Status indicator

---

## Step 8: Test Payment Flow (5 minutes)

### Test Cards (Razorpay Test Mode)

**Success:**

- Card: `4111 1111 1111 1111`
- CVV: Any 3 digits
- Expiry: Any future date

**Failure:**

- Card: `4000 0000 0000 0002`
- CVV: Any 3 digits
- Expiry: Any future date

### Test Flow

1. Go to `http://localhost:3000/subscription`
2. Click "Choose Plan" on Monthly plan
3. Complete payment with test card
4. Verify subscription activation

---

## 📁 File Structure

After implementation, your structure will be:

```
backend/
├── payment_service.py          # NEW - Razorpay integration
├── subscription_service.py     # NEW - Subscription logic
├── invoice_service.py          # NEW - Invoice generation
├── routes/
│   └── subscription_routes.py  # NEW - API endpoints
├── main.py                     # UPDATED - Add routes
└── .env                        # UPDATED - Add keys

exam-app/
├── src/
│   ├── app/
│   │   ├── subscription/
│   │   │   └── page.tsx        # NEW - Plans page
│   │   ├── checkout/
│   │   │   └── page.tsx        # NEW - Checkout page
│   │   └── dashboard/
│   │       └── subscription/
│   │           └── page.tsx    # NEW - Management page
│   └── components/
│       └── SubscriptionBadge.tsx # NEW - Status badge
```

---

## 🧪 Testing Checklist

- [ ] View subscription plans
- [ ] Click "Choose Plan"
- [ ] See Razorpay checkout
- [ ] Complete payment with test card
- [ ] See success message
- [ ] Check subscription status in dashboard
- [ ] View payment history
- [ ] Download invoice PDF
- [ ] Test payment failure scenario
- [ ] Test subscription expiry

---

## 🐛 Troubleshooting

### Issue: "Razorpay key not found"

**Solution**: Check `.env` file has correct keys, restart backend

### Issue: "Payment verification failed"

**Solution**: Check webhook secret is correct

### Issue: "Subscription not activated"

**Solution**: Check database connection, verify payment record created

### Issue: "Razorpay checkout not opening"

**Solution**: Check Razorpay key in frontend, check browser console

---

## 📊 Monitoring

### Check Active Subscriptions

```sql
SELECT COUNT(*) FROM subscriptions WHERE payment_status = 'active';
```

### Check Today's Revenue

```sql
SELECT SUM(amount) FROM payments
WHERE DATE(payment_date) = CURRENT_DATE AND status = 'success';
```

### Check Failed Payments

```sql
SELECT * FROM payments WHERE status = 'failed' ORDER BY payment_date DESC;
```

---

## 🎯 Next Steps After Implementation

1. **Test thoroughly** with all test cards
2. **Review security** - ensure HTTPS in production
3. **Set up monitoring** - track payment success rate
4. **Prepare customer support** - FAQs, refund policy
5. **Plan launch** - marketing, pricing strategy
6. **Go live** - switch to production keys

---

## 📞 Support

- **Razorpay Support**: support@razorpay.com
- **Razorpay Docs**: https://razorpay.com/docs/
- **Test Cards**: https://razorpay.com/docs/payments/payments/test-card-details/

---

**Ready to start?** Let's create the backend files first!
