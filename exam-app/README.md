# ExamAI Frontend

Next.js App Router frontend for ExamAI.

## Setup

```bash
npm install
copy env.example .env.local
npm run dev
```

The app runs at `http://localhost:3000`.

## Required Environment

```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Google OAuth

Both Google buttons force Google's account chooser. Login and signup set a short-lived intent cookie before redirecting to Google:

- Login uses `/auth/google-signin`.
- Signup uses `/auth/google-signup`.
- Duplicate Google signup returns to `/auth/signup?error=AccountAlreadyExists`.

## Verify

```bash
npm run build
```
