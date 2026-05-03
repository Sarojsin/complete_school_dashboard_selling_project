"""
College Research Repository

Async CRUD operations for college research management.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from .models import ResearchProject, ResearchPublication, ResearchPatent


# ── Project Repository ─────────────────────────────────────────
class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, project_id: int) -> Optional[ResearchProject]:
        result = await self.db.execute(select(ResearchProject).filter(ResearchProject.id == project_id))
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[ResearchProject]:
        result = await self.db.execute(select(ResearchProject).offset(skip).limit(limit))
        return list(result.scalars().all())
    
    async def list_by_faculty(self, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ResearchProject]:
        result = await self.db.execute(
            select(ResearchProject).filter(ResearchProject.principal_investigator_id == faculty_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, project: ResearchProject) -> ResearchProject:
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project
    
    async def update(self, project: ResearchProject) -> ResearchProject:
        await self.db.commit()
        await self.db.refresh(project)
        return project


# ── Publication Repository ──────────────────────────────────────
class PublicationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, pub_id: int) -> Optional[ResearchPublication]:
        result = await self.db.execute(select(ResearchPublication).filter(ResearchPublication.id == pub_id))
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[ResearchPublication]:
        result = await self.db.execute(select(ResearchPublication).offset(skip).limit(limit))
        return list(result.scalars().all())
    
    async def list_by_faculty(self, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ResearchPublication]:
        result = await self.db.execute(
            select(ResearchPublication).filter(ResearchPublication.faculty_id == faculty_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, publication: ResearchPublication) -> ResearchPublication:
        self.db.add(publication)
        await self.db.commit()
        await self.db.refresh(publication)
        return publication
    
    async def update(self, publication: ResearchPublication) -> ResearchPublication:
        await self.db.commit()
        await self.db.refresh(publication)
        return publication


# ── Patent Repository ───────────────────────────────────────────
class PatentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, patent_id: int) -> Optional[ResearchPatent]:
        result = await self.db.execute(select(ResearchPatent).filter(ResearchPatent.id == patent_id))
        return result.scalars().first()
    
    async def list(self, skip: int = 0, limit: int = 100) -> List[ResearchPatent]:
        result = await self.db.execute(select(ResearchPatent).offset(skip).limit(limit))
        return list(result.scalars().all())
    
    async def list_by_faculty(self, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ResearchPatent]:
        result = await self.db.execute(
            select(ResearchPatent).filter(ResearchPatent.faculty_id == faculty_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, patent: ResearchPatent) -> ResearchPatent:
        self.db.add(patent)
        await self.db.commit()
        await self.db.refresh(patent)
        return patent
    
    async def update(self, patent: ResearchPatent) -> ResearchPatent:
        await self.db.commit()
        await self.db.refresh(patent)
        return patent