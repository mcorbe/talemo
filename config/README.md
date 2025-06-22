# Django Configuration

This directory contains the Django configuration files for the Talemo project. These files define how the Django application is set up, including URL routing, settings, and application configuration.

## Overview

The configuration is structured to support different environments (development, staging, production) through the use of separate settings files in the `settings` directory.

## File Structure

- `asgi.py`: ASGI configuration for asynchronous web servers
- `celery.py`: Celery configuration for asynchronous task processing
- `__init__.py`: Package initialization file that imports Celery app
- `settings/`: Directory containing environment-specific settings
  - `__init__.py`: Imports development settings by default
  - `base.py`: Base settings shared across all environments
  - `dev.py`: Development-specific settings
- `urls.py`: URL routing configuration for the entire application
- `wsgi.py`: WSGI configuration for traditional web servers

## Usage

### Settings

The settings are organized hierarchically:

1. `settings/base.py` contains common settings used across all environments
2. `settings/dev.py` extends the base settings with development-specific configurations

To use a different environment, modify the import in `settings/__init__.py`:

```python
# Use development settings
from .dev import *

# For production (commented out by default)
# from .prod import *
```

### URL Configuration

The `urls.py` file defines the URL routing for the application. It includes:

- Admin interface routes
- API routes organized by app
- Authentication routes
- App-specific routes
- Static and media file serving in development

## Adding New Configuration

When adding new configuration:

1. For environment-specific settings, add them to the appropriate file in `settings/`
2. For URL patterns, add them to `urls.py` in the appropriate section
3. For new Celery tasks or configuration, modify `celery.py`

## Related Documentation

For more information about Django configuration, refer to:

- [Django Settings Documentation](https://docs.djangoproject.com/en/4.2/topics/settings/)
- [Django URL Dispatcher](https://docs.djangoproject.com/en/4.2/topics/http/urls/)
- [Celery Documentation](https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html)