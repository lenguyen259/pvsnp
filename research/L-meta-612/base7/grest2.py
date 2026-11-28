# Extended restriction family: A (independent) := 1, B := 0 (B disjoint from A, arbitrary),
# U = N(A) \ B stay free as OR-singletons, H = G - A - N(A) - B.
# Restricted function = OR_{u in U} x_u  v  f_H.  Bounds (all PROVED, see README):
#   U empty, H pseudoforest: AND>=tau(H), OR>=|E(H)|-1           (Theorem PF)
#   U empty, H in proven table: total>=L(H)
#   U nonempty: total >= L(H)+|U| if H has an edge (sequential elimination), |U|-1 if H edgeless
import itertools, json, sys
import networkx as nx
from grest import tau, is_pf, load_proven
def family2(E,proven,minL=1):
    n=max(max(e) for e in E)+1; adj={v:set() for v in range(n)}
    for a,b in E: adj[a].add(b); adj[b].add(a)
    def Lof(H):
        if not H: return 0,0,0
        if is_pf(H): t=tau(H); return t,len(H)-1,len(H)+t-1
        GH=nx.Graph(H); best=None
        for PG,L in proven:
            if PG.number_of_edges()==GH.number_of_edges() and PG.number_of_nodes()==GH.number_of_nodes() and nx.is_isomorphic(PG,GH):
                best=L if best is None else max(best,L)
        if best is None: return None
        return 0,0,best
    out=[]
    for ka in range(0,n+1):
        for Aa in itertools.combinations(range(n),ka):
            if any(b in adj[a] for a in Aa for b in Aa): continue
            NA=set().union(*[adj[a] for a in Aa]) if Aa else set()
            others=[v for v in range(n) if v not in Aa]
            for kb in range(0,len(others)+1):
                for B in itertools.combinations(others,kb):
                    if not Aa and not B: continue
                    U=NA-set(B); V=set(others)-NA-set(B)
                    H=[(a,b) for a,b in E if a in V and b in V]
                    r=Lof(H)
                    if r is None: continue
                    aL,oL,tL=r
                    if U:
                        if not H: aL,oL,tL=0,0,len(U)-1
                        else: aL,oL,tL=0,0,tL+len(U)   # split bounds implied by the U:=0 restriction
                    if tL<minL: continue
                    out.append([list(Aa),sorted(B),aL,oL,tL])
    return out
if __name__=='__main__':
    E=[tuple(e) for e in json.loads(sys.argv[1])]; minL=int(sys.argv[3]) if len(sys.argv)>3 else 1
    fam=family2(E,load_proven(),minL); json.dump(fam,open(sys.argv[2],'w'))
    from collections import Counter
    print(len(fam),'restrictions', sorted(Counter(x[4] for x in fam).items()))
