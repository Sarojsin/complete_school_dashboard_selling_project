# Missing Endpoints Migration Plan - Priority 2: Media & Library Modules

**Plan 2: Media & Learning Resources**

This plan covers Notes, Videos, and enhanced Library modules.

## Module Overview

| Module | Missing Endpoints | Priority |
|--------|------------------|----------|
| Notes | 8 endpoints | MEDIUM |
| Videos | 8 endpoints | MEDIUM |
| Library (Enhanced) | 7 endpoints | MEDIUM |

---

## 1. Notes Module

**Target Location:** `modules/school/notes/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| POST | `/api/notes/upload` | Upload note | backup/api/endpoints/notes.py |
| GET | `/api/notes/teacher/my-notes` | Get my notes | backup/api/endpoints/notes.py |
| DELETE | `/api/notes/{note_id}` | Delete note | backup/api/endpoints/notes.py |
| GET | `/api/notes/course/{course_id}` | Get course notes | backup/api/endpoints/notes.py |
| GET | `/api/notes/{note_id}` | Get note | backup/api/endpoints/notes.py |
| GET | `/api/notes/{note_id}/download` | Download note | backup/api/endpoints/notes.py |
| GET | `/api/notes/search/{query}` | Search notes | backup/api/endpoints/notes.py |
| GET | `/api/notes/recent/all` | Get recent notes | backup/api/endpoints/notes.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/school/notes/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/notes_repository.py`

3. **Implement file storage integration:**
   - Use local file storage or cloud storage
   - Implement download endpoint

4. **Implement API endpoints**

5. **Test endpoints**

---

## 2. Videos Module

**Target Location:** `modules/school/videos/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| POST | `/api/videos/upload` | Upload video | backup/api/endpoints/videos.py |
| GET | `/api/videos/teacher/my-videos` | Get my videos | backup/api/endpoints/videos.py |
| GET | `/api/videos/{video_id}` | Get video | backup/api/endpoints/videos.py |
| DELETE | `/api/videos/{video_id}` | Delete video | backup/api/endpoints/videos.py |
| GET | `/api/videos/course/{course_id}` | Get course videos | backup/api/endpoints/videos.py |
| GET | `/api/videos/{video_id}/stream` | Stream video | backup/api/endpoints/videos.py |
| GET | `/api/videos/search/{query}` | Search videos | backup/api/endpoints/videos.py |
| GET | `/api/videos/recent/all` | Get recent videos | backup/api/endpoints/videos.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/school/videos/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/videos_repository.py`

3. **Implement video streaming:**
   - Implement chunked video streaming
   - Handle multiple video formats

4. **Implement API endpoints**

5. **Test endpoints**

---

## 3. Library Enhancement Module

**Target Location:** `modules/school/library/` (enhance existing)

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/library/loans` | Get all loans | backup/api/endpoints/library.py |
| POST | `/library/loans` | Issue book | backup/api/endpoints/library.py |
| POST | `/library/loans/{loan_id}/return` | Return book | backup/api/endpoints/library.py |
| GET | `/library/loans/student/{student_id}` | Get student loans | backup/api/endpoints/library.py |
| POST | `/library/books` | Add new book | backup/api/endpoints/library.py |
| GET | `/library/books/{book_id}` | Get book | backup/api/endpoints/library.py |
| PUT | `/library/books/{book_id}` | Update book | backup/api/endpoints/library.py |

### Implementation Steps

1. **Review existing library module:**
   - Check `modules/college/college_library/` for college version
   - Need to create `modules/school/library/` for school version

2. **Create module structure:**
   ```
   modules/school/library/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

3. **Copy models from backup:**
   - Source: `backup/repositories/library_repository.py`

4. **Implement API endpoints**

5. **Test endpoints**

---

## Migration Strategy

### Step 1: Analyze Existing Code
- Review `backup/api/endpoints/notes.py`
- Review `backup/api/endpoints/videos.py`
- Review `backup/api/endpoints/library.py`

### Step 2: Extract Logic
- Copy repository logic from backup/repositories/
- Adapt for new module structure

### Step 3: Create New Modules
- Follow existing module pattern
- Use consistent naming conventions

### Step 4: Integration
- Register routes in main.py
- Add to module exports

### Step 5: Testing
- Test file upload/download
- Test video streaming
- Test library operations

---

## Time Estimate

| Module | Development Time | Testing Time |
|--------|-----------------|--------------|
| Notes | 1-2 days | 0.5 day |
| Videos | 2-3 days | 1 day |
| Library (School) | 1-2 days | 0.5 day |
| **Total** | **4-7 days** | **2 days** |

---

## Files to Reference

### Source Files (from backup/)
- `backup/api/endpoints/notes.py`
- `backup/api/endpoints/videos.py`
- `backup/api/endpoints/library.py`
- `backup/repositories/notes_repository.py`
- `backup/repositories/videos_repository.py`
- `backup/repositories/library_repository.py`

### Reference Templates
- `modules/college/college_library/` (for structure reference)

---

## Dependencies

- Notes requires file storage setup
- Videos requires video processing/streaming capability
- Library requires book catalog database

---

*Plan created: 2026-03-26*