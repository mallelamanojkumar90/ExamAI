# 🚀 PostgreSQL Migration - Quick Start

## ⚡ TL;DR - Fastest Path

### Option 1: Supabase (Recommended - 5 minutes)

```bash
# 1. Go to https://supabase.com and create a project
# 2. Copy your connection string
# 3. Run these commands:

cd backend
.\setup_postgres.ps1                    # Install dependencies
# Edit .env and paste your DATABASE_URL
python database.py                      # Test connection
python migrate_to_postgres.py           # Migrate data
copy main.py main_sqlite_backup.py      # Backup old version
copy main_postgres.py main.py           # Use new version
python main.py                          # Start server
```

### Option 2: Local PostgreSQL (15 minutes)

```bash
# 1. Install PostgreSQL from postgresql.org
# 2. Create database: CREATE DATABASE exam_platform;
# 3. Run these commands:

cd backend
.\setup_postgres.ps1                    # Install dependencies
# Edit .env: DATABASE_URL=postgresql://postgres:password@localhost:5432/exam_platform
python database.py                      # Test connection
python migrate_to_postgres.py           # Migrate data
copy main.py main_sqlite_backup.py      # Backup old version
copy main_postgres.py main.py           # Use new version
python main.py                          # Start server
```

---

## 📋 Files Created

| File                            | Purpose                       |
| ------------------------------- | ----------------------------- |
| `database.py`                   | PostgreSQL models (10 tables) |
| `migrate_to_postgres.py`        | Migration script              |
| `main_postgres.py`              | Updated backend               |
| `.env.example`                  | Config template               |
| `setup_postgres.ps1`            | Setup automation              |
| `POSTGRESQL_MIGRATION_GUIDE.md` | Full guide                    |
| `MIGRATION_SUMMARY.md`          | Technical details             |

---

## 🎯 What Changed

### Database

- **Before:** SQLite (3 tables)
- **After:** PostgreSQL (10 tables)
- **Compliance:** 33% → 100% (PRD Section 9.1)

### New Tables

1. ✅ users (enhanced)
2. ✅ exams
3. ✅ syllabus
4. ✅ questions
5. ✅ exam_attempts
6. ✅ answers
7. ✅ study_materials
8. ✅ subscriptions
9. ✅ payments
10. ✅ reports

---

## ✅ Testing

After migration, test:

```bash
# Health check
curl http://localhost:8000/

# Login (admin)
# Email: admin@exam.com
# Password: admin123

# Check users
curl http://localhost:8000/admin/users
```

---

## 🆘 Troubleshooting

### Can't connect to database

- Check DATABASE_URL in `.env`
- Verify PostgreSQL is running
- Test with: `python database.py`

### Migration fails

- Check if tables already exist
- Verify SQLite database exists
- Check error logs

### Server won't start

- Check all dependencies installed
- Verify .env file exists
- Check port 8000 is free

---

## 📞 Need Help?

1. Read `POSTGRESQL_MIGRATION_GUIDE.md` (detailed)
2. Read `MIGRATION_SUMMARY.md` (technical)
3. Check `PRD_GAP_ANALYSIS.md` (roadmap)

---

## 🎉 Success Criteria

✅ Server starts without errors  
✅ Can login with admin account  
✅ Can create new users  
✅ Can generate questions  
✅ Can upload documents  
✅ Can submit exams

---

**Quick Start Version:** 1.0  
**Estimated Time:** 5-15 minutes  
**Difficulty:** Easy
