# PostgreSQL Migration Setup Script
# Run this script to install dependencies and set up the database

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  PostgreSQL Migration Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python installation
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Step 2: Install dependencies
Write-Host ""
Write-Host "Step 2: Installing PostgreSQL dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

$packages = @(
    "psycopg2-binary",
    "sqlalchemy",
    "bcrypt",
    "alembic",
    "python-dotenv"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    python -m pip install $package --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ $package installed" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $package installation failed" -ForegroundColor Yellow
    }
}

# Step 3: Check for .env file
Write-Host ""
Write-Host "Step 3: Checking environment configuration..." -ForegroundColor Yellow

if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
    Write-Host "   Creating .env from template..." -ForegroundColor Gray
    
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ .env file created from template" -ForegroundColor Green
        Write-Host ""
        Write-Host "⚠️  IMPORTANT: Edit .env file and add your database connection string!" -ForegroundColor Red
        Write-Host "   Example: DATABASE_URL=postgresql://user:password@host:port/database" -ForegroundColor Gray
    } else {
        Write-Host "❌ .env.example not found!" -ForegroundColor Red
    }
}

# Step 4: Summary
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Setup Summary" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Set up PostgreSQL database (Supabase or local)" -ForegroundColor White
Write-Host "  2. Edit .env file with your DATABASE_URL" -ForegroundColor White
Write-Host "  3. Run: python database.py (to test connection)" -ForegroundColor White
Write-Host "  4. Run: python migrate_to_postgres.py (to migrate data)" -ForegroundColor White
Write-Host "  5. Run: python main.py (to start server)" -ForegroundColor White
Write-Host ""
Write-Host "📖 See POSTGRESQL_MIGRATION_GUIDE.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""
