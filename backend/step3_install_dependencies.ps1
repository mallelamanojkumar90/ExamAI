# Step 3: Install Python Dependencies
# This installs all required packages for PostgreSQL

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Installing Python Dependencies" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$packages = @(
    "psycopg2-binary",
    "sqlalchemy", 
    "bcrypt",
    "alembic",
    "python-dotenv"
)

Write-Host "Installing packages..." -ForegroundColor Yellow
Write-Host ""

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Gray
    python -m pip install $package --quiet --disable-pip-version-check
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ $package" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $package failed" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✅ Dependencies installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. python database.py              # Test connection & create tables" -ForegroundColor White
Write-Host "  2. python migrate_to_postgres.py   # Migrate existing data" -ForegroundColor White
Write-Host "  3. copy main.py main_sqlite_backup.py" -ForegroundColor White
Write-Host "  4. copy main_postgres.py main.py" -ForegroundColor White
Write-Host "  5. python main.py                  # Start server" -ForegroundColor White
Write-Host ""
