"""sav-version of Lemma D on the min-degree>=2 cache, and on the case-(a) constructions."""
import sys, pickle, collections
sys.path.insert(0, '.')
from h1 import red, nor, chv, parse
def savs(n, E, c):
    R, T = red(n, c); base = nor(R); ch = chv(n, R, T)
    sup = sorted({x for e in E for x in e}); deg = {v: sum(1 for e in E if v in e) for v in sup}
    s = {v: base - nor(red(n, c, {v: 0})[0]) for v in sup}
    return deg, s, ch
if __name__ == '__main__':
    D = pickle.load(open('/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/lemD/data.pkl', 'rb'))
    st = collections.Counter(); ex = []
    for d in D:
        deg, s, ch = savs(d['n'], d['E'], d['c']); md = min(deg.values())
        good = [v for v in deg if s[v] >= deg[v]]
        st['n'] += 1; st['some'] += bool(good); st['some_mindeg'] += any(deg[v] == md for v in good)
        st['all'] += len(good) == len(deg); st['all_mindeg'] += all(s[v] >= deg[v] for v in deg if deg[v] == md)
        st['ch_some_mindeg'] += any(ch[v] >= deg[v] for v in deg if deg[v] == md)
        hubs = [v for v in deg if deg[v] >= 3]
        if hubs:
            st['has_hub'] += 1; st['some_hub_sav'] += any(s[v] >= deg[v] for v in hubs)
        if not all(s[v] >= deg[v] for v in deg if deg[v] == md) and len(ex) < 3:
            ex.append((d['E'], ' '.join('%d=%d%s%d' % (i, j, o, k) for i, o, j, k in d['c']), s, ch))
    print(dict(st))
    for e in ex: print(e)
