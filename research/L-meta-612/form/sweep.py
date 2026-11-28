import networkx as nx, sys, time, json
from networkx.generators.atlas import graph_atlas_g
from drv import run, tau
mode=sys.argv[1]; nmax=int(sys.argv[2]); nmin=int(sys.argv[3]) if len(sys.argv)>3 else 2
def c4free(G):
    for a in G:
        for b in G:
            if a<b and len(set(G[a])&set(G[b]))>=2: return False
    return True
res=[]
for G in graph_atlas_g():
    n=G.number_of_nodes()
    if n<nmin or n>nmax or G.number_of_edges()==0: continue
    if any(G.degree(v)==0 for v in G): continue
    if not c4free(G): continue
    E=sorted(tuple(sorted(e)) for e in G.edges())
    t=tau(n,E); t0=time.time()
    m,w=run(n,E,mode,len(E)+t,timeout=900)
    tri=sum(nx.triangles(G).values())//3
    print(json.dumps(dict(n=n,E=E,tau=t,phi=len(E)+t-1,minleaves=m,tri=tri,w=w,sec=round(time.time()-t0,1))),flush=True)
