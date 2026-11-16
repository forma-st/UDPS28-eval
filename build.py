#!/usr/bin/env python3
"""Construit l'application à partir de src/app.html.

- fichier-unique.html : fichier unique autonome (polices, logo et module PDF intégrés)
- docs/app/  : application installable (site GitHub Pages) (PWA hors ligne) = contenu de l'app Android (Capacitor)
"""
import base64, hashlib, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

src = open('src/app.html', encoding='utf-8').read()
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
LOGO = 'data:image/jpeg;base64,' + b64('brand/logo-480.jpg')
MARK = 'data:image/png;base64,' + b64('brand/symbole-96.png')
import json
QCM = json.dumps({'PSE1': json.load(open('data/qcm-pse1.json', encoding='utf-8')), 'PSE2': json.load(open('data/qcm-pse2.json', encoding='utf-8'))}, ensure_ascii=False)
src = src.replace('__LOGO__', LOGO).replace('__MARK__', MARK).replace('const QCM=__QCM__;', 'const QCM=' + QCM + ';').replace('const FORM_FILES=__FORM_FILES__;', 'const FORM_FILES=' + json.dumps(sorted(f[:-4] for f in os.listdir('docs/app/forms') if f.endswith('.png'))) + ';').replace('const SCENARIOS=__SCENARIOS__;', 'const SCENARIOS=' + open('data/scenarios.json', encoding='utf-8').read() + ';').replace('const FICHES=__FICHES__;', 'const FICHES=' + json.dumps(json.load(open('data/fiches-pedagogiques.json', encoding='utf-8')), ensure_ascii=False, separators=(',', ':')) + ';')

WEIGHTS = (400, 500, 600, 700, 800)
FONT_FILES = [f'montserrat-latin-{w}-normal.woff2' for w in WEIGHTS]
def font_css(url):
    return ''.join(f"@font-face{{font-family:'Montserrat';font-style:normal;font-weight:{w};font-display:swap;src:url({url(f)}) format('woff2')}}\n"
                   for w, f in zip(WEIGHTS, FONT_FILES))

HEAD = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style>
'''
def page(body, extra_head='', extra_body=''):
    return HEAD + extra_head + '</head>\n<body>\n' + body + extra_body + '\n</body>\n</html>\n'

jspdf = open('vendor/jspdf.umd.min.js', encoding='utf-8').read()
sdk = open('vendor/anthropic-sdk.min.js', encoding='utf-8').read()  # SDK officiel Anthropic (tools/sdk-bundle)
el = open('vendor/elevenlabs-client.min.js', encoding='utf-8').read()  # client officiel ElevenLabs (tools/el-bundle)

# 1) Fichier unique
FORMS = {os.path.splitext(f)[0]: 'data:image/png;base64,' + b64('docs/app/forms/' + f) for f in sorted(os.listdir('docs/app/forms')) if f.endswith('.png')}
embed = '<script>window.__FORMS_EMBED__=' + json.dumps(FORMS) + ';window.__TECH_LAYOUT__=' + open('docs/app/forms/layout-tech.json', encoding='utf-8').read() + ';</script>'
single = src.replace('<!--FONTS-->', '<style>' + font_css(lambda f: 'data:font/woff2;base64,' + b64('docs/app/fonts/' + f)) + '</style>') \
            .replace('<!--JSPDF-->', embed + '<script>' + jspdf + '</script><script>' + sdk + '</script><script>' + el + '</script>')
open('fichier-unique.html', 'w', encoding='utf-8').write(page(single))

# 2) PWA / Android
os.makedirs('docs/app/vendor', exist_ok=True)
open('docs/app/vendor/jspdf.umd.min.js', 'w', encoding='utf-8').write(jspdf)
open('docs/app/vendor/anthropic-sdk.min.js', 'w', encoding='utf-8').write(sdk)
open('docs/app/vendor/elevenlabs-client.min.js', 'w', encoding='utf-8').write(el)
body = src.replace('<!--FONTS-->', '<style>' + font_css(lambda f: 'fonts/' + f) + '</style>') \
          .replace('<!--JSPDF-->', '<script src="vendor/jspdf.umd.min.js"></script><script src="vendor/anthropic-sdk.min.js"></script><script src="vendor/elevenlabs-client.min.js"></script>')
head = '''<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Eval">
'''
sw_reg = '''
<script>
if('serviceWorker' in navigator && location.protocol.startsWith('http') && !(window.Capacitor&&window.Capacitor.isNativePlatform&&window.Capacitor.isNativePlatform())){
  window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js',{updateViaCache:'none'}).then(function(r){r.update()}).catch(function(){})});
  var hadSW=!!navigator.serviceWorker.controller,reloaded=false;
  navigator.serviceWorker.addEventListener('controllerchange',function(){if(hadSW&&!reloaded){reloaded=true;location.reload()}});
}
</script>'''
html = page(body, head, sw_reg)
open('docs/app/index.html', 'w', encoding='utf-8').write(html)

assets = ['./', 'index.html', 'manifest.webmanifest', 'vendor/jspdf.umd.min.js', 'vendor/anthropic-sdk.min.js', 'vendor/elevenlabs-client.min.js'] + [f'fonts/{f}' for f in FONT_FILES] + \
         [f'forms/{f}' for f in sorted(os.listdir('docs/app/forms'))] + ['icons/icon-192.png', 'icons/icon-512.png', 'icons/maskable-512.png', 'icons/apple-touch-icon.png']
version = hashlib.sha1((html + jspdf + sdk + el).encode()).hexdigest()[:10]
open('docs/app/sw.js', 'w', encoding='utf-8').write(f'''// Service worker : met l'application en cache pour un fonctionnement hors ligne.
const CACHE='eval-pse-{version}';
const ASSETS={assets!r};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n!==CACHE).map(n=>caches.delete(n)))).then(()=>self.clients.claim()))}});
// Page : réseau d'abord (nouvelle version dès qu'il y a du réseau), cache sinon (terrain sans réseau).
// Autres fichiers : cache d'abord.
self.addEventListener('fetch',e=>{{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);const page=e.request.mode==='navigate'||u.pathname.endsWith('/')||u.pathname.endsWith('index.html');
  if(page){{e.respondWith(fetch(e.request,{{cache:'no-store'}}).then(r=>{{const c=r.clone();caches.open(CACHE).then(ca=>ca.put('index.html',c));return r}}).catch(()=>caches.match('index.html')));return}}
  e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request).catch(()=>caches.match('index.html'))));
}});
''')
open('docs/app/manifest.webmanifest', 'w', encoding='utf-8').write('''{
  "name": "Eval - UDPS 28",
  "short_name": "Eval",
  "description": "Évaluations des formations PSE1, PSE2, PIC F, PAE FPSE et chef d’équipe, sans réseau.",
  "lang": "fr",
  "start_url": "./index.html",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#f4f7fa",
  "theme_color": "#002b6b",
  "icons": [
    {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
''')
print('OK - index.html (%d Ko) et docs/app/ générés, cache %s' % (os.path.getsize('fichier-unique.html') // 1024, version))
