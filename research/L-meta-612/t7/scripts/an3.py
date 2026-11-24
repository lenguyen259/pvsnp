"""which first-order (LO) / LT-paid options exist: localisation tests."""
from lib7 import *
from t2lib import minimal_ands, support
import time
secs=float(sys.argv[1]); st=collections.Counter(); t0=time.time(); ex=collections.defaultdict(list)
for src,d in pools():
    if time.time()-t0>secs: break
    g=Graph(d['E']); c=parse(d['c']); st['circ']+=1
    LOp=set(); LTp=set()
    for nm,v,rho,need in g.options():
        K,cp,Tp,T=parts(g,c,rho)
        if len(K|cp)>=need: LOp.add((nm,v))
        if len(K|cp|Tp)-1>=need: LTp.add((nm,v))
    supp=set()
    for m in minimal_ands(c): supp|=support(g,c,m)
    md=max(len(g.N[v]) for v in g.sup)
    tests={
     'mANB_LT': any(v in supp for nm,v in LTp),
     'mANB_LO': any(v in supp for nm,v in LOp),
     'N_LT': any(nm=='N' for nm,v in LTp),
     'AB_LT': any(nm!='N' for nm,v in LTp),
     'maxdeg_LT': any(len(g.N[v])==md for nm,v in LTp),
     'deg3+_LT': any(len(g.N[v])>=3 for nm,v in LTp),
    }
    # leaf test for locpool: L = bad leaves
    if 'L' in d:
        for v in d['L']:
            u=next(iter(g.N[v])); W=g.N[u]-{v}
            st['leaf']+=1
            st['leaf_Nw_LT']+= any(('N',w) in LTp for w in W)
            st['leaf_Nw_LO']+= any(('N',w) in LOp for w in W)
    for k,x in tests.items():
        st[k]+=x
        if not x and (not ex[k] or len(c)<len(parse(ex[k][0][1]))): ex[k]=[(d.get('g'),d['c'])]
print(dict(st))
for k in ex: print(k,ex[k])
