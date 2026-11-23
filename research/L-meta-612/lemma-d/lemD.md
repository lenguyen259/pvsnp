# Lemma D: what is proved, and the exact remaining gap

Labels: PROVED (a full proof is given here, or the statement is the accepted Lean file L_meta_599),
DATA (machine check only).

Notation is as in or-bound/or.md:
* C is reduced, monotone and fan-in 2, and computes f = f_G.
* G is C4-free with min degree delta >= 2.
* core(q) = {v : q <= x_v}.
* The charge set of an OR gate g = a|b is core(a) ∪ core(b).
* ch(v) = #{OR gates g : v in chargeset(g)}.
* v is *single-charged* if ch(v) = 1. release_exists gives ch(v) >= 1, because G - v has an edge.
* V2 = the vertices of degree 2. H = the vertices of degree >= 3.

Scripts in this folder:
* `base.py`: cache of the 23,056 reduced min-degree->=2 circuits, with Boolean semantics.
* `t1.py`-`t8.py`: candidate tests.
* `sat_*.txt`: the SAT runs.

## 1. Tools (PROVED)

**L1 (multi-vertex changed-domination).** Fix a vertex set S, and let P be the set of all OR gates
charged by some v in S. Suppose x and y agree outside S and agree on every gate of P. Then
f(x) = f(y), provided that for every v in S some accepted z has z_v = 0.

*Proof.* This is the Lean `changed_dominated` induction, with "j = p" replaced by "j in P". Take a
wire on which x and y differ. Either it is <= x_v for some v in S, or the difference passed through
an OR gate whose differing input is <= x_v. Such a gate is in P, and x and y agree there. So if the
outputs differed, the output would be <= x_v, which contradicts "free". ∎

For S = {v} with P = {g}, this gives the **bottleneck property BN(v, g)**: if g(x) = g(x ⊕ v),
then f(x) = f(x ⊕ v). A single-charged v satisfies BN with its unique gate g_v. BN survives
restricting any other variables to constants.

**L2 (set restriction).** Setting x_X := 0 removes at least |Q_X| OR gates, where Q_X is the set
of OR gates charged by some vertex of X. *Proof:* restrict one vertex at a time. A gate charged by
w in X keeps a dominated input <= x_w until x_w is set. ∎

So (OR) would also follow from finding a nonempty X with |Q_X| >= e(X), the number of edges meeting
X. The test candidates for this were abandoned (§4).

**L3 (dominated chain).** If q1 ∧ q2 <= x_v, then q1 <= x_v or q2 <= x_v. Suppose v is
single-charged with gate g_v = a_v | b_v, where a_v <= x_v. Then a_v is x_v itself, or
a_v = x_v ∧ r_1 ∧ ... ∧ r_m, an AND chain whose side inputs r_i all lie below a_v.

*Proof.* A monotone function with a minterm avoiding v is not <= x_v. If both q1 and q2 had such
minterms, their union would be a true point of q1 ∧ q2 without v. An OR gate below a_v that is
<= x_v would be a second charged gate of v. ∎

## 2. Local structure of single-charged vertices (PROVED)

**L4 (BN at a minimal OR gate).** Let g = x_A | x_B be a minimal OR gate, with A and B incomparable,
and let BN(v, g) hold with deg v >= 2. Then one of the following holds:
* (i) v is in A \ B and A = {v}. Moreover, if B is independent, then v ∉ N(B), N(v) ⊆ N(B) and
  |B| >= deg v. The symmetric case has v in B \ A and B = {v}.
* (ii) deg v = 2 and {A, B} = {{v,u}, {v,w}}, where N(v) = {u, w}.

*Proof.*
* Fix u in N(v). Then f({u,v}) = 1 and f({u}) = 0, so g({u,v}) = 1 and g({u}) = 0.
* If v is in A \ B, then B ⊆ {u,v} would force B ⊆ {u}, which is impossible. So A ⊆ {u,v}.
  Doing this for two neighbours gives A = {v}.
* If v is in A ∩ B, then neither A nor B is {v} (they are incomparable). So each neighbour u gives
  A = {v,u} or B = {v,u}, and therefore deg v <= 2.
* In case (i), g(T + v) = 1 for every T, so f(T + v) = f(T) for every T ⊇ B. Take B independent.
  T = B gives v ∉ N(B). T = B + u gives u in N(B). Each b in B sees at most one neighbour of v
  (two would give the 4-cycle v-u-b-u'). ∎

**L5.** In every minimal OR gate, at most one vertex of the support S = A ∪ B is single-charged.

*Proof from L4.* If v is in A ∩ B, the others are in A Δ B with |A|, |B| = 2. Otherwise A = {a} and
B = {b} would both be single-charged, and then |B| = 1 >= deg a >= 2. ∎

This strengthens pay_core, which gives one vertex with ch >= 2. DATA check: 50,395 (gate, support)
pairs; every single-charged vertex found is case (i) with B spanning an edge.

**L6 (type R).** Let v be single-charged with deg v >= 2, and suppose a_v ≠ x_v. Then for every
u in N(v), some OR gate charged by u lies strictly below g_v.

*Proof.*
* By L3 and reducedness, some side input r has r(v) = 0, while r({u,v}) = 1 for all u in N(v).
  These values come from BN applied with T = {u}.
* Let r' = r|_{x_v=1}. It depends on x_u, and r' is not <= x_u because r'({w}) = 1 for the other
  neighbour w.
* The release argument, applied to the subcircuit of r with x_v := 1, gives an OR gate with an
  input q for which q|_{v=1} <= x_u. By monotonicity, q <= x_u. ∎

DATA: 19,980 type-R instances, 0 failures.

**Corollary L7.** Two adjacent single-charged vertices of degree >= 2 cannot both be of type R.
Each one's gate would lie strictly below the other's.

## 3. New cases of Lemma D (PROVED)

**Theorem F.** Lemma D holds for every C4-free G with delta >= 2 and at most one vertex c of
degree >= 3. Examples: the bowtie, every friendship graph F_k, and bouquets of cycles of lengths
other than 4 at one vertex.

*Proof.*
* Here delta = 2, so we need a degree-2 vertex with ch >= 2.
* Take a minimal OR gate g = x_A | x_B. Its support S satisfies |S| >= 2.
* If S contains two degree-2 vertices, L5 makes one of them good.
* Otherwise S = {v, c}. Case (ii) needs |S| = 3. In case (i), A = {v} and B = {c} is independent
  of size 1 < 2 = deg v.
* So v is not single-charged, and ch(v) >= 2 = deg v. ∎

**Corollary.** (OR) #OR >= |E| - 1 holds for every C4-free graph with at most one vertex of degree
>= 3. Theorem R in or.md applies because this class is closed under subgraphs. In particular, the
SAT runs for bowtie at Phi+3 and F3 are no longer needed: Lemma D is proved there at every size.

**Corollary M.** If delta = 2 and some minimal OR gate of C has two degree-2 vertices in its
support, then Lemma D holds for C. DATA: this covers every data circuit except 1,185 bowtie
circuits, and Theorem F covers those.

## 4. Abandoned candidates (DATA counterexamples)

* "Every min-degree vertex is good": fails on the triangle (3,438 circuits), e.g. 3=0|1, ...
* "Some vertex of degree >= 3 is good": fails on 7,640 bowtie circuits and on all 29 triangle+C5
  circuits.
* **Edge-set version** "∃ edge uv with |Q_{uv}| >= deg u + deg v - 1": fails on the triangle
  (3,647 circuits; smallest), the bowtie (174) and two disjoint triangles (312).
* **High-set version** "|Q_H| >= e(H)", which would reduce to the Lean pseudoforest result: fails on
  the bowtie at Phi. In `5=0&1 6=2&3 7=2|3 8=0|7 9=1|8 10=4&9 11=5|6 12=10|11` we get
  Q_{4} = 1 < 4.
* "Every minimal OR gate contains a good vertex": fails on 4 triangle+C5 circuits, because of the
  minimal gate x2|x3 inside H.
* "Σ ch/deg >= n": fails on most circuits.

Still unrefuted (DATA):
* Some min-degree vertex is good.
* Every minimal OR gate containing a min-degree vertex contains a good min-degree vertex.

## 5. Exact remaining gap

Lemma D is open in two cases.

**(a) delta = 2 and |H| >= 2.** Smallest cases: triangle+C5 [02,05,12,13,23,34,45] and two
triangles + bridge, both with H an edge. L4 and L5 leave exactly these configurations for a
minimal gate in which every degree-2 vertex is single-charged:
* S ⊆ H (e.g. x2|x3);
* A = {v} with B ⊆ H spanning an edge (e.g. x1 | x2x3);
* A = {v} with B ⊆ H independent, |B| >= 2 and N(v) ⊆ N(B);
* x_v x_u | x_v x_w with u, w in H.

A global argument is needed. L6 and L7 are the pieces available: type-R vertices push charged gates
of their neighbours below them. Type-X vertices (g_v = x_v | b_v) have no analogous "below" lemma.
For them the u-charged gate that fires on ({u,v}, {v}) can sit anywhere.

**(b) delta >= 3.** The tools give only ch >= 2 for one support vertex, since L4 uses only
single-charge. There are no data and no small instances. The smallest C4-free graph with delta >= 3
has 10 vertices (the Petersen graph). Smaller ones are impossible because ex(n, C4) < 3n/2 for
n <= 9.

## 6. SAT (dsat.py, at most 2 processes, timeout 5400 s)

See `sat_t5_x2.txt` (triangle+C5, Phi+2) and `sat_ttb_x1.txt` (two triangles + bridge, Phi+1).
Results (DATA):

| graph | Phi + X | result | time |
|---|---|---|---|
| triangle+C5 [02,05,12,13,23,34,45] | X = 2 | UNSAT: no circuit in which every v has ch(v) <= deg v - 1 | 1079 s |
| two triangles + bridge [01,02,12,23,34,35,45] | X = 1 | UNSAT | 874 s |

With these, Lemma D is SAT-verified for triangle+C5 through Phi+2 and for two triangles + bridge
through Phi+1. The bowtie and F3 runs were not needed, because Theorem F proves those cases at
every size.
