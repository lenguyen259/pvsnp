import collections,sys
from lib import *
st=collections.Counter(); ex=collections.defaultdict(list)
for n,E,c in data():
    sup=sorted({x for e in E for x in e}); deg={v:sum(1 for e in E if v in e) for v in sup}
    if min(deg.values())<2: continue
    R,T,o=red(n,c); a0,o0=cnt(R)
    so={}
    for v in sup:
        R1,_,_=red(n,c,{v:0}); a1,o1=cnt(R1); so[v]=o0-o1
    st['n']+=1
    bad=[v for v in sup if deg[v]==2 and so[v]<2]
    hubs=[v for v in sup if deg[v]==3]
    st['hashub']+=bool(hubs)
    if bad:
        st['has bad deg2']+=1
        if hubs: st['bad&hub']+=1
        if len(ex[tuple(E)])<2: ex[tuple(E)].append((' '.join('%d=%d%s%d'%(i,j,op,k) for i,op,j,k in c),so))
    st['all deg2 bad']+=all(so[v]<2 for v in sup if deg[v]==2)
print(dict(st))
for k,v in ex.items():
    for e in v: print(k,e)
