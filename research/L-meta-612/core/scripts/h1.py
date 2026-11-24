"""Hybrid restriction test.  For a circuit c on n vars computing f_G:
 sav(rho) = #OR(reduce(c)) - #OR(reduce(c|rho)), rho a partial 0/1 assignment.
 good0(v): ch(v) >= deg v            (Lemma D branch, x_v:=0)
 good1(v): sav(v=1, N(v)=0) >= e(N(v)) (edges meeting N(v))
 goodZ(v): sav(N[v]=0) >= e(N(v))
Reduction: drop gates computing a constant or a function equal to an earlier node; drop dead gates."""
import sys, pickle, collections
def tables(n, c, rho):
    full = (1 << (1 << n)) - 1
    T = {}
    for u in range(n):
        if u in rho: T[u] = full if rho[u] else 0
        else: T[u] = sum(1 << r for r in range(1 << n) if (r >> u) & 1)
    for i, o, j, k in c: T[i] = (T[j] & T[k]) if o == '&' else (T[j] | T[k])
    return T, full
def red(n, c, rho={}):
    T, full = tables(n, c, rho)
    canon = {}; first = {}; real = {}
    for u in range(n):
        if T[u] in (0, full): canon[u] = 'K'
        else: canon[u] = u; first.setdefault(T[u], u)
    for i, o, j, k in c:
        if T[i] in (0, full): canon[i] = 'K'; continue
        if T[i] in first: canon[i] = first[T[i]]; continue
        first[T[i]] = i; canon[i] = i; real[i] = (o, canon[j], canon[k])
    out = canon[c[-1][0]]; seen = set(); st = [out]
    while st:
        x = st.pop()
        if x in real and x not in seen: seen.add(x); st.extend(y for y in real[x][1:] if y != 'K')
    R = {i: real[i] for i in seen}
    return R, T
def nor(R): return sum(1 for g in R.values() if g[0] == '|')
def chv(n, R, T):
    xv = {v: sum(1 << r for r in range(1 << n) if (r >> v) & 1) for v in range(n)}
    core = lambda q: {v for v in range(n) if T[q] & ~xv[v] == 0}
    ch = collections.Counter()
    for i, (o, j, k) in R.items():
        if o == '|':
            for v in core(j) | core(k): ch[v] += 1
    return ch
def analyse(n, E, c):
    sup = sorted({x for e in E for x in e})
    N = {v: {b for a, b in E if a == v} | {a for a, b in E if b == v} for v in sup}
    R, T = red(n, c); base = nor(R); ch = chv(n, R, T)
    eN0 = lambda X: sum(1 for a, b in E if a in X or b in X)
    eN = lambda X: eN0(X) - (1 if eN0(X) == len(E) else 0)
    res = {}
    for v in sup:
        r1 = {v: 1}; r1.update({w: 0 for w in N[v]})
        rz = {w: 0 for w in N[v] | {v}}
        s1 = base - nor(red(n, c, r1)[0]); sz = base - nor(red(n, c, rz)[0])
        res[v] = dict(deg=len(N[v]), ch=ch[v], g0=ch[v] >= len(N[v]), s1=s1, sz=sz, need=eN(N[v]),
                      g1=s1 >= eN(N[v]), gz=sz >= eN(N[v]))
    return res, base
def parse(s):
    c = []
    for t in s.split():
        i, rest = t.split('=')
        o = '&' if '&' in rest else '|'
        j, k = rest.split(o); c.append((int(i), o, int(j), int(k)))
    return c
if __name__ == '__main__':
    PK = '/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/lemD/data.pkl'
    D = pickle.load(open(PK, 'rb'))
    st = collections.Counter(); ex = {}
    for d in D:
        res, base = analyse(d['n'], d['E'], d['c'])
        a0 = any(r['g0'] for r in res.values()); a1 = any(r['g1'] for r in res.values())
        az = any(r['gz'] for r in res.values())
        a01 = any(r['g0'] or r['g1'] for r in res.values())
        V2 = [v for v, r in res.items() if r['deg'] == 2]
        v2_0 = any(res[v]['g0'] for v in V2); v2_01 = any(res[v]['g0'] or res[v]['g1'] for v in V2)
        st['n'] += 1; st['any0'] += a0; st['any1'] += a1; st['anyZ'] += az; st['any01'] += a01
        st['V2_0'] += v2_0; st['V2_01'] += v2_01
        allv1 = all(r['g1'] for r in res.values()); st['all1'] += allv1
        st['s1>sz'] += any(r['s1'] > r['sz'] for r in res.values()); st['s1<sz'] += any(r['s1'] < r['sz'] for r in res.values())
        mind = min(r['deg'] for r in res.values())
        st['mindeg1'] += any(r['g1'] for r in res.values() if r['deg'] == mind)
        if not a1 and 'no1' not in ex: ex['no1'] = (d['E'], d['c'], res)
        if not v2_01 and V2 and 'noV2' not in ex: ex['noV2'] = (d['E'], d['c'], res)
    print(dict(st))
    for k, v in ex.items(): print(k, v[0], ' '.join('%d=%d%s%d' % (i, j, o, kk) for i, o, j, kk in v[1])); print('  ', v[2])
