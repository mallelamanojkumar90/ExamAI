@echo off
echo ========================================
echo Starting ExamAI Platform
echo ========================================
echo.

REM Start backend in a new window
echo Starting Backend Server...
start "ExamAI Backend" cmd /k "cd backend && call venv311\Scripts\activate.bat && python -m uvicorn main:app --reload --port 8000"

REM Wait a moment for backend to initialize
timeout /t 3 /nobreak > nul

REM Start frontend in a new window
echo Starting Frontend Server...
start "ExamAI Frontend" cmd /k "cd exam-app && npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit this window (servers will keep running)...
pause > nul
