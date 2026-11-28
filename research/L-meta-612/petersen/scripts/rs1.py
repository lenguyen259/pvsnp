# randomized family: J = OR of chosen edge monomials; z_v = x_v|J for v in Z; F = star cover on nodes, optionally J joined into outer OR
import random, sys, itertools
from common import *
n=10;E=PET; random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
N={v:[b for a,b in E if a==v]+[a for a,b in E if b==v] for v in range(n)}
def covers():
    out=[]
    for k in (6,7):
        for T in itertools.combinations(range(n),k):
            s=set(T)
            if all(a in s or b in s for a,b in E): out.append(T)
    return out
CV=covers(); best={}
for t in range(int(sys.argv[2]) if len(sys.argv)>2 else 3000):
    k=random.choice([2,2,2,3])
    pairs=random.sample(E,k)
    Z=[v for v in range(n) if random.random()<random.choice([0.5,0.7,0.9,1.0])]
    cov=list(random.choice(CV)); random.shuffle(cov)
    joinJ=random.random()<0.5
    b=B(n); J=b.OR([b.g('&',a,c) for a,c in pairs])
    node={v:(b.g('|',v,J) if v in Z else v) for v in range(n)}
    rest=[e for e in E if not (joinJ and e in pairs)]
    terms=[J] if joinJ else []
    for h in cov:
        L=[q if p==h else p for p,q in rest if h in (p,q)]
        random.shuffle(L)
        if not L: continue
        terms.append(b.g('&',node[h],b.OR([node[x] for x in L]))); rest=[e for e in rest if h not in e]
    if random.random()<0.5: random.shuffle(terms)
    b.OR(terms)
    r=analyze(n,b.c,E)
    assert r['ok']
    key=r['slack']
    if key<=-1 and (key not in best or r['size']<best[key][0]):
        best[key]=(r['size'],r['nor'],r['nand'],fmt(r['R']),r['ch']); print(key,best[key][:3],best[key][4],flush=True)
print(best)
