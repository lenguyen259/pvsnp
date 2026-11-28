import json,sys,collections
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from t2lib import Graph
st=collections.Counter(); G={}; ex={}
for pool in sys.argv[1:]:
  for l in open(pool):
    D=json.loads(l)
    key=tuple(map(tuple,D['E']))
    if key not in G: G[key]=Graph(key)
    g=G[key]; good={(a,v) for a,v,e,nd in D['good']}
    for v in g.sup:
        if len(g.N[v])!=1: continue
        u=next(iter(g.N[v]))
        if len(g.N[u])<3: continue
        fl={k:(k[0],{'v':v,'u':u}[k[1]]) in good for k in ['Nv','Au','Bu','Nu','Bv']}
        st[(D['g'],'inst')]+=1
        for k,b in fl.items():
            if not b: st[(D['g'],'not'+k)]+=1
        if not (fl['Nv'] or fl['Bu'] or fl['Nu'] or fl['Au']): st[(D['g'],'FAIL4')]+=1; ex.setdefault(D['g'],(D['s'],D['c'],v))
        if not (fl['Nv'] or fl['Nu']): st[(D['g'],'FAIL_NvNu')]+=1
        if not (fl['Nv'] or fl['Bu'] or fl['Nu']): st[(D['g'],'FAIL_NvBuNu')]+=1
for k,v in sorted(st.items()): print(k,v)
print(ex)
