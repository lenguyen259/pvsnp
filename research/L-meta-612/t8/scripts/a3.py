from lib8 import *
from t5an import load
for d in load(sys.argv[1:]):
    g=Graph(d['E']); c=parse(d['c'])
    if not ok(g,c): continue
    res=[(nm,v,LD(g,c,rho)-need,LR(g,c,rho)-need) for nm,v,rho,need in g.options()]
    if not any(r[2]>=0 for r in res):
        print(d.get('g'),d['E'],len(c),g.P,d['c']); print([r for r in res if r[3]>=0]); print(max(r[2] for r in res))
