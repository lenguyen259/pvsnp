# exact synthesis: AND/OR (fan-in 2) and NOT gates, NOT counts as a gate
import sys, itertools, time, json
from pysat.solvers import Solver
from pysat.card import CardEnc

def graph_fn(n, E):
    return [int(any((t>>a)&1 and (t>>b)&1 for a,b in E)) for t in range(1<<n)]

def encode(n, tt, s, monotone=False, maxnot=None):
    rows = range(1<<n)
    cnt = [0]
    def nv():
        cnt[0]+=1; return cnt[0]
    cls = []
    W = n + s
    sa = [[nv() for j in range(n+i)] for i in range(s)]
    sb = [[nv() for j in range(n+i)] for i in range(s)]
    isn = [nv() for i in range(s)]
    isa = [nv() for i in range(s)]
    x = [[nv() for t in rows] for i in range(s)]
    va = [[nv() for t in rows] for i in range(s)]
    vb = [[nv() for t in rows] for i in range(s)]
    def val(j,t):  # literal or bool
        if j < n: return bool((t>>j)&1)
        return x[j-n][t]
    for i in range(s):
        m = n+i
        for S in (sa[i], sb[i]):
            cls.append(list(S))
            for a in range(m):
                for b in range(a+1,m):
                    cls.append([-S[a],-S[b]])
        if monotone: cls.append([-isn[i]])
        # non-not: a<b ; not: sb=sa
        for j in range(m):
            for k in range(j+1):
                cls.append([isn[i], -sa[i][j], -sb[i][k]])
            cls.append([-isn[i], -sa[i][j], sb[i][j]])
        cls.append([-isn[i], -isa[i]])
        for t in rows:
            for (S, V) in ((sa[i], va[i]), (sb[i], vb[i])):
                for j in range(m):
                    v = val(j,t)
                    if isinstance(v,bool):
                        cls.append([-S[j], V[t] if v else -V[t]])
                    else:
                        cls.append([-S[j], -V[t], v]); cls.append([-S[j], V[t], -v])
            X, A, B = x[i][t], va[i][t], vb[i][t]
            # NOT
            cls.append([-isn[i], X, A]); cls.append([-isn[i], -X, -A])
            # AND
            cls.append([isn[i], -isa[i], -X, A]); cls.append([isn[i], -isa[i], -X, B]); cls.append([isn[i], -isa[i], X, -A, -B])
            # OR
            cls.append([isn[i], isa[i], X, -A]); cls.append([isn[i], isa[i], X, -B]); cls.append([isn[i], isa[i], -X, A, B])
    # output = last gate
    for t in rows:
        cls.append([x[s-1][t] if tt[t] else -x[s-1][t]])
    # every gate except last used
    for i in range(s-1):
        w = n+i
        lits = []
        for k in range(i+1, s):
            lits.append(sa[k][w]); lits.append(sb[k][w])
        cls.append(lits)
    # no NOT of NOT
    for i in range(s):
        for j in range(n, n+i):
            cls.append([-isn[i], -sa[i][j], -isn[j-n]])
    # symmetry: gates ordered by first input? (skip)
    if maxnot is not None:
        enc = CardEnc.atmost(lits=isn, bound=maxnot, top_id=cnt[0])
        cnt[0] = max(cnt[0], enc.nv)
        cls.extend(enc.clauses)
    return cls, dict(sa=sa,sb=sb,isn=isn,isa=isa,n=n,s=s)

def decode(model, info):
    M = set(l for l in model if l>0)
    n, s = info['n'], info['s']
    gates = []
    for i in range(s):
        a = [j for j,v in enumerate(info['sa'][i]) if v in M][0]
        b = [j for j,v in enumerate(info['sb'][i]) if v in M][0]
        op = 'NOT' if info['isn'][i] in M else ('AND' if info['isa'][i] in M else 'OR')
        gates.append((op,a,b))
    return gates

def evalc(n, gates, t):
    w = [(t>>j)&1 for j in range(n)]
    for op,a,b in gates:
        if op=='NOT': w.append(1-w[a])
        elif op=='AND': w.append(w[a]&w[b])
        else: w.append(w[a]|w[b])
    return w[-1]

def solve(n, tt, s, monotone=False, maxnot=None, solver='cadical195', verbose=True):
    cls, info = encode(n, tt, s, monotone, maxnot)
    t0=time.time()
    with Solver(name=solver, bootstrap_with=cls) as S:
        r = S.solve()
        dt=time.time()-t0
        if r:
            g = decode(S.get_model(), info)
            ok = all(evalc(n,g,t)==tt[t] for t in range(1<<n))
            if verbose: print('SAT', s, 'gates', 'verified', ok, '%.1fs'%dt, g, flush=True)
            return g
        else:
            if verbose: print('UNSAT', s, '%.1fs'%dt, flush=True)
            return None

if __name__ == '__main__':
    n = int(sys.argv[1]); E = json.loads(sys.argv[2]); s = int(sys.argv[3])
    mono = len(sys.argv)>4 and sys.argv[4]=='mono'
    solve(n, graph_fn(n,E), s, monotone=mono)
