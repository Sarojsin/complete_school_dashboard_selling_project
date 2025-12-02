# School Management System

A comprehensive FastAPI-based school management system with role-based access control for students, teachers, and administrators.

## Features

- **Student Portal**: View courses, assignments, grades, attendance, fees, notices, timetable, notes, and videos
- **Teacher Portal**: Manage students, courses, assignments, attendance, grades, and tests
- **Admin Portal**: Oversee all students, teachers, courses, fees, notices, analytics, and reports
- **Authentication**: JWT-based authentication with role-based access control
- **Real-time Chat**: WebSocket-based messaging system
- **Testing System**: Create and manage online tests with automatic grading

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update the database credentials:

```bash
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/school_db
SECRET_KEY=your-secret-key-change-this-in-production
```

### 3. Setup Database

```bash
python setup_database.py
```

This creates default users:
- **Admin**: username=`admin`, password=`admin123`
- **Teacher**: username=`teacher`, password=`teacher123`
- **Student**: username=`student`, password=`student123`

### 4. Run the Application

```bash
python run.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --port 8000
```

The application will be available at: http://localhost:8000

## API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Project Structure

```
claud/
├── routes/          # API route handlers
├── models/          # Database models
├── repositories/    # Data access layer
├── services/        # Business logic
├── templates/       # HTML templates
├── static/          # Static files (CSS, JS, images)
├── config/          # Configuration files
├── database/        # Database connection
├── dependencies.py  # Authentication dependencies
├── main.py          # Application entry point
└── run.py           # Server runner
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/signup` - Register new user

### Student Endpoints
- `GET /api/students/dashboard` - Student dashboard
- `GET /api/students/courses` - Enrolled courses
- `GET /api/students/assignments` - Assignments
- `GET /api/students/grades` - Grades
- `GET /api/students/attendance` - Attendance records
- `GET /api/students/fees` - Fee records
- `GET /api/students/notices` - Notices
- `GET /api/students/timetable` - Class schedule
- `GET /api/students/notes` - Course notes
- `GET /api/students/videos` - Course videos

### Teacher Endpoints
- `GET /api/teachers/dashboard` - Teacher dashboard
- `GET /api/teachers/students` - Students list
- `GET /api/teachers/courses` - Teaching courses
- `GET /api/teachers/assignments` - Created assignments
- `GET /api/teachers/attendance` - Attendance records
- `GET /api/teachers/grades` - Grades

### Authority Endpoints
- `GET /api/authority/dashboard` - Admin dashboard
- `GET /api/authority/students` - All students
- `GET /api/authority/teachers` - All teachers
- `GET /api/authority/courses` - All courses
- `GET /api/authority/fees` - All fee records
- `GET /api/authority/notices` - All notices
- `GET /api/authority/analytics` - System analytics
- `GET /api/authority/reports` - System reports

## Testing

Run the endpoint verification script:

```bash
python verify_endpoints.py
```

## Documentation

- [API Testing Guide](api_testing.md) - Detailed API testing examples
- [Deployment Guide](deployment.md) - Production deployment instructions
- [Quick Start Guide](quickstart.md) - Getting started guide
- [Feature Checklist](finally_check_list.md) - Complete feature list

## License

MIT License
