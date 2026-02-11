# ExamAI Platform - Startup Guide

This guide explains how to run both the frontend and backend of the ExamAI platform together.

## Prerequisites

### Backend Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Frontend Requirements
- Node.js 16 or higher
- npm (Node package manager)

## Installation

### First Time Setup

1. **Install Backend Dependencies (in virtual environment)**
   ```bash
   cd backend
   # Activate virtual environment
   .\venv311\Scripts\activate
   # Install dependencies
   pip install -r requirements.txt
   cd ..
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd exam-app
   npm install
   cd ..
   ```

3. **Install Root Dependencies (for npm method)**
   ```bash
   npm install
   ```

**Note:** The backend uses a Python virtual environment (`venv311`) to isolate dependencies.

## Running the Application

You have **three options** to run both frontend and backend together:

### Option 1: Using npm (Recommended for Development)

This method runs both servers in a single terminal with colored output.

```bash
npm run dev
```

This will start:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000

To stop both servers, press `Ctrl+C` in the terminal.

---

### Option 2: Using Windows Batch File

Double-click `start.bat` or run from terminal:

```bash
start.bat
```

This will open **two separate terminal windows**:
- One for the backend server
- One for the frontend server

To stop the servers, close each terminal window individually.

---

### Option 3: Using PowerShell Script

Right-click `start.ps1` and select "Run with PowerShell" or run from PowerShell terminal:

```powershell
.\start.ps1
```

This will open **two separate PowerShell windows**:
- One for the backend server
- One for the frontend server

To stop the servers, close each PowerShell window individually.

---

## Individual Server Commands

If you need to run servers separately:

### Backend Only
```bash
cd backend
.\venv311\Scripts\activate
python -m uvicorn main:app --reload --port 8000
```

### Frontend Only
```bash
cd exam-app
npm run dev
```

## Troubleshooting

### Port Already in Use

If you get a "port already in use" error:

**For Backend (Port 8000):**
```bash
# Find the process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the actual process ID)
taskkill /PID <PID> /F
```

**For Frontend (Port 3000):**
```bash
# Find the process using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with the actual process ID)
taskkill /PID <PID> /F
```

### Backend Not Starting

1. Ensure Python is installed: `python --version`
2. Ensure all dependencies are installed: `pip install -r backend/requirements.txt`
3. Check if `.env` file exists in the backend folder with required environment variables

### Frontend Not Starting

1. Ensure Node.js is installed: `node --version`
2. Ensure dependencies are installed: `cd exam-app && npm install`
3. Clear npm cache if needed: `npm cache clean --force`

## Environment Variables

Make sure you have a `.env` file in the `backend` folder with the following variables:

```env
# Database
DATABASE_URL=your_database_url

# API Keys
PINECONE_API_KEY=your_pinecone_key
OPENAI_API_KEY=your_openai_key

# Other configurations
PORT=8000
```

## Development Workflow

1. **Start the application** using any of the three methods above
2. **Make changes** to your code
3. **Auto-reload**: Both servers support hot-reload
   - Backend: Changes to Python files will auto-reload
   - Frontend: Changes to React/Next.js files will auto-reload
4. **View changes** in your browser at http://localhost:3000

## Production Deployment

For production deployment, refer to the deployment documentation specific to your hosting platform.

---

**Happy Coding! 🚀**
