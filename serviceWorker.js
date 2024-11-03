//----------------------------------------------------//
//  serviceWorker.js
//  JavaScript file, script that runs seperate from webpage
//  ServiceWorker
//----------------------------------------------------//

// Caching System, used to store assets
const staticPhoneStore = "phone-store-site-v1"

const assets = [
  "/",
  "/index.html"
]

// runs immediately after installation: sets up resources needed right away
self.addEventListener("install", installEvent => {
  installEvent.waitUntil(
    caches.open(staticPhoneStore).then(cache => {
      cache.addAll(assets)
    })
  )
})

// requesting information 
self.addEventListener("fetch", fetchEvent => {
    fetchEvent.respondWith(
      caches.match(fetchEvent.request).then(res => {
        return res || fetch(fetchEvent.request)
      })
    )
  })

  