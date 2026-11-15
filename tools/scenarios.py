# -*- coding: utf-8 -*-
"""Génère data/scenarios.json à partir des scénarios PSE1 et PSE2."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scenarios_pse1 import PSE1
from scenarios_pse2 import PSE2
from scenarios_pse1b import PSE1B
from scenarios_pse2b import PSE2B
OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios.json')
CRIT = {'PSE1': {'c1','c2','c3','c4','c5','c6','c7'}, 'PSE2': {'d1','d2','d3','d4','d5','d6','d7','d8','d11'}}
CASES = {'ova','hemo','pc','acr','detresse','malaise','trauma'}
CHK = {'PSE1': {'c3a','c3b','c3c','c3d'}, 'PSE2': {'d1a','d1b','d1c','d2a','d2b'}}
out = []
for cur, L in (('PSE1', PSE1 + PSE1B), ('PSE2', PSE2 + PSE2B)):
    ids = set()
    for s in L:
        s = dict(s, cur=cur)
        assert s['id'] not in ids; ids.add(s['id'])
        assert set(s['observe']) <= CRIT[cur], (s['id'], set(s['observe']) - CRIT[cur])
        assert set(s['cases']) <= CASES and set(s['checks']) <= CHK[cur], s['id']
        for k in ('titre','theme','jour','etape','message','contexte','secouristes','securite'): assert s[k], (s['id'], k)
        out.append(s)
json.dump(out, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(out), 'scénarios ·', os.path.getsize(OUT), 'octets')
