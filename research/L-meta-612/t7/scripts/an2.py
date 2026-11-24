"""|Top| distribution; circuits where every option has |Top|=1; averaging sums; LT_N >= e(N[a])."""
from lib7 import *
import time
secs=float(sys.argv[1]); st=collections.Counter(); t0=time.time(); allone=[]; mins={}
topdist=collections.Counter()
for src,d in pools():
    if time.time()-t0>secs: break
    g=Graph(d['E']); c=parse(d['c']); st['circ']+=1
    sums=collections.Counter(); maxtop=0
    for nm,v,rho,need in g.options():
        K,cp,Tp,T=parts(g,c,rho)
        lo=len(K|cp); lt=len(K|cp|Tp)-1
        topdist[(nm,len(Tp))]+=1; maxtop=max(maxtop,len(Tp-K-cp))
        sums[nm]+=lo-need; sums[nm+'_lt']+=lt-need
        if nm=='N':
            X=g.N[v]|{v}; eN=sum(1 for e in g.E if e[0] in X or e[1] in X)
            st['Npairs']+=1; st['LT>=eN']+= lt>=eN; st['LO>=eN']+=lo>=eN
    if maxtop<=1:
        st['all_top_trivial']+=1
        if len(allone)<1 or len(c)<len(allone[0][2].split()): allone=[(src,d['E'],d['c'])]
    for k,x in sums.items():
        st[k+'>=0']+= x>=0
        if k not in mins or x<mins[k][0]: mins[k]=(x,d.get('g'),d['c'])
print(dict(st)); print(sorted(topdist.items())[:40]); print(allone)
for k in mins: print(k,mins[k][:2])
