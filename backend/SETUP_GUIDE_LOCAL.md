# 🚀 Local PostgreSQL Setup - Step-by-Step Guide

## Current Status

✅ PostgreSQL 18 is installed and running on your system!

---

## 📋 Manual Setup Steps

Since the automated scripts require interactive password input, please follow these manual steps:

### Step 1: Create Database (2 minutes)

Open a **new PowerShell terminal** and run:

```powershell
cd C:\Manojkumar\development\Exam\backend

# Create the database
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "CREATE DATABASE exam_platform;"
```

**You will be prompted for your PostgreSQL password** (the one you set during installation).

**Expected output:**

```
CREATE DATABASE
```

If you see "database already exists", that's fine - it means it's already created.

---

### Step 2: Create .env File (1 minute)

Create a file named `.env` in the `backend` folder with this content:

```env
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/exam_platform

# Pinecone Configuration
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-environment
PINECONE_INDEX_NAME=your-index-name

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# JWT Secret
JWT_SECRET_KEY=exam-platform-secret-key-change-in-production

# Application Settings
PORT=8000
ENVIRONMENT=development
```

**IMPORTANT:** Replace `YOUR_PASSWORD` with your actual PostgreSQL password!

---

### Step 3: Install Dependencies (3 minutes)

In PowerShell, run:

```powershell
cd C:\Manojkumar\development\Exam\backend

python -m pip install psycopg2-binary sqlalchemy bcrypt alembic python-dotenv
```

**Expected output:**

```
Successfully installed psycopg2-binary-... sqlalchemy-... bcrypt-... alembic-... python-dotenv-...
```

---

### Step 4: Test Database Connection (1 minute)

```powershell
python database.py
```

**Expected output:**

```
Creating database tables...
✅ Database tables created successfully!
```

If you see this, your database connection is working! 🎉

---

### Step 5: Migrate Existing Data (2 minutes)

```powershell
python migrate_to_postgres.py
```

**Expected output:**

```
============================================================
🚀 Database Migration: SQLite → PostgreSQL
============================================================

1️⃣  Initializing PostgreSQL database...
✅ Database initialized successfully!

2️⃣  Migrating data...
📦 Migrating users...
✅ Migrated user: [usernames]
✨ Successfully migrated X users!

3️⃣  Setting up admin user...
✅ Admin user created successfully!
   Email: admin@exam.com
   Password: admin123

============================================================
✨ Migration completed!
============================================================
```

---

### Step 6: Update Backend Code (30 seconds)

```powershell
# Backup the old version
copy main.py main_sqlite_backup.py

# Use the PostgreSQL version
copy main_postgres.py main.py
```

---

### Step 7: Start the Server (1 minute)

```powershell
python main.py
```

**Expected output:**

```
INFO:     Started server process
INFO:     Waiting for application startup.
🚀 Starting ExamAI Backend...
✅ Database initialized!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## ✅ Verification

### Test 1: Health Check

Open browser and go to: http://localhost:8000

You should see:

```json
{
  "status": "online",
  "message": "ExamAI RAG Backend is running",
  "database": "PostgreSQL"
}
```

### Test 2: Admin Login

Try logging in with:

- **Email:** admin@exam.com
- **Password:** admin123

### Test 3: Check Database Tables

You can verify tables were created using pgAdmin or psql:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d exam_platform -c "\dt"
```

You should see 10 tables:

- users
- exams
- syllabus
- questions
- exam_attempts
- answers
- study_materials
- subscriptions
- payments
- reports

---

## 🐛 Troubleshooting

### Error: "password authentication failed"

**Solution:** Double-check your password in the `.env` file

### Error: "database does not exist"

**Solution:** Run Step 1 again to create the database

### Error: "could not connect to server"

**Solution:**

1. Check if PostgreSQL service is running:
   ```powershell
   Get-Service postgresql-x64-18
   ```
2. If stopped, start it:
   ```powershell
   Start-Service postgresql-x64-18
   ```

### Error: "No module named 'psycopg2'"

**Solution:** Run Step 3 again to install dependencies

---

## 📊 Quick Command Reference

```powershell
# Navigate to backend
cd C:\Manojkumar\development\Exam\backend

# Create database
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "CREATE DATABASE exam_platform;"

# Install dependencies
python -m pip install psycopg2-binary sqlalchemy bcrypt alembic python-dotenv

# Test connection
python database.py

# Migrate data
python migrate_to_postgres.py

# Backup and update
copy main.py main_sqlite_backup.py
copy main_postgres.py main.py

# Start server
python main.py
```

---

## 🎯 Success Checklist

After completing all steps, verify:

- [ ] Database `exam_platform` created
- [ ] `.env` file created with correct password
- [ ] Dependencies installed
- [ ] `python database.py` runs successfully
- [ ] Migration completed
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000
- [ ] Can login with admin account

---

## 🔐 Default Credentials

**Admin Account:**

- Email: admin@exam.com
- Password: admin123

⚠️ **Change this password in production!**

---

## 📞 Next Steps

After successful setup:

1. ✅ Test all existing features
2. ✅ Update Pinecone and OpenAI keys in `.env`
3. ✅ Test question generation
4. ✅ Test document upload
5. ✅ Review `PRD_GAP_ANALYSIS.md` for next features

---

**Setup Time:** ~10 minutes  
**Difficulty:** Easy  
**Status:** Ready to execute
