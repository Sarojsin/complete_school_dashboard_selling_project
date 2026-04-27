# 🔐 ELITE PLAN 6 — Auth Module + Shared Security
## Phase: AUTHENTICATION — Extract auth system into modules/auth/
### Goal: Migrate the largest file (auth.py, 29KB) + secure all module endpoints

---

## 📌 Pre-Conditions (from Plans 1–5)
- [ ] ✅ All 20 role modules exist and run
- [ ] ✅ `modules/shared/auth.py` is confirmed working (JWT basics)
- [ ] ✅ `modules/shared/models.py` has or references the User model

---

## 🗂️ Current Auth State

```
app/api/endpoints/auth.py         ← 29119 bytes (biggest single file!)
app/services/auth_service.py      ← 2635 bytes
app/core/                         ← security, config
app/dependencies/                 ← get_current_user, role deps
modules/shared/auth.py            ← 270 bytes (stub only)
```

---

## 🏗️ Target Structure

```
modules/
└── auth/
    ├── __init__.py
    ├── models.py        ← UserRole enum, token models (if any)
    ├── schemas.py       ← LoginRequest, TokenResponse, RefreshToken, PasswordReset
    ├── repository.py    ← user lookup by email/username
    ├── service.py       ← login, logout, refresh, password reset logic
    ├── api.py           ← /api/v1/auth/* routes
    ├── dependencies.py  ← get_current_user, require_role, require_super_admin
    └── utils.py         ← password hash/verify, JWT create/decode
```

---

## ✅ STEP 1 — Create the auth Module Folder

```powershell
New-Item -ItemType Directory -Force -Path "modules\auth"
New-Item -ItemType File -Force -Path "modules\auth\__init__.py"
```

---

## ✅ STEP 2 — Build `modules/auth/utils.py` (JWT + Password)

This becomes the **single source of truth** for all security utilities:

```python
# modules/auth/utils.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from modules.shared.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {**data, "exp": expire, "type": "refresh"}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return {}
```

---

## ✅ STEP 3 — Build `modules/auth/schemas.py`

Extract from `app/api/endpoints/auth.py` (find all Pydantic models at top):

```python
# modules/auth/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN    = "super_admin"
    SCHOOL_AUTHORITY = "school_authority"
    SCHOOL_TEACHER  = "school_teacher"
    SCHOOL_STUDENT  = "school_student"
    SCHOOL_PARENT   = "school_parent"
    COLLEGE_FACULTY = "college_faculty"
    COLLEGE_STUDENT = "college_student"
    COLLEGE_HOD     = "college_hod"
    COLLEGE_DEAN    = "college_dean"
    COLLEGE_REGISTRAR = "college_registrar"

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: UserRole

class RefreshRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
```

---

## ✅ STEP 4 — Build `modules/auth/repository.py`

```python
# modules/auth/repository.py
from sqlalchemy.orm import Session
from modules.shared.base import Base
# Import User from wherever it lives in shared models
from app.models.models import User  # adjust this as models migrate

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def update_password(self, user_id: int, hashed_password: str):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.hashed_password = hashed_password
            self.db.commit()
        return user
```

---

## ✅ STEP 5 — Build `modules/auth/service.py`

Copy logic from `app/services/auth_service.py` (2635 bytes) + extract login logic from `app/api/endpoints/auth.py`:

```python
# modules/auth/service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from modules.auth.repository import AuthRepository
from modules.auth.schemas import LoginRequest, TokenResponse
from modules.auth.utils import verify_password, create_access_token, create_refresh_token

class AuthService:
    def __init__(self, db: Session):
        self.repo = AuthRepository(db)

    def login(self, data: LoginRequest) -> TokenResponse:
        user = self.repo.get_user_by_username(data.username)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Account is deactivated")

        token_data = {"sub": str(user.id), "role": user.role}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
            role=user.role
        )

    def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        from modules.auth.utils import decode_token
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user = self.repo.get_user_by_id(int(payload["sub"]))
        token_data = {"sub": str(user.id), "role": user.role}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
            role=user.role
        )

    def change_password(self, user_id: int, current_pw: str, new_pw: str):
        from modules.auth.utils import hash_password
        user = self.repo.get_user_by_id(user_id)
        if not verify_password(current_pw, user.hashed_password):
            raise HTTPException(status_code=400, detail="Current password is wrong")
        self.repo.update_password(user_id, hash_password(new_pw))
        return {"message": "Password changed successfully"}
```

---

## ✅ STEP 6 — Build `modules/auth/dependencies.py`

This is the **global permission layer** used by ALL modules:

```python
# modules/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from modules.shared.database import get_db
from modules.auth.utils import decode_token
from modules.auth.schemas import UserRole
from modules.auth.repository import AuthRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = AuthRepository(db).get_user_by_id(int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(*allowed_roles: UserRole):
    """Factory: creates a dependency that checks user role."""
    def checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return checker

# Convenience shortcuts
require_super_admin    = require_role(UserRole.SUPER_ADMIN)
require_school_staff   = require_role(UserRole.SCHOOL_AUTHORITY, UserRole.SCHOOL_TEACHER, UserRole.SUPER_ADMIN)
require_college_staff  = require_role(UserRole.COLLEGE_FACULTY, UserRole.COLLEGE_HOD, UserRole.COLLEGE_DEAN, UserRole.SUPER_ADMIN)
require_any_student    = require_role(UserRole.SCHOOL_STUDENT, UserRole.COLLEGE_STUDENT)
```

---

## ✅ STEP 7 — Build `modules/auth/api.py`

Copy routes from `app/api/endpoints/auth.py` (29KB). Key routes to migrate:

```python
# modules/auth/api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.shared.database import get_db
from modules.auth.service import AuthService
from modules.auth.schemas import LoginRequest, TokenResponse, RefreshRequest, ChangePasswordRequest
from modules.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).login(data)

@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    return AuthService(db).refresh_access_token(data.refresh_token)

@router.post("/logout")
def logout(current_user=Depends(get_current_user)):
    # Stateless JWT: client discards tokens
    return {"message": "Logged out successfully"}

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return AuthService(db).change_password(
        current_user.id, data.current_password, data.new_password
    )

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "role": current_user.role}
```

---

## ✅ STEP 8 — Update modules/shared/auth.py to Delegate

After `modules/auth/` is built, update `modules/shared/auth.py` to just re-export:

```python
# modules/shared/auth.py — now just a re-export shim
from modules.auth.dependencies import get_current_user, require_role, require_super_admin
from modules.auth.utils import verify_password, hash_password, create_access_token, decode_token

__all__ = [
    "get_current_user", "require_role", "require_super_admin",
    "verify_password", "hash_password", "create_access_token", "decode_token"
]
```

This means all existing code that does `from modules.shared.auth import get_current_user` keeps working.

---

## ✅ STEP 9 — Wire auth into app/main.py

```python
from modules.auth.api import router as auth_router
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
```

---

## ✅ STEP 10 — Add Auth Protection to ALL Module Endpoints

Every module's `api.py` should now use dependencies from `modules.auth.dependencies`:

```python
# Example in modules/school_teacher/api.py
from modules.auth.dependencies import get_current_user, require_school_staff

@router.get("/teachers/")
def list_teachers(current_user=Depends(require_school_staff), db: Session = Depends(get_db)):
    ...

@router.post("/teachers/")
def create_teacher(data: TeacherCreate, current_user=Depends(require_school_staff), db: Session = Depends(get_db)):
    ...
```

**Auth protection matrix:**

| Module | Required Role |
|--------|-------------|
| school_authority | SCHOOL_AUTHORITY, SUPER_ADMIN |
| school_teacher | SCHOOL_AUTHORITY, SCHOOL_TEACHER, SUPER_ADMIN |
| school_student | SCHOOL_STUDENT, SCHOOL_AUTHORITY, SUPER_ADMIN |
| school_parent | SCHOOL_PARENT, SCHOOL_AUTHORITY, SUPER_ADMIN |
| school_exam_section | SCHOOL_AUTHORITY, SCHOOL_TEACHER, SUPER_ADMIN |
| school_account_section | SCHOOL_AUTHORITY, SUPER_ADMIN |
| school_library | Any school role, SUPER_ADMIN |
| school_attendance | SCHOOL_TEACHER, SCHOOL_AUTHORITY, SUPER_ADMIN |
| college_* modules | Equivalent college roles + SUPER_ADMIN |
| super_admin | SUPER_ADMIN only |

---

## 📊 Phase 6 Completion Checklist

- [ ] `modules/auth/` folder created with all files
- [ ] `modules/auth/utils.py` — JWT + password utilities working
- [ ] `modules/auth/schemas.py` — UserRole enum has SUPER_ADMIN entry
- [ ] `modules/auth/dependencies.py` — `get_current_user`, `require_role` working
- [ ] `modules/auth/service.py` — login/refresh/change-password all working
- [ ] `modules/auth/api.py` — `POST /api/v1/auth/login` returns valid JWT
- [ ] `modules/shared/auth.py` — re-exports from `modules.auth`
- [ ] `POST /api/v1/auth/login` tested with real user credentials
- [ ] All module endpoints protected with appropriate role dependency
- [ ] `GET /api/v1/auth/me` returns correct user after login

---

## 🔜 Next: Plan 7 — Super Admin Module
