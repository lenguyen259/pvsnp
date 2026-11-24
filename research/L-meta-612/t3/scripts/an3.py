import json,sys,collections
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t2/scripts')
from t2lib import Graph
from collections import deque
def dist(g,s):
    d={s:0};q=deque([s])
    while q:
        x=q.popleft()
        for y in g.N[x]:
            if y not in d: d[y]=d[x]+1; q.append(y)
    return d
st=collections.Counter(); ex={}; G={}
for l in open(sys.argv[1]):
    D=json.loads(l)
    if len(sys.argv)>2 and D['g']!=sys.argv[2]: continue
    key=tuple(map(tuple,D['E']))
    if key not in G: G[key]=Graph(key)
    g=G[key]
    good={(a,v) for a,v,e,nd in D['good']}
    for v in g.sup:
        if len(g.N[v])!=1: continue
        u=next(iter(g.N[v]))
        if len(g.N[u])<3: continue
        if ('N',v) in good or ('B',u) in good or ('A',u) in good: continue
        dd=dist(g,v)
        desc=tuple(sorted((a, dd[w], 'leaf' if len(g.N[w])==1 else 'deg%d'%len(g.N[w])) for a,w in good))
        st[(D['g'],desc)]+=1
        ex.setdefault((D['g'],desc),(D['s'],D['c'],v))
for k,v in st.most_common(40): print(v,k,ex[k])
