# Test Suite

This directory contains the test suite for the Talemo platform. The tests are organized by type to ensure comprehensive coverage of the application's functionality.

## Overview

The test suite is designed to validate the functionality, performance, and reliability of the Talemo platform. It includes different types of tests to cover various aspects of the application, from individual components to end-to-end user journeys.

## Test Types

The tests are organized into the following categories:

- `unit/`: Unit tests for individual components
- `integration/`: Integration tests for component interactions
- `e2e/`: End-to-end tests for complete user journeys
- `performance/`: Performance and load tests

## Unit Tests

Unit tests focus on testing individual components in isolation. They verify that each component behaves as expected and handles edge cases correctly. These tests are fast, isolated, and provide immediate feedback during development.

Key characteristics:
- Test individual functions, methods, and classes
- Mock external dependencies
- Focus on a single component's behavior
- Fast execution time

## Integration Tests

Integration tests verify that different components work together correctly. They test the interactions between components and ensure that they integrate properly.

Key characteristics:
- Test interactions between multiple components
- May involve database operations
- Verify API endpoints and service interactions
- More comprehensive than unit tests

## End-to-End Tests

End-to-end (E2E) tests validate complete user journeys from start to finish. They simulate real user interactions with the application and verify that the entire system works together correctly.

Key characteristics:
- Test complete user flows
- Interact with the application through the UI
- Verify that all components work together
- Slower execution time but more comprehensive coverage

## Performance Tests

Performance tests evaluate the system's responsiveness, stability, and resource usage under various conditions. They help identify bottlenecks and ensure the application meets performance requirements.

Key characteristics:
- Measure response times
- Test system behavior under load
- Identify performance bottlenecks
- Verify scalability

## Running Tests

### Running All Tests

To run all tests:

```bash
make test
```

Or using Docker Compose directly:

```bash
docker compose -f docker/docker-compose.dev.yml exec web pytest
```

### Running Specific Test Types

To run specific types of tests:

```bash
# Unit tests
make test-unit

# Integration tests
make test-integration

# E2E tests
docker compose -f docker/docker-compose.dev.yml exec web python manage.py cypress run

# Performance tests
docker compose -f docker/docker-compose.dev.yml exec web locust -f tests/performance/locustfile.py
```

### Running with Coverage

To run tests with coverage reporting:

```bash
make coverage
```

Or using Docker Compose directly:

```bash
docker compose -f docker/docker-compose.dev.yml exec web pytest --cov=talemo
```

## Test Configuration

The test configuration is defined in the following files:

- `pytest.ini`: Configuration for pytest
- `conftest.py`: Shared fixtures and configuration for pytest
- `tests/e2e/cypress.json`: Configuration for Cypress E2E tests
- `tests/performance/locust.conf`: Configuration for Locust performance tests

## Writing Tests

### Unit Test Example

```python
# tests/unit/test_story_model.py
import pytest
from talemo.stories.models import Story

@pytest.mark.django_db
def test_story_creation():
    story = Story.objects.create(
        title="Test Story",
        content="This is a test story.",
        age_range="4-8"
    )
    assert story.title == "Test Story"
    assert story.content == "This is a test story."
    assert story.age_range == "4-8"
```

### Integration Test Example

```python
# tests/integration/test_story_api.py
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_story_api_list(api_client, create_story):
    # Create test stories
    create_story(title="Story 1")
    create_story(title="Story 2")
    
    # Make API request
    response = api_client.get('/api/v1/stories/')
    
    # Verify response
    assert response.status_code == 200
    assert len(response.data['results']) == 2
```

## Best Practices

- Write tests before or alongside code (Test-Driven Development)
- Keep tests focused and isolated
- Use descriptive test names
- Use fixtures for common setup
- Mock external dependencies in unit tests
- Test edge cases and error conditions
- Maintain test independence (tests should not depend on each other)

## CI Integration

Tests are automatically run in the CI pipeline:
- Unit and integration tests on every pull request
- E2E tests on merge to main branch
- Performance tests on a scheduled basis

## Related Documentation

- [pytest Documentation](https://docs.pytest.org/)
- [Django Test Framework](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Cypress Documentation](https://docs.cypress.io/)
- [Locust Documentation](https://docs.locust.io/)