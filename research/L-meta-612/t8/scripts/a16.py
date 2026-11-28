from lib8 import *
from t2lib import load_cached, red, renum
seen=set()
for fn,n,E,c in load_cached():
    g=Graph(E,n)
    if len(E)==max(len(g.N[v]) for v in g.sup): continue
    c=renum(n,red(g,c)); key=(tuple(g.E),fmt(c))
    if key in seen: continue
    seen.add(key)
    if not starall_viol(g,c):
        cs=centres(g,c)
        if not any(LD(g,c,rho)>=need for nm,v,rho,need in g.options() if nm=='A' and v in cs): print(g.E,len(c),g.P,fmt(c),sorted(cs))
