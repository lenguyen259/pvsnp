import networkx as nx, itertools, collections
from mcsat import exists_circuit, target_tt
from run1h import has_c4, tau as tauG
def tauE(E):
    return tauG(nx.Graph(E)) if E else 0
def phiE(E):
    return len(E)+tauE(E)-1 if E else 0
def nbrs(E,v): return {b for a,b in E if a==v}|{a for a,b in E if b==v}
def phi0(E,v): return phiE([(a,b) for a,b in E if v not in (a,b)])
def phi1(E,v):
    N=nbrs(E,v); H=[(a,b) for a,b in E if a not in N|{v} and b not in N|{v}]
    if not H: return len(N)-1
    return len(N)+phiE(H)
def restrict(n,circ,v,b):
    rep={i:('n',i) for i in range(n)}; rep[v]=('c',b); live={}
    for (i,o,j,k) in circ:
        A,B=rep[j],rep[k]
        if A[0]=='c' or B[0]=='c':
            c,other=(A,B) if A[0]=='c' else (B,A)
            if o=='&': rep[i]= other if c[1]==1 else ('c',0)
            else: rep[i]= other if c[1]==0 else ('c',1)
        elif A==B: rep[i]=A
        else: rep[i]=('n',i); live[i]=(A[1],B[1])
    out=rep[circ[-1][0]]
    if out[0]=='c': return 0
    seen=set(); st=[out[1]]
    while st:
        x=st.pop()
        if x in live and x not in seen: seen.add(x); st.extend(live[x])
    return len(seen)
def minimal_ands(n,circ):
    sets={i:frozenset([i]) for i in range(n)}; isor={i:True for i in range(n)}; res=[]
    for (i,o,j,k) in circ:
        if o=='|' and isor[j] and isor[k]: sets[i]=sets[j]|sets[k]; isor[i]=True
        else:
            isor[i]=False
            if o=='&' and isor[j] and isor[k]: res.append((i,sets[j],sets[k]))
    return res
def goodset(n,E,c):
    """(v,b) with elim >= Phi-Phi(G_b)"""
    s=len(c); P=phiE(E); out=set(); slack={}
    for v in range(n):
        for b in (0,1):
            need=P-(phi0(E,v) if b==0 else phi1(E,v))
            el=s-restrict(n,c,v,b); slack[(v,b)]=el-need
            if el>=need: out.add((v,b))
    return out,slack
def graphs(nmin,nmax):
    for G in nx.graph_atlas_g():
        n=G.number_of_nodes()
        if n<nmin or n>nmax or G.number_of_edges()==0 or any(d==0 for _,d in G.degree()) or has_c4(G): continue
        yield n,list(G.edges())
def fmt(c):
    return ' '.join('%d=%d%s%d'%(i,j,o,k) for i,o,j,k in c)
def restrict_plus(n,circ,v,b):
    """restriction followed by functional reduction: every gate whose function equals a constant
    or an earlier node is replaced by it; returns remaining live gates"""
    full=(1<<(1<<n))-1
    T={}
    for u in range(n): T[u]=sum(1<<r for r in range(1<<n) if (r>>u)&1)
    T[v]=full if b else 0
    rep={u:u for u in range(n)}; first={}
    for u in range(n):
        if u!=v: first.setdefault(T[u],u)
    first.setdefault(0,'c0'); first.setdefault(full,'c1')
    live={}
    for (i,o,j,k) in circ:
        a,bb=T[rep[j]] if rep[j] not in ('c0','c1') else (0 if rep[j]=='c0' else full), None
        tj=T[j] ; tk=T[k]
        t=(tj&tk) if o=='&' else (tj|tk); T[i]=t
        if t in first: rep[i]=first[t]
        else: first[t]=i; rep[i]=i; live[i]=(j,k)
    def R(x):
        while x in rep and rep[x]!=x: x=rep[x]
        return x
    out=R(circ[-1][0])
    if out not in live: return 0
    seen=set(); st=[out]
    while st:
        x=st.pop()
        if x in live and x not in seen:
            seen.add(x); st.extend(R(y) for y in live[x])
    return len(seen)
