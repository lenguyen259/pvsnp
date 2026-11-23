# Lemma E*: status after e612

**Bottom line.** E* as stated in `p612/argument.md`, which covers every monotone circuit without
constant or copy gates, is **FALSE**. The smallest counterexample found is on the net N, with
6 vertices and a circuit of size Phi+1 = 9. Two weakenings survive every test, and each one
still implies the claim:

* **E\*_opt**: E* for minimum-size circuits only.
* **E\*+**: E* where restriction R is followed by functional reduction R+.

A sub-case of E* is proved rigorously (Theorem A below). It does not need C4-freeness. No full
proof of E*_opt or E*+ is given. Everything marked "data" is a machine check, not a proof.

Notation: `C` is a circuit of fan-in-2 AND/OR gates over x_0..x_{n-1}. e_a is the unit vector
of vertex a. F_a is the number of gates that read x_a. deg is degree in G.
need(v,0) = Phi(G) - Phi(G-v), and need(v,1) = Phi(G) - Phi(G_1), as in argument.md.

## 1. Counterexample to E* (as stated)

Take the net N: the triangle {3,4,5} with pendant edges 0-4, 1-5 and 2-3. Then
E = {04, 15, 23, 34, 35, 45}, tau = 3 and Phi = 8. Consider the circuit

    6=x1|x3  7=x2|x5  8=6&7  9=x4|8  10=x0&9  11=x3|x5  12=x4&10  13=9&11  14=12|13

It has 9 gates and computes f_N. Check:
* 8 accepts the pairs 12, 15, 23 and 35.
* 13 = (x4|8)&(x3|x5) gives 34, 45 and 8&(x3|x5), so the junk pair 12 is killed.
* 12 = x4&x0&(x4|8) = x0x4.

The circuit has no constant gates, no copy gates, and no two nodes computing the same function.
Its only minimal AND gate is 8 = OR{1,3} & OR{2,5}. Elimination by rule R:

| v | elim(v,0) | need(v,0) | elim(v,1) | need(v,1) |
|---|---|---|---|---|
| 1 | 1 | 2 | 2 | 3 |
| 2 | 1 | 2 | 2 | 3 |
| 3 | 2 | 4 | 4 | 6 |
| 5 | 2 | 4 | 4 | 6 |

So no v in A∪B = {1,2,3,5} works, and E* fails. L6 still holds via (0,0), (4,0) and (4,1).

Data on how common this is:
* Exhaustive star-free enumeration on N at size 9 found 42 such circuits (`r5_6_1_nostar.txt`),
  36 of them with no duplicate node functions.
* General enumeration on N at size 9 found 37 failures in the first 30,000 circuits
  (`r_net_1.txt`).
* There is no failure at size Phi+1 on <= 5 vertices (caps of 20,000) or at Phi+2 on <= 5
  vertices (`r7p_5_2.txt`, caps of 20,000). So N at Phi+1 is the smallest instance found.

**Lesson.** The circuit is wasteful: the gates 10 and 12 compute x0x4 with an extra gate, and that
waste absorbs the elimination. Any proof must therefore use optimality, or a strong reduction
rule. The local normal forms "no constants, no copies, no duplicate functions" are not enough.

## 2. Two repaired statements, both implying the claim

**R+ (functional reduction).** After substituting x_v := b, replace every gate whose function
(on all 2^n inputs, with x_v fixed) equals a constant or the function of an earlier node by that
node. Then delete the gates that no longer reach the output. The result is a circuit for
f restricted to x_v=b, and it is at least as small as the circuit R produces. A script rebuilds
and evaluates the reduced circuit on every input, for all 42 failures above.

**Lemma E\*+.** Same statement as E*, with "restriction R eliminates" replaced by "restriction R
followed by R+ eliminates".

**Lemma E\*_opt.** Same statement as E*, but only for minimum-size circuits computing f_G.

**Implication (spelled out).** Suppose the claim fails, and pick a counterexample G with |V|+|E|
minimal. Let C be a minimum-size circuit for f_G, with s = size(C) < Phi(G). First remove
constants. Since C is minimum, it has no constant gates, no copy gates and no duplicates. Now
apply E*_opt (or E*+). This gives a v and b such that the reduced restricted circuit C' computes
f_{G_b} and has size s' <= s - (Phi(G) - Phi(G_b)).

* If b = 0, then G_0 = G - v is smaller, so s' >= Phi(G-v) by minimality.
* If b = 1, then C' computes f_{H,F} with H = G - N[v] and F = N(v). By Fact F of argument.md
  (each forced variable set to 0 removes at least one gate), together with minimality on H,
  s' >= |F| + Phi(H). If H has no edges, s' >= |F| - 1. That bound is Phi(G_1).

In both cases s >= s' + Phi(G) - Phi(G_b) >= Phi(G), a contradiction.

Either lemma is enough for the claim. E*+ is the more useful target to test, because it can be
checked on circuits larger than the minimum.

## 3. Rigorous partial results (valid for any graph G; C4-freeness not used)

Let C have minimum size for f_G, where G has an edge.

**(O) Normal form.**
* (O1) Every gate reaches the output.
* (O2) No node computes a constant: with no constant inputs, every gate is 0 at 0^n and 1 at 1^n.
* (O3) No two nodes compute the same function. If p precedes q and both compute the same
  function, redirect the readers of q (and the output mark) to p. Then q is dead, which
  contradicts minimality. In particular no gate reads the same node twice.
* (O4) Every variable that C reads is relevant. Otherwise, setting it to 0 leaves f unchanged
  and turns its reader into a copy or a constant, which gives a smaller circuit.

**Lemma 1.** Under x_a := 0 with rule R:
* every gate that reads x_a is eliminated, because it becomes the constant 0 or a copy;
* every gate that reads a node which became the constant 0 is eliminated as well.

**Lemma 2 (R_a).** Let R_a = {nodes p : p(e_a) = 1}. Suppose x_a has exactly one reader, the
gate g = x_a & y with y(e_a) = 0. Then R_a = {x_a}. Consequently N(a) ⊆ B, where y computes OR_B.

*Proof.* Induct in topological order. Each input x_u with u ≠ a has value 0 at e_a. The gate g
has value y(e_a) = 0 at e_a. Any other gate reads neither x_a nor a node of R_a, so its value at
e_a is 0. By Fact C, each edge ac is created at an AND gate h1 & h2 with h1(e_a) = 1, h2(e_c) = 1
and h2(e_a) = 0. Then h1 ∈ R_a forces h1 = x_a, so the gate is g, and h2 = y gives c ∈ B. ∎

**Theorem A (center rule).** Let g = x_a & y be a minimal AND gate with y = OR_B and a ∉ B. Let T
be the set of OR gates of the OR-only subcircuit computing y. Assume either
* (A1) F_a >= deg(a), or
* (A2) F_a = 1, and every gate of T has all its readers in T ∪ {g}.

Then x_a := 0 eliminates at least need(a,0) gates.

*Proof.* First, need(a,0) <= deg(a) + 1, because tau(G-a) >= tau(G) - 1. This holds whenever
G - a has an edge.

If G - a has no edges, then G is a star centred at a, need(a,0) = Phi(G) = deg(a), and the
output becomes the constant 0. All s gates are then eliminated, and s >= deg(a) because C reads
deg(a) + 1 variables.

Otherwise g is not the output, since otherwise G would be a star. So g has a reader s1. By (O3),
s1 does not read x_a: the gate x_a|g equals x_a and the gate x_a&g equals g. Under x_a := 0:
* every reader of x_a is eliminated (Lemma 1), and g is one of them;
* s1 reads the constant g = 0, so s1 is eliminated too.

This gives at least F_a + 1 eliminated gates.
* (A1) F_a + 1 >= deg(a) + 1 >= need(a,0).
* (A2) Every gate of T now feeds only dead gates, so all of T is deleted. T reads only inputs
  in B ∌ a, so T is disjoint from the gates already counted. T has at least |B| - 1 gates.
  The total is at least 2 + |B| - 1 >= deg(a) + 1 by Lemma 2. ∎

Theorem A covers the good-leaf case: g = x_a & x_b with F_a = 1, which makes a a leaf.

Coverage (data, `t6.py`; the script also asserts that the theorem's conclusion holds):
* Theorem A applies to some gate in 700 of the 725 minimum circuits on <= 5 vertices.
* Exceptions: paw 3, bull 12, P4 with a pendant 1, and [(0,4),(1,4),(2,3),(2,4),(3,4)] 9.
* In the exceptions, typically F_a = 2 < deg(a) = 3. The third edge at a is created by a killer
  AND gate above g.
* There the center is still good, according to the data, but Theorem A does not prove it.

## 4. Data for the refined lemmas (all zero failures unless stated)

* E* at size Phi (minimum circuits):
  - all circuits on <= 5 vertices;
  - 25 of the 26 graphs on 6 vertices (caps of 3,000; `r_6_0.txt`);
  - star-free circuits exhaustively on <= 6 vertices: 1 on the bull, 21 on the net and 6 on
    [(0,3),(0,4),(1,4),(2,4),(3,4),(3,5)];
  - 27 graphs on 7 vertices with <= 7 edges (caps of 400; `r7_0.txt`). 10 graphs timed out
    and the rest were not reached.
* Rule S held in every circuit examined (Phi and Phi+1 on <= 5 vertices, Phi on 6 vertices,
  Phi on 7 vertices). Rule S: every minimal AND gate x_a & OR_B with a ∉ B contains a good vertex
  in {a} ∪ B. The center a alone is NOT always good: it fails in minimum circuits of the net
  whenever the OR-tree for B is shared.
* E*+ at size Phi+1 or larger, zero failures. Plain E* fails in each of the following, and E*+
  repairs every case:
  - net at Phi+1: 37 failures of 30,000;
  - net at Phi+1, star-free: 42;
  - net at Phi+2, star-free: 351 failures of 30,000. Here even L6 with R fails (4 circuits),
    so no vertex anywhere works under plain R;
  - two 7-vertex net extensions (net+3-6 and net+4-6) at Phi+1, star-free: 73 of 9,687 and
    86 of 12,823 (`r_net7.txt`);
  - also tested, with no E* failures: net+0-6 at Phi+1, and the bull, star-free, at Phi+1
    through Phi+3 (50,000 cap).

## 5. Smallest open lemma (refined)

**E\*+ (open).** Let G be C4-free with an edge, and let C be any monotone circuit for f_G. Then
some minimal AND gate g = OR_A & OR_B, some v ∈ A ∪ B and some b satisfy
size(R+(C|x_v=b)) <= size(C) - (Phi(G) - Phi(G_b)).

It splits into:
* (S) the star case, which Theorem A settles when F_a >= deg a, or when F_a = 1 and the tree is
  private; still open: shared OR-trees, and 2 <= F_a < deg a;
* (Q) star-free circuits, where every minimal AND is a rectangle or overlaps. This is where the
  net counterexample to plain E* lives. Minimum star-free circuits exist only for "tie" graphs
  such as the bull and the net.

If E*+ itself fails, the fallback is E*_opt. Any proof of E*_opt must use global minimality,
because of Section 1.
