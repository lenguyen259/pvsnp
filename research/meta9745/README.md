# L-meta-9745: a 25-gate circuit for f_G, G = Heawood graph minus an edge? (bounded search)

Statement: HasCircuitSize 14 f_G 25, f_G = OR of x_u x_v over the 20 edges
0-8 0-10 1-7 1-9 1-13 2-8 2-12 2-13 3-7 3-11 3-12 4-10 4-11 4-13 5-9 5-10 5-12 6-8 6-9 6-11.
Best known: 26 = |E| + tau - 1 (star cover). Model (Defs/MetaComplexity.lean): AND/OR/NOT, fan-in <= 2,
every gate counted, inputs free. A 25-gate monotone circuit would refute L-meta-612.

Labels: PROVED / DATA / TIMEOUT as in the playbooks.

## Graph facts (DATA, `g.py` + networkx)

* G + edge 0-7 is isomorphic to the Heawood graph (incidence graph of the Fano plane): G is the
  Fano incidence graph minus one flag. Bipartite 7+7, girth 6, degrees 2 (vertices 0, 7) and 3.
* tau = 7; the only vertex covers of size 7 are the two sides {0..6} and {7..13}. So every star-cover
  circuit uses one whole side as centres: 20 + 7 - 1 = 26.
* alpha = 7, 37 maximal independent sets, |Aut(G)| = 16 (= 336/21, the flag stabiliser).

## Structural notes

1. No local saving inside a set of stars (PROVED, easy). Let Q be a set of left centres and g the OR of
   their stars. Zeroing every variable outside Q u N(Q) kills all other stars (their centres are 0),
   so any circuit for f restricts to a circuit for g = f_{G[Q u N(Q)]} (a smaller C4-free graph; a
   forest unless Q spans a cycle). Hence, as long as the bound holds for these smaller graphs (PF for
   forests/pseudoforests), a saving cannot come from re-implementing a sub-collection of stars on its own
   variables; it must mix in variables or wires of the rest of the circuit ("global" sharing).
2. Monotone sharing of a sub-OR between two stars needs two common neighbours (a C4): impossible.
3. Rectangle gadgets (OR A) & (OR B) (`gadgets.py`): cost |A|+|B|-1, cover e(A,B) edges. Excess
   e - (|A|+|B|-1) is positive for every A x B containing a cycle (6-cycle: excess 1, junk 3; 4x4:
   excess 2, junk 7; 7x7: excess 7, junk 29). Junk non-edges per unit of excess is always >= 3 (minimum at 6-cycles),
   and killing junk on the 2-slice is the same problem as computing f on G[A u B] (edges vs non-edges),
   so no gadget gives a saving for free; this is the familiar reason the conjecture is believed.

## Search (DATA)

`lns.py`: large-neighbourhood search on 26-gate circuits (random star covers, both sides, random OR
trees). Each step picks a random connected convex window of 3..7 gates (<= 8 window inputs, <= 3
window outputs) and resynthesises it as a Boolean RELATION: the allowed window-output vectors for each
window-input pattern are computed exactly on all 2^14 inputs (satisfiability AND observability don't
cares: rest of the circuit evaluated with each output vector forced), then SAT (CaDiCaL 1.5.3 via pysat,
AND/OR/NOT gates, conflict budget 20000) looks for k-1 gates (improvement), else with prob 0.6 a random
k-gate replacement (plateau), else with prob 0.05 k+1 gates (uphill, size cap 27). Every accepted circuit
is checked on all 16384 inputs.

Validation: from a 27-gate circuit (star of vertex 1 split as (x1&x7)|(x1&(x9|x13))) the search finds 26
after 21 windows (`test2.py`).

## Results (DATA, 2026-11-25, about 45 min CPU in one slot)

| phase | windows (gates) | max window inputs | starts | windows tried | best |
|---|---|---|---|---|---|
| 1 (`run.sh`, `lns.py`) | 3..7 | 8 | 6 runs x 240 s, left/right covers | 2764 | 26 |
| 2 (`run2.sh`, `lns2.py`) | 6..9 | 10 | 2 runs x 150 s | 20 | 26 (too slow: 1024-row encodings) |
| 3 (`run3.sh`, `lns2.py`) | 5..8 | 9 | 2 runs x 240 s | 241 | 26 |

No circuit with <= 25 gates found (no `found_*.json`). The walk moved freely on the 26/27 plateau
(e.g. mixed-side circuits such as x8 & (x0|x6) next to x6 & (x9|x11) at size 27) but never below 26.
No accepted circuit contained a NOT gate: every window replacement SAT chose was monotone.
This is weak evidence only (windows <= 9 gates); it does not bear on L-meta-612 beyond "no local
NOT-saving or monotone saving near star covers".

Not attempted: global SAT at 25 (out of reach, per brief); LNS with CEGAR rows for windows of 10+
gates (would be the next step: build the window encoding incrementally on counterexample rows instead
of all 2^|ins| patterns, which is what made phase 2 slow).
