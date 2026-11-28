from lib8 import *
from t2lib import load_cached, red, renum, triangle_free
st=collections.Counter(); ex={}; seen=set()
for fn,n,E,c in load_cached():
    g=Graph(E,n)
    if len(E)==max(len(g.N[v]) for v in g.sup): continue
    c=renum(n,red(g,c)); key=(tuple(g.E),fmt(c))
    if key in seen: continue
    seen.add(key); dl=len(c)-g.P
    okLD=any(LD(g,c,rho)>=need for nm,v,rho,need in g.options())
    st[('n',dl)]+=1; st[('LD',dl)]+=okLD
    if not okLD and dl not in ex: ex[dl]=(g.E,fmt(c))
    # STAR-ALL centre
    if not starall_viol(g,c):
        cs=centres(g,c); st[('SA',dl)]+=1
        st[('SAc',dl)]+=any(LD(g,c,rho)>=need for nm,v,rho,need in g.options() if nm=='A' and v in cs)
print(sorted(st.items())); print(ex)
