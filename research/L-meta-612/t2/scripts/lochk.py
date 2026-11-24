"""(i) local bound test: exists option whose first-order lower bound >= need.
   (ii) sanity: cycle lemma (v with ch(v)>=2 has lo0>=3 or lo1>=4 on Delta<=2 graphs)."""
import collections,sys
from t2lib import *
st=collections.Counter(); seen=set(); ex={}
for fn,n,E,c in load_cached():
    g=Graph(E,n)
    if g.t==1: continue
    c=renum(n,red(g,c)); k=(g.E,tuple(c))
    if k in seen: continue
    seen.add(k); st['circ']+=1
    good=False
    for name,v,rho,need in g.options():
        if name=='A': L=lo_bounds(g,c,{v},0)
        elif name=='N': L=lo_bounds(g,c,g.N[v]|{v},0)
        else: L=lo_bounds(g,c,{v},1)
        if L>=need: good=True; break
    if not good:
        st['LOfail']+=1
        d=len(c)-g.P
        if d not in ex: ex[d]=(g.E,fmt(c))
    if max(len(g.N[v]) for v in g.sup)<=2:
        for v in g.sup:
            if len(g.N[v])==2 and charged(g,c,v)>=2:
                st['cyc_v']+=1
                if not (lo_bounds(g,c,{v},0)>=3 or lo_bounds(g,c,{v},1)>=4): st['CYC_VIOL']+=1; print('CYCVIOL',g.E,fmt(c),v)
print(dict(st)); print(ex)
