# 🏫 School & College Management System — Setup & Run Guide

## ⚡ Quickest Way to Start — `model_run.py`

`model_run.py` is a single launcher script connected directly to `app/main.py`.  
After completing the one-time setup below, just run:

```bash
# Dev mode (auto-reload ON, opens browser automatically)
python model_run.py

# Also start the React frontend in a new window
python model_run.py --with-frontend

# Production mode (reload OFF, multiple workers)
python model_run.py --prod --workers 4

# Custom host / port
python model_run.py --host 0.0.0.0 --port 9000
```

**What it does:**
- Starts the FastAPI backend via `app.main:app`
- Auto-opens `http://localhost:8000/docs` in your browser
- Optionally launches `npm run dev` for the frontend (`--with-frontend`)
- Gracefully shuts down everything with `Ctrl+C`

---

## 📋 Prerequisites

Make sure you have the following installed before starting:

| Tool | Version | Check Command |
|------|---------|---------------|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Git | Any | `git --version` |

---

## 🗂️ Project Structure

```
claud_sc/
├── app/              # FastAPI application entry point
├── modules/          # Backend feature modules (school & college)
│   ├── auth/         # Authentication (login, signup, JWT)
│   ├── school/       # All school modules (student, teacher, authority…)
│   └── college/      # All college modules (courses, enrollments…)
├── frontend/         # React + Vite frontend
├── alembic/          # Database migration scripts
├── .env              # Environment variables (must be created)
├── requirements.txt  # Python dependencies
└── school.db         # SQLite database (auto-created)
```

---

## ⚙️ Backend Setup (FastAPI)

### Step 1 — Clone & Enter the Project

```bash
git clone <your-repo-url>
cd claud_sc
```

### Step 2 — Create a Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

Copy the example file and edit it:

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Then open `.env` and set at minimum:

```env
# Database (SQLite for local dev — no extra setup needed)
DATABASE_URL=sqlite:///./school.db

# Security — generate a strong key:
# python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-secret-key-here

# App settings
DEBUG=True
APP_NAME=School Management System
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> [!NOTE]
> For **PostgreSQL** instead of SQLite, set:
> ```env
> DATABASE_URL=postgresql://user:password@localhost:5432/school_db
> ```
> You'll also need PostgreSQL running locally.

### Step 5 — Run Database Migrations

```bash
# Create all tables (uses alembic)
alembic upgrade head
```

> [!TIP]
> If you get migration errors, you can reset by deleting `school.db` and running again:
> ```bash
> del school.db        # Windows
> alembic upgrade head
> ```

### Step 6 — Start the Backend Server

```bash
# From the project root (claud_sc/)
.venv\Scripts\python -m uvicorn app.main:app --port 8000 --reload
```

The API will be available at:
- **API Base:** `http://localhost:8000/api/v1/`
- **Swagger Docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## 🌐 Frontend Setup (React + Vite)

### Step 1 — Navigate to Frontend

```bash
cd frontend
```

### Step 2 — Install Node Dependencies

```bash
npm install
```

### Step 3 — Start the Dev Server

```bash
npm run dev
```

The app will open at: **`http://localhost:5173`**

> [!IMPORTANT]
> The frontend proxies all `/api` requests to the backend at port `8000`. **Both servers must be running at the same time.**

---

## 🚀 Running Both Servers (Recommended)

Open **two separate terminals**:

**Terminal 1 — Backend:**
```bash
cd claud_sc
.venv\Scripts\activate
.venv\Scripts\python -m uvicorn app.main:app --port 8000 --reload
```

**Terminal 2 — Frontend:**
```bash
cd claud_sc\frontend
npm run dev
```

Then open your browser at `http://localhost:5173`.

---

## 👤 User Roles & Signup

The system supports the following roles. Register via the UI at `/register-choice`:

| Role | Description |
|------|-------------|
| `student` | Student portal (grades, assignments, timetable) |
| `teacher` | Teacher portal (courses, create assignments/tests) |
| `authority` | Admin authority (manage students, teachers, fees) |
| `parent` | Parent portal (view child's progress) |
| `hod` | Head of Department |
| `account_section` | Fee and expense management |
| `exam_section` | Exam scheduling and results |

> [!IMPORTANT]
> **Password must be at least 6 characters** when registering.

### First-Time Authority Signup

Authority and Admin roles require a secret key set in `.env`:
```env
AUTHORITY_SECRET_KEY=your-authority-key
ADMIN_SECRET_KEY=your-admin-key
```

---

## 🗃️ Database Options

### Option A — SQLite (Default, No Setup Needed)

```env
DATABASE_URL=sqlite:///./school.db
```

Best for development and testing.

### Option B — PostgreSQL (Recommended for Production)

1. Install PostgreSQL and create a database:
```sql
CREATE DATABASE school_db;
```

2. Update `.env`:
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/school_db
```

3. Run migrations:
```bash
alembic upgrade head
```

---

## 🐳 Docker (Optional)

If Docker is installed, you can run the full stack:

```bash
docker-compose up --build
```

This starts both the backend and database together.

---

## 🧪 Running Tests

```bash
# From project root with venv active
pytest tests/ -v
```

---

## 🔧 Troubleshooting

### Backend won't start
- Make sure `.venv` is activated: `.venv\Scripts\activate`
- Check `.env` has `DATABASE_URL` and `SECRET_KEY` set
- Try: `pip install -r requirements.txt` again

### Frontend shows blank page
- Ensure **both** backend (port 8000) and frontend (port 5173) are running
- Clear browser cache or try incognito mode

### Login returns 422 error
- Ensure username exists (sign up first)
- Password must be **≥ 6 characters**

### `ModuleNotFoundError` on startup
- Activate virtualenv: `.venv\Scripts\activate`
- Run: `pip install -r requirements.txt`

### Database table errors
- Run: `alembic upgrade head`
- Or delete `school.db` and rerun migrations

---

## 📌 Quick Reference

```
Backend URL   → http://localhost:8000
Frontend URL  → http://localhost:5173
Swagger Docs  → http://localhost:8000/docs
Login Page    → http://localhost:5173/login
Register      → http://localhost:5173/register-choice
```
