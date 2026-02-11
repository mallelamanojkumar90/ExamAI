@echo off
echo ========================================
echo Git Commit Helper
echo ========================================
echo.

REM Check if Git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    echo.
)

REM Show current status
echo Current Git Status:
echo ----------------------------------------
git status
echo.

REM Ask for commit message
set /p commit_msg="Enter commit message: "

if "%commit_msg%"=="" (
    echo Error: Commit message cannot be empty!
    pause
    exit /b 1
)

REM Add all changes
echo.
echo Adding all changes...
git add .

REM Show what will be committed
echo.
echo Files to be committed:
git status --short

REM Confirm
echo.
set /p confirm="Commit these changes? (y/n): "

if /i "%confirm%"=="y" (
    git commit -m "%commit_msg%"
    echo.
    echo ✅ Changes committed successfully!
    echo.
    echo To push to remote, run: git push origin master
) else (
    echo.
    echo ❌ Commit cancelled.
    git reset
)

echo.
pause
