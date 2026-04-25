# How to Add a New Module

This guide explains how to add a new feature module to the School & College Management System.

## Overview

The system uses a **modular monolith** architecture. Each module is a self-contained package that owns all its data:
- Models (database tables)
- Schemas (Pydantic validation)
- Repository (database CRUD)
- Service (business logic)
- API (FastAPI routes)

## Step 1: Create Module Folder

Create a new folder under `modules/`:

```bash
mkdir -p modules/my_new_module/tests
touch modules/my_new_module/__init__.py
```

## Step 2: Create the 5 Core Files

### models.py — Database Schema
```python
# modules/my_new_module/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from modules.shared.base import Base
from modules.shared.base import TimestampMixin

class MyModel(Base, TimestampMixin):
    __tablename__ = "my_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    description = Column(String(500))
```

### schemas.py — Request/Response Models
```python
# modules/my_new_module/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class MyModelBase(BaseModel):
    name: str
    description: Optional[str] = None

class MyModelCreate(MyModelBase):
    pass

class MyModelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class MyModelResponse(MyModelBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

### repository.py — Database Operations
```python
# modules/my_new_module/repository.py
from sqlalchemy.orm import Session
from modules.my_new_module import models

class MyRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.MyModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, id: int):
        return self.db.query(models.MyModel).filter(models.MyModel.id == id).first()
    
    def create(self, data: models.MyModel):
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data
    
    def delete(self, id: int):
        model = self.get_by_id(id)
        if model:
            self.db.delete(model)
            self.db.commit()
        return model
```

### service.py — Business Logic
```python
# modules/my_new_module/service.py
from sqlalchemy.orm import Session
from modules.my_new_module import models, schemas, repository

class MyService:
    def __init__(self, db: Session):
        self.repo = repository.MyRepository(db)
    
    def list_models(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)
    
    def get_model(self, id: int):
        return self.repo.get_by_id(id)
    
    def create_model(self, data: schemas.MyModelCreate):
        model = models.MyModel(**data.model_dump())
        return self.repo.create(model)
```

### api.py — FastAPI Routes
```python
# modules/my_new_module/api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from modules.my_new_module import schemas, service
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.MyModelResponse])
def list_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    svc = service.MyService(db)
    return svc.list_models(skip, limit)

@router.get("/{id}", response_model=schemas.MyModelResponse)
def get_model(id: int, db: Session = Depends(get_db)):
    svc = service.MyService(db)
    model = svc.get_model(id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.post("/", response_model=schemas.MyModelResponse)
def create_model(data: schemas.MyModelCreate, db: Session = Depends(get_db)):
    svc = service.MyService(db)
    return svc.create_model(data)
```

## Step 3: Wire into app/main.py

```python
# app/main.py
from modules.my_new_module.api import router as my_router

app.include_router(
    my_router,
    prefix="/api/v1/my-module",
    tags=["My Module"]
)
```

## Step 4: Create Alembic Migration

```bash
# Generate migration
alembic revision --autogenerate -m "add_my_new_module"

# Apply migration
alembic upgrade head
```

## Step 5: Add Feature Flag (Optional)

Add to the features table to enable/disable the module:

```sql
INSERT INTO features (name, is_enabled) 
VALUES ('my_new_module', true);
```

Or use the feature guard in your API:

```python
from modules.shared.feature_guard import require_feature

@router.get("/", dependencies=[Depends(require_feature("my_new_module"))])
def list_models(...):
    ...
```

## Step 6: Write Tests

### Unit Tests
```python
# tests/unit/test_my_new_module.py
import pytest
from modules.my_new_module import service, schemas

def test_create_model():
    # Test business logic
    pass
```

### Integration Tests
```python
# tests/integration/test_my_new_module_flow.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_model():
    response = client.post("/api/v1/my-module/", json={"name": "Test"})
    assert response.status_code == 200
```

## Module Structure Summary

```
modules/
├── my_new_module/
│   ├── __init__.py          # Package marker
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── repository.py        # Database CRUD
│   ├── service.py           # Business logic
│   ├── api.py               # FastAPI routes
│   ├── constants.py         # Module constants
│   ├── exceptions.py        # Custom exceptions
│   └── tests/               # Module tests
```

## Best Practices

1. **Use the Base class** from `modules.shared.base`
2. **Add Timestamps** using `TimestampMixin`
3. **Use Pydantic** for all API inputs/outputs
4. **Keep API thin** - delegate to service layer
5. **Add feature flags** for gradual rollout
6. **Write tests** before creating PRs
7. **Use Alembic** for all database changes

## Need Help?

- See `plans/elite_plan*.md` for migration details
- Check `modules/shared/` for shared utilities
- Review existing modules in `modules/school_*/` or `modules/college_*/`
