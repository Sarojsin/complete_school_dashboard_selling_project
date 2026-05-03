"""
API v1 Router
=============
Version 1 API with school/college route separation.

Routes:
    - /api/v1/auth/* - Authentication endpoints
    - /api/v1/school/* - School-specific endpoints
    - /api/v1/college/* - College-specific endpoints
"""
from fastapi import APIRouter

api_router = APIRouter()

# Import and include sub-routers
# Note: Importing after router definition to avoid circular imports
from backup.api.v1 import school, college

# Auth router will be included from app.api.v1.school and college
# as authentication is shared

# Include school and college routers
api_router.include_router(school.router, prefix="/school", tags=["School"])
api_router.include_router(college.router, prefix="/college", tags=["College"])

__all__ = ["api_router"]
