# Agent Templates

This directory contains HTML templates for the agent-related views in the Talemo platform. These templates provide the user interface for interacting with AI agents that generate and enhance stories.

## Overview

The agent templates allow users to interact with the CrewAI-powered agents that are responsible for story creation, illustration description generation, and narration script creation.

## File Structure

- `index.html`: Main landing page for the agents section
- `playground.html`: Interactive playground for testing and experimenting with agents

## Template Details

### index.html

The `index.html` template serves as the main landing page for the agents section. It provides:

- An overview of available agents
- Links to the agent playground
- Information about agent capabilities

This template extends the base template and uses Bootstrap for layout and styling.

### playground.html

The `playground.html` template provides an interactive interface for testing and experimenting with agents. It includes:

- Agent selection dropdown
- Input form for providing prompts or existing stories
- Output display area for agent results
- Real-time status updates during agent processing

This template uses HTMX for asynchronous communication with the agent API endpoints and Alpine.js for managing the UI state.

## Integration with Backend

The agent templates interact with the backend through several API endpoints:

- `/api/v1/agents/generate-story/`: For generating new stories
- `/api/v1/agents/enhance-story/`: For enhancing existing stories
- `/api/v1/agents/task-status/<task_id>/`: For checking the status of agent tasks

These endpoints are called asynchronously using HTMX, and the results are displayed in the UI without requiring a full page reload.

## Usage Example

The playground template allows users to:

1. Select an agent type (story creation or story enhancement)
2. Provide input (prompt for new stories or existing story for enhancement)
3. Submit the request to the appropriate API endpoint
4. View real-time status updates during processing
5. See the results when the agent task completes

Example HTMX interaction:

```html
<button hx-post="/api/v1/agents/generate-story/"
        hx-trigger="click"
        hx-target="#result-container"
        hx-swap="innerHTML"
        hx-indicator="#loading-indicator">
  Generate Story
</button>

<div id="loading-indicator" class="htmx-indicator">
  Processing...
</div>

<div id="result-container">
  <!-- Results will appear here -->
</div>
```

## Styling

The agent templates use Bootstrap 5 for styling, with custom components for:

- Agent cards
- Input forms
- Result displays
- Status indicators

## JavaScript Functionality

The templates include JavaScript functionality for:

- Form validation
- Dynamic form field toggling based on agent type
- Polling for task status updates
- Formatting and displaying agent results

## Related Components

- `talemo/agents/views.py`: Backend views that handle agent requests
- `talemo/agents/tasks.py`: Celery tasks for asynchronous agent processing
- `talemo/agents/crew/`: CrewAI integration for agent functionality

## Best Practices

When modifying these templates:

- Maintain the responsive design for mobile and desktop
- Keep JavaScript functionality minimal and focused
- Use HTMX for dynamic interactions
- Ensure accessibility for all users
- Test with different agent inputs and outputs

## Related Documentation

- [CrewAI Documentation](https://docs.crewai.com/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Alpine.js Documentation](https://alpinejs.dev/start-here)