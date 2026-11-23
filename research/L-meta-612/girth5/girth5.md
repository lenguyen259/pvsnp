# L-meta-612 for girth >= 5: reduction to one normal-form lemma

Status: **NOT closed.** What follows is a complete, rigorous lower bound for every circuit in a
normal form called STAR-ALL, for any C4-free G (triangles allowed). It needs no induction and does
not use E*. The open part is the normalisation: some (or every) minimum circuit for f_G is
STAR-ALL. The data says every minimum circuit of every tested girth >= 5 graph is STAR-ALL.

Labels: **PROVED** means a full proof is given here. **DATA** means a machine check (scripts in
this folder) and nothing more.

Notation: for a node p, S_p = sing(p) = {u : p(e_u) = 1}. For an AND gate h = h1 & h2, write
S1 = S_{h1}, S2 = S_{h2}, and R_h = (S1 \ S2) x (S2 \ S1) for its rectangle.

## 1. Definitions

* **Clean**: no gate p and non-edge uv with p(e_u+e_v) = 1 and p(e_u) = p(e_v) = 0.
* **STAR-ALL**: every AND gate h = h1 & h2 satisfies all three of:
  - (N1) S1 ∩ S2 = ∅ (no singleton is carried through an AND);
  - (N2) S1 ≠ ∅ and S2 ≠ ∅ (no killer or filter gate);
  - (N3) S1 x S2 ⊆ E (clean at h).

**Lemma 0 (clean is local). PROVED.** C is clean iff R_h ⊆ E for every AND gate h.

*Proof.* (⇐) Take the topologically first gate p with a junk pair uv. By the argument of Fact C,
p is not an OR gate and is not an input. So p = h1 & h2 with u ∈ S1 \ S2 and v ∈ S2 \ S1, which
puts uv in R_p. (⇒) If uv ∈ R_h, then h(e_u+e_v) = 1 and h(e_u) = h(e_v) = 0. ∎

So STAR-ALL is the same as: clean, plus (N1) and (N2). It is exactly "clean, no junk singletons,
no killers". The U construction of argument.md is STAR-ALL.

**Lemma 1 (stars). PROVED, C4-free only.** In a STAR-ALL circuit, every AND gate h has one input
q_h with S_{q_h} = {c_h} and the other input p_h with L_h := S_{p_h} ⊆ N(c_h).

*Proof.* By (N1) and (N2), S1 x S2 is a complete bipartite graph between two disjoint nonempty
sets, and it lies in E by (N3). If both sides had size >= 2, E would contain a C4. ∎

If both sides have size 1, either orientation can be chosen.

## 2. Main theorem

**Theorem S (STAR-ALL bound). PROVED, C4-free G, any circuit (minimality not used).** If C is a
STAR-ALL monotone circuit computing f_G and E ≠ ∅, then size(C) >= |E| + tau(G) - 1.

*Proof.* Delete the gates that do not reach the output. This keeps STAR-ALL and does not
increase the size. Let m be the number of AND gates. Split the OR gates into:
* B2: OR gates whose two inputs both have nonempty S and with |S| >= 2;
* Z: OR gates with at least one input having S = ∅.

These classes are disjoint, so size >= m + |B2| + |Z|.

*(a) m >= tau.* Let uv ∈ E. Its Fact-C gate h has u ∈ S1 \ S2 and v ∈ S2 \ S1, so
{u, v} = {c_h, leaf}. Hence the centres {c_h} form a vertex cover, and
m >= |{c_h}| >= tau.

*(b) |B2| >= |E| - m.* For a centre c, let H_c be the AND gates with centre c, j_c = |H_c| and
N_c = ∪_{h ∈ H_c} L_h. By (a), E ⊆ ∪_c {c} x N_c, so Σ_c |N_c| >= |E|.

Define the S-cone of {p_h : h ∈ H_c} as follows. From an OR gate, step to each input with
nonempty S. Stop at nodes with |S| = 1, which are the leaves. AND gates have S = ∅ by (N1), so
they never occur in the cone.
* Each internal node has |S| >= 2. It has two S-children (a B2 gate) or one (an OR gate with
  one empty input).
* Its S is the union of its children's S.
* So N_c is covered by the leaves.

A spanning forest with j_c roots in which every node has at most 2 children has at most
j_c + #(2-child nodes) leaves. Hence |N_c| <= j_c + |D_c|, where D_c is the set of B2 gates in
that cone.

The sets D_c are pairwise disjoint. Suppose t ∈ D_c ∩ D_{c'} with c ≠ c'. Then
S_t ⊆ N(c) ∩ N(c') and |S_t| >= 2, which gives a C4 (c, c' ∉ S_t since u ∈ N(c) implies u ≠ c).
So |B2| >= Σ_c (|N_c| - j_c) >= |E| - m.

*(c) |Z| >= m - 1.* The nodes with S = ∅ are the AND gates and the OR gates whose two inputs
both have S = ∅. No input variable has S = ∅, and the output has S = ∅ because f(e_u) = 0.
* By (N2), no AND gate reads a node with S = ∅, so every reader of such a node lies in Z.
* Every non-output node with S = ∅ has a reader.
* Let z0 be the number of Z-gates with two empty inputs and z1 the number with one. Counting the
  links from empty nodes to their readers: 2 z0 + z1 >= (m + z0) - 1.
* So |Z| = z0 + z1 >= m - 1.

Summing (a), (b) and (c): size >= m + (|E| - m) + (m - 1) = |E| + m - 1 >= |E| + tau - 1. ∎

Corollary (PROVED). STAR-ALL circuits satisfy the split conjecture: #AND >= tau and
#OR >= |E| - 1.

Data check (`starall.py`, which asserts (a), (b) and (c) on every STAR-ALL circuit):
**all minimum STAR-ALL circuits are tight in each of (a), (b) and (c)** (slack (0,0,0,0)
everywhere).

## 3. Consequences for the plan in the task

**Reduction (PROVED).** For C4-free G, the claim size(f_G) >= Phi(G) is equivalent to:

    (NF) f_G has a minimum circuit that is STAR-ALL.

(⇐) is Theorem S. (⇒) holds because the U circuit is STAR-ALL of size Phi. So (NF) for all
girth >= 5 graphs is exactly what remains. The E* machinery (privacy of T, ATT, the trichotomy,
the forced-set induction) is no longer needed for the girth >= 5 route. It is only an alternative
way to use (NF).

The checks requested in the task, under STAR-ALL:
* **Minimal AND gates are stars. PROVED.** Every minimal AND gate is x_a & OR_B with a ∉ B and
  B ⊆ N(a) (Lemma 1, plus the fact that an OR-only node with S = {a} is x_a itself by (O3)).
  Overlaps are excluded by (N1). Rectangles with both sides >= 2 are excluded by C4-freeness.
* **ATT conditions (star.md §2): PROVED.**
  - "R_a has no AND gate" holds by (N1).
  - "h has no singletons and no junk pair" holds by (N1) and (N3).
  - The other two conditions are not automatic: they can fail when an OR reader of x_a is
    x_a | z with S_z = ∅, for example z an AND output. Theorem S makes them irrelevant.
* **Lemma 6 (shared tree): PROVED.** Case (i) is excluded by (N1), (ii) by (N3) and (iii) by (N2).
  So S2 (shared tree with F_a = 1) cannot occur in a STAR-ALL circuit.
* **Induction (proof.md §2).** It only needs SOME minimum circuit per graph, so choosing one with
  extra properties is legitimate. The class girth >= 5 is hereditary under G - v and G - N[v].
  With Theorem S, no induction is needed once (NF) is known.

## 4. Data (exact SAT enumeration of minimum circuits, CaDiCaL)

* girth >= 5 graphs on <= 6 vertices without isolated vertices: 22 graphs, all minimum circuits
  (`../s_case/circs`). **494 of 494 circuits are STAR-ALL.**
* girth >= 5 graphs on 7 vertices: 22 of the 25 graphs (`tf/circs`, cap 1500 circuits, 600 s per graph; every one of the 22 was enumerated exhaustively, below the cap). Over the 44 graphs on <= 7 vertices in `tf/circs`, **4229 of 4229 minimum circuits are STAR-ALL**, with zero slack in (a), (b) and (c). Timed out, so UNCHECKED: C7 (Phi = 10), [01,05,06,12,23,34,36,45] (Phi = 11) and [02,04,05,14,23,36,56].
* Over all graphs: no unclean circuit, no AND gate carrying a singleton, no killer, no
  minimal-AND overlap or rectangle. Every star orientation is A1, A2, or S1 with T private and
  ATT (`an.py`). So Theorems A/B also prove E*_opt on every tested girth >= 5 circuit.
* Contrast with C4-free graphs that have triangles (s_case): the 9 graphs net, bull and
  relatives have non-STAR-ALL minimum circuits (junk 408, junk+killer 119, singleton-AND 242;
  all tie Phi). Every graph has at least one STAR-ALL minimum circuit, as it must.

## 5. Exact remaining gap

**(NF5) Normal-form lemma, OPEN (DATA only).** If G has girth >= 5, every minimum monotone
circuit for f_G satisfies (N1), (N2) and (N3). A weaker statement is enough: some minimum circuit
does, or any circuit can be transformed into one that does with no size increase.

Facts about (NF5):
* It must use C4-freeness. For general quadratic functions, killers and junk do help
  (Amano–Maruoka; Jukna's refutation of the single-level conjecture).
* It must use triangle-freeness if it is stated for every minimum circuit, because the net has
  minimum circuits violating each of N1, N2 and N3.
* For C4-free graphs with triangles, the corresponding needed statement is the weaker "some
  minimum circuit is STAR-ALL", equivalent to the claim itself.

Suggested next step: a weighted extension of Theorem S. Charge each violation of N1, N2 or N3 to
extra gates, aiming at the inequality size >= |E| + tau - 1 for all clean circuits first (that is,
allow N1 and N2 violations). The counting step (c) is what breaks when an AND output has
S ≠ ∅, or when an AND reads an S = ∅ node.

Scripts: `glist.py` (graph list), `drive.sh`/`tdump.py` (enumeration), `starall.py` (STAR-ALL
check and the asserts of Theorem S), `an.py` (E* route statistics).
