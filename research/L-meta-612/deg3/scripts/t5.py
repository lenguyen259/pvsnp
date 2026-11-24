import collections,sys,itertools
from lib import *
st=collections.Counter(); ex=[]
for n,E,c in data(maxdeg=3):
    sup=sorted({x for e in E for x in e}); deg={v:sum(1 for e in E if v in e) for v in sup}
    R,T,o=red(n,c); a0,o0=cnt(R)
    xv={v:sum(1<<r for r in range(1<<n) if (r>>v)&1) for v in range(n)}
    core=lambda q:{v for v in range(n) if T[q]&~xv[v]==0}
    chg={i:core(j)|core(k) for i,(op,j,k) in R.items() if op=='|'}
    md=max(deg.values())
    for a,b in E:
        if deg[a]==2 and deg[b]==2:
            rest=[e for e in E if a not in e and b not in e]
            if not rest: continue
            key='sub3' if md<=3 else 'big'
            st[key]+=1
            R1,_,_=red(n,c,{a:0,b:0}); s=o0-cnt(R1)[1]
            q=sum(1 for i in chg if chg[i]&{a,b})
            st[key+' sav>=3']+=s>=3; st[key+' Q>=3']+=q>=3
            if s<3 and len(ex)<6: ex.append((E,(a,b),' '.join('%d=%d%s%d'%(i,j,op,k) for i,op,j,k in c),q,s))
print(dict(st))
for e in ex: print(e)
