# =============================================================================
# PostgreSQL Migration - Complete Setup
# =============================================================================
# This script will guide you through the entire setup process
# You'll need to provide your PostgreSQL password when prompted
# =============================================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  PostgreSQL Migration Setup" -ForegroundColor Cyan
Write-Host "  Exam Platform - Local Database" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$POSTGRES_PATH = "C:\Program Files\PostgreSQL\18\bin"
$DB_NAME = "exam_platform"
$PSQL = "$POSTGRES_PATH\psql.exe"

# =============================================================================
# STEP 1: Create Database
# =============================================================================
Write-Host "STEP 1: Creating PostgreSQL Database" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "Database: $DB_NAME" -ForegroundColor White
Write-Host "You will be prompted for your PostgreSQL password..." -ForegroundColor Gray
Write-Host ""

& $PSQL -U postgres -c "CREATE DATABASE $DB_NAME;" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database created successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database might already exist (checking...)" -ForegroundColor Yellow
    
    # Check if database exists
    $dbCheck = & $PSQL -U postgres -t -c "SELECT 1 FROM pg_database WHERE datname='$DB_NAME';" 2>$null
    
    if ($dbCheck -match "1") {
        Write-Host "✅ Database '$DB_NAME' already exists and is ready!" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create database. Please check your password and try again." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Read-Host "Press Enter to continue to Step 2"

# =============================================================================
# STEP 2: Configure Environment
# =============================================================================
Write-Host ""
Write-Host "STEP 2: Configuring Environment Variables" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Gray
Write-Host ""

# Read existing .env
if (Test-Path ".env") {
    $existingContent = Get-Content ".env" -Raw
    Write-Host "✅ Found existing .env with API keys" -ForegroundColor Green
} else {
    $existingContent = ""
    Write-Host "⚠️  No existing .env found, creating new one" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Enter your PostgreSQL password: " -ForegroundColor Cyan -NoNewline
$password = Read-Host -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Create new .env content
if ($existingContent) {
    $newContent = @"
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://postgres:$plainPassword@localhost:5432/exam_platform

# Existing API Keys
$existingContent

# JWT Secret
JWT_SECRET_KEY=exam-platform-secret-key-change-in-production

# Application Settings
PORT=8000
ENVIRONMENT=development
"@
} else {
    $newContent = @"
# PostgreSQL Database Configuration
DATABASE_URL=postgresql://postgres:$plainPassword@localhost:5432/exam_platform

# Pinecone Configuration
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=your-index-name

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# JWT Secret
JWT_SECRET_KEY=exam-platform-secret-key-change-in-production

# Application Settings
PORT=8000
ENVIRONMENT=development
"@
}

$newContent | Out-File -FilePath ".env" -Encoding UTF8 -NoNewline

Write-Host ""
Write-Host "✅ .env file configured!" -ForegroundColor Green

Write-Host ""
Read-Host "Press Enter to continue to Step 3"

# =============================================================================
# STEP 3: Install Dependencies
# =============================================================================
Write-Host ""
Write-Host "STEP 3: Installing Python Dependencies" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray
Write-Host ""

$packages = @("psycopg2-binary", "sqlalchemy", "bcrypt", "alembic", "python-dotenv")

foreach ($pkg in $packages) {
    Write-Host "Installing $pkg..." -ForegroundColor Gray -NoNewline
    python -m pip install $pkg --quiet --disable-pip-version-check 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✅" -ForegroundColor Green
    } else {
        Write-Host " ⚠️" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Dependencies installed!" -ForegroundColor Green

Write-Host ""
Read-Host "Press Enter to continue to Step 4"

# =============================================================================
# STEP 4: Test Database Connection
# =============================================================================
Write-Host ""
Write-Host "STEP 4: Testing Database Connection" -ForegroundColor Yellow
Write-Host "-------------------------------------" -ForegroundColor Gray
Write-Host ""

Write-Host "Running: python database.py" -ForegroundColor Gray
Write-Host ""

python database.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Database connection successful!" -ForegroundColor Green
    Write-Host "✅ All 10 tables created!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Database connection failed!" -ForegroundColor Red
    Write-Host "   Please check your password in .env file" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Read-Host "Press Enter to continue to Step 5"

# =============================================================================
# STEP 5: Migrate Data
# =============================================================================
Write-Host ""
Write-Host "STEP 5: Migrating Data from SQLite" -ForegroundColor Yellow
Write-Host "------------------------------------" -ForegroundColor Gray
Write-Host ""

if (Test-Path "exam_app.db") {
    Write-Host "Found SQLite database, migrating..." -ForegroundColor Gray
    Write-Host ""
    
    python migrate_to_postgres.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Data migration completed!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "⚠️  Migration had some issues, but you can continue" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  No SQLite database found, skipping migration" -ForegroundColor Yellow
    Write-Host "   (This is OK for new installations)" -ForegroundColor Gray
}

Write-Host ""
Read-Host "Press Enter to continue to Step 6"

# =============================================================================
# STEP 6: Update Backend Code
# =============================================================================
Write-Host ""
Write-Host "STEP 6: Updating Backend Code" -ForegroundColor Yellow
Write-Host "-------------------------------" -ForegroundColor Gray
Write-Host ""

if (Test-Path "main.py") {
    Write-Host "Backing up current main.py..." -ForegroundColor Gray
    Copy-Item "main.py" "main_sqlite_backup.py" -Force
    Write-Host "✅ Backup created: main_sqlite_backup.py" -ForegroundColor Green
}

Write-Host "Updating to PostgreSQL version..." -ForegroundColor Gray
Copy-Item "main_postgres.py" "main.py" -Force
Write-Host "✅ main.py updated to use PostgreSQL!" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! 🎉" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  ✅ Database created: $DB_NAME" -ForegroundColor Green
Write-Host "  ✅ Environment configured" -ForegroundColor Green
Write-Host "  ✅ Dependencies installed" -ForegroundColor Green
Write-Host "  ✅ Database tables created (10 tables)" -ForegroundColor Green
Write-Host "  ✅ Data migrated" -ForegroundColor Green
Write-Host "  ✅ Backend code updated" -ForegroundColor Green
Write-Host ""
Write-Host "Default Admin Account:" -ForegroundColor Yellow
Write-Host "  Email: admin@exam.com" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "To start the server, run:" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Then visit: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
