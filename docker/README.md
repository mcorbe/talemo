# Docker Configuration

This directory contains Docker configuration files for the Talemo project. These files define how the application and its dependencies are containerized and orchestrated.

## Overview

The Docker setup is designed to create a complete development environment with all necessary services running in separate containers. This approach ensures consistency across development environments and simplifies the setup process.

## File Structure

- `docker-compose.dev.yml`: Docker Compose configuration for the development environment
- `Dockerfile.web`: Dockerfile for the Django web server
- `Dockerfile.celery`: Dockerfile for the Celery worker
- `Dockerfile.celery-beat`: Dockerfile for the Celery Beat scheduler
- `Dockerfile.flower`: Dockerfile for the Flower monitoring tool
- `Dockerfile.dev`: Dockerfile for general development environment

## Container Architecture

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

## Usage

### Starting the Environment

To start the development environment:

```bash
docker-compose -f docker/docker-compose.dev.yml up -d
```

Or using the Makefile:

```bash
make up
```

### Accessing Services

- Django Web Server: http://localhost:8000
- Django Admin: http://localhost:8000/admin
- MinIO Console: http://localhost:9001 (login with minioadmin/minioadmin)
- Flower Dashboard: http://localhost:5555
- Mailhog: http://localhost:8025

### Running Commands

To run commands in a container:

```bash
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py migrate
```

Or using the Makefile:

```bash
make migrate
```

## Customizing the Docker Setup

### Adding Dependencies

To add new dependencies:

1. Add the dependency to `requirements.txt` or `requirements-dev.txt`
2. Rebuild the containers:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml build
   ```
   Or using the Makefile:
   ```bash
   make build
   ```

### Modifying Service Configuration

To modify a service configuration:

1. Edit the appropriate Dockerfile (e.g., `Dockerfile.web` for the web service)
2. Update the `docker-compose.dev.yml` file if necessary
3. Rebuild and restart the containers

### Adding New Services

To add a new service:

1. Create a new Dockerfile for the service
2. Add the service to `docker-compose.dev.yml`
3. Update the Makefile if necessary
4. Rebuild and restart the containers

## Troubleshooting

- **Container fails to start**: Check the logs with `docker-compose -f docker/docker-compose.dev.yml logs [service_name]`
- **Database connection issues**: Ensure the PostgreSQL container is running and healthy
- **Volume mounting issues**: Check that the volume paths in `docker-compose.dev.yml` are correct

## Related Documentation

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL with pgvector](https://github.com/pgvector/pgvector)
- [MinIO Documentation](https://docs.min.io/)