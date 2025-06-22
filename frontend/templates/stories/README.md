# Story Templates

This directory contains HTML templates for the story-related views in the Talemo platform. These templates provide the user interface for discovering, listening to, and co-creating audio stories.

## Overview

The story templates are the core user-facing components of the Talemo platform, allowing families to interact with audio stories. These templates support the primary functions of browsing, playing, and creating stories.

## File Structure

- `index.html`: Main landing page for the stories section

## Template Details

### index.html

The `index.html` template serves as the main landing page for the stories section. It provides:

- Featured stories carousel
- Story browsing with filtering options
- Story creation entry point
- Recently played stories section

This template extends the base template and uses Bootstrap for layout and styling.

## Planned Templates

As the application develops, additional templates will be added:

- `detail.html`: Detailed view of a single story with playback controls
- `create.html`: Interface for creating new stories
- `edit.html`: Interface for editing existing stories
- `components/`: Directory for reusable story components
  - `story_card.html`: Card component for story listings
  - `audio_player.html`: Audio playback component
  - `illustration_viewer.html`: Component for viewing story illustrations

## Integration with Backend

The story templates interact with the backend through several API endpoints:

- `/api/v1/stories/`: For listing and creating stories
- `/api/v1/stories/<id>/`: For retrieving, updating, and deleting specific stories
- `/api/v1/stories/<id>/play/`: For playing a story
- `/api/v1/stories/<id>/illustrations/`: For retrieving story illustrations

These endpoints are called asynchronously using HTMX, and the results are displayed in the UI without requiring a full page reload.

## Story Playback

The story playback functionality includes:

- Audio streaming from MinIO storage
- Synchronized illustration display
- Playback controls (play, pause, seek)
- Progress tracking
- Offline playback support through PWA capabilities

## Story Creation

The story creation interface will allow users to:

1. Enter a story prompt or theme
2. Select age range and preferences
3. Submit the request to the agent system
4. View real-time creation progress
5. Preview and edit the generated story
6. Save and publish the final story

## Mobile-First Design

The story templates follow a mobile-first design approach:

- Touch-friendly controls
- Responsive layouts
- Optimized for various screen sizes
- Minimal data usage for mobile networks

## Accessibility Features

The templates include accessibility features:

- Proper heading structure
- ARIA attributes for interactive elements
- Keyboard navigation support
- Screen reader compatibility
- Transcripts for audio content

## Usage Example

Example HTMX interaction for story playback:

```html
<div class="story-card" hx-get="/api/v1/stories/{{ story.id }}/"
     hx-target="#story-detail"
     hx-trigger="click"
     hx-swap="innerHTML">
  <h3>{{ story.title }}</h3>
  <p>{{ story.description|truncatechars:100 }}</p>
  <span class="badge bg-primary">{{ story.age_range }}</span>
</div>

<div id="story-detail">
  <!-- Story detail will be loaded here -->
</div>
```

## Related Components

- `talemo/stories/views.py`: Backend views that handle story requests
- `talemo/stories/models.py`: Story data models
- `talemo/agents/crew/story_crew.py`: CrewAI integration for story generation

## Best Practices

When modifying these templates:

- Maintain the responsive design for mobile and desktop
- Keep JavaScript functionality minimal and focused
- Use HTMX for dynamic interactions
- Ensure accessibility for all users
- Optimize audio and image loading for performance

## Related Documentation

- [Django Templates](https://docs.djangoproject.com/en/4.2/topics/templates/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Howler.js Documentation](https://howlerjs.com/) (for audio playback)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/)