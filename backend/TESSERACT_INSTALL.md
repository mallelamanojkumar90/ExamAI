# Tesseract OCR Installation Guide for Windows

## The Issue
Your scanned PDF uploads are failing because the Tesseract OCR engine is not installed or not found in your system PATH.

## Solution: Install Tesseract OCR

### Step 1: Download Tesseract
1. Visit: https://github.com/UB-Mannheim/tesseract/wiki
2. Download the latest Windows installer (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)

### Step 2: Install Tesseract
1. Run the installer
2. **Important**: During installation, note the installation path (usually `C:\Program Files\Tesseract-OCR`)
3. Complete the installation

### Step 3: Verify Installation
Open PowerShell and run:
```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

You should see output like:
```
tesseract 5.3.3
```

### Step 4: Restart Backend
After installing Tesseract, restart your backend server:
```powershell
# Stop the current server (Ctrl+C)
# Then restart:
py main.py
```

## Alternative: Add Tesseract to PATH

If you've already installed Tesseract but it's not being found:

1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find and select "Path"
5. Click "Edit"
6. Click "New"
7. Add: `C:\Program Files\Tesseract-OCR` (or wherever you installed it)
8. Click "OK" on all dialogs
9. **Restart your terminal and backend**

## Testing OCR

After installation, upload a scanned PDF. You should see in the backend console:
```
⚠️  WARNING: Very little text detected. Attempting OCR fallback...
Found Tesseract at: C:\Program Files\Tesseract-OCR\tesseract.exe
   OCR processing page 1/5...
   OCR processing page 2/5...
   ...
✅ OCR extracted text from 5 pages.
```

## Still Having Issues?

If Tesseract is installed in a different location, you can manually configure it:

1. Find where `tesseract.exe` is located on your system
2. Edit `backend/rag_service.py` and add the path to the `tesseract_paths` list (around line 17)
3. Restart the backend
