# ExamAI

ExamAI is a full-stack exam preparation platform for IIT/JEE, NEET, and EAMCET practice. The app combines a Next.js frontend, a FastAPI backend, PostgreSQL persistence, Redis-backed question caching, Pinecone retrieval, and AI-generated practice questions.

This repository is a monorepo:

```text
Exam/
├── backend/      FastAPI API, SQLAlchemy models, RAG, payments, analytics
├── exam-app/     Next.js App Router frontend and NextAuth routes
├── package.json  Root scripts for running both apps
└── render.yaml   Render backend deployment blueprint
```

## Features

- Email/password authentication.
- Google OAuth login and signup.
- Google signup rejects an email that already has an account.
- Exam dashboards for IIT/JEE, NEET, and EAMCET.
- AI question generation with RAG fallback behavior.
- Redis question caching and cache warming.
- Document upload and ingestion for study material.
- Exam attempts, answer tracking, and performance analytics.
- Razorpay subscription and payment flows.

## Prerequisites

- Node.js and npm.
- Python 3.11.
- PostgreSQL or Supabase.
- Redis, optional but recommended for caching.
- Pinecone and OpenAI API credentials for RAG/question generation.
- Google OAuth credentials for Google sign-in.

## Environment

Backend environment values belong in `backend/.env`. Start from `backend/.env.example`.

Frontend environment values belong in `exam-app/.env.local`. Start from `exam-app/env.example`.

Important frontend values:

```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

For local Google OAuth, add this redirect URI in Google Cloud Console:

```text
http://localhost:3000/api/auth/callback/google
```

For production, add the deployed frontend origin:

```text
https://your-frontend-domain/api/auth/callback/google
```

## Install

```bash
npm install

cd exam-app
npm install

cd ../backend
python -m venv venv311
.\venv311\Scripts\activate
pip install -r requirements.txt
```

## Run Locally

From the repository root:

```bash
npm run dev
```

This starts:

- Frontend: `http://localhost:3000`
- Backend: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

On Windows, the backend script sets `PYTHONIOENCODING=utf-8` so Unicode log output does not crash the console. The default backend command intentionally avoids `uvicorn --reload`; use reload manually only if your local shell supports it cleanly.

## Auth Behavior

Google login and Google signup intentionally do different things:

- `Sign in with Google` calls `/auth/google-signin` and requires an existing account.
- `Sign up with Google` calls `/auth/google-signup` and fails with an account-exists error when the email is already registered.
- Both flows force Google's account chooser with `prompt=select_account`.

## Runtime Files

The repository does not track generated/runtime content:

- `backend/uploads/` is created when documents are uploaded.
- `*.db`, `__pycache__/`, `*.pyc`, `.next/`, `node_modules/`, and local env files are ignored.
- Large uploaded PDFs and local databases should stay outside Git.

## Verification

Frontend build:

```bash
cd exam-app
npm run build
```

Backend syntax check:

```bash
cd backend
.\venv311\Scripts\python.exe -m py_compile main.py
```

Backend smoke checks after starting the server:

```bash
curl http://127.0.0.1:8000/docs
curl http://localhost:3000/api/auth/providers
```

## Deployment

- Frontend: Vercel, from `exam-app`.
- Backend: Render, from `backend`, using `render.yaml`.
- Database: Supabase/PostgreSQL.

See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment-specific environment variables and OAuth redirect setup.

## Useful Docs

- [DEPLOYMENT.md](./DEPLOYMENT.md)
- [STARTUP_GUIDE.md](./STARTUP_GUIDE.md)
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
