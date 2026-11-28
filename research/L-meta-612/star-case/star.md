# Star case (S) of E*_opt: what is proved, what is data, what is open

Notation as in `estar/proof.md`. C is a minimum circuit for f_G (so O1-O4 hold), G is C4-free
with an edge. g = x_a & y is a minimal AND gate, y = OR_B is computed by the OR-only subcircuit T
(T is empty iff |B| = 1), and a is not in B. k = F_a is the number of readers of x_a, and r_g is the
number of readers of g. For a node p, sing(p) = {u : p(e_u) = 1}. The private closure P(T) is the
largest P ⊆ T such that every reader of a gate of P lies in P ∪ {g}. T is *private* if P(T) = T
(this is hypothesis A2 of Theorem A). need(a,0) <= deg a + 1 (proof.md).

Labels: **PROVED** means a full proof is given here. **DATA** means a machine check (scripts in this
directory) and nothing more.

## 0. Data (exact search, all minimum circuits)

Source: `dump.py` -> `circs/*.json`, see §5. Every minimum circuit (size Phi) was enumerated for
all 17 C4-free graphs on <= 5 vertices, and for 25 of the 26 C4-free graphs on 6 vertices (cap 2000
circuits per graph). Two 7-vertex net extensions were also enumerated (cap 1500 each). Classification is in `att.py`,
`an1.py`-`an9.py`, `l5.py` and `l6.py`. Every orientation of every star gate is classified as follows:

| class | meaning | (a,0) good | rule S |
|---|---|---|---|
| A1 / A2 | Theorem A applies | always | always |
| S1, abs(B) = 1 | g = x_a & x_b, 2 <= F_a < deg a | never (160 cases) | yes. **Every one is covered by the other orientation** (center b, with F_b = 1, which is A2) |
| S1, abs(B) >= 2 | 2 <= F_a < deg a | always on <= 6 vertices; fails in 25 cases on 7 vertices (§4(b)) | yes |
| S2 | F_a = 1, T shared | **never** (270 cases: net 31, net+36 121, net+46 118) | yes, through (v,1) for v in B |

Further observations, all DATA:
* In every S1 orientation with |B| >= 2, T is private. ATT (§2) holds in 6035 of 6060 cases, and
  in each of those Theorem B proves (a,0) good. A script asserts this on every case. The 25
  exceptions are §4(b).
* S2 occurs only on the net N and its extensions (6 vertices: 31 of 489 minimum circuits;
  7 vertices: 239 more), always with F_a = 1 and B = N(a). In every case, every v in the support S of a shared tree gate has (v,1) good. Example:
  `6=1|3 7=2|5 8=3|5 9=0|8 10=4&9 11=6&8 12=7&11 13=10|12`, with g = 10, a = 4, B = {0,3,5}, shared
  gate 8 = x3|x5 and S = {3,5}. Here elim(4,0) = 3 < 4 = need(4,0), while (3,1) and (5,1) are good,
  with elim 7 >= 6.
* The S2 circuits always contain a non-star minimal AND gate (an overlap or rectangle gate), so
  they lie inside the Q case as well.
* Every minimum circuit of a triangle-free graph is *clean*: no gate p and non-edge uv have
  p(e_u+e_v) = 1 with p(e_u) = p(e_v) = 0. Junk appears only on graphs with triangles.

## 1. Basic lemmas

**Lemma 3 (readers of x_a). PROVED.** For a node p, p(e_a) = 1 iff p >= x_a. Every reader of x_a
is x_a ∘ z with z(e_a) = 0. Consequently every reader of x_a that lies in R_a = {p : p >= x_a} is
an OR gate.

*Proof.* The first claim holds by monotonicity. If z(e_a) = 1, then z >= x_a, so x_a|z = z and
x_a&z = x_a. In both cases two nodes compute the same function, which contradicts (O3). An AND
reader x_a&z has value z(e_a) = 0 at e_a. ∎

**Lemma 4 (base count). PROVED.** Suppose g is not the output. Under x_a := 0 with rule R, the
following gates are eliminated and are pairwise distinct: the k readers of x_a, the r_g >= 1
readers of g, and the |P(T)| gates of P(T). So elim(a,0) >= k + r_g + |P(T)|.

*Proof.* Readers of x_a become constant or copies. g becomes the constant 0, so each reader of g
becomes the constant 0 (an AND) or a copy (an OR). A reader of g does not read x_a, because
x_a|g = x_a and x_a&g = g, which (O3) forbids. Gates of T read only B-inputs and T-gates, and a is
not in B, so they are neither readers of x_a nor readers of g (they lie below g). Process P(T) in
reverse topological order: each of its gates has all its readers in P(T) ∪ {g}, and those readers
are gone, so the gate no longer reaches the output and is deleted. ∎

**Lemma 5 (center obstruction; exchange). PROVED.** Let a be any vertex such that G - a has an
edge. Suppose that after x_a := 0 and rule R, some live node computes OR_{B'} (as a function with
x_a = 0), where ∅ ≠ B' ⊆ N(a). Then elim(a,0) <= 2 + deg a - |B'|.

*Proof.* Let C' be the reduced circuit: it computes f_{G-a} and has size s - e. Extend the node by
|N(a) \ B'| ORs to OR_{N(a)}, then add x_a & (that node) and OR the result into the output. This
computes f_{G-a} ∨ (x_a ∧ OR_{N(a)}) = f_G with s - e + |N(a)\B'| + 2 gates. Minimality of C gives
s <= s - e + deg a - |B'| + 2. ∎

*Use.* In S2, suppose a shared gate t = OR_S of T survives x_a := 0. Then (a,0) is provably bad
as soon as |S| > 2 - δ, where δ = need(a,0) - deg a. On the net, |S| = 2 and δ = 1, so the bound
elim <= 3 < 4 explains every S2 failure. Over the whole data set, `l5.py` checked the inequality
on 3808 (circuit, a, B') instances with no violation. It certifies 3781 of the cases where (a,0) is
bad. **So rule S cannot be proved through the center in S2. The good vertex must come from B.**

## 2. Sub-case S1 (2 <= F_a < deg a): closed under private T and attribution

**Hypothesis ATT(a,g).** For each c in N(a) \ B there is an OR reader p = x_a | z of x_a such that
∅ ≠ sing(z) ⊆ N(c).

**Theorem B. PROVED.** Let G be C4-free and C minimum. Let g = x_a & OR_B be a minimal star with
a not in B and T private, and assume ATT(a,g). Then elim(a,0) >= need(a,0).

*Proof.* If g is the output, G is a star and Theorem A applies. Otherwise define the map
c -> p_c of ATT on N(a) \ B.

*The map is injective.* Suppose c ≠ c' share p = x_a | z, and pick u in sing(z). Then u is in
N(c) ∩ N(c'), and so is a. Also u ≠ a, since z(e_a) = 0 by Lemma 3. Further c, c' ∉ {a, u}, since
c ∈ N(a) and u ∈ N(c). So a and u have two common neighbours, which gives the 4-cycle
a-c-u-c'-a. This contradicts C4-freeness.

*Counting.* Each p_c is an OR reader, and g is an AND reader. So |N(a) \ B| <= k - 1 and
deg a <= |B| + k - 1. By Lemma 4 with P(T) = T, and with |T| >= |B| - 1 (an OR of |B| variables
needs |B| - 1 gates),
elim(a,0) >= k + 1 + |B| - 1 >= deg a + 1 >= need(a,0). ∎

Remarks (PROVED):
* For k = 1, ATT is vacuous because N(a) ⊆ B by Lemma 2. So Theorem B contains Theorem A(A2).
* *When ATT holds automatically.* Let c ∈ N(a) \ B and let h = h1 & h2 be its Fact-C gate. Assume:
  - h1 ≠ x_a (otherwise h is a second star x_a & h2 at a; see §4);
  - R_a contains no AND gate;
  - every OR reader x_a|z of x_a has sing(z) ≠ ∅;
  - h has no singletons and accepts no non-edge pair.

  Then ATT holds for c. *Proof.* Each gate of R_a is an OR with an input in R_a, and the only input
  in R_a is x_a. So descending from h1 through R_a-inputs reaches a reader p of x_a in R_a, which is
  an OR reader p = x_a|z by Lemma 3, and h1 >= p. For u ∈ sing(z) we have h1(e_u) = 1, so u ≠ c (because
  h1(e_c) = 0) and h(e_u+e_c) = 1. Then h(e_u) = h(e_c) = 0 and cleanness give uc ∈ E. ∎
* Theorem B without the privacy hypothesis gives elim(a,0) - need(a,0) >= -|T \ P(T)|. **The only
  deficit is the shared tree gates.**

**S1, |B| = 1** (g = x_a & x_b). Either orientation with F = 1 is A2 with T = ∅ (PROVED, Theorem A).
An uncovered gate therefore needs F_a, F_b >= 2. If ATT holds for either orientation, Theorem B
closes it (PROVED). The remaining configuration (both F >= 2, ATT failing in both orientations)
never occurs in the data (DATA; all 160 cases with |B| = 1 have F_b = 1).

## 3. Sub-case S2 (F_a = 1, shared tree): structure only

**Lemma 6 (where a shared tree goes). PROVED.** Assume F_a = 1 and that g is clean, so B ⊆ N(a);
by Lemma 2, B = N(a). Let t ∈ T compute OR_S with |S| >= 2, and let t have a reader q ∉ T ∪ {g}.

*Setting up q\*.* Follow any path from t through q to the output. Not every gate on it is an OR,
since otherwise output >= x_s but f(e_s) = 0. Let q* = r & w be the first AND gate on the path,
with r >= t. Then q* ∉ T ∪ {g}: q is not in the cone of g, so neither are its ancestors.

*The trichotomy.* Exactly one of the following holds:
* (i) q* has a singleton, that is, sing(r) ∩ sing(w) ≠ ∅. This is junk, and a later AND must kill
  it.
* (ii) q* accepts a non-edge pair from sing(r) × sing(w).
* (iii) sing(w) = ∅, so q* <= w is a filter or killer on a singleton-free function.

*Proof.* Suppose (i) and (ii) both fail and w0 ∈ sing(w). Then w0 ≠ a, because R_a = {x_a}
(Lemma 2) and w ≠ x_a (x_a's only reader is g). For s1 ≠ s2 in S ⊆ sing(r) \ sing(w), the gate q*
accepts {s_i, w0}, so s_i w0 ∈ E. Also s_i ∈ N(a). So a and w0 have two common neighbours, which
is a C4. ∎

Data agrees: across the 270 S2 cases `l6.py` found (i) 118 times, (ii) 95 times and (iii) 57 times.
Consequence: **in a circuit without junk singletons, junk pairs and killers, S2 cannot occur.** S2 is
inseparable from the junk/killer phenomenon of the Q case. It appears only in triangle graphs (net).

## 4. Exact remaining open sub-case

**(S-open).** g = x_a & OR_B, a ∉ B, |B| >= 2, and one of the following holds:
* (a) the tree T has a gate read outside T ∪ {g} (any F_a; this includes all of S2);
* (b) T is private but ATT(a,g) fails, and some edge at a outside B is created only through a
  junk-carrying or singleton-free path.

Status:
* (b) has 25 instances, all on net+36 and net+46 (7 vertices). There (a,0) is bad, but a leaf
  v ∈ B gives (v,0) good. Example: `7=0|5 8=1|4 9=2|6 10=3&9 11=4|10 12=5|11 13=7&8 14=3|13
  15=12&14` with a = 3, B = {2,6} and N(3) = {2,4,5,6}. The only OR reader of x_3 is
  14 = x3|((x0|x5)&(x1|x4)), and its z is a junk rectangle with no singletons. (2,0) and (6,0) are
  good; so are (3,1), (4,1) and (5,1).
* (a) has 270 instances, all on the net and its extensions, with F_a = 1. For those, the
  conjecture that matches every case is: **every v in the support S of a shared tree gate
  satisfies elim(v,1) >= need(v,1)** (DATA, 270/270). By Lemma 6 every instance also contains junk or a killer, which is the same
  mechanism as in the Q case.

Lemma 5 shows that no proof can use the center in (a). Also, |B| = 1 with F_a, F_b >= 2 and ATT
failing both ways is unproved but never observed.

## 5. Final data counts

Status of each graph:
* <= 5 vertices: all 17 graphs, exhaustive.
* 6 vertices: 24 graphs exhaustive.
  - [01,02,03,04,05,23,45] was capped at 2000 circuits.
  - [01,02,03,12,34,35,45] (two triangles joined by an edge, Phi = 10) timed out at 500 s, so 0
    circuits.
* 7 vertices: net+36 and net+46 were capped at 1500 circuits each.

Results:
* Rule S: no failure anywhere.
* Theorem B: its conclusion was asserted on every case where its hypotheses hold.
* Lemma 5: checked on 8849 instances; it certifies 8669 of the bad-center cases.
* Lemma 6: trichotomy confirmed on all 270 S2 instances.
* Scripts: `dump.py`/`drive.sh` (enumeration), `cl.py` (classification library), `att.py`
  (Theorem B check), `an9.py` (S2), `an10.py` (§4(b)), `l5.py`, `l6.py`.
