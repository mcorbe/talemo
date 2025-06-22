# Integration Tests

This directory contains integration tests for the Talemo platform. Integration tests verify that different components of the application work together correctly.

## Overview

Integration tests focus on testing the interactions between different components of the system. Unlike unit tests, which test components in isolation, integration tests verify that components integrate properly and work together as expected.

## Directory Structure

Integration tests are organized by feature or API endpoint:

```
integration/
├── api/                # Tests for API endpoints
│   ├── test_stories_api.py
│   ├── test_agents_api.py
│   └── test_assets_api.py
├── auth/               # Tests for authentication
├── tenant/             # Tests for multi-tenant functionality
└── workflows/          # Tests for complete workflows
```

## Writing Integration Tests

### Test File Naming

Integration test files should follow the naming convention:

```
test_<feature_or_endpoint>.py
```

For example:
- `test_stories_api.py` - Tests for the stories API endpoints
- `test_agent_workflow.py` - Tests for agent workflows
- `test_tenant_isolation.py` - Tests for tenant data isolation

### Test Case Structure

Integration tests typically use the Django test client or REST framework's APIClient to make requests to the application:

```python
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestStoriesAPI:
    def setup_method(self):
        self.client = APIClient()
        # Set up test data
        
    def test_list_stories(self):
        """Test that the stories API returns a list of stories."""
        response = self.client.get('/api/v1/stories/')
        assert response.status_code == 200
        assert 'results' in response.data
        
    def test_create_story(self):
        """Test that a story can be created through the API."""
        data = {
            'title': 'Test Story',
            'content': 'This is a test story.',
            'age_range': '4-8'
        }
        response = self.client.post('/api/v1/stories/', data)
        assert response.status_code == 201
        assert response.data['title'] == 'Test Story'
```

### Testing API Endpoints

When testing API endpoints, verify:
- Response status codes
- Response data structure
- Authentication and authorization
- Error handling
- Pagination
- Filtering and sorting

Example:

```python
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestStoriesAPIAuthentication:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
    def test_authentication_required(self):
        """Test that authentication is required to access the API."""
        # Unauthenticated request
        response = self.client.get('/api/v1/stories/')
        assert response.status_code == 401
        
        # Authenticated request
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/stories/')
        assert response.status_code == 200
```

### Testing Multi-Tenant Functionality

For multi-tenant applications, test data isolation between tenants:

```python
import pytest
from rest_framework.test import APIClient
from talemo.core.models import Tenant
from talemo.stories.models import Story

@pytest.mark.django_db
class TestTenantIsolation:
    def setup_method(self):
        self.client = APIClient()
        
        # Create two tenants
        self.tenant1 = Tenant.objects.create(name='Tenant 1', schema_name='tenant1')
        self.tenant2 = Tenant.objects.create(name='Tenant 2', schema_name='tenant2')
        
        # Create stories for each tenant
        with tenant_context(self.tenant1):
            Story.objects.create(title='Tenant 1 Story')
            
        with tenant_context(self.tenant2):
            Story.objects.create(title='Tenant 2 Story')
    
    def test_tenant_isolation(self):
        """Test that tenants can only see their own stories."""
        # Set tenant context to tenant1
        self.client.headers.update({'X-Tenant-ID': 'tenant1'})
        response = self.client.get('/api/v1/stories/')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Tenant 1 Story'
        
        # Set tenant context to tenant2
        self.client.headers.update({'X-Tenant-ID': 'tenant2'})
        response = self.client.get('/api/v1/stories/')
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Tenant 2 Story'
```

## Running Integration Tests

To run all integration tests:

```bash
make test-integration
```

Or using Docker Compose directly:

```bash
docker-compose -f docker/docker-compose.dev.yml exec web pytest tests/integration/
```

To run a specific test file:

```bash
docker-compose -f docker/docker-compose.dev.yml exec web pytest tests/integration/api/test_stories_api.py
```

## Best Practices

- **Focus on component interactions**: Test how components work together, not individual component behavior.
- **Use realistic test data**: Create test data that resembles real-world scenarios.
- **Test API contracts**: Verify that API endpoints adhere to their contracts.
- **Test error handling**: Verify that the application handles errors gracefully.
- **Test authentication and authorization**: Verify that access controls work correctly.
- **Clean up test data**: Ensure tests clean up after themselves to avoid affecting other tests.
- **Use fixtures for common setup**: Use pytest fixtures for common setup tasks.

## Related Documentation

- [pytest Documentation](https://docs.pytest.org/)
- [Django Testing Tools](https://docs.djangoproject.com/en/4.2/topics/testing/tools/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)