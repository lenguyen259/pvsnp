# hypothetical: graphs with <=K non-isolated vertices get lb = m+tau-1 if (canonical) in allowed set
import sys, itertools
from functools import lru_cache
import gsearch as g
K = int(sys.argv[1])
def tau(E):
    V = sorted({v for e in E for v in e})
    for r in range(len(V)+1):
        for C in itertools.combinations(V,r):
            s=set(C)
            if all(a in s or b in s for a,b in E): return r
used = {}
@lru_cache(None)
def val(A,E):
    best = (-1,None)
    if not E: best=(len(A)-1,('emp',))
    if not A and E:
        c = g.ccanon(E)
        if c in g.BASEC: best=max(best,(g.BASEC[c][1],('base',)))
        nv = len({v for e in E for v in e})
        if nv<=K:
            lb = len(E)+tau(E)-1
            if lb>best[0]: best=(lb,('hyp',c))
    verts = {v for e in E for v in e}|set(A)
    for p in sorted(verts):
        if not g.dep(A,E,p): continue
        A0,E0=g.fix0(A,E,p); v0 = val(A0,E0)[0] if (A0 or E0) else None
        if v0 is not None and 1+v0>best[0]: best=(1+v0,('f0',p))
        if p in A: continue
        A1,E1=g.fix1(A,E,p); v1 = val(A1,E1)[0] if (A1 or E1) else None
        if v1 is not None and 1+v1>best[0]: best=(1+v1,('f1',p))
        if v0 is not None and v1 is not None and 2+min(v0,v1)>best[0]: best=(2+min(v0,v1),('b2',p))
    return best
def tree(A,E):
    v,st=val(A,E)
    if st[0] in('emp','base'): return (st[0],v,sorted(E))
    if st[0]=='hyp': return ('HYP',v,sorted(E))
    p=st[1]
    if st[0]=='f0': return ('f0',p,tree(*g.fix0(A,E,p)))
    if st[0]=='f1': return ('f1',p,tree(*g.fix1(A,E,p)))
    return ('b2',p,tree(*g.fix0(A,E,p)),tree(*g.fix1(A,E,p)))
r=val(frozenset(),frozenset(g.G)); print(r); print(tree(frozenset(),frozenset(g.G)))
