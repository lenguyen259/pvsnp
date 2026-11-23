import collections
from tr import *
st=collections.Counter(); seen=set(); H=collections.Counter()
for fn,n,E,X,c in load(DIRS):
    key=(tuple(E),tuple(c))
    if key in seen: continue
    seen.add(key)
    sup=sorted({x for e in E for x in e})
    ds={v:deg(E,v) for v in sup}
    if min(ds.values())<2: continue
    R,V,out=reduce(n,c); a,o=counts(R)
    good=[]
    for v in sup:
        ch=0
        for i,(op,j,k) in R.items():
            if op=='|':
                for q in (j,k):
                    S,P=V[q]
                    if S<=frozenset([v]) and all(v in p for p in P): ch+=1;break
        if ch>=ds[v]: good.append(v)
    md=min(ds.values())
    st[(tuple(E), max(ds.values()))]+=1
    H['mindeg good',any(ds[v]==md for v in good)]+=1
    H['maxdeg good',any(ds[v]==max(ds.values()) for v in good)]+=1
    H['ngood',len(good)]+=1
for k in st: print(k,st[k])
for k in sorted(H): print(k,H[k])
