from lib8 import *
import json
unc=json.load(open('unc157.json')); st=collections.Counter(); shown=0
for d in unc:
    g=Graph(d['E']); c=parse(d['c'])
    for nm,v,rho,need in g.options():
        if nm!='A' or LR(g,c,rho)<need: continue
        r=DV2(g,c,v); Z,L,I,aI,F,exc=zone(g,c,rho)
        reason=('kZ0' if r['kZ']==0 else '')+('pen%d'%r['pen'] if r['pen'] else '')+('' if r['singok'] or not r['rest'] else 'nosing')+('' if r['single'] else 'multi')
        st[reason]+=1
        if shown<6: shown+=1; print(d['g'],d['c'],'v',v,'need',need,'LD',r['LD'],'F',F,'aI',aI,'exc',exc,'kZ',r['kZ'],'kL',r['kL'],'ND',r['ND'],'rest',r['rest'],'car',r['car'],reason)
print(dict(st))
