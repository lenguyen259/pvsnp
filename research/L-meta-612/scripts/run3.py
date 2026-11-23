import networkx as nx, time
from mcsat import *
from run1h import tau
gs={'F3 windmill':[(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(0,5),(0,6),(5,6)],
    'K3+path-pendants':[(0,1),(1,2),(0,2),(0,3),(3,4),(1,5),(5,6)],
    'two triangles + bridge path':[(0,1),(1,2),(0,2),(2,3),(3,4),(4,5),(5,6),(4,6)]}
for name,E in gs.items():
    G=nx.Graph(E); n=G.number_of_nodes(); t=tau(G); phi=len(E)+t-1
    t0=time.time(); r,_=exists_circuit(n,target_tt(n,E),phi-1)
    print(name,'E',len(E),'tau',t,'phi',phi,'size phi-1 possible:',r,'%.0fs'%(time.time()-t0),flush=True)
