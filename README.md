# Talemo

Talemo is a mobile-first platform where families can discover, listen to, and co-create short audio stories—all inside a lightning-fast Progressive Web App that works on any phone or tablet. The platform is built with Django, Celery, CrewAI, and MinIO, and follows a multi-tenant architecture with strict data isolation.

## Project Overview

Talemo is an AI-powered platform designed to create and explore audio stories for families. Key features include:

- **Story Generation**: AI-powered creation of age-appropriate stories
- **Audio Narration**: High-quality voice narration of stories
- **Illustration Generation**: AI-generated illustrations for stories
- **Mobile-First Design**: Optimized for phones and tablets
- **Multi-Tenant Architecture**: Strict data isolation between tenants
- **Progressive Web App**: Works offline and can be installed on devices

## Key Technologies

- **Backend**: Django, Django REST Framework, Celery, PostgreSQL with pgvector
- **AI & Agents**: CrewAI, LlamaIndex for RAG pipeline
- **Storage**: MinIO (S3-compatible object storage)
- **Frontend**: HTMX, Bootstrap 5, Alpine.js, Workbox (PWA)
- **DevOps**: Docker, Docker Compose, GitHub Actions
- **Monitoring**: StatsD, ELK Stack (Elasticsearch, Logstash, Kibana), APM, Prometheus, Grafana, Langtrace (LLM observability)

## Project Structure

The project follows a modular structure organized by domain:

```
talemo/
├── config/                   # Project configuration
├── talemo/                   # Main application package
│   ├── core/                 # Core functionality (multi-tenant, users)
│   ├── stories/              # Story management
│   ├── agents/               # Agent framework and CrewAI integration
│   ├── assets/               # Asset management (audio, images)
│   ├── governance/           # Governance and compliance
│   └── subscriptions/        # Subscription management
├── frontend/                 # Frontend assets
├── docker/                   # Docker configuration files
├── scripts/                  # Utility scripts
├── tests/                    # Test suite
└── docs/                     # Documentation
```

## Docker-Based Development Environment

This project uses Docker Compose to set up a development environment with all the necessary services, including PostgreSQL with pgvector extension for vector similarity search. Each service runs in its own container for better isolation and scalability.

### Prerequisites

- Docker (version 24.0+)
- Docker Compose (version 2.20+)
- Git (version 2.40+)

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/talemo.git
   cd talemo
   ```

2. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to customize environment variables if needed. This file is used by all containers to ensure consistent configuration across services.

3. Initialize the application (this will build, start, setup tenants, setup development environment, and create a superuser):
   ```bash
   make init
   ```
   This will perform all the necessary setup steps for development.

   Alternatively, you can run the steps individually:

   a. Build and start the development containers:
      ```bash
      make up
      ```

   b. Setup the development environment (migrations, seed data, static files):
      ```bash
      make setup-dev
      ```

   c. Create a superuser:
      ```bash
      make superuser
      ```

4. Load additional fixtures (if available):
   ```bash
   make loaddata
   ```

### Available Makefile Commands

The project includes a comprehensive set of Makefile commands to streamline development. You can view all available commands by running `make help`. Here's an overview of the key command categories:

#### Docker Environment Commands

These commands manage the Docker environment:

- `make up` - Build (if needed) and start all development containers
- `make down` - Stop all development containers
- `make ps` - Check container status
- `make restart` - Restart all development containers
- `make logs` - Check logs for web service
- `make clean` - Remove all containers and volumes

#### Celery Commands

These commands manage Celery services and tasks:

- `make celery-up` - Start Celery worker
- `make celery-beat-up` - Start Celery beat scheduler
- `make flower-up` - Start Flower monitoring
- `make celery-down` - Stop Celery worker
- `make celery-beat-down` - Stop Celery beat scheduler
- `make flower-down` - Stop Flower monitoring
- `make celery-restart` - Restart Celery worker
- `make celery-beat-restart` - Restart Celery beat scheduler
- `make flower-restart` - Restart Flower monitoring
- `make celery-logs` - Check logs for Celery worker
- `make logs-celery` - Alias for celery-logs (backward compatibility)
- `make celery-beat-logs` - Check logs for Celery beat scheduler
- `make flower-logs` - Check logs for Flower monitoring
- `make celery-status` - Check status of Celery workers
- `make celery-inspect` - Inspect registered Celery tasks
- `make celery-purge` - Purge all Celery task queues
- `make celery-run` - Run a one-off Celery task (e.g., `make celery-run TASK='generate_hero' ARGS='[{"age_range": "6-8"}]'`)
- `make celery-example` - Run a Celery example script (e.g., `make celery-example SCRIPT='test_celery_task'`)

#### Docker Build Commands

These commands build Docker containers:

- `make build` - Build all containers (infrastructure and application)
- `make build-infrastructure` - Build infrastructure containers (db, redis, minio, mailhog)
- `make build-application` - Build application containers (web, celery, celery-beat, flower)

#### Application Commands

These commands run operations inside the Docker containers:

- `make init` - Initialize the application (build, start, setup tenants, setup development environment, create superuser)
- `make migrate` - Apply database migrations
- `make migrations` - Create database migrations
- `make apply-migrations` - Apply migrations for multi-tenant setup (both shared and tenant-specific)
- `make superuser` - Create a superuser
- `make seed` - Seed the database with initial data
- `make collectstatic` - Collect static files
- `make setup-dev` - Setup development environment (migrate, seed, collectstatic)
- `make loaddata` - Load additional fixtures
- `make test` - Run tests
- `make test-unit` - Run unit tests
- `make test-integration` - Run integration tests
- `make coverage` - Run tests with coverage
- `make shell` - Open a Django shell
- `make pgvector` - Create pgvector extension in the database
- `make create-tenant` - Create a new tenant for multi-tenant development


#### Monitoring Commands

These commands manage the Docker-based monitoring stack:

- `make build-monitoring` - Build monitoring containers
- `make monitoring-up` - Start the monitoring stack
- `make monitoring-down` - Stop the monitoring stack
- `make monitoring-ps` - Check monitoring container status
- `make monitoring-logs` - Check logs for monitoring services
- `make test-monitoring` - Run monitoring tests

### Container Architecture

The development environment consists of the following containers:

- **db**: PostgreSQL database with pgvector extension for vector similarity search
- **web**: Django web server for the main application
- **redis**: Redis for caching and as a message broker for Celery
- **minio**: MinIO for object storage (S3-compatible)
- **celery**: Celery worker for asynchronous task processing
- **celery-beat**: Celery Beat for scheduled tasks
- **flower**: Flower for monitoring Celery tasks
- **mailhog**: Mailhog for email testing

Each service has its own Dockerfile to ensure proper isolation and to make it easier to scale individual components as needed.

### Accessing Services

- Django Web Server: http://localhost:8000
- Django Admin: http://localhost:8000/admin
- MinIO Console: http://localhost:9001 (login with minioadmin/minioadmin)
- Flower Dashboard: http://localhost:5555
- Mailhog: http://localhost:8025

### Working with PostgreSQL and pgvector

The development environment includes PostgreSQL with the pgvector extension for vector similarity search. The database is initialized with a utility function to create vector columns and indexes:

```sql
-- Example usage in your SQL queries:
SELECT create_vector_index('my_table', 'embedding', 1536);
```

In your Django models, you can use pgvector with the following pattern:

```python
from django.db import models

class Document(models.Model):
    content = models.TextField()
    # The vector field will be added by the create_vector_index function
    # or you can add it manually in a migration
```

### Stopping the Environment

To stop the development environment:

```bash
make down
```

To stop and remove all data (volumes):

```bash
make clean
```

### Troubleshooting

- **Database connection issues**: Ensure the PostgreSQL container is running with `make up` and then check the status with `make ps`. If it's not running, check the logs with `make logs`.

- **pgvector extension not available**: The extension should be automatically installed during container initialization. If you encounter issues, you can manually install it by running:
  ```bash
  make pgvector
  ```

- **Container build failures**: If you encounter issues building the containers, try rebuilding with:
  ```bash
  make build
  ```

- **"relation does not exist" error when creating a superuser**: This error occurs when the database tables for the core app haven't been properly migrated in the multi-tenant setup. To fix this, run:
  ```bash
  make apply-migrations
  ```
  This will apply migrations for both shared apps (on the public schema) and tenant-specific apps.

### Customizing the Docker Setup

All Docker-related files are organized in the `docker` directory:

- `docker/Dockerfile.web`: Django web server
- `docker/Dockerfile.celery`: Celery worker
- `docker/Dockerfile.celery-beat`: Celery Beat scheduler
- `docker/Dockerfile.flower`: Flower monitoring tool
- `docker/docker-compose.dev.yml`: Docker Compose configuration for development

If you need to customize a specific service, you can modify its Dockerfile in the `docker` directory. For example, if you need to add a new system dependency to the web service, you would modify `docker/Dockerfile.web`.

You can also customize the Docker Compose setup by modifying the `docker/docker-compose.dev.yml` file. For example, you might want to add a new service or change the port mappings.

## Docker-Based Monitoring Stack

The project includes a complete Docker-based monitoring stack with StatsD, ELK (Elasticsearch, Logstash, Kibana), APM (Application Performance Monitoring), and Grafana. This stack provides comprehensive monitoring and observability for the application.

### Monitoring Components

- **Elasticsearch**: For storing logs and APM data
- **Logstash**: For processing and forwarding logs
- **Kibana**: For visualizing logs and APM data
- **APM Server**: For collecting application performance data
- **StatsD**: For collecting metrics
- **Prometheus**: For storing metrics
- **Grafana**: For visualizing metrics
- **Langtrace**: For LLM observability and tracing

### Starting the Monitoring Stack

To start the monitoring stack:

```bash
make monitoring-up
```

This will start all the monitoring services in detached mode.

### Accessing Monitoring Services

- **Grafana**: http://localhost:3000 (default credentials: admin/admin)
- **Kibana**: http://localhost:5601
- **Prometheus**: http://localhost:9090
- **APM**: http://localhost:8200 (via Kibana)
- **Langtrace**: http://localhost:3001 (for LLM observability)

### Enabling Monitoring in Django

To enable monitoring in the Django application, set the `MONITORING_ENABLED` environment variable to `true` in your `.env` file:

```
MONITORING_ENABLED=true
```

### Enabling Langtrace for LLM Observability

To enable Langtrace for LLM observability, set the following environment variables in your `.env` file:

```
LANGTRACE_ENABLED=true
LANGTRACE_HOST=http://langtrace:3000
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
```

After setting up Langtrace, you can instrument your LLM calls in the agents module to track:
- Token usage
- Prompt templates
- Model parameters
- Response times
- Completion content


## Development Workflow

### Code Changes

- Make changes to the codebase
- Django's auto-reload will detect changes and restart the server
- For frontend changes, run `npm run watch` to compile assets automatically

### Database Changes

- Create migrations: `make migrations`
- Apply migrations: `make migrate` (for standard Django migrations)
- Apply multi-tenant migrations: `make apply-migrations` (for both shared and tenant-specific apps)

### Testing

- Run all tests: `make test`
- Run unit tests: `make test-unit`
- Run integration tests: `make test-integration`
- Generate coverage report: `make coverage`

### Debugging

- Django Debug Toolbar is enabled in development
- Use `print()` or `import pdb; pdb.set_trace()` for Python debugging
- Use browser developer tools for frontend debugging
- Check Flower dashboard for Celery task monitoring

## Working with Agents

Talemo uses CrewAI for agent-based workflows:

### Agent Development

- Agents run in the Celery worker container
- Monitor agent tasks in the Flower dashboard
- Use the agent playground at `/agents/playground/`

### Agent Testing

- Create mock agent responses for testing
- Use the agent test harness in `tests/agents/`
- Monitor token usage with the built-in tracking

## Multi-Tenant Development

Talemo follows a multi-tenant architecture with strict data isolation:

1. Create test tenants: `make create-tenant`
2. Switch tenants:
   - Use the tenant switcher in the development UI
   - Or set the `X-Tenant-ID` header in API requests
3. Test tenant isolation:
   - Create test data in multiple tenants
   - Verify data isolation using the tenant switcher
   - Run tenant isolation tests

## Testing Strategy

### Test Types

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test interactions between components
3. **End-to-End Tests**: Test complete user journeys with Cypress
4. **Performance Tests**: Load testing with Locust

### Test Organization

Tests are organized by domain and test type:

```
tests/
├── unit/              # Unit tests for individual components
├── integration/       # Integration tests for component interactions
├── e2e/               # End-to-end tests for user journeys
└── performance/       # Performance and load tests
```

## Version Control Strategy

We follow a GitHub Flow branching strategy:

1. **Main Branch**: Always deployable, protected branch
2. **Feature Branches**: Created from main, named `feature/short-description`
3. **Bugfix Branches**: Created from main, named `bugfix/short-description`
4. **Hotfix Branches**: Created from main, named `hotfix/short-description`

### Pull Request Process

1. Create a feature/bugfix branch from main
2. Make changes and commit to the branch
3. Push the branch to GitHub
4. Create a pull request with a description of the changes
5. Ensure CI checks pass
6. Request review from at least one team member
7. Address review comments
8. Merge the pull request when approved

## Development Best Practices

### Code Quality

- Follow PEP 8 style guide for Python code
- Use Black for code formatting
- Use Flake8 for linting
- Use MyPy for type checking
- Use pre-commit hooks to enforce standards

### Security Practices

- Follow OWASP Top 10 guidelines
- Use Django's security features (CSRF, XSS protection, etc.)
- Implement proper input validation
- Use parameterized queries to prevent SQL injection
- Regularly update dependencies for security patches

### Performance Considerations

- Optimize database queries (use select_related, prefetch_related)
- Use caching appropriately
- Minimize HTTP requests
- Optimize asset loading (lazy loading, compression)
- Monitor and optimize API response times

## Additional Documentation

For more detailed information, please refer to the following documentation:

- [Development Setup Guide](docs/development-setup.md): Comprehensive guide to setting up the development environment
- [Monitoring Setup Guide](docs/monitoring.md): Detailed information about the monitoring stack
- [Docker Configuration](docker/README.md): Information about the Docker setup, including both development and monitoring environments
