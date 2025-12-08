# PostgreSQL Migration Guide

## Overview

This guide will help you migrate from SQLite to PostgreSQL as per the PRD requirements (Section 3.3).

## Prerequisites

- PostgreSQL installed locally OR Supabase account (recommended)
- Python 3.8+
- Existing exam-app project

---

## Option 1: Using Supabase (Recommended - Free Tier Available)

### Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up / Log in
3. Click "New Project"
4. Fill in:
   - **Project Name**: exam-platform
   - **Database Password**: (save this securely!)
   - **Region**: Choose closest to you
5. Wait for project to be created (~2 minutes)

### Step 2: Get Connection Details

1. In your Supabase project dashboard, go to **Settings** → **Database**
2. Find the **Connection String** section
3. Copy the **URI** format connection string
4. It will look like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```

### Step 3: Configure Environment Variables

1. Create a `.env` file in the `backend` folder:

   ```bash
   cd backend
   copy .env.example .env
   ```

2. Edit `.env` and add your Supabase connection string:

   ```env
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

   # Your existing environment variables
   PINECONE_API_KEY=your-pinecone-key
   OPENAI_API_KEY=your-openai-key
   ```

---

## Option 2: Using Local PostgreSQL

### Step 1: Install PostgreSQL

**Windows:**

1. Download from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run installer
3. Remember the password you set for the `postgres` user
4. Default port: 5432

### Step 2: Create Database

1. Open **pgAdmin** or **psql**
2. Create a new database:
   ```sql
   CREATE DATABASE exam_platform;
   ```

### Step 3: Configure Environment Variables

Create `.env` file in `backend` folder:

```env
DATABASE_URL=postgresql://postgres:your-password@localhost:5432/exam_platform

# Your existing environment variables
PINECONE_API_KEY=your-pinecone-key
OPENAI_API_KEY=your-openai-key
```

---

## Migration Steps

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:

- `psycopg2-binary` - PostgreSQL adapter
- `sqlalchemy` - ORM for database operations
- `bcrypt` - Password hashing
- `alembic` - Database migrations

### Step 2: Test Database Connection

```bash
python database.py
```

Expected output:

```
Creating database tables...
✅ Database tables created successfully!
```

### Step 3: Run Migration Script

```bash
python migrate_to_postgres.py
```

This will:

1. ✅ Create all required tables in PostgreSQL
2. ✅ Migrate existing users from SQLite
3. ✅ Create default admin user

Expected output:

```
============================================================
🚀 Database Migration: SQLite → PostgreSQL
============================================================

1️⃣  Initializing PostgreSQL database...
✅ Database initialized successfully!

2️⃣  Migrating data...
📦 Migrating users...
✅ Migrated user: user1@example.com
✅ Migrated user: user2@example.com
✨ Successfully migrated 2 users!

3️⃣  Setting up admin user...
✅ Admin user created successfully!
   Email: admin@exam.com
   Password: admin123
   ⚠️  Please change the password in production!

============================================================
✨ Migration completed!
============================================================
```

### Step 4: Update Backend to Use PostgreSQL

```bash
# Backup old main.py
copy main.py main_sqlite_backup.py

# Replace with PostgreSQL version
copy main_postgres.py main.py
```

### Step 5: Restart Backend Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --port 8000
```

---

## Verification

### 1. Check Database Tables

**Using Supabase:**

- Go to **Table Editor** in Supabase dashboard
- You should see all 9 tables:
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

**Using pgAdmin:**

- Connect to your database
- Expand **Schemas** → **public** → **Tables**
- Verify all tables are created

### 2. Test API Endpoints

```bash
# Health check
curl http://localhost:8000/

# Should return:
{
  "status": "online",
  "message": "ExamAI RAG Backend is running",
  "database": "PostgreSQL"
}
```

### 3. Test Login

Try logging in with the admin account:

- Email: `admin@exam.com`
- Password: `admin123`

---

## Database Schema (PRD Section 9.1)

The migration creates the following tables:

### Core Tables

1. **users** - User accounts (students & admins)
2. **exams** - Exam metadata (IIT/JEE, NEET, etc.)
3. **syllabus** - Exam syllabi with topics
4. **questions** - Question bank
5. **exam_attempts** - Student exam attempts
6. **answers** - Individual question answers
7. **study_materials** - Uploaded documents
8. **subscriptions** - User subscriptions
9. **payments** - Payment transactions
10. **reports** - Generated PDF reports

### Relationships

- Users → Exam Attempts (one-to-many)
- Exams → Questions (one-to-many)
- Exam Attempts → Answers (one-to-many)
- Users → Subscriptions (one-to-many)
- Subscriptions → Payments (one-to-many)

---

## Troubleshooting

### Error: "could not connect to server"

**Solution:**

- Check if PostgreSQL is running
- Verify DATABASE_URL in `.env` is correct
- Check firewall settings

### Error: "password authentication failed"

**Solution:**

- Double-check your password in DATABASE_URL
- Ensure no special characters need URL encoding

### Error: "database does not exist"

**Solution:**

- Create the database first (see Step 2 in Local PostgreSQL setup)

### Error: "relation already exists"

**Solution:**

- Tables already created, safe to ignore
- Or drop all tables and re-run migration

---

## Next Steps

After successful migration:

1. ✅ **Test all existing features** to ensure backward compatibility
2. ✅ **Implement exam type selection** (IIT/JEE, NEET, EAMCET)
3. ✅ **Add syllabus management** (admin feature)
4. ✅ **Implement subscription system** (payment gateway)
5. ✅ **Add performance tracking** (student dashboard)

Refer to `PRD_GAP_ANALYSIS.md` for the complete implementation roadmap.

---

## Rollback (If Needed)

If you need to rollback to SQLite:

```bash
# Restore old main.py
copy main_sqlite_backup.py main.py

# Restart server
python main.py
```

Your SQLite database (`exam_app.db`) is still intact and can be used.

---

## Security Notes

⚠️ **Important:**

1. Never commit `.env` file to Git
2. Change default admin password immediately
3. Use strong passwords in production
4. Enable SSL for database connections in production
5. Regularly backup your database

---

## Support

If you encounter issues:

1. Check the error logs
2. Verify all environment variables are set
3. Ensure PostgreSQL is running
4. Review the PRD document (Section 3.3 - Database)

---

**Document Version:** 1.0  
**Last Updated:** December 8, 2025  
**Status:** Migration Guide
