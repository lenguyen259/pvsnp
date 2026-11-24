from lib8 import *
from t2lib import load_cached, red, renum, triangle_free
import time
st=collections.Counter(); ex={}; seen=set(); t0=time.time()
for fn,n,E,c in load_cached():
    g=Graph(E,n)
    degs=[len(g.N[v]) for v in g.sup]
    if len(E)==max(degs): continue   # star
    c=renum(n,red(g,c)); key=(tuple(g.E),fmt(c))
    if key in seen: continue
    seen.add(key)
    dl=(len(c)-g.P,triangle_free(g)); st[("n",dl)]+=1
    if any(cert2(g,c,v) for v in g.sup if g.Eminus({v})): st[('cert',dl)]+=1
    else:
        if dl not in ex or len(c)<len(ex[dl][1].split()): ex[dl]=(g.E,fmt(c))
print(sorted(st.items()),time.time()-t0); print(ex)
