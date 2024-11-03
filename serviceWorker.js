//----------------------------------------------------//
//  serviceWorker.js
//  JavaScript file, script that runs seperate from webpage
//  ServiceWorker
//----------------------------------------------------//

// Caching System, used to store assets
const staticPhoneStore = "phone-store-site-v1"

const assets = [
  "/",
  "/index.html",
  "/css/style.css",
  "/js/app.js",
  "/images/phone1.jpg",
  "/images/phone2.jpg",
  "/images/phone3.jpg",
  "/images/phone4.jpg",
  "/images/phone5.jpg",
  "/images/phone6.jpg",
  "/images/phone7.jpg",
  "/images/phone8.jpg",
  "/images/phone9.jpg",
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

  // Register serviceWorker, allows to install web app
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function() {
      navigator.serviceWorker
        .register("/serviceWorker.js")
        .then(res => console.log("service worker registered"))
        .catch(err => console.log("service worker not registered", err))
    })
  }