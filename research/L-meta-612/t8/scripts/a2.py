from lib8 import *
import time
from t5an import load
files=sys.argv[1:]
st=collections.Counter(); fails=[]; t0=time.time()
src=allsrc() if not files else (('f',d) for d in load(files))
for s_,d in src:
    g=Graph(d['E']); c=parse(d['c'])
    if not ok(g,c): st['bad']+=1; continue
    st['circ']+=1; sub=max(len(g.N[v]) for v in g.sup)<=3
    st['sub']+=sub
    res=[(nm,v,LD(g,c,rho)-need) for nm,v,rho,need in g.options()]
    okA=any(x>=0 for nm,v,x in res if nm=='A'); okAll=any(x>=0 for nm,v,x in res)
    okAB=any(x>=0 for nm,v,x in res if nm in 'AB')
    st['LD']+=okAll; st['LD_A']+=okA; st['LD_AB']+=okAB
    if sub: st['sub_LD_A']+=okA
    if not okA and len(fails)<12: fails.append((d.get('g'),sub,d['E'],d['c'],[r for r in res if r[2]>=0]))
print(dict(st),time.time()-t0); [print(f) for f in fails]
