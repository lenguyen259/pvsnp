# L-meta-9246: RUP run for PHP(5,4) with at most 12 learned clauses? (2026-11-26)

Status: UNRESOLVED after about 75 minutes. No run with <= 12 found, no run with 13 found either, no
impossibility proof. No Lean file written.

## Definitions (lean/PEqualNP/Defs/SearchRUP.lean, Defs/ProofComplexity.lean)

- Clause V = Finset (V x Bool); (v, true) is the positive literal. PHP m n = m pigeon clauses
  (width n) and the binary hole clauses {-(i,j), -(i',j)}, i != i'.
- UPForces G A l: least fixed point; l is in A, or some D in G contains l and every other literal of
  D has its complement forced. Propagation does not stop at a conflict.
- IsRUP G C: some D in G has every literal's complement forced from A = negations of C.
- IsRUPRun F rho: list NEWEST FIRST; each clause is RUP over F plus the clauses after it in the list.
  The empty clause is an element of rho and counts in rho.length. Duplicates, tautologies and clauses
  after the empty clause are allowed but useless. No deletion.

## Files

- rup.py: exact checker (runs given oldest first). enc.py: SAT encoding, layered unit propagation
  (T parallel layers, sound for every T, complete for T >= number of variables), options --unit
  pos|neg (symmetry: some learned unit is x00, or -x00 with no positive unit), --need (clauses that
  must occur in order), --noempty, --maxw. enc2.py: same with deterministic propagation (both
  directions). decode.py: read a kissat model of a dumped CNF.

## Results

- DATA/UNSAT (pysat cadical153, T = 12, 148 s): PHP(4,3) has no run with 4 clauses; agrees with
  accepted L_meta_9208. So the encoding is validated on a negative, and on positives below.
- DATA: PHP(3,2) minimum 2; PHP(4,3) minimum 5, many shapes, all checked by rup.py, e.g.
  [-x32 x10], [-x00], [-x21], [-x20], []   and   [-x02 x20], [x11 x12], [x31 x32], [x12], [].
  The useful clauses are not symmetric: one conditional helper with a positive literal, then units.
  Sequence so far 2, 5, then 13 claimed by the desk (2,5,12 would be Pell; 2,5,13 odd Fibonacci).
- TIMEOUT: PHP(5,4), k = 12 and k = 13, plain encoding T = 10 (kissat, about 9 CPU-min each) and
  deterministic encoding with --unit pos, T = 9 (kissat, about 9 CPU-min each): no answer. The same
  solver does not even rediscover a 13-clause run, so these timeouts say nothing about 12.
- TIMEOUT: restricted class 'exclude pigeons 1,2,3 from hole 0 (clauses x_i1 x_i2 x_i3) within 7
  clauses, then the 6-clause finish -x11-x22, -x11, -x12-x21, -x12, -x21, empty': no answer in 4 min.
- Known from origin/main: <= 6 is impossible (L_meta_9237); <= 24 holds (L_meta_9250, run of 20).

## What to try next

- Monolithic SAT is too slow (UNSAT of k=4 for PHP(4,3) already takes minutes). Break symmetry by
  enumerating the first clause up to S5 x S4 among subset-minimal RUP clauses (WLOG: a learned clause
  can be replaced by any subset that is RUP at that time), then cube on it.
- Or explicit search over skeletons 'conditional helpers + units' taken from the PHP(4,3) optima.
- Get the desk's 13-clause run if it is published; validate enc.py on it with --need.
