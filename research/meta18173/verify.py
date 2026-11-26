from base import *
import itertools
pairs=[(a,b) for a in range(6) for b in range(a+1,6)]
def col(m):
    for c in itertools.product(range(3),repeat=6):
        if all(not(m>>i&1) or c[a]!=c[b] for i,(a,b) in enumerate(pairs)): return True
    return False
T=target()
bad=[m for m in range(M) if col(m)!=bool(T>>m&1)]
print("mismatch vs 3-col brute force:",len(bad))
# hint check: not3col iff contains K4 or W5
def has(m):
    E=lambda a,b:m>>pairs.index((min(a,b),max(a,b)))&1
    for q in itertools.combinations(range(6),4):
        if all(E(a,b) for a,b in itertools.combinations(q,2)):return True
    for h in range(6):
        o=[v for v in range(6) if v!=h]
        if all(E(h,v) for v in o):
            for p in itertools.permutations(o):
                if p[0]==min(o) and all(E(p[i],p[(i+1)%5]) for i in range(5)):return True
    return False
print("hint mismatch:",sum(1 for m in range(M) if has(m)==col(m)))
