# Django Templates

This directory contains HTML templates for the Talemo platform. These templates define the structure and layout of the user interface.

## Overview

Talemo uses Django's template system combined with HTMX for dynamic interactions. The templates follow a hierarchical structure with a base template that defines the common layout and app-specific templates that extend it.

## Directory Structure

- `base.html`: The main base template that defines the overall layout
- `agents/`: Templates for agent-related views
- `assets/`: Templates for asset management views
- `stories/`: Templates for story-related views

## Base Template

The `base.html` file serves as the foundation for all pages in the application. It includes:

- HTML5 doctype and responsive viewport settings
- Common CSS and JavaScript includes
- Navigation bar
- Main content area (defined as a block)
- Footer
- HTMX and Alpine.js setup

Key blocks defined in the base template:

- `{% block title %}`: Page title
- `{% block content %}`: Main content area
- `{% block extra_css %}`: Additional CSS for specific pages
- `{% block extra_js %}`: Additional JavaScript for specific pages

## Template Inheritance

All app-specific templates extend the base template using Django's template inheritance:

```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
  <!-- Page-specific content here -->
{% endblock %}
```

## HTMX Integration

HTMX is used for dynamic interactions without full page reloads. Example usage:

```html
<button hx-get="/api/stories/{{ story.id }}"
        hx-target="#story-content"
        hx-trigger="click"
        hx-swap="innerHTML">
  Load Story
</button>

<div id="story-content">
  <!-- Content will be loaded here -->
</div>
```

## Alpine.js Integration

Alpine.js is used for lightweight JavaScript functionality:

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle Menu</button>
  
  <div x-show="open" x-transition>
    <!-- Menu content -->
  </div>
</div>
```

## Template Tags and Filters

Common custom template tags and filters used in templates:

- `{% load static %}`: For loading static files
- `{% url 'name' %}`: For generating URLs
- `{{ variable|filter }}`: For applying filters to variables

## Partial Templates

Reusable components are implemented as partial templates and included using:

```html
{% include "components/story_card.html" with story=story %}
```

## Mobile-First Approach

All templates follow a mobile-first approach using Bootstrap's responsive grid system:

```html
<div class="container">
  <div class="row">
    <div class="col-12 col-md-8">
      <!-- Content for small and medium+ screens -->
    </div>
    <div class="col-12 col-md-4">
      <!-- Sidebar for medium+ screens -->
    </div>
  </div>
</div>
```

## Accessibility

Templates are designed with accessibility in mind:

- Proper heading hierarchy (h1, h2, etc.)
- ARIA attributes where appropriate
- Sufficient color contrast
- Keyboard navigation support
- Screen reader friendly markup

## Best Practices

- Keep templates DRY (Don't Repeat Yourself) by using inheritance and includes
- Minimize logic in templates; use template tags and filters instead
- Use meaningful variable names
- Comment complex sections
- Maintain consistent indentation and formatting
- Separate structure (HTML), presentation (CSS), and behavior (JavaScript)

## Related Documentation

- [Django Templates](https://docs.djangoproject.com/en/4.2/topics/templates/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Alpine.js Documentation](https://alpinejs.dev/start-here)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/)