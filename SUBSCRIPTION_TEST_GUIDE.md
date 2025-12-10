# 🚀 Subscription System - Quick Test Guide

## ⚡ Quick Start (5 Minutes)

### 1. Set Up Razorpay (2 minutes)

```
1. Go to https://razorpay.com/ → Sign Up (Test Mode)
2. Dashboard → Settings → API Keys → Generate Test Key
3. Copy Key ID and Key Secret
4. Settings → Webhooks → Create Webhook
5. URL: http://localhost:8000/api/payment/webhook
6. Copy Webhook Secret
```

### 2. Update .env (1 minute)

```env
RAZORPAY_KEY_ID=rzp_test_YOUR_KEY_HERE
RAZORPAY_KEY_SECRET=YOUR_SECRET_HERE
RAZORPAY_WEBHOOK_SECRET=YOUR_WEBHOOK_SECRET_HERE
MONTHLY_PLAN_PRICE=499
QUARTERLY_PLAN_PRICE=1347
ANNUAL_PLAN_PRICE=4788
FRONTEND_URL=http://localhost:3000
```

### 3. Restart Backend (1 minute)

```powershell
# Stop current backend (Ctrl+C)
cd c:\Manojkumar\development\Exam\backend
py -m uvicorn main:app --reload --port 8000
```

### 4. Test Flow (1 minute)

```
1. Open: http://localhost:3000/subscription
2. Click "Choose Plan" on any plan
3. Click "Pay ₹XXX"
4. Use test card: 4111 1111 1111 1111
5. CVV: 123, Expiry: 12/25
6. Click Pay
7. See success page! 🎉
```

---

## 📋 Test Checklist

### Backend APIs

- [ ] GET http://localhost:8000/api/subscription/plans
- [ ] POST http://localhost:8000/api/payment/create-order
- [ ] POST http://localhost:8000/api/payment/verify
- [ ] GET http://localhost:8000/api/subscription/status/1
- [ ] GET http://localhost:8000/api/payment/history/1

### Frontend Pages

- [ ] http://localhost:3000/subscription (Plans page)
- [ ] http://localhost:3000/checkout?plan=monthly (Checkout)
- [ ] http://localhost:3000/payment/success (Success page)
- [ ] http://localhost:3000/payment/failure (Failure page)
- [ ] http://localhost:3000/dashboard/subscription (Dashboard)

### Payment Flow

- [ ] View plans
- [ ] Select plan
- [ ] See Razorpay checkout
- [ ] Complete payment
- [ ] See success message
- [ ] Check subscription status
- [ ] Download invoice

---

## 🧪 Test Cards

### ✅ Success

```
Card: 4111 1111 1111 1111
CVV: Any 3 digits
Expiry: Any future date
```

### ❌ Failure

```
Card: 4000 0000 0000 0002
CVV: Any 3 digits
Expiry: Any future date
```

---

## 🔍 Quick Debug

### Backend Not Starting?

```powershell
# Check if dependencies installed
py -m pip list | findstr razorpay

# Reinstall if needed
py -m pip install razorpay==1.4.1 reportlab==4.0.7
```

### Frontend Not Loading?

```powershell
# Check if running
# Should see: http://localhost:3000

# Restart if needed
cd c:\Manojkumar\development\Exam\exam-app
npm run dev
```

### Payment Not Working?

```
1. Check .env has correct Razorpay keys
2. Check backend console for errors
3. Check browser console for errors
4. Verify Razorpay script loaded (F12 → Network)
```

---

## 📊 Quick Status Check

### Check Subscription Status

```bash
curl http://localhost:8000/api/subscription/status/1
```

### Check Payment History

```bash
curl http://localhost:8000/api/payment/history/1
```

### Check Plans

```bash
curl http://localhost:8000/api/subscription/plans
```

---

## 🎯 Expected Results

### After Successful Payment:

1. ✅ Payment record in database
2. ✅ Subscription record created
3. ✅ Invoice PDF generated
4. ✅ Success page shown
5. ✅ Subscription status = "active"

### Dashboard Should Show:

- Current plan type
- Days remaining
- Start and end dates
- Payment history
- Download invoice button

---

## 🚨 Common Issues

### Issue: "Razorpay is not defined"

**Fix**: Razorpay script not loaded. Check internet connection.

### Issue: "Invalid payment signature"

**Fix**: Check RAZORPAY_KEY_SECRET in .env is correct.

### Issue: "Order creation failed"

**Fix**: Check RAZORPAY_KEY_ID in .env is correct.

### Issue: "Invoice not found"

**Fix**: Check `backend/invoices/` folder exists.

---

## 📞 Need Help?

1. Check `SUBSCRIPTION_IMPLEMENTATION_COMPLETE.md` for full details
2. Check `SUBSCRIPTION_QUICK_START.md` for setup guide
3. Check Razorpay docs: https://razorpay.com/docs/

---

**Ready to test? Start with Step 1! 🚀**
