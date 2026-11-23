import sys, json, time
from mcsat import *
import networkx as nx
from run1h import tau
E=json.loads(sys.argv[1]); G=nx.Graph(E); n=max(max(e) for e in E)+1
t=tau(G); phi=len(E)+t-1; t0=time.time()
r,m=exists_circuit(n,target_tt(n,E),phi-1,want_model=True)
print(len(E),t,phi,'PHI-1 POSSIBLE' if r else 'unsat', m if r else '', '%.0fs'%(time.time()-t0),E,flush=True)
