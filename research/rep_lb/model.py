"""Exact-semantics Python mirror of the Lean definitions and of the live-set search engine.

Lean side (PEqualNP.CircuitLowerBounds / Represents / MetaComplexityLgpMono):
  GateOp.eval and = all, or = any;  wires = inputs ++ one value per gate (missing wire reads false);
  eval = wires.getD output false;  size = number of gates;
  Monotone2 C : every gate op is and/or and has at most 2 inputs;
  Represents A C : forall u v, C.eval (oneEach u v) = A u v   (oneEach = unit vector of u ++ unit vector of v).
"""
from functools import lru_cache

# ---------------------------------------------------------------- circuits
def one_each(n, m, u, v):
    return [i == u for i in range(n)] + [j == v for j in range(m)]

def circ_eval(gates, output, x):
    w = list(x)
    for op, ins in gates:
        vals = [(w[i] if i < len(w) else False) for i in ins]
        w.append(all(vals) if op == 'and' else any(vals))
    return w[output] if output < len(w) else False

def mono2(gates):
    return all(op in ('and', 'or') and len(ins) <= 2 for op, ins in gates)

def mask_fn(n, m, mask):
    return lambda u, v: bool((mask >> (m * u + v)) & 1)

def represents(n, m, mask, gates, output):
    A = mask_fn(n, m, mask)
    return all(circ_eval(gates, output, one_each(n, m, u, v)) == A(u, v)
               for u in range(n) for v in range(m))

def rep_size_at_most(n, m, mask, gates, output, s):
    return mono2(gates) and len(gates) <= s and represents(n, m, mask, gates, output)

# ---------------------------------------------------------------- samples / words
class Inst:
    def __init__(self, n, m, mask):
        self.n, self.m, self.mask = n, m, mask
        A = mask_fn(n, m, mask)
        cells = [(u, v) for u in range(n) for v in range(m)]
        self.pos = [c for c in cells if A(*c)]       # row major, same as the accepted files
        self.neg = [c for c in cells if not A(*c)]
        self.P = len(self.pos) * len(self.neg)
        self.nw = n + m
        P = self.P
        self.full = (1 << P) - 1
        self.W = 2 * P
        # bit k < P : negative sample neg[k % |neg|];  bit P + i : positive sample pos[i // |neg|]
        def samp(k):
            if k < P:
                return self.neg[k % len(self.neg)]
            return self.pos[(k - P) // len(self.neg)]
        self.samp = samp
        inputs = []
        for j in range(self.nw):
            x = 0
            for k in range(self.W):
                u, v = samp(k)
                bit = (u == j) if j < n else (v == j - n)
                if bit:
                    x |= 1 << k
            inputs.append(x)
        self.inputs = inputs
        self.goal = self.full << P            # ones on the positive half, zeros on the negative half
    def sep(self, x):
        return ((x >> self.P) & ~x) & self.full
    def cuts(self, ws):
        r = 0
        for w in ws:
            r |= self.sep(w)
        return r

# ---------------------------------------------------------------- the search (mirror of optC / dispatch)
class Search:
    """optimized k extra ws, memoised on (k, sorted multiset).  The result depends on the multiset only."""
    def __init__(self, inst):
        self.I = inst
        self.memo = {}
        self.sepc = {}
        self.nodes = 0
        self.path = {}
    def sep(self, x):
        s = self.sepc.get(x)
        if s is None:
            s = self.I.sep(x)
            self.sepc[x] = s
        return s
    def children(self, st, extra):
        """All next states of dispatch over all pairs, as (state tuple sorted) with full cuts,
        plus the gate used (for witness extraction)."""
        I = self.I
        full = I.full
        out = []
        L = len(st)
        for i in range(L):
            a = st[i]
            sa = self.sep(a)
            for j in range(i + 1, L):
                b = st[j]
                sb = self.sep(b)
                r = st[:i] + st[i + 1:j] + st[j + 1:]
                base = 0
                for x in r:
                    base |= self.sep(x)
                for opn, w in (('and', a & b), ('or', a | b)):
                    v = self.sep(w) | base
                    if v == full:
                        out.append((tuple(sorted((w,) + r)), (opn, a, b)))
                    if extra != 0:
                        if v | sa == full:
                            out.append((tuple(sorted((w, a) + r)), (opn, a, b)))
                        if v | sb == full:
                            out.append((tuple(sorted((w, b) + r)), (opn, a, b)))
                    if extra >= 2 and (v | sa | sb) == full:
                        out.append((tuple(sorted((w, a, b) + r)), (opn, a, b)))
        return out
    def solve(self, k, st):
        key = (k, st)
        r = self.memo.get(key)
        if r is not None:
            return r
        self.nodes += 1
        g = self.I.goal
        if st == (g,):
            self.memo[key] = True
            return True
        if k == 0:
            self.memo[key] = False
            return False
        extra = k + 1 - len(st)
        if extra < 0:
            extra = 0
        res = False
        for ch, gate in self.children(st, extra):
            if self.solve(k - 1, ch):
                self.path[key] = (ch, gate)
                res = True
                break
        self.memo[key] = res
        return res

def unfolded_cost(S, k, st, cache):
    """Number of optimized-calls Lean makes without any table (dead states: all children are visited)."""
    key = (k, st)
    c = cache.get(key)
    if c is not None:
        return c
    g = S.I.goal
    if st == (g,) or k == 0:
        c = 1
    else:
        extra = max(k + 1 - len(st), 0)
        c = 1
        for ch, _ in S.children(st, extra):
            c += unfolded_cost(S, k - 1, ch, cache)
    cache[key] = c
    return c
