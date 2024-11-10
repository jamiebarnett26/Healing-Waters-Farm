//----------------------------------------------------//
//  serviceWorker.js
//  JavaScript file, script that runs seperate from webpage
//  ServiceWorker
//----------------------------------------------------//

// Caching System, used to store assets
const staticPhoneStore = "phone-store-site-v1";

const assets = [
  '/',
];

// runs immediately after installation: sets up resources needed right away
self.addEventListener("install", function(installEvent) {
    console.log("WE ARE IN THE EVENTLISTENER!");
  installEvent.waitUntil(
    caches.open(staticPhoneStore).then(function(cache) {
      return cache.addAll(assets);
    })
  );
});

self.addEventListener('activate', function(e) {
  console.log('[ServiceWorker] Activate');
    e.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        if (key !== cacheName) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  return self.clients.claim();
});

// requesting information 
self.addEventListener("fetch", fetchEvent => {
    fetchEvent.respondWith(
      caches.match(fetchEvent.request).then(res => {
        return res || fetch(fetchEvent.request)
      })
    )
  })

  