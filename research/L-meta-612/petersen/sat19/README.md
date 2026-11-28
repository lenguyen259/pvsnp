# Petersen at size 19: SAT attempts (verdict unknown)

Goal: decide whether the Petersen graph (|E|=15, tau=6, bound 20) has a monotone circuit with 19 gates.
Every size-19 run timed out (up to 2 h, CaDiCaL 1.9.5; Kissat once). Nothing was refuted.

Encodings (`enc.py`, `enc2.py`, `enc3.py`): 15 edge rows must output 1 and the 15 maximal independent sets
must output 0; canonical gate order; first-gate symmetry break; optional constraints from Theorems S/S2
and Fact C; `enc3.py` adds an associativity normal form and exact restriction-count constraints
(setting a vertex or a pair to 0 removes at most size - L(G - Z) gates).

Validated: the U circuit and the 13-OR size-20 circuit are accepted, and the 13-OR circuit is found when
constrained. An unconstrained search does not find a size-20 circuit within 30 min.

Conditional result (restriction constraints assume every proper induced subgraph meets |E|+tau-1):
size <= 16 UNSAT immediately, size 17 UNSAT (146 s), sizes 18 and 19 timed out.
`rec.py` proved the assumption for all induced subgraphs with <= 6 vertices and 2 of the 3 types with 7
vertices; [01,12,23,34,40,05,26,56] (bound 11) is open at size 10; 8- and 9-vertex subgraphs not attempted.
