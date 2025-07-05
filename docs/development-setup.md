# Talemo - Development Setup Guide

## 1. Document Control

| Item          | Value                                           |
| ------------- | ----------------------------------------------- |
| **Product**   | Talemo - Family Audio-Stories Platform          |
| **Version**   | 1.0                                             |
| **Author**    | Engineering Team                                |
| **Date**      | 2025                                            |
| **Reviewers** | CTO, Product Team, DevOps, Security             |

---

## 2. Introduction

This document outlines the development setup process for the Talemo platform. It provides instructions for setting up the development environment, required technologies, local development workflow, testing strategy, deployment pipeline, version control strategy, and documentation approach.

Talemo is a mobile-first platform where French families can discover, listen to, and co-create short audio stories—all inside a lightning-fast Progressive Web App that works on any phone or tablet. The platform is built with Django, Celery, CrewAI, and MinIO, and follows a multi-tenant architecture with strict data isolation.

---

## 3. Development Environment Setup

### 3.1 Prerequisites

Before setting up the development environment, ensure you have the following installed:

- **Docker** (version 24.0+) and **Docker Compose** (version 2.20+)
- **Git** (version 2.40+)
- **Python** (version 3.11+) for local development tools
- **Node.js** (version 20.0+) and **npm** (version 9.0+) for frontend development
- **PostgreSQL** client tools (version 15+) for database management

### 3.2 Repository Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/talemo.git
   cd talemo
   ```

2. Create a virtual environment (optional, for local Python tools):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

### 3.3 Docker Environment

The development environment is containerized using Docker to ensure consistency across developer machines and to simplify the setup of complex dependencies.

1. Build and start the development containers:
   ```bash
   docker compose -f docker/docker-compose.dev.yml up -d
   ```

2. The development environment includes the following services:
   - **Django Web Server**: Main application server
   - **PostgreSQL**: Database with pgvector extension
   - **MinIO**: Object storage for assets
   - **Redis**: Cache and message broker
   - **Celery**: Asynchronous task processing
   - **Celery Beat**: Scheduled tasks
   - **Flower**: Celery monitoring
   - **Mailhog**: Email testing

3. Access the development services:
   - Django Web Server: http://localhost:8000
   - Django Admin: http://localhost:8000/admin
   - MinIO Console: http://localhost:9001
   - Flower Dashboard: http://localhost:5555
   - Mailhog: http://localhost:8025
   - Redis: localhost:6380 (mapped from internal port 6379)

### 3.4 Environment Configuration

1. Create a `.env` file in the project root with the following variables:
   ```
   # Django
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database
   DB_NAME=talemo
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432

   # MinIO
   MINIO_ROOT_USER=minioadmin
   MINIO_ROOT_PASSWORD=minioadmin
   MINIO_ENDPOINT=minio:9000
   MINIO_SECURE=False
   MINIO_BUCKET=talemo

   # Redis
   REDIS_HOST=redis
   REDIS_PORT=6379
   # Note: Redis is mapped to port 6380 on the host machine

   # OAuth (for development)
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   APPLE_CLIENT_ID=your-apple-client-id
   APPLE_CLIENT_SECRET=your-apple-client-secret

   # AI Services (for development)
   OPENAI_API_KEY=your-openai-api-key
   STABILITY_API_KEY=your-stability-api-key

   # Observability
   LANGFUSE_PUBLIC_KEY=your-langfuse-public-key
   LANGFUSE_SECRET_KEY=your-langfuse-secret-key
   ```

2. For local development without Docker, create a `.env.local` file with appropriate localhost values.

---

## 4. Project Structure

The Talemo project follows a modular structure organized by domain:

```
talemo/
├── .github/                  # GitHub workflows and templates
├── config/                   # Project configuration
│   ├── settings/             # Django settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI configuration
├── docs/                     # Documentation
├── talemo/                   # Main application package
│   ├── core/                 # Core functionality
│   │   ├── middleware/       # Multi-tenant middleware
│   │   ├── models/           # Core models (Tenant, Profile, User)
│   │   └── permissions/      # Profile-based permission system
│   ├── stories/              # Story management
│   │   ├── models/           # Story models
│   │   ├── views/            # Story views
│   │   ├── api/              # Story API endpoints
│   │   └── templates/        # Story templates
│   ├── agents/               # Agent framework
│   │   ├── models/           # Agent models
│   │   ├── tasks/            # Celery tasks for agents
│   │   └── crew/             # CrewAI integration
│   ├── assets/               # Asset management
│   │   ├── models/           # Asset models
│   │   ├── storage/          # Storage backends
│   │   └── api/              # Asset API endpoints
│   ├── governance/           # Governance and compliance
│   │   ├── models/           # Governance models
│   │   ├── audit/            # Audit logging
│   │   └── api/              # Governance API endpoints
│   └── subscriptions/        # Subscription management
│       ├── models/           # Subscription models
│       └── api/              # Subscription API endpoints
├── frontend/                 # Frontend assets
│   ├── static/               # Static files
│   ├── templates/            # Base templates
│   └── pwa/                  # PWA configuration
├── scripts/                  # Utility scripts
├── tests/                    # Test suite
├── .env.example              # Example environment variables
├── docker/                  # Docker configuration files
│   ├── docker-compose.dev.yml    # Development Docker Compose
│   ├── Dockerfile.web            # Web service Dockerfile
│   ├── Dockerfile.celery         # Celery worker Dockerfile
│   ├── Dockerfile.celery-beat    # Celery Beat Dockerfile
│   └── Dockerfile.flower         # Flower monitoring Dockerfile
├── Dockerfile                # Main Dockerfile
├── Dockerfile.dev            # Development Dockerfile
├── manage.py                 # Django management script
├── pyproject.toml            # Python project configuration
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── README.md                 # Project README
```

---

## 5. Required Technologies and Dependencies

### 5.1 Backend Dependencies

- **Django**: Web framework
- **Django REST Framework**: API framework
- **django-allauth**: Authentication with SSO providers
- **django-storages**: Storage backends for MinIO/S3
- **Celery**: Asynchronous task processing
- **CrewAI**: Agent-based workflows
- **psycopg2-binary**: PostgreSQL adapter
- **redis**: Redis client
- **minio**: MinIO client
- **pyjwt**: JWT authentication
- **LlamaIndex**: RAG pipeline for semantic search
- **pgvector**: Vector similarity search

### 5.2 Frontend Dependencies

- **HTMX**: Dynamic interactions without full page reloads
- **Bootstrap 5**: Responsive design framework
- **Alpine.js**: Lightweight JavaScript framework
- **Workbox**: Service worker for PWA
- **Howler.js**: Audio playback library
- **Chart.js**: Data visualization

### 5.3 Development Tools

- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking
- **pre-commit**: Git hooks
- **coverage**: Test coverage
- **django-debug-toolbar**: Debugging
- **django-extensions**: Development utilities
- **factory_boy**: Test data generation
- **Cypress**: End-to-end testing

### 5.4 DevOps Tools

- **Docker**: Containerization
- **Docker Compose**: Container orchestration
- **GitHub Actions**: CI/CD
- **Prometheus**: Monitoring
- **Grafana**: Dashboards
- **Sentry**: Error tracking
- **Arize Phoenix**: AI observability (development)
- **Langfuse**: AI observability (production)

---

## 6. Local Development Workflow

### 6.1 Getting Started

1. Start the development environment:
   ```bash
   docker compose -f docker/docker-compose.dev.yml up -d
   ```

2. Apply migrations:
   ```bash
   docker compose -f docker/docker-compose.dev.yml exec web python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   docker compose -f docker/docker-compose.dev.yml exec web python manage.py createsuperuser
   ```

4. Load initial data:
   ```bash
   docker compose -f docker/docker-compose.dev.yml exec web python manage.py loaddata initial_data
   ```

### 6.2 Development Workflow using the Makefile

The project includes a Makefile to simplify common development tasks. To see all available commands, run:

```bash
make help
```

Some common commands include:

- `make up` - Start the development environment
- `make down` - Stop the development environment
- `make ps` - Check container status
- `make build` - Build the containers
- `make migrate` - Apply migrations
- `make migrations` - Create migrations
- `make test` - Run tests
- `make coverage` - Run tests with coverage
- `make logs` - Check logs for web service
- `make logs-celery` - Check logs for celery service
- `make shell` - Open a Django shell
- `make clean` - Remove all containers and volumes
- `make pgvector` - Create pgvector extension in the database

Using the Makefile is the recommended way to interact with the development environment as it provides a consistent interface and handles the complexity of the underlying commands.

### 6.3 Development Workflow

1. **Code Changes**:
   - Make changes to the codebase
   - Django's auto-reload will detect changes and restart the server
   - For frontend changes, run `npm run watch` to compile assets automatically

2. **Database Changes**:
   - Create migrations: `docker-compose -f docker/docker-compose.dev.yml exec web python manage.py makemigrations`
   - Apply migrations: `docker-compose -f docker/docker-compose.dev.yml exec web python manage.py migrate`

3. **Testing**:
   - Run tests: `docker-compose -f docker/docker-compose.dev.yml exec web pytest`
   - Run specific tests: `docker-compose -f docker/docker-compose.dev.yml exec web pytest tests/test_stories.py`
   - Generate coverage report: `docker-compose -f docker/docker-compose.dev.yml exec web pytest --cov=talemo`

4. **Debugging**:
   - Django Debug Toolbar is enabled in development
   - Use `print()` or `import pdb; pdb.set_trace()` for Python debugging
   - Use browser developer tools for frontend debugging
   - Check Flower dashboard for Celery task monitoring

### 6.4 Working with Agents

1. **Local Agent Development**:
   - Agents run in the Celery worker container
   - Monitor agent tasks in the Flower dashboard
   - Use Arize Phoenix for local agent observability

2. **Agent Testing**:
   - Create mock agent responses for testing
   - Use the agent test harness in `tests/agents/`
   - Monitor token usage with the built-in tracking

3. **Agent Debugging**:
   - Enable verbose logging for agents
   - Use the agent playground at `/agents/playground/`
   - Inspect agent tasks in the database

### 6.5 Multi-Tenant Development

1. **Creating Test Tenants**:
   ```bash
   make create-tenant
   ```

2. **Switching Tenants**:
   - Use the tenant switcher in the development UI
   - Or set the `X-Tenant-ID` header in API requests

3. **Testing Tenant Isolation**:
   - Create test data in multiple tenants
   - Verify data isolation using the tenant switcher
   - Run tenant isolation tests: `docker-compose -f docker/docker-compose.dev.yml exec web pytest tests/test_tenant_isolation.py`

---

## 7. Testing Strategy

### 7.1 Test Types

1. **Unit Tests**:
   - Test individual components in isolation
   - Focus on models, services, and utility functions
   - Use pytest fixtures for test data

2. **Integration Tests**:
   - Test interactions between components
   - Focus on API endpoints and agent workflows
   - Use factory_boy for test data generation

3. **End-to-End Tests**:
   - Test complete user journeys
   - Use Cypress for browser-based testing
   - Focus on critical paths (story creation, playback, etc.)

4. **Performance Tests**:
   - Load testing with Locust
   - Database query optimization
   - API response time benchmarking

### 7.2 Test Organization

Tests are organized by domain and test type:

```
tests/
├── unit/
│   ├── core/
│   ├── stories/
│   ├── agents/
│   └── ...
├── integration/
│   ├── api/
│   ├── agents/
│   └── ...
├── e2e/
│   ├── cypress/
│   └── ...
└── performance/
    ├── locust/
    └── ...
```

### 7.3 Running Tests

1. **Run all tests**:
   ```bash
   docker compose -f docker/docker-compose.dev.yml exec web pytest
   ```

2. **Run specific test types**:
   ```bash
   docker compose -f docker/docker-compose.dev.yml exec web pytest tests/unit/
   docker compose -f docker/docker-compose.dev.yml exec web pytest tests/integration/
   ```

3. **Run with coverage**:
   ```bash
   docker compose -f docker/docker-compose.dev.yml exec web pytest --cov=talemo
   ```

4. **Run E2E tests**:
   ```bash
   docker compose -f docker/docker-compose.dev.yml exec web python manage.py cypress run
   ```

5. **Run performance tests**:
   ```bash
   docker compose -f docker/docker-compose.dev.yml exec web locust -f tests/performance/locustfile.py
   ```

### 7.4 CI Integration

Tests are automatically run in the CI pipeline:
- Unit and integration tests on every pull request
- E2E tests on merge to main branch
- Performance tests on a scheduled basis

---

## 8. Deployment Pipeline

### 8.1 Environments

1. **Development**:
   - Local development environment
   - Feature branches
   - Developer-specific instances

2. **Staging**:
   - Mirrors production configuration
   - Used for integration testing
   - Accessible to internal team

3. **Production**:
   - French cloud hosting with SecNumCloud certification
   - Strict security controls
   - Production data

### 8.2 CI/CD Pipeline

The CI/CD pipeline is implemented using GitHub Actions:

1. **Continuous Integration**:
   - Triggered on pull requests
   - Runs linting, type checking, and tests
   - Builds Docker images
   - Generates test coverage reports

2. **Continuous Deployment**:
   - Triggered on merge to main branch
   - Deploys to staging environment
   - Runs integration tests
   - Manual approval for production deployment

3. **Production Deployment**:
   - Blue/green deployment strategy
   - Database migrations with safety checks
   - Cache warming
   - Post-deployment smoke tests

### 8.3 Deployment Configuration

Deployment configuration is managed using:
- Kubernetes manifests for container orchestration
- Helm charts for package management
- Terraform for infrastructure as code
- Sealed Secrets for sensitive information

### 8.4 Monitoring & Alerting

- Prometheus for metrics collection
- Grafana for dashboards and visualization
- Sentry for error tracking
- PagerDuty for alerting
- Langfuse for AI observability

#### 8.4.1 Monitoring Stack Setup

The project includes a complete monitoring stack with StatsD, ELK (Elasticsearch, Logstash, Kibana), APM (Application Performance Monitoring), and Grafana.

1. **Starting the Monitoring Stack**:
   ```bash
   docker-compose -f docker/docker-compose.monitoring.yml up -d
   ```
   Or using the Makefile:
   ```bash
   make monitoring-up
   ```

2. **Stopping the Monitoring Stack**:
   ```bash
   docker-compose -f docker/docker-compose.monitoring.yml down
   ```
   Or using the Makefile:
   ```bash
   make monitoring-down
   ```

3. **Accessing Monitoring Services**:
   - Grafana: http://localhost:3000 (default credentials: admin/admin)
   - Kibana: http://localhost:5601
   - Prometheus: http://localhost:9090
   - APM: http://localhost:8200 (via Kibana)
   - Langtrace: http://localhost:3001 (for LLM observability)

4. **Enabling Monitoring in Django**:
   To enable monitoring in the Django application, set the `MONITORING_ENABLED` environment variable to `true` in your `.env` file:
   ```
   MONITORING_ENABLED=true
   ```

5. **Enabling Langtrace for LLM Observability**:
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

6. **Monitoring Commands**:
   The Makefile includes several commands for working with the monitoring stack:
   - `make monitoring-up` - Start the monitoring stack
   - `make monitoring-down` - Stop the monitoring stack
   - `make monitoring-ps` - Check monitoring container status
   - `make monitoring-logs` - Check logs for monitoring services
   - `make test-monitoring` - Run monitoring tests

6. **Adding Custom Metrics**:
   - StatsD metrics:
     ```python
     from django_statsd.clients import statsd

     # Increment a counter
     statsd.incr('talemo.custom.counter')

     # Record a timing
     statsd.timing('talemo.custom.timing', 123)

     # Set a gauge
     statsd.gauge('talemo.custom.gauge', 42)
     ```

   - APM metrics:
     ```python
     from elasticapm.contrib.django.client import client

     # Record a custom transaction
     with client.capture_transaction('custom_transaction'):
         # Do something

     # Record a custom span
     with client.capture_span('custom_span'):
         # Do something

     # Record a custom error
     try:
         # Do something that might fail
     except Exception as e:
         client.capture_exception()
     ```

   - Langtrace (Langfuse) for LLM observability:
     ```python
     from langfuse.client import Langfuse
     import os

     # Initialize Langfuse client
     langfuse = Langfuse(
         public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
         secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
         host=os.getenv("LANGTRACE_HOST")
     )

     # Create a trace for a user session
     trace = langfuse.trace(
         name="story_creation",
         user_id="user-123",
         metadata={"tenant_id": "tenant-456"}
     )

     # Log LLM generation
     generation = trace.generation(
         name="story_draft",
         model="gpt-4",
         prompt="Create a story about...",
         completion="Once upon a time...",
         usage={
             "prompt_tokens": 50,
             "completion_tokens": 200,
             "total_tokens": 250
         }
     )
     ```

For more detailed information about the monitoring setup, see the [Monitoring Setup Guide](../docs/monitoring.md).

---

## 9. Version Control Strategy

### 9.1 Branching Strategy

We follow a GitHub Flow branching strategy:

1. **Main Branch**:
   - Always deployable
   - Protected branch (requires pull request and approval)
   - Automatically deployed to staging

2. **Feature Branches**:
   - Created from main
   - Named with format: `feature/short-description`
   - Merged back to main via pull request

3. **Bugfix Branches**:
   - Created from main
   - Named with format: `bugfix/short-description`
   - Merged back to main via pull request

4. **Hotfix Branches**:
   - Created from main
   - Named with format: `hotfix/short-description`
   - Merged back to main via pull request
   - Deployed immediately after merge

### 9.2 Pull Request Process

1. Create a feature/bugfix branch from main
2. Make changes and commit to the branch
3. Push the branch to GitHub
4. Create a pull request with a description of the changes
5. Ensure CI checks pass
6. Request review from at least one team member
7. Address review comments
8. Merge the pull request when approved

### 9.3 Commit Guidelines

- Use conventional commits format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep commits focused and atomic
- Write clear commit messages

### 9.4 Version Tagging

- Semantic versioning (MAJOR.MINOR.PATCH)
- Tag releases in GitHub
- Include release notes with each tag

---

## 10. Documentation Approach

### 10.1 Documentation Types

1. **Code Documentation**:
   - Docstrings for all modules, classes, and functions
   - Type hints for all function parameters and return values
   - Comments for complex logic

2. **API Documentation**:
   - OpenAPI/Swagger specification
   - Endpoint descriptions, parameters, and responses
   - Authentication requirements
   - Example requests and responses

3. **User Documentation**:
   - Admin user guide
   - Developer guide
   - API reference
   - Deployment guide

4. **Architecture Documentation**:
   - System architecture diagrams
   - Component interactions
   - Data flow diagrams
   - Security architecture

### 10.2 Documentation Tools

- **Sphinx**: Python documentation generator
- **MkDocs**: Project documentation site
- **drf-spectacular**: OpenAPI schema generation
- **PlantUML**: Diagrams as code
- **Docusaurus**: Developer portal (future)

### 10.3 Documentation Workflow

1. Update documentation alongside code changes
2. Include documentation updates in pull requests
3. Review documentation as part of code review
4. Generate and publish documentation on release

### 10.4 Documentation Location

- Code documentation: In the codebase as docstrings
- API documentation: Generated from code and published to developer portal
- User documentation: In the `docs/` directory and published to documentation site
- Architecture documentation: In the `docs/architecture/` directory

---

## 11. Development Best Practices

### 11.1 Code Quality

- Follow PEP 8 style guide for Python code
- Use Black for code formatting
- Use Flake8 for linting
- Use MyPy for type checking
- Use pre-commit hooks to enforce standards

### 11.2 Security Practices

- Follow OWASP Top 10 guidelines
- Use Django's security features (CSRF, XSS protection, etc.)
- Implement proper input validation
- Use parameterized queries to prevent SQL injection
- Regularly update dependencies for security patches

### 11.3 Performance Considerations

- Optimize database queries (use select_related, prefetch_related)
- Use caching appropriately
- Minimize HTTP requests
- Optimize asset loading (lazy loading, compression)
- Monitor and optimize API response times

### 11.4 Multi-Tenant Development

- Always consider tenant context in queries
- Test features with multiple tenants
- Ensure proper data isolation
- Use the tenant middleware for all requests
- Implement row-level security for all tenant-bound tables

### 11.5 AI Agent Development

- Follow CrewAI best practices
- Implement proper error handling and fallbacks
- Monitor token usage and costs
- Ensure agent tasks are idempotent
- Implement proper observability

---

## 12. Getting Help

### 12.1 Documentation Resources

- Project documentation: `/docs`
- API documentation: `/api/docs/`
- CrewAI documentation: https://docs.crewai.com/
- Django documentation: https://docs.djangoproject.com/

### 12.2 Communication Channels

- GitHub Issues: Bug reports and feature requests
- Slack: Day-to-day communication
- Email: For sensitive or private matters
- Weekly team meetings: For discussion and planning

### 12.3 Troubleshooting

1. Check the logs:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml logs -f web
   docker-compose -f docker/docker-compose.dev.yml logs -f celery
   ```

2. Debug the application:
   - Use Django Debug Toolbar
   - Check Flower dashboard for Celery tasks
   - Use browser developer tools for frontend issues

3. Common issues:
   - Database migration conflicts
   - Celery task failures
   - MinIO connection issues
   - Agent API rate limits

---

## 13. Conclusion

This development setup guide provides a comprehensive overview of the Talemo platform development environment, workflow, and best practices. By following these guidelines, developers can quickly set up their environment and start contributing to the project.

For any questions or issues, please contact the engineering team.
