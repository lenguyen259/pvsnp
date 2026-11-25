import itertools, json
import networkx as nx
PET=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
def tau(E):
    Vs=sorted({x for e in E for x in e})
    for k in range(len(Vs)+1):
        for T in itertools.combinations(Vs,k):
            s=set(T)
            if all(a in s or b in s for a,b in E): return k
classes=[]
def relabel(edges):
    vs=sorted({x for e in edges for x in e}); m={v:i for i,v in enumerate(vs)}
    return [(m[a],m[b]) for a,b in edges]
def cls_of(edges):
    if not edges: return None
    G=nx.Graph(edges)
    for idx,(H,E) in enumerate(classes):
        if H.number_of_edges()==G.number_of_edges() and H.number_of_nodes()==G.number_of_nodes() and nx.is_isomorphic(G,H): return idx
    E=relabel(edges); classes.append((nx.Graph(E),E)); return len(classes)-1
def induced(E,Z): return [(a,b) for a,b in E if a not in Z and b not in Z]
for r in range(10,1,-1):
    for keep in itertools.combinations(range(10),r):
        cls_of(induced(PET,set(range(10))-set(keep)))
def info(c):
    G,E=classes[c]; m=len(E); t=tau(E); n=G.number_of_nodes()
    return dict(n=n,m=m,tau=t,phi=m+t-1,maxdeg=max(d for _,d in G.degree()),E=E)
def restrictions(E,fam):
    """yield (S0,S1,F,Hclass) """
    n=max(max(e) for e in E)+1; adj={v:set() for v in range(n)}
    for a,b in E: adj[a].add(b); adj[b].add(a)
    out=[]; seen=set()
    def addr(S0,S1):
        S0=frozenset(S0); S1=frozenset(S1)
        if S0&S1: return
        if any(b in adj[a] for a in S1 for b in S1): return
        if (S0,S1) in seen: return
        seen.add((S0,S1))
        F=set().union(*[adj[v] for v in S1])-S0-S1 if S1 else set()
        H=induced(E,S0|S1|F)
        if not H and not F: return
        out.append((sorted(S0),sorted(S1),len(F),cls_of(H) if H else None))
    V=range(n)
    if 'A2' in fam:
        for k in (1,2):
            for Z in itertools.combinations(V,k): addr(Z,())
    if 'A3' in fam:
        for Z in itertools.combinations(V,3): addr(Z,())
    if 'N' in fam:
        for v in V: addr(adj[v]|{v},()); addr(adj[v],(v,))
    if 'B' in fam:
        for v in V: addr((),(v,))
    if 'B1' in fam:
        for v in V:
            for w in V:
                if w!=v: addr((w,),(v,))
    if 'B2' in fam:
        for v in V:
            for w1,w2 in itertools.combinations([x for x in V if x!=v],2): addr((w1,w2),(v,))
    if 'BB1' in fam:
        for v,w in itertools.combinations(V,2):
            for z in V:
                if z not in (v,w): addr((z,),(v,w))
    if 'BBB' in fam:
        for T in itertools.combinations(V,3): addr((),T)
    if 'BB' in fam:
        for v,w in itertools.combinations(V,2): addr((),(v,w))
    return out
def auts(E):
    G=nx.Graph(E); from networkx.algorithms.isomorphism import GraphMatcher
    return [dict(m) for m in GraphMatcher(G,G).isomorphisms_iter()]
def pair_orbits(E):
    n=max(max(e) for e in E)+1; Au=auts(E); seen=set(); orbs=[]
    Es=set(map(tuple,E))|{(b,a) for a,b in E}
    ps=sorted(itertools.combinations(range(n),2),key=lambda p:(0 if p in Es else 1,p))
    for p in ps:
        if p in seen: continue
        o=sorted({tuple(sorted((g[p[0]],g[p[1]]))) for g in Au}); seen|=set(o); orbs.append([list(x) for x in o])
    return orbs
def stab_orbits(E,fixed_pairs,excl):
    """orbits of pairs under the setwise stabilizer of each pair in fixed_pairs; excl pairs removed"""
    n=max(max(e) for e in E)+1; Au=auts(E)
    St=[g for g in Au if all(tuple(sorted((g[a],g[b])))==tuple(p) for a,b in fixed_pairs for p in [sorted((a,b))])]
    Es=set(map(tuple,E))|{(b,a) for a,b in E}
    ps=sorted(itertools.combinations(range(n),2),key=lambda p:(0 if p in Es else 1,p))
    seen=set(tuple(p) for p in excl); orbs=[]
    for p in ps:
        if p in seen: continue
        o=sorted({tuple(sorted((g[p[0]],g[p[1]]))) for g in St}); seen|=set(o); orbs.append([list(x) for x in o])
    return orbs,len(St)
