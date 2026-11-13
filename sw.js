/* Hors ligne : réseau d'abord (les mises à jour arrivent tout de suite),
   copie enregistrée si pas de réseau. */
const CACHE = "coach-trail-v9";
const FILES = ["./", "index.html", "data.js", "sync.js", "manifest.webmanifest", "icons/apple-touch-icon.png", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png"];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES.map((f) => new Request(f, { cache: "reload" })))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== self.location.origin) return;
  const key = url.origin + url.pathname;
  e.respondWith(
    fetch(key, { cache: "no-store", credentials: "same-origin" })
      .then((res) => { if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(key, copy)); } return res; })
      .catch(() => caches.match(key).then((hit) => hit || caches.match(url.origin + url.pathname.replace(/[^/]*$/, ""))))
  );
});
