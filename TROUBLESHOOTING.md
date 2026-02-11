# Troubleshooting Guide

## Common Issues and Solutions

### 1. "API Error: Internal Server Error" in Frontend

**Symptoms:**
- Frontend shows "API Error: Internal Server Error"
- Questions fail to generate

**Possible Causes & Solutions:**

#### A. OpenAI API Key Issues
```bash
# Check if API key is set
cd backend
.\venv311\Scripts\activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OpenAI Key:', os.getenv('OPENAI_API_KEY')[:20] + '...')"
```

**Solution:** Verify your OpenAI API key in `backend/.env` is valid and has credits.

#### B. Database Connection Issues
```bash
# Test database connection
cd backend
.\venv311\Scripts\activate
python -c "from database import init_db; init_db(); print('DB OK')"
```

**Solution:** Ensure PostgreSQL is running and DATABASE_URL in `.env` is correct.

#### C. Pinecone Connection Issues
```bash
# Test Pinecone connection
cd backend
.\venv311\Scripts\activate
python -c "from pinecone import Pinecone; import os; from dotenv import load_dotenv; load_dotenv(); pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY')); print('Pinecone OK')"
```

**Solution:** Verify PINECONE_API_KEY in `.env` is valid.

---

### 2. Backend Not Starting

**Symptoms:**
- "Connection error. Please ensure the backend server is running."
- Cannot access http://localhost:8000

**Solutions:**

#### Check if backend is running:
```powershell
netstat -ano | findstr :8000
```

#### Check for port conflicts:
```powershell
# Kill process on port 8000
taskkill /F /PID <PID>
```

#### Restart backend:
```bash
# Stop all
Ctrl+C in the npm run dev terminal

# Restart
npm run dev
```

---

### 3. Virtual Environment Issues

**Symptoms:**
- "ModuleNotFoundError" errors
- "bcrypt" or other packages not found

**Solution:**
```bash
cd backend
.\venv311\Scripts\activate
pip install -r requirements.txt
```

---

### 4. Redis Cache Warnings

**Symptoms:**
- "⚠️ Redis connection failed" in logs
- Cache disabled warnings

**Impact:** Non-critical - questions will be generated in real-time instead of cached.

**Solution (Optional):**
1. Install Redis for Windows
2. Start Redis server
3. Restart backend

---

### 5. Frontend Build Errors

**Symptoms:**
- Next.js compilation errors
- Module not found errors

**Solution:**
```bash
cd exam-app
rm -rf .next node_modules
npm install
npm run dev
```

---

### 6. Database Migration Issues

**Symptoms:**
- "Table does not exist" errors
- Schema mismatch errors

**Solution:**
```bash
cd backend
.\venv311\Scripts\activate
python -c "from database import init_db; init_db()"
```

---

## Quick Health Check

Run this script to check all services:

```powershell
# Check Backend
curl http://localhost:8000

# Check Frontend
curl http://localhost:3000

# Check Database
cd backend
.\venv311\Scripts\activate
python -c "from database import get_db; next(get_db()); print('DB OK')"

# Check API Keys
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OpenAI:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'); print('Pinecone:', 'SET' if os.getenv('PINECONE_API_KEY') else 'NOT SET')"
```

---

## Getting Help

If you're still experiencing issues:

1. Check the backend logs in the terminal running `npm run dev`
2. Check the browser console for frontend errors (F12)
3. Look for error messages in the terminal output
4. Verify all environment variables in `backend/.env`

---

## Environment Variables Checklist

Make sure these are set in `backend/.env`:

- ✅ `DATABASE_URL` - PostgreSQL connection string
- ✅ `PINECONE_API_KEY` - Pinecone API key
- ✅ `PINECONE_INDEX_NAME` - Pinecone index name (default: rag-questions)
- ✅ `OPENAI_API_KEY` - OpenAI API key
- ⚪ `REDIS_URL` - Redis connection (optional)
- ⚪ `GOOGLE_API_KEY` - Google Gemini (optional)
- ⚪ `ANTHROPIC_API_KEY` - Claude (optional)
