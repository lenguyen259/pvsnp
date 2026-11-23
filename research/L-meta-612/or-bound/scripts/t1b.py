import collections
from tr import *
st=collections.Counter(); ex={}; seen=set()
for fn,n,E,X,c in load(DIRS):
    key=(tuple(E),tuple(c))
    if key in seen: continue
    seen.add(key)
    R,T,out=breduce(n,c); a,o=counts(R)
    slack=o-(len(E)-1)
    sup=sorted({x for e in E for x in e})
    best=-99; bestch=-99
    for v in sup:
        Rv,Tv,ov=breduce(n,c,dead=(v,)); av,oov=counts(Rv)
        d=deg(E,v); best=max(best,(o-oov)-d)
        xv=sum(1<<r for r in range(1<<n) if (r>>v)&1)
        ch=sum(1 for i,(op,j,k) in R.items() if op=='|' and ((T[j]&~xv)==0 or (T[k]&~xv)==0))
        bestch=max(bestch,ch-d)
    mind=min(deg(E,v) for v in sup)
    k=(mind>=2,slack,best>=0,bestch>=0); st[k]+=1; ex.setdefault(k,(E,c))
for k in sorted(st): print(k,st[k],ex[k] if (not k[2] or not k[3]) else '')
