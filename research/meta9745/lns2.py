# LNS for AND/OR/NOT fan-in-2 circuits of f_G (meta9745): random convex windows, exact resynthesis of the
# window as a Boolean RELATION (satisfiability + observability don't-cares, computed exactly on all 2^14
# inputs with big-int truth tables), with k-1 gates (improve) or k gates (plateau move, random variant).
# usage: lns.py seed seconds start(left|right|mix) [plateau_prob] [maxk]
import sys, random, json, time, itertools
from pysat.solvers import Solver
from g import *
import os
BUDGET=int(os.environ.get('BUDGET','20000')); MAXIN=int(os.environ.get('MAXIN','8')); MINK=int(os.environ.get('MINK','3'))
def star(cover_side):
    C=[]; W=lambda: n+len(C)-1
    def g(*x): C.append(x); return W()
    adj={v:[] for v in range(n)}
    for a,b in E: adj[a].append(b); adj[b].append(a)
    centers=list(range(7)) if cover_side=='left' else list(range(7,14))
    random.shuffle(centers); S=[]
    for v in centers:
        nb=adj[v][:]; random.shuffle(nb); o=nb[0]
        for u in nb[1:]: o=g('or',o,u)
        S.append(g('and',v,o))
    while len(S)>1:
        random.shuffle(S); a=S.pop(); b=S.pop(); S.append(g('or',a,b))
    return C
def deps(C):
    D=[]
    for i,gt in enumerate(C):
        d=0
        for w in gt[1:]:
            if w>=n: d|=(1<<(w-n))|D[w-n]
        D.append(d)
    return D
def synth(rows, m, no, k, rnd):
    """rows: list of (inpattern tuple, set of forbidden output vectors). find k gates over m inputs,
    outputs = any wires."""
    S=Solver(name='cadical153'); cnt=[0]
    def nv(): cnt[0]+=1; return cnt[0]
    ch=[];sel=[];op=[]
    for i in range(k):
        L=[('u',j,None) for j in range(m+i)]+[('b',j,l) for l in range(m+i) for j in range(l)]
        if rnd: random.shuffle(L)
        ch.append(L); sel.append([nv() for _ in L]); op.append(nv())
        S.add_clause(sel[i])
        for a in range(len(L)):
            for b in range(a+1,len(L)): S.add_clause([-sel[i][a],-sel[i][b]])
    osel=[[nv() for w in range(m+k)] for o in range(no)]
    for o in range(no):
        S.add_clause(osel[o])
        for a in range(m+k):
            for b in range(a+1,m+k): S.add_clause([-osel[o][a],-osel[o][b]])
    # every gate used (by a later gate or an output) -- sound for minimal size
    for r,(pat,forb) in enumerate(rows):
        x=[nv() for i in range(k)]
        def lit(w,v):
            if w<m: return pat[w]==v
            return x[w-m] if v else -x[w-m]
        for i in range(k):
            for a,c in enumerate(ch[i]):
                sv=sel[i][a]
                if c[0]=='u':
                    for v in (0,1):
                        l=lit(c[1],v); out=x[i] if v==0 else -x[i]
                        if l is True: S.add_clause([-sv,out])
                        elif l is not False: S.add_clause([-sv,-l,out])
                else:
                    for a1 in (0,1):
                        for b1 in (0,1):
                            lj=lit(c[1],a1); lk=lit(c[2],b1)
                            if lj is False or lk is False: continue
                            pre=[-sv]+([-lj] if lj is not True else [])+([-lk] if lk is not True else [])
                            if a1==b1: S.add_clause(pre+[x[i] if a1 else -x[i]])
                            else: S.add_clause(pre+[-op[i],x[i]]); S.add_clause(pre+[op[i],-x[i]])
        # output value vars
        ov=[nv() for o in range(no)]
        for o in range(no):
            for w in range(m+k):
                for v in (0,1):
                    l=lit(w,v); ol=ov[o] if v else -ov[o]
                    if l is True: S.add_clause([-osel[o][w],ol])
                    elif l is not False: S.add_clause([-osel[o][w],-l,ol])
        for vec in forb:
            S.add_clause([(-ov[o] if vec[o] else ov[o]) for o in range(no)])
    S.conf_budget(BUDGET)
    if S.solve_limited()!=True: S.delete(); return None
    M=set(v for v in S.get_model() if v>0); S.delete()
    G=[]
    for i in range(k):
        c=ch[i][[a for a in range(len(ch[i])) if sel[i][a] in M][0]]
        G.append(('not',c[1]) if c[0]=='u' else (('or' if op[i] in M else 'and'),c[1],c[2]))
    outs=[[w for w in range(m+k) if osel[o][w] in M][0] for o in range(no)]
    return G,outs
def window_problem(C,Wset):
    Wset=sorted(Wset); L=len(C); gw=set(n+i for i in Wset)
    D=deps(C)
    ins=sorted(set(w for i in Wset for w in C[i][1:] if w not in gw))
    wm=sum(1<<i for i in Wset)
    for w in ins:
        if w>=n and D[w-n]&wm: return None
    users=set()
    for i,gt in enumerate(C):
        if i not in Wset: users|=set(gt[1:])
    outs=[w for w in sorted(gw) if w in users or w==n+L-1]
    if len(outs)>3 or len(ins)>MAXIN: return None
    w0=ev(C)
    # good[o-vector] = mask of t where rest gives f with window outputs forced to o (constant)
    good={}
    for vec in itertools.product((0,1),repeat=len(outs)):
        w=list(X); force=dict(zip(outs,vec))
        for i,gt in enumerate(C):
            ww=n+i
            if ww in force: w.append(ALL if force[ww] else 0); continue
            if i in Wset: w.append(w0[ww]); continue  # internal window gate: irrelevant to rest
            if gt[0]=='not': w.append(ALL^w[gt[1]])
            elif gt[0]=='and': w.append(w[gt[1]]&w[gt[2]])
            else: w.append(w[gt[1]]|w[gt[2]])
        good[vec]=~(w[-1]^F)&ALL
    # group by input pattern: for each pattern p, mask of t having it
    pats={(): ALL}
    for wi in ins:
        npats={}
        for p,msk in pats.items():
            a=msk&w0[wi]; b=msk&~w0[wi]
            if b: npats[p+(0,)]=b
            if a: npats[p+(1,)]=a
        pats=npats
    rows=[]
    for p,msk in pats.items():
        forb=[vec for vec,gm in good.items() if msk&~gm]
        if len(forb)==len(good): return 'BUG'
        rows.append((p,forb))
    return Wset,ins,outs,rows
def rebuild(C,Wset,ins,outs,G,oo):
    m=len(ins); gw=set(n+i for i in Wset); nodes={}
    for i,gt in enumerate(C):
        if n+i not in gw: nodes[('o',i)]=gt
    for i,gt in enumerate(G): nodes[('n',i)]=gt
    def ref_new(w): return ('in',ins[w]) if w<m else ('n',w-m)
    outmap={outs[o]:ref_new(oo[o]) for o in range(len(outs))}
    def ref_old(w):
        if w<n: return ('x',w)
        if w in outmap:
            r=outmap[w]; return ref_old(r[1]) if r[0]=='in' else r
        return ('o',w-n)
    dp={}
    for key,gt in nodes.items():
        if key[0]=='o': dp[key]=[ref_old(w) for w in gt[1:]]
        else: dp[key]=[(ref_old(r[1]) if r[0]=='in' else r) for r in map(ref_new,gt[1:])]
    order=[];done=set()
    def visit(k):
        if k[0]=='x' or k in done: return
        done.add(k)
        for d in dp[k]: visit(d)
        order.append(k)
    outref=ref_old(n+len(C)-1)
    if outref[0]=='x': return None
    visit(outref); idx={}; newC=[]
    for k in order:
        idx[k]=n+len(newC)
        newC.append((nodes[k][0],*[d[1] if d[0]=='x' else idx[d] for d in dp[k]]))
    return newC
def rand_window(C,k):
    L=len(C); start=random.randrange(L); Wset={start}
    while len(Wset)<k:
        cand=set()
        for i in Wset:
            for w in C[i][1:]:
                if w>=n: cand.add(w-n)
            for j,gt in enumerate(C):
                if n+i in gt[1:]: cand.add(j)
        cand-=Wset
        if not cand: break
        Wset.add(random.choice(sorted(cand)))
    return Wset
if __name__=='__main__':
    seed=int(sys.argv[1]); T=float(sys.argv[2]); side=sys.argv[3]
    pp=float(sys.argv[4]) if len(sys.argv)>4 else 0.5; maxk=int(sys.argv[5]) if len(sys.argv)>5 else 7; kick=float(sys.argv[6]) if len(sys.argv)>6 else 0.0
    random.seed(seed)
    C=star(side); assert ok(C) and len(C)==26
    best=len(C); t0=time.time(); it=0; nimp=0; npl=0; nnot=0
    while time.time()-t0<T:
        it+=1
        k=random.randint(MINK,maxk)
        Wset=rand_window(C,k)
        pr=window_problem(C,Wset)
        if pr is None or pr=='BUG':
            if pr=='BUG': print('BUG'); 
            continue
        Wset,ins,outs,rows=pr
        r=synth(rows,len(ins),len(outs),len(Wset)-1,True)
        if r is None and len(C)<27 and random.random()<kick:
            r=synth(rows,len(ins),len(outs),len(Wset)+1,True)
            if r is not None:
                nc=rebuild(C,Wset,ins,outs,*r)
                if nc and ok(nc) and len(nc)<=27: C=nc
            continue
        if r is None:
            if random.random()<pp:
                r=synth(rows,len(ins),len(outs),len(Wset),True)
                if r is None: continue
            else: continue
        nc=rebuild(C,Wset,ins,outs,*r)
        if nc is None or not ok(nc): print('rebuild fail'); continue
        if len(nc)<=len(C) or (len(nc)<=27 and len(C)==27):
            C=nc
            if any(g[0]=='not' for g in C): nnot+=1
            if len(C)<best:
                best=len(C); print('IMPROVED',best,json.dumps(C),flush=True)
                if best<=25: json.dump(C,open('found_%d_%d.json'%(best,seed),'w'))
        if it%20==0: print('it',it,'size',len(C),'best',best,'withNOT',nnot,round(time.time()-t0),flush=True)
    print('done',it,'best',best,json.dumps(C))
