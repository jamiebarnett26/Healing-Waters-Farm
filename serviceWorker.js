const staticPhoneStore = "phone-store-site-v1"; 

const assets = [
  "/static/css/styles.css",
  "/static/css/checkbox.css",
  "/static/js/script.js",
  "/manifest.json",
  "/homepage"       
];

self.addEventListener("install", installEvent => {
  installEvent.waitUntil(
    caches.open(staticPhoneStore).then(async (cache) => {
      try {
        for (const asset of assets) {
          await cache.add(asset);  // Attempt to cache each asset individually
          console.log(`Successfully cached: ${asset}`);  // Log successful caching
        }
      } catch (error) {
        console.error(`Failed to cache asset:`, error);  // Log which asset failed
      }
    })
  );
});

self.addEventListener("fetch", (fetchEvent) => {
  console.log('Fetch request for:', fetchEvent.request.url);  // Debug log

  if (fetchEvent.request.url.includes('/homepage')) {
    fetchEvent.respondWith(
      fetch(fetchEvent.request).then((networkResponse) => {
        caches.open(staticPhoneStore).then((cache) => {
          cache.put(fetchEvent.request, networkResponse);
        });
        return networkResponse;  
      }).catch(() => {
        return caches.match(fetchEvent.request);
      })
    );
  } else {
    fetchEvent.respondWith(
      caches.match(fetchEvent.request).then((res) => {
        if (res) {
          return res; 
        }

        return fetch(fetchEvent.request).catch(() => {
          return caches.match('/offline.html');
        });
      }).catch((err) => {
        console.error('Error in fetching:', err);
        return caches.match('/offline.html'); 
      })
    );
  }
});


self.addEventListener('activate', (event) => {
  const currentCache = staticPhoneStore;
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== currentCache) {
            return caches.delete(cacheName); 
          }
        })
      );
    })
  );
});
