"""Exact mirror of PEqualNP.Search.IsRUPRun for PHP m n.
Literal = (i, j, sign) ; code: 2*(i*n+j) + (0 if sign True else 1).  neg = l ^ 1.
A run is given OLDEST FIRST here (Lean list is newest first)."""
def lit(i, j, s, n): return 2 * (i * n + j) + (0 if s else 1)
def unlit(l, n): return ((l >> 1) // n, (l >> 1) % n, (l & 1) == 0)
def php(m, n):
    F = [frozenset(lit(i, j, True, n) for j in range(n)) for i in range(m)]
    for j in range(n):
        for i in range(m):
            for i2 in range(i + 1, m):
                F.append(frozenset([lit(i, j, False, n), lit(i2, j, False, n)]))
    return F
def up_closure(G, A):
    """least set of forced literals (UPForces G A), no stopping at conflicts (as in Lean)"""
    forced = set(A); ch = True
    while ch:
        ch = False
        for D in G:
            unf = [l for l in D if (l ^ 1) not in forced]
            if len(unf) == 1 and unf[0] not in forced:
                forced.add(unf[0]); ch = True
    return forced
def is_rup(G, C):
    f = up_closure(G, {l ^ 1 for l in C})
    return any(all((l ^ 1) in f for l in D) for D in G)
def is_run(F, run):
    G = list(F)
    for idx, C in enumerate(run):
        if not is_rup(G, C): return False, idx
        G.append(frozenset(C))
    return True, None
def refutes(F, run, k=None):
    ok, idx = is_run(F, run)
    return ok and any(len(C) == 0 for C in run) and (k is None or len(run) <= k)
def show(run, n):
    return [sorted(('' if s else '-') + f"x{i}{j}" for (i, j, s) in (unlit(l, n) for l in C)) for C in run]
