# Requirements Files Structure

This project uses a modular approach to managing Python dependencies, with separate requirements files for different components of the application. This approach ensures that each Docker container only installs the dependencies it needs, which speeds up the build process.

## Requirements Files Overview

- `requirements-base.txt`: Common dependencies for all containers
- `requirements-web.txt`: Web-specific dependencies (includes base)
- `requirements-celery.txt`: Celery-specific dependencies (includes base)
- `requirements-celery-beat.txt`: Celery Beat-specific dependencies (includes base)
- `requirements-flower.txt`: Flower-specific dependencies (includes base)
- `requirements-monitoring.txt`: Monitoring-specific dependencies
- `requirements.txt`: All dependencies for local development (includes web and testing tools)

## Docker Container Requirements

Each Docker container uses a specific requirements file:

- Web container: `requirements-web.txt`
- Celery container: `requirements-celery.txt`
- Celery Beat container: `requirements-celery-beat.txt`
- Flower container: `requirements-flower.txt`

## Adding New Dependencies

When adding new dependencies:

1. Determine which container(s) need the dependency
2. Add the dependency to the appropriate requirements file:
   - If all containers need it, add to `requirements-base.txt`
   - If only the web container needs it, add to `requirements-web.txt`
   - If only Celery workers need it, add to `requirements-celery.txt`
   - If only Celery Beat needs it, add to `requirements-celery-beat.txt`
   - If only Flower needs it, add to `requirements-flower.txt`
   - If it's a monitoring dependency, add to `requirements-monitoring.txt`
   - If it's a development/testing tool, add to `requirements.txt`

3. Rebuild the affected container(s):
   ```bash
   make build-application  # For all application containers
   ```
   
   Or for a specific container:
   ```bash
   docker compose -f docker/docker-compose.dev.yml build web  # For web container
   ```

## Local Development

For local development outside of Docker, you can install all dependencies using:

```bash
pip install -r requirements.txt
```

This will install all dependencies needed for development, including testing tools.