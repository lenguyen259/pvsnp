import json,sys,collections
from gen import *
from t3slack import FAM
st=collections.Counter(); G={}; ex={}; seen=set()
for pool in sys.argv[1:]:
  for l in open(pool):
    D=json.loads(l)
    if D['s']!=0 or D['c'] in seen: continue
    seen.add(D['c'])
    key=tuple(map(tuple,D['E']))
    if key not in G: G[key]=Graph(key)
    g=G[key]; c=parse(D['c'])
    for v in g.sup:
        if len(g.N[v])!=1: continue
        u=next(iter(g.N[v])); d=len(g.N[u])
        if d<3: continue
        rv=[x for x in c if v in x[2:]]
        if len(rv)!=1 or rv[0][1]!='|': continue
        gg=rv[0][0]; rg=[x for x in c if gg in x[2:]]
        if not (len(rg)==1 and rg[0][1]=='&'): continue
        Fu=[x for x in c if u in x[2:]]
        if len(Fu)!=1: continue
        typ='star' if Fu[0][0]==rg[0][0] else ('ORp' if Fu[0][1]=='|' else 'ANDp?')
        R={}
        for k,(S0,S1) in FAM(g,v,['ALLW']).items():
            r=gopt(g,c,S0,S1); R[k]=bool(r and r[2])
        st[(D['g'],typ,'inst')]+=1
        for k,b in R.items():
            if b: st[(D['g'],typ,k)]+=1
        pat=tuple(sorted(k for k,b in R.items() if b))
        ex.setdefault((D['g'],typ,pat),D['c']+' v=%d'%v)
for k,v in sorted(st.items()): print(k,v)
import pickle; pickle.dump(ex,open('an7ex.pkl','wb'))
