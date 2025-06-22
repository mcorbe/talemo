# Unit Tests

This directory contains unit tests for the Talemo platform. Unit tests focus on testing individual components in isolation to ensure they behave as expected.

## Overview

Unit tests are the foundation of the testing pyramid. They test individual functions, methods, and classes in isolation from the rest of the system. This approach allows for fast, focused testing of specific functionality and edge cases.

## Directory Structure

Unit tests are organized by application module to mirror the structure of the main codebase:

```
unit/
├── core/              # Tests for core functionality
├── stories/           # Tests for story-related functionality
├── agents/            # Tests for agent-related functionality
├── assets/            # Tests for asset management functionality
├── governance/        # Tests for governance functionality
└── subscriptions/     # Tests for subscription functionality
```

## Writing Unit Tests

### Test File Naming

Unit test files should follow the naming convention:

```
test_<module_name>.py
```

For example:
- `test_story_model.py` - Tests for the Story model
- `test_agent_service.py` - Tests for the agent service
- `test_tenant_middleware.py` - Tests for the tenant middleware

### Test Case Structure

Each test file should contain one or more test classes that inherit from `django.test.TestCase` or use pytest fixtures. Test methods should have descriptive names that explain what they're testing.

Example using pytest:

```python
import pytest
from talemo.stories.models import Story

@pytest.mark.django_db
class TestStoryModel:
    def test_story_creation(self):
        """Test that a story can be created with valid data."""
        story = Story.objects.create(
            title="Test Story",
            content="This is a test story.",
            age_range="4-8"
        )
        assert story.title == "Test Story"
        assert story.content == "This is a test story."
        assert story.age_range == "4-8"
    
    def test_story_str_representation(self):
        """Test the string representation of a story."""
        story = Story.objects.create(
            title="Test Story",
            content="This is a test story."
        )
        assert str(story) == "Test Story"
```

### Using Fixtures

Fixtures can be used to set up common test data:

```python
import pytest
from talemo.stories.models import Story

@pytest.fixture
def sample_story():
    return Story.objects.create(
        title="Sample Story",
        content="This is a sample story.",
        age_range="4-8"
    )

@pytest.mark.django_db
def test_story_update(sample_story):
    sample_story.title = "Updated Title"
    sample_story.save()
    
    updated_story = Story.objects.get(id=sample_story.id)
    assert updated_story.title == "Updated Title"
```

### Mocking

Use mocking to isolate the component being tested from its dependencies:

```python
import pytest
from unittest.mock import patch, MagicMock
from talemo.agents.services import StoryGenerationService

def test_story_generation_service():
    # Mock the OpenAI client
    with patch('talemo.agents.services.openai.OpenAI') as mock_openai:
        # Configure the mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = "Generated story content"
        
        # Create the service and call the method
        service = StoryGenerationService()
        result = service.generate_story("A story about a cat")
        
        # Assert the result
        assert "Generated story content" in result
        
        # Verify the mock was called correctly
        mock_client.chat.completions.create.assert_called_once()
```

## Running Unit Tests

To run all unit tests:

```bash
make test-unit
```

Or using Docker Compose directly:

```bash
docker-compose -f docker/docker-compose.dev.yml exec web pytest tests/unit/
```

To run a specific test file:

```bash
docker-compose -f docker/docker-compose.dev.yml exec web pytest tests/unit/test_story_model.py
```

To run a specific test:

```bash
docker-compose -f docker/docker-compose.dev.yml exec web pytest tests/unit/test_story_model.py::TestStoryModel::test_story_creation
```

## Best Practices

- **Test one thing per test**: Each test should focus on testing a single aspect of the component.
- **Use descriptive test names**: Test names should describe what the test is checking.
- **Keep tests independent**: Tests should not depend on each other or on the order in which they're run.
- **Mock external dependencies**: Use mocking to isolate the component being tested.
- **Test edge cases**: Include tests for edge cases and error conditions.
- **Keep tests fast**: Unit tests should run quickly to provide immediate feedback.
- **Use assertions effectively**: Make assertions specific and include helpful error messages.

## Related Documentation

- [pytest Documentation](https://docs.pytest.org/)
- [Django Testing Tools](https://docs.djangoproject.com/en/4.2/topics/testing/tools/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)