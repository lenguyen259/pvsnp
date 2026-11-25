#!/usr/bin/env python3
"""Exact synthesis for L-meta-12906 in the project's circuit model.
Wires: 0 = a missing wire (reads false), 1..6 = inputs x0..x5, 7.. = gates.
Gate kinds: AND(a,b), OR(a,b), NOT(a), TRUE (AND of no wire). a,b any earlier wire, a<=b
(a=b gives a fan-in-1 copy; OR of no wire = AND(0,0) = false).  Output = last gate.
usage: enc.py s mono|gen [--cnf file] [--nosym]
"""
import sys, itertools
from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical153
N = 4276813546 * 2**32 + 4276791976
n = 6
F = [(N >> r) & 1 for r in range(64)]

def build(s, mono, sym=True):
    P = IDPool(); cl = []
    W = 1 + n + s
    def val(j, r):  # literal or bool
        if j == 0: return False
        if j <= n: return bool((r >> (j - 1)) & 1)
        return P.id(('v', j, r))
    kinds = ['and', 'or'] + ([] if mono else ['not', 'true'])
    for i in range(1 + n, W):
        A = [P.id(('a', i, j)) for j in range(i)]
        B = [P.id(('b', i, j)) for j in range(i)]
        T = {k: P.id(('t', i, k)) for k in kinds}
        for X in (A, B, list(T.values())):
            cl.append(X[:])
            for p, q in itertools.combinations(X, 2): cl.append([-p, -q])
        # a <= b
        for j in range(i):
            for k in range(j):
                cl.append([-A[j], -B[k]])
        if not mono:
            # NOT / TRUE: b fixed to wire 0 ; TRUE: a fixed to 0
            cl.append([-T['not'], B[0]]); cl.append([-T['true'], B[0]]); cl.append([-T['true'], A[0]])
        for r in range(64):
            v = P.id(('v', i, r)); pa = P.id(('pa', i, r)); pb = P.id(('pb', i, r))
            for X, p in ((A, pa), (B, pb)):
                for j in range(i):
                    w = val(j, r)
                    if w is True: cl.append([-X[j], p])
                    elif w is False: cl.append([-X[j], -p])
                    else: cl.append([-X[j], -w, p]); cl.append([-X[j], w, -p])
            cl += [[-T['and'], -pa, -pb, v], [-T['and'], pa, -v], [-T['and'], pb, -v]]
            cl += [[-T['or'], pa, pb, -v], [-T['or'], -pa, v], [-T['or'], -pb, v]]
            if not mono:
                cl += [[-T['not'], pa, v], [-T['not'], -pa, -v], [-T['true'], v]]
    for r in range(64):
        v = P.id(('v', W - 1, r)); cl.append([v] if F[r] else [-v])
    if sym:
        # every gate but the last is read by a later gate (sound: pad with copies at the end)
        for j in range(1 + n, W - 1):
            cl.append([P.id((x, i, j)) for i in range(j + 1, W) for x in 'ab'])
    return P, cl, kinds

def decode(P, model, s, kinds):
    ms = set(l for l in model if l > 0); gates = []
    for i in range(1 + n, 1 + n + s):
        a = next(j for j in range(i) if P.id(('a', i, j)) in ms)
        b = next(j for j in range(i) if P.id(('b', i, j)) in ms)
        k = next(k for k in kinds if P.id(('t', i, k)) in ms)
        gates.append((k, a, b))
    return gates

def to_project(gates):
    """Project gate list: (op, inputs) with wire indices: inputs 0..5, gates 6.. ; missing wire -> dropped
    when sound (OR drops false inputs; AND with false -> keep as index 10**6)."""
    out = []
    for k, a, b in gates:
        m = lambda j: 10**6 if j == 0 else j - 1
        if k == 'true': out.append(('and', []))
        elif k == 'not': out.append(('not', [m(a)]))
        else: out.append((k, [m(a), m(b)]))
    return out

def ev(pg, x):
    w = list(x)
    for op, ins in pg:
        vals = [w[i] if i < len(w) else False for i in ins]
        if op == 'and': w.append(all(vals))
        elif op == 'or': w.append(any(vals))
        else: w.append((not vals[0]) if vals else True)
    return w[-1]

if __name__ == '__main__':
    s = int(sys.argv[1]); mono = sys.argv[2] == 'mono'
    P, cl, kinds = build(s, mono, '--nosym' not in sys.argv)
    if '--cnf' in sys.argv:
        CNF(from_clauses=cl).to_file(sys.argv[sys.argv.index('--cnf') + 1]); sys.exit()
    S = Cadical153(bootstrap_with=cl)
    if S.solve():
        g = decode(P, S.get_model(), s, kinds); pg = to_project(g)
        ok = all(ev(pg, [bool((r >> i) & 1) for i in range(n)]) == bool(F[r]) for r in range(64))
        print('SAT', s, sys.argv[2], 'validated' if ok else 'INVALID', pg, flush=True)
    else:
        print('UNSAT', s, sys.argv[2], flush=True)
