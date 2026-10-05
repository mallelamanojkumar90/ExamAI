# Startup Guide

This guide explains how to run the ExamAI frontend and backend locally.

## Prerequisites

- Python 3.11
- Node.js and npm
- PostgreSQL or Supabase connection string
- Optional Redis server for question caching

## First-Time Setup

Install root and frontend dependencies:

```bash
npm install

cd exam-app
npm install
cd ..
```

Install backend dependencies:

```powershell
cd backend
python -m venv venv311
.\venv311\Scripts\activate
pip install -r requirements.txt
cd ..
```

Create environment files:

- Copy `backend/.env.example` to `backend/.env`.
- Copy `exam-app/env.example` to `exam-app/.env.local`.

## Run Everything

From the repository root:

```bash
npm run dev
```

This starts:

- Backend: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`
- Frontend: `http://localhost:3000`

## Run Servers Separately

Backend:

```powershell
cd backend
$env:PYTHONIOENCODING = "utf-8"
.\venv311\Scripts\activate
python -m uvicorn main:app --port 8000
```

Frontend:

```bash
cd exam-app
npm run dev
```

## Windows Launch Scripts

You can also use:

- `start.bat` to open backend and frontend in separate Command Prompt windows.
- `start.ps1` to open backend and frontend in separate PowerShell windows.
- `start-combined.ps1` to run both as background jobs in one PowerShell window.

## Notes

- The backend startup sets `PYTHONIOENCODING=utf-8` because backend logs include Unicode symbols.
- The default backend command avoids `uvicorn --reload`; reload can hit Windows named-pipe permission issues in some environments.
- Uploaded documents are written to `backend/uploads/` at runtime and are ignored by Git.

## Troubleshooting

Port already in use:

```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Missing Python packages:

```powershell
cd backend
.\venv311\Scripts\activate
pip install -r requirements.txt
```

Frontend dependency issues:

```bash
cd exam-app
npm install
npm run dev
```
