import warnings; warnings.filterwarnings('ignore')
from gen import gen
from model import solve, build
from common import analyze, fmt, tau
res=[]
for n,E in gen():
    deg={v:sum(1 for e in E if v in e) for v in range(n)}; H=[v for v in range(n) if deg[v]>=3]
    hedge=sum(1 for a,b in E if a in H and b in H)
    r=solve(n,E,40)
    phi=len(E)+tau(E)-1
    best=None; K=40
    while r is not None:
        c=build(n,E,*r); a=analyze(n,c,E)
        if a['ok'] and a['slack']<=-1 and (best is None or a['size']<best['size']): best=a
        K-=1; r=solve(n,E,K)
    if best is None: res.append((len(H),n,hedge,'none',E)); continue
    a=best
    res.append((len(H),n,hedge,a['size']-phi,E,fmt(a['R']),a['ch'],[deg[v] for v in range(n)]))
import collections
for h in (2,3):
    for he in (0,1,2,3):
        L=[x for x in res if x[0]==h and x[2]==he]
        if not L: continue
        hit=[x for x in L if x[3]!='none']
        print('hubs',h,'hub-edges',he,'graphs',len(L),'LemmaD-cex',len(hit), 'min n with cex', min([x[1] for x in hit]) if hit else '-')
        for x in sorted(hit,key=lambda x:(x[1],x[3]))[:2]: print('   n',x[1],'size-Phi',x[3],x[4]); print('     ',x[5]); print('     ch',x[6],'deg',x[7])
