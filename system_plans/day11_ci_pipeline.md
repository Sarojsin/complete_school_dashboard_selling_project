# Day 11 Production Implementation Plan
**Date**: 2026-05-16
**Focus**: CI/CD Pipeline - GitHub Actions Setup

## Objectives
- Implement automated CI pipeline with GitHub Actions
- Enforce code quality gates (linting, tests, security scanning)
- Add automated coverage reporting via Codecov or Coveralls
- Configure branch protection rules (documented)
- Setup automatic Docker image builds on push to main

## Tasks

### 1. Morning: GitHub Actions Workflow Configuration (2.5 hours)
**Create `.github/workflows/ci.yml`**:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop, feature/*]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Cache pip dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov
          pip install bandit safety
          pip install ruff black isort
      
      - name: Lint with ruff
        run: ruff check . --output-format=github
      
      - name: Format check with black
        run: black --check .
      
      - name: Import sort check with isort
        run: isort --check-only .
      
      - name: Security scan with bandit
        run: bandit -r modules/ -f json -o bandit-report.json || true
      
      - name: Dependency vulnerability scan with safety
        run: safety check --json || true
      
      - name: Run tests with pytest
        env:
          DATABASE_MODE: separate
          SCHOOL_DATABASE_URL: sqlite:///./test_school.db
          COLLEGE_DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
          SECRET_KEY: test_secret_key_for_ci_only_1234567890
          ALGORITHM: HS256
          ACCESS_TOKEN_EXPIRE_MINUTES: 15
        run: |
          pytest tests/ -v --cov=modules --cov-report=xml --cov-report=term
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: pytest-results-${{ matrix.python-version }}
          path: |
            htmlcov/
            bandit-report.json
```

### 2. Setup Code Quality Tools (1 hour)
**Install & configure**:
- [ ] Ensure `ruff` in `requirements.txt`:
  ```
  ruff>=0.3.0
  black>=24.0.0
  isort>=5.12.0
  ```
- [ ] Create `pyproject.toml` for tool configuration:
  ```toml
  [tool.ruff]
  line-length = 100
  target-version = "py311"
  select = ["E", "F", "I", "N", "W", "B", "A", "C4", "UP", "RUF"]
  
  [tool.black]
  line-length = 100
  include = '\.pyi?$'
  
  [tool.isort]
  profile = "black"
  line_length = 100
  ```
- [ ] Add `pre-commit` config (optional but recommended):
  ```yaml
  repos:
    - repo: https://github.com/astral-sh/ruff-pre-commit
      rev: v0.3.0
      hooks:
        - id: ruff
          args: [--fix]
    - repo: https://github.com/psf/black
      rev: 24.2.0
      hooks:
        - id: black
    - repo: https://github.com/pycqa/isort
      rev: 5.12.0
      hooks:
        - id: isort
  ```
- [ ] Install: `pre-commit install`

**Manual lint check**:
- [ ] `ruff check modules/` – fix any errors
- [ ] `black .` – apply formatting
- [ ] `isort .` – sort imports
- [ ] Commit clean code

### 3. Docker Image Build Workflow (1 hour)
**Create `.github/workflows/docker.yml`**:

```yaml
name: Build & Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub (optional)
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: |
            school-college-backend:latest
            school-college-backend:${{ github.sha }}
            ${{ github.event_name != 'pull_request' && format('school-college-backend:v{0}', github.ref_name) || '' }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 4. Branch Protection Rules Documentation (30 min)
**Document in `DEPLOYMENT.md` or `CI_CD.md`**:
- [ ] Create `CI_CD.md`:
  - Required status checks: `test (ubuntu-latest, python-version: 3.11)` must pass
  - Require linear history (rebase)
  - Require code review (1+ approving review)
  - Do not allow bypassing for anyone
  - Automatically delete head branches after merge
- [ ] Instructions to enable:
  ```bash
  gh repo edit <repo> --enable-branch-protection="main"
  # Or via GitHub UI: Settings → Branches → Add rule
  ```

### 5. Test Coverage Badge (30 min)
**Add to README.md**:
```markdown
![Tests](https://img.shields.io/github/actions/workflow/status/<owner>/<repo>/ci.yml?branch=main)
![Coverage](https://img.shields.io/codecov/c/github/<owner>/<repo>/main)
```

### 6. Commit & Verify (1 hour)
- [ ] `.github/workflows/ci.yml` committed
- [ ] `.github/workflows/docker.yml` committed
- [ ] `pyproject.toml` updated with lint/format configs
- [ ] `requirements.txt` has ruff, black, isort
- [ ] Push to GitHub: `git push origin main`
- [ ] Monitor Actions tab: ensure workflow runs and passes
- [ ] Fix any failures (import errors, missing deps)

### 7. Optional: Additional Workflows (1 hour)
**Consider adding**:
- [ ] `security.yml` – weekly bandit + safety scan on schedule
- [ ] `deploy.yml` – auto-deploy to staging on merge to develop
- [ ] `notify.yml` – Slack/Teams notification on failure

## Deliverables
- ✅ `.github/workflows/ci.yml` – test, lint, security scan, coverage
- ✅ `pyproject.toml` – tool configurations
- ✅ `requirements.txt` updated with code quality tools
- ✅ `.github/workflows/docker.yml` – auto Docker builds
- ✅ `CI_CD.md` – documentation of pipeline and branch rules
- ✅ README badges added
- ✅ CI passing on first commit (green check)

## Success Criteria
- Every push triggers CI; workflow completes successfully
- Lint step fails on ruff errors (test with intentional error)
- Test coverage uploaded to Codecov (visible badge)
- Docker image built and tagged on push to main
- Branch protection can be configured based on documented rules

## Notes
- Use `GITHUB_TOKEN` secret already available; need `CODECOV_TOKEN` from codecov.io (free for public)
- Keep CI fast (<10 min); split into matrix if needed
- Cache pip dependencies to speed up
- Ensure test DB created in CI (use service container)

## Next: Day 12
Implement Redis caching for frequently accessed reference data (fee structures, programs, departments). Add caching decorators to repository methods, invalidate on writes.
