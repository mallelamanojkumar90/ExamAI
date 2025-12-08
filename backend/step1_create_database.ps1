# Step 1: Create PostgreSQL Database
# Run this script to create the exam_platform database

$POSTGRES_PATH = "C:\Program Files\PostgreSQL\18\bin"
$DB_NAME = "exam_platform"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Creating PostgreSQL Database" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Database Name: $DB_NAME" -ForegroundColor Yellow
Write-Host "You will be prompted for your PostgreSQL password..." -ForegroundColor Gray
Write-Host ""

# Create database
& "$POSTGRES_PATH\psql.exe" -U postgres -c "CREATE DATABASE $DB_NAME;"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Database '$DB_NAME' created successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠️  Database might already exist (this is OK)" -ForegroundColor Yellow
    Write-Host "   Or there was an authentication issue" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Next: Run step2_configure_env.ps1" -ForegroundColor Cyan
