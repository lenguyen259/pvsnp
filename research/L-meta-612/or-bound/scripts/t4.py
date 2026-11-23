import collections
from tr import *
H=collections.Counter(); seen=set(); ex={}; C2=collections.Counter()
for fn,n,E,X,c in load(DIRS):
    key=(tuple(E),tuple(c))
    if key in seen: continue
    seen.add(key)
    sup=sorted({x for e in E for x in e})
    ds={v:deg(E,v) for v in sup}
    if min(ds.values())<2: continue
    R,V,out=reduce(n,c)
    feats={}
    for v in sup:
        isd=lambda q: V[q][0]<=frozenset([v]) and all(v in p for p in V[q][1])
        ch=sum(1 for i,(op,j,k) in R.items() if op=='|' and (isd(j) or isd(k)))
        rA=any(op=='&' and v in (j,k) for i,(op,j,k) in R.items())
        big=any(isd(i) and len(V[i][1])>=2 for i in R)
        bigr=any(op=='|' and any(isd(q) and len(V[q][1])>=2 and q in R for q in (j,k)) for i,(op,j,k) in R.items())
        good=ch>=ds[v]
        k=(rA,big,good); H[k]+=1; ex.setdefault(k,(E,c,v))
        feats[v]=(rA,big,good)
    C2['exists nonbig', any(not f[1] for f in feats.values())]+=1
    C2['exists nonbig good', any((not f[1]) and f[2] for f in feats.values())]+=1
    C2['all nonbig good', all(f[2] for f in feats.values() if not f[1])]+=1
for k in sorted(H): print(k,H[k],ex[k] if (not k[1] and not k[2]) else '')
for k in sorted(C2): print(k,C2[k])
