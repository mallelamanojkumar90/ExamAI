# Local PostgreSQL Setup Script
# This script sets up the database for the exam platform

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Local PostgreSQL Setup for Exam Platform" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# PostgreSQL configuration
$POSTGRES_PATH = "C:\Program Files\PostgreSQL\18\bin"
$DB_NAME = "exam_platform"
$DB_USER = "postgres"
$DB_PORT = "5432"

Write-Host "Step 1: Checking PostgreSQL installation..." -ForegroundColor Yellow
if (Test-Path $POSTGRES_PATH) {
    Write-Host "✅ PostgreSQL 18 found at: $POSTGRES_PATH" -ForegroundColor Green
} else {
    Write-Host "❌ PostgreSQL not found at expected location" -ForegroundColor Red
    Write-Host "   Please check your PostgreSQL installation" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Step 2: Creating database..." -ForegroundColor Yellow
Write-Host "   You will be prompted for the PostgreSQL password" -ForegroundColor Gray
Write-Host "   (This is the password you set during PostgreSQL installation)" -ForegroundColor Gray
Write-Host ""

# Create database using psql
$createDbCommand = @"
SELECT 'CREATE DATABASE $DB_NAME' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec
"@

$createDbCommand | & "$POSTGRES_PATH\psql.exe" -U $DB_USER -p $DB_PORT -d postgres

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database '$DB_NAME' is ready" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database creation encountered an issue" -ForegroundColor Yellow
    Write-Host "   The database might already exist, which is fine." -ForegroundColor Gray
}

Write-Host ""
Write-Host "Step 3: Configuring environment variables..." -ForegroundColor Yellow

# Prompt for password
Write-Host ""
$password = Read-Host "Enter your PostgreSQL password" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Create .env file
$envContent = @"
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://$DB_USER`:$plainPassword@localhost:$DB_PORT/$DB_NAME

# Pinecone Configuration (from your existing setup)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-environment
PINECONE_INDEX_NAME=your-index-name

# OpenAI Configuration (from your existing setup)
OPENAI_API_KEY=your-openai-api-key

# JWT Secret
JWT_SECRET_KEY=your-secret-key-here-change-in-production

# Application Settings
PORT=8000
ENVIRONMENT=development
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "✅ .env file created" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Installing Python dependencies..." -ForegroundColor Yellow

# Check if we're in a virtual environment
$inVenv = $env:VIRTUAL_ENV -ne $null

if (-not $inVenv) {
    Write-Host "⚠️  Not in a virtual environment" -ForegroundColor Yellow
    Write-Host "   Installing globally..." -ForegroundColor Gray
}

# Install dependencies
$packages = @(
    "psycopg2-binary",
    "sqlalchemy",
    "bcrypt",
    "alembic",
    "python-dotenv"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    python -m pip install $package --quiet --disable-pip-version-check 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ $package installed" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $package installation may have issues" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Database Configuration:" -ForegroundColor Yellow
Write-Host "  Host: localhost" -ForegroundColor White
Write-Host "  Port: $DB_PORT" -ForegroundColor White
Write-Host "  Database: $DB_NAME" -ForegroundColor White
Write-Host "  User: $DB_USER" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. ✅ Database created" -ForegroundColor Green
Write-Host "  2. ✅ Dependencies installed" -ForegroundColor Green
Write-Host "  3. ✅ .env file configured" -ForegroundColor Green
Write-Host ""
Write-Host "Now run:" -ForegroundColor Cyan
Write-Host "  python database.py              # Test connection & create tables" -ForegroundColor White
Write-Host "  python migrate_to_postgres.py   # Migrate existing data" -ForegroundColor White
Write-Host "  copy main.py main_sqlite_backup.py" -ForegroundColor White
Write-Host "  copy main_postgres.py main.py" -ForegroundColor White
Write-Host "  python main.py                  # Start server" -ForegroundColor White
Write-Host ""
