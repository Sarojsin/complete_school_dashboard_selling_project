"""
Placement API Routes

API routes for placement management.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.database import get_async_db
from modules.shared.auth import get_current_user
from modules.shared.models import User

router = APIRouter(prefix="/placements", tags=["College Placements"])


@router.get("/")
async def list_placements(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """List all placements"""
    return {"message": "Placements endpoint - use app/api/v1/college/placements.py for full implementation"}
