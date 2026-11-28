import collections
from tr import *
H=collections.Counter(); ex={}; seen=set()
for fn,n,E,X,c in load(DIRS):
    key=(tuple(E),tuple(c))
    if key in seen or len(E)<2: continue
    seen.add(key)
    sup=sorted({x for e in E for x in e})
    R,T,out=breduce(n,c)
    good=set()
    for v in sup:
        xv=sum(1<<r for r in range(1<<n) if (r>>v)&1)
        ch=sum(1 for i,(op,j,k) in R.items() if op=='|' and ((T[j]&~xv)==0 or (T[k]&~xv)==0))
        if ch>=deg(E,v): good.add(v)
    md=min(deg(E,v) for v in sup)>=2
    for name,val in [('goodcover',all(a in good or b in good for a,b in E)),
                     ('badindep',all(a in good or b in good for a,b in E)),
                     ('goodindep',all(not(a in good and b in good) for a,b in E)),
                     ('everyleafgood',all(v in good for v in sup if deg(E,v)==1))]:
        H[(md,name,val)]+=1; ex.setdefault((md,name,val),(E,c,good))
for k in sorted(H): print(k,H[k],ex[k] if not k[2] else '')
