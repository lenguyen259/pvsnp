# search circuit of size s for f_G with  B2 + m0e <= |E|-1  (violates (B), since m0c <= m0e)
import sys, json, time
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/e612')
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from mcsat import target_tt
from lib import phiE, fmt
def search(n,E,s):
    tt=target_tt(n,E); pool=IDPool(); cl=[]; N=n+s
    pairs={i:[(j,k) for j in range(i) for k in range(j+1,i)] for i in range(n,N)}
    sel=lambda i,p: pool.id(('s',i,p)); op=lambda i: pool.id(('o',i))
    def val(i,r):
        if i<n: return True if (r>>i)&1 else False
        return pool.id(('v',i,r))
    def add(lits):
        out=[]
        for l in lits:
            if l is True: return
            if l is False: continue
            out.append(l)
        cl.append(out)
    neg=lambda l: (not l) if isinstance(l,bool) else -l
    for i in range(n,N):
        lits=[sel(i,p) for p in range(len(pairs[i]))]; cl.append(lits)
        cl.extend(CardEnc.atmost(lits=lits,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
        for p,(j,k) in enumerate(pairs[i]):
            sp=sel(i,p); o=op(i)
            for r in range(1<<n):
                a,b,c=val(j,r),val(k,r),val(i,r)
                add([-sp,-o,neg(a),neg(b),c]); add([-sp,-o,a,neg(c)]); add([-sp,-o,b,neg(c)])
                add([-sp,o,neg(a),c]); add([-sp,o,neg(b),c]); add([-sp,o,a,b,neg(c)])
    for r in range(1<<n): add([val(N-1,r)] if tt[r] else [neg(val(N-1,r))])
    for g in range(n,N-1):
        cl.append([sel(i,p) for i in range(g+1,N) for p,(j,k) in enumerate(pairs[i]) if g in (j,k)])
    for i in range(n,N-1):
        for p,(j,k) in enumerate(pairs[i]):
            for q,(j2,k2) in enumerate(pairs[i+1]):
                if i not in (j2,k2) and (j2,k2)<(j,k): cl.append([-sel(i,p),-sel(i+1,q)])
    U=[1<<u for u in range(n)]
    ne=lambda j: True if j<n else pool.id(('ne',j))
    emp=lambda j: pool.id(('em',j))
    for j in range(n,N):
        for u in range(n): add([neg(val(j,U[u])),ne(j)])
        add([val(j,U[u]) for u in range(n)]+[emp(j)])
    cnt=[]
    for i in range(n,N):
        b=pool.id(('b',i)); c=pool.id(('c',i)); cnt+=[b,c]
        for p,(j,k) in enumerate(pairs[i]):
            sp=sel(i,p)
            for u in range(n):
                for v in range(u+1,n):
                    add([-sp,op(i),neg(ne(j)),neg(ne(k)),neg(val(i,U[u])),neg(val(i,U[v])),b])
            add([-sp,-op(i),neg(ne(j)),neg(ne(k)),-emp(i),c])
    cl.extend(CardEnc.atmost(lits=cnt,bound=len(E)-1+SL,vpool=pool,encoding=EncType.seqcounter).clauses)
    S=Cadical153(bootstrap_with=cl)
    if S.solve():
        m=set(l for l in S.get_model() if l>0); model=[]
        for i in range(n,N):
            for p,(j,k) in enumerate(pairs[i]):
                if sel(i,p) in m: model.append((i,'&' if op(i) in m else '|',j,k))
        return model
    return None
SL=int(sys.argv[3]) if len(sys.argv)>3 else 0
E=[tuple(e) for e in json.loads(sys.argv[1])]; X=int(sys.argv[2]); n=max(max(e) for e in E)+1
t0=time.time(); r=search(n,E,phiE(E)+X)
print(sys.argv[1],X,'VIOLATION '+fmt(r) if r else 'none','%.0fs'%(time.time()-t0),flush=True)
