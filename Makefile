.PHONY: help install run test clean docker-build docker-run docker-stop lint format

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

run: ## Run the application locally
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	pytest -v

test-coverage: ## Run tests with coverage
	pytest --cov=app --cov-report=html --cov-report=term-missing

lint: ## Run linting
	flake8 app tests
	mypy app

format: ## Format code
	black app tests
	isort app tests

clean: ## Clean cache and temp files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-build: ## Build Docker image
	docker-compose build

docker-run: ## Run with Docker Compose
	docker-compose up -d

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

init-db: ## Initialize database
	python -c "from app.database import init_db; init_db()"

dev-setup: install init-db ## Setup development environment
	@echo "Development environment ready!"
