# Day 16 Production Implementation Plan
**Date**: 2026-05-21
**Focus**: Two-Factor Authentication (2FA) with TOTP

## Objectives
- Implement Time-based One-Time Password (TOTP) 2FA for enhanced account security
- Require 2FA for high-privilege roles: super_admin, authority, college_dean, college_registrar
- Provide backup codes for account recovery
- Generate QR codes for easy authenticator app setup
- Test complete login flow with 2FA challenge

## Tasks

### 1. Install Dependencies (Morning - 1 hour)
- [ ] `pip install pyotp qrcode[pil]`
- [ ] Pillow already installed with qrcode; verify: `pip show Pillow`

### 2. Database Schema Changes (1 hour)
**Add columns to `users` table**:
- [ ] Create Alembic migration: `alembic/versions/20260516_add_2fa_columns.py`
```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('tfa_secret', sa.String(32), nullable=True))
    op.add_column('users', sa.Column('tfa_enabled', sa.Boolean(), nullable=False, default=False, server_default='false'))
    op.add_column('users', sa.Column('tfa_backup_codes', sa.JSON(), nullable=True))  # list of hashed codes
    op.add_column('users', sa.Column('tfa_last_used', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('users', 'tfa_secret')
    op.drop_column('users', 'tfa_enabled')
    op.drop_column('users', 'tfa_backup_codes')
    op.drop_column('users', 'tfa_last_used')
```
- [ ] Apply: `alembic upgrade head`

### 3. 2FA Service Layer (2 hours)
**Create `modules/auth/services/two_factor_service.py`**:

```python
import pyotp
import qrcode
import io
import base64
from typing import Optional, List
from modules.shared.database import get_db
from modules.auth.models import User
from modules.shared.exceptions import ValidationError

class TwoFactorService:
    def __init__(self):
        self.issuer_name = "SchoolCollegeSystem"
    
    async def enable_2fa(self, db: AsyncSession, user: User) -> dict:
        """Generate 2FA secret and return QR code data URL"""
        if user.tfa_enabled:
            raise ValidationError("2FA already enabled")
        
        # Generate secret
        secret = pyotp.random_base32()
        user.tfa_secret = secret
        user.tfa_enabled = False  # will be enabled after verification
        await db.commit()
        
        # Generate QR code
        provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name=self.issuer_name
        )
        
        qr = qrcode.make(provisioning_uri)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode()
        
        # Generate backup codes (10 codes, SHA256 hashed)
        backup_codes = [secrets.token_hex(8) for _ in range(10)]
        user.tfa_backup_codes = [self._hash_code(code) for code in backup_codes]
        await db.commit()
        
        return {
            "secret": secret,  # shown once for manual entry
            "qr_code_data_url": f"data:image/png;base64,{qr_base64}",
            "backup_codes": backup_codes,  # shown once, user must save
        }
    
    async def verify_and_enable(self, db: AsyncSession, user: User, token: str, backup_code: str = None) -> bool:
        """Verify TOTP token or backup code, then enable 2FA"""
        if backup_code:
            # Verify backup code
            for hashed_code in user.tfa_backup_codes or []:
                if self._verify_backup_code(backup_code, hashed_code):
                    # Remove used backup code
                    user.tfa_backup_codes.remove(hashed_code)
                    user.tfa_enabled = True
                    await db.commit()
                    return True
            return False
        else:
            # Verify TOTP
            totp = pyotp.TOTP(user.tfa_secret)
            if totp.verify(token, valid_window=1):
                user.tfa_enabled = True
                await db.commit()
                return True
            return False
    
    async def verify_token(self, db: AsyncSession, user: User, token: str) -> bool:
        """Verify 2FA token during login (after password)"""
        if not user.tfa_enabled:
            return True  # 2FA not enabled, skip
        
        totp = pyotp.TOTP(user.tfa_secret)
        valid = totp.verify(token, valid_window=1)
        if valid:
            user.tfa_last_used = datetime.utcnow()
            await db.commit()
        return valid
    
    async def disable_2fa(self, db: AsyncSession, user: User, token: str) -> bool:
        """Disable 2FA with confirmation token"""
        totp = pyotp.TOTP(user.tfa_secret)
        if totp.verify(token, valid_window=1):
            user.tfa_enabled = False
            user.tfa_secret = None
            user.tfa_backup_codes = None
            await db.commit()
            return True
        return False
    
    def _hash_code(self, code: str) -> str:
        import hashlib
        return hashlib.sha256(code.encode()).hexdigest()
    
    def _verify_backup_code(self, code: str, hashed: str) -> bool:
        return hashlib.sha256(code.encode()).hexdigest() == hashed
    
    def is_enabled(self, user: User) -> bool:
        return user.tfa_enabled
```

### 4. Auth Endpoints with 2FA (1.5 hours)
**Update `modules/auth/router.py`**:

**New endpoints**:
```python
from modules.auth.services.two_factor_service import two_factor_service

@router.post("/2fa/enable")
async def enable_2fa(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate 2FA secret and QR code"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.AUTHORITY, 
                                   UserRole.COLLEGE_DEAN, UserRole.COLLEGE_REGISTRAR]:
        raise HTTPException(403, "2FA required for privileged roles only")
    
    result = await two_factor_service.enable_2fa(db, current_user)
    return result  # {secret, qr_code_data_url, backup_codes}

@router.post("/2fa/verify")
async def verify_and_enable_2fa(
    token: str,
    backup_code: Optional[str] = None,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify initial TOTP token and enable 2FA"""
    success = await two_factor_service.verify_and_enable(db, current_user, token, backup_code)
    if not success:
        raise ValidationError("Invalid token or backup code")
    return {"message": "2FA enabled successfully"}

@router.post("/2fa/disable")
async def disable_2fa(
    token: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Disable 2FA (requires current token)"""
    success = await two_factor_service.disable_2fa(db, current_user, token)
    if not success:
        raise ValidationError("Invalid token")
    return {"message": "2FA disabled"}

@router.get("/2fa/status")
async def get_2fa_status(current_user=Depends(get_current_user)):
    """Check if 2FA is enabled"""
    return {"enabled": current_user.tfa_enabled, "last_used": current_user.tfa_last_used}
```

**Update login endpoint** (`/auth/login`):
```python
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # 1. Authenticate user (password)
    user = await auth_service.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    
    # 2. Check if 2FA required and enabled
    if two_factor_service.is_enabled(user):
        # Return temp token requiring 2FA verification
        temp_token = create_temp_token(user)  # short-lived (5 min)
        return {
            "requires_2fa": True,
            "temp_token": temp_token,
            "message": "2FA verification required"
        }
    
    # 3. No 2FA – issue full access token
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/verify-2fa")
async def verify_2fa_login(
    temp_token: str,
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """Second step: verify 2FA token then issue final access token"""
    # Decode temp token to get user_id
    user = decode_temp_token(temp_token)
    verified = await two_factor_service.verify_token(db, user, token)
    if not verified:
        raise HTTPException(401, "Invalid 2FA token")
    
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
```

### 5. Frontend Integration Notes (30 min)
**Document for React team** (`docs/2fa_integration.md`):
- Login response now has `requires_2fa: true` and `temp_token`
- Frontend must show 2FA input field when `requires_2fa=true`
- Call `/auth/login/verify-2fa` with `temp_token` and TOTP code
- Store final `access_token` and proceed
- Settings page: enable/disable 2FA (needs QR code display)
- Backup codes: display once; user must download/print

### 6. Testing 2FA (1 hour)
**Unit tests** (`tests/auth/test_2fa.py`):
- [ ] `test_enable_2fa_creates_secret_and_qr()`
- [ ] `test_enable_2fa_duplicate_raises_error()`
- [ ] `test_verify_token_correct()`
- [ ] `test_verify_token_incorrect()`
- [ ] `test_verify_backup_code()`
- [ ] `test_disable_2fa_requires_token()`

**Integration tests**:
- [ ] `test_login_flow_with_2fa()`:
  1. POST `/auth/login` (correct password) → `requires_2fa=True`
  2. POST `/auth/login/verify-2fa` with valid token → access_token returned
- [ ] `test_login_with_backup_code()`
- [ ] `test_access_denied_if_2fa_required_but_not_enabled()`: super_admin without 2FA can't use protected endpoint? (optional enforce)

### 7. Role Enforcement (30 min)
**Middleware or dependency** to enforce 2FA for privileged roles:
```python
async def require_2fa_if_privileged(current_user=Depends(get_current_user)):
    privileged_roles = [UserRole.SUPER_ADMIN, UserRole.AUTHORITY, 
                        UserRole.COLLEGE_DEAN, UserRole.COLLEGE_REGISTRAR]
    if current_user.role in privileged_roles and not current_user.tfa_enabled:
        raise HTTPException(403, "2FA required for this role. Please enable 2FA in settings.")
    return current_user
```
- [ ] Apply `require_2fa_if_privileged` on all dean/registrar/super_admin endpoints

### 8. Documentation & Commit (30 min)
- [ ] `docs/2fa_setup.md`: How to enable, backup codes, recovery flow
- [ ] Update `README.md`: 2FA required for privileged roles
- [ ] Update `SECURITY.md`: 2FA implementation details
- [ ] Commit: "feat(auth): Add TOTP-based 2FA with backup codes, QR code, enforce for privileged roles"

## Deliverables
- ✅ `pyotp` + `qrcode` in requirements.txt
- ✅ Alembic migration: `tfa_secret`, `tfa_enabled`, `tfa_backup_codes`, `tfa_last_used`
- ✅ `TwoFactorService` implementation
- ✅ Endpoints: `/auth/2fa/enable`, `/verify`, `/disable`, `/status`
- ✅ Updated login flow (`requires_2fa` + `/verify-2fa`)
- ✅ 2FA enforcement dependency on privileged endpoints
- ✅ Tests: unit + integration (2FA login complete flow)
- ✅ Frontend integration guide

## Success Criteria
- Super admin can enable 2FA, receive QR code and backup codes
- Login requires TOTP after password if 2FA enabled
- Backup code works once; invalidated after use
- Disabling 2FA requires current token (prevents lockout without recovery)
- All privileged endpoints check `tfa_enabled`; return 403 if not enabled

## Notes
- Backup codes should be one-time use; remove from DB after consumption
- TOTP window: 30 seconds; allow ±1 step for clock skew (`valid_window=1`)
- Store `tfa_last_used` to detect suspicious logins from new devices
- Consider adding WebAuthn/FIDO2 later for passwordless

## Next: Day 17
UUID migration: Convert integer primary keys to UUIDs for public-facing resources to prevent ID enumeration. Requires careful data migration and frontend updates.
