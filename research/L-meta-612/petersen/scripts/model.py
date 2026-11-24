# design-model search: stars in J (raw x) or F2 (over z), z_v = x_v | J. minimize k+|Z| with all ch<=deg-1. then build + verify exactly.
import sys, json, itertools
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from common import *
def solve(n,E,K,cap=None):
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    cap=cap or {v:deg[v]-1 for v in range(n)}
    pool=IDPool(); cl=[]
    C=lambda e,h: pool.id(('C',e,h))   # edge e centered at h
    P=lambda e: pool.id(('P',e))      # true: J part
    s=lambda h,p: pool.id(('s',h,p))
    Z=lambda v: pool.id(('Z',v))
    for ei,(a,b) in enumerate(E):
        cl.append([C(ei,a),C(ei,b)]); cl.append([-C(ei,a),-C(ei,b)])
        for h in (a,b):
            cl.append([-C(ei,h),-P(ei),s(h,1)]); cl.append([-C(ei,h),P(ei),s(h,0)])
    # s only if used
    for h in range(n):
        for p in (0,1):
            inc=[ei for ei,e in enumerate(E) if h in e]
            # s(h,p) -> exists e centered at h with part p : aux
            aux=[]
            for ei in inc:
                x=pool.id(('cp',ei,h,p)); aux.append(x)
                cl.append([-x,C(ei,h)]); cl.append([-x,P(ei) if p else -P(ei)])
            cl.append([-s(h,p)]+aux)
    # charges
    for v in range(n):
        lits=[Z(v)]
        for ei,(a,b) in enumerate(E):
            if v not in (a,b): continue
            u=b if a==v else a
            # v is leaf if centered at u; charged if J part or not Z(v)
            x=pool.id(('lc',ei,v)); lits.append(x)
            cl.append([-C(ei,u),-P(ei),x]); cl.append([-C(ei,u),Z(v),x])
        for p in (0,1):
            x=pool.id(('cc',v,p)); lits.append(x)
            cl.append([-s(v,p),x] if p==1 else [-s(v,p),Z(v),x])
        cl.extend(CardEnc.atmost(lits=lits,bound=cap[v],vpool=pool,encoding=EncType.seqcounter).clauses)
    # J has >=2 stars if any Z
    js=[s(h,1) for h in range(n)]
    for v in range(n):
        cl.extend([[-Z(v)]+[a for a in js if a!=s(v,1)]])
    cl.extend(CardEnc.atleast(lits=js,bound=2,vpool=pool,encoding=EncType.seqcounter).clauses) if True else None
    obj=[s(h,p) for h in range(n) for p in (0,1)]+[Z(v) for v in range(n)]
    cl.extend(CardEnc.atmost(lits=obj,bound=K,vpool=pool,encoding=EncType.seqcounter).clauses)
    S=Cadical153(bootstrap_with=cl)
    if not S.solve(): return None
    m=set(l for l in S.get_model() if l>0)
    cen={ei:(a if C(ei,a) in m else b) for ei,(a,b) in enumerate(E)}
    part={ei:(1 if P(ei) in m else 0) for ei in range(len(E))}
    Zs=[v for v in range(n) if Z(v) in m]
    return cen,part,Zs
def build(n,E,cen,part,Zs):
    b=B(n); stars={}
    for ei,(a,c) in enumerate(E):
        h=cen[ei]; u=c if a==h else a; stars.setdefault((h,part[ei]),[]).append(u)
    Jt=[b.g('&',h,b.OR(L)) for (h,p),L in stars.items() if p==1]
    terms=[]
    if Jt: J=b.OR(Jt); terms.append(J)
    node={v:(b.g('|',v,J) if v in Zs else v) for v in range(n)}
    for (h,p),L in stars.items():
        if p==0: terms.append(b.g('&',node[h],b.OR([node[u] for u in L])))
    b.OR(terms); return b.c
if __name__=='__main__':
    E=[tuple(e) for e in json.loads(sys.argv[1])] if len(sys.argv)>1 else PET
    n=max(max(e) for e in E)+1
    for K in range(20,4,-1):
        r=solve(n,E,K)
        if r is None: print('K',K,'infeasible'); break
        c=build(n,E,*r); a=analyze(n,c,E)
        print('K',K,'Z',r[2],{k:a[k] for k in ('ok','size','nor','nand','ch','slack')}); last=fmt(a['R'])
    print(last)
