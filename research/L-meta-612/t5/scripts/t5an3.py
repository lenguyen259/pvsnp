import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t5')
from t5an import *
import collections
def eNa(g,X): return sum(1 for e in g.E if e[0] in X or e[1] in X)
def row(g,c,v):
    X=g.N[v]|{v}; H=g.Eminus(X)
    if not H: return None
    nd=g.P-phi(H); D,dD=Dsets(g,c,X); rho={x:0 for x in X}
    return dict(v=v,need=nd,elim=elim(g,c,rho),L1=len(D|dD),Lt=Ltop(g,c,X),eN=eNa(g,X),drop=g.t-tau(H),deg=len(g.N[v]))
if __name__=='__main__':
    stats=collections.Counter(); ex=[]
    for d in load(sys.argv[1:]):
        g=Graph(d['E']); c=parse(d['c'])
        for rec in d['rec']:
            i,a,b=rec[:3]; R=[row(g,c,v) for v in (a,b)]
            for r in R:
                if r is None: stats['noH']+=1; continue
                stats['pairs']+=1
                for k in ('elim','L1','Lt','eN'):
                    if r[k]>=r['need']: stats[k+'>=need']+=1
                if r['L1']>=r['eN']: stats['L1>=eN']+=1
                if r['elim']<r['need'] or r['Lt']<r['need']: ex.append((d['g'],d['s'],d['c'],r))
            R=[r for r in R if r]
            stats['inst']+=1
            if any(r['elim']>=r['need'] for r in R): stats['someN']+=1
            if all(r['elim']>=r['need'] for r in R): stats['bothN']+=1
            if any(r['L1']>=r['need'] for r in R): stats['someL1']+=1
            if any(r['Lt']>=r['need'] for r in R): stats['someLt']+=1
            stats['s=%d'%d['s']]+=1
    print(dict(stats))
    for x in ex[:20]: print(x)
