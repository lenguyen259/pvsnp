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

### Level 8, triangle-free bicyclic (task (b), first part): ALL 4 CLOSED, DRAT

| name | edges | tau | Phi | label | restrictions | kissat total | drat-trim at Phi-1 |
|---|---|---|---|---|---|---|---|
| G8tf0 | 01 02 03 14 15 26 37 47 67 | 4 | 12 | DRAT | 2156 | 3.9 s | VERIFIED (0.9 s, 1.8 MB) |
| G8tf1 | 01 02 03 14 15 26 37 46 57 | 4 | 12 | DRAT | 2202 | 237.9 s | VERIFIED (358.9 s, 271 MB) |
| G8tf2 (theta(3,3,3), girth 6) | 01 02 03 14 25 36 47 57 67 | 4 | 12 | DRAT | 2162 | 519.0 s | VERIFIED (693.4 s, 401 MB) |
| G8tf3 | 01 02 03 14 25 37 46 57 67 | 4 | 12 | DRAT | 2188 | 296.1 s | VERIFIED (428.8 s, 294 MB) |

### Level 8 with triangles (task (b), second part; 27 graphs G8t00..G8t26 in `batch8tr.txt`)

Run in chunks (`batch8tr_a.txt` = G8t00..G8t07 first). The container restarted once (2026-11-25/26);
no run was lost (all results above were already recorded).

Chunk a (G8t00..G8t07, run 2026-11-26 03:13-03:15 UTC): 8/8 CLOSED, DRAT, every one in seconds.

| name | edges | tau | Phi | label | restrictions | kissat total | drat-trim at Phi-1 |
|---|---|---|---|---|---|---|---|
| G8t00 | 01 02 03 14 15 26 27 47 67 | 4 | 12 | DRAT | 2169 | 8.4 s | VERIFIED (1.1 s, 1.8 MB) |
| G8t01 | 01 02 03 14 17 25 36 47 57 | 4 | 12 | DRAT | 2213 | 6.8 s | VERIFIED (1.0 s, 2.1 MB) |
| G8t02 | 01 02 03 14 17 25 46 47 57 | 4 | 12 | DRAT | 2166 | 5.3 s | VERIFIED (1.0 s, 1.8 MB) |
| G8t03 | 01 02 03 14 25 27 46 47 57 | 4 | 12 | DRAT | 2175 | 7.0 s | VERIFIED (1.0 s, 2.0 MB) |
| G8t04 | 01 02 03 14 25 27 46 57 67 | 4 | 12 | DRAT | 2183 | 8.7 s | VERIFIED (0.8 s, 1.3 MB) |
| G8t05 | 01 02 03 14 25 37 46 47 67 | 4 | 12 | DRAT | 2183 | 11.3 s | VERIFIED (1.7 s, 2.3 MB) |
| G8t06 | 01 02 03 14 25 46 47 57 67 | 4 | 12 | DRAT | 2153 | 7.4 s | VERIFIED (0.9 s, 1.8 MB) |
| G8t07 | 01 02 03 14 27 45 47 56 57 | 4 | 12 | DRAT | 2136 | 2.4 s | VERIFIED (0.7 s, 1.2 MB) |

Why these are fast: each contains a closed 7-vertex graph H = G - v with Phi(H) = Phi(G) - 1 = 11
(max tL 11; G8t05 has max tL 10). The restriction x_v := 0 then forces at least 11 = s surviving gates,
i.e. every gate survives, which leaves almost nothing to search. The triangle-free G8tf1..3 have no such
subgraph (max tL 9-10) and took 4-9 min plus 6-12 min of drat-trim.

Chunks b/c/d/e/f (G8t08..G8t26, 2026-11-26 03:2x-09:49 UTC, one solver at a time, kissat cap 1800 s):
G8t08..G8t14 DRAT (see logs, ledger); G8t15..G8t18 and G8t20 DRAT; **G8t19, G8t21..G8t26 TIMEOUT**.
All TIMEOUTs are at s = Phi-1 (all smaller s UNSAT); no SAT anywhere. Cube-and-conquer not started.

| name | edges | tau | Phi | label | restrictions | kissat total | drat-trim at Phi-1 |
|---|---|---|---|---|---|---|---|
| G8t15 | 01 02 03 14 16 25 37 46 57 | 5 | 13 | DRAT | 2238 | 696.5 s | VERIFIED (804.7 s, 503 MB) |
| G8t16 | 01 02 06 13 16 24 27 35 47 | 5 | 13 | DRAT | 2249 | 25.7 s | VERIFIED (4.3 s, 64 MB) |
| G8t17 | 01 02 13 24 26 35 37 46 57 | 5 | 13 | DRAT | 2238 | 559.3 s | VERIFIED (513.1 s, 430 MB) |
| G8t18 | 01 02 03 14 15 26 27 46 57 67 | 4 | 13 | DRAT | 2134 | 9.9 s | VERIFIED (1.0 s, 1.8 MB) |
| G8t19 | 01 02 03 14 25 36 46 47 57 67 | 4 | 13 | TIMEOUT at s=12 (1800 s) | 2118 | - | - |
| G8t20 | 01 02 06 13 17 24 26 35 37 47 | 4 | 13 | DRAT | 2131 | 11.6 s | VERIFIED (1.4 s, 1.7 MB) |
| G8t21 | 01 02 06 13 24 26 35 37 47 57 | 4 | 13 | TIMEOUT at s=12 (1800 s) | 2120 | - | - |
| G8t22 | 01 02 03 14 16 25 27 46 47 57 | 5 | 14 | TIMEOUT at s=13 (1800 s; s<=12 UNSAT) | 2170 | - | - |
| G8t23 | 01 02 03 14 16 25 37 46 47 57 | 5 | 14 | TIMEOUT at s=13 (s<=12 UNSAT, s=12 kissat 738 s) | 2159 | - | - |
| G8t24 | 01 02 03 14 17 25 36 46 47 57 | 5 | 14 | TIMEOUT at s=13 (s<=12 UNSAT, s=12 kissat 776 s) | 2156 | - | - |
| G8t25 | 01 02 06 13 16 24 27 35 47 57 | 5 | 14 | TIMEOUT at s=13 (s<=12 UNSAT, s=12 kissat 596 s) | 2156 | - | - |
| G8t26 | 01 02 06 13 17 24 26 35 37 47 56 | 5 | 15 | TIMEOUT at s=13 (s<=12 UNSAT) | 2078 | - | - |

Open (TIMEOUT, candidates for cube-and-conquer, `cubes7.py`): G8t19, G8t21, G8t22, G8t23, G8t24, G8t25, G8t26.
Note: G8t22..G8t26 time out at s = 13 = Phi-1 for Phi = 14, and G8t26 at s = 13 < Phi-1 = 14
(its s = 14 was never reached). Interrupted partial logs: `logs/G8t15|16|23|25.interrupted.log` (the
background-task limit of 2 h kills a whole batch.sh; the runs were restarted from the interrupted graph).

## Run log (UTC)

* 2026-11-25 16:17-16:18: N6a, N6b (DRAT).
* 16:18-17:31: batch7 (G7a..G7h), all DRAT; hardest G7g (s = 11: kissat 841 s, drat-trim 1230 s, 1.1 GB).
* 17:31-18:15: batch8tf (G8tf0..G8tf3), all DRAT.
* 2026-11-26 03:13-03:15 (after container restart): batch8tr_a (G8t00..G8t07), all DRAT.
* 2026-11-26 03:43-09:49: batch8tr_c..f (G8t15..G8t26): 5 DRAT, 7 TIMEOUT (see above); no SAT.
