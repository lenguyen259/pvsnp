# Gate-elimination tree search with exactly the checkGTree step semantics (L_meta_9409 checker).
import itertools, sys
from functools import lru_cache
BASE = [  # (k, edges, lb) as in L_meta_982 E0..E20
(3,[(0,1),(0,2),(1,2)],4),
(5,[(0,1),(0,4),(1,2),(2,3),(3,4)],7),
(5,[(0,1),(0,2),(0,3),(0,4),(1,2),(3,4)],8),
(6,[(0,1),(0,2),(0,3),(1,2),(1,4),(2,5)],8),
(6,[(0,1),(0,2),(1,3),(2,4),(3,5),(4,5)],8),
(6,[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)],9),
(6,[(0,1),(0,2),(0,3),(1,2),(1,4),(3,5),(4,5)],9),
(6,[(0,1),(0,2),(0,3),(1,2),(3,4),(3,5),(4,5)],10),
(7,[(0,1),(0,2),(1,3),(2,4),(3,5),(4,6),(5,6)],10),
(7,[(0,1),(0,2),(0,3),(0,4),(1,2),(1,5),(2,6),(3,4)],11),
(7,[(0,1),(0,2),(0,3),(0,4),(1,2),(3,5),(4,6),(5,6)],11),
(7,[(0,1),(0,2),(0,3),(1,2),(1,4),(2,5),(3,6),(4,6)],11),
(7,[(0,1),(0,2),(0,3),(1,2),(1,4),(3,5),(3,6),(4,5)],11),
(7,[(0,1),(0,2),(0,3),(1,2),(1,4),(3,5),(4,6),(5,6)],11),
(7,[(0,1),(0,2),(0,3),(1,2),(3,4),(4,5),(4,6),(5,6)],11),
(7,[(0,1),(0,2),(0,3),(1,4),(2,5),(3,6),(4,5),(4,6)],11),
(7,[(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,2),(3,4),(5,6)],12),
(7,[(0,1),(0,2),(0,3),(0,4),(1,2),(1,5),(1,6),(3,4),(5,6)],12),
(7,[(0,1),(0,2),(0,3),(0,4),(1,2),(1,5),(3,4),(3,6),(5,6)],12),
(7,[(0,1),(0,2),(0,3),(1,2),(1,4),(2,5),(3,6),(4,6),(5,6)],12),
(7,[(0,1),(0,2),(0,3),(1,2),(1,4),(3,5),(3,6),(4,5),(5,6)],12),
]
def canon(E):
    V = sorted({v for e in E for v in e})
    best = None
    for p in itertools.permutations(range(len(V))):
        m = dict(zip(V,p))
        key = tuple(sorted(tuple(sorted((m[a],m[b]))) for a,b in E))
        if best is None or key < best: best = key
    return best
_cc = {}
def ccanon(E):
    E = frozenset(E)
    if E not in _cc: _cc[E] = canon(E)
    return _cc[E]
BASEC = {}
for i,(k,E,lb) in enumerate(BASE):
    c = canon(E)
    if c not in BASEC or BASEC[c][1] < lb: BASEC[c] = (i, lb)
N = 9
G = [(0,4),(1,5),(0,6),(2,6),(1,7),(3,7),(5,7),(2,8),(3,8),(4,8),(7,8)]
G = [tuple(sorted(e)) for e in G]

def nbrs(E,p): return [b if a==p else a for a,b in E if p in (a,b)]
def fix0(A,E,p): return (frozenset(A-{p}), frozenset(e for e in E if p not in e))
def fix1(A,E,p):
    A1 = frozenset(A | set(nbrs(E,p)))
    return (A1, frozenset(e for e in E if p not in e and e[0] not in A1 and e[1] not in A1))
def dep(A,E,p): return p in A or any((a==p and b not in A) or (b==p and a not in A) for a,b in E)

@lru_cache(None)
def val(A,E):
    best = (-1, None)
    if not E: best = (len(A)-1, ('emp',))
    if not A and E:
        c = ccanon(E)
        if c in BASEC and BASEC[c][1] > best[0]: best = (BASEC[c][1], ('base', BASEC[c][0]))
    verts = {v for e in E for v in e} | set(A)
    for p in sorted(verts):
        if not dep(A,E,p): continue
        A0,E0 = fix0(A,E,p)
        v0 = val(A0,E0)[0] if (A0 or E0) else None
        if v0 is not None and 1+v0 > best[0]: best = (1+v0, ('f0',p))
        if p in A: continue
        A1,E1 = fix1(A,E,p)
        v1 = val(A1,E1)[0] if (A1 or E1) else None
        if v1 is not None and 1+v1 > best[0]: best = (1+v1, ('f1',p))
        if v0 is not None and v1 is not None and 2+min(v0,v1) > best[0]: best = (2+min(v0,v1), ('b2',p))
    return best

def tree(A,E):
    v, st = val(A,E)
    if st[0]=='emp': return 'emp'
    if st[0]=='base': return ('base',st[1],sorted(E))
    p = st[1]
    if st[0]=='f0': return ('f0',p,tree(*fix0(A,E,p)))
    if st[0]=='f1': return ('f1',p,tree(*fix1(A,E,p)))
    return ('b2',p,tree(*fix0(A,E,p)),tree(*fix1(A,E,p)))
if __name__=='__main__':
    r = val(frozenset(), frozenset(G))
    print('best', r)
    print(tree(frozenset(), frozenset(G)))
