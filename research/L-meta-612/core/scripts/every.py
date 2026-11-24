"""Test 'every v: sav(x_v:=0) >= deg v - [G-v edgeless]' (URP1) on the whole corpus; also ch-version counts."""
import sys, collections, random
sys.path.insert(0, '/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/orb')
sys.path.insert(0, '.')
from tr import load, DIRS
from h1 import red, nor, chv
st = collections.Counter(); seen = set(); ex = []
for fn, n, E, X, c in load(DIRS):
    key = (tuple(E), tuple(c))
    if key in seen: continue
    seen.add(key)
    sup = sorted({x for e in E for x in e})
    if len(E) < 2: continue
    R, T = red(n, c); base = nor(R); ch = chv(n, R, T)
    st['circ'] += 1
    bad = []
    for v in sup:
        d = sum(1 for e in E if v in e); need = d - (1 if d == len(E) else 0)
        s = base - nor(red(n, c, {v: 0})[0])
        if s < need: bad.append((v, s, need, ch[v]))
    st['allv_ok'] += (not bad); st['some_ok'] += len(bad) < len(sup)
    if bad:
        st['bad_vertices'] += len(bad)
        if len(ex) < 6: ex.append((E, ' '.join('%d=%d%s%d' % (i, j, o, k) for i, o, j, k in c), bad))
print(dict(st))
for e in ex: print(e)
