# Talemo Django Project Configuration

This file provides specific guidance for the Talemo project - a Django-based platform for families to discover, listen to, and co-create short audio stories.

## Project Overview

Talemo is a Progressive Web App (PWA) built with Django that features:
- AI-powered story generation using CrewAI
- Audio streaming with HLS (HTTP Live Streaming)
- Text-to-speech conversion for story narration
- Multi-tenant architecture for data isolation
- Asynchronous task processing with Celery

## Talemo-Specific Development Commands

### Development Environment
- `make up` - Start all Docker containers
- `make down` - Stop all containers
- `make restart` - Restart all containers
- `make logs` - View container logs
- `make shell` - Access Django shell in container
- `make init` - Initialize development environment

### Django Management
- `python manage.py runserver` - Start development server
- `python manage.py runserver 0.0.0.0:8000` - Start server accessible from network

### Database Management
- `python manage.py makemigrations` - Create database migrations
- `python manage.py migrate` - Apply database migrations
- `python manage.py showmigrations` - Show migration status
- `python manage.py sqlmigrate app_name migration_name` - Show SQL for migration
- `python manage.py dbshell` - Open database shell

### User Management
- `python manage.py createsuperuser` - Create admin superuser
- `python manage.py changepassword username` - Change user password
- `python manage.py shell` - Open Django shell

### Static Files & Media
- `python manage.py collectstatic` - Collect static files for production
- `python manage.py findstatic filename` - Find static file location

### Testing & Quality
- `python manage.py test` - Run Django tests
- `python manage.py test app_name` - Run tests for specific app
- `python manage.py test --keepdb` - Run tests keeping test database
- `coverage run --source='.' manage.py test` - Run tests with coverage

### Development Tools
- `python manage.py check` - Check for Django issues
- `python manage.py validate` - Validate models
- `python manage.py inspectdb` - Generate models from existing database
- `python manage.py dumpdata app_name` - Export data
- `python manage.py loaddata fixture.json` - Import data

## Talemo Project Structure

```
talemo/
├── manage.py                    # Django management script
├── config/                      # Project configuration
│   ├── __init__.py
│   ├── settings/               # Settings modules
│   │   ├── __init__.py
│   │   ├── base.py            # Base settings
│   │   └── dev.py             # Development settings
│   ├── urls.py                # Main URL configuration
│   ├── public_urls.py         # Public URL routing
│   ├── wsgi.py                # WSGI configuration
│   ├── asgi.py                # ASGI configuration
│   └── celery.py              # Celery configuration
├── talemo/                     # Main application package
│   ├── __init__.py
│   ├── stories/               # Story management app
│   │   ├── models/            # Story and Chapter models
│   │   ├── ai_crew.py         # AI story generation
│   │   ├── services.py        # Business logic
│   │   └── tasks.py           # Celery tasks
│   ├── audiostream/           # Audio streaming app
│   │   ├── hls.py             # HLS streaming
│   │   ├── tts.py             # Text-to-speech
│   │   ├── pipeline.py        # Audio processing
│   │   └── llm.py             # LLM integration
│   └── agents/                # AI agents (CrewAI)
│       └── crew/              # Agent configurations
├── frontend/                  # Frontend assets
│   └── templates/             # Django templates
├── static/                    # Static files
├── media/                     # User uploads
│   └── hls/                   # HLS stream files
├── docker/                    # Docker configs
│   ├── Dockerfile.dev
│   └── docker-compose.dev.yml
└── requirements/              # Dependency files
    ├── requirements-base.txt
    ├── requirements-web.txt
    ├── requirements-ai.txt
    ├── requirements-celery.txt
    └── requirements-dev.txt
```

## Django Settings Configuration

### Base Settings (config/settings/base.py)
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_spectacular',
    'django_extensions',
    'django_filters',
    'storages',
]

LOCAL_APPS = [
    'talemo.stories',
    'talemo.audiostream',
    'talemo.agents',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Database - PostgreSQL with pgvector extension
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'talemo'),
        'USER': os.environ.get('DB_USER', 'talemo'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 30,
        }
    }
}

# Celery Configuration
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# MinIO/S3 Storage Configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('MINIO_ROOT_USER', 'minioadmin')
AWS_SECRET_ACCESS_KEY = os.environ.get('MINIO_ROOT_PASSWORD', 'minioadmin')
AWS_STORAGE_BUCKET_NAME = os.environ.get('MINIO_BUCKET', 'talemo')
AWS_S3_ENDPOINT_URL = os.environ.get('MINIO_URL', 'http://minio:9000')
AWS_S3_USE_SSL = False
AWS_S3_VERIFY = False

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Django Best Practices

### Models
- Use descriptive model names (singular)
- Add `__str__` methods for better admin interface
- Use `related_name` for foreign keys
- Implement `get_absolute_url` method
- Add proper Meta class with ordering

### Views
- Use class-based views for complex logic
- Implement proper error handling
- Add pagination for list views
- Use `select_related` and `prefetch_related` for optimization
- Implement proper permission checks

### URLs
- Use app namespaces
- Use descriptive URL names
- Group related URLs in separate files
- Use slug fields for SEO-friendly URLs

### Templates
- Extend base templates
- Use template inheritance effectively
- Create reusable template tags
- Implement proper CSRF protection
- Use Django's built-in template filters

### Forms
- Use Django forms for validation
- Implement custom form validation
- Use ModelForms when appropriate
- Add proper error handling
- Implement CSRF protection

## Security Considerations

### Django Security Settings
```python
# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### User Authentication
- Use Django's built-in authentication
- Implement proper password policies
- Add two-factor authentication if needed
- Use Django's permission system
- Implement proper session management

## Testing Strategy

### Test Organization
```python
# tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.blog.models import Post

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(str(post), 'Test Post')
```

### Test Types
- **Unit tests** for models and utilities
- **Integration tests** for views and forms
- **Functional tests** for user workflows
- **API tests** for REST endpoints

## Deployment Considerations

### Production Settings
- Use environment variables for sensitive data
- Configure proper logging
- Set up static file serving
- Configure database connection pooling
- Implement proper caching strategy

### Docker Configuration
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
```

## Performance Optimization

### Database Optimization
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for many-to-many
- Add database indexes for frequent queries
- Implement database connection pooling
- Use database query optimization tools

### Caching Strategy
- Implement Redis/Memcached for session storage
- Use template fragment caching
- Implement view-level caching
- Add database query caching
- Use CDN for static files

## Common Django Patterns

### Custom User Model
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
```

### Custom Managers
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='draft')
    
    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager
```

## Talemo Dependencies & Tools

### Core Dependencies
- **Django 4.2+** - Web framework
- **PostgreSQL with pgvector** - Database with vector search
- **Redis** - Caching and message broker
- **MinIO** - S3-compatible object storage
- **Celery** - Asynchronous task processing
- **Docker & Docker Compose** - Development environment

### AI & Audio Processing
- **CrewAI** - AI agent framework for story generation
- **LlamaIndex** - RAG pipeline for context retrieval
- **litellm** - Unified LLM interface
- **gTTS** - Google Text-to-Speech
- **FFmpeg** - Audio/video processing (for HLS)

### API & Documentation
- **Django REST Framework** - RESTful API
- **drf-spectacular** - OpenAPI/Swagger documentation
- **django-filter** - API filtering

### Development Tools
- **pytest** - Testing framework
- **black** - Code formatter
- **flake8** - Linter
- **mypy** - Type checker
- **django-debug-toolbar** - Debug panel
- **factory-boy** - Test fixtures
- **coverage** - Code coverage

## Talemo-Specific Commands

### Celery Management
- `make celery-up` - Start Celery worker
- `make celery-logs` - View Celery logs
- `make flower` - Open Flower monitoring UI

### Testing
- `make test` - Run all tests
- `make test-unit` - Run unit tests only
- `make test-integration` - Run integration tests
- `make coverage` - Generate coverage report

### Database Operations
- `make migrate` - Apply migrations
- `make migrations` - Create new migrations
- `make dbshell` - Access PostgreSQL shell
- `make reset-db` - Reset database (WARNING: destroys data)

### Code Quality
- `make lint` - Run flake8 linter
- `make format` - Format code with black
- `make type-check` - Run mypy type checker
- `make pre-commit` - Run all pre-commit hooks

## Environment Variables

### Required
- `SECRET_KEY` - Django secret key
- `DB_NAME` - PostgreSQL database name
- `DB_USER` - PostgreSQL username
- `DB_PASSWORD` - PostgreSQL password

### Optional with Defaults
- `DB_HOST` - Database host (default: 'db')
- `DB_PORT` - Database port (default: '5432')
- `REDIS_URL` - Redis connection URL (default: 'redis://redis:6379/0')
- `MINIO_URL` - MinIO endpoint (default: 'http://minio:9000')
- `MINIO_ROOT_USER` - MinIO access key (default: 'minioadmin')
- `MINIO_ROOT_PASSWORD` - MinIO secret key (default: 'minioadmin')
- `MINIO_BUCKET` - MinIO bucket name (default: 'talemo')

### AI Configuration
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key (optional)
- `LANGFUSE_SECRET_KEY` - Langfuse tracking (optional)
- `LANGFUSE_PUBLIC_KEY` - Langfuse public key (optional)