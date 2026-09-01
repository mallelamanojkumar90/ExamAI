# Deployment Guide: Vercel + Render + Supabase

Deploy ExamAI with:
- **Frontend** → Vercel (`exam-app`)
- **Backend** → Render (`backend`)
- **Database** → Supabase (PostgreSQL)

---

## 1. Supabase (Database)

1. Go to [supabase.com](https://supabase.com) and create a new project.
2. Open **Project Settings → Database**.
3. Copy the **Connection string (URI)** under **Connection pooling** or **Direct connection**.
   - Use the **Transaction** pooler URL for serverless-friendly connections.
   - Example format:
     ```
     postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
     ```
4. If your password contains special characters, URL-encode them (e.g. `@` → `%40`).
5. Keep this URL — you'll use it as `DATABASE_URL` on Render.

### Initialize tables

After the backend is deployed, tables are created automatically on startup via `init_db()`.
You can also run locally against Supabase:

```bash
cd backend
.\venv311\Scripts\activate
set DATABASE_URL=your-supabase-connection-string
python -c "from database import init_db; init_db()"
```

---

## 2. Render (Backend)

### Option A: Blueprint (recommended)

1. Push this repo to GitHub (already at `https://github.com/mallelamanojkumar90/ExamAI`).
2. Open the Render Blueprint deeplink:
   ```
   https://dashboard.render.com/blueprint/new?repo=https://github.com/mallelamanojkumar90/ExamAI
   ```
3. Click **Apply** and fill in secret environment variables:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Supabase PostgreSQL connection string |
| `FRONTEND_URL` | Your Vercel URL (e.g. `https://examai.vercel.app`) |
| `ALLOWED_ORIGINS` | Optional extra origins, comma-separated |
| `PINECONE_API_KEY` | From pinecone.io |
| `PINECONE_INDEX_NAME` | Your Pinecone index name |
| `OPENAI_API_KEY` | From platform.openai.com |
| `JWT_SECRET_KEY` | Random secret string |
| `RAZORPAY_KEY_ID` | Razorpay test/live key |
| `RAZORPAY_KEY_SECRET` | Razorpay secret |
| `REDIS_URL` | Optional — Upstash Redis URL |

4. Wait for deploy to finish. Note your backend URL, e.g.:
   ```
   https://examai-backend.onrender.com
   ```

### Option B: Manual Web Service

1. [Render Dashboard](https://dashboard.render.com) → **New → Web Service**
2. Connect GitHub repo `ExamAI`
3. Settings:
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add the environment variables from the table above.

---

## 3. Vercel (Frontend)

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub.
2. **Add New Project** → import `mallelamanojkumar90/ExamAI`.
3. Configure:
   - **Root Directory:** `exam-app`
   - **Framework Preset:** Next.js (auto-detected)
4. Add environment variables:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | Render backend URL (e.g. `https://examai-backend.onrender.com`) |
| `NEXTAUTH_URL` | Your Vercel URL (e.g. `https://examai.vercel.app`) |
| `NEXTAUTH_SECRET` | Random secret (generate with `openssl rand -base64 32`) |
| `GOOGLE_CLIENT_ID` | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | From Google Cloud Console |

5. Click **Deploy**.

### CLI deploy (alternative)

```bash
cd exam-app
npx vercel --prod
```

---

## 4. Post-deploy checklist

### Update Render CORS
Set `FRONTEND_URL` on Render to your final Vercel URL after the first deploy.

### Google OAuth
In [Google Cloud Console](https://console.cloud.google.com/apis/credentials):
- Add authorized redirect URI:
  ```
  https://your-app.vercel.app/api/auth/callback/google
  ```

### Razorpay
- Update webhook URL to point to your Render backend if using payments.

### Test endpoints
- Backend health: `https://your-backend.onrender.com/`
- API docs: `https://your-backend.onrender.com/docs`
- Frontend: `https://your-app.vercel.app`

---

## Environment variable summary

```
# Vercel (exam-app)
NEXT_PUBLIC_API_URL=https://examai-backend.onrender.com
NEXTAUTH_URL=https://examai.vercel.app
NEXTAUTH_SECRET=<random-secret>
GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client-secret>

# Render (backend)
DATABASE_URL=postgresql://postgres.[ref]:[password]@...supabase.com:6543/postgres
FRONTEND_URL=https://examai.vercel.app
PINECONE_API_KEY=<key>
PINECONE_INDEX_NAME=<index>
OPENAI_API_KEY=<key>
JWT_SECRET_KEY=<secret>
RAZORPAY_KEY_ID=<key>
RAZORPAY_KEY_SECRET=<secret>
```

---

## Notes

- Render free tier services **sleep after inactivity** — first request may take ~30s.
- Supabase free tier includes 500MB database storage.
- Vercel free tier is sufficient for the Next.js frontend.
- Redis is optional; the app works without it (questions generated in real-time).
