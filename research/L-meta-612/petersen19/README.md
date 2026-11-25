# Petersen graph at sizes 18 and 19: an unconditional hierarchy plus SAT

Question: does f_P (Petersen, |E| = 15, tau = 6, conjectured bound Phi = 20) have a monotone fan-in-2
AND/OR circuit with 19 (or 18) gates? Labels: **PROVED** (argument here or cited proved theorem),
**UNSAT** (SAT solver, encoding validated for non-vacuity; "DRAT" = kissat proof checked by drat-trim),
**DATA**, **TIMEOUT**.

RESULTS: see section 5 (filled at the end of the run).

## 1. Encoding `enc5.py` (new)

Variables per gate i (gates n..n+s-1): left selector l(i,j), right selector r(i,k), j < k, op(i)
(true = AND), child values L(i,t), R(i,t) and gate value v(i,t) for every row t. This is much smaller
than the pair-selector encodings of `../petersen/sat19/enc*.py`: a restriction costs 4 binary clauses per
gate, because "gate i survives restriction rho" is just L(i,hi) & ~L(i,lo) & R(i,hi) & ~R(i,lo).

Rows: the 15 edges (output 1) and the 15 maximal independent sets (output 0) determine a monotone
function; plus singleton rows (for Fact C / violation) and two rows per restriction.

Constraints and why each is sound. We prove "no circuit of size <= s" by showing that every size m <= s
is UNSAT, where the size-m encoding only needs to admit **some** circuit of size m *if the minimum size
is m*:
* (min) every non-output gate is used; gates pairwise distinct and non-constant on the 30 core rows.
  If two gates agree on the core rows, replacing one by the other keeps every value on the core rows,
  so the output is still correct on the 30 rows, hence (monotone) still computes f with fewer gates.
  A gate constant on the core rows can be replaced by a constant and propagated away.
* (canon) depth-canonical order: depth non-decreasing; equal depth => (j,k,op) strictly
  lex-increasing (AND before OR). Every circuit has exactly one such ordering (level by level).
* (lexbot, PROVED symmetry breaking) let b be the 2*C(n,2)-bit vector "some gate reads input pair p with
  op o". We require b to be lex-maximal over Aut(G) (all automorphisms, computed with networkx). Every
  circuit has an automorphic image with lex-max b; all other constraints are Aut-invariant (the
  restriction families below are closed under Aut by construction: they are all (A,B) with a bound
  that depends only on the isomorphism type). Supersedes `--symb`.
* (factc) Fact C (argument.md/girth5.md): every edge uv is created at an AND gate h1&h2 with
  u in S1\S2, v in S2\S1. Valid for every circuit.
* (viol) Theorem S2 (nf/nf.md, PROVED for C4-free G): a circuit satisfying N1 and N3 has size >= Phi.
  So for s < Phi some AND gate violates N1 (h(e_u)=1) or N3 (u in S1, v in S2, u != v, uv not an edge).
  Used only for s < Phi(G).
* (rest) restriction constraints, the new lever. A restriction rho sets an independent set A to 1 and
  a set B (disjoint from A) to 0; U = N(A)\B stays free, H = G - A - N(A) - B. Then
  f|rho = OR_{u in U} x_u  v  f_H. Gate g *survives* if both its inputs are non-constant under rho
  (for monotone g: value 1 on the row hi = all-ones-except-B and 0 on lo = indicator of A). The
  surviving gates, with copies collapsed, form a circuit for f|rho, so:
  - U empty, H a pseudoforest: #surviving AND >= tau(H), #surviving OR >= |E(H)| - 1
    (**Theorem PF**, t9.md, Lean PF_AND.lean + L_meta_599; H is C4-free as an induced subgraph);
  - U empty, H with a bound L(H) PROVED in this folder (table `proven.json`): #surviving >= L(H);
  - U non-empty: #surviving >= L(H) + |U| if H has an edge (zero the u in U one at a time: f still
    depends on the next u, so a reader of x_u is eliminated each time; then L(H) remain), and
    >= |U| - 1 if H is edgeless.
  Families: `grest.py` (U empty) and `grest2.py` (all, with a threshold minL on the bound, which
  keeps the family Aut-invariant).

Validation (non-vacuity): for every graph, the U (star-cover) circuit of size Phi, put in lexbot form,
is accepted at s = Phi with all flags except viol (`mku.py`, `ulb.py`, `--fixc`). For Petersen also the
13-OR size-20 circuit of deg3.md is accepted (also with viol). `--lexbot` rejects the U circuit in a
non-lex-max labelling (sanity check). All SAT models are decoded and verified on all 2^n inputs.

## 2. The hierarchy (making the old conditional assumption unconditional)

Induced subgraphs of P that are not pseudoforests, up to isomorphism: H7 = P - (path of 3 vertices)
(7 v, 8 e, Phi 11), H8a = P - edge (8 v, 10 e, Phi 13), H8b = P - non-edge (8 v, 9 e, Phi 12),
H9 = P - v (9 v, 12 e, Phi 16). Every induced subgraph on <= 6 vertices, and every 7-vertex one other
than H7, is a pseudoforest (checked in plib.py/grest.py). Each level is proved with the levels below.

## 3. Runs and results

All solver times are wall-clock on a shared 4-core machine. Sizes s <= 4 are trivially UNSAT at every
level (some restriction demands more surviving gates than s; the encoder then emits an empty clause).

### 3.1 Hierarchy levels

| graph | Phi | sizes | result | certificate |
|---|---|---|---|---|
| H7 = [01,05,16,24,46,63,35,52] | 11 | s=7..10 (`rest_H7.json`, factc, viol) | UNSAT (s=10: 68.5 s pysat) | DRAT, s=5..10 kissat + drat-trim VERIFIED |
| H8b = P - {0,2} | 12 | s<=11 (`rest_H8b.json`, uses H7) | UNSAT (s=11: 0.4 s) | DRAT s=5..11 VERIFIED |
| H8a = P - {0,1} | 13 | s<=11 (`rest_H8a.json`); s=12 (`rest2_H8a.json`, lexbot) | UNSAT (s=12: 243.6 s pysat) | DRAT s=5..12 VERIFIED |
| H9 = P - 0 | 16 | s<=14 (`rest2_H9.json`, lexbot, uses H7/H8a/H8b) | UNSAT (s=13: 7.7 s, s=14: 3292.9 s pysat) | no DRAT yet |
| H9 | 16 | s=15 monolithic | TIMEOUT (pysat 5400 s; kissat 5400 s) | |
| H9 | 16 | s=15 cube-and-conquer | see 3.3 | |

Non-vacuity at s = Phi (U circuit in lexbot form, all flags except viol): SAT for H7 (also found
unconstrained at s=11 in 7.5 s), H8a, H8b, H9 and P (both `rest2_P_noH9.json`; P also accepts the
13-OR circuit with viol).

**PROVED (modulo the cited theorems and solver correctness; DRAT-certified):** C(f_H7) = 11,
C(f_H8b) = 12, C(f_H8a) = 13 (upper bounds: U circuits). The H7 value was open in sat19/README.md.

### 3.2 Petersen, unconditional family (`rest2_P_noH9.json`: pseudoforests + H7/H8a/H8b + U-singletons, minL 8)

| s | result |
|---|---|
| 1..14 | UNSAT (s=14: 7.4 s) |
| 15 | UNSAT (559.1 s pysat) |
| 16 | TIMEOUT (no result after ~1 h; a parallel kissat run stopped after 46 min) |

So **C(f_P) >= 16 unconditionally** (UNSAT, not yet DRAT-certified for s=15). Earlier (first try,
weak family `rest_all.json` = pseudoforest restrictions only) s=15 did not finish in 600 s.
