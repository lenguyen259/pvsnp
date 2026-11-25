# enc5: exact monotone AND/OR circuit synthesis for f_G (default Petersen), size exactly s.
# Scheme: per gate i a left selector l(i,j) and right selector r(i,k) (j<k), child-value variables L(i,t),R(i,t),
# gate values on a set of rows. Every constraint below is satisfied by (an automorphic image of) every
# MINIMUM circuit put in depth-canonical order; see README.md for the soundness argument of each flag.
import sys, json, time, argparse, itertools
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
ap=argparse.ArgumentParser(); ap.add_argument('s',type=int)
ap.add_argument('--graph'); ap.add_argument('--rest',help='json file: list of [A,B,andL,orL,totL]')
ap.add_argument('--nodist',action='store_true'); ap.add_argument('--nocanon',action='store_true')
ap.add_argument('--symb',action='store_true',help='Petersen: first gate pair (0,1), or (0,2) and no depth-1 gate on an edge')
ap.add_argument('--factc',action='store_true'); ap.add_argument('--viol',action='store_true')
ap.add_argument('--fixc',help='json canonical circuit [[op,j,k],...] to impose (validation)')
ap.add_argument('--partial',help='json list of [gateidx,op,j,k] (op may be "?") to impose')
ap.add_argument('--cube',help='json list of literal specs')
ap.add_argument('--nand',type=int); ap.add_argument('--nor',type=int); ap.add_argument('--maxand',type=int); ap.add_argument('--minand',type=int)
ap.add_argument('--outop',choices=['&','|'])
ap.add_argument('--dimacs'); ap.add_argument('--solve',action='store_true'); ap.add_argument('--solver',default='cadical195')
ap.add_argument('--timeout',type=float); ap.add_argument('--meta')
A=ap.parse_args()
PET=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
E=[tuple(e) for e in json.loads(A.graph)] if A.graph else PET
n=max(max(e) for e in E)+1; s=A.s; N=n+s; t0=time.time()
ES=set(E)|{(b,a) for a,b in E}
f=lambda r: any((r>>a)&1 and (r>>b)&1 for a,b in E)
T=[(1<<a)|(1<<b) for a,b in E]
F=[r for r in range(1<<n) if not f(r) and all(f(r|(1<<v)) for v in range(n) if not (r>>v)&1)]
core=T+F
rows=list(core); ridx={r:i for i,r in enumerate(rows)}
def row(r):
    if r not in ridx: ridx[r]=len(rows); rows.append(r)
    return ridx[r]
SING={}
if A.factc or A.viol:
    for u in range(n): SING[u]=row(1<<u)
REST=json.load(open(A.rest)) if A.rest else []
RR=[]
FULL=(1<<n)-1
for Aset,Bset,aL,oL,tL in REST:
    hi=FULL^sum(1<<b for b in Bset); lo=sum(1<<a for a in Aset)
    RR.append((row(hi), row(lo) if lo else None, aL,oL,tL))
R=len(rows)
pool=IDPool(); cl=[]
def add(lits):
    out=[]
    for l in lits:
        if l is True: return
        if l is False: continue
        out.append(l)
    assert out, ('empty clause',lits)
    cl.append(out)
neg=lambda l: (not l) if isinstance(l,bool) else -l
op=lambda i: pool.id(('o',i))
lv=lambda i,j: pool.id(('l',i,j)); rv=lambda i,k: pool.id(('r',i,k))
def val(i,t):
    if i<n: return bool((rows[t]>>i)&1)
    return pool.id(('v',i,t))
Lc=lambda i,t: pool.id(('L',i,t)); Rc=lambda i,t: pool.id(('R',i,t))
G=range(n,N)
for i in G:
    ls=[lv(i,j) for j in range(i-1)]; rs=[rv(i,k) for k in range(1,i)]
    cl.append(ls); cl.extend(CardEnc.atmost(ls,1,vpool=pool,encoding=EncType.seqcounter).clauses)
    cl.append(rs); cl.extend(CardEnc.atmost(rs,1,vpool=pool,encoding=EncType.seqcounter).clauses)
    for j in range(i-1):
        for k in range(1,j+1): cl.append([-lv(i,j),-rv(i,k)])
    for t in range(R):
        for j in range(i-1):
            add([-lv(i,j),neg(val(j,t)),Lc(i,t)]); add([-lv(i,j),val(j,t),-Lc(i,t)])
        for k in range(1,i):
            add([-rv(i,k),neg(val(k,t)),Rc(i,t)]); add([-rv(i,k),val(k,t),-Rc(i,t)])
        v=val(i,t); o=op(i); a=Lc(i,t); b=Rc(i,t)
        cl += [[-a,-b,v],[a,b,-v],[-o,a,-v],[-o,b,-v],[o,-a,v],[o,-b,v]]
# output
for t,r in enumerate(rows): add([val(N-1,t)] if f(r) else [neg(val(N-1,t))])
# every non-output gate is used
for g in range(n,N-1):
    cl.append([lv(i,g) for i in range(g+1,N) if g<=i-2]+[rv(i,g) for i in range(g+1,N)])
# depth (exact): D(i,d) <-> depth(i)>=d, d>=2 ; depth(input)=0, depth(gate)>=1
DMAX=s
def dep(i,d):
    if d<=0: return True
    if i<n: return False
    if d==1: return True
    if d>DMAX: return False
    return pool.id(('dp',i,d))
for i in G:
    for d in range(2,DMAX): add([neg(dep(i,d+1)),dep(i,d)])
    for d in range(1,DMAX+1):
        # depth(i)>=d+1 <-> depth(left)>=d or depth(right)>=d
        dl=pool.id(('dl',i,d)); dr=pool.id(('dr',i,d))
        for j in range(i-1):
            add([-lv(i,j),neg(dep(j,d)),dl]); add([-lv(i,j),dep(j,d),-dl])
        for k in range(1,i):
            add([-rv(i,k),neg(dep(k,d)),dr]); add([-rv(i,k),dep(k,d),-dr])
        add([-dl,dep(i,d+1)]); add([-dr,dep(i,d+1)]); add([neg(dep(i,d+1)),dl,dr])
# distinct and non-constant on core rows (valid for minimum circuits)
if not A.nodist:
    C=len(core)
    for i in G:
        add([val(i,t) for t in range(C)]); add([neg(val(i,t)) for t in range(C)])
        for j in range(i):
            ds=[]
            for t in range(C):
                x,y=val(i,t),val(j,t)
                if isinstance(y,bool): ds.append(neg(x) if y else x); continue
                d=pool.id(('d',i,j,t)); add([-d,x,y]); add([-d,-x,-y]); ds.append(d)
            add(ds)
# unary j>=q, k>=q
JG=lambda i,q: True if q<=0 else (False if q>i-2 else pool.id(('jg',i,q)))
KG=lambda i,q: True if q<=1 else (False if q>i-1 else pool.id(('kg',i,q)))
for i in G:
    for q in range(1,i-1):
        # JG(i,q) <-> OR_{j>=q} l(i,j)
        add([neg(JG(i,q))]+[lv(i,j) for j in range(q,i-1)])
        for j in range(q,i-1): add([-lv(i,j),JG(i,q)])
    for q in range(2,i):
        add([neg(KG(i,q))]+[rv(i,k) for k in range(q,i)])
        for k in range(q,i): add([-rv(i,k),KG(i,q)])
if not A.nocanon:
    # canonical order: depth nondecreasing; equal depth => (j,k,op) lex strictly increasing (AND<OR)
    for i in range(n,N-1):
        for d in range(2,DMAX+1): add([neg(dep(i,d)),dep(i+1,d)])
        eq=pool.id(('eq',i))
        for d in range(1,DMAX+1): add([neg(dep(i,d)),dep(i+1,d+1),eq])  # same depth -> eq
        for q in range(1,i-1): add([-eq,neg(JG(i,q)),JG(i+1,q)])
        for j in range(i-1):
            ej=pool.id(('ej',i,j)); add([-eq,-lv(i,j),-lv(i+1,j),ej])
            for q in range(2,i): add([-ej,neg(KG(i,q)),KG(i+1,q)])
            for k in range(j+1,i):
                add([-ej,-rv(i,k),-rv(i+1,k),op(i)]); add([-ej,-rv(i,k),-rv(i+1,k),-op(i+1)])
if A.symb:
    a=pool.id(('symA',)); add([-a,lv(n,0)]); add([-a,rv(n,1)])
    b=pool.id(('symB',)); add([-b,lv(n,0)]); add([-b,rv(n,2)]); add([a,b])
    for i in G:
        for (x,y) in E:
            x,y=min(x,y),max(x,y)
            if y<i: add([-b,-lv(i,x),-rv(i,y)])
# Fact C and violation (Theorem S2): singleton supports of children
aS=lambda i,u: Lc(i,SING[u]); bS=lambda i,u: Rc(i,SING[u])
if A.factc:
    for (u,v) in E:
        alts=[]
        for h in G:
            for (x,y) in ((u,v),(v,u)):
                c=pool.id(('fc',h,x,y)); alts.append(c)
                cl.extend([[-c,op(h)],[-c,aS(h,x)],[-c,-bS(h,x)],[-c,-aS(h,y)],[-c,bS(h,y)]])
        cl.append(alts)
if A.viol:
    VS=[]
    for h in G:
        w=pool.id(('w',h)); VS.append(w); cl.append([-w,op(h)])
        alts=[val(h,SING[u]) for u in range(n)]
        for u in range(n):
            for v in range(n):
                if u!=v and (u,v) not in ES:
                    p=pool.id(('p',h,u,v)); alts.append(p); cl.append([-p,aS(h,u)]); cl.append([-p,bS(h,v)])
        cl.append([-w]+alts)
    cl.append(VS)
# restriction constraints: gate survives (both children non-constant) ; surviving AND>=aL, OR>=oL, total>=tL
for ri,(th,tl,aL,oL,tL) in enumerate(RR):
    sa=[];so=[]
    for i in G:
        x=pool.id(('sa',ri,i)); y=pool.id(('so',ri,i)); sa.append(x); so.append(y)
        cl.append([-x,op(i)]); cl.append([-y,-op(i)])
        for z in (x,y):
            cl.append([-z,Lc(i,th)]); cl.append([-z,Rc(i,th)])
            if tl is not None: cl.append([-z,-Lc(i,tl)]); cl.append([-z,-Rc(i,tl)])
        cl.append([-x,-y])
    if aL>0: cl.extend(CardEnc.atleast(sa,aL,vpool=pool,encoding=EncType.seqcounter).clauses)
    if oL>0: cl.extend(CardEnc.atleast(so,oL,vpool=pool,encoding=EncType.seqcounter).clauses)
    if tL>aL+oL: cl.extend(CardEnc.atleast(sa+so,tL,vpool=pool,encoding=EncType.totalizer).clauses)
ands=[op(i) for i in G]
if A.nand is not None: cl.extend(CardEnc.equals(ands,A.nand,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.maxand is not None: cl.extend(CardEnc.atmost(ands,A.maxand,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.minand is not None: cl.extend(CardEnc.atleast(ands,A.minand,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.nor is not None: cl.extend(CardEnc.equals(ands,s-A.nor,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.outop: cl.append([op(N-1)] if A.outop=='&' else [-op(N-1)])
def impose(i,o,j,k):
    if o!='?': cl.append([op(i)] if o=='&' else [-op(i)])
    if j is not None: cl.append([lv(i,j)])
    if k is not None: cl.append([rv(i,k)])
if A.fixc:
    for idx,(o,j,k) in enumerate(json.loads(A.fixc)): impose(n+idx,o,j,k)
if A.partial:
    for i,o,j,k in json.loads(A.partial): impose(i,o,j,k)
if A.cube:
    for spec in json.loads(A.cube):
        kind=spec[0]; sign=spec[-1]; key=tuple(spec[:-1])
        if kind=='o': lit=op(spec[1])
        elif kind=='l': lit=lv(spec[1],spec[2])
        elif kind=='r': lit=rv(spec[1],spec[2])
        elif kind=='v': lit=val(spec[1],row(spec[2])) if spec[2] in ridx else None
        cl.append([lit] if sign else [-lit])
VMAP={'n':n,'s':s,'l':{},'r':{},'o':{}}
for i in G:
    VMAP['o'][i]=op(i)
    VMAP['l'][i]={j:lv(i,j) for j in range(i-1)}; VMAP['r'][i]={k:rv(i,k) for k in range(1,i)}
print('s',s,'rows',R,'rest',len(RR),'vars',pool.top,'clauses',len(cl),flush=True)
def decode(m):
    m=set(l for l in m if l>0); model=[]
    for i in G:
        j=[j for j,x in VMAP['l'][i].items() if x in m][0]; k=[k for k,x in VMAP['r'][i].items() if x in m][0]
        model.append(('&' if VMAP['o'][i] in m else '|',j,k))
    return model
def verify(model):
    for r in range(1<<n):
        v=[(r>>u)&1 for u in range(n)]
        for o,j,k in model: v.append(v[j]&v[k] if o=='&' else v[j]|v[k])
        if v[-1]!=f(r): return False
    return True
if A.meta: json.dump({'n':n,'s':s,'o':{str(k):v for k,v in VMAP['o'].items()},'l':{str(i):{str(j):x for j,x in d.items()} for i,d in VMAP['l'].items()},'r':{str(i):{str(j):x for j,x in d.items()} for i,d in VMAP['r'].items()},'E':E},open(A.meta,'w'))
if A.dimacs:
    with open(A.dimacs,'w') as fh:
        fh.write('p cnf %d %d\n'%(pool.top,len(cl)))
        for c in cl: fh.write(' '.join(map(str,c))+' 0\n')
if A.solve:
    import pysat.solvers as PS
    Sv=PS.Solver(name=A.solver,bootstrap_with=cl)
    if A.timeout:
        import threading
        tm=threading.Timer(A.timeout,lambda: Sv.interrupt()); tm.start()
        res=Sv.solve_limited(expect_interrupt=True); tm.cancel()
    else: res=Sv.solve()
    if res:
        model=decode(Sv.get_model())
        print('VERIFIED' if verify(model) else 'VERIFY-FAIL',' '.join('%d=%d%s%d'%(n+i,j,o,k) for i,(o,j,k) in enumerate(model)),flush=True)
    print('RESULT',{True:'SAT',False:'UNSAT',None:'TIMEOUT'}[res],'%.1fs'%(time.time()-t0),flush=True)
