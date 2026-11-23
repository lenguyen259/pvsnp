# (OR) #OR >= |E| - 1 for C4-free G: the L_meta_599 method and how far it goes

Status: **(OR) NOT closed.** What this file adds:
* the exact argument of the accepted Lean proof L_meta_599;
* where its sparsity hypothesis enters (one place only);
* a PROVED reduction of (OR) for all C4-free G to a single per-circuit lemma (Lemma D), with zero
  counterexamples in the data and in a direct SAT search;
* the same reduction for (AND) (Lemma M');
* a negative fact: the degree-<=2 truncation is unsound for (AND).

Labels: PROVED (full proof here or in the accepted Lean file), DATA (machine check only).

Notation:
* C is a monotone fan-in-2 circuit with f_C = f_G.
* *Reduced*: no gate computes a constant, or the same Boolean function as an earlier node. Replacing
  such a gate by that node and deleting dead gates never increases #OR or #AND.
* For a vertex v, a node q is *v-dominated* if q <= x_v as Boolean functions.
* ch(v) = #OR gates with at least one v-dominated input. This is Lean's `Charged C v j`.

## 1. What L_meta_599 proves, and how

Theorem (Lean, accepted): if G is a pseudoforest (every S spans <= |S| edges) with no 4-cycle, then
|E| <= #OR + 1 for every Monotone2 circuit.

The argument is a vertex-deletion induction on best(G) = min #OR (`of_paid_deletions`, `edge_bound`).
If |E| > best(G) + 1, it finds a vertex v with best(G - v) + deg v <= best(G). That makes G - v a
smaller counterexample.

Circuit side (no graph hypothesis is used here):
1. **Restriction (`restrict_many`, `restrict_charged`, `charged_saving`).** Set x_v := 0. Every
   charged OR gate a|b with a <= x_v becomes a copy of b. Rerouting gives a circuit for
   f_{G-v} = f_G|_{x_v=0}, with #OR reduced by the number of charged gates. So
   best(G - v) + |S| <= #OR for any set S of charged gates of v.
2. **Release (`release_exists`).** Suppose f depends on x_v and f is not <= x_v (some accepted z has
   z_v = 0). Then v has a charged OR gate. Proof: follow a sensitive wire down from the output. An
   AND gate with a v-dominated sensitive input is itself v-dominated, so if no OR gate had a
   v-dominated input, the output would be <= x_v.
   This gives `leaf_paid`: a leaf saves 1 = deg v.
3. **Core (`pay_core`), for every support vertex of degree 2.**
   * Take the first OR gate g. Everything before it is an AND gate, so its inputs are monomials
     x_A and x_B (`all_and_principal`, `prefix_decision`).
   * A and B are incomparable. Otherwise g is a copy, which contradicts OR-minimality
     (`forbids_copy`, `discard_redundant_or`).
   * Every v in S = A ∪ B is charged at g.
   * If some v in S has a second charged gate, that is double saving (`double_saving`):
     2 = deg v, done.
   * Otherwise g is the only charged gate of every v in S. Then f restricted to the S-variables
     factors through the bit [A ⊆ X or B ⊆ X] (`changed_dominated`, `factor_gate`,
     `graph_factors`). `no_module_of_no_four` shows that this is impossible when every vertex of
     S has 2 neighbours and G has no C4. The two cases are: S spans an edge (then S would have to
     be closed and carry at most two edges), or S is independent (then S would contain twins,
     which give a C4).

**Where sparsity is used: only in `regular_of_no_leaf`.** For a pseudoforest with no leaf, every
support vertex has degree exactly 2. That is the only reason a saving of 2 suffices. Every circuit
lemma above is graph-free. `no_module` needs only "every vertex of S has >= 2 neighbours" plus
no C4. So, PROVED by the same proof: **for every C4-free G with min degree >= 2, some v in S has
ch(v) >= 2.** That pays for v exactly when deg v = 2.

## 2. Removing sparsity: reduction to Lemma D (PROVED)

**Lemma D (DATA).** Let G be C4-free with min degree >= 2, and let C be a reduced circuit for f_G.
Then some vertex v has ch(v) >= deg(v).

**Theorem R (PROVED).** Lemma D implies (OR) for every C4-free G.

*Proof.* Induction on |E|, over all circuits; neither the circuit nor its restrictions need to be
minimal.
* Reduce C. This does not increase #OR.
* If |E| <= 1, the bound is trivial.
* If G has a leaf v: since |E| >= 2, some edge avoids v, so release gives ch(v) >= 1 = deg v.
* Otherwise the min degree is >= 2, and Lemma D gives v with ch(v) >= deg v.
* In both cases, restricting x_v := 0 gives a circuit for f_{G-v}. Here G - v is C4-free, and the
  new circuit has <= #OR - deg v ORs. By induction it has >= |E| - deg v - 1 ORs.
  (If E(G - v) is empty, then #OR >= ch(v) >= deg v = |E|.) ∎

Lemma D is a statement about every reduced circuit, not only minimum ones, so near-minimum
circuits are real tests of it.

Evidence (`t1b.py`, Boolean semantics, all dumps: s_case, tf and nf/circs, sizes Phi..Phi+2):
* **0 failures on 23,056 reduced circuits of min-degree->=2 graphs:** K3, C5, C6, bowtie, two
  triangles joined by an edge, two disjoint triangles, and triangle+C5 sharing an edge.
  "Exists v with sav(v) >= deg v" (all eliminations counted, not just charged ones) also holds.
* On all 102k circuits with |E| >= 2, leaves included, there is always a vertex with ch >= deg.
  The 21 failures are the single edge x0&x1.
* **SAT (`dsat.py`, CaDiCaL).** A circuit is asked for in which every v has ch(v) <= deg(v) - 1,
  with no constant gates and no gate equal to an earlier node. Results:

| graph | Phi + X | result |
|---|---|---|
| bowtie | X = 0, 1, 2 | UNSAT (11 s, 43 s, 90 s) |
| triangle+C5 [02,05,12,13,23,34,45] | X = 0, 1 | UNSAT (183 s, 267 s) |
| two triangles + bridge | X = 0 | UNSAT (196 s) |
| C6 | X = 0 | UNSAT (14 s) |
| bowtie X = 3, triangle+C5 X = 2, others X >= 1 | | not run: stopped to stay within the solver budget |

What does **not** work (DATA, `t2.py`-`t7.py`):
* Plain averaging. Σ_v ch(v) >= 2|E| - n + 1 fails: on a bowtie circuit, Σ ch = 2|E| - n
  exactly.
* None of these fixed rules picks a good vertex: "min degree", "x_v never read by AND", "v is not
  the centre of a >= 2-leaf star", "good vertices form a cover", "good vertices are independent".
* Weaker statements that do hold on all data: a min-degree vertex is always good; some minimal OR
  gate always contains a good vertex. Even "every minimal OR gate contains a good vertex" fails on
  only 4 circuits (triangle+C5 junk-killer circuits).

**Why Lemma D is hard.** This is PROVED as an obstruction, not as a theorem. For one vertex,
ch(v) = 1 is locally consistent: q = x_v ∧ OR N(v) can be read by a single OR. Changed-domination
only says that the restrictions b_i of the non-dominated inputs of v's charged gates jointly reject
every set z with f(z) = 0 and f(z + v) = 1. Any lower-bound proof must choose v globally. The
deficit mechanisms are exactly those of nf.md:
* v as a star centre, where one star serves |L| edges;
* one OR x_v | b with S_b = ∅ (an N1/Z-type gate) serving several neighbours;
* junk rectangles.

The C5 size-Phi+2 circuit (nf.md) satisfies Lemma D, as do all of the 7 non-STAR-ALL junk-killer
types in the data.

Small new local fact (PROVED, from `changed_dominated` with S = {a}). Suppose g = x_a | x_B is
the first OR gate and g is the only charged gate of a (a ∉ B). Then f(z + a) = f(z) for every
z ⊇ B. Consequences:
* If B = {b}: then a ≁ b and N(a) ⊆ N(b). By C4-freeness, deg a <= 1.
* If B = {b, c} with bc ∉ E: then a ≁ b, c and N(a) ⊆ N(b) ∪ N(c). So deg a <= 2.

So in these cases ch(a) >= 2 as soon as deg a >= 2 (respectively >= 3). This still gives only 2
charges, not deg a.

## 3. (AND) by the same method

**Reduction (PROVED).** (AND) #AND >= tau follows from Lemma M' below.

**Lemma M' (DATA).** If every vertex of a C4-free G lies in some minimum vertex cover, then every
reduced circuit for f_G has a v for which restricting x_v := 0 removes >= 1 AND gate. "Removes"
means the gate becomes 0, becomes a copy, or becomes dead.

*Proof of the reduction.* tau(G - v) >= tau(G) - 1 always.
* If some v lies in no minimum cover, then tau(G - v) = tau(G), and restriction does not increase
  #AND.
* Otherwise Lemma M' supplies the saving of 1. ∎

Data (`t6b.py`): 0 failures over all dumps. The stronger form "some AND gate is <= x_v" fails on
587 circuits, all of them the net (e.g. `6=0|5 ... 13=9&12`). So M' must count gates that become
copies, not just gates that become 0.

**Truncation is unsound for (AND) (PROVED by example).** In `6=3|5 7=0|6 8=1|3 9=2|5 10=4|6
11=8&9 12=4|11 13=7&12 14=10&13` (net, Phi = 8):
* gate 13 already has degree-<=2 part exactly f_net;
* gate 14 is needed only to kill degree-3 junk monomials such as x0x1x2.

So circuits that are correct only "modulo degree >= 3" can have #AND = 2 < tau = 3. Any proof of
(AND) must use exact Boolean semantics. The S/P bookkeeping of girth5.md and nf.md alone cannot
give it. For (OR), the truncated version of Lemma D and of (OR) holds on all data (`t1.py`).

## 4. Exact remaining gap

* (OR) for C4-free G is equivalent, via Theorem R, to Lemma D, a per-circuit statement. Lemma D is
  PROVED for 2-regular graphs (Lean core), and it holds with 0 counterexamples in the data and in
  SAT. Open: graphs with min degree >= 2 and a vertex of degree >= 3. The smallest such graph is
  the bowtie, where SAT has checked Lemma D through Phi+2.
* (AND) follows from Lemma M' (DATA). It needs Boolean, not truncated, reasoning.

Files (this folder):
* `tr.py`: semantics and reduction.
* `t1.py`/`t1b.py`: Lemma D, truncated / Boolean.
* `t2.py`-`t5.py`, `t7.py`: rule tests.
* `t6.py`/`t6b.py`: (AND) restriction.
* `dsat.py`, `ddrive.sh`, `log*.txt`: SAT search.
