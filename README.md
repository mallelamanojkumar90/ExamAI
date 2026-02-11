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
- **Performance Analytics**: Track your progress and performance over time
- **Subscription Management**: Flexible subscription plans
- **Multi-Model Support**: Choose from various AI models for question generation
- **Question Caching**: Fast question delivery with intelligent caching
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
   REDIS_URL=redis://localhost:6379
   PORT=8000
   ```

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

### Performance
- `GET /performance/analytics` - Get performance analytics
- `GET /performance/subject-wise` - Subject-wise performance

### Subscription
- `GET /subscription/plans` - Get subscription plans
- `POST /subscription/subscribe` - Subscribe to a plan

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

### Backend Deployment
The backend can be deployed to platforms like:
- Render
- Heroku
- AWS EC2
- Google Cloud Run

### Frontend Deployment
The frontend can be deployed to:
- Vercel (recommended for Next.js)
- Netlify
- AWS Amplify

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
