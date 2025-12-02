# Quick Start Guide

Get the School Management System running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Git

## Installation Methods

### Method 1: Docker (Easiest - Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd school_dashboard_project

# 2. Start the application
make docker-up

# 3. Access the application
# Open your browser and go to: http://localhost:8000
```

That's it! The application is now running with a PostgreSQL database.

**Default Login Credentials:**
- Admin: `admin` / `admin123`
- Teacher: `teacher` / `teacher123`
- Student: `student` / `student123`

### Method 2: Local Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd school_dashboard_project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
make install
# Or: pip install -r requirements.txt

# 4. Setup PostgreSQL database
sudo -u postgres psql
CREATE DATABASE school_db;
CREATE USER school_user WITH PASSWORD 'school_password';
GRANT ALL PRIVILEGES ON DATABASE school_db TO school_user;
\q

# 5. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 6. Setup database and create default users
make setup
# Or: python setup_database.py

# 7. Run the application
make dev
# Or: python run.py --reload

# 8. Access the application
# Open your browser and go to: http://localhost:8000
```

## First Steps After Installation

### 1. Login to the System

Visit http://localhost:8000 and click "Get Started" or go directly to http://localhost:8000/login

### 2. Explore as Different Users

#### As Student (student/student123):
- View dashboard with courses, assignments, and grades
- Take available tests
- Check attendance records
- View pending fees
- Chat with teachers

#### As Teacher (teacher/teacher123):
- View teaching dashboard
- Create and manage tests
- Grade assignments
- Take attendance
- Upload course materials
- Chat with students

#### As Authority (admin/admin123):
- Manage students and teachers
- Configure courses
- View analytics
- Manage fee structures
- Create system-wide notices

### 3. Create Your First Test

1. Login as teacher
2. Go to Tests → Create Test
3. Fill in test details (title, duration, dates)
4. Add questions with answers
5. Save and publish

### 4. Take a Test as Student

1. Login as student
2. Go to Tests → Available Tests
3. Click "Start Test"
4. Answer questions
5. Submit before time expires
6. View results after grading

### 5. Upload Course Materials

1. Login as teacher
2. Go to Courses → Select Course
3. Upload Notes or Videos
4. Students can now access the materials

## Common Commands

```bash
# Start development server
make dev

# Run tests
make test

# Clean temporary files
make clean

# Create database backup
make backup

# View Docker logs
make docker-logs

# Stop Docker containers
make docker-down

# Rebuild Docker containers
make docker-rebuild
```

## API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
school_dashboard_project/
├── app/
│   ├── main.py              # Application entry point
│   ├── models/              # Database models
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── repositories/        # Data access layer
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── tests/                   # Test files
├── requirements.txt         # Dependencies
├── setup_database.py        # Database initialization
├── run.py                   # Application runner
└── Makefile                 # Common commands
```

## Key Features

### 🎓 For Students
- View courses and schedules
- Submit assignments
- Take online tests with timer
- Check grades and attendance
- Access course materials
- Real-time chat with teachers
- View fee status

### 👨‍🏫 For Teachers
- Manage courses
- Create and grade tests
- Upload notes and videos
- Take attendance
- Input grades
- Chat with students
- View student performance

### 🏢 For Authority
- Manage users (students/teachers)
- Configure courses
- Fee management
- System analytics
- Create notices
- Generate reports

### 🚀 Technical Features
- JWT Authentication
- Role-based access control
- WebSocket real-time chat
- Automatic test grading
- File upload support
- Background job scheduling
- Responsive design

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python run.py --port 8080
```

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify database credentials in .env
cat .env

# Test database connection
psql -U school_user -d school_db -h localhost
```

### Permission Denied Errors
```bash
# Fix upload directory permissions
chmod 755 app/static/uploads
```

### Docker Issues
```bash
# View logs
docker-compose logs -f

# Restart containers
docker-compose restart

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Next Steps

1. **Customize**: Update branding, colors, and logos
2. **Add Data**: Create courses, enroll students
3. **Configure**: Set up fee structures, schedules
4. **Test**: Create and take tests
5. **Deploy**: Follow DEPLOYMENT.md for production

## Getting Help

- **Documentation**: Check README.md and IMPLEMENTATION_GUIDE.md
- **API Docs**: http://localhost:8000/docs
- **Issues**: Create an issue on GitHub
- **Logs**: Check application logs for errors

## Security Notes

⚠️ **Important for Production:**

1. Change default passwords immediately
2. Generate a secure SECRET_KEY
3. Set DEBUG=False
4. Configure ALLOWED_ORIGINS properly
5. Use HTTPS
6. Set up firewall rules
7. Enable rate limiting
8. Regular database backups

## Development Workflow

```bash
# 1. Make changes to code
vim app/routes/students.py

# 2. Run in development mode (auto-reload)
make dev

# 3. Test changes
make test

# 4. Format code
make format

# 5. Commit changes
git add .
git commit -m "Add feature"
git push
```

## Performance Tips

- Use connection pooling for database
- Enable caching for static files
- Use CDN for media files
- Optimize database queries
- Monitor application performance
- Scale horizontally with multiple workers

## Updating the Application

```bash
# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt

# Run migrations
make migrate

# Restart application
make dev  # or restart production server
```

## Support

For additional help:
- Read the full README.md
- Check IMPLEMENTATION_GUIDE.md for detailed patterns
- Review DEPLOYMENT.md for production setup
- Visit the API documentation at /docs

---

**Congratulations!** You now have a fully functional school management system running locally. Start exploring and customizing it to your needs!