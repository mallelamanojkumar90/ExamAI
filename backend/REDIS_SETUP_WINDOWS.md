# Redis Setup for Windows - Easy Installation Guide

## Option 1: Download Pre-Built Redis (Recommended - Easiest)

### Step 1: Download Redis

1. Download from: https://github.com/tporadowski/redis/releases
2. Get the latest `.zip` file (e.g., `Redis-x64-5.0.14.1.zip`)
3. Extract to `C:\Redis`

### Step 2: Start Redis

```powershell
cd C:\Redis
.\redis-server.exe
```

Keep this window open - Redis is now running!

### Step 3: Test Redis (in a new PowerShell window)

```powershell
cd C:\Redis
.\redis-cli.exe ping
# Should return: PONG
```

---

## Option 2: Use Docker (If you have Docker Desktop)

```powershell
docker run -d -p 6379:6379 --name redis-cache redis:latest
```

Test:

```powershell
docker exec -it redis-cache redis-cli ping
# Should return: PONG
```

---

## Option 3: Use Memurai (Redis-compatible for Windows)

1. Download from: https://www.memurai.com/get-memurai
2. Install the free developer edition
3. It runs as a Windows service automatically

---

## Quick Test Without Installing Redis

**You can test the system WITHOUT Redis!** The cache will be disabled but questions will still work (just slower).

Just skip Redis installation and:

1. Start backend: `cd backend && python main.py`
2. You'll see: `⚠️ Redis cache disabled - questions will be generated in real-time`
3. Everything still works, just without caching

---

## Recommended: Download Pre-Built Redis

**Direct download link:**
https://github.com/tporadowski/redis/releases/download/v5.0.14.1/Redis-x64-5.0.14.1.zip

**Quick steps:**

1. Download and extract to `C:\Redis`
2. Run `C:\Redis\redis-server.exe`
3. Done! ✅

---

## After Redis is Running

Continue with the setup:

```powershell
# Install Python dependency
cd backend
pip install redis

# Add to .env
# REDIS_HOST=localhost
# REDIS_PORT=6379

# Start backend
python main.py
```

You should see:

```
✅ Redis connected: localhost:6379
🔥 Warming question cache...
```
