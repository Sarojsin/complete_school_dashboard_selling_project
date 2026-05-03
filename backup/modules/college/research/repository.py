"""
Research Repository

Data access layer for research projects and publications.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from backup.models.college.research import ResearchProject, Publication


class ResearchRepository:
    """Repository for research data access"""

    @staticmethod
    async def get_project(db: AsyncSession, project_id: int) -> Optional[ResearchProject]:
        """Get a research project by ID"""
        result = await db.execute(
            select(ResearchProject).where(ResearchProject.id == project_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_projects(
        db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> tuple[List[ResearchProject], int]:
        """List all research projects with pagination"""
        # Get total count
        count_result = await db.execute(select(ResearchProject))
        total = len(count_result.scalars().all())

        # Get paginated results
        result = await db.execute(
            select(ResearchProject)
            .offset(skip)
            .limit(limit)
            .order_by(ResearchProject.created_at.desc())
        )
        projects = result.scalars().all()
        return list(projects), total

    @staticmethod
    async def get_publication(db: AsyncSession, publication_id: int) -> Optional[Publication]:
        """Get a publication by ID"""
        result = await db.execute(
            select(Publication).where(Publication.id == publication_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_publications(
        db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> tuple[List[Publication], int]:
        """List all publications with pagination"""
        # Get total count
        count_result = await db.execute(select(Publication))
        total = len(count_result.scalars().all())

        # Get paginated results
        result = await db.execute(
            select(Publication)
            .offset(skip)
            .limit(limit)
            .order_by(Publication.publication_date.desc())
        )
        publications = result.scalars().all()
        return list(publications), total
