"""
College Research Service

Business logic for college research operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .repository import ProjectRepository, PublicationRepository, PatentRepository
from .models import ResearchProject, Publication, Patent
from .schemas import ProjectCreate, ProjectUpdate, PublicationCreate, PublicationUpdate, PatentCreate, PatentUpdate


class ResearchService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.pub_repo = PublicationRepository(db)
        self.patent_repo = PatentRepository(db)
    
    # ── Project Methods ─────────────────────────────────────────
    async def create_project(self, data: ProjectCreate) -> ResearchProject:
        project = ResearchProject(**data.model_dump())
        return await self.project_repo.create(project)
    
    async def get_project(self, project_id: int) -> Optional[ResearchProject]:
        return await self.project_repo.get_by_id(project_id)
    
    async def list_projects(self, skip: int = 0, limit: int = 100) -> List[ResearchProject]:
        return await self.project_repo.list(skip, limit)
    
    async def list_projects_by_faculty(self, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ResearchProject]:
        return await self.project_repo.list_by_faculty(faculty_id, skip, limit)
    
    async def update_project(self, project_id: int, data: ProjectUpdate) -> Optional[ResearchProject]:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(project, key, value)
        return await self.project_repo.update(project)
    
    # ── Publication Methods ─────────────────────────────────────
    async def create_publication(self, data: PublicationCreate) -> Publication:
        publication = Publication(**data.model_dump())
        return await self.pub_repo.create(publication)
    
    async def get_publication(self, pub_id: int) -> Optional[Publication]:
        return await self.pub_repo.get_by_id(pub_id)
    
    async def list_publications(self, skip: int = 0, limit: int = 100) -> List[Publication]:
        return await self.pub_repo.list(skip, limit)
    
    async def list_publications_by_faculty(self, faculty_id: int, skip: int = 0, limit: int = 100) -> List[Publication]:
        return await self.pub_repo.list_by_faculty(faculty_id, skip, limit)
    
    async def update_publication(self, pub_id: int, data: PublicationUpdate) -> Optional[Publication]:
        publication = await self.pub_repo.get_by_id(pub_id)
        if not publication:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(publication, key, value)
        return await self.pub_repo.update(publication)
    
    # ── Patent Methods ─────────────────────────────────────────
    async def create_patent(self, data: PatentCreate) -> Patent:
        patent = Patent(**data.model_dump())
        return await self.patent_repo.create(patent)
    
    async def get_patent(self, patent_id: int) -> Optional[Patent]:
        return await self.patent_repo.get_by_id(patent_id)
    
    async def list_patents(self, skip: int = 0, limit: int = 100) -> List[Patent]:
        return await self.patent_repo.list(skip, limit)
    
    async def list_patents_by_faculty(self, faculty_id: int, skip: int = 0, limit: int = 100) -> List[Patent]:
        return await self.patent_repo.list_by_faculty(faculty_id, skip, limit)
    
    async def update_patent(self, patent_id: int, data: PatentUpdate) -> Optional[Patent]:
        patent = await self.patent_repo.get_by_id(patent_id)
        if not patent:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(patent, key, value)
        return await self.patent_repo.update(patent)