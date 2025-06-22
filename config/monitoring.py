"""
Monitoring configuration for the Talemo application.
This module provides configuration for StatsD, ELK, and APM with Grafana UI.
"""

import os

# Elastic APM Configuration
ELASTIC_APM = {
    'SERVICE_NAME': os.environ.get('APM_SERVICE_NAME', 'talemo'),
    'SERVER_URL': os.environ.get('APM_SERVER_URL', 'http://apm-server:8200'),
    'ENVIRONMENT': os.environ.get('ENVIRONMENT', 'development'),
    'DEBUG': os.environ.get('APM_DEBUG', 'false').lower() == 'true',
    'DJANGO_TRANSACTION_NAME_FROM_ROUTE': True,
    'CAPTURE_BODY': 'all',
    'CAPTURE_HEADERS': True,
    'METRICS_INTERVAL': '30s',
}

# StatsD Configuration
STATSD_HOST = os.environ.get('STATSD_HOST', 'statsd')
STATSD_PORT = int(os.environ.get('STATSD_PORT', 9125))
STATSD_PREFIX = os.environ.get('STATSD_PREFIX', 'talemo')
STATSD_CLIENT = 'django_statsd.clients.normal'

# Prometheus Configuration
PROMETHEUS_EXPORT_MIGRATIONS = False

# Logging Configuration for ELK
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': os.environ.get('LOGSTASH_HOST', 'logstash'),
            'port': int(os.environ.get('LOGSTASH_PORT', 5000)),
            'version': 1,
            'message_type': 'django',
            'fqdn': False,
            'tags': ['django', 'talemo'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logstash'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'logstash'],
            'level': 'INFO',
            'propagate': False,
        },
        'talemo': {
            'handlers': ['console', 'logstash'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# Monitoring Apps
MONITORING_APPS = [
    'elasticapm.contrib.django',
    'django_statsd',
    'django_prometheus',
]

# Monitoring Middleware
MONITORING_MIDDLEWARE = [
    'elasticapm.contrib.django.middleware.TracingMiddleware',
    'django_statsd.middleware.StatsdMiddleware',
    'django_statsd.middleware.StatsdMiddlewareTimer',
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]