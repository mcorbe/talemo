# Docker Configuration

This directory contains Docker configuration files for the Talemo project. These files define how the application and its dependencies are containerized and orchestrated.

## Overview

The Docker setup is designed to create a complete development environment with all necessary services running in separate containers. This approach ensures consistency across development environments and simplifies the setup process.

## File Structure

- `docker-compose.dev.yml`: Docker Compose configuration for the development environment
- `docker-compose.monitoring.yml`: Docker Compose configuration for the monitoring stack
- `Dockerfile.web`: Dockerfile for the Django web server
- `Dockerfile.celery`: Dockerfile for the Celery worker
- `Dockerfile.celery-beat`: Dockerfile for the Celery Beat scheduler
- `Dockerfile.flower`: Dockerfile for the Flower monitoring tool
- `Dockerfile.dev`: Dockerfile for general development environment

## Container Architecture

### Development Environment

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

### Monitoring Stack

The monitoring stack consists of the following containers:

- **elasticsearch**: For storing logs and APM data
- **logstash**: For processing and forwarding logs
- **kibana**: For visualizing logs and APM data
- **apm-server**: For collecting application performance data
- **statsd**: For collecting metrics
- **prometheus**: For storing metrics
- **grafana**: For visualizing metrics
- **langtrace**: For LLM observability and tracing
- **langtrace-db**: PostgreSQL database for Langtrace

The monitoring stack is defined in `docker-compose.monitoring.yml` and can be started separately from the development environment.

## Development Setup

### Prerequisites

Before setting up the development environment, ensure you have the following installed:

- **Docker** (version 24.0+) and **Docker Compose** (version 2.20+)
- **Git** (version 2.40+)
- **Python** (version 3.11+) for local development tools
- **Node.js** (version 20.0+) and **npm** (version 9.0+) for frontend development
- **PostgreSQL** client tools (version 15+) for database management

### Environment Configuration

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/talemo.git
   cd talemo
   ```

2. Create a `.env` file in the project root with the necessary environment variables. You can use the `.env.example` file as a template:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file to set your specific configuration values.

### Initial Setup

1. Start the development environment:
   ```bash
   make up
   ```

2. Apply database migrations:
   ```bash
   make migrate
   ```

3. Create a superuser for the Django admin:
   ```bash
   make superuser
   ```

4. Load initial data (if available):
   ```bash
   make loaddata
   ```

5. Create the pgvector extension for vector similarity search:
   ```bash
   make pgvector
   ```

## Usage

### Development Environment

#### Starting the Environment

To start the development environment:

```bash
docker-compose -f docker/docker-compose.dev.yml up -d
```

Or using the Makefile:

```bash
make up
```

#### Accessing Development Services

- Django Web Server: http://localhost:8000
- Django Admin: http://localhost:8000/admin
- MinIO Console: http://localhost:9001 (login with minioadmin/minioadmin)
- Flower Dashboard: http://localhost:5555
- Mailhog: http://localhost:8025

#### Running Commands

To run commands in a container:

```bash
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py migrate
```

Or using the Makefile:

```bash
make migrate
```

### Monitoring Stack

#### Starting the Monitoring Stack

To start the monitoring stack:

```bash
docker-compose -f docker/docker-compose.monitoring.yml up -d
```

Or using the Makefile:

```bash
make monitoring-up
```

#### Stopping the Monitoring Stack

To stop the monitoring stack:

```bash
docker-compose -f docker/docker-compose.monitoring.yml down
```

Or using the Makefile:

```bash
make monitoring-down
```

#### Accessing Monitoring Services

- Grafana: http://localhost:3000 (login with admin/admin)
- Kibana: http://localhost:5601
- Prometheus: http://localhost:9090
- APM: http://localhost:8200 (via Kibana)
- Langtrace: http://localhost:3001 (for LLM observability)

#### Enabling Monitoring in Django

To enable monitoring in the Django application, set the `MONITORING_ENABLED` environment variable to `true` in your `.env` file:

```
MONITORING_ENABLED=true
```

#### Enabling Langtrace for LLM Observability

To enable Langtrace for LLM observability, set the following environment variables in your `.env` file:

```
LANGTRACE_ENABLED=true
LANGTRACE_HOST=http://langtrace:3000
LANGTRACE_PUBLIC_KEY=your-public-key
LANGTRACE_SECRET_KEY=your-secret-key
```

After setting up Langtrace, you can instrument your LLM calls in the agents module to track:
- Token usage
- Prompt templates
- Model parameters
- Response times
- Completion content

Example integration with the CrewAI framework:

```python
from langfuse.client import Langfuse

# Initialize Langfuse client
langfuse = Langfuse(
    public_key=os.getenv("LANGTRACE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGTRACE_SECRET_KEY"),
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

#### Monitoring Commands

The Makefile includes several commands for working with the monitoring stack:

- `make monitoring-up` - Start the monitoring stack
- `make monitoring-down` - Stop the monitoring stack
- `make monitoring-ps` - Check monitoring container status
- `make monitoring-logs` - Check logs for monitoring services
- `make test-monitoring` - Run monitoring tests

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

### Development Environment

- **Container fails to start**: Check the logs with `docker-compose -f docker/docker-compose.dev.yml logs [service_name]`
- **Database connection issues**: Ensure the PostgreSQL container is running and healthy
- **Volume mounting issues**: Check that the volume paths in `docker-compose.dev.yml` are correct

### Monitoring Stack

- **Elasticsearch not starting**: Check if you have enough memory allocated to Docker. Elasticsearch requires at least 2GB of memory.
- **APM data not showing up**: Check if the APM server is running and if the Django application is configured to send data to it.
- **StatsD metrics not showing up**: Check if the StatsD exporter is running and if the Django application is configured to send data to it.
- **Monitoring service logs**: View logs with `docker-compose -f docker/docker-compose.monitoring.yml logs [service_name]` or use `make monitoring-logs`

## Related Documentation

### Docker and Services

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL with pgvector](https://github.com/pgvector/pgvector)
- [MinIO Documentation](https://docs.min.io/)

### Monitoring

- [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [APM Documentation](https://www.elastic.co/guide/en/apm/index.html)
- [StatsD Exporter Documentation](https://github.com/prometheus/statsd_exporter)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Langtrace (Langfuse) Documentation](https://langfuse.com/docs)

### Project Documentation

- [Development Setup Guide](../docs/development-setup.md)
- [Monitoring Setup Guide](../docs/monitoring.md)
