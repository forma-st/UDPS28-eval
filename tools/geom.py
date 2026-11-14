#!/usr/bin/env python3
"""Mesure la géométrie d'une page PDF d'origine (mots, traits, rectangles) en millimètres."""
import sys, pdfplumber
MM = 25.4 / 72
with pdfplumber.open(sys.argv[1]) as pdf:
    pg = pdf.pages[0]
    print('page', round(pg.width * MM, 1), 'x', round(pg.height * MM, 1), 'mm')
    if 'words' in sys.argv:
        for w in pg.extract_words(keep_blank_chars=True, x_tolerance=1.5):
            print('W %6.1f %6.1f %6.1f %6.1f  %s' % (w['x0']*MM, w['top']*MM, w['x1']*MM, w['bottom']*MM, w['text']))
    if 'lines' in sys.argv:
        hs = sorted({round(l['top']*MM, 1) for l in pg.lines + pg.edges if abs(l['top']-l['bottom']) < 1})
        vs = sorted({round(l['x0']*MM, 1) for l in pg.lines + pg.edges if abs(l['x0']-l['x1']) < 1})
        print('H', hs); print('V', vs)
    if 'rects' in sys.argv:
        for r in pg.rects:
            print('R %6.1f %6.1f %6.1f %6.1f fill=%s' % (r['x0']*MM, r['top']*MM, r['x1']*MM, r['bottom']*MM, r.get('non_stroking_color')))
    if 'images' in sys.argv:
        for im in pg.images:
            print('I %6.1f %6.1f %6.1f %6.1f' % (im['x0']*MM, im['top']*MM, im['x1']*MM, im['bottom']*MM))
