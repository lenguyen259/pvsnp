"""lib612: shared semantics for the L-meta-612 ledger (graphs, circuits, restrictions, counts).

Conventions (as in argument.md, t2.md, deg3.md):
* A graph is (n, edges) with vertices 0..n-1; edges are sorted pairs (u, v), u < v.
* A circuit is Circ(n, gates, out): gates[k] = (op, a, b) with op in {'&', '|'} is node n + k,
  and a, b are earlier nodes (inputs 0..n-1 or gates). out is the output node (default: last gate).
* Truth tables are Python ints over the 2^n rows; row r is the input with x_i = bit i of r.
* red(C, fix) = functional reduction of C under the partial assignment fix (dict var -> 0/1):
  constant gates and gates equal (as functions) to an earlier node are removed, then dead gates.
  This is the `red` of deg3.md / t2.md section 0.
* ruleR(C, fix) = syntactic reduction (argument.md rule R): AND(0,.), OR(1,.) -> constant;
  AND(1,y), OR(0,y), op(y,y) -> copy of y; then dead gates removed.
"""
import itertools, json, re, hashlib
from functools import lru_cache

# ---------------------------------------------------------------- truth tables
_VT = {}


def var_tts(n):
    """Truth tables of x_0..x_{n-1} over 2^n rows, and the all-ones mask."""
    if n in _VT:
        return _VT[n]
    R = 1 << n
    full = (1 << R) - 1
    vs = []
    for i in range(n):
        blk = ((1 << (1 << i)) - 1) << (1 << i)       # one block of size 2^(i+1)
        period = 1 << (i + 1)
        t = blk
        width = period
        while width < R:                                # doubling replication
            t |= t << width
            width *= 2
        vs.append(t & full)
    _VT[n] = (vs, full)
    return _VT[n]


def fG_tt(n, edges):
    vs, full = var_tts(n)
    t = 0
    for u, v in edges:
        t |= vs[u] & vs[v]
    return t


def bit(tt, row):
    return (tt >> row) & 1


# ---------------------------------------------------------------- graphs
def norm_edges(edges):
    return sorted({(min(a, b), max(a, b)) for a, b in edges if a != b})


def adj(n, edges):
    A = [set() for _ in range(n)]
    for u, v in edges:
        A[u].add(v)
        A[v].add(u)
    return A


@lru_cache(maxsize=None)
def tau_key(n, ekey):
    """Vertex cover number by branching on a max-degree vertex (n <= ~20)."""
    edges = list(ekey)
    if not edges:
        return 0
    best = [len({x for e in edges for x in e})]

    def rec(E, k):
        if k >= best[0]:
            return
        if not E:
            best[0] = k
            return
        deg = {}
        for u, v in E:
            deg[u] = deg.get(u, 0) + 1
            deg[v] = deg.get(v, 0) + 1
        w = max(deg, key=deg.get)
        if deg[w] == 1:  # matching remains: need one per edge
            best[0] = min(best[0], k + len(E))
            return
        # branch: w in cover, or N(w) in cover
        rec([e for e in E if w not in e], k + 1)
        N = {u if v == w else v for u, v in E if w in (u, v)}
        rec([e for e in E if e[0] not in N and e[1] not in N], k + len(N))

    rec(edges, 0)
    return best[0]


def tau(n, edges):
    return tau_key(n, tuple(norm_edges(edges)))


def phi(n, edges):
    edges = norm_edges(edges)
    return len(edges) + tau(n, edges) - 1 if edges else 0


def delete(edges, X):
    X = set(X)
    return [(u, v) for u, v in edges if u not in X and v not in X]


def is_c4free(n, edges):
    A = adj(n, edges)
    for u in range(n):
        for w in range(u + 1, n):
            if len(A[u] & A[w]) >= 2:
                return False
    return True


def girth(n, edges):
    A = adj(n, edges)
    best = None
    for s in range(n):
        dist = {s: 0}
        par = {s: -1}
        q = [s]
        for x in q:
            for y in A[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1
                    par[y] = x
                    q.append(y)
                elif par[x] != y:
                    c = dist[x] + dist[y] + 1
                    if best is None or c < best:
                        best = c
    return best  # None = forest


def is_pseudoforest(n, edges):
    """Every component has at most as many edges as vertices."""
    A = adj(n, edges)
    seen = [False] * n
    for s in range(n):
        if seen[s] or not A[s]:
            continue
        comp = [s]
        seen[s] = True
        for x in comp:
            for y in A[x]:
                if not seen[y]:
                    seen[y] = True
                    comp.append(y)
        ne = sum(len(A[x]) for x in comp) // 2
        if ne > len(comp):
            return False
    return True


def components(n, edges):
    A = adj(n, edges)
    seen = [False] * n
    out = []
    for s in range(n):
        if seen[s] or not A[s]:
            continue
        comp = [s]
        seen[s] = True
        for x in comp:
            for y in A[x]:
                if not seen[y]:
                    seen[y] = True
                    comp.append(y)
        out.append(sorted(comp))
    return out


def graph_class(n, edges):
    edges = norm_edges(edges)
    A = adj(n, edges)
    degs = [len(a) for a in A]
    nz = [d for d in degs if d > 0]
    g = girth(n, edges)
    comps = components(n, edges)
    cubic_comp = any(all(degs[x] == 3 for x in c) for c in comps)
    return {
        "c4free": is_c4free(n, edges),
        "maxdeg": max(degs) if degs else 0,
        "mindeg": min(nz) if nz else 0,
        "subcubic": (max(degs) if degs else 0) <= 3,
        "pseudoforest": is_pseudoforest(n, edges),
        "forest": g is None,
        "girth": g,
        "triangle_free": g is None or g >= 4,
        "n_hubs": sum(1 for d in degs if d >= 3),
        "n_comp": len(comps),
        "has_cubic_component": cubic_comp,
        "isolated": sum(1 for d in degs if d == 0),
    }


def is_star(edges):
    edges = norm_edges(edges)
    if not edges:
        return False
    common = set(edges[0])
    for e in edges[1:]:
        common &= set(e)
    return len(common) >= 1


def gkey(n, edges):
    return "%d:" % n + ",".join("%d-%d" % e for e in norm_edges(edges))


# ---------------------------------------------------------------- circuits
class Circ:
    __slots__ = ("n", "gates", "out")

    def __init__(self, n, gates, out=None):
        self.n = n
        self.gates = [(op, int(a), int(b)) for op, a, b in gates]
        self.out = (n + len(self.gates) - 1) if out is None else int(out)

    @property
    def size(self):
        return len(self.gates)

    def n_and(self):
        return sum(1 for g in self.gates if g[0] == '&')

    def n_or(self):
        return sum(1 for g in self.gates if g[0] == '|')

    def tts(self, fix=None):
        vs, full = var_tts(self.n)
        T = list(vs)
        if fix:
            for v, b in fix.items():
                T[v] = full if b else 0
        for op, a, b in self.gates:
            T.append(T[a] & T[b] if op == '&' else T[a] | T[b])
        return T

    def out_tt(self, fix=None):
        return self.tts(fix)[self.out]

    def readers(self):
        R = [[] for _ in range(self.n + len(self.gates))]
        for k, (op, a, b) in enumerate(self.gates):
            g = self.n + k
            R[a].append(g)
            if b != a:
                R[b].append(g)
        return R

    def to_str(self):
        return " ".join("%d=%d%s%d" % (self.n + k, a, op, b) for k, (op, a, b) in enumerate(self.gates)) + \
            ("" if self.out == self.n + len(self.gates) - 1 else " out=%d" % self.out)

    def to_json(self):
        return [[op, a, b] for op, a, b in self.gates]

    def live(self):
        """set of gate nodes reaching the output"""
        L = set()
        if self.out < self.n:
            return L
        st = [self.out]
        while st:
            x = st.pop()
            if x < self.n or x in L:
                continue
            L.add(x)
            op, a, b = self.gates[x - self.n]
            st += [a, b]
        return L


def parse_str(s):
    """Parse '6=0|5 7=1&4 ...' (also accepts 'x1' and '|'/'&' with spaces removed). Returns Circ.
    Gate numbers need not be consecutive; n = first gate number."""
    s = s.replace('x', '')
    toks = re.findall(r'(\d+)\s*=\s*(\d+)\s*([|&])\s*(\d+)', s)
    if not toks:
        raise ValueError("no gates")
    return from_indexed([(int(k), op, int(a), int(b)) for k, a, op, b in toks])


def from_indexed(lst, n=None):
    """lst = [(idx, op, a, b)] in topological order. n = number of inputs (default min idx)."""
    lst = [(int(i), op, int(a), int(b)) for i, op, a, b in lst]
    if n is None:
        n = min(i for i, _, _, _ in lst)
    m = {j: j for j in range(n)}
    gates = []
    for i, op, a, b in lst:
        if a not in m or b not in m:
            raise ValueError("forward reference at gate %d" % i)
        op = {'AND': '&', 'OR': '|', 'and': '&', 'or': '|'}.get(op, op)
        if op not in '&|':
            raise ValueError("bad op %r" % op)
        gates.append((op, m[a], m[b]))
        m[i] = n + len(gates) - 1
    return Circ(n, gates)


def graph_of_circuit(C):
    """If C computes f_G for a graph G on C.n vertices, return the edge list, else None."""
    T = C.tts()
    t = T[C.out]
    n = C.n
    for u in range(n):
        if bit(t, 1 << u):
            return None
    if bit(t, 0):
        return None
    E = [(u, v) for u in range(n) for v in range(u + 1, n) if bit(t, (1 << u) | (1 << v))]
    if fG_tt(n, E) != t:
        return None
    return E


def red(C, fix=None):
    """Functional reduction under fix. Returns a new Circ (possibly with 0 gates; then out is an input
    node or the constant marker: out = -1 for constant 0, -2 for constant 1)."""
    vs, full = var_tts(C.n)
    T = C.tts(fix)
    rep = {}
    newid = {}
    for v in range(C.n):
        t = T[v]
        if t != 0 and t != full and t not in rep:
            rep[t] = v
            newid[v] = v
    gates = []
    for k, (op, a, b) in enumerate(C.gates):
        g = C.n + k
        t = T[g]
        if t == 0 or t == full or t in rep:
            continue
        na, nb = newid[rep[T[a]]], newid[rep[T[b]]]
        gates.append((op, na, nb, g))
        rep[t] = g
        newid[g] = C.n + len(gates) - 1
    to = T[C.out]
    if to == 0:
        return Circ(C.n, [], -1)
    if to == full:
        return Circ(C.n, [], -2)
    o = newid[rep[to]]
    # dead removal
    if o < C.n:
        return Circ(C.n, [], o)
    live = set()
    st = [o]
    while st:
        x = st.pop()
        if x < C.n or x in live:
            continue
        live.add(x)
        op, a, b, _ = gates[x - C.n]
        st += [a, b]
    m = {j: j for j in range(C.n)}
    out = []
    for k, (op, a, b, _) in enumerate(gates):
        x = C.n + k
        if x in live:
            out.append((op, m[a], m[b]))
            m[x] = C.n + len(out) - 1
    return Circ(C.n, out, m[o])


def ruleR_survivors(C, fix):
    """Syntactic rule R. Returns (set of surviving original gate nodes, alias of output)."""
    st = {}   # node -> ('c', b) or ('n', node)
    for v in range(C.n):
        st[v] = ('c', fix[v]) if fix and v in fix else ('n', v)
    kept = {}
    for k, (op, a, b) in enumerate(C.gates):
        g = C.n + k
        sa, sb = st[a], st[b]
        if op == '&':
            if sa == ('c', 0) or sb == ('c', 0):
                s = ('c', 0)
            elif sa == ('c', 1):
                s = sb
            elif sb == ('c', 1):
                s = sa
            elif sa == sb:
                s = sa
            else:
                s = ('n', g)
                kept[g] = (sa[1], sb[1])
        else:
            if sa == ('c', 1) or sb == ('c', 1):
                s = ('c', 1)
            elif sa == ('c', 0):
                s = sb
            elif sb == ('c', 0):
                s = sa
            elif sa == sb:
                s = sa
            else:
                s = ('n', g)
                kept[g] = (sa[1], sb[1])
        st[g] = s
    so = st[C.out]
    if so[0] == 'c':
        return set(), so
    live = set()
    stk = [so[1]]
    while stk:
        x = stk.pop()
        if x < C.n or x in live:
            continue
        live.add(x)
        stk += list(kept[x])
    return live, so


def ruleR_size(C, fix):
    return len(ruleR_survivors(C, fix)[0])


def LD(C, fix):
    """t8 LD(rho) = |K u Cp u Dead| for a 0-option (fix all 0) or a 1-option (fix all 1)."""
    n = C.n
    val = set(fix.values())
    assert len(val) == 1
    b0 = val.pop()
    K = set()
    const = {v for v in fix}
    for k, (op, a, b) in enumerate(C.gates):
        g = n + k
        ca, cb = (a in const), (b in const)
        if b0 == 0:
            c = (ca or cb) if op == '&' else (ca and cb)
        else:
            c = (ca or cb) if op == '|' else (ca and cb)
        if c:
            K.add(g)
            const.add(g)
    Cp = {n + k for k, (op, a, b) in enumerate(C.gates) if (n + k) not in K and (a in const or b in const)}
    R = C.readers()
    Z = set()
    for k in range(len(C.gates) - 1, -1, -1):
        g = n + k
        if g in K:
            Z.add(g)
        elif g != C.out and R[g] and all(r in Z for r in R[g]):
            Z.add(g)
    return len(K | Cp | Z)


def LR(C, fix):
    """t7 LR(rho) = size - |ruleR(C|rho)| + (#Top gates among rule-R survivors - 1)."""
    surv, so = ruleR_survivors(C, fix)
    if so[0] == 'c':
        return C.size
    T = C.tts(fix)
    to = T[C.out]
    top = sum(1 for g in surv if T[g] == to)
    return C.size - len(surv) + max(0, top - 1)


# ---------------------------------------------------------------- structure
def sing(T, n, node):
    t = T[node]
    return frozenset(u for u in range(n) if bit(t, 1 << u))


def and_ancestors(C):
    """has_and[node] = node has an AND gate in its cone (excluding itself)."""
    h = [False] * (C.n + C.size)
    for k, (op, a, b) in enumerate(C.gates):
        g = C.n + k
        h[g] = h[a] or h[b] or (a >= C.n and C.gates[a - C.n][0] == '&') or \
            (b >= C.n and C.gates[b - C.n][0] == '&')
    return h


def minimal_ands(C):
    h = and_ancestors(C)
    return [C.n + k for k, (op, a, b) in enumerate(C.gates) if op == '&' and not h[C.n + k]]


def star_all_violations(C, edges):
    """Return (j1, j2, j3): numbers of AND gates violating N1, N2, N3 (girth5.md), on the live part."""
    T = C.tts()
    E = set(norm_edges(edges))
    L = C.live()
    j1 = j2 = j3 = 0
    for k, (op, a, b) in enumerate(C.gates):
        g = C.n + k
        if op != '&' or g not in L:
            continue
        S1, S2 = sing(T, C.n, a), sing(T, C.n, b)
        if S1 & S2:
            j1 += 1
        if not S1 or not S2:
            j2 += 1
        if any(u != v and (min(u, v), max(u, v)) not in E for u in S1 for v in S2):
            j3 += 1
    return j1, j2, j3


def is_star_all(C, edges):
    return star_all_violations(C, edges) == (0, 0, 0)


def is_clean(C, edges):
    """No node p and non-edge uv with p(e_u+e_v)=1, p(e_u)=p(e_v)=0."""
    T = C.tts()
    E = set(norm_edges(edges))
    n = C.n
    for t in T[n:]:
        for u in range(n):
            if bit(t, 1 << u):
                continue
            for v in range(u + 1, n):
                if (u, v) not in E and not bit(t, 1 << v) and bit(t, (1 << u) | (1 << v)):
                    return False
    return True


def ch(C, v):
    """number of OR gates with an input q <= x_v (or.md)."""
    T = C.tts()
    xv = T[v]
    dom = [(t & ~xv) == 0 and t != 0 for t in T]
    return sum(1 for (op, a, b) in C.gates if op == '|' and (dom[a] or dom[b]))


# ---------------------------------------------------------------- the graph-side bookkeeping
class GraphCtx:
    """Cached graph quantities for one graph."""

    def __init__(self, n, edges):
        self.n = n
        self.E = norm_edges(edges)
        self.A = adj(n, self.E)
        self.deg = [len(a) for a in self.A]
        self.tau = tau(n, self.E)
        self.phi = phi(n, self.E)
        self.V = [v for v in range(n) if self.deg[v] > 0]

    def phi_minus(self, X):
        return phi(self.n, delete(self.E, X))

    def has_edge_minus(self, X):
        return bool(delete(self.E, X))

    def need_A(self, v):
        """None if G - v is edgeless (option not allowed)."""
        return self.phi - self.phi_minus([v]) if self.has_edge_minus([v]) else None

    def N(self, v):
        return sorted(self.A[v] | {v})

    def need_N(self, v):
        X = self.N(v)
        return self.phi - self.phi_minus(X) if self.has_edge_minus(X) else None

    def need_B(self, v):
        X = self.N(v)
        if self.has_edge_minus(X):
            p1 = self.deg[v] + self.phi_minus(X)
        else:
            p1 = self.deg[v] - 1
        return self.phi - p1

    def need_OR(self, X):
        X = set(X)
        e = sum(1 for (u, w) in self.E if u in X or w in X)
        return e - (0 if self.has_edge_minus(X) else 1)

    def need_AND(self, X):
        return self.tau - tau(self.n, delete(self.E, X))


def elim(C, fix):
    """size(C) - size(red(C|fix)); C should already be reduced."""
    return C.size - red(C, fix).size


def counts_after(C, fix):
    R = red(C, fix)
    return R.size, R.n_and(), R.n_or()


# ---------------------------------------------------------------- store
def circuit_key(C, edges):
    """Dedup key: graph + multiset of (op, tt(in1), tt(in2)) over live gates (gate order ignored)."""
    T = C.tts()
    L = C.live()
    items = []
    for k, (op, a, b) in enumerate(C.gates):
        g = C.n + k
        if g not in L:
            continue
        ta, tb = T[a], T[b]
        if ta > tb:
            ta, tb = tb, ta
        items.append("%s:%x:%x" % (op, ta, tb))
    items.sort()
    h = hashlib.sha1((gkey(C.n, edges) + "|" + ";".join(items) + "|%d" % len(C.gates)).encode()).hexdigest()
    return h[:20]


def load_store(paths, filt=None):
    import gzip
    for p in paths:
        op = gzip.open if p.endswith('.gz') else open
        with op(p, 'rt') as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                if filt and not filt(r):
                    continue
                yield r


def rec_circ(r):
    return Circ(r["n"], r["gates"], r["out"])
