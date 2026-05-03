"""
Research Service

Business logic for research projects and publications.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from backup.modules.college.research.schemas import (
    ResearchProjectResponse,
    ResearchProjectListResponse,
    PublicationResponse,
    PublicationListResponse,
)
from backup.modules.college.research.repository import ResearchRepository


class ResearchService:
    """Service for research business logic"""

    async def list_projects(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> ResearchProjectListResponse:
        """List all research projects"""
        projects, total = await ResearchRepository.list_projects(db, skip, limit)
        return ResearchProjectListResponse(
            projects=[ResearchProjectResponse.model_validate(p) for p in projects],
            total=total
        )

    async def get_project(
        self, db: AsyncSession, project_id: int
    ) -> Optional[ResearchProjectResponse]:
        """Get a research project by ID"""
        project = await ResearchRepository.get_project(db, project_id)
        if project:
            return ResearchProjectResponse.model_validate(project)
        return None

    async def list_publications(
        self, db: AsyncSession, skip: int = 0, limit: int = 20
    ) -> PublicationListResponse:
        """List all publications"""
        publications, total = await ResearchRepository.list_publications(db, skip, limit)
        return PublicationListResponse(
            publications=[PublicationResponse.model_validate(p) for p in publications],
            total=total
        )

    async def get_publication(
        self, db: AsyncSession, publication_id: int
    ) -> Optional[PublicationResponse]:
        """Get a publication by ID"""
        publication = await ResearchRepository.get_publication(db, publication_id)
        if publication:
            return PublicationResponse.model_validate(publication)
        return None
