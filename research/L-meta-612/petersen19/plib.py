# Petersen library: graph, automorphisms, restriction family with unconditional bounds
import itertools
PET=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,5),(1,6),(2,7),(3,8),(4,9),(5,7),(7,9),(9,6),(6,8),(8,5)]
n=10
ADJ={v:set() for v in range(n)}
for a,b in PET: ADJ[a].add(b); ADJ[b].add(a)
ES=set(PET)|{(b,a) for a,b in PET}
def f(r): return any((r>>a)&1 and (r>>b)&1 for a,b in PET)
def auts():
    out=[]
    for p in itertools.permutations(range(n)):
        if all((p[a],p[b]) in ES for a,b in PET): out.append(p)
    return out
def induced(V):
    V=set(V); return [(a,b) for a,b in PET if a in V and b in V]
def tau(E):
    Vs=sorted({x for e in E for x in e})
    for k in range(len(Vs)+1):
        for T in itertools.combinations(Vs,k):
            s=set(T)
            if all(a in s or b in s for a,b in E): return k
def is_pf(V):
    V=sorted(V)
    for k in range(1,len(V)+1):
        for S in itertools.combinations(V,k):
            if len(induced(S))>k: return False
    return True
def restrictions():
    """all (A,B): A independent (set to 1), B superset of N(A) (set to 0), A,B disjoint,
    H=P-A-B a pseudoforest with an edge. Bound: surviving AND>=tau(H), OR>=|E(H)|-1."""
    out=[]
    for ka in range(0,4):
        for A in itertools.combinations(range(n),ka):
            if any(b in ADJ[a] for a in A for b in A): continue
            NA=set().union(*[ADJ[a] for a in A]) if A else set()
            rest=[v for v in range(n) if v not in A and v not in NA]
            for kz in range(0,len(rest)+1):
                for Z in itertools.combinations(rest,kz):
                    B=NA|set(Z); V=[v for v in rest if v not in Z]
                    H=induced(V)
                    if not H: continue
                    if not is_pf(V): continue
                    out.append((tuple(A),tuple(sorted(B)),len(H),tau(H)))
    return out
if __name__=='__main__':
    Au=auts(); print('aut',len(Au))
    R=restrictions(); print('restr',len(R))
    from collections import Counter
    print(Counter((len(A),len(B),m,t) for A,B,m,t in R))
