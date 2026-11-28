"""For explicit circuits, test every vertex set X: sav(X:=0) >= e(X) - [G-X edgeless]."""
import sys, itertools
sys.path.insert(0, '.')
from h1 import red, nor, chv, parse
import star, thmN2
def test(name, n, E, c, show=5):
    R, T = red(n, c); base = nor(R); ch = chv(n, R, T)
    sup = sorted({x for e in E for x in e})
    deg = {v: sum(1 for e in E if v in e) for v in sup}
    N = {v: {b for a, b in E if a == v} | {a for a, b in E if b == v} for v in sup}
    indep = lambda X: not any(a in X and b in X for a, b in E)
    fails = []; nfail_ind = 0; nind = 0
    for k in range(1, len(sup) + 1):
        for X in itertools.combinations(sup, k):
            X = set(X); eX = sum(1 for a, b in E if a in X or b in X)
            need = eX - (1 if eX == len(E) else 0)
            s = base - nor(red(n, c, {x: 0 for x in X})[0])
            if indep(X): nind += 1
            if s < need:
                fails.append((sorted(X), s, need)); nfail_ind += indep(X)
    nbr = [v for v in sup if any(sorted(N[v]) == f[0] for f in fails)]
    print(name, '#OR', base, '|E|', len(E), 'ch', dict(ch), 'deg', deg)
    print('  failing X:', len(fails), 'of', 2 ** len(sup) - 1, '; independent failing', nfail_ind, 'of', nind,
          '; N(v) failing for v in', nbr)
    print('  smallest fails', sorted(fails, key=lambda f: len(f[0]))[:show])
    return fails
if __name__ == '__main__':
    E7 = [(0,1),(0,4),(0,5),(1,2),(1,4),(2,6),(3,5),(3,6),(5,6)]
    c7 = parse('7=6|1 8=2&7 9=5|6 10=3&9 11=0|1 12=4&11 13=1|5 14=0&13 15=5&6 16=8|10 17=16|12 18=17|14 19=18|15')
    test('constrS n7', 7, E7, c7)
    Et = [(0,1),(0,2),(0,3),(1,2),(3,4),(3,5),(4,5)]
    ct = parse('6=0&3 7=1|6 8=2|6 9=4|6 10=5|6 11=7&8 12=7|8 13=0&12 14=11|13 15=9&10 16=9|10 17=3&16 18=15|17 19=14|18')
    test('thmN 2tri+bridge', 6, Et, ct)
    # subdivided K4: hubs 0..3, subdivision vertex for each pair
    EK = []; s = 4
    for a, b in itertools.combinations(range(4), 2): EK += [(a, s), (b, s)]; s += 1
    test('subdiv K4 constrS', 10, EK, star.build(10, EK), show=8)
    EN = [(0,3),(1,3),(1,4),(2,4),(0,5),(2,5),(0,6),(6,7),(1,7),(2,8),(8,9),(0,9)]
    test('N2 n10', 10, EN, thmN2.build(10, EN, 3, 4), show=8)
