# L-meta-18434: RepSizeAtMost (u != v on Fin 10) 33 -- NOT FOUND (best 34)

Defs (origin/main lean/PEqualNP/Defs/Represents.lean; the local clone working tree is STALE and lacks it):
`Represents A C` quantifies ONLY over the 100 `oneEach u v` inputs, so the value of C on every other input
is irrelevant (checked). `RepSizeAtMost` = Monotone2 circuit (AND/OR, <= 2 inputs, constants/copies allowed
but useless), size <= s.

Files: g.py (exact 100-row evaluator, wire w<10 = left, 10..19 = right, gate j = wire 20+j; parses the Lean circuit),
c34.json (the accepted 34-gate circuit of L_meta_18262, validated on all 100 pairs), lns.py (windowed LNS with exact
don't-cares on the 100 rows, k-1 improve / k plateau moves), t2.py (promise-T2 exact synthesis), logs.

Model: wires as 100-bit sets (rows R_a, columns C_b; AND = intersection, OR = union). The 34 circuit is
z_i = x_i|y_i (10 gates) + promise threshold-2 on the z's (weight 1 vs 2) with 24 gates.

Results (DATA):
- LNS, 2 seeds x 30 min, windows 3..8 gates (<= 8 inputs, <= 3 outputs), ~75k windows, plateau moves accepted at 34: no 33.
- Promise-T2 on n z-variables (exact SAT): n=4: 7 (6 not found in 0.6 s, UNSAT-like), n=5: 10, n=6: 13, n=7: 16 SAT;
  all equal the halving recursion (T,OR pairs); the 10-variable case needs 24 (halving gives 25), so savings only appear for larger n.
  This is within the z-model only, not a bound for the full problem.
- n=7 at 15 gates: no answer in 7 min (timeout), n=6 at 12 not run to completion.
