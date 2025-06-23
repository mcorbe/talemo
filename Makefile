# Talemo Makefile
# This file contains common commands for development

# Variables
DOCKER_COMPOSE = docker-compose -f docker/docker-compose.dev.yml
DOCKER_COMPOSE_MONITORING = docker-compose -f docker/docker-compose.monitoring.yml
DOCKER_COMPOSE_EXEC_WEB = $(DOCKER_COMPOSE) exec web

# Colors
YELLOW := \033[1;33m
GREEN := \033[1;32m
RED := \033[1;31m
NC := \033[0m # No Color

# Help
.PHONY: help
help:
	@echo "$(YELLOW)Talemo Commands$(NC)"
	@echo ""
	@echo "$(YELLOW)Setup Commands:$(NC)"
	@echo "$(GREEN)make setup$(NC)                  - Setup the entire environment"
	@echo "$(GREEN)make setup-infrastructure$(NC)   - Setup infrastructure environment"
	@echo "$(GREEN)make setup-monitoring$(NC)       - Setup monitoring environment"
	@echo "$(GREEN)make setup-application$(NC)      - Setup application environment"
	@echo ""
	@echo "$(YELLOW)Install Commands:$(NC)"
	@echo "$(GREEN)make install$(NC)                - Install all dependencies"
	@echo "$(GREEN)make install-infrastructure$(NC) - Install infrastructure dependencies"
	@echo "$(GREEN)make install-monitoring$(NC)     - Install monitoring dependencies"
	@echo "$(GREEN)make install-application$(NC)    - Install application dependencies"
	@echo ""
	@echo "$(YELLOW)Build Commands:$(NC)"
	@echo "$(GREEN)make build$(NC)                  - Build all containers"
	@echo "$(GREEN)make build-infrastructure$(NC)   - Build infrastructure containers"
	@echo "$(GREEN)make build-monitoring$(NC)       - Build monitoring containers"
	@echo "$(GREEN)make build-application$(NC)      - Build application containers"
	@echo ""
	@echo "$(YELLOW)Run Commands:$(NC)"
	@echo "$(GREEN)make run$(NC)                    - Run all services as daemons"
	@echo "$(GREEN)make run-infrastructure$(NC)     - Run infrastructure services as daemons"
	@echo "$(GREEN)make run-monitoring$(NC)         - Run monitoring services as daemons"
	@echo "$(GREEN)make run-application$(NC)        - Run application services as daemons"
	@echo ""
	@echo "$(YELLOW)Development Commands:$(NC)"
	@echo "$(GREEN)make up$(NC)                     - Start the development environment"
	@echo "$(GREEN)make down$(NC)                   - Stop the development environment"
	@echo "$(GREEN)make ps$(NC)                     - Check container status"
	@echo "$(GREEN)make restart$(NC)                - Restart the development environment"
	@echo "$(GREEN)make migrate$(NC)                - Apply migrations"
	@echo "$(GREEN)make migrations$(NC)             - Create migrations"
	@echo "$(GREEN)make superuser$(NC)              - Create a superuser"
	@echo "$(GREEN)make loaddata$(NC)               - Load initial data"
	@echo "$(GREEN)make test$(NC)                   - Run tests"
	@echo "$(GREEN)make test-unit$(NC)              - Run unit tests"
	@echo "$(GREEN)make test-integration$(NC)       - Run integration tests"
	@echo "$(GREEN)make coverage$(NC)               - Run tests with coverage"
	@echo "$(GREEN)make logs$(NC)                   - Check logs for web service"
	@echo "$(GREEN)make logs-celery$(NC)            - Check logs for celery service"
	@echo "$(GREEN)make shell$(NC)                  - Open a Django shell"
	@echo "$(GREEN)make clean$(NC)                  - Remove all containers and volumes"
	@echo "$(GREEN)make pgvector$(NC)               - Create pgvector extension in the database"
	@echo "$(GREEN)make create-tenant$(NC)          - Create a new tenant for multi-tenant development"
	@echo ""
	@echo "$(YELLOW)Monitoring Commands:$(NC)"
	@echo "$(GREEN)make monitoring-up$(NC)          - Start the monitoring stack"
	@echo "$(GREEN)make monitoring-down$(NC)        - Stop the monitoring stack"
	@echo "$(GREEN)make monitoring-ps$(NC)          - Check monitoring container status"
	@echo "$(GREEN)make monitoring-logs$(NC)        - Check logs for monitoring services"
	@echo "$(GREEN)make test-monitoring$(NC)        - Run monitoring tests"

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
build: build-infrastructure build-application
	@echo "$(GREEN)All containers built!$(NC)"

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

# Monitoring commands
.PHONY: monitoring-up
monitoring-up:
	@echo "$(YELLOW)Starting monitoring stack...$(NC)"
	$(DOCKER_COMPOSE_MONITORING) up -d
	@echo "$(GREEN)Monitoring stack started!$(NC)"
	@echo "Grafana: http://localhost:3000 (login with admin/admin)"
	@echo "Kibana: http://localhost:5601"
	@echo "Prometheus: http://localhost:9090"
	@echo "APM: http://localhost:8200 (via Kibana)"

.PHONY: monitoring-down
monitoring-down:
	@echo "$(YELLOW)Stopping monitoring stack...$(NC)"
	$(DOCKER_COMPOSE_MONITORING) down
	@echo "$(GREEN)Monitoring stack stopped!$(NC)"

.PHONY: monitoring-ps
monitoring-ps:
	@echo "$(YELLOW)Checking monitoring container status...$(NC)"
	$(DOCKER_COMPOSE_MONITORING) ps

.PHONY: monitoring-logs
monitoring-logs:
	@echo "$(YELLOW)Checking logs for monitoring services...$(NC)"
	@echo "Available services: elasticsearch, logstash, kibana, apm-server, statsd, prometheus, grafana"
	@read -p "Enter service name: " service; \
	$(DOCKER_COMPOSE_MONITORING) logs -f $$service

.PHONY: test-monitoring
test-monitoring:
	@echo "$(YELLOW)Running monitoring tests...$(NC)"
	$(DOCKER_COMPOSE_EXEC_WEB) python scripts/test_monitoring.py --all
	@echo "$(GREEN)Monitoring tests completed!$(NC)"

# Setup commands
.PHONY: setup setup-infrastructure setup-monitoring setup-application

setup: setup-infrastructure setup-monitoring setup-application
	@echo "$(GREEN)All environments have been set up!$(NC)"

setup-infrastructure:
	@echo "$(YELLOW)Setting up infrastructure environment...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file from .env.example"; \
	fi
	@echo "$(GREEN)Infrastructure environment setup complete!$(NC)"

setup-monitoring:
	@echo "$(YELLOW)Setting up monitoring environment...$(NC)"
	@mkdir -p docker/prometheus/data
	@mkdir -p docker/grafana/data
	@mkdir -p docker/elasticsearch/data
	@echo "$(GREEN)Monitoring environment setup complete!$(NC)"

setup-application:
	@echo "$(YELLOW)Setting up application environment...$(NC)"
	@if [ ! -d "venv" ]; then \
		python -m venv venv; \
		echo "Created virtual environment"; \
	fi
	@echo "$(GREEN)Application environment setup complete!$(NC)"

# Install commands
.PHONY: install install-infrastructure install-monitoring install-application

install: install-infrastructure install-monitoring install-application
	@echo "$(GREEN)All dependencies have been installed!$(NC)"

install-infrastructure:
	@echo "$(YELLOW)Installing infrastructure dependencies...$(NC)"
	@echo "No specific infrastructure dependencies to install"
	@echo "$(GREEN)Infrastructure dependencies installed!$(NC)"

install-monitoring:
	@echo "$(YELLOW)Installing monitoring dependencies...$(NC)"
	@. venv/bin/activate && pip install -r requirements-monitoring.txt
	@echo "$(GREEN)Monitoring dependencies installed!$(NC)"

install-application:
	@echo "$(YELLOW)Installing application dependencies...$(NC)"
	@. venv/bin/activate && pip install -r requirements-dev.txt
	@echo "$(GREEN)Application dependencies installed!$(NC)"

# Build commands
.PHONY: build-infrastructure build-monitoring build-application

build-infrastructure:
	@echo "$(YELLOW)Building infrastructure containers...$(NC)"
	$(DOCKER_COMPOSE) build db redis minio mailhog
	@echo "$(GREEN)Infrastructure containers built!$(NC)"

build-monitoring:
	@echo "$(YELLOW)Building monitoring containers...$(NC)"
	$(DOCKER_COMPOSE_MONITORING) build
	@echo "$(GREEN)Monitoring containers built!$(NC)"

build-application:
	@echo "$(YELLOW)Building application containers...$(NC)"
	$(DOCKER_COMPOSE) build web celery celery-beat flower
	@echo "$(GREEN)Application containers built!$(NC)"

# Run commands
.PHONY: run run-infrastructure run-monitoring run-application

run: run-infrastructure run-monitoring run-application
	@echo "$(GREEN)All services are running as daemons!$(NC)"
	@echo "Django Web Server: http://localhost:8000"
	@echo "Django Admin: http://localhost:8000/admin"
	@echo "MinIO Console: http://localhost:9001 (login with minioadmin/minioadmin)"
	@echo "Flower Dashboard: http://localhost:5555"
	@echo "Mailhog: http://localhost:8025"
	@echo "Grafana: http://localhost:3000 (login with admin/admin)"
	@echo "Kibana: http://localhost:5601"
	@echo "Prometheus: http://localhost:9090"
	@echo "APM: http://localhost:8200 (via Kibana)"

run-infrastructure:
	@echo "$(YELLOW)Running infrastructure services as daemons...$(NC)"
	$(DOCKER_COMPOSE) up -d db redis minio mailhog
	@echo "$(GREEN)Infrastructure services are running!$(NC)"

run-monitoring:
	@echo "$(YELLOW)Running monitoring services as daemons...$(NC)"
	$(DOCKER_COMPOSE_MONITORING) up -d
	@echo "$(GREEN)Monitoring services are running!$(NC)"

run-application:
	@echo "$(YELLOW)Running application services as daemons...$(NC)"
	$(DOCKER_COMPOSE) up -d web celery celery-beat flower
	@echo "$(GREEN)Application services are running!$(NC)"
