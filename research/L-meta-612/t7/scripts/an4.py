"""pseudoforest (locpool) : roles of LT-paid options."""
from lib7 import *
import time
secs=float(sys.argv[1]); st=collections.Counter(); t0=time.time(); ex={}
for src,d in pools([SC+'/t3/locpool.jsonl']):
    if time.time()-t0>secs: break
    g=Graph(d['E']); c=parse(d['c'])
    deg={v:len(g.N[v]) for v in g.sup}
    leaves={v for v in g.sup if deg[v]==1}; hold={next(iter(g.N[v])) for v in leaves}
    run={v for v in g.sup if v not in leaves and v not in hold}
    role=lambda v: 'P' if v in leaves else ('U' if v in hold else 'R')
    paid=set()
    for nm,v,rho,need in g.options():
        K,cp,Tp,T=parts(g,c,rho)
        if len(K|cp|Tp)-1>=need: paid.add(nm+role(v))
    st['circ']+=1; st[tuple(sorted(paid))]+=0
    for p in paid: st[p]+=1
    key=d['g']+':'+'/'.join(sorted(paid))
    st['G:'+d['g']]+=1
    for r in ['NR','NU','NP','AU','AP','AR','BU','BP','BR']:
        pass
    sig=frozenset(paid)
    st[('sig',d['g'],tuple(sorted(sig)))]+=1
for k,v in sorted(st.items(),key=lambda x:str(x[0])):
    if v: print(k,v)
