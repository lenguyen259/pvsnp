"""enum: all minimum monotone circuits of f_{C_n} (size n+ceil(n/2)-1), one per DAG (depth-canonical order).
Sound for minimum circuits: test set (edges=1, maximal independent sets=0), gates distinct & nonconstant on it, all used."""
import sys,json,time,itertools
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
import pysat.solvers as PS
# andsat: is there a monotone circuit for f_G with s gates and at most amax AND gates? (G given as edge list)
E=[tuple(map(int,e.split('-'))) for e in sys.argv[1].split(',')]; n=1+max(max(e) for e in E)
s=int(sys.argv[2]); amax=int(sys.argv[3]); out=sys.argv[4]; tlim=float(sys.argv[5])
fG=lambda r: any((r>>a)&1 and (r>>b)&1 for a,b in E)
rows=[(1<<a)|(1<<b) for a,b in E]
for r in range(1<<n):
    if not fG(r) and all(fG(r|(1<<v)) for v in range(n) if not (r>>v)&1): rows.append(r)
R=len(rows); N=n+s
pool=IDPool(); cl=[]
op=lambda i: pool.id(('o',i))
def val(i,t):
    if i<n: return bool((rows[t]>>i)&1)
    return pool.id(('v',i,t))
neg=lambda l: (not l) if isinstance(l,bool) else -l
def add(lits):
    o=[]
    for l in lits:
        if l is True: return
        if l is False: continue
        o.append(l)
    assert o; cl.append(o)
pairs={i:[(j,k) for j in range(i) for k in range(j+1,i)] for i in range(n,N)}
sv=lambda i,j,k: pool.id(('s',i,j,k))
for i in range(n,N):
    ss=[sv(i,j,k) for j,k in pairs[i]]; cl.append(ss)
    cl.extend(CardEnc.atmost(lits=ss,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    o=op(i)
    for t in range(R):
        c=val(i,t)
        for j,k in pairs[i]:
            a,b=val(j,t),val(k,t); z=sv(i,j,k)
            # o=AND: c=a&b ; o=OR: c=a|b
            add([-z,-o,neg(a),neg(b),c]); add([-z,-o,a,neg(c)]); add([-z,-o,b,neg(c)])
            add([-z,o,neg(a),c]); add([-z,o,neg(b),c]); add([-z,o,a,b,neg(c)])
for t,r in enumerate(rows): add([val(N-1,t)] if fG(r) else [neg(val(N-1,t))])
for gt in range(n,N-1): cl.append([sv(i,j,k) for i in range(gt+1,N) for j,k in pairs[i] if gt in (j,k)])
for i in range(n,N):
    add([val(i,t) for t in range(R)]); add([neg(val(i,t)) for t in range(R)])
    for j in range(i):
        ds=[]
        for t in range(R):
            x,y=val(i,t),val(j,t)
            if isinstance(y,bool): ds.append(neg(x) if y else x); continue
            d=pool.id(('d',i,j,t)); add([-d,x,y]); add([-d,-x,-y]); ds.append(d)
        add(ds)
D=s
dep=lambda i,d: pool.id(('dp',i,d))
def depl(i,d):
    if d<=0: return True
    if i<n: return False
    if d==1: return True
    if d>D: return False
    return dep(i,d)
for i in range(n,N):
    for j,k in pairs[i]:
        x=sv(i,j,k)
        for d in range(1,D+1):
            add([-x,neg(depl(i,d+1)),depl(j,d),depl(k,d)])
            add([-x,depl(i,d+1),neg(depl(j,d))]); add([-x,depl(i,d+1),neg(depl(k,d))])
    for d in range(2,D): cl.append([-dep(i,d+1),dep(i,d)])
Pq=lambda i,q: pool.id(('P',i,q))
for i in range(n,N-1):
    for d in range(2,D+1): add([neg(depl(i,d)),depl(i+1,d)])
    eq=pool.id(('eq',i))
    for d in range(1,D+1):
        add([depl(i,d),neg(depl(i+1,d)),-eq]); add([neg(depl(i,d)),depl(i+1,d+1),eq])
for i in range(n,N):
    Q=len(pairs[i])
    for q in range(Q):
        j,k=pairs[i][q]; cl.append([-sv(i,j,k),Pq(i,q)])
        if q+1<Q: cl.append([-sv(i,j,k),-Pq(i,q+1)]); cl.append([-Pq(i,q+1),Pq(i,q)]); cl.append([-Pq(i,q),sv(i,j,k),Pq(i,q+1)])
        else: cl.append([-Pq(i,q),sv(i,j,k)])
for i in range(n,N-1):
    eq=pool.id(('eq',i)); Q=len(pairs[i])
    for q in range(Q):
        j,k=pairs[i][q]
        if q>0: cl.append([-eq,-sv(i,j,k),Pq(i+1,q)])
        cl.append([-eq,-sv(i,j,k),-sv(i+1,j,k),op(i),-op(i+1)])
cl.extend(CardEnc.atmost(lits=[op(i) for i in range(n,N)],bound=amax,vpool=pool,encoding=EncType.seqcounter).clauses)
import threading
Sv=PS.Solver(name='cadical195',bootstrap_with=cl)
tm=threading.Timer(tlim,lambda: Sv.interrupt()); tm.start()
res=Sv.solve_limited(expect_interrupt=True); tm.cancel()
print('G',sys.argv[1],'s',s,'amax',amax,{True:'SAT',False:'UNSAT',None:'TIMEOUT'}[res],flush=True)
if res:
    m=set(l for l in Sv.get_model() if l>0); c=[]
    for i in range(n,N):
        (j,k),=[(j,k) for j,k in pairs[i] if sv(i,j,k) in m]; c.append('%d=%d%s%d'%(i,j,'&' if op(i) in m else '|',k))
    print('CIRCUIT',' '.join(c),flush=True)
sys.exit(0)
full=(1<<(1<<n))-1
X=[sum(1<<m for m in range(1<<n) if (m>>u)&1) for u in range(n)]
fT=sum(1<<m for m in range(1<<n) if fG(m))
t0=time.time(); cnt=0; keys=set()
with open(out,'w') as F:
  while time.time()-t0<tlim and Sv.solve():
    m=set(l for l in Sv.get_model() if l>0); c=[]; bl=[]
    for i in range(n,N):
        (j,k),=[(j,k) for j,k in pairs[i] if sv(i,j,k) in m]
        o='&' if op(i) in m else '|'; c.append((i,o,j,k)); bl+=[-sv(i,j,k), -op(i) if o=='&' else op(i)]
    Sv.add_clause(bl)
    T=X[:]+[0]*s
    for i,o,j,k in c: T[i]=(T[j]&T[k]) if o=='&' else (T[j]|T[k])
    assert T[N-1]==fT
    key=frozenset((T[i],o,T[j],T[k]) for i,o,j,k in c)
    if key in keys: continue
    keys.add(key); cnt+=1
    F.write(' '.join('%d=%d%s%d'%(i,j,o,k) for i,o,j,k in c)+'\n'); F.flush()
print('n',n,'s',s,'count',cnt,'done' if time.time()-t0<tlim else 'TIMELIMIT','%.1fs'%(time.time()-t0))
