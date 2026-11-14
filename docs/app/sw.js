// Service worker : met l'application en cache pour un fonctionnement hors ligne.
const CACHE='eval-pse-01fa87d699';
const ASSETS=['./', 'index.html', 'manifest.webmanifest', 'vendor/jspdf.umd.min.js', 'fonts/montserrat-latin-400-normal.woff2', 'fonts/montserrat-latin-500-normal.woff2', 'fonts/montserrat-latin-600-normal.woff2', 'fonts/montserrat-latin-700-normal.woff2', 'fonts/montserrat-latin-800-normal.woff2', 'forms/certification-pse1.png', 'forms/formative-pse1.png', 'forms/formative-pse2.png', 'forms/layout-tech.json', 'forms/pv-fc-pse1.png', 'forms/pv-fc-pse2.png', 'forms/pv-pse1.png', 'forms/pv-pse2.png', 'forms/technicite-pse1.png', 'forms/technicite-pse2.png', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/maskable-512.png', 'icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n!==CACHE).map(n=>caches.delete(n)))).then(()=>self.clients.claim()))});
// Page : réseau d'abord (nouvelle version dès qu'il y a du réseau), cache sinon (terrain sans réseau).
// Autres fichiers : cache d'abord.
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);const page=e.request.mode==='navigate'||u.pathname.endsWith('/')||u.pathname.endsWith('index.html');
  if(page){e.respondWith(fetch(e.request,{cache:'no-store'}).then(r=>{const c=r.clone();caches.open(CACHE).then(ca=>ca.put('index.html',c));return r}).catch(()=>caches.match('index.html')));return}
  e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request).catch(()=>caches.match('index.html'))));
});
