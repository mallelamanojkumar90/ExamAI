# ExamAI Backend

FastAPI backend for ExamAI. It owns authentication, users, exam attempts, question generation, RAG ingestion, subscriptions, payments, and performance analytics.

## Setup

```bash
python -m venv venv311
.\venv311\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in database, AI provider, Pinecone, Redis, Razorpay, and frontend values.

## Run

```powershell
$env:PYTHONIOENCODING = "utf-8"
.\venv311\Scripts\python.exe -m uvicorn main:app --port 8000
```

API docs are available at `http://127.0.0.1:8000/docs`.

## Notes

- `uploads/` is runtime storage for uploaded documents and is intentionally ignored by Git.
- Local SQLite databases, bytecode, and cache folders are ignored.
- Google OAuth is mediated by the frontend NextAuth route, then forwarded to `/auth/google-signin` or `/auth/google-signup`.
