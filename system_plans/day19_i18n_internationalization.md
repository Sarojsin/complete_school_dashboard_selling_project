# Day 19 Production Implementation Plan
**Date**: 2026-05-24
**Focus**: Internationalization (i18n) - Multi-Language Support

## Objectives
- Implement backend translation system for error messages, email templates, and API responses
- Support at least 2 languages: English (default) + Hindi (for India)
- Extract translatable strings from codebase into message catalogs
- Integrate with FastAPI for automatic Accept-Language header handling
- Coordinate with frontend i18n to ensure message key consistency
- Create translation management workflow for future additions

## Tasks

### 1. Install i18n Library (Morning - 1 hour)
**Options**:
- `fastapi-i18n` – FastAPI-specific, middleware for language detection
- `python-i18n` – lightweight, yaml-based
- `babel` – mature, gettext-compatible

**Choice**: Use `fastapi-i18n` for simplicity with FastAPI:
```bash
pip install fastapi-i18n
```

### 2. Configure i18n Setup (1 hour)
**Create `modules/shared/i18n.py`**:
```python
from fastapi_i18n import I18nMiddleware, I18nLocaleMiddleware
from fastapi_i18n.l10n import L18n
import os

# Supported languages
LANGUAGES = {
    "en": "English",
    "hi": "Hindi",  # Hindi for India
    # future: "ta": "Tamil", "te": "Telugu", "mr": "Marathi"
}

# Initialize L18n
l18n = L18n(
    locales=list(LANGUAGES.keys()),
    default_locale="en",
    translation_dir="modules/shared/translations",  # YAML files here
)

# FastAPI middleware - detects language from header, query param, or cookie
middleware = I18nMiddleware(l18n, locale_detector=None)  # uses Accept-Language by default

# Convenience function for non-FastAPI contexts (Celery tasks, emails)
def gettext(key: str, locale: str = "en", **variables) -> str:
    """Get translated string for key"""
    return l18n.gettext(key, locale=locale, **variables)
```

**Directory structure**:
```
modules/shared/translations/
├── en.yml
├── hi.yml
```

**Example `en.yml`**:
```yaml
en:
  errors:
    not_found: "Resource not found"
    unauthorized: "Unauthorized access"
    forbidden: "You don't have permission"
    validation_error: "Validation failed"
    invalid_email: "Invalid email address"
    weak_password: "Password must be at least 8 characters"
  auth:
    login_success: "Welcome, {name}!"
    login_failed: "Invalid email or password"
    signup_success: "Account created. Please check your email to verify."
    two_factor_required: "2FA verification required"
  college:
    student_created: "Student {roll_number} added successfully"
    enrollment_success: "Student enrolled in {program} for {semester}"
    fee_payment_received: "Payment of ₹{amount} received. Receipt: {receipt_no}"
```

**Example `hi.yml`** (transliterated or translated):
```yaml
hi:
  errors:
    not_found: "संसाधन नहीं मिला"
    unauthorized: "अनधिकृत पहुंच"
    forbidden: "आपके पास अनुमति नहीं है"
    validation_error: "सत्यापन में त्रुटि"
    invalid_email: "अमान्य ईमेल पता"
    weak_password: "पासवर्ड कम से कम 8 अक्षरों का होना चाहिए"
  auth:
    login_success: "स्वागत है, {name}!"
    login_failed: "ईमेल या पासवर्ड गलत"
    signup_success: "खाता बनाया गया। कृपया verify करने के लिए अपना ईमेल जांचें।"
    two_factor_required: "2FA सत्यापन आवश्यक"
  college:
    student_created: "छात्र {roll_number} सफलतापूर्वक जोड़ा गया"
    enrollment_success: "{program} में {semester} के लिए नामांकन किया गया"
    fee_payment_received: "₹{amount} की राशि प्राप्त हुई। रसीद: {receipt_no}"
```

### 3. Integrate Middleware into FastAPI (30 min)
**Update `app/main.py`**:
```python
from modules.shared.i18n import middleware as i18n_middleware

app = FastAPI(...)
app.add_middleware(i18n_middleware)
```

**Test**: Set `Accept-Language: hi` header; responses use Hindi

### 4. Update Existing Code to Use Translations (2 hours)
**Replace hardcoded strings**:

**Exceptions**:
- In `modules/shared/exceptions.py`:
  ```python
  class NotFoundError(HTTPException):
      def __init__(self, detail: str = None):
          from modules.shared.i18n import gettext
          super().__init__(
              status_code=404,
              detail=detail or gettext("errors.not_found")
          )
  ```
- Similarly for `ForbiddenError`, `ValidationError`

**Email templates**:
- In `modules/shared/email.py`: template strings become translation keys
  ```python
  body = gettext("emails.welcome", locale=user.locale, name=user.name)
  ```
- Load email templates from YAML

**Router responses**:
- In routers: `detail="Successfully created"` → `detail=gettext("college.student_created", roll_number=roll)`

**Quick sweep**:
- [ ] `grep -r "\".*\"" modules/college/college_exam_section/router.py` – find all string literals in `detail=` or `description=` fields
- [ ] Replace with translation calls

### 5. User Language Preference (1 hour)
**Add column to `users` table**:
- [ ] Migration: `alembic/versions/20260524_add_user_locale.py`:
  ```python
  op.add_column('users', sa.Column('locale', sa.String(5), nullable=True, server_default='en'))
  op.alter_column('users', 'locale', server_default=None)
  ```
- [ ] `User` model add `locale: str = Column(String(5), default="en")`

**Endpoint to update locale**:
```python
@router.patch("/me/locale")
async def set_locale(locale: str = Body(..., embed=True), current_user=Depends(get_current_user), db=AsyncSession=Depends(get_db)):
    if locale not in LANGUAGES:
        raise ValidationError(f"Unsupported locale: {locale}")
    current_user.locale = locale
    await db.commit()
    return {"message": "Locale updated", "locale": locale}
```

**Locale in responses**: Include `X-Current-Locale` header or `{"locale": "en"}` in JSON body

### 6. Frontend Coordination (30 min)
**Document API**: Language handling:
- Frontend should send `Accept-Language: hi` header on all requests OR
- Frontend sets locale via `PATCH /auth/me/locale`; backend returns translated messages using user's stored locale
- Frontend displays `detail` field from API; no need to translate again

**Message keys**: Provide `en.yml` to frontend team so they can align React i18next keys

### 7. Testing i18n (1 hour)
**Unit tests** (`tests/test_i18n.py`):
- [ ] `test_translation_english_default()`: default locale returns English
- [ ] `test_translation_hindi()`: with `Accept-Language: hi` returns Hindi
- [ ] `test_gettext_formatting()`: `gettext("welcome", name="John")` substitutes `{name}`
- [ ] `test_unsupported_locale_fallback()`: `fr` falls back to `en`
- [ ] `test_locale_saved_in_db()`: PATCH updates user.locale

**Integration tests**:
- [ ] `test_login_response_translated()`: login error message in Hindi when `Accept-Language: hi`

### 8. Documentation & Commit (30 min)
- [ ] `docs/i18n.md`: How to add new language, translation workflow, message keys
- [ ] Update `README.md`: multi-language support note
- [ ] Add `translations/` directory to version control
- [ ] Commit: "feat(i18n): Add internationalization support with English + Hindi translations"

## Deliverables
- ✅ `fastapi-i18n` installed
- ✅ `modules/shared/i18n.py` + `modules/shared/translations/en.yml`, `hi.yml`
- ✅ Middleware added to `app/main.py`
- ✅ Exceptions use translated messages
- ✅ Email templates use translation keys
- ✅ User can set locale via PATCH endpoint
- ✅ Tests for translation behavior
- ✅ Documentation for adding new languages

## Success Criteria
- `curl -H "Accept-Language: hi" http://localhost:8000/api/v1/...` returns Hindi error messages
- User sets locale: `PATCH /auth/me/locale` with `{"locale":"hi"}`; subsequent responses in Hindi
- Translation fallback works: unsupported locale → English
- All existing error messages now translatable (no hardcoded English strings left)

## Notes
- Keep translation keys nested (errors.not_found) for organization
- Use `{variable}` placeholders in translation strings for formatting
- For large catalogs, consider splitting YAML files by module (errors.yml, auth.yml, college.yml)
- Consider using a translation management platform (e.g., Crowdin) later

## Next: Day 20
Week 3 review: audit completed work, update production scorecard (target 78%), plan Week 4 (final compliance: GDPR export/delete, audit logging complete, user docs, final testing & go-live prep).
