import itertools
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
