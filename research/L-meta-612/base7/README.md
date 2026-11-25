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

Every row: validation (U circuit accepted at s = Phi) passed; every size m = 1..Phi-1 UNSAT; missing = [].
Times: "kissat total" is the sum over all m (almost all of it at m = Phi-1); the DRAT column is the
drat-trim check of the m = Phi-1 run (all smaller m were also VERIFIED, see logs/NAME.log).

### Level 6 (re-proved; inputs to the 7-vertex restriction families)

| name | edges | tau | Phi | label | restrictions | kissat total | drat-trim at Phi-1 |
|---|---|---|---|---|---|---|---|
| N6a (triangle + C5 sharing an edge) | 01 02 13 15 24 35 45 | 3 | 9 | DRAT | 241 | 1.4 s | VERIFIED (3.4 s, 2.7 MB) |
| N6b (two triangles + bridge) | 01 02 04 13 15 24 35 | 4 | 10 | DRAT | 256 | 4.8 s | VERIFIED (6.8 s, 13.1 MB) |

### Level 7: the 8 open graphs of subcubic.md section 3 (task (a)): ALL CLOSED, DRAT

| name | edges | tau | Phi | label | restrictions | kissat total | drat-trim at Phi-1 |
|---|---|---|---|---|---|---|---|
| G7a | 01 02 03 14 26 45 46 56 | 3 | 10 | DRAT | 702 | 0.7 s | VERIFIED (2.3 s, 2.4 MB) |
| G7b | 01 02 03 14 16 25 46 56 | 4 | 11 | DRAT | 736 | 79.1 s | VERIFIED (128.9 s, 128 MB) |
| G7c | 01 02 06 13 24 26 35 56 | 4 | 11 | DRAT | 733 | 82.0 s | VERIFIED (121.8 s, 128 MB) |
| G7d | 01 02 13 24 26 35 46 56 | 4 | 11 | DRAT | 736 | 49.3 s | VERIFIED (81.7 s, 73 MB) |
| G7e | 01 02 05 13 15 24 26 46 | 4 | 11 | DRAT | 746 | 0.7 s | VERIFIED (2.1 s, 2.6 MB) |
| G7f | 01 02 13 15 24 26 35 46 | 4 | 11 | DRAT | 749 | 20.0 s | VERIFIED (34.5 s, 34 MB) |
| G7g | 01 02 03 14 25 36 45 46 56 | 4 | 12 | DRAT | 717 | 870.2 s | VERIFIED (1229.8 s, 1119 MB) |
| G7h = constrS7 | 01 02 05 13 15 24 26 36 46 | 4 | 12 | DRAT | 727 | 639.2 s | VERIFIED (942.5 s, 882 MB) |

(The old 900 s sweep without restriction constraints timed out on all eight.)

### Level 8 (task (b))

(filled in as runs finish)
