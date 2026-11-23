# L-meta-612: monotone circuit size of f_G for C4-free G

Status: NOT proved. No counterexample found; exhaustive machine evidence (SAT) for all
C4-free graphs on <= 6 vertices (triangles included) plus three 7-vertex triangle graphs.
The gap is isolated to one lemma (Lemma E*, Section 4). Two pieces of negative structure are
established (Section 3): any gate-elimination proof must choose the vertex from the
circuit, not from the graph.

## 0. Setting

- G = (V,E) a finite simple graph, C4-free (no 4-cycle as a subgraph), E nonempty.
- f_G(x) = OR_{uv in E} (x_u AND x_v).
- Circuit: a DAG of gates, each gate AND or OR of two earlier nodes (inputs or gates). Constant
  and copy gates are allowed but counted. size = number of gates.
- tau(G) is the vertex cover number. Phi(G) = |E| + tau(G) - 1 if E is nonempty, and Phi(G) = 0 if
  E is empty (the function is then constant 0).
- Claim (L-meta-612): every monotone circuit computing f_G has size >= Phi(G).

## 1. Rigorous facts

**U (upper bound).** Take a minimum cover T and assign each edge to an endpoint in T. Let N_t be
the set of other endpoints of the edges assigned to t, with d_t = |N_t| (skip any t with d_t = 0;
this cannot happen for a minimum cover). The circuit OR_t (x_t AND OR_{w in N_t} x_w) uses
sum_t (d_t - 1) ORs, |T| ANDs and |T| - 1 ORs. The total is |E| + |T| - 1.
Correctness: an edge uv lies in some term, and a true term contains an edge.

**R (restriction accounting).** Substitute x_v := b. Then repeat the following:
- AND(0,.) and OR(1,.) become constants.
- AND(1,y), OR(0,y) and op(y,y) become copies of y.
- Delete every gate that does not reach the output.
Each deleted gate is "eliminated". What remains is a circuit for f|_{x_v=b} of size s - elim.
(This is the counting used in all the experiments below.)

**F (forced variables).** Let f_{G,F} = f_G OR OR_{w in F} x_w. Then
f_{G,F}|_{x_a=0} = f_{G-a, F-a} for a in F. If f depends on x_a, some gate reads x_a, and that
gate becomes a constant or a copy, so elim >= 1. By induction on |F|:
size(f_{G,F}) >= size(f_{G-F}) + |F| - [E(G-F) empty].
So the forced-set generalisation is free. Write G_0 = G - v and G_1 = (G - N[v], F = N(v)), with
- Phi(G_0) = Phi(G - v),
- Phi(G_1) = |N(v)| + Phi(G - N[v]) if G - N[v] has edges, else |N(v)| - 1.
Lean shape: `lemma forced_zero (C : Circuit) (hC : C.computes (fGF G F)) (ha : a ∈ F) :
∃ C', C'.computes (fGF (G.delete a) (F.erase a)) ∧ C'.size + 1 ≤ C.size`.

**P (OR-prefix).** Let g be a minimal AND gate: no AND gate is an ancestor of g. Then each input
of g is an input variable or an OR-only subcircuit. It computes OR_A or OR_B, with A and B
nonempty, provided constant gates were first removed by R. Proof: induction over the DAG.

**C (edge creation).** For every uv in E there is an AND gate g = h1 AND h2 with h1(e_u)=1,
h2(e_v)=1, h1(e_v)=0, h2(e_u)=0 (up to swapping the roles of h1 and h2).
Proof: take a topologically first gate g with g(e_u+e_v)=1 and g(e_u)=g(e_v)=0; the output is
such a gate. If g = h1 OR h2, then some h_i(e_u+e_v)=1, and h_i <= g gives h_i(e_u)=h_i(e_v)=0,
which contradicts minimality. So g is an AND gate, and by minimality each h_i is 1 on e_u or on
e_v. Since g(e_u) = 0, not both are 1 on e_u. The same holds for e_v.
Corollary: E is covered by the rectangles (S1\S2) x (S2\S1) of AND gates, where S_i is the set
of singletons of h_i. If G is C4-free, a rectangle with both sides >= 2 contains a non-edge.
The circuit accepts that non-edge at g, so a later AND gate must kill it. This is exactly what
(x0|x2)&(x1|x3) avoids for C4, and why C4-freeness matters.

## 2. Machine evidence (pysat/CaDiCaL exact search, scripts mcsat.py and run*.py)

Encoding: s gates, each with a one-hot choice of an input pair, an AND/OR bit and all 2^n
truth-table rows. Every non-output gate is used. Consecutive independent gates are in lex order,
which is sound. Sanity check: C4 is found with 3 gates, and C4 plus a pendant edge with 5 gates.

1. **The claim holds on all 1+2+4+10+26 = 43 C4-free graphs without isolated vertices on
   <= 6 vertices** (run1.py; n6.txt). For each graph, no circuit of size Phi-1 exists (UNSAT)
   and one of size Phi exists. This includes every graph with triangles on these vertex counts:
   K3, the paw, the bull, the bowtie (Phi=8), K3+K2, K3 with pendants, and two triangles joined
   by an edge (Phi=10, 416 s).
2. 7 vertices (73 C4-free graphs; one.py, s7.txt, 900 s cap each): 46 graphs are UNSAT at
   size Phi-1, so the claim holds for them. These are all graphs with <= 6 edges and all with
   7 edges and tau <= 3, which includes many triangle graphs. The other 27 graphs timed out
   and are UNCHECKED: 7 edges with tau=4, and all graphs with 8 or 9 edges, including the
   windmill F3. No circuit of size Phi-1 was found anywhere.
3. **Split conjecture**, checked for all C4-free graphs on <= 5 vertices except the bowtie
   (timeout), over all circuits of size <= Phi+4 (run2.py):
   - no circuit with <= tau-1 AND gates exists;
   - no circuit with <= |E|-2 OR gates exists.
   So the conjecture #AND >= tau and #OR >= |E|-1 is consistent with the data.
   Caution: for general quadratic functions, AND gates that kill non-edges can beat single-level
   circuits. Amano and Maruoka (Algorithmica 2006) show an exponential gap in the number of AND
   gates, and Jukna (ECCC TR05-021) disproved the single-level conjecture. Those constructions
   use dense bipartite structure, and I could not check whether any of them is C4-free. Treat
   #AND >= tau as plausible but risky.

## 3. What a gate-elimination proof can and cannot look like (new, machine-checked)

Single-step lemma L6(C,v,b): restriction R with x_v := b eliminates >= Phi(G) - Phi(G_b) gates.
Then induction gives size >= Phi.

- (a) For every circuit of size Phi on <= 5 vertices (all of them enumerated: up to 431 per
  graph), on 6 vertices (up to 3000 per graph), and for every circuit of size Phi+1 on <= 5
  vertices (up to 7085 per graph), **some (v,b) satisfies L6** (run4/run5/run8).
- (b) **No vertex chosen from the graph alone works.** For C5 and for the bowtie, every vertex v
  fails L6 for both b on some optimal circuit (run6.py). For P4, K3 and others, no fixed pair
  (v,b) works for all circuits. So L6 in the form "for the chosen vertex v (leaf, minimum
  degree, hub, ...) there is b" is FALSE already for C5 and the bowtie. Any proof must choose v
  from the circuit. This explains why the project's girth-9 and good-leaf proofs need heavy
  case analysis.
- (c) **The circuit-based choice that survives the tests:** there EXISTS a minimal AND gate
  g = OR_A AND OR_B (Fact P) and some v in A ∪ B that satisfies L6 with a suitable b. This held
  for every tested circuit (size Phi and Phi+1 on <= 5 vertices, size Phi on 6 vertices). The
  same was true for EVERY minimal AND gate on <= 5 vertices, but not on 6 vertices; see (d).
  The stronger rule "v on the smaller side" holds for all optimal circuits but FAILS at size
  Phi+1. Example, K3: (x0|x1),(x0&x1),(x2&(x0|x1)),OR,(..)&(x0|x1).

- (d) **The rule "every minimal AND gate contains a good v" is FALSE.** Let N be the net: the
  triangle {3,4,5} with pendants 0-4, 2-3 and 1-5. Then |E|=6, tau=3 and Phi=8. N has optimal
  circuits that contain a non-clean rectangle gate:

      f_N = (x1 & x5) | ( (x3|x4) & ( x5 | ((x0|x3) & (x2|x4)) ) )      [8 gates]

  The rectangle {0,3}x{2,4} carries the junk pair 02. The triangle edge 34 lets the gate
  (x3|x4) do two jobs: it kills 02, and its AND with x5 creates 35 and 45. In 4 of the
  489 optimal circuits of N, no vertex of the rectangle gate is good (machine-checked). The good
  restrictions there are only (1,0) and (5,1), which come from the clean gate x1&x5. So
  **triangles do allow optimal circuits with C4-type rectangles**. They tie but do not beat the
  bound, and any normal-form proof assuming "all useful AND gates are clean stars" is wrong for
  triangle graphs.

- (e) **Why this trick only ties (rigorous for this template).** Consider a sub-circuit
  Q = OR_K & (x_X | (OR_A & OR_B)), with |A|, |B| >= 2, computing a quadratic C4-free piece.
  - Any vertex in K ∩ A is adjacent to all of B, so C4-freeness forces |K∩A| <= 1 and
    |K∩B| <= 1.
  - A vertex w in A∩B must lie outside K, and is then adjacent to all of K.
  - x_X contributes X x K, so |X| + |A∩B| <= 1 when |K| >= 2.
  - Hence the rectangle yields at most |A|+|B|-1 edges.
  - Cost: |A|+|B|+|K| gates. Edges: <= |K|+|A|+|B|-1. The piece contains the triangle
    x a* b*, so tau >= 2.
  - So cost >= |E| + tau - 1. Equality holds exactly when tau = 2, as in the net.
  This settles the one-level template. Deeper nesting, or sharing the killer between pieces,
  is not covered.

## 4. The smallest unproved lemma

**Lemma E\*.** Let G be C4-free with E nonempty, and let C be a monotone {AND,OR} circuit without
constant or copy gates computing f_G. Then THERE EXIST a minimal AND gate g = OR_A AND OR_B of C
(by 3(d), "for every minimal AND gate" is false), v in A ∪ B and b in {0,1} such that restriction R with x_v := b eliminates at least
Phi(G) - Phi(G_b) gates.

Here Phi(G) - Phi(G_0) = deg v + [tau(G-v) < tau(G)], and
Phi(G) - Phi(G_1) = |E| + tau(G) - |N(v)| - |E(G-N[v])| - tau(G-N[v]), with the empty-edge
conventions of Section 1.

E\* together with R and F implies the claim, by induction on |V| + |E|. Constant and copy gates
are first removed (this only lowers the size). Then pick g by Fact P and apply E\*. The
restricted circuit computes f_{G_0}, or f_{G_1}, which reduces to f_{G-N[v]} by F.

Evidence for E\*: Section 3(c), with zero failures. Evidence against: none found.
Partial cases one can try to prove first:
- (i) A ∩ B nonempty. Then g accepts the singleton w in A ∩ B, so a later AND gate must kill it.
- (ii) |A| = 1, A = {a}, a not in B. Then x_a := 0 kills g directly. One must still find
  deg(a) - 1 (+1) further eliminations among the gates fed by g or by the OR-prefix of B.
- (iii) |A|, |B| >= 2 and disjoint. By Fact C, the rectangle A x B contains a non-edge, which a
  later AND gate must kill.

Case (ii) with deg a = 1 is the project's good-leaf case.

Triangles: no special obstruction appears. K3 = maj needs 4 gates (12 optimal circuits, all
satisfying E\*). The windmill circuits c&OR(all) | OR(a_i&b_i), and the alternative
(c|M)&U with M = OR a_ib_i and U = OR of all leaves, both give exactly 4k = Phi. So triangles
create many optimal circuits (431 for the bowtie), and this, not a cheaper circuit, is the
difficulty. Degree-2 vertices: the C5 data shows that a fixed degree-2 vertex cannot be
eliminated universally, which is consistent with the project needing runs of 4 such vertices.

## 5. Files

- mcsat.py: SAT encoding (exists_circuit, enum_all).
- run1.py: claim check. Output in n6.txt.
- run2.py: AND/OR split check.
- run3.py: abandoned. one.py + g7s.txt: 7-vertex sweep. Output in s7.txt.
- run4.py to run8.py: L6 and E\* tests. Output in r8_*.txt.
