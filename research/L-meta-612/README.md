# L-meta-612: research notes

Gap L-meta-612 from https://pequalnp.com: for every graph G with an edge and no 4-cycle,
every monotone circuit of fan-in-two AND/OR gates computing the edge function
f_G(x) = OR over edges uv of (x_u AND x_v) has at least |E| + tau(G) - 1 gates,
where tau is the vertex cover number.

Status: open. Not proved, no counterexample found.

- `argument.md`: what is proved (upper bound, restriction accounting, forced variables,
  OR-prefix, edge creation), the machine evidence, two negative structural results, and the
  single open lemma E* that would imply the claim.
- `scripts/`: exact SAT search (python-sat, CaDiCaL). `mcsat.py` is the encoding.
- `data/`: outputs. `n6.txt`: all 43 C4-free graphs on at most 6 vertices satisfy the bound
  (UNSAT at size bound - 1). `s7.txt`: the 7-vertex sweep (46 of 73 checked, 27 timed out).

Run a script with `python3 -I scripts/<name>.py` after `pip install python-sat`.
