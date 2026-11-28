import collections
from tr import *
st=collections.Counter(); ex={}
seen=set()
for fn,n,E,X,c in load(DIRS):
    key=(tuple(E),tuple(c))
    if key in seen: continue
    seen.add(key)
    R,V,out=reduce(n,c)
    a,o=counts(R)
    assert V[out][1]==frozenset(frozenset(e) for e in E) and not V[out][0]
    slack=o-(len(E)-1)
    sup=sorted({x for e in E for x in e})
    best=-99; bestch=-99
    for v in sup:
        Rv,Vv,ov=reduce(n,c,dead=(v,))
        av,oov=counts(Rv)
        Ev=[e for e in E if v not in e]
        assert oov>=len(Ev)-1 or not Ev, (E,c,v)
        d=deg(E,v)
        best=max(best,(o-oov)-d)
        ch=0
        for i,(op,j,k) in R.items():
            if op=='|':
                for q in (j,k):
                    S,P=V[q]
                    if S<=frozenset([v]) and all(v in p for p in P): ch+=1;break
        bestch=max(bestch,ch-d)
    mind=min(deg(E,v) for v in sup)
    k=(mind>=2,slack,best,bestch)
    st[k]+=1
    if k not in ex: ex[k]=(E,c)
for k in sorted(st): print(k,st[k],ex[k] if (k[2]<0 or k[3]<0) and k[0] else '')
