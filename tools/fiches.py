#!/usr/bin/env python3
"""Fiches d'évaluation des techniques pédagogiques (PIC F, PAE FPSE) extraites des référentiels.
Les pages sont mises bout à bout (« flux » sans pieds de page) car certaines fiches sont à cheval sur
deux pages dans le PDF du référentiel. Chaque fiche est recomposée sur une page A4 :
  - docs/app/forms/fe-<cursus>-<num>.png : fond (image 200 dpi)
  - data/fiches-pedagogiques.json : éléments, compétences et positions (mm) des cases."""
import json, os, re, subprocess, tempfile, pdfplumber
from PIL import Image
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MM = 25.4 / 72; DPI = 200; PX = DPI / 25.4; TOP = 12.0
SRC = {'PICF': ('modeles/sources/rifric-picf-2025.pdf', range(71, 82), 'Pédagogie Initiale et Commune'),
       'PAEFPSE': ('modeles/sources/rifric-paefpse-2025.pdf', range(65, 78), 'PAE Formateur en Premiers')}
r2 = lambda v: round(v, 2)
TITRES = {'PICF': ['LE TRAVAIL DE GROUPE', 'L’ÉTUDE DE CAS', 'LE REMUE-MÉNINGES', 'MÉTAPLAN', 'LA CARTE MENTALE', 'L’EXPOSÉ INTERACTIF', 'LA DÉMONSTRATION PRATIQUE',
                    'LA DÉMONSTRATION PRATIQUE EN MIROIR', 'LA DÉMONSTRATION PRATIQUE DIRIGÉE', 'L’APPRENTISSAGE DU GESTE', 'LA MISE EN SITUATION'],
          'PAEFPSE': ['ANIMATION GQS', 'LE TRAVAIL DE GROUPE', 'L’ÉTUDE DE CAS', 'LE REMUE-MÉNINGES', 'MÉTAPLAN', 'L’EXPOSÉ INTERACTIF', 'LA DÉMONSTRATION PRATIQUE',
                      'LA DÉMONSTRATION PRATIQUE DIRIGÉE', 'LA DÉMONSTRATION PRATIQUE EN MIROIR', 'L’APPRENTISSAGE DU GESTE', 'LA MISE EN SITUATION']}
out = {}
for cur, (path, pages, footer) in SRC.items():
    W, H, V, bands = [], [], [], []
    flow = 0.0
    with pdfplumber.open(path) as pdf:
        for pno in pages:
            pg = pdf.pages[pno - 1]
            ws = pg.extract_words(x_tolerance=1.5, extra_attrs=['size'])
            foot = min([w['top'] * MM for w in ws if footer.startswith(w['text'][:6]) and w['top'] * MM > 250] + [284])
            ann = [w for w in ws if w['text'] == 'Annexe' and w['top'] * MM < 30]
            items_top = [w['top'] * MM for w in ws if w['top'] * MM < foot - .5 and not (ann and w['top'] * MM < ann[0]['bottom'] * MM + 1)] + \
                        [e['top'] * MM for e in pg.edges if e['top'] * MM < foot - .5 and not (ann and e['top'] * MM < ann[0]['bottom'] * MM + 1)]
            if not items_top: continue
            top = min(items_top) - 1.2; bot = foot - 1.0
            bands.append((pno, top, bot, flow))
            f = lambda y: y - top + flow
            for w in ws:
                y = w['top'] * MM
                if top <= y <= bot: W.append(dict(x0=w['x0'] * MM, x1=w['x1'] * MM, top=f(y), bottom=f(w['bottom'] * MM), t=w['text'], size=w['size']))
            for e in pg.edges:
                col = e.get('stroking_color') or e.get('non_stroking_color') or (0,)
                dark = isinstance(col, (tuple, list)) and len(col) > 0 and all(isinstance(c, (int, float)) and c < .3 for c in col)
                if e['orientation'] == 'h' and top <= e['top'] * MM <= bot: H.append((f(e['top'] * MM), e['x0'] * MM, e['x1'] * MM, dark))
                elif e['orientation'] == 'v':
                    a, b = max(e['top'] * MM, top), min(e['bottom'] * MM, bot)
                    if b > a: V.append((e['x0'] * MM, f(a), f(b)))
            flow += bot - top
    # début de chaque fiche : mot « CONCEPTION » (cadre d'en-tête), fin : légende « Degré d'atteinte »
    starts = sorted(w['top'] for w in W if w['t'] == 'CONCEPTION')
    ends = sorted(w['bottom'] for w in W if w['t'] == 'Degré')
    fiches = []
    imgs = {}
    for k, s0 in enumerate(starts):
        hl = [h[0] for h in H if s0 - 6 < h[0] < s0 - .5]; fs = (max(hl) if hl else s0 - 3) - .6
        fe = min(e for e in ends if e > s0) + 1.0
        Wf = [w for w in W if fs <= w['top'] <= fe]; Hf = [h for h in H if fs - .3 <= h[0] <= fe]; Vf = [v for v in V if v[2] > fs and v[1] < fe]
        T = lambda y: r2(y - fs + TOP)
        text = ' '.join(w['t'] for w in Wf)
        m = re.search(r'FE/\s*([A-Z ]*?)\s*/?\s*(\d{2})\b', text.replace('FE/PAE FPSE/', 'FE/PAE FPSE/ ').replace('FE/PICF/', 'FE/PICF/ '))
        num = re.search(r'Évaluation n°\s*(\d+)', text).group(1)
        ref = ('FE/PICF/%02d' if cur == 'PICF' else 'FE/PAE FPSE/%02d') % int(num)
        big = [w for w in Wf if w['size'] > 11.5 and w['top'] - fs < 25 and re.search('[A-ZÉ]', w['t']) and w['t'].upper() == w['t'] and not w['t'].startswith(('FE/', 'N°', 'CONCEPTION', 'FORMATIONS', 'DES'))]
        seq = ' '.join(w['t'] for w in sorted(Wf, key=lambda w: (round(w['top'] * 2), w['x0'])) if w['top'] - fs < 40)
        mt = re.search(r'Évaluation n°\s*\d+\s+(.*?)\s+(?:Fiche d.évaluation|Évaluation d.un|Page|Mise)', seq)
        title = ' '.join(w for w in (mt.group(1) if mt else '').split() if w.upper() == w and not re.match(r'^(FE/|PAE|FPSE/|PICF/|\d)', w))
        el = next(w for w in Wf if w['t'].startswith('Éléments'))
        hdr = [w for w in Wf if w['t'] in ('A', 'B', 'C') and 0 < w['top'] - el['top'] < 9 and w['x0'] > el['x1'] - 5]
        ytop = max(w['bottom'] for w in hdr) + .3
        imp = next(w for w in Wf if w['t'].startswith('Impression') and w['top'] > ytop); ybot = imp['top'] - .5
        # traits verticaux du corps du tableau (entre l'en-tête A/B/C et « Impression générale »)
        VX = sorted({round(v[0], 1) for v in Vf if min(v[2], ybot) - max(v[1], ytop) > 3})
        VX = [x for i, x in enumerate(VX) if i == 0 or x - VX[i - 1] > .6]
        def near(x, side):
            c = [vx for vx in VX if ((vx < x - .3) if side == 'L' else (vx > x + .3))]
            return min(c, key=lambda vx: abs(vx - x))
        cols = {w['t']: [r2(near((w['x0'] + w['x1']) / 2, 'L')), r2(near((w['x0'] + w['x1']) / 2, 'R'))] for w in sorted(hdr, key=lambda w: w['x0'])}
        ax0 = min(c[0] for c in cols.values()); cx1 = max(c[1] for c in cols.values())
        ex0 = near(el['x0'], 'L'); tx0 = min(VX)
        ys = sorted({round(h[0], 1) for h in Hf if h[1] <= (ex0 + ax0) / 2 <= h[2] and ytop - 1 <= h[0] <= ybot + 1})
        ys = [y for i, y in enumerate(ys) if i == 0 or y - ys[i - 1] > .8]
        yc = sorted({round(h[0], 1) for h in Hf if h[3] and h[1] <= (tx0 + ex0) / 2 <= h[2] and ytop - 1.5 <= h[0] <= ybot + 1})
        yc = [y for i, y in enumerate(yc) if i == 0 or y - yc[i - 1] > .8]
        rows = []
        for y0, y1 in zip(ys, ys[1:]):
            if y1 - y0 < 2: continue
            ym = (y0 + y1) / 2
            words = [w for w in Wf if y0 - .2 <= (w['top'] + w['bottom']) / 2 <= y1 + .2]
            label = ' '.join(w['t'] for w in sorted(words, key=lambda w: (round(w['top'] * 2), w['x0'])) if ex0 - .5 <= w['x0'] < ax0 - .5)
            ne = any(w['t'].lower() == 'évalué' and w['x0'] >= ax0 - 1 for w in words)
            seg = [(a, b) for a, b in zip(yc, yc[1:]) if a - .3 <= ym <= b + .3]
            comp = ''
            if seg:
                a, b = seg[0]; comp = ' '.join(w['t'] for w in Wf if tx0 - .5 <= w['x0'] < ex0 - .5 and a <= (w['top'] + w['bottom']) / 2 <= b)
            sep = any(v[1] <= ym <= v[2] and ex0 + 5 < v[0] < cx1 - .5 for v in Vf)
            if not label: continue
            if not sep and not ne: rows.append({'sec': label, 'y0': T(y0), 'y1': T(y1)}); continue
            comps = [t for t in re.findall(r'\d+(?:\.\d+)?', comp)]
            rows.append({'comp': comps, 'label': label, 'y0': T(y0), 'y1': T(y1), **({'ne': True} if ne else {})})
        def cell_box(x, y):
            l = max([v[0] for v in Vf if v[0] < x and v[1] <= y <= v[2]] or [tx0]); r = min([v[0] for v in Vf if v[0] > x and v[1] <= y <= v[2]] or [cx1])
            t = max([h[0] for h in Hf if h[0] < y and h[1] <= x <= h[2]] or [y - 3]); b = min([h[0] for h in Hf if h[0] > y and h[1] <= x <= h[2]] or [y + 3])
            return [r2(l), T(t), r2(r), T(b)]
        fields = {}
        for key, lab in (('eleve', 'ÉLÈVE'), ('formateur', 'FORMATEUR'), ('theme', 'THÈME'), ('date', 'DATE'), ('temps', 'TEMPS')):
            ws = [w for w in Wf if w['t'] == lab and w['top'] < ytop]
            if key == 'formateur': ws = [w for w in ws if not any(o['t'] == 'ÉLÈVE' and abs(o['top'] - w['top']) < 1 and o['x1'] + 3 > w['x0'] for o in Wf)]
            if not ws: continue
            w = ws[0]; hb = cell_box((w['x0'] + w['x1']) / 2, (w['top'] + w['bottom']) / 2)
            hb_raw = [hb[0], hb[1] - TOP + fs, hb[2], hb[3] - TOP + fs]
            fields[key] = cell_box(hb_raw[2] + 2, (hb_raw[1] + hb_raw[3]) / 2) if key in ('date', 'temps') else cell_box((w['x0'] + w['x1']) / 2, hb_raw[3] + 2)
        impb = cell_box(imp['x1'] + 2, imp['bottom'] + 1)
        right = max(VX)
        # fond : tranches d'images des pages, recollées
        canvas = Image.new('RGB', (round(210 * PX), round(297 * PX)), 'white')
        for pno, top, bot, off in bands:
            a, b = max(fs, off), min(fe, off + bot - top)
            if b <= a: continue
            if pno not in imgs:
                with tempfile.TemporaryDirectory() as td:
                    subprocess.run(['pdftoppm', '-r', str(DPI), '-png', '-singlefile', '-f', str(pno), '-l', str(pno), path, f'{td}/p'], check=True)
                    imgs[pno] = Image.open(f'{td}/p.png').convert('RGB')
            y_src = a - off + top
            crop = imgs[pno].crop((0, round(y_src * PX), imgs[pno].width, round((y_src + b - a) * PX)))
            canvas.paste(crop, (0, round((a - fs + TOP) * PX)))
        name = f'fe-{cur.lower()}-{int(num):02d}'
        title = TITRES[cur][int(num) - (1 if cur == 'PICF' else 0)]
        canvas.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(f'docs/app/forms/{name}.png', optimize=True)
        fiches.append({'id': name, 'ref': ref, 'num': num, 'title': title, 'cols': cols, 'el': [r2(ex0), r2(ax0)],
                       'obs': [r2(cx1), T(ytop), r2(right), T(ybot)], 'imp': [impb[0], T(imp['bottom']), impb[2], impb[3]], 'fields': fields, 'rows': rows})
        print(cur, ref, '|', title, '|', sum(1 for r in rows if 'comp' in r), 'élém.', sum(1 for r in rows if 'sec' in r), 'sect.', sum(1 for r in rows if r.get('ne')), 'NE | cols', ''.join(cols), '| champs', ','.join(fields), '| haut.', round(fe - fs))
    out[cur] = fiches
json.dump(out, open('data/fiches-pedagogiques.json', 'w'), ensure_ascii=False, indent=1)
