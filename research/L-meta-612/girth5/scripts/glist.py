import sys, json
sys.path.insert(0,'../e612')
import networkx as nx
from lib import phiE
nmin,nmax=int(sys.argv[1]),int(sys.argv[2])
for G in nx.graph_atlas_g():
    n=G.number_of_nodes()
    if n<nmin or n>nmax or G.number_of_edges()==0 or any(d==0 for _,d in G.degree()): continue
    if nx.girth(G)<5: continue
    E=list(G.edges()); print(json.dumps(E), phiE(E))
