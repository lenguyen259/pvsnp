# monotone fan-in-2 circuit SAT on key rows (min true pts, max false pts, V-v), exact by monotonicity.
# usage: msat.py EDGES_JSON size [--maxor k] [--maxand k] [--lemd] [--v2only] [--brk pet] [--timeout s]
import sys, json, time, argparse, threading
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from rows import key_rows
ap=argparse.ArgumentParser(); ap.add_argument('E'); ap.add_argument('s',type=int)
ap.add_argument('--maxor',type=int); ap.add_argument('--maxand',type=int)
ap.add_argument('--lemd',action='store_true'); ap.add_argument('--v2only',action='store_true')
ap.add_argument('--brk'); ap.add_argument('--full',action='store_true'); ap.add_argument('--timeout',type=int,default=2400)
A=ap.parse_args()
E=[tuple(e) for e in json.loads(A.E)]; n=max(max(e) for e in E)+1; s=A.s; t0=time.time()
T,F,D=key_rows(n,E); rows=list(range(1<<n)) if A.full else sorted(set(T+F+D)); R=len(rows); ridx={r:i for i,r in enumerate(rows)}
pool=IDPool(); cl=[]; N=n+s
op=lambda i: pool.id(('o',i))      # true = AND
def val(i,t):
    if i<n: return bool((rows[t]>>i)&1)
    return pool.id(('v',i,t))
def add(lits):
    out=[]
    for l in lits:
        if l is True: return
        if l is False: continue
        out.append(l)
    cl.append(out)
neg=lambda l: (not l) if isinstance(l,bool) else -l
L=lambda i,j: pool.id(('L',i,j)); Rr=lambda i,k: pool.id(('R',i,k))
for i in range(n,N):
    ls=[L(i,j) for j in range(i-1)]; rs=[Rr(i,k) for k in range(1,i)]
    cl.append(ls); cl.append(rs)
    cl.extend(CardEnc.equals(lits=ls,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses) if False else None
    cl.extend(CardEnc.atmost(lits=ls,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    cl.extend(CardEnc.atmost(lits=rs,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    for j in range(i-1):   # left < right
        cl.append([-L(i,j)]+[Rr(i,k) for k in range(j+1,i)])
    for t in range(R):
        a=pool.id(('a',i,t)); b=pool.id(('b',i,t)); c=val(i,t)
        for j in range(i-1):
            add([-L(i,j),neg(val(j,t)),a]); add([-L(i,j),val(j,t),-a])
        for k in range(1,i):
            add([-Rr(i,k),neg(val(k,t)),b]); add([-Rr(i,k),val(k,t),-b])
        o=op(i)
        add([-o,-a,-b,c]); add([-o,a,neg(c)]); add([-o,b,neg(c)])
        add([o,-a,c]); add([o,-b,c]); add([o,a,b,neg(c)])
f=lambda r: any((r>>a)&1 and (r>>b)&1 for a,b in E)
for t,r in enumerate(rows): add([val(N-1,t)] if f(r) else [neg(val(N-1,t))])
# every non-output gate used
for g in range(n,N-1):
    cl.append([L(i,g) for i in range(g+1,N)]+[Rr(i,g) for i in range(g+1,N)])
# canonical order: if gate i+1 does not use i, then (left,right) of i <= that of i+1 lexicographically (weakly: left_i <= left_{i+1})
for i in range(n,N-1):
    for j in range(i-1):
        for j2 in range(j):
            # L(i,j) & L(i+1,j2) & not uses(i+1,i) -> false  (i+1 uses i only as right since left<right... left could be i? left<right<=i so left<=i-1)
            cl.append([-L(i,j),-L(i+1,j2),Rr(i+1,i)])
if A.full:
    for i in range(n,N):
        for j in range(i):
            lits=[]
            for t in range(R):
                x=pool.id(('x',i,j,t)); lits.append(x); a,b=val(i,t),val(j,t)
                add([-x,a,b]); add([-x,neg(a),neg(b)])
            cl.append(lits)
# no two gates identical (op,left,right): skip (implied mostly). Petersen symmetry: first gate inputs (0,1) or (0,2)
if A.brk=='pet':
    cl.append([L(n,0)]); cl.append([Rr(n,1),Rr(n,2)])
ors=[-op(i) for i in range(n,N)]; ands=[op(i) for i in range(n,N)]
if A.maxor is not None: cl.extend(CardEnc.atmost(lits=ors,bound=A.maxor,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.maxand is not None: cl.extend(CardEnc.atmost(lits=ands,bound=A.maxand,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.lemd:
    deg={v:sum(1 for e in E if v in e) for v in range(n)}
    for v in range(n):
        if deg[v]==0 or (A.v2only and deg[v]!=2): continue
        tv=ridx[((1<<n)-1)^(1<<v)]
        chs=[]
        for i in range(n,N):
            c=pool.id(('ch',i,v)); chs.append(c)
            a=pool.id(('a',i,tv)); b=pool.id(('b',i,tv))
            # input dominated by v  <=> its value at V-v is 0
            cl.append([op(i),a,c]); cl.append([op(i),b,c])
        cl.extend(CardEnc.atmost(lits=chs,bound=(1 if A.v2only else deg[v]-1),vpool=pool,encoding=EncType.seqcounter).clauses)
nv=pool.top; S=Cadical153(bootstrap_with=cl)
print('vars',nv,'clauses',len(cl),'rows',R,flush=True)
timer=threading.Timer(A.timeout,lambda: S.interrupt()); timer.start()
res=S.solve_limited(expect_interrupt=True); timer.cancel(); model=None
if res:
    m=set(l for l in S.get_model() if l>0); model=[]
    for i in range(n,N):
        j=[j for j in range(i-1) if L(i,j) in m][0]; k=[k for k in range(1,i) if Rr(i,k) in m][0]
        model.append((i,'&' if op(i) in m else '|',j,k))
print(json.dumps(E),s,vars(A),'RESULT',{True:'SAT',False:'UNSAT',None:'TIMEOUT'}[res],model,'%.0fs'%(time.time()-t0),flush=True)
