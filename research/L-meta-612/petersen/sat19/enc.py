# monotone fan-in-2 circuit SAT for f_G (Petersen), rows = edges (1) + maximal independent sets (0) [+ singletons (0)]
import sys, json, time, argparse, itertools
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
import pysat.solvers as PS
PET=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
ap=argparse.ArgumentParser(); ap.add_argument('s',type=int)
ap.add_argument('--rep',type=int,default=-1); ap.add_argument('--solver',default='cadical195')
ap.add_argument('--sing',action='store_true'); ap.add_argument('--viol',action='store_true')
ap.add_argument('--nor',type=int); ap.add_argument('--maxor',type=int); ap.add_argument('--nand',type=int)
ap.add_argument('--nodist',action='store_true'); ap.add_argument('--outor',action='store_true')
ap.add_argument('--fix',help='json list of (op,j,k) prefix gates to force'); ap.add_argument('--dimacs')
A=ap.parse_args()
E=PET; n=10; s=A.s; N=n+s; t0=time.time()
Es=set(E)|{(b,a) for a,b in E}
f=lambda r: any((r>>a)&1 and (r>>b)&1 for a,b in E)
T=[(1<<a)|(1<<b) for a,b in E]
F=[r for r in range(1<<n) if not f(r) and all(f(r|(1<<v)) for v in range(n) if not (r>>v)&1)]
S=[1<<u for u in range(n)] if (A.sing or A.viol) else []
rows=T+F+S; R=len(rows); sidx={u:len(T)+len(F)+u for u in range(n)}
pool=IDPool(); cl=[]
op=lambda i: pool.id(('o',i))      # true = AND
L=lambda i,j: pool.id(('L',i,j)); Rr=lambda i,k: pool.id(('R',i,k))
def val(i,t):
    if i<n: return bool((rows[t]>>i)&1)
    return pool.id(('v',i,t))
neg=lambda l: (not l) if isinstance(l,bool) else -l
def add(lits):
    out=[]
    for l in lits:
        if l is True: return
        if l is False: continue
        out.append(l)
    assert out, lits
    cl.append(out)
aV=lambda i,t: pool.id(('a',i,t)); bV=lambda i,t: pool.id(('b',i,t))
for i in range(n,N):
    ls=[L(i,j) for j in range(i-1)]; rs=[Rr(i,k) for k in range(1,i)]
    cl.append(ls); cl.append(rs)
    cl.extend(CardEnc.atmost(lits=ls,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    cl.extend(CardEnc.atmost(lits=rs,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    for j in range(i-1): cl.append([-L(i,j)]+[Rr(i,k) for k in range(j+1,i)])
    for t in range(R):
        a=aV(i,t); b=bV(i,t); c=val(i,t)
        for j in range(i-1): add([-L(i,j),neg(val(j,t)),a]); add([-L(i,j),val(j,t),-a])
        for k in range(1,i): add([-Rr(i,k),neg(val(k,t)),b]); add([-Rr(i,k),val(k,t),-b])
        o=op(i)
        add([-o,-a,-b,c]); add([-o,a,neg(c)]); add([-o,b,neg(c)])
        add([o,-a,c]); add([o,-b,c]); add([o,a,b,neg(c)])
for t,r in enumerate(rows): add([val(N-1,t)] if f(r) else [neg(val(N-1,t))])
if A.outor: cl.append([-op(N-1)])
for g in range(n,N-1): cl.append([L(i,g) for i in range(g+1,N)]+[Rr(i,g) for i in range(g+1,N)])
# distinct from every earlier node on rows, nonconstant (sound for minimum circuits)
if not A.nodist:
    for i in range(n,N):
        add([val(i,t) for t in range(R)]); add([neg(val(i,t)) for t in range(R)])
        for j in range(i):
            ds=[]
            for t in range(R):
                d=pool.id(('d',i,j,t)); x,y=val(i,t),val(j,t)
                if isinstance(y,bool): ds.append(neg(x) if y else x); continue
                add([-d,x,y]); add([-d,-x,-y]); ds.append(d)
            add(ds)
# lex order of consecutive independent gates (skip gate n if rep fixes it)
st=n+1 if A.rep>=0 else n
for i in range(st,N-1):
    for j in range(i-1):
        for j2 in range(j): cl.append([-L(i,j),-L(i+1,j2),Rr(i+1,i)])
        for k in range(j+1,i):
            for k2 in range(j+1,k): cl.append([-L(i,j),-L(i+1,j),-Rr(i,k),-Rr(i+1,k2)])
            cl.append([-L(i,j),-L(i+1,j),-Rr(i,k),-Rr(i+1,k),op(i)])
            cl.append([-L(i,j),-L(i+1,j),-Rr(i,k),-Rr(i+1,k),-op(i+1)])
# first-gate orbit representative; types: 0 AND-edge,1 AND-nonedge,2 OR-edge,3 OR-nonedge
if A.rep>=0:
    typ=lambda o,j,k: (0 if o else 2)+(0 if (j,k) in Es else 1)
    pr=(0,1) if A.rep in (0,2) else (0,2)
    cl.append([L(n,pr[0])]); cl.append([Rr(n,pr[1])]); cl.append([op(n)] if A.rep<2 else [-op(n)])
    for i in range(n+1,N):
        for j in range(n):
            for k in range(j+1,n):
                for o in (1,0):
                    if typ(o,j,k)<A.rep: cl.append([-L(i,j),-Rr(i,k),(-op(i) if o else op(i))])
# non-STAR-ALL (Theorem S + S2: size<Phi => some AND violates N1 or N3)
if A.viol:
    VS=[]
    for h in range(n,N):
        w=pool.id(('w',h)); VS.append(w); cl.append([-w,op(h)])
        alts=[val(h,sidx[u]) for u in range(n)]
        for u in range(n):
            for v in range(n):
                if u!=v and (u,v) not in Es:
                    p=pool.id(('p',h,u,v)); alts.append(p)
                    cl.append([-p,aV(h,sidx[u])]); cl.append([-p,bV(h,sidx[v])])
        cl.append([-w]+alts)
    cl.append(VS)
ors=[-op(i) for i in range(n,N)]
if A.nor is not None: cl.extend(CardEnc.equals(lits=ors,bound=A.nor,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.maxor is not None: cl.extend(CardEnc.atmost(lits=ors,bound=A.maxor,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.nand is not None: cl.extend(CardEnc.equals(lits=[-x for x in ors],bound=A.nand,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.fix:
    for idx,(o,j,k) in enumerate(json.loads(A.fix)):
        i=n+idx; cl+= [[L(i,j)],[Rr(i,k)],[op(i) if o=='&' else -op(i)]]
print('s',s,'rows',R,'(T%d F%d S%d)'%(len(T),len(F),len(S)),'vars',pool.top,'clauses',len(cl),vars(A),flush=True)
if A.dimacs:
    with open(A.dimacs,'w') as fh:
        fh.write('p cnf %d %d\n'%(pool.top,len(cl)))
        for c in cl: fh.write(' '.join(map(str,c))+' 0\n')
    json.dump({'L':{str(i):{str(j):L(i,j) for j in range(i-1)} for i in range(n,N)},'R':{str(i):{str(k):Rr(i,k) for k in range(1,i)} for i in range(n,N)},'op':{str(i):op(i) for i in range(n,N)}},open(A.dimacs+'.map','w'))
    sys.exit()
Sv=PS.Solver(name=A.solver,bootstrap_with=cl); res=Sv.solve()
model=None
if res:
    m=set(l for l in Sv.get_model() if l>0); model=[]
    for i in range(n,N):
        j=[j for j in range(i-1) if L(i,j) in m][0]; k=[k for k in range(1,i) if Rr(i,k) in m][0]
        model.append(('&' if op(i) in m else '|',j,k))
    # brute-force verification on all 2^n inputs
    ok=True
    for r in range(1<<n):
        v=[(r>>u)&1 for u in range(n)]
        for o,j,k in model: v.append(v[j]&v[k] if o=='&' else v[j]|v[k])
        if v[-1]!=f(r): ok=False; break
    print('VERIFIED' if ok else 'VERIFY-FAIL', ' '.join('%d=%d%s%d'%(n+i,j,o,k) for i,(o,j,k) in enumerate(model)))
print('RESULT',{True:'SAT',False:'UNSAT'}[res],'%.1fs'%(time.time()-t0),flush=True)
