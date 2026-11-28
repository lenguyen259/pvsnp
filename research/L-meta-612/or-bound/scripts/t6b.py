import collections
from tr import *
H=collections.Counter(); seen=set(); ex={}; TC={}
for fn,n,E,X,c in load(DIRS):
    key=(tuple(E),tuple(c))
    if key in seen: continue
    seen.add(key)
    sup=sorted({x for e in E for x in e})
    if tuple(E) not in TC:
        t=tau(E); TC[tuple(E)]=(t,{v:tau([e for e in E if v not in e]) for v in sup})
    t,tv=TC[tuple(E)]
    R,V,out=breduce(n,c); a,o=counts(R)
    hard=all(tv[v]==t-1 for v in sup)
    best=-9; bestdom=-9
    for v in sup:
        Rv,Vv,ov=breduce(n,c,dead=(v,)); av,_=counts(Rv)
        best=max(best,(a-av)-(t-tv[v]))
        dom=0
        bestdom=max(bestdom,min(dom,1)-(t-tv[v]))
    k=(hard,a-t,best>=0,bestdom>=0); H[k]+=1; ex.setdefault(k,(E,c))
for k in sorted(H): print(k,H[k],ex[k] if not k[2] or not k[3] else '')
