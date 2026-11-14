#!/usr/bin/env python3
"""Extrait la grille (traits horizontaux / verticaux) d'une page PDF, en mm."""
import sys, pdfplumber
MM = 25.4 / 72
def cl(v): return round(v * MM, 1)
with pdfplumber.open(sys.argv[1]) as pdf:
    pg = pdf.pages[0]; H = {}; V = {}
    for r in pg.rects + pg.lines:
        w, h = (r['x1'] - r['x0']) * MM, (r['bottom'] - r['top']) * MM
        if h < 0.8 and w > 2: H.setdefault(cl(r['top']), []).append((cl(r['x0']), cl(r['x1'])))
        elif w < 0.8 and h > 2: V.setdefault(cl(r['x0']), []).append((cl(r['top']), cl(r['bottom'])))
        elif w > 2 and h > 2 and len(sys.argv) > 2: print('BOX', cl(r['x0']), cl(r['top']), cl(r['x1']), cl(r['bottom']), r.get('non_stroking_color'))
    def merge(d):
        out = []
        for k in sorted(d):
            segs = sorted(d[k]); lo, hi = segs[0][0], max(s[1] for s in segs)
            out.append((k, lo, hi))
        return out
    print('H y:[x0-x1]'); [print('  %.1f  %.1f-%.1f' % t) for t in merge(H)]
    print('V x:[y0-y1]'); [print('  %.1f  %.1f-%.1f' % t) for t in merge(V)]
