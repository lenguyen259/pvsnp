# Literature check: monotone circuits for graph functions f_G of sparse / C4-free graphs

Setting: f_G(x) = OR over uv in E of (x_u AND x_v). Monotone fan-in-2 AND/OR circuits, size = number of gates.
tau(G) = vertex cover number. "Star-cover circuit": for a vertex cover S with the edges split into stars at the
vertices of S, use OR(neighbours) AND x_s for each s in S, then OR the results. Size = |E| + tau - 1 gates
(|E| - tau ORs inside the stars, tau ANDs, tau - 1 top ORs).

Notation used in the literature:
- C(f_G): monotone circuit size.
- C^1(f_G): size of the best single-level circuit (every input-output path has at most one AND gate).
- C_mult(f_G), C^1_mult(f_G): number of AND gates ("conjunctive" or "multiplicative" complexity), in general and in single-level circuits.
- L(f_G) or L+(f_G): monotone formula leafsize.
- cc(G): bipartite clique (biclique) covering number.

## Sources actually read (full text)

- [J-SLC] S. Jukna, "Disproving the single level conjecture", ECCC TR05-021 (2005); SIAM J. Comput. 36(1):83-98 (2006), doi:10.1137/S0097539705447001. Full ECCC text read.
- [J-surv] S. Jukna, "Computational Complexity of Graphs", survey chapter in *Advances in Network Complexity* (Dehmer, Emmert-Streib, Mowshowitz, eds.), Wiley 2013, pp. 99-154. Full text read (web.vu.lt/mif/s.jukna/ftp/graph-compl.pdf).
- [J-book] S. Jukna, *Boolean Function Complexity: Advances and Frontiers*, Springer 2012. Full-text draft read (web.vu.lt/mif/s.jukna/boolean/bool-V7.pdf), plus the published table of contents. §7.2 is "Lower bounds for quadratic functions" (p. 206 in print) and §1.7 is "Graph complexity".
- [W-book] I. Wegener, *The Complexity of Boolean Functions*, Wiley-Teubner 1987. Full text read (the "blue book" PDF). §4.7 is "Boolean sums and quadratic functions"; the single-level material is in the formula chapter (Ch. 8, p. 236ff), plus exercises.

## Sources seen only through abstracts, zbMATH or secondary citations (full text not reachable here)

- [LW] K. Lenz, I. Wegener, "The conjunctive complexity of quadratic Boolean functions", CSL '87, LNCS 329 (1988), 138-150; TCS 81(2):257-268 (1991). The zbMATH review of the CSL version was read. ScienceDirect was not reachable from this session.
- [AM] K. Amano, A. Maruoka, "On the monotone circuit complexity of quadratic Boolean functions", ISAAC 2004, LNCS 3341, 28-40; journal version "The monotone circuit complexity of quadratic Boolean functions", Algorithmica 46(1):3-14 (2006). Only the abstract and Jukna's account in [J-SLC] were seen. Springer was not reachable.
- [B] S. Bublitz, "Decomposition of graphs and monotone formula size of homogeneous functions", Acta Inf. 23:689-696 (1986). The zbMATH review and Wegener's exercise were read.
- [MS] R. Mirwald, C. P. Schnorr, "The multiplicative complexity of quadratic Boolean forms", TCS 102(2):307-328 (1992). Seen through [J-SLC].
- [J-CPC] S. Jukna, "On graph complexity", Combin. Probab. Comput. 15 (2006) 855-876 (ECCC TR04-005). Its results were read as they are reproduced in [J-surv] and [J-book].

Not checked (no access or nothing found): Bloniarz's PhD thesis (MIT 1979; the dspace copy returned an HTML wall), Krichevskii (1964) beyond what Wegener and Jukna cite, Sergeev, Grinchuk, Krieger. Web searches, alphaXiv discovery and OpenAlex/zbMATH title searches found no paper giving an exact C(f_G) for paths, cycles, forests or pseudoforests. Consensus was unavailable (monthly quota used up).

---

## What the literature does say (relevant facts, with quotes)

**F1. Single-level conjunctive complexity equals the biclique cover number** ([LW], as reported in [J-SLC] §2). [J-SLC]:
> "Lenz and Wegener [12] ... observed that in this basis C^1_mult(f_G) is just the bipartite clique covering number cc(G) of G, i.e. the minimal number of bipartite complete subgraphs of G covering all edges of G."

*Inference (mine):* if G is C4-free, every biclique of G is a star, so cc(G) = tau(G). Hence C^1_mult(f_G) = tau(G) for every C4-free G. The AND-gate part of Theorem PF is therefore the statement "C_mult(f_G) = C^1_mult(f_G)" for C4-free pseudoforests, i.e. the single-level conjecture for AND gates on that class.

**F2. The single-level conjecture fails in general, for both AND-count and total size.**
- [LW] (zbMATH review of the CSL version): "The single level conjecture is disproved, i.e. some quadratic function is defined whose single level complexity is larger than its conjunctive complexity." [J-SLC] says this is a graph with C_mult = 3 but C^1_mult = 4. The graph is not identified in the sources I could read, so I could not check whether it contains a C4. It almost certainly does, since the gap must come from a non-star biclique structure, but this is not verified.
- [J-SLC] Theorem 3: for the saturated extension of an n-to-n matching, C_mult(f_G) = O(log n) but C^1_mult(f_G) >= n/2. Theorem 4: some n-vertex G have C(f_G) = O(n) but C^1(f_G) = Omega(n^2/log^3 n). These graphs are saturated, so they are dense and full of C4s.
- [J-SLC] also cites smaller gaps: Krichevskii, Gap = 1 for K_n; Bublitz, formula gap 8/7; [AM], gap 29/28 "for circuits computing sets of quadratic functions". [W-book] Ex. 2 to Ch. 4 (Bublitz): f = x1x4 v x1x6 v x2x4 v x2x6 v x3x6 v x4x5 v x4x6 has C_m(f) = 7 and a single-level circuit of size 7, but every single-level formula needs >= 8 gates. That graph contains the 4-cycle 1-4-2-6.
- [W-book] p. 236: "It is reasonable to conjecture that all quadratic functions ... have optimal single-level formulas and circuits. This claim is open for circuits and has been disproved for formulas." This was written in 1987, before [LW] and [J-SLC].

**F3. Lower bound for single-level circuits on K2,2-free graphs** ([AM], as reported in [J-SLC] p. 9):
> "Amano and Maruoka [2] used this lemma [Wegener's disjunctive-complexity lemma for (h,k)-disjoint Boolean sums] to prove that C^1(f_G) >= |E| for any graph G = (V,E) with no copies of K2,2."

This covers single-level circuits only, and gives |E| rather than |E| + tau - 1.

**F4. Formula lower bound for C4-free graphs** ([J-CPC]; [J-surv] Thm 1.23; [J-book] §7.2 Thm 7.2; [J-SLC] Thm 5 states a weaker |E|/2 version from the ECCC preprint):
> "If G = (V,E) is a triangle-free graph without 4-cycles, then L+(f_G) >= |E|."

The proof is a GF(2) rank argument (Khrapchenko-Rychkov rectangles). It is about formulas (fan-out 1), counts leaves, and needs triangle-freeness as well as C4-freeness. Leafsize |E| means at least |E| - 1 gates. The star-cover formula has |E| + tau leaves, i.e. |E| + tau - 1 gates, so even for formulas the known lower bound misses the tight value by tau.

**F5. Circuits for quadratic functions of C4-free graphs are explicitly open.** [J-SLC] §8 (open problems):
> "Explicit constructions of bipartite n x n graphs G without a copy of K2,2 and with Omega(n^{3/2}) edges are well known. For these graphs Theorem 5 yields a lower bound L(f_G) = Omega(n^{3/2}). However, proving lower bounds on the monotone size of quadratic functions in the case of circuits (arbitrary fanout) is a more difficult task. Razborov's argument works well only if both minterms and maxterms are short enough. In the case of quadratic functions this is not the case ... Hence, for functions of the form f_G we need some new arguments."
>
> "Problem 24. Prove C(f_G) = Omega(n^{1+eps}) for an explicit n-vertex graph G."

Problem 22 there asks for an explicit graph with Gap(G) = n^{Omega(1)}. Problem 23 asks for which graphs C(G) = Omega(C(f_G)). [J-surv] and [J-book] repeat that superlinear monotone circuit lower bounds for explicit graphs (or for representations of them) would have strong non-monotone consequences, via the "Magnification Lemma" and Research Problems 1.37/1.38 of [J-book]. Those concern representing G rather than computing f_G, but saturated graphs make the two the same ([J-SLC] Fact 2).

**F6. The star-cover upper bound is folklore.** [J-book] §1.7 and [J-surv] give the representation OR_{u in S} (z_u AND OR_{v: uv in E} z_v), with S an arbitrary vertex cover, as a standard upper bound (stated for unbounded fan-in, where it costs <= 2n gates). The fan-in-2 count |E| + tau - 1 follows immediately; I found no source that states it with that exact count.

**F7. Other bases.** [MS] (as quoted in [J-SLC], Thm 1): over {XOR, AND, 0, 1}, C^1_mult(f_G^xor) = C_mult(f_G^xor) for every G, and every AND-optimal circuit is single-level. This is not transferable to the monotone basis, since F2 shows it fails there.

---

## Verdicts

### Item 1: Theorem PF (C4-free pseudoforests: #AND >= tau, size >= |E| + tau - 1, tight)

**Verdict: apparently new, but the upper bound and the relevant framework are known.**
- Known: the upper bound / tightness. The star-cover circuit is folklore (F6).
- Known: the single-level version of the AND bound, C^1_mult(f_G) = cc(G) = tau(G) for C4-free G (F1 plus the trivial inference).
- Known: a weaker single-level total-size bound, C^1(f_G) >= |E| for K2,2-free G, by [AM] (F3).
- Not found anywhere: a lower bound on AND gates for general (multi-level) monotone circuits for any non-trivial class of sparse graphs, or any exact C(f_G) for paths, cycles, forests or pseudoforests. The sources I read state no such theorem, and Jukna (2005/06) says circuit lower bounds for f_G "need some new arguments" (F5).
- In the literature's language, Theorem PF says that the single-level conjecture holds exactly, for both AND-count and total size, on C4-free pseudoforests. This matters because the conjecture is false in general (F2). All known counterexamples (Lenz-Wegener's 3 vs 4 example, Jukna's saturated matchings and Sylvester graphs, Bublitz's formula example) contain 4-cycles, as far as I could check. Lenz-Wegener's 3 vs 4 graph could not be inspected.
- Caveat: I could not read [LW] or [AM] in full. [LW] contains "many other results" according to [J-SLC], so a small-case exact result for some sparse graph might be in there. The abstracts and Jukna's detailed summary of both papers mention nothing about paths, trees or pseudoforests. Before claiming novelty, it is worth getting [LW] (TCS 81, Elsevier open archive) and [AM] (Algorithmica 46) by a route that can reach sciencedirect.com and link.springer.com.

### Item 2: #OR >= |E| - 1 for C4-free graphs with at most one vertex of degree >= 3

**Verdict: apparently new; the closest known tool is Wegener's disjunctive-complexity lemma as used by Amano-Maruoka.**
- The closest relatives:
  - [J-SLC] Lemma 14 (Wegener [W-book]): an (h,k)-disjoint family of Boolean sums has disjunctive complexity >= (1/kh) sum |A_i| - m/h. [AM] used it for C^1(f_G) >= |E| on K2,2-free graphs. This is OR-counting, but inside single-level circuits, where the bottom ORs compute Boolean sums.
  - Jukna's formula bound L+(f_G) >= |E| (F4) gives >= |E| - 1 gates for formulas only, and needs triangle-freeness.
- I found no lower bound of the form "#OR >= |E| - 1" for general monotone circuits for any graph class. Even for paths I found no published exact OR-count.

### Item 3: Conjecture C(f_G) >= |E| + tau(G) - 1 for every C4-free G

**Verdict: apparently new as stated; it is a strong form of open problems that Jukna posed explicitly.**
- It would imply C(f_G) >= |E| for C4-free G. For the explicit dense C4-free graphs (projective-plane incidence graphs, sum-product graphs with Theta(n^{3/2}) edges), this gives C(f_G) = Omega(n^{3/2}), which solves Jukna's **Problem 24** in [J-SLC] / SIAM J. Comput. 2006 ("Prove C(f_G) = Omega(n^{1+eps}) for an explicit n-vertex graph G") with eps = 1/2. Jukna stresses that Razborov-type methods fail for f_G because maxterms are long (F5). The conjecture is therefore at least as hard as an open problem that has stood since 2005 with no published progress I could find.
- Since the conjecture is tight for star-cover circuits, it also says that single-level (star) circuits are exactly optimal for all C4-free graphs. That is an exact single-level conjecture restricted to C4-free graphs, a class not covered by any known counterexample. I found no source that states this restricted conjecture. Jukna's formula result L+ >= |E| (triangle-free, C4-free) is the nearest proved analogue, for formulas and off by tau.
- Possible obstacle to the AND-gate analogue (#AND >= tau for all C4-free G): [J-SLC] Thm 3 shows the AND count can be exponentially smaller than the biclique cover number. That uses saturated (C4-rich) graphs, so it does not refute the C4-free version, but it shows that AND-count bounds cannot come from the biclique structure alone. Note that the conjecture in item 3 is about total size, not the AND count.

---

## Remaining gaps

1. Full texts of [LW] (TCS 81, 1991) and [AM] (Algorithmica 46, 2006 / ISAAC 2004) were not readable because sciencedirect.com and link.springer.com are blocked in this session. The Lenz-Wegener 3-vs-4 example graph should be checked for C4-freeness. It almost surely has a C4, but this is unverified.
2. Bloniarz's thesis (MIT LCS TR-238, 1979) was not readable. [W-book] cites it only for the AND-count exercise ("f in H2n can be computed with n-1 AND-gates"; smallest n with n-2) and for C(H^1_{n,n}) facts.
3. Russian-language work (Krichevskii; Sergeev; Grinchuk) was not checked beyond secondary citations.

## Addendum: full text of Lenz-Wegener (TCS 81 (1991) 257-268) read

The full journal version was read (12 pages). What it contains, relative to our results:

- **Theorem 2.1.** The single-level AND complexity C^1_∧(f_G) equals the biclique cover number of G. In a C4-free graph every biclique is a star, so C^1_∧(f_G) = tau(G). This confirms the inference in the main text.
- **Proposition 2.3.** C_∧(f_G) = C^1_∧(f_G) = 2 for the graph of Fig. 2, with edges 14, 15, 24, 25, 26, 35, 36. The lower bound is proved by "the well-known elimination method". This graph contains the C4 1-4-2-5.
- **Theorem 4.2.** For G(n) = floor(n/3) disjoint triangles, C_∧(f_G) = 2 floor(n/3). The lower bound comes from eliminating two AND gates per triangle by setting x_1 := 1 and the other two variables := 0. **This is a special case of the AND half of Theorem PF**, since disjoint triangles form a C4-free pseudoforest with tau = 2 per triangle. So PF's AND half is known for disjoint triangles. Its leaf step (our Lemma AL) is the same elimination method.
- **Theorem 5.3.** The counterexample to the single-level conjecture (C_∧ = 3 < 4 = C^1_∧) is the 8-vertex graph of Fig. 3. Its vertices 1, 3, 5, 7 form a K4, so **it contains C4s**. This confirms that the known counterexamples avoid the C4-free class.
- **Section 6, open problem (6).** "Does the single level conjecture hold for quadratic functions and the monotone circuit complexity, i.e. if we count conjunctions *and* disjunctions?" Theorem PF, combined with L_meta_599, gives a **positive answer for C4-free pseudoforests**: the star-cover single-level circuit of size |E| + tau - 1 is optimal for total size. Problems (3) and (7) concern worst-case values and are not touched.
- Nothing on paths, cycles C_n (n >= 5), forests or pseudoforests beyond the triangle example. Nothing on the number of OR gates.

**Updated verdict for item 1 (Theorem PF):**
- AND half: known for forests (folklore elimination) and for disjoint triangles (LW Thm 4.2). For cycles C_n with n >= 5, and for general C4-free pseudoforests, apparently new. A single elimination step does not suffice there, which is why Lemma AND-core is needed.
- Total-size statement: apparently new. It is a restricted positive case of LW's open problem (6).

Amano-Maruoka (Algorithmica 2006) is still unread.
