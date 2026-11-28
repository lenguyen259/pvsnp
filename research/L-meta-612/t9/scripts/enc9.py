"""enc6: insertion encoding for a min cex on a partial sun G = C_n0 + pendants P.
PROVED facts used (t2 Cor M, t3 Thm L, t4, t6): x_v -> g_v = x_v | z_v -> q_v = g_v & y_v, single readers.
Contracting every g_v (g_v := z_v) gives C' of size s-|P| computing f_{G-P}=f_{C_n0}.
C = C' with, for each pendant v, x_v OR-ed into one input (side) of one AND gate q_v of C'.
Options: --cnd : C' reduced & minimum for C_n0 (valid when elim(A(P)) <= |P|, i.e. sum floor(k/2)=1).
"""
import sys,json,time,argparse,itertools
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t6')
from lib6 import *
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
import pysat.solvers as PS
ap=argparse.ArgumentParser()
ap.add_argument('n0',type=int); ap.add_argument('S'); ap.add_argument('--s',type=int,help='size of C (default Phi-1)')
ap.add_argument('--cnd',action='store_true'); ap.add_argument('--noholder',action='store_true'); ap.add_argument('--norun',action='store_true')
ap.add_argument('--nolb',action='store_true'); ap.add_argument('--nozr',action='store_true'); ap.add_argument('--runz',action='store_true')
ap.add_argument('--fix',help='circuit string of C in G numbering to test soundness (must be SAT)')
ap.add_argument('--zu',action='store_true'); ap.add_argument('--andcap',action='store_true')
ap.add_argument('--timeout',type=int,default=3600); ap.add_argument('--solver',default='cadical195')
ap.add_argument('--nodist',action='store_true'); ap.add_argument('--pdist',action='store_true'); ap.add_argument('--forcezw',action='append',default=[]); ap.add_argument('--nocanon',action='store_true')
A=ap.parse_args(); t0=time.time()
Sh=[int(x) for x in A.S.split(',')]; n0=A.n0
E,L=psun(n0,Sh); g=Graph(E); nG=g.n; P=sorted(L); k=len(P)
s=A.s if A.s is not None else g.P-1; s0=s-k; N=n0+s0
NB={w:set() for w in range(nG)}
for a,b in E: NB[a].add(b); NB[b].add(a)
def fG(r): return any((r>>a)&1 and (r>>b)&1 for a,b in E)
def maxind(V):
    V=list(V); out=[]
    for mask in range(1<<len(V)):
        r=sum(1<<V[i] for i in range(len(V)) if (mask>>i)&1)
        if fG(r): continue
        if all(fG(r|(1<<v)) for v in V if not (r>>v)&1): out.append(r)
    return out
Ecyc=[(a,b) for a,b in E if a<n0 and b<n0]
rows=[]; rk={}
def addrow(r,kind):
    if r not in rk: rk[r]=len(rows); rows.append(r)
    return rk[r]
for a,b in E: addrow((1<<a)|(1<<b),'T')
FG_=maxind(range(nG)); [addrow(r,'F') for r in FG_]
FC=maxind(range(n0)); [addrow(r,'F') for r in FC]
coreG=[rk[(1<<a)|(1<<b)] for a,b in E]+[rk[r] for r in FG_]
coreC=[rk[(1<<a)|(1<<b)] for a,b in Ecyc]+[rk[r] for r in FC]
eu={v:addrow(1<<L[v],'S') for v in P}
zrows={}
for v in P:
    u=L[v]; rest=[x for x in range(nG) if x not in NB[u] and x!=u]
    zrows[v]=[addrow(r,'Z') for r in maxind(rest)]
zurows={}
for v in P:
    u=L[v]; rest=[x for x in range(nG) if x!=v and x!=u and x not in NB[u]]
    zurows[v]=[addrow(r|(1<<u),'ZU') for r in maxind(rest)]
PDIST=[]
if A.pdist and s==g.P-1:
    # for P' subset of P with tau(G)-tau(G-P')=1: red(C|x_P'=0) = C with g_{P'} contracted is a MINIMUM circuit
    # of G-P' (size s-|P'| = Phi(G-P')), so its gates (all C' gates among them) are distinct/nonconstant on its test rows.
    for r_ in range(1,k+1):
        for Pp in itertools.combinations(P,r_):
            Ep=tuple(e for e in g.E if e[0] not in Pp and e[1] not in Pp)
            if g.t-tau(Ep)!=1: continue
            assert phi(Ep)==s-len(Pp)
            Vp=[x for x in range(nG) if x not in Pp]
            def fGp(r): return any((r>>a)&1 and (r>>b)&1 for a,b in Ep)
            mis=[]
            for mask in range(1<<len(Vp)):
                r=sum(1<<Vp[i] for i in range(len(Vp)) if (mask>>i)&1)
                if fGp(r): continue
                if all(fGp(r|(1<<v)) for v in Vp if not (r>>v)&1): mis.append(r)
            rs=[rk[(1<<a)|(1<<b)] for a,b in Ep]
            for r in mis:
                rs.append(addrow(r,'PD'))
            PDIST.append((Pp,rs))
R=len(rows)
pool=IDPool(); cl=[]
op=lambda i: pool.id(('o',i))
def val(i,t):
    if i<n0: return bool((rows[t]>>i)&1)
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
pairs={i:[(j,kk) for j in range(i) for kk in range(j+1,i)] for i in range(n0,N)}
sv=lambda i,j,kk: pool.id(('s',i,j,kk))
ins=lambda v,i,sd: pool.id(('ins',v,i,sd))
for i in range(n0,N):
    ss=[sv(i,j,kk) for j,kk in pairs[i]]
    cl.append(ss); cl.extend(CardEnc.atmost(lits=ss,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
# insertions
for v in P:
    lits=[ins(v,i,sd) for i in range(n0,N) for sd in (0,1)]
    cl.append(lits); cl.extend(CardEnc.atmost(lits=lits,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    for i in range(n0,N):
        for sd in (0,1): cl.append([-ins(v,i,sd),op(i)])
for i in range(n0,N):
    for sd in (0,1):
        lits=[ins(v,i,sd) for v in P]
        for a_,b_ in itertools.combinations(lits,2): cl.append([-a_,-b_])
# gate semantics
for i in range(n0,N):
    o=op(i)
    for t in range(R):
        a=pool.id(('a',i,t)); b=pool.id(('b',i,t)); c=val(i,t)
        on=[v for v in P if (rows[t]>>v)&1]
        for sd,x in ((0,a),(1,b)):
            for v in on: cl.append([-ins(v,i,sd),x])
            for j,kk in pairs[i]:
                y=val(j if sd==0 else kk,t); z=sv(i,j,kk)
                add([-z,neg(y),x]); add([-z,-x,y]+[ins(v,i,sd) for v in on])
        cl.extend([[-o,-a,-b,c],[-o,a,-c],[-o,b,-c],[o,-a,c],[o,-b,c],[o,a,b,-c]])
for t,r in enumerate(rows): add([val(N-1,t)] if fG(r) else [neg(val(N-1,t))])
# all used
for gt in range(n0,N-1):
    cl.append([sv(i,j,kk) for i in range(gt+1,N) for j,kk in pairs[i] if gt in (j,kk)])
def distinct(rowset,tag):
    for i in range(n0,N):
        add([val(i,t) for t in rowset]); add([neg(val(i,t)) for t in rowset])
        for j in range(i):
            ds=[]
            for t in rowset:
                x,y=val(i,t),val(j,t)
                if isinstance(y,bool): ds.append(neg(x) if y else x); continue
                d=pool.id(('d',tag,i,j,t)); add([-d,x,y]); add([-d,-x,-y]); ds.append(d)
            add(ds)
if not A.nodist: distinct(coreG,'G')
for Pp,rs in PDIST: distinct(rs,'P'+''.join(map(str,Pp)))
if A.cnd: distinct(coreC,'C')
# canonical order (depth, lex pair, AND before OR) on C'
if not A.nocanon:
    D=s0
    dep=lambda i,d: pool.id(('dp',i,d))
    def depl(i,d):
        if d<=0: return True
        if i<n0: return False
        if d==1: return True
        if d>D: return False
        return dep(i,d)
    for i in range(n0,N):
        for j,kk in pairs[i]:
            x=sv(i,j,kk)
            for d in range(1,D+1):
                add([-x,neg(depl(i,d+1)),depl(j,d),depl(kk,d)])
                add([-x,depl(i,d+1),neg(depl(j,d))]); add([-x,depl(i,d+1),neg(depl(kk,d))])
        for d in range(2,D): cl.append([-dep(i,d+1),dep(i,d)])
    Pq=lambda i,q: pool.id(('P',i,q))
    for i in range(n0,N-1):
        for d in range(2,D+1): add([neg(depl(i,d)),depl(i+1,d)])
        eq=pool.id(('eq',i))
        for d in range(1,D+1):
            add([depl(i,d),neg(depl(i+1,d)),-eq]); add([neg(depl(i,d)),depl(i+1,d+1),eq])
    for i in range(n0,N):
        Q=len(pairs[i])
        for q in range(Q):
            j,kk=pairs[i][q]
            cl.append([-sv(i,j,kk),Pq(i,q)])
            if q+1<Q: cl.append([-sv(i,j,kk),-Pq(i,q+1)]); cl.append([-Pq(i,q+1),Pq(i,q)]); cl.append([-Pq(i,q),sv(i,j,kk),Pq(i,q+1)])
            else: cl.append([-Pq(i,q),sv(i,j,kk)])
    for i in range(n0,N-1):
        eq=pool.id(('eq',i)); Q=len(pairs[i])
        for q in range(Q):
            j,kk=pairs[i][q]
            if q>0: cl.append([-eq,-sv(i,j,kk),Pq(i+1,q)])
            cl.append([-eq,-sv(i,j,kk),-sv(i+1,j,kk),op(i),-op(i+1)])  # non-strict: equal (pair,op) allowed (insertions may differ)
# z/y facts per insertion
def zy_clause(v,i,sd,fn):
    for j,kk in pairs[i]:
        z,y=(j,kk) if sd==0 else (kk,j)
        fn(z,y,[-ins(v,i,sd),-sv(i,j,kk)])
for v in P:
    u=L[v]
    for i in range(n0,N):
        for sd in (0,1):
            def f1(z,y,pre):
                if z==u: cl.append(pre)            # z != x_u (Thm L)
                if not A.nolb:
                    add(pre+[neg(val(z,eu[v]))]); add(pre+[val(y,eu[v])])   # z(e_u)=0, y(e_u)=1 (Thm L(b))
                if not A.nozr:
                    for t in zrows[v]: add(pre+[neg(val(z,t))])   # z_v=0 on indep sets missing N[u]-v (Lemma PN)
                if A.zu:
                    for t in zurows[v]: add(pre+[neg(val(z,t))])  # t9 Lemma ZU: z_v=0 on indep sets containing u
            zy_clause(v,i,sd,f1)
# readers of cycle vertices in C: C' readers + g_v with z_v = x_w
zw={}
for v in P:
    for w in NB[L[v]]:
        if w>=n0 : continue
        lit=pool.id(('zw',v,w)); zw[(v,w)]=lit; terms=[]
        for i in range(n0,N):
            for j,kk in pairs[i]:
                for sd,node in ((0,j),(1,kk)):
                    if node==w:
                        cl.append([-ins(v,i,sd),-sv(i,j,kk),lit]); terms.append((ins(v,i,sd),sv(i,j,kk)))
        aux=[]
        for a_,b_ in terms:
            t_=pool.id(('zwt',v,w,a_,b_)); cl.extend([[-t_,a_],[-t_,b_]]); aux.append(t_)
        cl.append([-lit]+aux)
OCC={}
def occ(i,sd):
    if (i,sd) in OCC: return OCC[(i,sd)]
    x=pool.id(('occ',i,sd)); OCC[(i,sd)]=x; ls=[ins(v,i,sd) for v in P]
    cl.append([-x]+ls); [cl.append([-l,x]) for l in ls]; return x
def rsel(i,w):
    # C-reader: gate i reads x_w directly (w at a side of the selected pair WITHOUT an insertion there)
    x=pool.id(('rs',i,w)); terms=[]
    for j,kk in pairs[i]:
        for sd,node in ((0,j),(1,kk)):
            if node==w:
                t_=pool.id(('rst',i,w,j,kk,sd)); o_=occ(i,sd)
                cl.extend([[-t_,sv(i,j,kk)],[-t_,-o_],[-sv(i,j,kk),o_,t_]]); terms.append(t_)
    cl.append([-x]+terms); [cl.append([-t_,x]) for t_ in terms]; return x
holders=set(L.values())
for w in range(n0):
    rl=[rsel(i,w) for i in range(n0,N)]; ex=[zw[(v,w)] for v in P if (v,w) in zw]
    allr=rl+ex
    if w in holders:
        if not A.noholder:
            cl.extend(CardEnc.equals(lits=allr,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
    elif not A.norun:
        nb=gneed(g,[],[w])
        cl.extend(CardEnc.atmost(lits=allr,bound=2,vpool=pool,encoding=EncType.seqcounter).clauses)
        for idx,i in enumerate(range(n0,N)):
            for l in allr:
                if l!=rl[idx]: cl.append([-rl[idx],-op(i),-l])   # an AND reader => only reader
        if nb-1<4:   # F + min(k_or,2) <= nb-1 ; with F=2 => both OR => 4
            cl.extend(CardEnc.atmost(lits=allr,bound=1,vpool=pool,encoding=EncType.seqcounter).clauses)
for fz_ in A.forcezw:
    v_,w_=map(int,fz_.split(',')); cl.append([zw[(v_,w_)]])
if A.fix:
    # map a G-circuit with min-cex structure into C' + insertions
    c=parse(A.fix); node={u:u for u in range(n0)}; gv={}
    for i,o,j,kk in c:
        if o=='|' and (j in P or kk in P): gv[i]=(j if j in P else kk, kk if j in P else j); continue
    idx=n0; ins_list=[]
    for i,o,j,kk in c:
        if i in gv: continue
        def mp(x,sd):
            if x in gv: ins_list.append((gv[x][0],idx,sd)); return node[gv[x][1]]
            return node[x]
        a_,b_=mp(j,0),mp(kk,1)
        if a_>b_:
            a_,b_=b_,a_; ins_list[:]=[(vv,ii,1-sd if ii==idx else sd) for vv,ii,sd in ins_list]
        cl.append([sv(idx,a_,b_)]); cl.append([op(idx)] if o=='&' else [-op(idx)]); node[i]=idx; idx+=1
    for vv,ii,sd in ins_list: cl.append([ins(vv,ii,sd)])
if A.andcap:
    cap=s-(len(E)-1)   # Lean L_meta_599: #OR(C) >= |E(G)|-1, C has s gates, AND gates of C = AND gates of C'
    cl.extend(CardEnc.atmost(lits=[op(i) for i in range(n0,N)],bound=cap,vpool=pool,encoding=EncType.seqcounter).clauses)
print('G',A.n0,A.S,'Phi',g.P,'s',s,'s0',s0,'rows',R,'vars',pool.top,'clauses',len(cl),{kk:vv for kk,vv in vars(A).items() if vv},flush=True)
import threading
Sv=PS.Solver(name=A.solver,bootstrap_with=cl)
tm=threading.Timer(A.timeout,lambda: Sv.interrupt()); tm.start()
res=Sv.solve_limited(expect_interrupt=True); tm.cancel()
if res:
    m=set(l for l in Sv.get_model() if l>0); out=[]; nm={u:u for u in range(n0)}; nxt=nG; gates=[]
    for i in range(n0,N):
        (j,kk),=[(j,kk) for j,kk in pairs[i] if sv(i,j,kk) in m]
        ins_=[[v for v in P if ins(v,i,sd) in m] for sd in (0,1)]
        inp=[]
        for sd,x in ((0,j),(1,kk)):
            y=nm[x]
            if ins_[sd]:
                v=ins_[sd][0]; gates.append((nxt,'|',v,y)); y=nxt; nxt+=1
            inp.append(y)
        gates.append((nxt,'&' if op(i) in m else '|',inp[0],inp[1])); nm[i]=nxt; nxt+=1
    T=tables(g,gates,{}); okk=T[gates[-1][0]]==g.f
    print('VERIFIED' if okk else 'VERIFY-FAIL',fmt(gates),flush=True)
print('RESULT',{True:'SAT',False:'UNSAT',None:'TIMEOUT'}[res],'%.1fs'%(time.time()-t0),flush=True)
