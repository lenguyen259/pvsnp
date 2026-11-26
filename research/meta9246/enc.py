import sys, time, argparse, json
from pysat.solvers import Solver
from pysat.formula import CNF
from rup import *
ap = argparse.ArgumentParser()
ap.add_argument('m', type=int); ap.add_argument('n', type=int); ap.add_argument('k', type=int)
ap.add_argument('-T', type=int, default=8); ap.add_argument('--solver', default='cadical153')
ap.add_argument('--maxw', type=int, default=0); ap.add_argument('--dump'); ap.add_argument('--sym', action='store_true')
ap.add_argument('--out')
a = ap.parse_args()
m, n, k, T = a.m, a.n, a.k, a.T
L = 2 * m * n
F = php(m, n)
cnt = 0
def nv():
    global cnt; cnt += 1; return cnt
cl = []
inn = [[nv() for l in range(L)] for s in range(k)]
val = [[[nv() for t in range(T + 1)] for l in range(L)] for s in range(k)]
for s in range(k):
    for l in range(0, L, 2): cl.append([-inn[s][l], -inn[s][l + 1]])
    if s == k - 1:
        for l in range(L): cl.append([-inn[s][l]])
    else:
        cl.append([inn[s][l] for l in range(L)])
    if a.maxw and s < k - 1:
        from pysat.card import CardEnc
        ce = CardEnc.atmost(lits=inn[s], bound=a.maxw, top_id=cnt, encoding=1)
        cnt = max(cnt, ce.nv); cl += ce.clauses
    for l in range(L):
        cl.append([-val[s][l][0], inn[s][l ^ 1]])
        cl.append([val[s][l][0], -inn[s][l ^ 1]])
        for t in range(1, T + 1):
            cl.append([-val[s][l][t - 1], val[s][l][t]])
            just = [val[s][l][t - 1]]
            for D in F:
                if l in D:
                    oth = [x for x in D if x != l]
                    if len(oth) == 1: just.append(val[s][oth[0] ^ 1][t - 1])
                    else:
                        u = nv(); just.append(u)
                        for x in oth: cl.append([-u, val[s][x ^ 1][t - 1]])
            for j in range(s):
                u = nv(); just.append(u)
                cl.append([-u, inn[j][l]])
                for x in range(L):
                    if x != l: cl.append([-u, -inn[j][x], val[s][x ^ 1][t - 1]])
            cl.append([-val[s][l][t]] + just)
    conf = []
    for D in F:
        u = nv(); conf.append(u)
        for x in D: cl.append([-u, val[s][x ^ 1][T]])
    for j in range(s):
        u = nv(); conf.append(u)
        for x in range(L): cl.append([-u, -inn[j][x], val[s][x ^ 1][T]])
    cl.append(conf)
print('vars', cnt, 'clauses', len(cl), flush=True)
if a.dump:
    CNF(from_clauses=cl).to_file(a.dump); sys.exit()
t0 = time.time()
with Solver(name=a.solver, bootstrap_with=cl) as S:
    r = S.solve()
    print('SAT' if r else 'UNSAT', 'time %.1f' % (time.time() - t0), flush=True)
    if r:
        mod = set(x for x in S.get_model() if x > 0)
        run = [frozenset(l for l in range(L) if inn[s][l] in mod) for s in range(k)]
        print(show(run, n)); print('checker:', refutes(F, run, k))
        if a.out: json.dump([sorted(C) for C in run], open(a.out, 'w'))
