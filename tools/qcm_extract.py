#!/usr/bin/env python3
"""Extrait le corrigé du QCM d'un référentiel ANPS (texte pdftotext -layout) en JSON.
Usage : python3 tools/qcm_extract.py rif.txt "CORRIGE QCM PSE1" > qcm.json"""
import json, re, sys
txt = open(sys.argv[1], encoding='utf-8').read().split('\n')
start = next(i for i, l in enumerate(txt) if sys.argv[2] in l)
end = next((i for i in range(start, len(txt)) if re.search(r'Annexe \d+ : Proc', txt[i])), len(txt))
qs, cur, pending_q = [], None, False
for raw in txt[start:end]:
    l = raw.rstrip()
    s = l.strip()
    if not s or ('Premiers Secours en' in s and 'EPN' in s) or re.fullmatch(r'\d{1,3}', s) or 'NOM / PR' in s or s.startswith(('L’objectif', 'Important', 'EPN ANPS', 'Conception', 'Correction', 'EVAL/')) or re.search(r'\d+ pages$', s):
        continue
    m = re.match(r'^\s*(\d{1,2})\.\s+(.*)$', l)
    if m and (not cur or int(m.group(1)) == cur['n'] + 1):
        cur = {'n': int(m.group(1)), 'q': m.group(2).strip(), 'o': []}
        qs.append(cur); pending_q = not cur['q'].endswith(('?', ':')); continue
    if cur is None:
        continue
    if pending_q:
        cur['q'] += ' ' + s; pending_q = not s.endswith(('?', ':')); continue
    mo = re.match(r'^\s*(X)?\s+(.*)$', l)
    ok = bool(mo and mo.group(1))
    label = (mo.group(2) if mo else s).strip()
    # ligne d'option très indentée sans X et option précédente sans majuscule de départ : suite de l'option
    prev=cur['o'][-1]['t'] if cur['o'] else ''
    if cur['o'] and not ok and (label[:1].islower() or prev.endswith((',',' de',' des',' du',' le',' la',' en'))):
        cur['o'][-1]['t'] += ' ' + label; continue
    cur['o'].append({'t': label, 'ok': ok})
print(json.dumps(qs, ensure_ascii=False))
