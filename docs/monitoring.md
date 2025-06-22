# Talemo Monitoring Setup

This document describes the monitoring setup for the Talemo application, which includes StatsD, ELK (Elasticsearch, Logstash, Kibana), APM (Application Performance Monitoring), and Grafana.

## Overview

The monitoring stack consists of the following components:

- **Elasticsearch**: For storing logs and APM data
- **Logstash**: For processing and forwarding logs
- **Kibana**: For visualizing logs and APM data
- **APM Server**: For collecting application performance data
- **StatsD**: For collecting metrics
- **Prometheus**: For storing metrics
- **Grafana**: For visualizing metrics

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Talemo application running

### Starting the Monitoring Stack

To start the monitoring stack, run the following command:

```bash
docker-compose -f docker/docker-compose.monitoring.yml up -d
```

This will start all the monitoring services in detached mode.

### Stopping the Monitoring Stack

To stop the monitoring stack, run the following command:

```bash
docker-compose -f docker/docker-compose.monitoring.yml down
```

### Enabling Monitoring in Django

To enable monitoring in the Django application, set the `MONITORING_ENABLED` environment variable to `true`:

```bash
export MONITORING_ENABLED=true
```

Or add it to your `.env` file:

```
MONITORING_ENABLED=true
```

## Accessing the Monitoring UI

- **Grafana**: http://localhost:3000 (default credentials: admin/admin)
- **Kibana**: http://localhost:5601
- **Prometheus**: http://localhost:9090
- **APM**: http://localhost:8200 (via Kibana)

## Available Dashboards

### Django Application Metrics

The Django Application Metrics dashboard provides an overview of the Django application's performance, including:

- Request rate
- Request latency
- Database query count
- Database query latency

### Elasticsearch Logs

The Elasticsearch Logs dashboard provides a view of the application logs, including:

- Log levels
- Log messages
- Log sources
- Log timestamps

### APM Transactions

The APM Transactions dashboard provides a view of the application's transactions, including:

- Transaction duration
- Transaction errors
- Transaction throughput
- Transaction breakdown

## Adding Custom Metrics

### StatsD Metrics

To add custom StatsD metrics in your Django application, use the `django_statsd` client:

```python
from django_statsd.clients import statsd

# Increment a counter
statsd.incr('talemo.custom.counter')

# Record a timing
statsd.timing('talemo.custom.timing', 123)

# Set a gauge
statsd.gauge('talemo.custom.gauge', 42)
```

### APM Metrics

To add custom APM metrics in your Django application, use the `elasticapm` client:

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

## Troubleshooting

### Logs

To view the logs of the monitoring services, run:

```bash
docker-compose -f docker/docker-compose.monitoring.yml logs -f <service>
```

Replace `<service>` with one of: `elasticsearch`, `logstash`, `kibana`, `apm-server`, `statsd`, `prometheus`, `grafana`.

### Common Issues

- **Elasticsearch not starting**: Check if you have enough memory allocated to Docker. Elasticsearch requires at least 2GB of memory.
- **APM data not showing up**: Check if the APM server is running and if the Django application is configured to send data to it.
- **StatsD metrics not showing up**: Check if the StatsD exporter is running and if the Django application is configured to send data to it.