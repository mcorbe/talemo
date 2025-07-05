// Talemo Service Worker
importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.5.4/workbox-sw.js');

// Set workbox config
workbox.setConfig({
  debug: false
});

// Cache static assets
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

// Cache CSS and JS
workbox.routing.registerRoute(
  ({request}) => request.destination === 'script' || request.destination === 'style',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'static-resources',
  })
);

// Cache audio files
workbox.routing.registerRoute(
  ({request}) => request.destination === 'audio',
  new workbox.strategies.CacheFirst({
    cacheName: 'audio-files',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 30,
        maxAgeSeconds: 7 * 24 * 60 * 60, // 7 Days
      }),
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// Cache API responses
workbox.routing.registerRoute(
  ({url}) => url.pathname.startsWith('/api/'),
  new workbox.strategies.NetworkFirst({
    cacheName: 'api-responses',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 24 * 60 * 60, // 1 Day
      }),
    ],
  })
);

// Offline fallback
workbox.routing.registerRoute(
  ({request}) => request.mode === 'navigate',
  async ({event}) => {
    try {
      return await workbox.strategies.NetworkFirst({
        cacheName: 'pages',
        plugins: [
          new workbox.expiration.ExpirationPlugin({
            maxEntries: 25,
            maxAgeSeconds: 24 * 60 * 60, // 1 Day
          }),
        ],
      }).handle({event});
    } catch (error) {
      return caches.match('/offline.html');
    }
  }
);

// Background sync for offline actions
workbox.backgroundSync.registerPlugin(
  'offline-story-interactions',
  {
    maxRetentionTime: 24 * 60, // Retry for up to 24 hours (specified in minutes)
    onSync: async ({queue}) => {
      let entry;
      while ((entry = await queue.shiftRequest())) {
        try {
          await fetch(entry.request);
          console.log('Replay successful for request', entry.request);
        } catch (error) {
          console.error('Replay failed for request', entry.request, error);
          await queue.unshiftRequest(entry);
          return;
        }
      }
      console.log('Background sync complete!');
    }
  }
);

// Cache the Google Fonts stylesheets with a stale-while-revalidate strategy.
workbox.routing.registerRoute(
  /^https:\/\/fonts\.googleapis\.com/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'google-fonts-stylesheets',
  })
);

// Cache the underlying font files with a cache-first strategy for 1 year.
workbox.routing.registerRoute(
  /^https:\/\/fonts\.gstatic\.com/,
  new workbox.strategies.CacheFirst({
    cacheName: 'google-fonts-webfonts',
    plugins: [
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new workbox.expiration.ExpirationPlugin({
        maxAgeSeconds: 60 * 60 * 24 * 365, // 1 year
        maxEntries: 30,
      }),
    ],
  })
);

// Skip waiting and claim clients
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim());
});