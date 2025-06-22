# Django Settings

This directory contains the Django settings files for the Talemo project. The settings are organized in a hierarchical structure to support different environments (development, staging, production).

## Overview

The settings are split into multiple files:
- A base settings file with common configurations
- Environment-specific settings files that extend the base settings

This approach allows for easy configuration management across different environments while minimizing code duplication.

## File Structure

- `__init__.py`: Imports the appropriate settings file based on the environment
- `base.py`: Base settings shared across all environments
- `dev.py`: Development-specific settings that extend the base settings

## Usage

### Environment Selection

By default, the development settings are used. This is controlled in `__init__.py`:

```python
# Use development settings by default
from .dev import *
```

To use a different environment in production, you would modify this file to import the production settings instead.

### Base Settings

The `base.py` file contains settings that are common across all environments, including:

- Installed applications
- Middleware configuration
- URL configuration
- Template settings
- Authentication backends
- REST Framework configuration
- Celery configuration
- Multi-tenant settings

### Environment-Specific Settings

The `dev.py` file extends the base settings with development-specific configurations:

- Debug mode enabled
- Secret key (for development only)
- Database configuration
- MinIO/S3 storage settings
- Email backend configuration
- Debug toolbar settings
- AI service API keys

## Adding New Settings

When adding new settings:

1. Add common settings to `base.py`
2. Add environment-specific settings to the appropriate environment file (e.g., `dev.py`)
3. For new environments, create a new file (e.g., `prod.py`) that imports from `base.py` and overrides as needed

## Security Considerations

- Never commit sensitive information (API keys, passwords) to version control
- Use environment variables for sensitive settings
- In production, ensure `DEBUG` is set to `False`
- Use a strong, unique `SECRET_KEY` in production

## Related Documentation

For more information about Django settings, refer to:

- [Django Settings Documentation](https://docs.djangoproject.com/en/4.2/topics/settings/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)