# Frontend Assets

This directory contains all frontend-related assets for the Talemo project, including templates, static files, and Progressive Web App (PWA) configuration.

## Overview

The frontend of Talemo is built using a combination of Django templates, HTMX for dynamic interactions, Bootstrap 5 for styling, and Alpine.js for lightweight JavaScript functionality. The application is designed as a Progressive Web App (PWA) to provide offline capabilities and a mobile-first experience.

## Directory Structure

- `templates/`: HTML templates organized by app
- `static/`: Static assets (CSS, JavaScript, images, fonts)
- `pwa/`: Progressive Web App configuration and service worker

## Technology Stack

- **HTMX**: For dynamic interactions without full page reloads
- **Bootstrap 5**: For responsive design and UI components
- **Alpine.js**: For lightweight JavaScript functionality
- **Workbox**: For service worker and PWA capabilities
- **Howler.js**: For audio playback
- **Chart.js**: For data visualization

## Templates

The `templates/` directory contains HTML templates organized by app. The templates follow a hierarchical structure:

- Base templates that define the overall layout
- App-specific templates that extend the base templates
- Partial templates for reusable components

Templates use Django's template language for server-side rendering and HTMX for client-side interactions.

## Static Assets

The `static/` directory contains static assets organized by type:

- `css/`: Stylesheets, including custom styles and Bootstrap
- `js/`: JavaScript files, including custom scripts and libraries
- `images/`: Image assets
- `fonts/`: Font files
- `icons/`: Icon assets for the PWA

## Progressive Web App

The `pwa/` directory contains configuration for the Progressive Web App:

- Service worker implementation using Workbox
- Manifest file for app installation
- Offline fallback pages
- Cache strategies for different types of assets

## Development Workflow

### Adding New Templates

1. Create templates in the appropriate app subdirectory
2. Extend the base template using `{% extends "base.html" %}`
3. Define blocks for content, title, extra CSS, and extra JavaScript

Example:
```html
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
  <!-- Page content here -->
{% endblock %}

{% block extra_css %}
  <link rel="stylesheet" href="{% static 'css/page-specific.css' %}">
{% endblock %}

{% block extra_js %}
  <script src="{% static 'js/page-specific.js' %}"></script>
{% endblock %}
```

### Adding Static Assets

1. Place assets in the appropriate subdirectory
2. Reference them in templates using the `{% static %}` template tag

Example:
```html
<img src="{% static 'images/logo.png' %}" alt="Logo">
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
<script src="{% static 'js/script.js' %}"></script>
```

### PWA Development

1. Update the service worker configuration in `pwa/service-worker.js`
2. Modify the manifest file in `pwa/manifest.json`
3. Test PWA functionality using Lighthouse in Chrome DevTools

## Best Practices

- Follow mobile-first design principles
- Optimize assets for performance (minify, compress)
- Use HTMX for dynamic interactions instead of heavy JavaScript
- Implement proper caching strategies for offline functionality
- Ensure accessibility compliance (WCAG 2.1 AA)
- Test on multiple devices and browsers

## Related Documentation

- [Django Templates](https://docs.djangoproject.com/en/4.2/topics/templates/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- [Alpine.js Documentation](https://alpinejs.dev/start-here)
- [Workbox Documentation](https://developers.google.com/web/tools/workbox)