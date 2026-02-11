Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting ExamAI Platform (Same Window)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start backend in background job
Write-Host "Starting Backend Server on port 8000..." -ForegroundColor Green
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Manojkumar\development\Exam\backend"
    & .\venv311\Scripts\Activate.ps1
    python -m uvicorn main:app --reload --port 8000
}

# Wait a bit for backend to start
Start-Sleep -Seconds 5

# Start frontend in background job  
Write-Host "Starting Frontend Server on port 3000..." -ForegroundColor Green
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Manojkumar\development\Exam\exam-app"
    npm run dev
}

# Wait a bit for frontend to start
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Both servers are starting!" -ForegroundColor Green
Write-Host "Backend: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop both servers..." -ForegroundColor Gray
Write-Host ""

# Show combined logs
Write-Host "=== Server Logs ===" -ForegroundColor Cyan
try {
    while ($true) {
        $backendOutput = Receive-Job -Job $backendJob -ErrorAction SilentlyContinue
        $frontendOutput = Receive-Job -Job $frontendJob -ErrorAction SilentlyContinue
        
        if ($backendOutput) {
            Write-Host "[BACKEND] " -ForegroundColor Green -NoNewline
            Write-Host $backendOutput
        }
        if ($frontendOutput) {
            Write-Host "[FRONTEND] " -ForegroundColor Blue -NoNewline
            Write-Host $frontendOutput
        }
        
        Start-Sleep -Milliseconds 500
    }
} finally {
    Write-Host ""
    Write-Host "Stopping servers..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob, $frontendJob
    Remove-Job -Job $backendJob, $frontendJob
    Write-Host "Servers stopped." -ForegroundColor Green
}
