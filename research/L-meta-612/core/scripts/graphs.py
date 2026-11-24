import sys
sys.path.insert(0,'/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/e612')
import networkx as nx
from lib import phiE
from run1h import has_c4
def casea(nmax):
    for G in nx.graph_atlas_g():
        n=G.number_of_nodes()
        if n<3 or n>nmax or G.number_of_edges()==0: continue
        d=dict(G.degree())
        if min(d.values())!=2 or has_c4(G): continue
        if sum(1 for x in d.values() if x>=3)<2: continue
        yield n,sorted(tuple(sorted(e)) for e in G.edges())
if __name__=='__main__':
    for n,E in casea(int(sys.argv[1])):
        print(n,len(E),phiE(E),[list(e) for e in E], nx.is_connected(nx.Graph(E)))
