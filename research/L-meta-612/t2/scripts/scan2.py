import collections
from t2lib import *
st=collections.Counter(); seen=set(); ex={}
for fn,n,E,c in load_cached():
    g=Graph(E,n)
    if g.t==1: continue
    c=renum(n,red(g,c)); k=(g.E,tuple(c))
    if k in seen: continue
    seen.add(k); st['circ']+=1
    S=set()
    for i in minimal_ands(c): S|=support(g,c,i)
    r=evaluate(g,c)
    good={(a,v) for a,v,e,nd,ok_ in r if ok_}
    for nm,kinds,loc in [('mANB','ANB',1),('mAB','AB',1),('AB','AB',0),('mA','A',1),('mB','B',1)]:
        if any(a in kinds and (not loc or v in S) for a,v in good): st[nm]+=1
        else:
            st['F_'+nm]+=1; d=len(c)-g.P
            if (nm,d) not in ex: ex[(nm,d)]=(g.E,fmt(c))
print(dict(st))
for k in sorted(ex): print(k,ex[k])
