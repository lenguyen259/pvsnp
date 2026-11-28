# case-(a)-type graphs: 2 or 3 hubs (deg>=3), all others deg 2, C4-free, simple, connected, n<=NMAX
import itertools, networkx as nx
from common import has_c4
def build(h, threads):
    # threads: list of (a,b,k) hub a to hub b (a==b loop) with k internal vertices
    E=[]; n=h
    for a,b,k in threads:
        path=[a]+list(range(n,n+k))+[b]; n+=k
        E+= [(path[i],path[i+1]) for i in range(len(path)-1)]
    return n,E
def gen(NMAX=10):
    seen=set(); out=[]
    for h in (2,3):
        pairs=[(a,b) for a in range(h) for b in range(a,h)]
        for m in range(2,6):
            for combo in itertools.combinations_with_replacement([(a,b,k) for a,b in pairs for k in range(0,6)],m):
                n,E=build(h,list(combo))
                if n>NMAX: continue
                es=[tuple(sorted(e)) for e in E]
                if len(set(es))<len(es) or any(a==b for a,b in es): continue
                G=nx.Graph(es); G.add_nodes_from(range(n))
                if not nx.is_connected(G): continue
                d=dict(G.degree())
                if min(d.values())<2 or sum(1 for v in d if d[v]>=3)!=h: continue
                if has_c4(n,es): continue
                key=nx.weisfeiler_lehman_graph_hash(G)
                if key in seen: continue
                seen.add(key); out.append((n,es))
    return out
if __name__=='__main__':
    L=gen(); print(len(L))
    for n,E in L: print(n,E)
