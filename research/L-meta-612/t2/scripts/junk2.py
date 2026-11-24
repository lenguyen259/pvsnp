"""Is 'size >= Phi + j3' (girth >= 5) closed under R-TOT?  Test: some option X with
elim(X) - need(X) >= j3(C) - j3(red(C|X)), X in {A(v), N(v), C(v) = (x_v:=1, x_N(v):=0)}."""
import collections
from t2lib import *
def j3(g,c): return viol_counts(g,c)[2] if c else 0
def sub(g,X):
    return Graph(g.Eminus(X),g.n) if g.Eminus(X) else None
st=collections.Counter(); seen=set(); ex={}
for fn,n,E,c in load_cached():
    g=Graph(E,n)
    if g.t==1 or not triangle_free(g): continue
    c=renum(n,red(g,c)); k=(g.E,tuple(c))
    if k in seen: continue
    seen.add(k); st['circ']+=1
    J=j3(g,c); st['withjunk']+= J>0
    okk=False
    for v in g.sup:
        Nv=g.N[v]
        for nm,rho,X in [('A',{v:0},{v}),('N',{u:0 for u in Nv|{v}},Nv|{v}),('C',{v:1,**{u:0 for u in Nv}},Nv|{v})]:
            h=sub(g,X)
            if h is None: continue
            need=g.P-h.P
            r=red(g,c,rho); e=len(c)-len(r)
            if not r: continue
            r=renum(n,r); Jr=j3(h,r)
            if e-need>=J-Jr: okk=True; break
        if okk: break
    if not okk:
        st['FAIL']+=1; d=len(c)-g.P
        if d not in ex: ex[d]=(g.E,fmt(c),J)
print(dict(st)); print(ex)
