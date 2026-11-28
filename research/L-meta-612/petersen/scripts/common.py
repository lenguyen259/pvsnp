import sys, itertools
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/orb')
from tr import breduce
PET=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
def tau(E):
    Vs=sorted({x for e in E for x in e})
    for k in range(len(Vs)+1):
        for T in itertools.combinations(Vs,k):
            s=set(T)
            if all(a in s or b in s for a,b in E): return k
def has_c4(n,E):
    N=[set() for _ in range(n)]
    for a,b in E: N[a].add(b); N[b].add(a)
    return any(len(N[a]&N[b])>=2 for a in range(n) for b in range(a+1,n))
def analyze(n,c,E,verbose=False):
    """exact Boolean check on all 2^n inputs; returns dict"""
    R,T,o=breduce(n,c)
    full=sum(1<<r for r in range(1<<n) if any((r>>a)&1 and (r>>b)&1 for a,b in E))
    ok=(T[o]==full)
    xv={v:sum(1<<r for r in range(1<<n) if (r>>v)&1) for v in range(n)}
    core=lambda q: {v for v in range(n) if T[q]&~xv[v]==0}
    ch={v:0 for v in range(n)}
    for i,(op,j,k) in R.items():
        if op=='|':
            for v in core(j)|core(k): ch[v]+=1
    nor=sum(1 for g in R.values() if g[0]=='|'); nand=len(R)-nor
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    return dict(ok=ok,size=len(R),nor=nor,nand=nand,ch=ch,deg=deg,
                slack=max(ch[v]-deg[v] for v in range(n) if deg[v]>0),
                R=R,out=o)
def fmt(R):
    return ' '.join('%d=%d%s%d'%(i,R[i][1],R[i][0],R[i][2]) for i in sorted(R))
class B:
    def __init__(s,n): s.c=[]; s.nx=n
    def g(s,op,j,k):
        i=s.nx; s.nx+=1; s.c.append((i,op,j,k)); return i
    def OR(s,L):
        cur=L[0]
        for x in L[1:]: cur=s.g('|',cur,x)
        return cur
def starcover(b,E,node,cover):
    """f_G on substituted nodes, via stars at cover vertices"""
    rest=list(E); terms=[]
    for h in cover:
        L=[q if p==h else p for p,q in rest if h in (p,q)]
        if not L: continue
        terms.append(b.g('&',node[h],b.OR([node[x] for x in L]))); rest=[e for e in rest if h not in e]
    assert not rest
    return b.OR(terms)
