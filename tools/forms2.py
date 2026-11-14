#!/usr/bin/env python3
"""Fonds des fiches PIC F / PAE FPSE / CE extraites des référentiels (titre « Annexe » et pied de page masqués)
+ détection des traits du tableau (mm) pour placer les données."""
import json, os, subprocess, tempfile, sys
import numpy as np
from PIL import Image, ImageDraw
import pdfplumber
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DPI = 200; PX = DPI / 25.4
S = 'modeles/sources/'
PAGES = [  # nom, pdf, page, zones masquées (mm) en plus du titre « Annexe » et du pied de page
  ('picf-suivi-1', S + 'rifric-picf-2025.pdf', 83, []), ('picf-suivi-2', S + 'rifric-picf-2025.pdf', 84, []),
  ('picf-pv', S + 'rifric-picf-2025.pdf', 67, []),
  ('paefpse-suivi-1', S + 'rifric-paefpse-2025.pdf', 63, []), ('paefpse-suivi-2', S + 'rifric-paefpse-2025.pdf', 64, []),
  ('paefpse-avis', S + 'rifric-paefpse-2025.pdf', 80, []),
  ('paefpse-pv', S + 'rifric-paefpse-2025.pdf', 91, []), ('paefpse-pv-fc', S + 'rifric-paefpse-2025.pdf', 92, []),
  ('ce-pv', S + 'rifric-ce-2022.pdf', 37, [(262, 180, 297, 210)]), ('ce-certif', S + 'rifric-ce-2022.pdf', 38, []), ('ce-formative', S + 'rifric-ce-2022.pdf', 39, [(175, 268, 210, 297)]),
]
lines = {}
for name, pdf, pno, extra in PAGES:
    with pdfplumber.open(pdf) as P:
        pg = P.pages[pno - 1]; W, Hh = pg.width * 25.4 / 72, pg.height * 25.4 / 72
        ws = pg.extract_words()
        ann = [w for w in ws if w['text'] == 'Annexe' and w['top'] * 25.4 / 72 < 40]
        foot = [w for w in ws if w['top'] * 25.4 / 72 > Hh - 22 and (w['text'].isdigit() or w['text'] in ('Pédagogie', 'PAE', 'Chef', 'Premiers'))]
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['pdftoppm', '-r', str(DPI), '-png', '-singlefile', '-f', str(pno), '-l', str(pno), pdf, f'{td}/p'], check=True)
        im = Image.open(f'{td}/p.png').convert('RGB')
    d = ImageDraw.Draw(im)
    masks = list(extra)
    if ann: masks.append((0, 0, W, ann[0]['bottom'] * 25.4 / 72 + 1.5))
    if foot: masks.append((0, min(w['top'] for w in foot) * 25.4 / 72 - 1.5, W, Hh))
    for x0, y0, x1, y1 in masks: d.rectangle([x0 * PX, y0 * PX, x1 * PX, y1 * PX], fill='white')
    im.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(f'docs/app/forms/{name}.png', optimize=True)
    a = np.array(im.convert('L')) < 140
    def det(arr, frac):
        res = []
        for i, row in enumerate(arr):
            dd = np.diff(np.concatenate(([0], row.astype(int), [0]))); s = np.where(dd == 1)[0]; e = np.where(dd == -1)[0]
            if len(s) and (e - s).max() > arr.shape[1] * frac: k = (e - s).argmax(); res.append((i, s[k], e[k]))
        g = []
        for r in res:
            if g and r[0] - g[-1][-1][0] <= 3: g[-1].append(r)
            else: g.append([r])
        return [(round(float(np.mean([x[0] for x in grp])) / PX, 1), round(min(x[1] for x in grp) / PX, 1), round(max(x[2] for x in grp) / PX, 1)) for grp in g]
    lines[name] = {'size': [round(W, 1), round(Hh, 1)], 'H': det(a, .04), 'V': det(a.T, .02)}
    print(name, lines[name]['size'], 'masques', [tuple(round(v, 1) for v in m) for m in masks], os.path.getsize(f'docs/app/forms/{name}.png') // 1024, 'Ko')
json.dump(lines, open('data/forms2-lines.json', 'w'), indent=0)
