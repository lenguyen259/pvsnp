# restriction family for an arbitrary graph G (edge list), with a table of PROVEN lower bounds for
# non-pseudoforest graphs (proven.json: list of [edges, L]); pseudoforests use Theorem PF split bounds.
import itertools, json, sys
import networkx as nx
def tau(E):
    Vs=sorted({x for e in E for x in e})
    for k in range(len(Vs)+1):
        for T in itertools.combinations(Vs,k):
            s=set(T)
            if all(a in s or b in s for a,b in E): return k
def is_pf(E):
    G=nx.Graph(E)
    return all(C.number_of_edges()<=C.number_of_nodes() for C in (G.subgraph(c) for c in nx.connected_components(G)))
def c4free(E):
    G=nx.Graph(E)
    return not any(len(set(G[a])&set(G[b]))>=2 for a,b in itertools.combinations(G.nodes(),2))
def load_proven(fn='proven.json'):
    try: return [(nx.Graph([tuple(e) for e in Es]),L) for Es,L in json.load(open(fn))]
    except FileNotFoundError: return []
def family(E,proven,include_self=False):
    n=max(max(e) for e in E)+1; adj={v:set() for v in range(n)}
    for a,b in E: adj[a].add(b); adj[b].add(a)
    out=[]
    for ka in range(0,n+1):
        for A in itertools.combinations(range(n),ka):
            if any(b in adj[a] for a in A for b in A): continue
            NA=set().union(*[adj[a] for a in A]) if A else set()
            rest=[v for v in range(n) if v not in A and v not in NA]
            for kz in range(0,len(rest)+1):
                for Z in itertools.combinations(rest,kz):
                    B=NA|set(Z)
                    if not A and not B: continue
                    V=set(rest)-set(Z)
                    H=[(a,b) for a,b in E if a in V and b in V]
                    if not H: continue
                    if is_pf(H):
                        t=tau(H); m=len(H); out.append([list(A),sorted(B),t,m-1,m+t-1]); continue
                    GH=nx.Graph(H); best=None
                    for PG,L in proven:
                        if PG.number_of_edges()==GH.number_of_edges() and PG.number_of_nodes()==GH.number_of_nodes() and nx.is_isomorphic(PG,GH):
                            best=L if best is None else max(best,L)
                    if best is not None: out.append([list(A),sorted(B),0,0,best])
    return out
if __name__=='__main__':
    E=[tuple(e) for e in json.loads(sys.argv[1])]; fam=family(E,load_proven())
    json.dump(fam,open(sys.argv[2],'w')); print(len(fam),'restrictions; max tL',max(x[4] for x in fam))
