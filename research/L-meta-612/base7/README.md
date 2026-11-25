# base7: SAT base cases for L-meta-612 on C4-free subcubic graphs (step 1 of subcubic.md section 4)

Claim per graph G: every monotone AND/OR fan-in-2 circuit for f_G has size >= Phi(G) = |E| + tau - 1.
Labels: **UNSAT** (kissat 4.0.4 says UNSAT for every size m = 1..Phi-1, encoding validated),
**DRAT** (additionally every one of those UNSAT runs has a kissat DRAT proof checked by drat-trim),
**TIMEOUT**, **SAT** (would be a counterexample).

## Method (`run7.py`, `batch.sh`)

* Encoder: `enc5.py` copied unchanged from `../petersen19/` (with `grest.py`, `grest2.py`, `mku.py`,
  `ulb.py`, `plib.py`). Soundness argument: `../petersen19/README.md` section 1. Since the size-m
  encoding only has to admit a circuit of size m when the minimum size is m, every m = 1..Phi-1 is run.
* Flags for m < Phi: `--factc --viol --lexbot --rest rest/rest_NAME.json`.
* Restriction family: `grest2.family2(E, proven, minL=1)` (all (A, B) with A independent, U = N(A) \ B,
  H = G - A - N(A) - B). Bounds used: Theorem PF for pseudoforest H (Lean), `../petersen19/proven.json`
  (H7, H8a, H8b) and entries of `../ledger/proven_subcubic.json` with status `UNSAT-all-m` (this run).
  `run7.py` lists every proper induced non-pseudoforest subgraph without a proven bound
  ("missing"); such H are just left out of the family (sound, weaker). Every row of the table below has
  missing = [] (the hierarchy is complete), so the result is unconditional modulo the solver.
* Bottom-up order: the two non-pseudoforest 6-vertex graphs (N6a, N6b) are re-proved first (they were
  only SAT-labelled in `data/n6.txt`, CaDiCaL, no proof), then the 7-vertex graphs, then 8 vertices.
* Non-vacuity, per graph: the lexbot-canonical U (star-cover) circuit is accepted at s = Phi with
  `--rest --factc --lexbot --fixc` (VERIFIED on all 2^n inputs).
* Per m: `enc5.py m ... --dimacs` -> `kissat -q --time=1800 --no-binary CNF PROOF` -> `drat-trim CNF PROOF`.
* One solver process at a time, launched through `research/tools/cpuslot.sh`.

Logs: `logs/NAME.log` (one line per step), `logs/batch*.out`. Records: `../ledger/proven_subcubic.json`.

## Results

(filled in below as runs finish)
