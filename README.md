# Talemo

Talemo is a mobile-first, AI-powered platform to create and explore audio stories for families. Built with Django, Celery, CrewAI & MinIO. Discover, generate, and listen to magical tales anytime. Cloud-agnostic, open-source, and agent-driven.

## Development Setup with Docker Compose

This project uses Docker Compose to set up a development environment with all the necessary services, including PostgreSQL with pgvector extension for vector similarity search.

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

2. Create a `.env` file in the project root (optional, for custom configuration):
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to customize environment variables if needed.

3. Build and start the development containers:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. Apply migrations:
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
   ```

6. Load initial data (if available):
   ```bash
   docker-compose -f docker-compose.dev.yml exec web python manage.py loaddata initial_data
   ```

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
docker-compose -f docker-compose.dev.yml down
```

To stop and remove all data (volumes):

```bash
docker-compose -f docker-compose.dev.yml down -v
```

### Troubleshooting

- **Database connection issues**: Ensure the PostgreSQL container is running with `docker-compose -f docker-compose.dev.yml ps`. If it's not running, check the logs with `docker-compose -f docker-compose.dev.yml logs db`.

- **pgvector extension not available**: The extension should be automatically installed during container initialization. If you encounter issues, you can manually install it by running:
  ```bash
  docker-compose -f docker-compose.dev.yml exec db psql -U postgres -d talemo -c "CREATE EXTENSION IF NOT EXISTS vector;"
  ```

- **Container build failures**: If you encounter issues building the containers, try rebuilding with:
  ```bash
  docker-compose -f docker-compose.dev.yml build --no-cache
  ```

## Additional Documentation

For more detailed information about the development setup, please refer to the [Development Setup Guide](docs/development-setup.md).
