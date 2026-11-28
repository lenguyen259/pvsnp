# SAT-based local improvement (windows) for AND/OR/NOT fan-in-2 circuits, every gate counted.
# circuit: list of gates ('and',a,b) | ('or',a,b) | ('not',a) over wires 0..8 inputs, 9.. gates; output = last gate.
import sys, random, itertools, json, time
from pysat.solvers import Solver
n=9
E=[(0,5),(0,6),(1,6),(2,6),(1,7),(3,7),(4,7),(2,8),(3,8),(5,8),(7,8)]
def f(t): return int(any((t>>a)&1 and (t>>b)&1 for a,b in E))
def wires(C,t):
    w=[(t>>j)&1 for j in range(n)]
    for g in C:
        if g[0]=='not': w.append(1-w[g[1]])
        elif g[0]=='and': w.append(w[g[1]]&w[g[2]])
        else: w.append(w[g[1]]|w[g[2]])
    return w
def ok(C): return all(wires(C,t)[-1]==f(t) for t in range(512))
def star14():
    C=[]; W=lambda: n+len(C)-1
    def g(*x): C.append(x); return W()
    a=g('or',5,6); s0=g('and',0,a)
    b=g('or',1,2); s6=g('and',6,b)
    c=g('or',1,3); c2=g('or',c,4); s7=g('and',7,c2)
    d=g('or',2,3); d2=g('or',d,5); d3=g('or',d2,7); s8=g('and',8,d3)
    o=g('or',s0,s6); o=g('or',o,s7); o=g('or',o,s8)
    return C
def synth(ins_vals, outs_vals, k, tl=None):
    """ins_vals: list of tuples (values of window inputs) ; outs_vals: required output tuple per row.
    find k gates over m=len(ins) inputs whose some wires realize each output. returns gates or None"""
    m=len(ins_vals[0]); R=len(ins_vals); no=len(outs_vals[0])
    S=Solver(name='cadical195'); cnt=[0]
    def nv(): cnt[0]+=1; return cnt[0]
    ch=[];sel=[];op=[]
    for i in range(k):
        L=[('u',j,None) for j in range(m+i)]+[('b',j,l) for l in range(m+i) for j in range(l)]
        ch.append(L); sel.append([nv() for _ in L]); op.append(nv())
        S.add_clause(sel[i])
        for a in range(len(L)):
            for b in range(a+1,len(L)): S.add_clause([-sel[i][a],-sel[i][b]])
    # output selectors: output o is wire w (any wire incl. inputs)
    osel=[[nv() for w in range(m+k)] for o in range(no)]
    for o in range(no):
        S.add_clause(osel[o])
    x=[[nv() for i in range(k)] for r in range(R)]
    for r in range(R):
        def lit(w,v):
            if w<m: return ins_vals[r][w]==v
            return x[r][w-m] if v else -x[r][w-m]
        for i in range(k):
            for a,c in enumerate(ch[i]):
                sv=sel[i][a]
                if c[0]=='u':
                    for v in (0,1):
                        l=lit(c[1],v); out=x[r][i] if v==0 else -x[r][i]
                        if l is True: S.add_clause([-sv,out])
                        elif l is not False: S.add_clause([-sv,-l,out])
                else:
                    for a1 in (0,1):
                        for b1 in (0,1):
                            lj=lit(c[1],a1); lk=lit(c[2],b1)
                            if lj is False or lk is False: continue
                            pre=[-sv]+([-lj] if lj is not True else [])+([-lk] if lk is not True else [])
                            if a1==b1: S.add_clause(pre+[x[r][i] if a1 else -x[r][i]])
                            else: S.add_clause(pre+[-op[i],x[r][i]]); S.add_clause(pre+[op[i],-x[r][i]])
        for o in range(no):
            for w in range(m+k):
                l=lit(w,outs_vals[r][o])
                if l is False: S.add_clause([-osel[o][w]])
                elif l is not True: S.add_clause([-osel[o][w],l])
    if not S.solve(): return None
    M=set(v for v in S.get_model() if v>0)
    G=[]
    for i in range(k):
        c=ch[i][[a for a in range(len(ch[i])) if sel[i][a] in M][0]]
        G.append(('not',c[1]) if c[0]=='u' else (('or' if op[i] in M else 'and'),c[1],c[2]))
    outs=[[w for w in range(m+k) if osel[o][w] in M][0] for o in range(no)]
    return G,outs
def try_window(C,Wset):
    N=n+len(C); Wset=sorted(Wset)
    gw=[n+i for i in Wset]
    ins=sorted(set(w for i in Wset for w in C[i][1:] if w not in gw))
    # window must be convex: inputs must not depend on window gates
    dep={}
    for i,g in enumerate(C):
        d=set()
        for w in g[1:]:
            if w>=n: d|={w}|dep[w]
        dep[n+i]=d
    for w in ins:
        if w>=n and dep[w]&set(gw): return None
    users=set()
    for i,g in enumerate(C):
        if i in Wset: continue
        users|=set(g[1:])
    outs=[w for w in gw if w in users or w==N-1]
    rows={}
    for t in range(512):
        wv=wires(C,t)
        key=tuple(wv[w] for w in ins); val=tuple(wv[w] for w in outs)
        rows[key]=val
    ivals=list(rows); ovals=[rows[k] for k in ivals]
    r=synth(ivals,ovals,len(Wset)-1)
    if r is None: return None
    G,oo=r
    # rebuild circuit: place new gates at position of first window gate... simplest: topo rebuild
    return (Wset,ins,outs,G,oo)
def rebuild(C,res):
    Wset,ins,outs,G,oo=res
    m=len(ins); gw=set(n+i for i in Wset)
    # new node list: old non-window gates + new gates, then topo sort by dependencies
    nodes={}
    for i,g in enumerate(C):
        if n+i not in gw: nodes[('o',i)]=g
    for i,g in enumerate(G): nodes[('n',i)]=g
    def ref_new(w):  # wire in new-gate space -> node ref
        return ('in',ins[w]) if w<m else ('n',w-m)
    outmap={outs[o]:ref_new(oo[o]) for o in range(len(outs))}
    def ref_old(w):
        if w<n: return ('x',w)
        if w in outmap: return outmap[w]
        return ('o',w-n)
    deps={}
    for key,g in nodes.items():
        if key[0]=='o': deps[key]=[ref_old(w) for w in g[1:]]
        else:
            rr=[]
            for w in g[1:]:
                r=ref_new(w); rr.append(ref_old(r[1]) if r[0]=='in' else r)
            deps[key]=rr
    order=[];done=set()
    def visit(k):
        if k[0]=='x' or k in done: return
        for d in deps[k]: visit(d)
        done.add(k); order.append(k)
    outref=ref_old(n+len(C)-1)
    visit(outref)
    idx={}
    newC=[]
    for k in order:
        idx[k]=n+len(newC)
        args=[d[1] if d[0]=='x' else idx[d] for d in deps[k]]
        newC.append((nodes[k][0],*args))
    if outref[0]=='x': return None
    # output must be last
    if idx[outref]!=n+len(newC)-1: return None
    return newC
if __name__=='__main__':
    random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 0)
    C=star14(); assert ok(C) and len(C)==14
    best=C; t0=time.time(); tries=0
    while time.time()-t0<float(sys.argv[2] if len(sys.argv)>2 else 600):
        tries+=1
        C=best; L=len(C)
        k=random.randint(3,min(8,L))
        # grow a random connected window
        start=random.randrange(L); Wset={start}
        while len(Wset)<k:
            cand=set()
            for i in Wset:
                for w in C[i][1:]:
                    if w>=n: cand.add(w-n)
                for j,g in enumerate(C):
                    if n+i in g[1:]: cand.add(j)
            cand-=Wset
            if not cand: break
            Wset.add(random.choice(sorted(cand)))
        res=try_window(C,Wset)
        if res:
            nc=rebuild(C,res)
            if nc and ok(nc) and len(nc)<len(best):
                best=nc; print('IMPROVED',len(best),json.dumps(best),flush=True)
    print('done tries',tries,'best',len(best))
