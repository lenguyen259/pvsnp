"""analysis of config-(2) instances: X=N[a] bounds."""
import sys,json,itertools,collections
sys.path.insert(0,'/home/user/pvsnp/research/L-meta-612/t3/scripts')
from gen import *   # t2lib + gneed/gopt
SC='/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad'
def load(files):
    seen=set()
    for fn in files:
        try: L=open(fn).read().split('\n')
        except FileNotFoundError: continue
        for l in L:
            if not l.strip(): continue
            d=json.loads(l); k=(tuple(map(tuple,d['E'])),d['c'])
            if k in seen: continue
            seen.add(k); yield d
def readers(c):
    R=collections.defaultdict(list)
    for i,o,j,k in c: R[j].append(i); R[k].append(i)
    return R
def Dsets(g,c,X):
    T=tables(g,c,{}); M=0
    for x in X: M|=g.X[x]
    D={i for i,o,j,k in c if (T[i]&~M&g.full)==0}
    nodesX=set(X)|D
    dD={i for i,o,j,k in c if i not in D and o=='|' and (j in nodesX or k in nodesX)}
    return D,dD
def dead(g,c,D,dD,X):
    """dead closure after constants (D) and copies (dD): syntactic"""
    R=readers(c); out=c[-1][0]; gone=set(D)|set(dD); dd=set()
    # copies in dD: q=d|p -> p ; readers of q become readers of p. alive(p) if some reader alive.
    alive={out}
    rep={}
    for i,o,j,k in reversed(c):
        pass
    # compute liveness top-down: node alive if it is output (and not gone) or some reader r alive and r not constant and (r not copy or p is the passing input)
    gate={x[0]:x for x in c}
    live=set()
    def passing(q):
        i,o,j,k=gate[q]; nodesX=set(X)|D
        return k if j in nodesX else j
    for i,o,j,k in reversed(c):
        if i==out: live.add(i) if i not in D else None
        # mark inputs
    # simple iterative
    live=set(); changed=True
    keep=[x[0] for x in c]
    status={}
    for q in reversed(keep):
        if q==out: status[q]=True
        else:
            st=False
            for r in R[q]:
                if not status.get(r,False) and r not in dD: continue
                if r in D: continue
                if r in dD:
                    # r alive in the sense of its readers
                    if passing(r)==q and status.get(('pass',r),False): st=True
                    continue
                st=True
            status[q]=st
        if q in dD: status[('pass',q)]=status[q]; status[q]=False
    return {q for q in keep if q not in D and q not in dD and not status[q]}
def info(g,c,a):
    X=set(g.N[a])|{a}
    H=g.Eminus(X)
    need=g.P-phi(H) if H else None
    D,dD=Dsets(g,c,X)
    e=elim(g,c,{x:0 for x in X})
    eR=len(c)-len(ruleR(g,c,{x:0 for x in X}))
    dd=dead(g,c,D,dD,X)
    eN=sum(1 for e_ in g.E if e_[0] in X or e_[1] in X)
    drop=g.t-tau(H) if H else g.t
    return dict(a=a,need=need,elim=e,L1=len(D)+len(dD),Ldead=len(D)+len(dD)+len(dd),eR=eR,eN=eN,drop=drop,D=len(D),dD=len(dD),dd=len(dd))
def topset(g,c,rho):
    T2=tables(g,c,rho); fo=T2[c[-1][0]]
    return {i for i,o,j,k in c if T2[i]==fo}
def Ltop(g,c,X):
    D,dD=Dsets(g,c,X); Tp=topset(g,c,{x:0 for x in X})
    return len(D|dD|Tp)-1
def L2b(g,c,rho):
    """|const|+sum over functions (#gates computing it - [first is gate]) : functional bound w/o dead"""
    T=tables(g,c,rho); full=g.full; seen=set(); n=0
    for u in range(g.n):
        if T[u] not in (0,full): seen.add(T[u])
    for i,o,j,k in c:
        if T[i] in (0,full) or T[i] in seen: n+=1
        else: seen.add(T[i])
    return n
