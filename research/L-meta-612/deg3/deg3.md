# L-meta-612 for max degree <= 3: status of the split and of the direct induction

Status: **NOT closed.** The proof does not close for subcubic C4-free graphs, and the split route
is dead on this class:
* **the split conjecture (OR) #OR >= |E| - 1 is FALSE for the Petersen graph** (§5, explicit
  circuit, exhaustive check);
* Lemma M' is false (explicit circuits), and so is the one-vertex direct induction;
* the sav-version of Lemma D is false (explicit circuits);
* the adjacent-pair OR lemma is false (explicit circuit).

The main claim survives every test. This file also gives:
* one new PROVED reduction lemma (Lemma S, AND side);
* the class on which the OR half is PROVED;
* adversarial fuzzing DATA on 17 new subcubic graphs, Petersen included;
* the exact remaining sub-cases, each with its smallest instance.

Labels: PROVED (full proof here, or an explicit circuit checked exhaustively with Boolean semantics
by `ver.py`/`ver2.py`/`chk.py`); DATA (machine search only).

Notation is as in core/core.md:
* red removes constant gates, gates equal to an earlier node, and dead gates.
* For a vertex set X, write C|X for C with x_X := 0. Then
  - sav(X) = #OR(red C) - #OR(red C|X),
  - sa(X) = #AND(red C) - #AND(red C|X),
  - tot(X) = sav(X) + sa(X).
* need_OR(X) = e(X) - [G - X edgeless]; need_AND(X) = tau(G) - tau(G - X);
  need(X) = Phi(G) - Phi(G - X).
* C3 = the C4-free graphs with max degree <= 3. C3' = the graphs in C3 with no 3-regular
  component. Both classes are closed under vertex deletion: deleting a vertex from a non-cubic
  component cannot create a cubic component.

## 1. Frameworks (PROVED)

**R-OR (Theorem R with sav, sets).** Let K be a class closed under vertex deletion. Suppose every
G in K with min degree >= 2, and every reduced C for f_G, has some X ≠ ∅ with
sav(X) >= need_OR(X). Then #OR >= |E| - 1 for every G in K.
*Proof:* or.md Theorem R, with L2 replaced by the definition of sav. Leaves are paid by
release_exists, since sav >= ch. ∎

**R-AND.** Same statement, with sa and need_AND and with every G with E ≠ ∅ (no degree
hypothesis): if such an X always exists, then #AND >= tau.
*Proof:* induction. tau(G - X) = tau(G) - need_AND(X), and restriction never increases #AND. ∎

**R-TOT.** If every G in K with E ≠ ∅ that is not a star, and every reduced C, has a
"restriction step" X with tot(X) >= need(X) and G - X not edgeless, then size >= Phi on K.
Stars are paid directly: a circuit that depends on d + 1 variables has >= d gates.

*Caution (PROVED).* Without the condition "G - X has an edge", the statement is vacuous: X = V
always works, and X = N[v] in a star-like G is circular.

## 2. Refutations (PROVED by explicit circuits)

**2.1 Lemma M' is false. The (AND) half cannot use one-vertex restrictions.**
Take G = two triangles plus a bridge, E = [01,02,12,23,34,35,45]. Here tau = 4 and Phi = 10, and
every vertex lies in some minimum cover. Circuit (size 13 = Phi + 3, #AND = 4 = tau, #OR = 9):

    6=2|4 7=5|2 8=1|0 9=3|5 10=6&8 11=3|10 12=11&7 13=4|12 14=0|12 15=9&13 16=1|2 17=14&16 18=17|15

For **every** v, red(C|v) still has 4 AND gates (`ver.py`). So sa(v) = 0 < 1 = need_AND(v) for
all v.

The minimal AND gate 10 = (x2|x4)&(x0|x1) is a junk rectangle: 04 and 14 are non-edges. Each of the
4 AND gates does two jobs. A second, independent instance (size 14) is
`6=0|3 7=5|3 8=4|2 9=8&6 10=4|9 11=2|0 12=5|2 13=9|3 14=13&12 15=1|14 16=14|10 17=16&7 18=11&15 19=18|17`.

The same circuit refutes the one-vertex direct induction: tot(v) = sav(v) <= 3 < need(v) for
every v. need(v) is 3 at degree-2 vertices and 4 at the hubs. Here (OR) and (AND) themselves both
hold, and so does R-OR for X = {2} (sav = 3 = deg).

In the same circuit, the 2-sets {0,1}, {0,4}, {1,4}, {2,4}, {2,5} and {3,4}, and every X = N[v],
satisfy sa(X) >= need_AND(X) and tot(X) >= need(X) (`ver2.py`). So set restrictions are not refuted.
or.md's "0 failures" for M' came from circuits of size <= Phi + 2; this one has size Phi + 3.

**2.2 The adjacent degree-2 pair lemma is false.** The candidate was: "if deg u = deg v = 2,
uv ∈ E and G - {u,v} has an edge, then sav({u,v}) >= 3".
* It held on all cached circuits of min-degree->=2 graphs (47,415 pairs) and failed only on P6.
* Lifting the P6 failure gives a counterexample on C7 (delta = 2), with size 11 = Phi + 1 and
  #OR = 6 = |E| - 1 (`chk.py`):

      7=0&1 8=5|7 9=0&8 10=4|9 11=2|10 12=3&11 13=8&10 14=12|13 15=1|2 16=6&15 17=14|16

  Here sav({4,5}) = 2 < 3, and sav(4) = sav(5) = 1.

The mechanism is z_5 = x5 | x0x1, the Theorem-N trick. Any fixed local set fails; the choice
has to come from the circuit.

## 3. New PROVED lemma

**Lemma S (one-sided minimal AND gates).** Let C be reduced and h = P & Q a minimal AND gate.
By Fact P, P = OR_A and Q = OR_B with A ⊄ B and B ⊄ A. If |A \ B| = 1, say A \ B = {a}, then
sa(a) >= 1.

*Proof.* Under x_a := 0, the node P computes OR_{A-a}, and Q is unchanged because a ∉ B.
* If A = {a}, then h = 0 and is removed as a constant.
* Otherwise A - a ⊆ B, so P|_a <= Q, and h|_a = P|_a equals the earlier node P. So h is removed as
  a duplicate. (P is not constant, because A - a ≠ ∅.)

Reduction keeps a subset of the gates with their operations, so #AND drops by >= 1. ∎

**Corollary.** A counterexample to "some v has sa(v) >= 1" (hence to M') must have every minimal
AND gate with |A \ B|, |B \ A| >= 2. By C4-freeness every such gate then carries a junk pair in
(A \ B) x (B \ A). Both circuits in 2.1 have this form.

## 4. What is PROVED for the OR half on C3

* (OR) holds on the class "C4-free with at most one vertex of degree >= 3". This is Theorem F +
  R-OR, already in lemD.md; in C3 it covers paths, cycles, spiders and lollipops.
* Lemma D (with ch, hence with sav) is PROVED for every G in C3 with delta = 2 such that:
  - H is independent,
  - no degree-2 vertex has N(v) ⊆ V2 (all threads have length <= 3), and
  - at most one degree-2 vertex has N(v) ⊆ H.

  This is lemDa Corollary A2. Examples: θ(2,3,3), θ(3,3,3), two triangles joined by a path of
  length 2 or 3. The class is not closed under deletion, so this does not give (OR) on a hereditary
  class beyond Theorem F.


## 5. (OR) is false for Petersen; sav-Lemma D is false (PROVED by explicit circuits)

**5.1 Petersen.** E = [01,12,23,34,40,05,16,27,38,49,57,79,96,68,85] (|E| = 15, tau = 6,
Phi = 20). The circuit below (file `pet_or13.txt`) has size 23, **#OR = 13 < 14 = |E| - 1** and
#AND = 10:

    10=8|0 11=5&10 12=7|11 13=12|6 14=5&13 15=12&14 16=2|15 17=13|4 18=17&9 19=0|3 20=10&19
    21=4&19 22=21|18 23=8|1 24=6&23 25=3|1 26=25|12 27=16&26 28=20&25 29=22|27 30=28|24
    31=23&30 32=31|29

It was checked by direct gate-by-gate evaluation of the raw circuit on all 1024 inputs, and again by
`tr.breduce`.

*Mechanism.* Mixed nodes such as 12 = x7 | x0x5 | x5x8 (an OR of a variable with AND-made pairs)
are reused as inputs of several products. For example, 27 = (x2|15) & (x1|x3|12) creates
12, 23, 27 and passes 05, 57, 58 in one AND. Junk is killed by ANDs: 14 = x5 & 13 carries junk 56,
and 15 = 12 & 14 kills it. ORs are traded for ANDs; the total, 23 >= 20, still respects the claim.

Consequences:
* (OR) fails in C3 and in C4-free graphs of girth 5. The split route (OR)+(AND) cannot prove the
  claim for max degree <= 3.
* The core.md remark "(OR) implies Problem 24" is moot.

A second fuzzing run (another seed) found another #OR = 13 Petersen circuit. Searches for
#OR <= 12, and for size <= 19 (the main claim), found nothing: 240 s each, about 0.8M edits.

DATA: on the smaller graphs of §6, (OR) was never violated (#OR minimised, 60 s each, size <= Phi+8).
So **Petersen (n = 10) is the smallest known (OR) counterexample**. Smaller cubic C4-free graphs do
not exist.

**5.2 sav-Lemma D / R-OR with single vertices is false even where (OR) holds.**
* constrS7 (E = [01,04,05,12,14,26,35,36,56], delta = 2, H = {0,1,5,6}). Circuit of size
  14 = Phi + 2 with #OR = 8 = |E| - 1, so it is OR-optimal:

      7=1|5 8=0&7 9=2|8 10=5|9 11=7&10 12=6|11 13=9&12 14=10&6 15=3|14 16=4|13 17=0|1 18=17&16 19=12&15 20=19|18

  sav = {0:2, 1:2, 2:1, 3:1, 4:1, 5:2, 6:2}, so no vertex has sav >= deg. This is
  cross-checked with `tr.breduce`.
  - The pairs {0,1}, {0,2}, {1,2} and {5,6}, and N(v) for v in {0,1,3,4,6}, do satisfy
    sav(X) >= need_OR(X).
* Petersen minus a vertex (delta = 2) and Petersen (cubic): fuzzed circuits with no vertex of
  sav >= deg (`found.txt`). On the first Petersen circuit some pairs work. On the #OR = 13 circuit
  **no X with |X| <= 2 works**, as it must, since (OR) fails there.

Thus case (b) of lemD (delta = 3) is not just open but false for sav, and case (a) is false for
sav as well.

## 6. Adversarial fuzzing DATA (`fz.py`, `run.py`, `run2.py`, logs c1-c5.log)

*Method.* Start from random star-cover circuits. Apply random function-preserving edits: insert
op(q,r) and redirect some readers of q to it, or rewire an input. Each edit is verified on the full
truth table, then reduced. Hill-climb on the number of "good" vertices (or sets) to reach 0. Size is
at most Phi + 4, unless stated otherwise. Each run is 40-90 s, about 0.1-0.8M edits.

*Validation.* The search rediscovers the known Construction-S ch-counterexample on constrS7 in
150 s.

Graphs: tri+C5, 2tri+bridge, θ(2,3,3), θ(1,2,5), θ(3,3,3), θ(1,4,4), 2tri+P2, constrS7, P6, net,
C5+pendant, C5+2 pendants, C6+2 pendants, spider(2,2,2), C7, Petersen-v, Petersen.

| statement (∃ ... for every reduced C) | result |
|---|---|
| R-OR, single v: sav(v) >= need_OR(v) | **FAILS**: constrS7, Pet-v, Pet |
| R-OR with X = v or a pair | survives all graphs except Pet (fails, §5.1) |
| M0 / M': some v with sa(v) >= need_AND(v) | **FAILS**: 12 of 17 graphs, incl. tri+C5, θ's, C7, P6, net |
| R-AND with X = v or N[v] (G - N[v] with an edge) | **FAILS**: net, C6+2pend, C7 |
| R-AND with X = v or a pair | survives all 9 graphs tested (incl. Pet-v, Pet), min. 3 good sets |
| R-TOT, single v | **FAILS** (2tri+bridge, §2.1) |
| **R-TOT2: X = {v} or X = N[v] (G - X with an edge)** | **survives all 17 graphs**; fewest good options 1 (net) |
| (AND) #AND >= tau | no violation found |
| main claim size >= Phi | no violation found (Pet, 240 s direct search) |

Cached data restricted to max degree <= 3: 52,919 reduced circuits (`t1.py`-`t5.py`), all of
size <= Phi + 2.
* There, "∃v sav(v) >= need_OR(v)", "∃v tot(v) >= need(v)" and "∃v sa(v) >= need_AND(v)" all hold.
* The counterexamples above have size Phi + 2 or more, often Phi + 3 or more. The cache was too
  small to see them.

## 7. Exact remaining gap

1. **The split is dead on C3** (§5.1). Only total-count arguments can work.
2. The only unrefuted one-step lemma of the requested shape is:

   **Lemma T2 (DATA).** Let G in C3 have an edge and not be a star, and let C be reduced. Then
   some v has either tot(v) >= Phi(G) - Phi(G - v) with G - v not edgeless, or
   tot(N[v]) >= Phi(G) - Phi(G - N[v]) with G - N[v] not edgeless.

   T2 + R-TOT implies the theorem on C3. It is not proved in any case. Even leaves fail with
   X = {v} (P6 circuits where tot(leaf) = 1 < 2), so the N[v] option is needed from the start.
3. Smallest instances:
   * for T2 with X = {v} only: 2tri+bridge, size 13 (§2.1);
   * for every split lemma: constrS7, size 14 (OR) and Petersen #OR = 13 (OR);
   * for AND with {v, N[v]}: net, size 12 (`found.txt`);
   * the hardest open case for T2 is cubic (Petersen, Phi = 20), where the N[v] step must save
     Phi(Pet) - Phi(C6) = 20 - 8 = 12 gates. On the fuzzed Petersen circuits it
     does.

## 8. Lean

Nothing closes, so there is no final theorem to formalise. What is formalisable now in the project
model (`Circuit`, `wiresFrom`/eval, `Monotone2`, L_meta_599's `of_paid_deletions`,
`release_exists`, `restrict_many`):
* the refutations: finite statements over 2^n inputs, by `decide`/`native_decide` on explicit gate
  lists (n <= 10);
* R-OR / R-AND / R-TOT as instances of `of_paid_deletions` with cost = best;
* Lemma S.

The missing infrastructure is a verified reduction `red` (constant, duplicate and dead-gate removal,
preserving the output and never increasing #AND or #OR); it is routine. Lemma T2 itself has no proof
to formalise.

Files (this folder): `lib.py`, `fz.py`, `run.py`, `run2.py`, `camp*.sh`, `chk.py`, `ver*.py`,
`anal.py`, `found.txt`, `pet_or13.txt`, `t1-t5.py`, `c1-c5.log`.

