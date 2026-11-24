"""Claim Z_k data: in circuits C0 for f_H, a node z with OR_W <= z <= OR_W | f_{H-W}, W (|W|>=2) pairwise no common nbr.
Record min (size(C0)-Phi(H)) over such (C0,W,z); Claim Z_k says >= k-1."""
import itertools,collections
from gen import *
st=collections.Counter(); best={}; seen=set()
for fn,nn,E,c in load_cached():
    g=Graph(E,nn)
    c=renum(nn,red(g,c)); k=(g.E,tuple(c))
    if k in seen: continue
    seen.add(k)
    T=tables(g,c,{}); sl=len(c)-g.P
    nodes=[x[0] for x in c]
    for kk in (2,3):
        for W in itertools.combinations(range(g.n),kk):
            if any(g.N[a]&g.N[b] for a,b in itertools.combinations(W,2)): continue
            lo=0
            for w in W: lo|=g.X[w]
            fr=0
            for a,b in g.Eminus(set(W)): fr|=g.X[a]&g.X[b]
            hi=lo|fr
            for zz in nodes:
                if T[zz]&lo==lo and T[zz]&~hi==0:
                    st[(kk,sl)]+=1
                    key=kk
                    if key not in best or sl<best[key][0]: best[key]=(sl,g.E,fmt(c),W,zz)
                    break
print(dict(st)); 
for k,v in best.items(): print(k,v)
