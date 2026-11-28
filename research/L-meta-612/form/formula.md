# Formulas for f_G: what the 2-slice can and cannot prove

Status: **the full formula bound is NOT proved**, neither for C4-free graphs nor for girth >= 5.
This round settles which proof techniques can work and supplies exact data. Labels:
PROVED (proof given here), DATA (exact machine computation, scripts in this folder),
REFUTED (explicit instance, checked exhaustively).

Notation: a formula is a tree of fan-in-2 AND/OR gates whose leaves are variables (repetition
allowed). L = number of leaves = size + 1. Target: **size >= Phi = |E| + tau − 1, i.e. L >= |E| + tau**.
The *2-slice* D2 is the set of inputs of weight 1 or 2. A function g *2-separates* G if
g(e_u) = 0 for all u, g(e_u + e_v) = [uv ∈ E], and g is arbitrary on weight >= 3. Write L2(G) for
the minimum number of formula leaves over all monotone 2-separating g. Then L2(G) <= L(f_G).

Every notion used so far (S_p, E_p, junk pairs, Fact C, w(p), N1–N3, Lemma P, Proposition F,
Theorem S) is a function of the gate's values on D2 alone. **Any argument built only from these
notions proves a lower bound on L2, not only on L(f_G).** That is why L2 is the right test.

## 1. Main negative result: triangles defeat every 2-slice argument (REFUTED)

**Net** N (triangle 345, pendant edges 04, 15, 23; |E| = 6, tau = 3, Phi = 8):

    g = (x0 | x3 | x5) & (x4 | ((x1 | x3) & (x2 | x5)))      7 gates, 8 leaves

g is correct on all of D2 (`fdp.c`, checked exhaustively), but g(e0+e1+e2) = 1 on the independent
set {0,1,2}. So **L2(net) = 8 < 9 = Phi + 1**. The real minimum formula for f_N has 9 leaves
(DATA, exact full-domain search), so the net does not refute the claim.

Consequences (PROVED, given the instance):
* No proof that uses only weight <= 2 inputs can give size >= Phi on C4-free graphs with
  triangles, even for formulas, and so not for circuits either (formulas are circuits). Such
  proofs include w-potentials with any junk term, Fact-C/centre counting and STAR-ALL charging.
  Any proof for triangle graphs must use some input of weight >= 3.
* Mechanism: the inner rectangle {1,3}x{2,5} creates the path 1-5-3-2 together with the junk
  pair 12. The gate x0|x3|x5 kills 12 "for free", because it is also the leaf set {0,3,5} of the
  star at 4, and 3,5 ∈ N(4) lie on the rectangle. That needs the triangle 345.
* DATA: the net is the only failure among the 43 C4-free graphs on <= 6 vertices. On 7 vertices
  there are exactly 4 failures among the 73 C4-free graphs (all contain a net, `sw_slice7.jsonl`).
  For three of them the 3-slice (inputs of weight <= 3) already gives L = |E| + tau, so minimum
  formula size = Phi (`sw_tri7_s3.jsonl`). Weight 3 suffices there. The fourth,
  [01,04,12,16,23,34,35,45,56], overflowed the 150M-state table at 12 leaves and is UNCHECKED.
* Literature fit: Jukna's formula bound (On graph complexity, Thm 7.3) is a graph-complexity
  (2-slice) argument and assumes triangle-free *and* C4-free. The net explains why.

## 2. Girth >= 5: the 2-slice is tight on all data (DATA)

Exact minimum-leaf search over all 2-separating formulas (`fdp.c`, level-by-level enumeration of
all functions on D2, bit-vector lattice):

| class | graphs | L2 = |E| + tau |
|---|---|---|
| C4-free, <= 5 vertices (with triangles) | 17 | 17 |
| girth >= 5, 6 vertices (incl. C6, P6, trees) | 12 | 12 |
| girth >= 5, 7 vertices (incl. C7) | 25 | 25 |
| girth >= 5, 8 vertices | 49 of 66 run | 49 (the other 17 were not run: CPU limit) |

So, for girth >= 5, it is consistent that the formula bound is a pure 2-slice (graph-complexity
with singletons) statement. Because L(f_G) >= L2(G) and the U formula gives the upper bound,
**L(f_G) = |E| + tau exactly (minimum formula size = Phi)** for every graph in the table, and for
the net (9).

## 3. Why bottom-up potentials cannot work even for formulas (PROVED)

t10's Heawood node p = OR(points) ∧ OR(lines) is itself a formula. It has 13 gates and
w(p) = 20. So no potential Ψ that depends only on the node's function and satisfies
Ψ(p) >= w(p) can satisfy Ψ(p) <= size(subformula). Fan-out 1 does not help a bottom-up
potential: the junk created at p is paid only by its context, the killers above p. A working
measure must depend on the context. The natural framework is the Karchmer–Wigderson top-down
one: each node carries a requirement (X; Y), where X is the set of edges it must accept and Y the
down-closed set of singletons and non-edges it must reject. The root has (E; all).

## 4. A top-down measure: what is proved, what fails

For a requirement (X; Y = (Y_s, Y_n)) classify an edge by how many endpoints lie in Y_s
(type 2, 1 or 0). Let F be the set of non-Y endpoints of type-1 edges. Define

    mu'(X;Y) = |X_2| + min{|T| : T ⊇ F, T covers X_0 ∪ X_2} − D(X;Y),

where D is the maximum of Σ (|H_i| − max side of H_i) over edge-disjoint bipartite subgraphs H_i of X_2
all of whose cross non-edges are missing from Y_n.

* PROVED: mu'(root) = |E| + tau for every C4-free G. D = 0 there, because a free bipartite
  pattern is complete bipartite inside G, hence a star.
* PROVED: mu' <= 1 at leaves, and mu' is subadditive at OR splits (D is superadditive in X).
* PROVED: mu' is subadditive at an AND split whenever no child certificate uses a junk pair
  killed by the sibling (in particular when K := Y_s1 ∩ Y_s2 = ∅). The proof takes
  T = T1 ∪ (T2 ∩ V_O(BO)), or its mirror, plus the rectangle A x B, which is free.
  Every junk-kill creates such a pair inside K, so this case is exactly the clean
  formulas. It reproves Proposition F(iii) by a different route.
* DATA: the AND step holds on every down-closed split, exhaustively, for P4, P5, C5, K_{1,4}, the
  spider, K3, the paw and two triangle graphs on 5 vertices. It also holds on 1,500 to 3,000
  random states of every girth >= 5 graph on 6 and 7 vertices (`meas.py`, `meas2.py`, `m2all.log`).
* REFUTED (net): the AND step fails at the root split of the 8-leaf 2-slice formula
  (9 > 3 + 5), as it must.
* **REFUTED (tree, 8 vertices): mu' is not a lower bound on the requirement complexity.**
  Take G = edges kb, bb', b'k', a1b, a1c1, a2b', a2c2, with Y = all singletons and all non-edges
  except the four A x B non-edges. Then mu' = 11, but r ∧ s with r = x_b|x_b'|x_c1|x_c2 and
  s = x_a1|x_a2|((x_k|x_b')&(x_b|x_k')) meets the requirement with 10 leaves. The junk kk' is
  created and killed inside the subformula. A correct measure needs a *recursive* junk
  credit, not one-level rectangles. Whether such a state is reachable from the root is open.

## 5. Comparison with the literature

The claimed bound gives L >= |E| + tau, which is stronger than Jukna's L >= |E|/2 (Disproving the
single level conjecture, Thm 5, and On graph complexity, Thm 7.3). There is no contradiction:
all data has L = |E| + tau. Note that Jukna's triangle-free hypothesis matches §1: for graphs
containing a net, graph-complexity (2-slice) methods provably lose at least 1. For girth >= 5
the exact constant is open even for formulas. Proving it needs a 2-slice measure with recursive
junk credit (§4), or a weight-3 argument.

## 6. Files

`fdp.c` (exact min-leaf formula search over a generated bit-vector lattice; DUMP mode lists all
functions), `drv.py` (modes slice / slice3 / full), `sweep.py`, `sweepf.py`, `geng5.py` (girth-5
graph generator), `req.py`/`cmpL.py` (exact requirement complexities, C5), `meas.py`/`meas2.py`
(measure tests), and the logs `sw_*.jsonl`, `m2all.log`, `m2tri.log`.

Not done: unfolding the t3–t10 pool circuits into formulas. That test is uninformative here,
because every rectangle in the corpus is a forest, so Proposition F already covers the unfolded
trees. Petersen-v was not run either: its 2-slice search space is too large for `fdp.c` at
16+ leaves.
