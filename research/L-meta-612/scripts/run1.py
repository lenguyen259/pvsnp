import networkx as nx, itertools, time, sys
from mcsat import *
def has_c4(G):
    for u,v in itertools.combinations(G.nodes(),2):
        if len(set(G[u])&set(G[v]))>=2: return True
    return False
def tau(G):
    V=list(G.nodes())
    for k in range(len(V)+1):
        for T in itertools.combinations(V,k):
            T=set(T)
            if all(a in T or b in T for a,b in G.edges()): return k
maxn=int(sys.argv[1]); onlytri=len(sys.argv)>2
for G in nx.graph_atlas_g():
    n=G.number_of_nodes()
    if n<2 or n>maxn or G.number_of_edges()==0: continue
    if any(d==0 for _,d in G.degree()): continue
    if has_c4(G): continue
    tri=sum(nx.triangles(G).values())//3
    if onlytri and tri==0: continue
    E=list(G.edges()); t=tau(G); phi=len(E)+t-1
    tt=target_tt(n,E)
    t0=time.time()
    r,_=exists_circuit(n,tt,phi-1)
    r2,m=exists_circuit(n,tt,phi,want_model=True)
    print(n,len(E),t,'tri',tri,'conn',nx.is_connected(G),'phi',phi,'size phi-1 possible:',r,'size phi possible:',r2,'%.1fs'%(time.time()-t0),E,flush=True)
