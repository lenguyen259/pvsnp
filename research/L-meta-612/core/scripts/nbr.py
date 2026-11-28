"""Every v: sav(N(v):=0) >= e(N(v)) - [G-N(v) edgeless]?  Plus all-X census on a sample."""
import sys, collections, random, itertools
sys.path.insert(0, '/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/orb'); sys.path.insert(0, '.')
from tr import load, DIRS
from h1 import red, nor
random.seed(1)
st = collections.Counter(); seen = set(); ex = []; cls = collections.Counter(); clsn = collections.Counter()
def need(E, X):
    e = sum(1 for a, b in E if a in X or b in X); return e - (1 if e == len(E) else 0)
for fn, n, E, Xx, c in load(DIRS):
    key = (tuple(E), tuple(c))
    if key in seen or len(E) < 2: continue
    seen.add(key)
    sup = sorted({x for e in E for x in e}); N = {v: {b for a, b in E if a == v} | {a for a, b in E if b == v} for v in sup}
    base = nor(red(n, c)[0]); sav = lambda X: base - nor(red(n, c, {x: 0 for x in X})[0])
    st['circ'] += 1
    bad = [v for v in sup if sav(N[v]) < need(E, N[v])]
    st['allN_ok'] += not bad
    if bad and len(ex) < 4: ex.append((E, ' '.join('%d=%d%s%d' % (i, j, o, k) for i, o, j, k in c), bad))
    if random.random() < 0.03:
        st['sample'] += 1
        for k in range(1, len(sup) + 1):
            for X in itertools.combinations(sup, k):
                X = set(X); ind = not any(a in X and b in X for a, b in E)
                vc = all(a in X or b in X for a, b in E)
                key2 = ('size%d' % k if k <= 2 else 'size>=3') + ('_ind' if ind else '') + ('_cover' if vc else '')
                clsn[key2] += 1
                if sav(X) < need(E, X): cls[key2] += 1
print(dict(st)); print('fail/total by class:', {k: (cls[k], clsn[k]) for k in sorted(clsn)})
for e in ex: print(e)
