from sqlalchemy.orm import Session
from typing import List, Optional
from models.models import FeeStructure

class FeeStructureRepository:
    @staticmethod
    def get_all(db: Session) -> List[FeeStructure]:
        return db.query(FeeStructure).order_by(FeeStructure.grade_level).all()
    
    @staticmethod
    def get_by_id(db: Session, structure_id: int) -> Optional[FeeStructure]:
        return db.query(FeeStructure).filter(FeeStructure.id == structure_id).first()
    
    @staticmethod
    def create(db: Session, data: dict) -> FeeStructure:
        structure = FeeStructure(**data)
        db.add(structure)
        db.commit()
        db.refresh(structure)
        return structure
    
    @staticmethod
    def update(db: Session, structure: FeeStructure, **kwargs) -> FeeStructure:
        for key, value in kwargs.items():
            if value is not None and hasattr(structure, key):
                setattr(structure, key, value)
        db.commit()
        db.refresh(structure)
        return structure
    
    @staticmethod
    def delete(db: Session, structure: FeeStructure):
        db.delete(structure)
        db.commit()
