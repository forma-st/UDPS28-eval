#!/usr/bin/env python3
"""Fonds de page des fiches d'origine (modeles/*.pdf -> docs/app/forms/*.png) et
positions des techniques sur les fiches de technicité (forms/layout-tech.json)."""
import json, os, re, subprocess, tempfile, unicodedata
from PIL import Image, ImageDraw
import pdfplumber
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = 'docs/app/forms'; os.makedirs(OUT, exist_ok=True)
DPI = 200; MM = 25.4 / 72
# zones à masquer (mm) : titre « Annexe 3 » et pied de page du référentiel sur la fiche de certification
MASKS = {'certification-pse1': [(0, 0, 297, 25.6), (0, 182, 297, 210), (262, 25, 297, 70), (240, 172.5, 297, 182)]}
for name in ['formative-pse1', 'formative-pse2', 'technicite-pse1', 'technicite-pse2', 'certification-pse1', 'pv-pse1', 'pv-fc-pse1', 'pv-pse2', 'pv-fc-pse2']:
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['pdftoppm', '-r', str(DPI), '-png', '-singlefile', f'modeles/{name}.pdf', f'{td}/p'], check=True)
        im = Image.open(f'{td}/p.png').convert('RGB')
    px = DPI / 25.4; d = ImageDraw.Draw(im)
    for x0, y0, x1, y1 in MASKS.get(name, []):
        d.rectangle([x0 * px, y0 * px, x1 * px, y1 * px], fill='white')
    im.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(f'{OUT}/{name}.png', optimize=True)
    print(name, im.size, os.path.getsize(f'{OUT}/{name}.png') // 1024, 'Ko')

def norm(s): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode())
layout = {}
for name in ['technicite-pse1', 'technicite-pse2']:
    with pdfplumber.open(f'modeles/{name}.pdf') as pdf:
        pg = pdf.pages[0]
        words = pg.extract_words(keep_blank_chars=True, x_tolerance=1.5)
        hl = [r for r in pg.rects + pg.lines if (r['bottom'] - r['top']) * MM < .8 and (r['x1'] - r['x0']) * MM > 2]
        vl = sorted({round(r['x0'] * MM, 1) for r in pg.rects + pg.lines if (r['x1'] - r['x0']) * MM < .8 and (r['bottom'] - r['top']) * MM > 2})
        starts = {0: set(), 1: set()}; rows = []
        def above_line(x0, top):
            ys = sorted({round(r['top'] * MM, 1) for r in hl if (r['x0'] * MM) - 1 < x0 < (r['x1'] * MM) + 1})
            a = [y for y in ys if y <= top + .3]
            return a[-1] if a else round(top - .8, 1)
        for w in words:
            t = w['text'].strip()
            if not t: continue
            x0, top = w['x0'] * MM, w['top'] * MM
            col = 0 if x0 < 148 else 1
            y0 = above_line(x0 + 2, top); starts[col].add(y0)
            if t == 'FAIT' or (t.isupper() and len(t) > 3) or 'NOM / PR' in t or t.startswith(('Date', '|', 'A', 'OUI', 'NON', '1 :', 'ligne A')) and len(t) < 12: continue
            rows.append({'t': norm(t), 'raw': t, 'col': col, 'y0': y0})
        # fusion des libellés sur plusieurs lignes (même cellule)
        merged = {}
        for r in rows:
            k = (r['col'], r['y0'])
            if k in merged: merged[k]['t'] += r['t']; merged[k]['raw'] += ' ' + r['raw']
            else: merged[k] = dict(r)
        for r in merged.values():
            nxt = sorted(y for y in starts[r['col']] if y > r['y0'] + 1)
            r['y1'] = min(nxt[0] if nxt else r['y0'] + 4.5, r['y0'] + 12)
        layout[name] = {'v': vl, 'rows': list(merged.values())}
        print(name, len(merged), 'lignes, traits verticaux', vl)
json.dump(layout, open(f'{OUT}/layout-tech.json', 'w'), ensure_ascii=False)
