# Validation of enc.py on functions that need NOT: XOR(x0,x1) (min 4: or, and, not, and) and
# NOT x0 (min 1), in both the faithful and the normal-form (--strict) encodings.
import enc
from pysat.solvers import Cadical153
def run(F, s, strict):
    enc.F = F
    P, cl, kinds = enc.build(s, False, True, strict)
    S = Cadical153(bootstrap_with=cl)
    if not S.solve(): return 'UNSAT'
    pg = enc.to_project(enc.decode(P, S.get_model(), s, kinds))
    assert all(enc.ev(pg, [bool((r >> i) & 1) for i in range(6)]) == bool(F[r]) for r in range(64))
    return 'SAT ' + str(pg)
xor = [((r ^ (r >> 1)) & 1) for r in range(64)]
nx = [1 - (r & 1) for r in range(64)]
mux = [((r >> 1) & 1) if r & 1 else ((r >> 2) & 1) for r in range(64)]
for name, F, lo in (('xor', xor, 4), ('not', nx, 1), ('mux', mux, 4)):
    for strict in (False, True):
        for s in range(max(1, lo - 1), lo + 1):
            print(name, 'strict' if strict else 'faithful', s, run(F, s, strict), flush=True)
