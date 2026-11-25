"""falsify.py: run candidate claims about (graph, circuit) against the L-meta-612 circuit store.

A claim is a Python function  pred(x) -> float | None  on a context object x (see class Ctx):
  * None       : the instance is outside the claim's scope;
  * value >= 0 : the claim holds on this instance (the value is the slack / margin);
  * value < 0  : VIOLATION.
Margins let the fresh-circuit search hill-climb towards violations.

Examples
  python3 -I falsify.py --list
  python3 -I falsify.py --claim T2 --claim or_E1                    # core store
  python3 -I falsify.py --claim T2 --filter subcubic --bulk         # + bulk pool
  python3 -I falsify.py --claim T2 --fresh petersen:60 --fresh n8:30  # + adversarial fresh circuits
  python3 -I falsify.py --pred-file my.py --claim mine              # my.py defines CLAIMS = {name: (fn, doc)}
  python3 -I falsify.py --claim T2 --closure                        # also all red(C|x_X:=0), X = {v}, N[v]
  python3 -I falsify.py --sanity                                     # every built-in claim, report json
  python3 -I falsify.py --stats                                      # composition of the store

Light CPU: one process; please run under `nice`. The core store has ~96k circuits; a full --sanity
pass takes a few minutes.
"""
import sys, os, json, time, random, argparse, importlib.util, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib612 import *

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.join(HERE, "circuits.jsonl")
BULK = os.path.join(HERE, "circuits_bulk.jsonl.gz")

_GC = {}


def gctx(n, edges):
    k = gkey(n, edges)
    if k not in _GC:
        if len(_GC) > 5000:
            _GC.clear()
        _GC[k] = GraphCtx(n, edges)
    return _GC[k]


class Ctx:
    """Everything a claim may want, computed lazily. R = red(C) (functional reduction, deg3/t2 sense).
    Option results are computed on R."""

    def __init__(self, C, edges, rec=None):
        self.C = C
        self.rec = rec or {}
        self.G = gctx(C.n, edges)
        self._R = None
        self._cache = {}

    # -- circuits
    @property
    def R(self):
        if self._R is None:
            self._R = red(self.C)
        return self._R

    def size(self):
        return self.R.size

    def n_and(self):
        return self.R.n_and()

    def n_or(self):
        return self.R.n_or()

    def _red_fix(self, fix):
        k = tuple(sorted(fix.items()))
        if k not in self._cache:
            S = red(self.R, fix)
            self._cache[k] = (S.size, S.n_and(), S.n_or())
        return self._cache[k]

    # -- eliminations (functional reduction)
    def tot(self, X):
        return self.R.size - self._red_fix({v: 0 for v in X})[0]

    def sav(self, X):
        return self.R.n_or() - self._red_fix({v: 0 for v in X})[2]

    def sa(self, X):
        return self.R.n_and() - self._red_fix({v: 0 for v in X})[1]

    def elim1(self, v):
        return self.R.size - self._red_fix({v: 1})[0]

    def ch(self, v):
        return ch(self.R, v)

    # -- the A / N / B options of t2.md (None if not allowed)
    def opt_A(self, v):
        nd = self.G.need_A(v)
        return None if nd is None else self.tot([v]) - nd

    def opt_N(self, v):
        nd = self.G.need_N(v)
        return None if nd is None else self.tot(self.G.N(v)) - nd

    def opt_B(self, v):
        return self.elim1(v) - self.G.need_B(v)

    def minimal_and_support(self):
        T = self.R.tts()
        S = set()
        for g in minimal_ands(self.R):
            op, a, b = self.R.gates[g - self.R.n]
            S |= sing(T, self.R.n, a) | sing(T, self.R.n, b)
        return S

    def violations(self):
        if "viol" not in self._cache:
            self._cache["viol"] = star_all_violations(self.R, self.G.E)
        return self._cache["viol"]


def best(vals):
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else None


# ============================================================== built-in claims
def c_main(x):
    """L-meta-612 itself: size(red C) >= Phi(G)."""
    if not x.G.E:
        return None
    return x.size() - x.G.phi


def c_and_tau(x):
    """(AND) #AND(red C) >= tau(G), any C4-free G."""
    if not x.G.E:
        return None
    return x.n_and() - x.G.tau


def c_or_E1(x):
    """(OR) #OR(red C) >= |E| - 1, any C4-free G."""
    if not x.G.E:
        return None
    return x.n_or() - (len(x.G.E) - 1)


def c_pf(x):
    """Theorem PF (LEAN): on pseudoforests #AND >= tau and #OR >= |E|-1 (margin = min of both)."""
    if not x.G.E or not is_pseudoforest(x.G.n, x.G.E):
        return None
    return min(x.n_and() - x.G.tau, x.n_or() - (len(x.G.E) - 1))


def c_thmF(x):
    """Theorem F + R-OR (lemD.md): #OR >= |E|-1 if at most one vertex has degree >= 3."""
    if not x.G.E or sum(1 for d in x.G.deg if d >= 3) > 1:
        return None
    return x.n_or() - (len(x.G.E) - 1)


def c_thmS(x):
    """Theorem S (girth5.md): STAR-ALL circuits have size >= Phi."""
    if not x.G.E or x.violations() != (0, 0, 0):
        return None
    return x.size() - x.G.phi


def c_thmS2(x):
    """Theorem S2 (nf.md): circuits satisfying N1 and N3 have size >= Phi."""
    if not x.G.E:
        return None
    j1, j2, j3 = x.violations()
    if j1 or j3:
        return None
    return x.size() - x.G.phi


def c_lemmaA(x):
    """Lemma A (nf.md): clean circuits have #AND >= tau."""
    if not x.G.E or not is_clean(x.R, x.G.E):
        return None
    return x.n_and() - x.G.tau


def _mindeg2(x):
    return x.G.E and all(x.G.deg[v] >= 2 for v in x.G.V)


def c_lemD_ch(x):
    """Lemma D (or.md): min degree >= 2 => some v has ch(v) >= deg v."""
    if not _mindeg2(x):
        return None
    return max(x.ch(v) - x.G.deg[v] for v in x.G.V)


def c_lemD_sav(x):
    """R-OR with single vertices / sav-Lemma D (deg3.md 5.2): min degree >= 2 => some v has
    sav(v) >= need_OR(v) = deg v - [G - v edgeless]."""
    if not _mindeg2(x):
        return None
    return max(x.sav([v]) - x.G.need_OR([v]) for v in x.G.V)


def c_Dmin(x):
    """(Dmin) core.md: min degree >= 2 => some minimum-degree vertex has sav(v) >= deg v."""
    if not _mindeg2(x):
        return None
    d = min(x.G.deg[v] for v in x.G.V)
    return max(x.sav([v]) - x.G.need_OR([v]) for v in x.G.V if x.G.deg[v] == d)


def c_Mprime(x):
    """M0 / Lemma M' (or.md, deg3.md): some v has sa(v) >= tau(G) - tau(G - v)."""
    if not x.G.E:
        return None
    return max(x.sa([v]) - x.G.need_AND([v]) for v in x.G.V)


def c_T2A(x):
    """One-vertex direct induction (deg3.md R-TOT single v): G not a star => some v with G - v not
    edgeless has tot(v) >= Phi(G) - Phi(G - v)."""
    if not x.G.E or is_star(x.G.E):
        return None
    return best(x.opt_A(v) for v in x.G.V)


def c_T2(x):
    """Lemma T2 (deg3.md 7): G subcubic, not a star => some v has tot(v) >= Phi(G)-Phi(G-v) (G-v with an
    edge) or tot(N[v]) >= Phi(G)-Phi(G-N[v]) (G-N[v] with an edge). Evaluated on every C4-free graph;
    use --filter subcubic for the literal scope."""
    if not x.G.E or is_star(x.G.E):
        return None
    return best([x.opt_A(v) for v in x.G.V] + [x.opt_N(v) for v in x.G.V])


def c_T2F(x):
    """T2F (t2.md): G not a star => some A(v), N(v) or B(v) option is good."""
    if not x.G.E or is_star(x.G.E):
        return None
    return best([x.opt_A(v) for v in x.G.V] + [x.opt_N(v) for v in x.G.V] + [x.opt_B(v) for v in x.G.V])


def c_mANB(x):
    """mANB (t2.md 5): G not a star => some v in the support of a minimal AND gate has a good A, N or B
    option."""
    if not x.G.E or is_star(x.G.E):
        return None
    S = x.minimal_and_support()
    return best([x.opt_A(v) for v in S] + [x.opt_N(v) for v in S] + [x.opt_B(v) for v in S])


def c_mAB(x):
    """mAB = Lemma E*+ (t2.md 2.1, estar/proof.md 5): some v in the support of a minimal AND gate has a
    good A or B option (functional reduction)."""
    if not x.G.E or is_star(x.G.E):
        return None
    S = x.minimal_and_support()
    return best([x.opt_A(v) for v in S] + [x.opt_B(v) for v in S])


def c_Estar(x):
    """Lemma E* (argument.md 4): some minimal AND gate, v in its support and b with rule-R (syntactic)
    elimination >= Phi(G) - Phi(G_b). Evaluated on red C (no constant/copy gates)."""
    if not x.G.E or is_star(x.G.E):
        return None
    S = x.minimal_and_support()
    R = x.R
    vals = []
    for v in S:
        nd = x.G.need_A(v)
        if nd is not None:
            vals.append(R.size - ruleR_size(R, {v: 0}) - nd)
        vals.append(R.size - ruleR_size(R, {v: 1}) - x.G.need_B(v))
    return best(vals)


def _opts_struct(x, fn):
    vals = []
    for v in x.G.V:
        nd = x.G.need_A(v)
        if nd is not None:
            vals.append(fn(x.R, {v: 0}) - nd)
        X = x.G.N(v)
        nd = x.G.need_N(v)
        if nd is not None:
            vals.append(fn(x.R, {w: 0 for w in X}) - nd)
        vals.append(fn(x.R, {v: 1}) - x.G.need_B(v))
    return best(vals)


def c_T2LD(x):
    """T2-LD (t8.md): some A/N/B option is paid by syntactic constants, copies and dead gates (LD)."""
    if not x.G.E or is_star(x.G.E):
        return None
    return _opts_struct(x, LD)


def c_T2LR(x):
    """T2-LR (t7.md 3): some A/N/B option is paid by rule R plus the Top merge (LR)."""
    if not x.G.E or is_star(x.G.E):
        return None
    return _opts_struct(x, LR)


def c_NF5(x):
    """(NF5) girth5.md: girth >= 5 and size <= Phi => STAR-ALL (margin 0 = holds, -1 = violation)."""
    g = girth(x.G.n, x.G.E)
    if not x.G.E or (g is not None and g < 5) or x.size() > x.G.phi:
        return None
    return 0 if x.violations() == (0, 0, 0) else -1


def c_J5(x):
    """J5 (t2.md 4): triangle-free => size >= Phi + j3 (j3 = #AND gates with a junk pair)."""
    g = girth(x.G.n, x.G.E)
    if not x.G.E or (g is not None and g < 4):
        return None
    return x.size() - x.G.phi - x.violations()[2]


CLAIMS = {
    # name: (fn, expected-on-store, ledger id)
    "main": (c_main, "survive", "MAIN"),
    "and_tau": (c_and_tau, "survive", "AND-split"),
    "or_E1": (c_or_E1, "refuted", "OR-split"),
    "PF": (c_pf, "survive", "THM-PF"),
    "thmF": (c_thmF, "survive", "THM-F"),
    "thmS": (c_thmS, "survive", "THM-S"),
    "thmS2": (c_thmS2, "survive", "THM-S2"),
    "lemmaA": (c_lemmaA, "survive", "LEM-A"),
    "lemD_ch": (c_lemD_ch, "refuted", "LEM-D"),
    "lemD_sav": (c_lemD_sav, "refuted", "LEM-D-sav"),
    "Dmin": (c_Dmin, "refuted", "DMIN"),
    "Mprime": (c_Mprime, "refuted", "LEM-M'"),
    "T2A": (c_T2A, "refuted", "T2-A"),
    "T2": (c_T2, "survive", "T2"),
    "T2F": (c_T2F, "survive", "T2F"),
    "mANB": (c_mANB, "survive", "mANB"),
    "mAB": (c_mAB, "refuted", "E*+"),
    "Estar": (c_Estar, "refuted", "E*"),
    "T2LD": (c_T2LD, "refuted", "T2-LD"),
    "T2LR": (c_T2LR, "survive", "T2-LR"),
    "NF5": (c_NF5, "refuted", "NF5"),
    "J5": (c_J5, "refuted", "J5"),
}


# ============================================================== filters
def make_filter(names):
    def f(r):
        c = r["cls"]
        for nm in names:
            if nm == "subcubic" and not c["subcubic"]:
                return False
            if nm == "girth5" and not (c["girth"] is None or c["girth"] >= 5):
                return False
            if nm == "trianglefree" and not c["triangle_free"]:
                return False
            if nm == "nonpf" and c["pseudoforest"]:
                return False
            if nm == "pf" and not c["pseudoforest"]:
                return False
            if nm == "mindeg2" and c["mindeg"] < 2:
                return False
            if nm.startswith("slack<=") and r["slack"] > int(nm[7:]):
                return False
            if nm.startswith("n>=") and r["n"] < int(nm[3:]):
                return False
            if nm.startswith("n<=") and r["n"] > int(nm[3:]):
                return False
        return True
    return f


# ============================================================== named graphs for fresh search
P10 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (1, 6), (2, 7), (3, 8), (4, 9), (5, 7), (7, 9), (9, 6), (6, 8), (8, 5)]
NAMED = {
    "petersen": (10, P10),
    "petv": (9, [(0, 1), (0, 5), (1, 2), (1, 6), (2, 3), (2, 7), (3, 8), (4, 6), (4, 7), (5, 7), (5, 8), (6, 8)]),
    "n8": (8, [(0, 1), (2, 3), (0, 4), (2, 4), (1, 5), (2, 5), (0, 6), (3, 6), (1, 7), (3, 7)]),
    "net": (6, [(0, 4), (1, 5), (2, 3), (3, 4), (3, 5), (4, 5)]),
    "bull": (5, [(0, 1), (0, 2), (0, 4), (1, 2), (2, 3)]),
    "C5": (5, [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]),
    "C7": (7, [(i, (i + 1) % 7) for i in range(7)]),
    "P6": (6, [(i, i + 1) for i in range(5)]),
    "2tri+bridge": (6, [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5)]),
    "tri+C5": (6, [(0, 2), (0, 5), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5)]),
    "constrS7": (7, [(0, 1), (0, 4), (0, 5), (1, 2), (1, 4), (2, 6), (3, 5), (3, 6), (5, 6)]),
    "theta233": (7, [(0, 2), (2, 1), (0, 3), (3, 4), (4, 1), (0, 5), (5, 6), (6, 1)]),
    "H7": (7, [(0, 1), (0, 5), (1, 6), (2, 4), (4, 6), (6, 3), (3, 5), (5, 2)]),
    "H8a": (8, [(0, 1), (1, 2), (0, 5), (1, 6), (2, 7), (3, 5), (5, 7), (7, 4), (4, 6), (6, 3)]),
    "H8b": (8, [(1, 2), (0, 4), (1, 6), (2, 7), (3, 5), (5, 7), (7, 4), (4, 6), (6, 3)]),
    "sun5": (10, [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)]),
    "C5{012}": (8, [(0, 1), (0, 4), (0, 5), (1, 2), (1, 6), (2, 3), (2, 7), (3, 4)]),
}


def parse_graph(spec):
    if spec in NAMED:
        return NAMED[spec]
    E = [tuple(int(t) for t in e.split("-")) for e in spec.split(",")]
    n = max(max(e) for e in E) + 1
    return n, E


def min_covers(n, edges, t):
    V = sorted({x for e in edges for x in e})
    out = []
    for T in itertools.combinations(V, t):
        s = set(T)
        if all(a in s or b in s for a, b in edges):
            out.append(T)
            if len(out) > 200:
                break
    return out


def star_cover(n, edges, rng):
    G = gctx(n, edges)
    covs = min_covers(n, G.E, G.tau)
    T = set(rng.choice(covs))
    leaves = {t: [] for t in T}
    for a, b in G.E:
        c = [z for z in (a, b) if z in T]
        t = rng.choice(c)
        leaves[t].append(b if t == a else a)
    gates = []

    def tree(nodes):
        nodes = list(nodes)
        rng.shuffle(nodes)
        while len(nodes) > 1:
            a = nodes.pop()
            b = nodes.pop()
            gates.append(('|', a, b))
            nodes.insert(rng.randrange(len(nodes) + 1), n + len(gates) - 1)
        return nodes[0]

    tops = []
    for t, L in leaves.items():
        if not L:
            continue
        y = tree(L)
        gates.append(('&', t, y))
        tops.append(n + len(gates) - 1)
    tree(tops)
    return Circ(n, gates)


def mutate(C, rng):
    n = C.n
    gates = list(C.gates)
    m = len(gates)
    r = rng.random()
    if r < 0.45 or m == 0:              # insert op(q, s) and redirect readers of q to it
        pos = rng.randrange(m + 1)
        q = rng.randrange(n + pos)
        s = rng.randrange(n + pos)
        op = rng.choice('&|')
        newid = n + pos

        def sh(x):
            return x + 1 if x >= newid else x
        ng = [(o, sh(a), sh(b)) for o, a, b in gates]
        ng.insert(pos, (op, q, s))
        for k in range(pos + 1, len(ng)):
            o, a, b = ng[k]
            if a == q and rng.random() < 0.6:
                a = newid
            if b == q and rng.random() < 0.6:
                b = newid
            ng[k] = (o, a, b)
        return Circ(n, ng, sh(C.out) if C.out >= newid else C.out)
    if r < 0.85:                        # rewire one input
        k = rng.randrange(m)
        o, a, b = gates[k]
        new = rng.randrange(n + k)
        gates[k] = (o, new, b) if rng.random() < 0.5 else (o, a, new)
        return Circ(n, gates, C.out)
    k = rng.randrange(m)                # flip an operation
    o, a, b = gates[k]
    gates[k] = ('&' if o == '|' else '|', a, b)
    return Circ(n, gates, C.out)


def fresh(fn, n, edges, seconds, max_slack, seed, report, gname):
    rng = random.Random(seed)
    G = gctx(n, edges)
    target = fG_tt(n, G.E)
    cur = star_cover(n, G.E, rng)
    cur_m = fn(Ctx(cur, G.E))
    t0 = time.time()
    tried = valid = 0
    seen = set()
    while time.time() - t0 < seconds:
        if rng.random() < 0.002:
            cur = star_cover(n, G.E, rng)
            cur_m = fn(Ctx(cur, G.E))
        D = mutate(cur, rng)
        tried += 1
        if D.out_tt() != target:
            continue
        D = red(D)
        if D.size > G.phi + max_slack or D.size == 0:
            continue
        valid += 1
        x = Ctx(D, G.E)
        mval = fn(x)
        k = D.to_str()
        if k not in seen:
            seen.add(k)
            report.see(x, mval, "fresh:%s:seed%d" % (gname, seed))
        # adversarial acceptance: move if margin does not increase (with some noise)
        if mval is None or cur_m is None or mval <= cur_m or rng.random() < 0.05:
            cur, cur_m = D, mval
    return tried, valid, len(seen)


# ============================================================== reporting
class Report:
    def __init__(self, name, keep=5):
        self.name = name
        self.checked = 0
        self.in_scope = 0
        self.viol = 0
        self.min_margin = None
        self.worst = []      # smallest counterexamples
        self.keep = keep

    def see(self, x, m, src):
        self.checked += 1
        if m is None:
            return
        self.in_scope += 1
        if self.min_margin is None or m < self.min_margin:
            self.min_margin = m
        if m < 0:
            self.viol += 1
            key = (x.G.n, len(x.G.E), x.R.size, x.R.to_str())
            if len(self.worst) < self.keep or key < self.worst[-1][0]:
                ent = (key, {"id": x.rec.get("id"), "src": src, "n": x.G.n, "edges": [list(e) for e in x.G.E],
                             "phi": x.G.phi, "size": x.R.size, "slack": x.R.size - x.G.phi,
                             "n_and": x.R.n_and(), "n_or": x.R.n_or(), "margin": m, "circuit": x.R.to_str()})
                if all(w[0] != key for w in self.worst):
                    self.worst.append(ent)
                    self.worst.sort(key=lambda w: w[0])
                    del self.worst[self.keep:]

    def as_dict(self):
        return {"claim": self.name, "checked": self.checked, "in_scope": self.in_scope, "violations": self.viol,
                "min_margin": self.min_margin, "smallest": [w[1] for w in self.worst]}

    def show(self):
        st = "VIOLATED" if self.viol else "survives"
        print("%-10s %-8s in-scope %7d / %7d   violations %6d   min margin %s" %
              (self.name, st, self.in_scope, self.checked, self.viol, self.min_margin))
        for w in self.worst[:3]:
            d = w[1]
            print("    n=%d |E|=%d Phi=%d size=%d (#AND %d, #OR %d) margin %s  [%s]" %
                  (d["n"], len(d["edges"]), d["phi"], d["size"], d["n_and"], d["n_or"], d["margin"], d["id"] or d["src"]))
            print("      E=%s" % ",".join("%d%d" % tuple(e) if max(e) < 10 else "%d-%d" % tuple(e) for e in d["edges"]))
            print("      C=%s" % d["circuit"])


def stats(paths):
    from collections import Counter
    c = Counter()
    graphs = {}
    for r in load_store(paths):
        cl = r["cls"]
        c["total"] += 1
        c["tier:" + r["tier"]] += 1
        c["slack=%s" % (r["slack"] if r["slack"] <= 4 else ">4")] += 1
        if cl["subcubic"]:
            c["subcubic"] += 1
        if cl["subcubic"] and not cl["pseudoforest"]:
            c["subcubic non-pseudoforest"] += 1
        if cl["girth"] is None or cl["girth"] >= 5:
            c["girth>=5 (incl. forests)"] += 1
        if not cl["triangle_free"]:
            c["with triangles"] += 1
        if r["n"] >= 8:
            c["n>=8"] += 1
        if not r["reduced"]:
            c["not reduced as stored"] += 1
        if "md-witness" in r["tags"]:
            c["cited in a .md file"] += 1
        graphs.setdefault(gkey(r["n"], r["edges"]), [r["n"], len(r["edges"]), r["phi"], cl["subcubic"], cl["pseudoforest"], 0])[5] += 1
    for k in sorted(c):
        print("%-30s %d" % (k, c[k]))
    print("distinct labelled graphs:", len(graphs))
    big = sorted(graphs.items(), key=lambda kv: (-kv[1][0], kv[0]))[:25]
    print("largest graphs (n, |E|, Phi, subcubic, pseudoforest, #circuits):")
    for k, v in big:
        print("  ", v, k)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim", action="append", default=[])
    ap.add_argument("--pred-file")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--sanity", action="store_true", help="run every built-in claim; write sanity_report.json")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--bulk", action="store_true", help="include circuits_bulk.jsonl.gz")
    ap.add_argument("--filter", action="append", default=[],
                    help="subcubic | girth5 | trianglefree | pf | nonpf | mindeg2 | slack<=K | n>=K | n<=K")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--closure", action="store_true", help="also test red(C|x_X:=0) for X={v}, N[v]")
    ap.add_argument("--fresh", action="append", default=[], help="graph:seconds (graph = name or 0-1,1-2,...)")
    ap.add_argument("--fresh-slack", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--no-store", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()

    claims = {k: v[0] for k, v in CLAIMS.items()}
    if a.pred_file:
        spec = importlib.util.spec_from_file_location("userpreds", a.pred_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k, v in mod.CLAIMS.items():
            claims[k] = v[0] if isinstance(v, tuple) else v
    if a.list:
        for k, v in CLAIMS.items():
            print("%-9s expected %-8s ledger %-10s %s" % (k, v[1], v[2], (v[0].__doc__ or "").split("\n")[0]))
        return
    paths = [CORE] + ([BULK] if a.bulk else [])
    if a.stats:
        stats(paths)
        return
    names = list(CLAIMS) if a.sanity else a.claim
    if not names:
        ap.error("give --claim NAME (or --sanity / --list / --stats)")
    reps = {nm: Report(nm) for nm in names}
    t0 = time.time()
    filt = make_filter(a.filter) if a.filter else None
    cnt = 0
    if not a.no_store:
        for r in load_store(paths, filt):
            cnt += 1
            if a.limit and cnt > a.limit:
                break
            C = rec_circ(r)
            x = Ctx(C, r["edges"], r)
            for nm in names:
                reps[nm].see(x, claims[nm](x), r["id"])
            if a.closure:
                Rc = x.R
                for v in x.G.V:
                    for X in ([v], x.G.N(v)):
                        S = red(Rc, {w: 0 for w in X})
                        E2 = delete(x.G.E, X)
                        if not E2 or S.size == 0:
                            continue
                        y = Ctx(S, E2, {"id": "%s|x%s:=0" % (r["id"], "".join(map(str, X)))})
                        for nm in names:
                            reps[nm].see(y, claims[nm](y), y.rec["id"])
            if cnt % 20000 == 0:
                print("  ... %d circuits, %.0f s" % (cnt, time.time() - t0), file=sys.stderr, flush=True)
    fr = []
    for spec in a.fresh:
        gname, secs = spec.rsplit(":", 1)
        n, E = parse_graph(gname)
        for nm in names:
            tr, va, un = fresh(claims[nm], n, E, float(secs) / len(names), a.fresh_slack, a.seed, reps[nm], gname)
            fr.append({"claim": nm, "graph": gname, "edits": tr, "valid": va, "distinct": un})
    print("store circuits read: %d   (%.0f s)" % (cnt, time.time() - t0))
    for f in fr:
        print("fresh %(graph)s for %(claim)s: %(edits)d edits, %(valid)d valid, %(distinct)d distinct circuits" % f)
    out = []
    for nm in names:
        reps[nm].show()
        d = reps[nm].as_dict()
        if nm in CLAIMS:
            d["expected"] = CLAIMS[nm][1]
            d["ledger_id"] = CLAIMS[nm][2]
            d["as_expected"] = (d["violations"] > 0) == (CLAIMS[nm][1] == "refuted")
        out.append(d)
    if a.sanity:
        bad = [d["claim"] for d in out if not d["as_expected"]]
        print("\nsanity: %d claims, %d as expected; unexpected: %s" % (len(out), len(out) - len(bad), bad or "none"))
    outp = a.out or (os.path.join(HERE, "sanity_report.json") if a.sanity else None)
    if outp:
        json.dump({"store_circuits": cnt, "filters": a.filter, "bulk": a.bulk, "fresh": fr, "results": out,
                   "seconds": round(time.time() - t0, 1)}, open(outp, "w"), indent=1)
        print("wrote", outp)


if __name__ == "__main__":
    main()
