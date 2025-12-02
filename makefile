.PHONY: help install dev prod test clean migrate setup docker-up docker-down

help:
	@echo "School Management System - Available Commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make setup      - Setup database and create default users"
	@echo "  make dev        - Run development server"
	@echo "  make prod       - Run production server"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean up temporary files"
	@echo "  make migrate    - Run database migrations"
	@echo "  make docker-up  - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Done!"

setup:
	@echo "Setting up database..."
	python setup_database.py
	@echo "Database setup complete!"

dev:
	@echo "Starting development server..."
	python run.py --reload

prod:
	@echo "Starting production server..."
	gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

test:
	@echo "Running tests..."
	pytest tests/ -v --cov=app --cov-report=html

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	@echo "Cleanup complete!"

migrate:
	@echo "Running migrations..."
	alembic upgrade head
	@echo "Migrations complete!"

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo "Containers started!"
	@echo "Access the application at http://localhost:8000"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down
	@echo "Containers stopped!"

docker-logs:
	docker-compose logs -f

docker-rebuild:
	@echo "Rebuilding Docker containers..."
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "Rebuild complete!"

backup:
	@echo "Creating database backup..."
	@mkdir -p backups
	docker-compose exec db pg_dump -U school_user school_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup created in backups/ directory"

restore:
	@echo "Restoring database from backup..."
	@echo "Usage: make restore BACKUP=backups/backup_YYYYMMDD_HHMMSS.sql"
	@if [ -z "$(BACKUP)" ]; then \
		echo "Error: BACKUP parameter is required"; \
		exit 1; \
	fi
	docker-compose exec -T db psql -U school_user school_db < $(BACKUP)
	@echo "Restore complete!"

lint:
	@echo "Running linters..."
	flake8 app/ --max-line-length=120
	black app/ --check
	@echo "Linting complete!"

format:
	@echo "Formatting code..."
	black app/
	isort app/
	@echo "Formatting complete!"