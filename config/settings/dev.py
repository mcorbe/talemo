"""
Development settings for config project.
"""
import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-7dbq8%y^m^u6na#nxpza1@*j=lhnp(++-ccuw)3uem5j969-$2")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(",")

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": os.environ.get("DB_NAME", "talemo"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# MinIO Storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Ensure static files are properly served in development
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "frontend" / "static"]

AWS_ACCESS_KEY_ID = os.environ.get("MINIO_ROOT_USER", "minioadmin")
AWS_SECRET_ACCESS_KEY = os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin")
AWS_STORAGE_BUCKET_NAME = os.environ.get("MINIO_BUCKET", "talemo")
AWS_S3_ENDPOINT_URL = f"http://{os.environ.get('MINIO_ENDPOINT', 'localhost:9000')}"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "mailhog")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "1025"))
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = "noreply@talemo.local"

# Debug Toolbar
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    # Ensure TenantMainMiddleware remains at the beginning
    tenant_middleware = MIDDLEWARE[0]
    MIDDLEWARE = [tenant_middleware, "debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE[1:]
    INTERNAL_IPS = ["127.0.0.1"]

# Celery
CELERY_TASK_ALWAYS_EAGER = True

# AI Services
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY", "")

# Observability
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")
LANGTRACE_ENABLED = os.environ.get("LANGTRACE_ENABLED", "False") == "True"
LANGTRACE_HOST = os.environ.get("LANGTRACE_HOST", "https://cloud.langfuse.com")
