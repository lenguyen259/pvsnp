# L-meta-612 for maximum degree <= 3: what is known, what is open, attack order

Target **MAIN-C3**: every monotone fan-in-2 circuit for f_G, with G C4-free and max degree <= 3, has
size >= Phi(G) = |E| + tau(G) - 1. Class C3 is closed under vertex deletion, so a vertex-minimal
counterexample exists if MAIN-C3 fails, and t2's Corollary M (COR-M) and t3's Theorem L describe it.
Claim ids refer to `ledger.md`. Census data: `subcubic_graphs.json`, made by `subcubic_enum.py`
(connected graphs only, n <= 9, isomorphism-checked).

## 1. Proved parts of C3

* **Pseudoforests (every component has at most one cycle): PROVED in Lean** (THM-PF = AND-PF + L599).
  In C3 these are cycles (C3 or C_n, n >= 5) with pendant trees of max degree 3. This includes paths,
  cycles, suns, partial suns, the net, spiders and every forest. The t4/t6 partial-sun SAT base cases are
  superseded.
* **Max degree <= 2** (THM-F2) and **forests** (THM-F1): special cases.
* **Theorem F gives nothing new on C3.** A connected subcubic graph with at most one vertex of degree 3 has
  2|E| <= 2n + 1, so it is a pseudoforest. Theorem F (OR half for <= 1 hub) is therefore covered by THM-PF.
* **Any class, any circuit in a normal form:** STAR-ALL circuits (THM-S), circuits satisfying N1 and N3
  (THM-S2), clean circuits have #AND >= tau (LEM-A), formulas with clean rectangles (PROP-F), AND-depth-1
  circuits pay A(c) at every star centre (THM-SL). A minimal counterexample in C3 must violate N1 or N3.

## 2. What is false on C3 (so do not use it)

| route | smallest counterexample in C3 |
|---|---|
| (OR) #OR >= |E| - 1 (OR-C3) | **n8 = H8a** (Petersen minus an edge: n = 8, 10 edges, girth 5, delta = 2), size 14 = Phi+1, #OR 8. Not Petersen as deg3.md says. So (OR) fails even on C3' (no cubic component) and on girth >= 5. |
| split (OR)+(AND) (SPLIT-C3) | dead because of the line above (each saved OR costs an AND) |
| Lemma D (ch), sav-Lemma D, Dmin | constrS7 (n = 7, subcubic), size 14 = Phi+2 |
| Lemma M' / M0, one-vertex A-only induction | P6 (size 11), net (size 11), two triangles + bridge (size 13) |
| E*, E*+ (= mAB) | net (size 9); two triangles + bridge (size 13) |
| NF5 / "minimum circuits of triangle-free graphs are clean" | C5 with pendants at 0,1,2 (n = 8), size Phi = 11 (new; was Petersen at size 20) |
| T2-LO, T2-LT, T2-LD, **T2-LR** (syntactic payment counts) | net Phi+1, Petersen Phi, net Phi+2, **Petersen Phi+2 (new, this ledger)** |

The common lesson: any one-step lemma must use **functional** eliminations (gates that become equal, as
functions, to earlier nodes), and the paying vertex is not local to the obstruction.

## 3. Exact Phi verified by SAT, and the census

Connected C4-free subcubic graphs (count by status). PF = pseudoforest (THM-PF); SAT = exact value proved
by an UNSAT run at Phi - 1; OPEN = not covered.

| n | graphs | PF / max deg 2 | SAT-verified non-PF | OPEN with triangles | OPEN triangle-free |
|---|---|---|---|---|---|
| <= 5 | 11 | 11 | 0 | 0 | 0 |
| 6 | 12 | 10 | 2 (two triangles + bridge, Phi 10; triangle + C5 sharing an edge, Phi 9; `data/n6.txt`) | 0 | 0 |
| 7 | 27 | 18 | 1 (H7 = theta(2,3,3), Phi 11; petersen19) | **8** | 0 |
| 8 | 70 | 37 | 2 (H8a = n8, Phi 13, DRAT-checked; H8b, Phi 12; petersen19) | 27 | **4** |
| 9 | 188 | 75 | 0 (H9 = Petersen - v: UNSAT for s <= 14, s = 15 running) | 90 | 23 |
| 10 | (not enumerated) | | Petersen: UNSAT for s <= 15 (without H9 bounds), s = 16 running; upper bound 20 | | |

Every circuit-level statement in the ledger that survives (T2, T2F, mANB) has 0 violations on all stored
circuits of these graphs; the store has subcubic non-pseudoforest circuits for two triangles + bridge,
triangle + C5, constrS7, H7, n8 = H8a, Pet-v = H9, Petersen and others (`--filter subcubic --filter nonpf`).

**Smallest open graphs (n = 7, all contain triangles; the 7-vertex sweep timed out at 900 s on each):**

| edges | |E| | tau | Phi |
|---|---|---|---|
| 01 02 03 14 16 25 46 56 | 8 | 4 | 11 |
| 01 02 03 14 26 45 46 56 | 8 | 3 | 10 |
| 01 02 06 13 24 26 35 56 | 8 | 4 | 11 |
| 01 02 13 24 26 35 46 56 | 8 | 4 | 11 |
| 01 02 05 13 15 24 26 46 | 8 | 4 | 11 |
| 01 02 13 15 24 26 35 46 | 8 | 4 | 11 |
| 01 02 03 14 25 36 45 46 56 | 9 | 4 | 12 |
| 01 02 05 13 15 24 26 36 46 (= constrS7, the Lemma-D counterexample graph) | 9 | 4 | 12 |

**Smallest open triangle-free graphs (n = 8, 9 edges, Phi = 12, bicyclic, girth >= 5):**
`01 02 03 14 15 26 37 47 67`, `01 02 03 14 15 26 37 46 57`, `01 02 03 14 25 36 47 57 67` (girth 6),
`01 02 03 14 25 37 46 57 67`. Smallest cubic graph: Petersen (no cubic C4-free graph has n <= 9).

Every proper induced subgraph of an open 7-vertex graph has <= 6 vertices, so it is SAT-verified; the
restriction hierarchy of `petersen19/enc5.py` (`--rest --factc --viol --lexbot`) is therefore
unconditional for all eight, exactly as it was for H7 (solved in 68 s where the old encoder timed out).

## 4. Proposed attack order for MAIN-C3

1. **Close the small base cases by SAT (cheap, mechanical).** Run `enc5.py` with the restriction
   hierarchy on the eight open 7-vertex graphs, then the 4 triangle-free and 27 triangle 8-vertex graphs,
   adding each result to `petersen19/proven.json` so that later levels use it; let the running H9 (s = 15)
   and Petersen (s = 16) jobs finish. This does not prove MAIN-C3 (the class is infinite) but it fixes the
   base of the induction and gives exact minimum circuits to mine (enumerate all minimum circuits of the
   closed graphs into the store: the store has very few circuits of bicyclic triangle graphs).
2. **Reduce a minimal C3 counterexample to minimum degree 2.** In C3 every holder of a leaf has degree
   <= 3, which is exactly the hypothesis of t3's Theorem L(b)-(c): a bad leaf has the gadget
   x_v -> g = x_v | z -> q = g & y and the star or ORp shape. Prove NW-LEAF (some w in N(u) - v has N(w)
   good; 17,463/17,463 in the data) for degree-3 holders, or the slack form of Lemma N'. The pseudoforest
   case is closed, so only leaves hanging on non-pseudoforest cores remain.
3. **Minimum degree 2, threads.** Here the cores are subdivisions of cubic multigraphs (theta graphs, the
   7-vertex triangle graphs above, H7, H8a, ...). Use Corollary M item 5 (the pay_core vertex has degree 3
   or a degree-3 neighbour) and the run arguments of t4/t6 (options x_{P u B} := 1, Lemmas R2, PN, AT),
   which are graph-general, on degree-2 threads between hubs. Target statement: T2 (A or N option) or T2F
   (with B), with functional eliminations; T2-LR is refuted, so the count must include gates that become
   duplicates as functions. Use the falsifier's candidate mode to evolve localised versions of T2 on
   threads before attempting proofs.
4. **Cubic cores last.** The only cubic graphs are those with girth >= 5 and n >= 10 (Petersen first).
   There the N[v] option must save Phi(P) - Phi(C6) = 12 gates and A(v) saves at most 4; OR-split fails
   (13-OR circuits of size 20). Expect to need the exact Petersen value from SAT and a global argument
   (trading saved ORs for extra ANDs, as in every known 13-OR circuit).

Evidence budget: all of the above statements are DATA-level in C3; nothing beyond pseudoforests and the
SAT base cases is proved.
