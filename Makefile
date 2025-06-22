# Talemo Makefile
# This file contains common commands for development

# Variables
DOCKER_COMPOSE = docker-compose -f docker/docker-compose.dev.yml
DOCKER_COMPOSE_EXEC_WEB = $(DOCKER_COMPOSE) exec web

# Colors
YELLOW := \033[1;33m
GREEN := \033[1;32m
RED := \033[1;31m
NC := \033[0m # No Color

# Help
.PHONY: help
help:
	@echo "$(YELLOW)Talemo Development Commands$(NC)"
	@echo "$(GREEN)make up$(NC)              - Start the development environment"
	@echo "$(GREEN)make down$(NC)            - Stop the development environment"
	@echo "$(GREEN)make ps$(NC)              - Check container status"
	@echo "$(GREEN)make build$(NC)           - Build the containers"
	@echo "$(GREEN)make restart$(NC)         - Restart the development environment"
	@echo "$(GREEN)make migrate$(NC)         - Apply migrations"
	@echo "$(GREEN)make migrations$(NC)      - Create migrations"
	@echo "$(GREEN)make superuser$(NC)       - Create a superuser"
	@echo "$(GREEN)make loaddata$(NC)        - Load initial data"
	@echo "$(GREEN)make test$(NC)            - Run tests"
	@echo "$(GREEN)make test-unit$(NC)       - Run unit tests"
	@echo "$(GREEN)make test-integration$(NC) - Run integration tests"
	@echo "$(GREEN)make coverage$(NC)        - Run tests with coverage"
	@echo "$(GREEN)make logs$(NC)            - Check logs for web service"
	@echo "$(GREEN)make logs-celery$(NC)     - Check logs for celery service"
	@echo "$(GREEN)make shell$(NC)           - Open a Django shell"
	@echo "$(GREEN)make clean$(NC)           - Remove all containers and volumes"
	@echo "$(GREEN)make pgvector$(NC)        - Create pgvector extension in the database"
	@echo "$(GREEN)make create-tenant$(NC)   - Create a new tenant for multi-tenant development"

# Docker commands
.PHONY: up
up:
	@echo "$(YELLOW)Starting development environment...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Development environment started!$(NC)"
	@echo "Django Web Server: http://localhost:8000"
	@echo "Django Admin: http://localhost:8000/admin"
	@echo "MinIO Console: http://localhost:9001 (login with minioadmin/minioadmin)"
	@echo "Flower Dashboard: http://localhost:5555"
	@echo "Mailhog: http://localhost:8025"

.PHONY: down
down:
	@echo "$(YELLOW)Stopping development environment...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)Development environment stopped!$(NC)"

.PHONY: build
build:
	@echo "$(YELLOW)Building containers...$(NC)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)Containers built!$(NC)"

.PHONY: restart
restart:
	@echo "$(YELLOW)Restarting development environment...$(NC)"
	$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)Development environment restarted!$(NC)"

.PHONY: clean
clean:
	@echo "$(YELLOW)Removing all containers and volumes...$(NC)"
	$(DOCKER_COMPOSE) down -v
	@echo "$(GREEN)All containers and volumes removed!$(NC)"

.PHONY: ps
ps:
	@echo "$(YELLOW)Checking container status...$(NC)"
	$(DOCKER_COMPOSE) ps

# Database commands
.PHONY: create-tenant
create-tenant:
	@echo "$(YELLOW)Creating a new tenant...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) python manage.py create_tenant
	@echo "$(GREEN)Tenant created!$(NC)"

.PHONY: pgvector
pgvector:
	@echo "$(YELLOW)Creating pgvector extension...$(NC)"
	$(DOCKER_COMPOSE) exec db psql -U postgres -d talemo -c "CREATE EXTENSION IF NOT EXISTS vector;"
	@echo "$(GREEN)pgvector extension created!$(NC)"

# Django commands
.PHONY: migrate
migrate:
	@echo "$(YELLOW)Applying migrations...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) python manage.py migrate
	@echo "$(GREEN)Migrations applied!$(NC)"

.PHONY: migrations
migrations:
	@echo "$(YELLOW)Creating migrations...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) python manage.py makemigrations
	@echo "$(GREEN)Migrations created!$(NC)"

.PHONY: superuser
superuser:
	@echo "$(YELLOW)Creating superuser...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) python manage.py createsuperuser
	@echo "$(GREEN)Superuser created!$(NC)"

.PHONY: loaddata
loaddata:
	@echo "$(YELLOW)Loading initial data...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) python manage.py loaddata initial_data
	@echo "$(GREEN)Initial data loaded!$(NC)"

.PHONY: shell
shell:
	@echo "$(YELLOW)Opening Django shell...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) python manage.py shell_plus
	@echo "$(GREEN)Shell closed!$(NC)"

# Testing commands
.PHONY: test
test:
	@echo "$(YELLOW)Running tests...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) pytest
	@echo "$(GREEN)Tests completed!$(NC)"

.PHONY: test-unit
test-unit:
	@echo "$(YELLOW)Running unit tests...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) pytest tests/unit/
	@echo "$(GREEN)Unit tests completed!$(NC)"

.PHONY: test-integration
test-integration:
	@echo "$(YELLOW)Running integration tests...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) pytest tests/integration/
	@echo "$(GREEN)Integration tests completed!$(NC)"

.PHONY: coverage
coverage:
	@echo "$(YELLOW)Running tests with coverage...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) pytest --cov=talemo
	@echo "$(GREEN)Coverage tests completed!$(NC)"

# Logging commands
.PHONY: logs
logs:
	@echo "$(YELLOW)Checking logs for web service...$(NC)"
	$(DOCKER_COMPOSE) logs -f web

.PHONY: logs-celery
logs-celery:
	@echo "$(YELLOW)Checking logs for celery service...$(NC)"
	$(DOCKER_COMPOSE) logs -f celery
