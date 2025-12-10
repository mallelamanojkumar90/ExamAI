# OAuth Integration Guide

**Date:** December 9, 2025  
**Status:** NextAuth.js Installed, Configuration Needed  
**Estimated Time:** 1-2 hours

---

## ✅ Completed

1. **NextAuth.js Installed** ✅
   - Package: `next-auth` and `@auth/core`
   - 20 packages added
   - Ready to configure

---

## 🔧 OAuth Setup Steps

### Step 1: Google Cloud Console Setup (15 minutes)

1. **Go to Google Cloud Console**

   - Visit: https://console.cloud.google.com/

2. **Create New Project** (if needed)

   - Click "Select a project" → "New Project"
   - Name: "ExamAI Platform"
   - Click "Create"

3. **Enable Google+ API**

   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Web application"
   - Name: "ExamAI Web App"
5. **Configure Authorized URLs**

   - **Authorized JavaScript origins:**

     - `http://localhost:3000`
     - `https://yourdomain.com` (for production)

   - **Authorized redirect URIs:**
     - `http://localhost:3000/api/auth/callback/google`
     - `https://yourdomain.com/api/auth/callback/google` (for production)

6. **Save Credentials**
   - Copy **Client ID**
   - Copy **Client Secret**
   - Keep these safe!

---

### Step 2: Environment Variables (5 minutes)

Create `.env.local` in `exam-app/` directory:

```env
# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-random-secret-key-here-generate-with-openssl

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Generate NEXTAUTH_SECRET:**

```bash
# On Windows PowerShell:
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})

# On Linux/Mac:
openssl rand -base64 32
```

---

### Step 3: Create NextAuth Configuration (10 minutes)

**File:** `exam-app/src/app/api/auth/[...nextauth]/route.ts`

```typescript
import NextAuth, { NextAuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions: NextAuthOptions = {
  providers: [
    // Google OAuth Provider
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),

    // Email/Password Provider (existing)
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.username || !credentials?.password) {
          return null;
        }

        try {
          const response = await fetch("http://localhost:8000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              username: credentials.username,
              password: credentials.password,
            }),
          });

          if (response.ok) {
            const data = await response.json();
            return {
              id: credentials.username,
              email: credentials.username,
              name: data.username,
              role: data.role,
            };
          }
        } catch (error) {
          console.error("Auth error:", error);
        }

        return null;
      },
    }),
  ],

  callbacks: {
    async signIn({ user, account, profile }) {
      // Handle Google OAuth sign-in
      if (account?.provider === "google") {
        try {
          // Check if user exists in backend
          const response = await fetch(
            "http://localhost:8000/auth/oauth-login",
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                email: user.email,
                name: user.name,
                provider: "google",
                provider_id: account.providerAccountId,
              }),
            }
          );

          if (response.ok) {
            return true;
          }
        } catch (error) {
          console.error("OAuth sign-in error:", error);
        }
      }

      return true;
    },

    async jwt({ token, user, account }) {
      if (user) {
        token.role = user.role;
      }
      return token;
    },

    async session({ session, token }) {
      if (session.user) {
        session.user.role = token.role as string;
      }
      return session;
    },
  },

  pages: {
    signIn: "/",
    error: "/",
  },

  session: {
    strategy: "jwt",
  },
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
```

---

### Step 4: Update Login Page (15 minutes)

**File:** `exam-app/src/app/page.tsx`

Add Google Sign-In button:

```typescript
import { signIn } from "next-auth/react";

// Add this button in your login form:
<button
  type="button"
  onClick={() => signIn("google", { callbackUrl: "/dashboard" })}
  className="w-full py-3 px-4 bg-white hover:bg-gray-100 text-gray-800 font-semibold rounded-lg border border-gray-300 flex items-center justify-center gap-3 transition-colors"
>
  <svg className="w-5 h-5" viewBox="0 0 24 24">
    <path
      fill="#4285F4"
      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
    />
    <path
      fill="#34A853"
      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
    />
    <path
      fill="#FBBC05"
      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
    />
    <path
      fill="#EA4335"
      d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
    />
  </svg>
  Sign in with Google
</button>;
```

---

### Step 5: Add Session Provider (10 minutes)

**File:** `exam-app/src/app/layout.tsx`

Wrap your app with SessionProvider:

```typescript
import { SessionProvider } from "next-auth/react";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  );
}
```

---

### Step 6: Backend OAuth Endpoint (15 minutes)

**File:** `backend/main.py`

Add OAuth login endpoint:

```python
class OAuthLogin(BaseModel):
    email: str
    name: Optional[str] = None
    provider: str
    provider_id: str

@app.post("/auth/oauth-login")
def oauth_login(oauth_data: OAuthLogin, db: Session = Depends(get_db)):
    """Handle OAuth login (Google, etc.)"""
    # Check if user exists
    user = db.query(User).filter(User.email == oauth_data.email).first()

    if not user:
        # Create new user
        user = User(
            email=oauth_data.email,
            full_name=oauth_data.name,
            password_hash="",  # No password for OAuth users
            role="student",
            created_at=datetime.utcnow(),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    return {
        "message": "OAuth login successful",
        "username": user.email,
        "role": user.role
    }
```

---

## 🧪 Testing OAuth

### Test Flow:

1. Start both servers (backend and frontend)
2. Go to `http://localhost:3000`
3. Click "Sign in with Google"
4. Google login popup should appear
5. Select your Google account
6. Grant permissions
7. Should redirect to `/dashboard`
8. Check if user is created in database

### Troubleshooting:

- **"Redirect URI mismatch"**: Check Google Console redirect URIs
- **"Invalid client"**: Check GOOGLE_CLIENT_ID in .env.local
- **"Callback error"**: Check NEXTAUTH_URL in .env.local
- **Backend error**: Check if OAuth endpoint exists

---

## 📝 Files to Create

1. ✅ `.env.local` - Environment variables
2. ✅ `exam-app/src/app/api/auth/[...nextauth]/route.ts` - NextAuth config
3. ✅ Update `exam-app/src/app/page.tsx` - Add Google button
4. ✅ Update `exam-app/src/app/layout.tsx` - Add SessionProvider
5. ✅ Update `backend/main.py` - Add OAuth endpoint

---

## 🎯 Benefits of OAuth

1. **Better UX**: One-click sign-in
2. **Security**: No password storage
3. **Trust**: Users trust Google
4. **Speed**: Faster registration
5. **Professional**: Modern auth standard

---

## ⚠️ Important Notes

1. **Google Console**: Must complete Step 1 first
2. **Environment Variables**: Keep .env.local secret
3. **HTTPS**: Production requires HTTPS
4. **Callback URL**: Must match exactly
5. **Testing**: Test with real Google account

---

## 🚀 Next Steps After OAuth

1. Test OAuth flow thoroughly
2. Add email verification (optional)
3. Add password recovery
4. Move to Testing Setup (Task 4)

---

**Status:** Configuration guide complete  
**Next Action:** Follow steps 1-6 to implement OAuth  
**Estimated Time:** 1-2 hours total

**Document Version:** 1.0  
**Created:** December 9, 2025
