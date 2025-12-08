# Quick .env Update Script
# This will add PostgreSQL configuration to your existing .env file

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Update .env with PostgreSQL Configuration" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Read existing .env content
$existingContent = Get-Content ".env" -Raw

Write-Host "Current .env file contains your API keys ✅" -ForegroundColor Green
Write-Host ""
Write-Host "Enter your PostgreSQL password: " -ForegroundColor Yellow -NoNewline
$password = Read-Host -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Add PostgreSQL configuration
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

$newContent | Out-File -FilePath ".env" -Encoding UTF8 -NoNewline

Write-Host ""
Write-Host "✅ .env file updated successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Your .env now contains:" -ForegroundColor Yellow
Write-Host "  ✅ DATABASE_URL (PostgreSQL)" -ForegroundColor Green
Write-Host "  ✅ PINECONE_API_KEY" -ForegroundColor Green
Write-Host "  ✅ OPENAI_API_KEY" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Install dependencies" -ForegroundColor Cyan
Write-Host "Run: .\step3_install_dependencies.ps1" -ForegroundColor White
Write-Host ""
