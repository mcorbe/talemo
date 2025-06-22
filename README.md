# Talemo

Talemo is a mobile-first, AI-powered platform to create and explore audio stories for families. Built with Django, Celery, CrewAI & MinIO. Discover, generate, and listen to magical tales anytime. Cloud-agnostic, open-source, and agent-driven.

## Development Setup with Docker Compose

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

3. Build and start the development containers:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml up -d
   ```

4. Apply migrations:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml exec web python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml exec web python manage.py createsuperuser
   ```

6. Load initial data (if available):
   ```bash
   docker-compose -f docker/docker-compose.dev.yml exec web python manage.py loaddata initial_data
   ```

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
docker-compose -f docker/docker-compose.dev.yml down
```

To stop and remove all data (volumes):

```bash
docker-compose -f docker/docker-compose.dev.yml down -v
```

### Troubleshooting

- **Database connection issues**: Ensure the PostgreSQL container is running with `docker-compose -f docker/docker-compose.dev.yml ps`. If it's not running, check the logs with `docker-compose -f docker/docker-compose.dev.yml logs db`.

- **pgvector extension not available**: The extension should be automatically installed during container initialization. If you encounter issues, you can manually install it by running:
  ```bash
  docker-compose -f docker/docker-compose.dev.yml exec db psql -U postgres -d talemo -c "CREATE EXTENSION IF NOT EXISTS vector;"
  ```

- **Container build failures**: If you encounter issues building the containers, try rebuilding with:
  ```bash
  docker-compose -f docker/docker-compose.dev.yml build --no-cache
  ```

### Customizing the Docker Setup

All Docker-related files are organized in the `docker` directory:

- `docker/Dockerfile.web`: Django web server
- `docker/Dockerfile.celery`: Celery worker
- `docker/Dockerfile.celery-beat`: Celery Beat scheduler
- `docker/Dockerfile.flower`: Flower monitoring tool
- `docker/docker-compose.dev.yml`: Docker Compose configuration for development

If you need to customize a specific service, you can modify its Dockerfile in the `docker` directory. For example, if you need to add a new system dependency to the web service, you would modify `docker/Dockerfile.web`.

You can also customize the Docker Compose setup by modifying the `docker/docker-compose.dev.yml` file. For example, you might want to add a new service or change the port mappings.

## Additional Documentation

For more detailed information about the development setup, please refer to the [Development Setup Guide](docs/development-setup.md).
