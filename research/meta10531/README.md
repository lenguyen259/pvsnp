# L-meta-10531 notes (in progress)

Statement: not (forall t, HasCircuitSize 9 f t -> 14 <= t), f = edge function of the graph
05 06 16 26 17 37 47 28 38 58 78 (m = 11, tau = 4, k = m + tau - 1 = 14). Refuting needs a
circuit with <= 13 gates.

Model (PEqualNP/Defs/MetaComplexity.lean + Defs/CircuitLowerBounds.lean): straight-line program,
gates AND / OR / NOT, fan-in <= 2, every gate counted (NOT included), inputs free, output any wire
(a missing wire reads false). AND/OR with < 2 distinct inputs are copies/constants (never in a
minimal circuit); NOT reads its first input only.

Vertex covers of size 4: {0,6,7,8} and {5,6,7,8}. Star-cover circuit (14 gates) in localimp.py.

## Files
* enc.py   - pair-selector encoding (choice = (NOT j) or (j<k, AND/OR)), canon(), check().
* enc2.py  - compact KKY-style encoding (left/right one-hot selectors), same model, plus sound
             pruning: every non-output gate read, no NOT(NOT g), no op(g, NOT g), no
             op(a, op(a,b)) with the same op, colex order of adjacent independent gates
             (lexicographically least topological order; exchange argument), equal inputs only AND<OR.
* run2.py  - CEGAR driver (rows: 0, the 11 edge minterms, the maximal independent sets, random;
             counterexample rows added each round). --cadical = incremental CaDiCaL 1.9.5.
* localimp.py - SAT window resynthesis from the 14-gate star circuit.
* validate.py - checks the encodings admit the canonicalised star circuit on all 512 rows.
