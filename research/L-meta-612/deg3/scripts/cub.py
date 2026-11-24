"""Enumerate cubic C4-free graphs on n vertices (backtracking, crude iso-reduction by invariants via networkx)."""
import sys,itertools
import networkx as nx
n=int(sys.argv[1])
res=[]
def ok_add(N,a,b):
    # adding ab creates C4 iff exists c,d: a-c-d-b path of length 3 (c!=b,d!=a) or common nbr pair
    if len(N[a])>=3 or len(N[b])>=3 or b in N[a]: return False
    # C4 a-b-x-y-a : x in N[b], y in N[a], x~y
    for x in N[b]:
        for y in N[a]:
            if x!=y and y in N[x]: return False
    # also two common neighbours? a-c-b-d-a needs a,b common nbrs c,d: |N[a]&N[b]|>=2 => C4 already among existing+? that C4 doesn't use ab; existing graph would have it. skip
    return True
found=[]
def rec(N):
    # pick smallest vertex with deg<3
    v=next((u for u in range(n) if len(N[u])<3),None)
    if v is None:
        G=nx.Graph(); G.add_edges_from((a,b) for a in range(n) for b in N[a] if a<b)
        if not any(nx.is_isomorphic(G,H) for H in found): found.append(G)
        return
    for w in range(v+1,n):
        if ok_add(N,v,w):
            N[v].add(w); N[w].add(v); rec(N); N[v].discard(w); N[w].discard(v)
    # if no completion, dead end
N=[set() for _ in range(n)]
rec(N)
for G in found:
    print(n,'girth',min(len(c) for c in nx.minimum_cycle_basis(G)),'tri',sum(nx.triangles(G).values())//3,sorted(G.edges()))
