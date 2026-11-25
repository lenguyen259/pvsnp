import networkx as nx, itertools, json, sys
N=int(sys.argv[1])
def dedupe(gs):
    buck={}
    out=[]
    for G in gs:
        h=nx.weisfeiler_lehman_graph_hash(G)
        L=buck.setdefault(h,[])
        if any(nx.is_isomorphic(G,H) for H in L): continue
        L.append(G); out.append(G)
    return out
level=[nx.empty_graph(1)]
for n in range(2,N+1):
    new=[]
    for G in level:
        D=dict(nx.all_pairs_shortest_path_length(G))
        V=list(G)
        for k in range(0,len(V)+1):
            for S in itertools.combinations(V,k):
                if all(D[a].get(b,99)>=3 for a,b in itertools.combinations(S,2)):
                    H=G.copy(); H.add_node(n-1); H.add_edges_from((n-1,s) for s in S); new.append(H)
    level=dedupe(new)
    print(n,len(level),file=sys.stderr)
for G in level:
    if min(dict(G.degree()).values())>=1:
        print(json.dumps(sorted(tuple(sorted(e)) for e in G.edges())))
