# Static Assets

This directory contains static assets for the Talemo platform, including CSS, JavaScript, images, fonts, and icons.

## Overview

Static assets are files that are served directly to the client without being processed by Django. These include stylesheets, JavaScript files, images, and other media that enhance the user interface and experience of the application.

## Expected Directory Structure

The static assets will be organized into the following subdirectories:

- `css/`: Stylesheets
  - `base.css`: Base styles for the entire application
  - `components/`: CSS for reusable components
  - `pages/`: Page-specific styles
- `js/`: JavaScript files
  - `app.js`: Main application JavaScript
  - `components/`: JavaScript for reusable components
  - `utils/`: Utility functions
  - `vendors/`: Third-party libraries
- `images/`: Image assets
  - `backgrounds/`: Background images
  - `illustrations/`: Illustrations for stories
  - `logos/`: Logo variations
  - `ui/`: UI-related images
- `fonts/`: Font files
- `icons/`: Icon assets
  - `app-icons/`: Icons for PWA installation
  - `ui-icons/`: Icons used in the UI

## CSS Architecture

The CSS follows a component-based architecture with the following principles:

- Use of Bootstrap 5 as the foundation
- Custom components built on top of Bootstrap
- Mobile-first approach
- BEM (Block Element Modifier) naming convention
- CSS variables for theming

Example of BEM naming convention:
```css
/* Block */
.story-card {
  background-color: var(--color-background);
  border-radius: 8px;
}

/* Element */
.story-card__title {
  font-size: 1.25rem;
  color: var(--color-text-primary);
}

/* Modifier */
.story-card--featured {
  border: 2px solid var(--color-primary);
}
```

## JavaScript Architecture

The JavaScript follows a modular approach:

- Alpine.js for lightweight interactivity
- HTMX for dynamic content loading
- Minimal custom JavaScript
- ES6 modules for organization

Example of a JavaScript module:
```javascript
// js/components/audio-player.js
export default {
  init() {
    // Initialize audio player
  },
  play(audioUrl) {
    // Play audio
  },
  pause() {
    // Pause audio
  }
};
```

## Image Guidelines

- Use SVG for icons and simple illustrations
- Use WebP with JPEG/PNG fallbacks for photos
- Optimize all images for web
- Provide multiple sizes for responsive images
- Include alt text in HTML

## Asset Compilation

During development, static assets are served directly from this directory. In production, they are collected, processed, and served from a CDN or the configured static files storage.

The asset compilation process includes:

1. Collecting all static files using Django's `collectstatic` command
2. Minifying CSS and JavaScript
3. Optimizing images
4. Adding cache-busting hashes to filenames
5. Uploading to the configured storage backend (e.g., MinIO/S3)

## Usage in Templates

Static assets are referenced in templates using the `{% static %}` template tag:

```html
{% load static %}

<link rel="stylesheet" href="{% static 'css/base.css' %}">
<script src="{% static 'js/app.js' %}"></script>
<img src="{% static 'images/logos/logo.svg' %}" alt="Talemo Logo">
```

## Best Practices

- Keep file sizes small for better performance
- Use appropriate file formats for each asset type
- Organize files logically by type and purpose
- Use descriptive filenames
- Minimize HTTP requests by combining files where appropriate
- Implement proper caching strategies

## Related Documentation

- [Django Static Files](https://docs.djangoproject.com/en/4.2/howto/static-files/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- [BEM Naming Convention](http://getbem.com/naming/)
- [Web Performance Optimization](https://web.dev/fast/)