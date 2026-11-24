# L-meta-612, the core: global methods, literature status, verdict

Labels:
* PROVED: full proof given here.
* DATA: exact Boolean machine check (scripts in this folder, `h1.py`, `xall.py`, `every.py`, `nbr.py`, `sav1.py`) and nothing more.
* LITERATURE: precise citation, read in the source.

Notation is as in or-bound/or.md and lemma-d/lemD.md.
* ch(v) is the number of OR gates with a v-dominated input.
* sav(X) = #OR(red C) - #OR(red C|_{x_X=0}), where red removes constant gates, gates equal to an earlier node, and dead gates. For a single vertex, sav(v) = sav({v}).
* e(X) is the number of edges meeting X.
* need(X) = e(X) - [G - X has no edge].

Theorem R only needs some X with sav(X) >= need(X) (L2, sequential restriction), and Lemma D is the case X = {v} counted with ch.

## 0. Headline: literature status (decides the question)

**LIT-1 (Jukna 2005, Problem 24).** S. Jukna, *Disproving the single level conjecture*, ECCC TR05-021 (SIAM J. Comput. 36 (2006)), §8: "Problem 24. Prove C(f_G) = Ω(n^{1+ε}) for an explicit n-vertex graph G." Here C is monotone fan-in-2 circuit size. Just before stating it, Jukna recalls that explicit K_{2,2}-free graphs with Ω(n^{3/2}) edges exist. His Theorem 5 only gives formulas L(f_G) >= |E|/2. He adds: "proving lower bounds on the monotone size of quadratic functions in the case of circuits (arbitrary fanout) is a more difficult task. Razborov's argument works well only if both minterms and maxterms are short ... for functions of the form f_G we need some new arguments."

**PROVED (consequence).** L-meta-612 implies a positive answer to Problem 24 with ε = 1/2.
* Even the OR half (OR) #OR >= |E| - 1 implies it.
* So does Lemma D, via Theorem R. So does "some v has sav(v) >= deg v", via Theorem R with sav in place of ch.

*Proof.* Take G = the point-line incidence graph of PG(2,q).
* It is explicit, bipartite and C4-free, because two points lie on exactly one line.
* It has n = 2(q^2+q+1) vertices and |E| = (q+1)(q^2+q+1) = Θ(n^{3/2}) edges.
* The claim gives C(f_G) >= |E| = Θ(n^{3/2}). ∎

So L-meta-612 is **not a known theorem**. It is **at least as strong as an open problem explicitly posed by Jukna in 2005**. My searches (Nov 2026) found no resolution of Problem 24. Its status after 2005 is not verified beyond that search.

The target is not known to be false. No monotone circuit beating a star cover is known for any C4-free graph, and the single-level counterexamples below all use large bicliques.

**LIT-2 (Amano–Maruoka, ISAAC 2004, LNCS 3341, 28–40; Algorithmica 46 (2006) 3–14).** As stated by Jukna 2005, p. 9, they prove C^1(f_G) >= |E| for K_{2,2}-free G, where C^1 is single-level circuit size. They use Wegener's (h,k)-disjoint Boolean-sum bound (Jukna 2005, Lemma 14, citing Wegener, TCS 43 (1986)).

**PROVED.** Every single-level circuit for f_G is STAR-ALL. So Theorem S (girth5.md) contains Amano–Maruoka and strengthens their bound to |E| + tau - 1.
* Proof: an input reaching the output on an AND-free path would give f(e_u) = 1. So the output is an OR of AND gates h = OR_A ∧ OR_B, and each h <= f.
* h <= f forces A ∩ B = ∅ (N1) and A x B ⊆ E (N3).
* A and B are nonempty after constant removal (N2). ∎

**LIT-3.** Lenz–Wegener (TCS 81 (1991) 257–268) observe that single-level AND complexity C^1_mult(f_G) equals cc(G), the bipartite clique cover number.
* For C4-free G every biclique is a star, so C^1_mult = tau. Our Lemma A (#AND >= tau for clean circuits) is the general-circuit analogue.
* Caution, to check: Lenz–Wegener exhibit a G with C_mult = 3 < C^1_mult = 4. I could not access the paper. If that G were C4-free, it would refute the split conjecture (AND) #AND >= tau, though not the total bound.
* Jukna 2005, Theorem 4, and Amano–Maruoka's gaps use saturated graphs, matchings and Sylvester/Kneser graphs, all full of C4.

**LIT-4 (Jukna, On graph complexity, ECCC TR04-005 rev. 1, Theorem 7.3).** G triangle-free and C4-free implies monotone formula length L+(f_G) >= |E|/2. This is the only general |E|-type bound I found for unrestricted depth, and it is for formulas only.

## 1. Global charging and set versions (route 1)

**PROVED (one-shot charging cannot work, even on optimal circuits).**
* Take G = K_{1,s} with s = 2^k and the optimal circuit x_t ∧ T, where T is a balanced OR tree on the leaves.
* #OR = s - 1 = |E| - 1, but only the s/2 bottom ORs have a dominated input. So |Q_V| = s/2, and ch(t) = 0 although deg t = s.
* Hence any inequality built from one-shot charges, such as Σ_v w(v) ch(v) >= Σ_v w(v) deg(v) - K, or Hall's condition for an edge-to-charged-OR matching, is off by a factor of 2.
* Sequential restriction is essential: after x_a := 0, the gate (x_a|x_b)|(...) becomes charged by b. This is why Theorem R, not an LP or Hall certificate over ch, is the right frame.

**DATA (set versions with true savings sav(X)).** On 125,420 reduced circuits (all dumps, sizes Phi..Phi+2):

| statement | result |
|---|---|
| some v: sav(v) >= need({v}) | holds on all 125,420 |
| every v: sav(v) >= need({v}) | fails on 12,425. Example: `6=4\|5 7=4&5 8=0\|7 9=1\|3 10=6\|9 11=8&10 12=2\|11 13=3\|8 14=12&13`, hub 0: sav 4 < 5 |
| every v: sav(N(v)) >= need(N(v)) | fails on 7,225, all graphs with leaves (N(leaf) = {hub}); holds on all 23,056 min-degree->=2 circuits |
| all X, sampled 3,821 circuits | fails for some singletons (494/20,278), pairs (711/42,517), independent sets of size >= 3 (55/12,602), other sets of size >= 3 (390/41,988); vertex covers never fail, but for them the statement is just (OR) itself |

So no fixed family of sets X works for every circuit. The useful currency is sav, not ch.

**PROVED (sav >= ch).** The case-(a) obstruction of lemDa.md is an artifact of counting with ch.
* In Construction S, s_v = x_v ∧ (x_u | x_w). Setting x_v := 0 makes the outer OR reading s_v a copy, and x_u | x_w becomes dead.
* So sav(v) >= 2 = deg v for every V2 vertex, while ch(v) = 1.
* DATA, explicit circuits: on the n=7 Construction S circuit, subdivided K4, the Theorem N two-triangles+bridge circuit and the N2 10-vertex circuit, **every** vertex set X satisfies sav(X) >= need(X) (`xall.py`). In particular every V2 vertex is sav-good there. The lemDa conclusion "only hubs are good" holds for ch only.

**DATA (sav-Lemma D, 23,056 min-degree->=2 circuits, `sav1.py`).**
* Some minimum-degree vertex has sav >= deg: 23,056/23,056.
* All minimum-degree vertices are sav-good: 21,385.
* Some hub is sav-good: only 7,828 of the 8,460 circuits that have a hub. In triangle+C5 the hubs have sav 2 < 3.

Unrefuted candidate: **(Dmin) some minimum-degree vertex v has sav(v) >= deg v.** It implies (OR). It is useless as a simplification for regular graphs, and the projective-plane case again implies Problem 24.

## 2. Restrictions to 1 (route 2)

**PROVED.** f_G|_{x_v=1, x_{N(v)}=0} = f_{G-N[v]} = f_G|_{x_{N[v]}=0}.
* The forced-variable step (Fact F) has an OR version, by release_exists: if F ≠ ∅ and G - F has an edge, every circuit for f_{G,F} has #OR >= #OR_min(f_{G-F}) + |F|. Each forced w has ch(w) >= 1, because f is not <= x_w and depends on x_w.
* Consequently the 1-branch at v ("set x_v := 1, then strip N(v)") must save e(N(v)) ORs. That is exactly the set version with X = N[v].
* Fact F's |F| term is far weaker than what is needed (e(N(v)) ~ deg^2).

**DATA.** On all 23,056 × n cases, the savings of (x_v := 1, N(v) := 0) and of (N[v] := 0) are identical. So restriction to 1 added no power. It pays exactly where X = N(v) pays: every v in min-degree->=2 graphs, never at the neighbour of a leaf.

## 3. Potential / LP duality (route 3)

* In Theorem S the dual certificate is Wegener's (1,1)-disjointness count: every OR gate merging >= 2 leaves lies in the S-cone of a single centre (C4-freeness). The other two counts are tight link-counts.
* Every minimum circuit in the data is tight in all three counts (girth5.md §4).
* For general circuits no static certificate over gates exists in the charged form (§1, PROVED). A certificate would have to be dynamic, as a restriction order.
* That is Theorem R plus Lemma D(sav), which is again Problem-24-hard in the dense case.

## 4. Verdict

* Most promising route: Theorem R with sav in place of ch. It is strictly weaker than Lemma D and true on all data, and it removes the case-(a) obstructions. Prove it for classes with |E| = O(n), for example max degree 3, or degeneracy 2 with C4-free. Such classes are closed under deletion, so Theorem R applies inside the class, and they do not touch Problem 24.
* Attainability: the full L-meta-612 is attainable only together with a solution of Jukna's Problem 24: the first super-linear (here n^{3/2}) monotone circuit lower bound for an explicit quadratic function. Jukna notes that known methods (Razborov approximation) fail for it. The high-degree core is therefore a genuine open problem, not a gap in our local toolkit.
* I recommend reclassifying L-meta-612 as "implies a known open problem". Pursue bounded-degree and STAR-ALL / single-level versions; the latter is proved (Theorem S, which generalises Amano–Maruoka).
