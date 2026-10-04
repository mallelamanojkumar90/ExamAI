# ExamAI Platform

An intelligent exam preparation platform powered by RAG (Retrieval-Augmented Generation) technology, supporting IIT-JEE, NEET, and EAMCET exam preparation.

**This is a monorepo** containing both the frontend (Next.js) and backend (FastAPI) in a single Git repository for easier development and deployment.

## 🚀 Quick Start

### Run Both Frontend and Backend Together

**Easiest Method - Using npm:**
```bash
npm run dev
```

**Alternative Methods:**
- **Windows Batch**: Double-click `start.bat`
- **PowerShell**: Run `.\start.ps1`

For detailed setup instructions, see [STARTUP_GUIDE.md](./STARTUP_GUIDE.md)

## 📋 Features

- **AI-Powered Question Generation**: Generate exam questions using advanced AI models
- **Multiple Exam Types**: Support for IIT-JEE, NEET, and EAMCET
- **Document Upload**: Upload study materials for RAG-based question generation
- **Performance Analytics**: Accuracy, subject and difficulty breakdown, trends, peer comparison, and recommendations
- **Exam Taking**: Timer, question palette, mark for review, and save-and-resume
- **Subscription Management**: Monthly, quarterly, and annual plans with Razorpay
- **Multi-Model Support**: Choose from various AI models for question generation
- **Question Caching**: Redis cache for repeated question sets
- **Google OAuth**: Sign in with your Google account

## 🛠️ Tech Stack

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Recharts** - Data visualization
- **NextAuth** - Authentication

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **Pinecone** - Vector database for RAG
- **OpenAI/Groq** - AI model providers
- **Redis** - Caching layer
- **bcrypt** - Password hashing

## 📁 Project Structure

```
Exam/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application entry
│   ├── database.py         # Database models and setup
│   ├── rag_service.py      # RAG implementation
│   ├── model_service.py    # AI model management
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── exam-app/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app directory
│   │   └── components/    # React components
│   ├── package.json       # Node dependencies
│   └── next.config.js     # Next.js configuration
├── package.json           # Root package.json for running both servers
├── start.bat             # Windows batch startup script
├── start.ps1             # PowerShell startup script
└── STARTUP_GUIDE.md      # Detailed startup instructions
```

## 🔧 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis (optional, for caching)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Exam
   ```

2. **Install dependencies**
   ```bash
   # Install root dependencies
   npm install

   # Install backend dependencies
   cd backend
   pip install -r requirements.txt
   cd ..

   # Install frontend dependencies
   cd exam-app
   npm install
   cd ..
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the `backend` folder:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/examai
   PINECONE_API_KEY=your_pinecone_api_key
   OPENAI_API_KEY=your_openai_api_key
   REDIS_HOST=localhost
   REDIS_PORT=6379
   PORT=8000
   ```

   Local Postgres does not use SSL. A Supabase `DATABASE_URL` does. Redis is optional; if it is not running, questions are generated live and are not cached.

4. **Run the application**
   ```bash
   npm run dev
   ```

   The application will be available at:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📖 Documentation

- [Startup Guide](./STARTUP_GUIDE.md) - Detailed instructions for running the application
- [Git Guide](./GIT_GUIDE.md) - Monorepo workflow and Git best practices
- [Troubleshooting](./TROUBLESHOOTING.md) - Common issues and solutions
- [PRD Compliance Check](./PRD_COMPLIANCE_CHECK.md) - Product requirements compliance
- [Migration Guide](./README_MIGRATION.md) - Database migration information

## 🔄 Git Workflow

This is a **monorepo** - both frontend and backend are in one Git repository.

```bash
# Quick start
git add .
git commit -m "feat: Your feature description"
git push origin master

# Or use the helper script
git-commit.bat
```

For detailed Git workflows, see [GIT_GUIDE.md](./GIT_GUIDE.md)

## 🎯 Usage

1. **Sign Up/Login**: Create an account or sign in with Google
2. **Upload Study Materials**: Upload PDFs for RAG-based question generation
3. **Generate Questions**: Select subject, difficulty, and exam type
4. **Take Exams**: Practice with AI-generated questions
5. **Track Progress**: View your performance analytics
6. **Manage Subscription**: Upgrade for premium features

## 🔑 API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/google-signin` - Google OAuth login

### Question Generation
- `POST /generate-questions` - Generate exam questions
- `GET /models` - Get available AI models
- `GET /exam-types` - Get supported exam types

### Document Management
- `POST /upload-document` - Upload study material
- `GET /documents` - List uploaded documents

### Exam attempts
- `POST /exams/attempts/start` - Save a generated paper so it can be resumed
- `GET /exams/attempts/{attempt_id}` - Load a saved paper
- `PUT /exams/attempts/{attempt_id}/progress` - Save answers in progress
- `POST /submit-exam` - Finish an attempt and store each question and answer

### Performance
- `GET /api/performance/dashboard/{user_id}` - Summary, timeline, peers, and recommendations

### Subscription
- `GET /api/subscription/plans` - Get subscription plans
- `POST /api/payment/create-order` - Start a Razorpay checkout

For complete API documentation, visit http://localhost:8000/docs after starting the backend.

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd exam-app
npm test
```

## 🚢 Deployment

The hosted layout is Vercel for the frontend, Render for the backend, and Supabase for Postgres. See [DEPLOYMENT.md](./DEPLOYMENT.md).

The schema migration is `backend/supabase/migrations/20260301120000_initial_exam_schema.sql`. `backend/migrate_to_supabase.py` copies rows from a local Postgres database when `SOURCE_DATABASE_URL` and `DATABASE_URL` are set. Do not commit exported SQL; those dumps can contain user records.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- OpenAI for GPT models
- Pinecone for vector database
- FastAPI and Next.js communities

---

**Need Help?** Check out the [STARTUP_GUIDE.md](./STARTUP_GUIDE.md) for detailed setup instructions.
