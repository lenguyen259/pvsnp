import json,sys,collections
from gen import *
from t3fuzz import getG
from collections import deque
def dist(g,s):
    d={s:0};q=deque([s])
    while q:
        x=q.popleft()
        for y in g.N[x]:
            if y not in d: d[y]=d[x]+1; q.append(y)
    return d
st=collections.Counter(); G={}; ex={}
for l in open(sys.argv[1]):
    D=json.loads(l); key=tuple(map(tuple,D['E']))
    if key not in G: G[key]=Graph(key)
    g=G[key]; c=parse(D['c'])
    for v in D['L']:
        u=next(iter(g.N[v]))
        rv=[x for x in c if v in x[2:]]; gg=rv[0][0]; rg=[x for x in c if gg in x[2:]]
        Fu=[x for x in c if u in x[2:]]
        typ=('i' if len(rg)==1 and rg[0][1]=='&' else 'noti')+'/F%d'%len(Fu)
        if len(Fu)==1: typ+=('star' if Fu[0][0]==rg[0][0] else ('ORp' if Fu[0][1]=='|' else 'ANDp'))
        dd=dist(g,v)
        goods=set((a,dd[w]) for a,w,e,nd in D['good'])
        st[(D['g'],D['s'],typ)]+=1
        for k in goods: st[(D['g'],'good',typ,k)]+=1
for k,v in sorted(st.items(),key=lambda kv:str(kv[0])): print(k,v)
