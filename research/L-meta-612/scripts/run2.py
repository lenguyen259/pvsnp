import networkx as nx, itertools, time, sys
from mcsat import *
from run1h import has_c4, tau
maxn=int(sys.argv[1]); extra=int(sys.argv[2])
for G in nx.graph_atlas_g():
    n=G.number_of_nodes()
    if n<2 or n>maxn or G.number_of_edges()==0: continue
    if any(d==0 for _,d in G.degree()): continue
    if has_c4(G): continue
    E=list(G.edges()); t=tau(G); phi=len(E)+t-1; tt=target_tt(n,E)
    resA=[s for s in range(1,phi+extra+1) if exists_circuit(n,tt,s,max_and=t-1)[0]]
    resO=[] if len(E)<2 else [s for s in range(1,phi+extra+1) if exists_circuit(n,tt,s,max_or=len(E)-2)[0]]
    print(n,len(E),t,'fewAND sizes',resA[:1],'fewOR sizes',resO[:1],E,flush=True)
