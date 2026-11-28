# Petersen monotone circuit SAT, v2: pair selectors, depth-canonical order (fully canonical up to Aut), distinctness on core rows
import sys, json, time, argparse
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
import pysat.solvers as PS
PET=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
ap=argparse.ArgumentParser(); ap.add_argument('s',type=int)
ap.add_argument('--first',help='op,j,k for first gate e.g. "&,0,1"'); ap.add_argument('--symb',action='store_true',help='first pair in {(0,1),(0,2)} rule')
ap.add_argument('--solver',default='glucose4'); ap.add_argument('--viol',action='store_true')
ap.add_argument('--sing',action='store_true'); ap.add_argument('--nodist',action='store_true')
ap.add_argument('--nor',type=int); ap.add_argument('--nand',type=int)
ap.add_argument('--fix',help='json list of [op,j,k] for gates n.. (in canonical order)')
ap.add_argument('--cube',help='json list of extra literal specs [["s",i,j,k],["o",i,1]] ')
ap.add_argument('--dimacs'); ap.add_argument('--factc',action='store_true'); ap.add_argument('--chain',action='store_true'); ap.add_argument('--graph'); ap.add_argument('--elim',help='json [[Z,bound],...]'); ap.add_argument('--rest',help='json [[S0,S1,bound],...]'); ap.add_argument('--orb',help='json [orbit pair lists, case index k, op]'); ap.add_argument('--timeout',type=float); ap.add_argument('--orbs')
A=ap.parse_args()
E=[tuple(e) for e in json.loads(A.graph)] if A.graph else PET; n=max(max(e) for e in E)+1; s=A.s; N=n+s; t0=time.time()
Es=set(E)|{(b,a) for a,b in E}
f=lambda r: any((r>>a)&1 and (r>>b)&1 for a,b in E)
T=[(1<<a)|(1<<b) for a,b in E]
F=[r for r in range(1<<n) if not f(r) and all(f(r|(1<<v)) for v in range(n) if not (r>>v)&1)]
core=len(T)+len(F)
S=[1<<u for u in range(n)] if (A.sing or A.viol or A.factc) else []
ELIM=[[Z,[],b] for Z,b in json.loads(A.elim)] if A.elim else []
if A.rest: ELIM+=json.loads(A.rest)
DZ=[]; RI=[]
for S0,S1,b in ELIM:
    i0=i1=None
    if S0: i0=len(DZ); DZ.append(((1<<n)-1)^sum(1<<z for z in S0))
    if S1:
        r1=sum(1<<z for z in S1)
        i1=len(DZ); DZ.append(r1)
    RI.append((i0,i1))
rows=T+F+S+DZ; R=len(rows); sidx={u:core+u for u in range(n)}
pool=IDPool(); cl=[]
op=lambda i: pool.id(('o',i))      # true = AND
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
pairs={i:[(j,k) for j in range(i) for k in range(j+1,i)] for i in range(n,N)}
sv=lambda i,j,k: pool.id(('s',i,j,k))
D=s  # max depth
dep=lambda i,d: pool.id(('dp',i,d))  # depth(i)>=d, d=1..D ; depth>=1 always for gates
def depl(i,d):
    if d<=0: return True
    if i<n: return False
    if d==1: return True
    if d>D: return False
    return dep(i,d)
for i in range(n,N):
    ss=[sv(i,j,k) for j,k in pairs[i]]
    cl.append(ss); cl.extend(CardEnc.atmost(lits=ss,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    o=op(i)
    for j,k in pairs[i]:
        x=sv(i,j,k)
        for t in range(R):
            c=val(i,t); a=val(j,t); b=val(k,t)
            add([-x,neg(a),neg(b),c]); add([-x,a,b,neg(c)])
            add([-x,-o,a,neg(c)]); add([-x,-o,b,neg(c)])
            add([-x,o,neg(a),c]); add([-x,o,neg(b),c])
        for d in range(1,D+1):  # depth(i)>=d+1 <-> depth(j)>=d or depth(k)>=d
            add([-x,neg(depl(i,d+1)),depl(j,d),depl(k,d)])
            add([-x,depl(i,d+1),neg(depl(j,d))]); add([-x,depl(i,d+1),neg(depl(k,d))])
    for d in range(2,D): cl.append([-dep(i,d+1),dep(i,d)])
for t,r in enumerate(rows): add([val(N-1,t)] if f(r) else [neg(val(N-1,t))])
users={g:[] for g in range(n,N)}
for i in range(n,N):
    for j,k in pairs[i]:
        if j>=n: users[j].append(sv(i,j,k))
        if k>=n: users[k].append(sv(i,j,k))
for g in range(n,N-1): cl.append(users[g])
if A.chain:  # associativity normal form: same-op fanout-1 trees are ascending chains
    INT=lambda g: False if g<n else pool.id(('int',g))
    for g in range(n,N):
        us=[]
        for i in range(g+1,N):
            for j,k in pairs[i]:
                if g in (j,k): us.append((i,sv(i,j,k)))
        if not us: cl.append([-INT(g)]); continue
        two=pool.id(('two',g)); prev=None
        for idx,(i,x) in enumerate(us):
            h=pool.id(('has',g,idx)); cl.append([-x,h])
            if prev is not None: cl.append([-prev,h]); cl.append([-x,-prev,two])
            prev=h
        it=INT(g); cl.append([-it,-two]); cl.append([-it]+[x for _,x in us])
        for i,x in us:
            cl.append([-x,-it,-op(i),op(g)]); cl.append([-x,-it,op(i),-op(g)])
            cl.append([-x,two,-op(i),-op(g),it]); cl.append([-x,two,op(i),op(g),it])
    NL=lambda g,q: True if q<=0 else (False if q>=g else pool.id(('nl',g,q)))
    for g in range(n,N):
        for q in range(1,g-1): cl.append([-NL(g,q+1),NL(g,q)])
        for j,k in pairs[g]:
            x=sv(g,j,k); ij=INT(j); ik=INT(k)
            if j>=n and k>=n: cl.append([-x,-ij,-ik])
            if j>=n:
                add([-x,-ij,NL(g,k)]); add([-x,-ij,neg(NL(g,k+1))]); add([-x,-ij,neg(NL(j,k))])
            if k>=n:
                add([-x,-ik,NL(g,j)]); add([-x,-ik,neg(NL(g,j+1))]); add([-x,-ik,neg(NL(k,j))])
            add([-x,ij,ik,NL(g,k)]); add([-x,ij,ik,neg(NL(g,k+1))])
if not A.nodist:
    for i in range(n,N):
        add([val(i,t) for t in range(core)]); add([neg(val(i,t)) for t in range(core)])
        for j in range(i):
            ds=[]
            for t in range(core):
                x,y=val(i,t),val(j,t)
                if isinstance(y,bool): ds.append(neg(x) if y else x); continue
                d=pool.id(('d',i,j,t)); add([-d,x,y]); add([-d,-x,-y]); ds.append(d)
            add(ds)
# canonical order: depth nondecreasing; equal depth -> (j,k) lex strictly increasing, equal pair -> AND then OR
P=lambda i,q: pool.id(('P',i,q))  # pair index of gate i >= q (pairs ordered lex, common prefix across i)
for i in range(n,N-1):
    for d in range(2,D+1): add([neg(depl(i,d)),depl(i+1,d)])
    eq=pool.id(('eq',i))  # depth(i)==depth(i+1)
    for d in range(1,D+1):  # if depth(i)<d and depth(i+1)>=d then not eq ; eq <- both same
        add([depl(i,d),neg(depl(i+1,d)),-eq])
    # eq is only needed one direction: not eq must imply depth differs -> encode eq true when same
    for d in range(1,D+1):
        add([neg(depl(i,d)),depl(i+1,d+1),eq])  # depth(i)>=d & depth(i+1)<d+1 ... (with nondecreasing => equal=d)
for i in range(n,N):
    Q=len(pairs[i])
    for q in range(Q):
        j,k=pairs[i][q]
        cl.append([-sv(i,j,k),P(i,q)])
        if q+1<Q: cl.append([-sv(i,j,k),-P(i,q+1)]); cl.append([-P(i,q+1),P(i,q)]); cl.append([-P(i,q),sv(i,j,k),P(i,q+1)])
        else: cl.append([-P(i,q),sv(i,j,k)])
for i in range(n,N-1):
    eq=pool.id(('eq',i)); Q=len(pairs[i])
    for q in range(Q):
        j,k=pairs[i][q]
        if q>0: cl.append([-eq,-sv(i,j,k),P(i+1,q)])
        cl.append([-eq,-sv(i,j,k),-sv(i+1,j,k),op(i)]); cl.append([-eq,-sv(i,j,k),-sv(i+1,j,k),-op(i+1)])
if A.symb:  # Aut(Petersen) edge- and arc-... : first gate pair (0,1), or (0,2) with no depth-1 gate on an edge
    cl.append([sv(n,0,1),sv(n,0,2)])
    for i in range(n+1,N):
        for (a,b) in E:
            j,k=min(a,b),max(a,b); cl.append([-sv(n,0,2),-sv(i,j,k)])
if A.first:
    o,j,k=A.first.split(','); j=int(j); k=int(k); cl.append([sv(n,j,k)]); cl.append([op(n) if o=='&' else -op(n)])
if A.fix:
    for idx,(o,j,k) in enumerate(json.loads(A.fix)):
        i=n+idx; cl.append([sv(i,j,k)]); cl.append([op(i) if o=='&' else -op(i)])
aV=lambda h,u: pool.id(('aS',h,u)); bV=lambda h,u: pool.id(('bS',h,u))
if A.viol or A.factc:
    for h in range(n,N):
        for j,k in pairs[h]:
            for u in range(n):
                t=sidx[u]
                add([-sv(h,j,k),neg(val(j,t)),aV(h,u)]); add([-sv(h,j,k),val(j,t),-aV(h,u)])
                add([-sv(h,j,k),neg(val(k,t)),bV(h,u)]); add([-sv(h,j,k),val(k,t),-bV(h,u)])
if A.factc:  # Fact C: every edge uv has an AND gate with u in S1\S2, v in S2\S1 (or swapped)
    for (u,v) in E:
        alts=[]
        for h in range(n,N):
            for (x,y) in ((u,v),(v,u)):
                c=pool.id(('fc',h,x,y)); alts.append(c)
                cl.extend([[-c,op(h)],[-c,aV(h,x)],[-c,-bV(h,x)],[-c,-aV(h,y)],[-c,bV(h,y)]])
        cl.append(alts)
if A.viol:
    VS=[]
    for h in range(n,N):
        w=pool.id(('w',h)); VS.append(w); cl.append([-w,op(h)])
        alts=[val(h,sidx[u]) for u in range(n)]
        for u in range(n):
            for v in range(n):
                if u!=v and (u,v) not in Es:
                    p=pool.id(('p',h,u,v)); alts.append(p); cl.append([-p,aV(h,u)]); cl.append([-p,bV(h,v)])
        cl.append([-w]+alts)
    cl.append(VS)
base=core+len(S)
for ei,(S0,S1,bnd) in enumerate(ELIM):
    i0,i1=RI[ei]
    def const(g,ei=ei,i0=i0,i1=i1):
        ls=[]
        if i0 is not None: ls.append(neg(val(g,base+i0)))
        if i1 is not None: ls.append(val(g,base+i1))
        if any(l is True for l in ls): return True
        ls=[l for l in ls if l is not False]
        if not ls: return False
        if len(ls)==1: return ls[0]
        c=pool.id(('cst',ei,g)); cl.append([-c]+ls)
        for l in ls: cl.append([-l,c])
        return c
    el=[]
    for g in range(n,N):
        za=pool.id(('za',ei,g)); zb=pool.id(('zb',ei,g)); dd=pool.id(('dd',ei,g)); e=pool.id(('el',ei,g)); el.append(e)
        for j,k in pairs[g]:
            x=sv(g,j,k)
            add([-x,-za,const(j)]); add([-x,za,neg(const(j))]); add([-x,-zb,const(k)]); add([-x,zb,neg(const(k))])
        cl.extend([[-za,e],[-zb,e],[-dd,e],[-e,za,zb,dd]])
    for g in range(n,N):
        dd=pool.id(('dd',ei,g))
        if g==N-1: cl.append([-dd]); add([neg(const(g))]); continue
        lus=[]
        for i in range(g+1,N):
            us=[sv(i,j,k) for j,k in pairs[i] if g in (j,k)]
            lu=pool.id(('lu',ei,g,i)); lus.append(lu)
            cl.append([-lu]+us); add([-lu,neg(const(i))]); cl.append([-lu,-pool.id(('dd',ei,i))])
            for x in us: add([-dd,-x,const(i),pool.id(('dd',ei,i))])
        cl.append([dd]+lus)
    if bnd<0: cl.append([-pool.id(('el',ei,n))]); cl.append([pool.id(('el',ei,n))])
    elif bnd<s: cl.extend(CardEnc.atmost(lits=el,bound=bnd,vpool=pool,encoding=EncType.totalizer).clauses)
LEVELS=[json.loads(A.orb)] if A.orb else []
if A.orbs: LEVELS+=json.loads(A.orbs)
for lvi,(orbs,kk,oo) in enumerate(LEVELS):
    lv=lambda j,k: [sv(i,j,k) for i in range(n,N) if (j,k) in pairs[i]]
    upto=orbs if kk<0 else orbs[:kk]
    for o2 in upto:
        for j,k in o2:
            for x in lv(j,k): cl.append([-x])
    if kk<0: continue
    j0,k0=orbs[kk][0]
    alts=[]
    for i in range(n,N):
        if (j0,k0) in pairs[i]:
            a=pool.id(('orb',lvi,i)); alts.append(a); cl.append([-a,sv(i,j0,k0)]); cl.append([-a,op(i)] if oo=='&' else [-a,-op(i)])
    cl.append(alts)
    if oo=='|':
        for j,k in orbs[kk]:
            for i in range(n,N):
                if (j,k) in pairs[i]: cl.append([-sv(i,j,k),-op(i)])
ors=[-op(i) for i in range(n,N)]
if A.nor is not None: cl.extend(CardEnc.equals(lits=ors,bound=A.nor,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.nand is not None: cl.extend(CardEnc.equals(lits=[-x for x in ors],bound=A.nand,vpool=pool,encoding=EncType.seqcounter).clauses)
if A.cube:
    for spec in json.loads(A.cube):
        if spec[0]=='s': cl.append([sv(*spec[1:4])] if spec[4] else [-sv(*spec[1:4])])
        elif spec[0]=='o': cl.append([op(spec[1])] if spec[2] else [-op(spec[1])])
print('s',s,'rows',R,'(T%d F%d S%d)'%(len(T),len(F),len(S)),'vars',pool.top,'clauses',len(cl),{k:v for k,v in vars(A).items() if v},flush=True)
if A.dimacs:
    with open(A.dimacs,'w') as fh:
        fh.write('p cnf %d %d\n'%(pool.top,len(cl)))
        for c in cl: fh.write(' '.join(map(str,c))+' 0\n')
    sys.exit()
Sv=PS.Solver(name=A.solver,bootstrap_with=cl)
if A.timeout:
    import threading
    tm=threading.Timer(A.timeout,lambda: Sv.interrupt()); tm.start()
    res=Sv.solve_limited(expect_interrupt=True); tm.cancel()
else: res=Sv.solve()
if res:
    m=set(l for l in Sv.get_model() if l>0); model=[]
    for i in range(n,N):
        (j,k),=[(j,k) for j,k in pairs[i] if sv(i,j,k) in m]
        model.append(('&' if op(i) in m else '|',j,k))
    ok=True
    for r in range(1<<n):
        v=[(r>>u)&1 for u in range(n)]
        for o,j,k in model: v.append(v[j]&v[k] if o=='&' else v[j]|v[k])
        if v[-1]!=f(r): ok=False; break
    print('VERIFIED' if ok else 'VERIFY-FAIL', ' '.join('%d=%d%s%d'%(n+i,j,o,k) for i,(o,j,k) in enumerate(model)),flush=True)
print('RESULT',{True:'SAT',False:'UNSAT',None:'TIMEOUT'}[res],'%.1fs'%(time.time()-t0),flush=True)
