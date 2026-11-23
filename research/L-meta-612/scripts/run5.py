import networkx as nx, itertools, sys, collections
from mcsat import *
from run1h import has_c4, tau
def phi_edges(E,Vs):
    if not E: return 0
    H=nx.Graph(E); return len(E)+tau(H)-1
def phiG(E):  return phi_edges(E,None)
def phi1(E,v):
    N={b for a,b in E if a==v}|{a for a,b in E if b==v}
    H=[(a,b) for a,b in E if a not in N|{v} and b not in N|{v}]
    if not H: return len(N)-1
    return len(N)+phi_edges(H,None)
def phi0(E,v): return phi_edges([(a,b) for a,b in E if v not in (a,b)],None)
def restrict(n,circ,v,b):
    # node values: ('c',0/1) or ('n',id) ; returns remaining gate count
    rep={i:('n',i) for i in range(n)}; rep[v]=('c',b)
    live={}
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
        if x in live and x not in seen:
            seen.add(x); st.extend(live[x])
    return len(seen)
maxn=int(sys.argv[1]); lim=int(sys.argv[2])
for G in nx.graph_atlas_g():
    n=G.number_of_nodes()
    if n<2 or n>maxn or G.number_of_edges()==0 or any(d==0 for _,d in G.degree()) or has_c4(G): continue
    E=list(G.edges()); P=phiG(E)
    X=int(sys.argv[3]); circs=exists_circuit(n,target_tt(n,E),P+X,enum_all=lim)
    bad=0; goodcount=collections.Counter(); leafok=0
    for c in circs:
        good=[(v,b) for v in range(n) for b in (0,1) if restrict(n,c,v,b)-X<=(phi0(E,v) if b==0 else phi1(E,v))]
        if not good: bad+=1; badc=c
        for vb in good: goodcount[vb]+=1
    allv=[vb for vb,cnt in goodcount.items() if cnt==len(circs)]
    print(n,len(E),'tri',sum(nx.triangles(G).values())//3,'#opt',len(circs),'no-good-restriction:',bad,'universally good (v,b):',allv,E,flush=True)
    if bad: print('   BAD circuit',badc,flush=True)
