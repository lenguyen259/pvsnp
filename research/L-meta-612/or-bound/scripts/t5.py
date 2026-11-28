import collections
from fractions import Fraction as Fr
from tr import *
H=collections.Counter(); seen=set(); ex={}
for fn,n,E,X,c in load(DIRS):
    key=(tuple(E),tuple(c))
    if key in seen: continue
    seen.add(key)
    sup=sorted({x for e in E for x in e})
    ds={v:deg(E,v) for v in sup}
    if min(ds.values())<2: continue
    R,V,out=reduce(n,c); a,o=counts(R)
    ch={}
    for v in sup:
        isd=lambda q: V[q][0]<=frozenset([v]) and all(v in p for p in V[q][1])
        ch[v]=sum(1 for i,(op,j,k) in R.items() if op=='|' and (isd(j) or isd(k)))
    s1=sum(ch.values())-(2*len(E)-len(sup))
    s2=sum(Fr(ch[v],ds[v]) for v in sup)-len(sup)
    k=(o-len(E)+1, min(s1,3), s2>=0); H[k]+=1; ex.setdefault(k,(E,c,ch))
for k in sorted(H): print(k,H[k], ex[k] if k[1]<=0 or not k[2] else '')
