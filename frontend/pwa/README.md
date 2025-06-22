# Progressive Web App Configuration

This directory contains configuration files for the Progressive Web App (PWA) functionality of the Talemo platform.

## Overview

Progressive Web Apps provide a native app-like experience on the web, allowing users to install the application on their devices, access it offline, and receive push notifications. This is particularly important for Talemo as a mobile-first platform for families.

## Expected Files

The following files will be added to this directory during implementation:

- `manifest.json`: Web app manifest that defines how the app appears when installed on a device
- `service-worker.js`: Service worker script for offline functionality and caching
- `offline.html`: Fallback page displayed when the user is offline
- `icons/`: Directory containing app icons in various sizes for different devices

## Implementation Details

### Web App Manifest

The `manifest.json` file will include:

```json
{
  "name": "Talemo - Family Audio Stories",
  "short_name": "Talemo",
  "description": "Discover, listen to, and co-create short audio stories for families",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#5c6bc0",
  "icons": [
    {
      "src": "/static/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### Service Worker

The service worker will be implemented using Workbox, a set of libraries and tools that make it easier to build PWAs. It will handle:

- Caching of static assets
- Caching of API responses
- Offline fallback pages
- Background sync for offline actions
- Push notifications

Example service worker configuration:

```javascript
importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.1.5/workbox-sw.js');

workbox.routing.registerRoute(
  ({request}) => request.destination === 'image',
  new workbox.strategies.CacheFirst({
    cacheName: 'images',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
      }),
    ],
  })
);

workbox.routing.registerRoute(
  ({request}) => request.destination === 'script' ||
                 request.destination === 'style',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'static-resources',
  })
);

// Offline fallback
workbox.routing.registerRoute(
  ({request}) => request.mode === 'navigate',
  async () => {
    try {
      return await workbox.strategies.NetworkFirst().handle(arguments);
    } catch (error) {
      return caches.match('/offline.html');
    }
  }
);
```

## Integration with Django

The PWA functionality will be integrated with Django using the following approach:

1. Link to the manifest in the base template:
   ```html
   <link rel="manifest" href="{% static 'pwa/manifest.json' %}">
   ```

2. Register the service worker in the base template:
   ```html
   <script>
     if ('serviceWorker' in navigator) {
       window.addEventListener('load', () => {
         navigator.serviceWorker.register('/service-worker.js');
       });
     }
   </script>
   ```

3. Configure Django URLs to serve the service worker from the root path

## Testing PWA Functionality

To test the PWA functionality:

1. Use Chrome DevTools' Lighthouse to audit PWA features
2. Test offline functionality by disabling network in DevTools
3. Test installation on various devices (Android, iOS)
4. Verify push notifications work correctly

## Related Documentation

- [Web App Manifest Specification](https://developer.mozilla.org/en-US/docs/Web/Manifest)
- [Service Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Workbox Documentation](https://developers.google.com/web/tools/workbox)
- [PWA Checklist](https://web.dev/pwa-checklist/)