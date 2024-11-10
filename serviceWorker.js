const staticPhoneStore = "phone-store-site-v1"; // Versioned cache name

const assets = [
  "/static/css/styles.css",
  "/static/js/script.js",
  "/manifest.json"
];

self.addEventListener("install", installEvent => {
  installEvent.waitUntil(
    caches.open(staticPhoneStore).then(cache => {
      return cache.addAll(assets).catch(error => {
        console.error("Failed to cache assets:", error);
      });
    })
  );
});

self.addEventListener("fetch", fetchEvent => {
  fetchEvent.respondWith(
    caches.match(fetchEvent.request).then(res => {
      if (res) {
        return res;
      }
      return fetch(fetchEvent.request).catch(() => {
        if (fetchEvent.request.url.includes('/images/')) {
          return caches.match('/images/fallback.jpg');
        }
      });
    })
  );
});
