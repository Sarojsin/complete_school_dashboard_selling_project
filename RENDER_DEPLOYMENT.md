# Render Deployment Guide

## Prerequisites
- GitHub account with your repository
- Render account (sign up at https://render.com)

## Deployment Steps

### 1. Repository Setup
✅ Your code is already on GitHub: https://github.com/Sarojsin/complete_school_dashboard_selling_project.git

### 2. Database Setup on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `school-db`
   - **Database**: `school_management`
   - **User**: `school_user`
   - **Region**: Oregon (US West)
   - **Plan**: Free
4. Click "Create Database"
5. **Important**: Save the "Internal Database URL" - you'll need it

### 3. Web Service Setup

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `complete_school_dashboard_selling_project`
4. Configure:
   - **Name**: `school-management-system`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### 4. Environment Variables

Add the following environment variables in Render dashboard:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | (from Step 2) | PostgreSQL connection string |
| `SECRET_KEY` | (generate random) | Use: `openssl rand -hex 32` |
| `AUTHORITY_SECRET_KEY` | (generate random) | Use: `openssl rand -hex 32` |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiry time |
| `DEBUG` | `false` | Production mode |
| `ALLOWED_ORIGINS` | `*` | CORS origins (customize for production) |

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your application
3. Wait for deployment to complete (~5-10 minutes)
4. Your app will be live at: `https://school-management-system.onrender.com`

### 6. Post-Deployment

#### Database Migration
If deployment succeeds but database tables are missing:

1. Go to your web service dashboard
2. Click "Shell" tab
3. Run:
```bash
python -c "from database.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

#### Create Admin User
```bash
python -c "from repositories.user_repository import UserRepository; from database.database import SessionLocal; from models.models import UserRole; db = SessionLocal(); UserRepository.create(db, 'admin@school.com', 'admin', 'admin123', 'Administrator', UserRole.AUTHORITY); db.commit()"
```

## Alternative: Blueprint Deployment

If you prefer using `render.yaml`:

1. Push the included `render.yaml` to your repository
2. In Render dashboard, click "New +" → "Blueprint"
3. Select your repository
4. Render will auto-configure from `render.yaml`

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Verify `requirements.txt` is correct
- Ensure Python version compatibility (3.11)

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Check database is in same region as web service
- Ensure database is running

### Application Won't Start
- Check start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Verify all environment variables are set
- Check application logs

### Static Files Not Loading
- Ensure `/static` route is configured in `main.py`
- Verify static files directory exists

## Configuration Files Created

- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Blueprint configuration
- ✅ `build.sh` - Build script
- ✅ `RENDER_DEPLOYMENT.md` - This guide

## Next Steps After Deployment

1. Test all routes and functionality
2. Update `ALLOWED_ORIGINS` to your domain
3. Set up custom domain (if needed)
4. Configure production database backups
5. Set up monitoring and alerts
6. Implement SSL (automatic with Render)

## Important Notes

- **Free Tier**: App sleeps after 15 mins of inactivity
- **Build Time**: ~5-10 minutes for first deployment
- **Database**: Free tier has 1GB storage limit
- **Performance**: Consider upgrading to paid tier for production

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Project Issues: https://github.com/Sarojsin/complete_school_dashboard_selling_project/issues
