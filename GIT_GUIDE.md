# Git Monorepo Guide

## Repository Structure

Your ExamAI project is set up as a **monorepo** - a single Git repository containing both frontend and backend:

```
Exam/                          ← Git Repository Root
├── .git/                      ← Git metadata
├── .gitignore                 ← Ignore rules
├── README.md                  ← Main documentation
├── package.json               ← Root package.json (runs both servers)
├── backend/                   ← Python/FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   ├── venv311/              ← Ignored by Git
│   └── .env                  ← Ignored by Git
├── exam-app/                  ← Next.js frontend
│   ├── src/
│   ├── package.json
│   └── node_modules/         ← Ignored by Git
└── start.bat, start.ps1      ← Startup scripts
```

## Benefits of Monorepo

✅ **Single source of truth** - All code in one place  
✅ **Atomic commits** - Frontend + backend changes in one commit  
✅ **Easier collaboration** - One repo to clone  
✅ **Shared tooling** - Common scripts and configs  
✅ **Simplified deployment** - Deploy both together  

---

## Initial Setup (First Time)

### 1. Add All Files to Git

```bash
# Add all new files
git add .

# Check what will be committed
git status

# Create initial commit
git commit -m "Initial commit: ExamAI monorepo with frontend and backend"
```

### 2. Connect to Remote Repository

If you don't have a remote repository yet:

```bash
# Create a new repo on GitHub/GitLab/Bitbucket first, then:
git remote add origin https://github.com/yourusername/ExamAI.git

# Push to remote
git branch -M main
git push -u origin main
```

If you already have a remote (which you do - origin/master):

```bash
# Just push
git push origin master
```

---

## Daily Git Workflow

### 1. Before Starting Work

```bash
# Pull latest changes
git pull origin master

# Create a new branch for your feature
git checkout -b feature/your-feature-name
```

### 2. Making Changes

```bash
# Check what changed
git status

# Add specific files
git add backend/main.py
git add exam-app/src/components/NewComponent.tsx

# Or add all changes
git add .

# Commit with a descriptive message
git commit -m "feat: Add new feature description"
```

### 3. Pushing Changes

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a Pull Request on GitHub/GitLab
# After review and merge, switch back to main
git checkout master
git pull origin master
```

---

## Commit Message Conventions

Use conventional commits for better history:

```bash
# Features
git commit -m "feat: Add user authentication"
git commit -m "feat(backend): Add new API endpoint"
git commit -m "feat(frontend): Add dashboard page"

# Bug fixes
git commit -m "fix: Resolve login issue"
git commit -m "fix(backend): Fix database connection"

# Documentation
git commit -m "docs: Update README with setup instructions"

# Refactoring
git commit -m "refactor: Improve code structure"

# Chores
git commit -m "chore: Update dependencies"
git commit -m "chore: Add .gitignore rules"
```

---

## Common Git Commands

### Checking Status

```bash
# See what changed
git status

# See detailed changes
git diff

# See commit history
git log --oneline
```

### Branching

```bash
# List branches
git branch

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout master

# Delete branch
git branch -d feature/old-feature
```

### Undoing Changes

```bash
# Discard changes in a file
git restore backend/main.py

# Unstage a file
git restore --staged backend/main.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - CAREFUL!
git reset --hard HEAD~1
```

### Stashing Changes

```bash
# Save changes temporarily
git stash

# List stashes
git stash list

# Apply stashed changes
git stash pop
```

---

## Working with Both Frontend and Backend

### Scenario 1: Change Only Backend

```bash
# Make changes to backend files
git add backend/
git commit -m "feat(backend): Add new API endpoint"
git push
```

### Scenario 2: Change Only Frontend

```bash
# Make changes to frontend files
git add exam-app/
git commit -m "feat(frontend): Add new component"
git push
```

### Scenario 3: Change Both (Atomic Commit)

```bash
# Make changes to both frontend and backend
git add backend/ exam-app/
git commit -m "feat: Add user profile feature (frontend + backend)"
git push
```

---

## Ignoring Files

The `.gitignore` file already excludes:

- ✅ `venv311/` - Python virtual environment
- ✅ `node_modules/` - Node.js dependencies
- ✅ `.env` files - Environment variables (secrets)
- ✅ `__pycache__/` - Python cache
- ✅ `.next/` - Next.js build output
- ✅ `uploads/` - Uploaded files
- ✅ `*.db` - Database files

**Never commit:**
- API keys or secrets
- Virtual environments
- node_modules
- Build outputs
- Database files
- Uploaded user files

---

## Syncing with Remote

### Pull Latest Changes

```bash
# Pull from master
git checkout master
git pull origin master

# Update your feature branch with latest master
git checkout feature/your-feature
git merge master
```

### Resolve Merge Conflicts

If you get conflicts:

```bash
# 1. Git will mark conflicts in files
# 2. Open conflicted files and resolve manually
# 3. After resolving:
git add .
git commit -m "merge: Resolve conflicts"
```

---

## Deployment Workflow

### Option 1: Deploy from Main Branch

```bash
# Merge feature to main
git checkout master
git merge feature/your-feature
git push origin master

# Deploy (manual or CI/CD will trigger)
```

### Option 2: Deploy from Tags

```bash
# Create a release tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Deploy specific tag
```

---

## Collaboration Workflow

### For Team Members

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/ExamAI.git
   cd ExamAI
   ```

2. **Install dependencies**
   ```bash
   # Install root dependencies
   npm install
   
   # Install backend dependencies
   cd backend
   .\venv311\Scripts\activate
   pip install -r requirements.txt
   cd ..
   
   # Install frontend dependencies
   cd exam-app
   npm install
   cd ..
   ```

3. **Set up environment**
   ```bash
   # Copy .env.example to .env
   cp backend/.env.example backend/.env
   # Edit .env with your API keys
   ```

4. **Start working**
   ```bash
   git checkout -b feature/my-feature
   # Make changes
   git commit -m "feat: My feature"
   git push origin feature/my-feature
   ```

---

## Best Practices

1. ✅ **Commit often** - Small, focused commits
2. ✅ **Write clear messages** - Describe what and why
3. ✅ **Pull before push** - Stay up to date
4. ✅ **Use branches** - Don't commit directly to master
5. ✅ **Review before commit** - Use `git diff` and `git status`
6. ✅ **Keep .gitignore updated** - Don't commit secrets or build files
7. ✅ **Test before push** - Ensure code works

---

## Quick Reference

```bash
# Daily workflow
git pull                          # Get latest
git checkout -b feature/name      # New branch
# ... make changes ...
git add .                         # Stage changes
git commit -m "feat: description" # Commit
git push origin feature/name      # Push

# Check status
git status                        # What changed
git log --oneline                 # History
git diff                          # Detailed changes

# Undo
git restore file.py               # Discard changes
git reset --soft HEAD~1           # Undo commit

# Branches
git branch                        # List branches
git checkout master               # Switch branch
git merge feature/name            # Merge branch
```

---

## Need Help?

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Guides**: https://guides.github.com/
- **Conventional Commits**: https://www.conventionalcommits.org/

---

**Your repo is ready!** You already have a proper monorepo setup. Just commit your changes and push to your remote repository.
