/* The Wonder Ship — offline cache.
   The shell holds the library; each book is a chunk fetched on first open.
   Everything already released is precached, so the whole year works with no
   network once the app has been opened one time. */
var CACHE = 'wondership-v2';
var ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon.svg",
  "./books/01.js",
  "./books/02.js",
  "./books/03.js",
  "./books/04.js",
  "./books/05.js",
  "./books/06.js",
  "./books/07.js",
  "./books/08.js",
  "./books/09.js",
  "./books/10.js",
  "./books/11.js",
  "./books/12.js",
  "./books/13.js"
];

self.addEventListener('install', function (e) {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(function (c) {
    return Promise.all(ASSETS.map(function (u) {
      return c.add(u).catch(function () { /* a missing chunk must not fail install */ });
    }));
  }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; })
                           .map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(function (hit) {
      if (hit) return hit;
      return fetch(e.request).then(function (res) {
        if (res && res.status === 200 && res.type === 'basic') {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
        }
        return res;
      }).catch(function () {
        return e.request.mode === 'navigate' ? caches.match('./index.html') : undefined;
      });
    })
  );
});
