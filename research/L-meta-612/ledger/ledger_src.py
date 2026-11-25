"""Source of the L-meta-612 claim ledger. build_ledger.py turns this into ledger.json and ledger.md,
verifies every witness circuit on all 2^n inputs and attaches the smallest counterexamples found by
falsify.py (sanity_report.json) and their store ids.

Field meanings
  id        short stable identifier
  st        status: PROVED | LEAN | SAT | REFUTED | OPEN | DATA (open, machine evidence only) | MOOT
  scope     (graph class, circuit class); circuit class is one of: any | reduced | minimum | STAR-ALL | ...
  where     pointer (file and section) to the proof / source
  ev        evidence or remark
  uses      claims it depends on;  implies: claims it would give
  fz        name of the ready-made falsify.py predicate (None if not statable that way)
  wit       hand-entered witness circuit(s) (string form); verified by build_ledger.py
  c3        role for the target MAIN-C3 ("612 for C4-free max degree <= 3"):
            'goal' | 'open-on-path' | 'proved-on-path' | 'dead-route' | 'base-case' | ''
"""

L = []


def C(**k):
    k.setdefault("uses", [])
    k.setdefault("implies", [])
    k.setdefault("fz", None)
    k.setdefault("wit", [])
    k.setdefault("c3", "")
    k.setdefault("ev", "")
    L.append(k)


# ------------------------------------------------------------------ targets
C(id="MAIN", st="OPEN", title="L-meta-612",
  stmt="Every monotone fan-in-2 AND/OR circuit computing f_G, G C4-free with E nonempty, has size >= Phi(G) = |E| + tau(G) - 1.",
  scope=("C4-free", "any"), where="README.md, argument.md", fz="main",
  ev="0 violations on the whole store (225k verified circuits) and in every fuzzing campaign. Tight by F-U.",
  implies=["P24"], c3="goal")
C(id="MAIN-C3", st="OPEN", title="L-meta-612 for max degree <= 3",
  stmt="MAIN restricted to C4-free G with maximum degree <= 3 (class C3, closed under vertex deletion).",
  scope=("C4-free, Delta <= 3", "any"), where="deg3/deg3.md, subcubic.md",
  ev="Proved for every subcubic pseudoforest (THM-PF). Open from the first non-pseudoforest graphs; see subcubic.md for the smallest open graphs.",
  uses=["THM-PF"], c3="goal")
C(id="P24", st="PROVED", title="MAIN implies Jukna's Problem 24",
  stmt="MAIN (even OR-split alone, or LEM-D via THM-R) gives C(f_G) = Omega(n^{3/2}) for the PG(2,q) incidence graph, answering Jukna 2005 Problem 24 with eps = 1/2.",
  scope=("C4-free", "any"), where="core/core.md section 0", ev="Shows that MAIN for unbounded degree is at least as hard as an explicitly open problem; MAIN-C3 is not affected (|E| = O(n)).")

# ------------------------------------------------------------------ foundations
C(id="F-U", st="PROVED", title="Upper bound (star cover)",
  stmt="f_G has a circuit of size |E| + tau - 1: OR over t in a minimum cover T of (x_t AND OR_{N_t} x_w).",
  scope=("any graph", "-"), where="argument.md 1 U", ev="Single-level, STAR-ALL; folklore (literature.md F6).", c3="proved-on-path")
C(id="F-R", st="PROVED", title="Restriction accounting",
  stmt="Substituting x_v := b and removing constant, copy and dead gates leaves a circuit for f|x_v=b of size s - elim.",
  scope=("any", "any"), where="argument.md 1 R; t2.md 0 (functional red)", c3="proved-on-path")
C(id="F-F", st="PROVED", title="Forced variables (Fact F)",
  stmt="size(f_{G,F}) >= size(f_{G-F}) + |F| - [E(G-F) empty] for f_{G,F} = f_G OR OR_F x_w; OR version: #OR >= #OR_min(f_{G-F}) + |F|.",
  scope=("any", "any"), where="argument.md 1 F; core.md 2", c3="proved-on-path")
C(id="F-P", st="PROVED", title="OR-prefix (Fact P)",
  stmt="After constant removal every minimal AND gate is OR_A AND OR_B with A, B nonempty.",
  scope=("any", "any"), where="argument.md 1 P", c3="proved-on-path")
C(id="F-C", st="PROVED", title="Edge creation (Fact C)",
  stmt="For every edge uv some AND gate h1&h2 has h1(e_u)=h2(e_v)=1, h1(e_v)=h2(e_u)=0; rectangles (S1\\S2)x(S2\\S1) cover E; with C4-freeness a rectangle with both sides >= 2 carries a junk pair.",
  scope=("any / C4-free", "any"), where="argument.md 1 C", c3="proved-on-path")
C(id="F-RTOT", st="PROVED", title="R-TOT-F / R-TOT-G induction frameworks",
  stmt="If, for a hereditary class K, every non-star G in K and every reduced C has a good option rho (elim(rho) >= Phi(G) - LB(rho); rho among A(v): x_v:=0, N(v): x_N[v]:=0, B(v): x_v:=1, or any (S0,S1) with S1 independent), then MAIN holds on K.",
  scope=("hereditary K", "reduced"), where="t2.md 0, t3.md 0; deg3.md 1 (R-OR, R-AND, R-TOT)", uses=["F-F", "F-R"],
  ev="The vehicle for T2, T2F, mANB, T2-LR; the min-cex version only needs minimum circuits of size Phi-1.", c3="proved-on-path")
C(id="F-ROR", st="PROVED", title="R-OR and R-AND (deg3 frameworks)",
  stmt="R-OR: if every G in K with min degree >= 2 and every reduced C have X != {} with sav(X) >= need_OR(X), then #OR >= |E|-1 on K. R-AND: same with sa(X) >= tau(G)-tau(G-X) gives #AND >= tau.",
  scope=("hereditary K", "reduced"), where="deg3.md 1")
C(id="THM-R", st="PROVED", title="Theorem R: Lemma D implies (OR)",
  stmt="LEM-D implies OR-split for every C4-free G (induction over all circuits, leaves paid by release_exists).",
  scope=("C4-free", "any"), where="or-bound/or.md 2", uses=["L599"], implies=["OR-split"])
C(id="NF-EQ", st="PROVED", title="MAIN <=> some minimum circuit is STAR-ALL",
  stmt="For C4-free G: size(f_G) >= Phi(G) iff f_G has a minimum circuit that is STAR-ALL (N1, N2, N3 at every AND gate).",
  scope=("C4-free", "minimum"), where="girth5/girth5.md 3", uses=["THM-S", "F-U"])
C(id="COR-M", st="PROVED", title="Structure of a minimal counterexample",
  stmt="A vertex-minimal counterexample (size Phi-1) has: every leaf unique at a holder of degree >= 3 with delta_v = 1 and a single OR reader; no tree component; first-order bounds F_v + min(k_and,2) <= deg v + delta_v - 1, etc.",
  scope=("C4-free", "minimum"), where="t2.md 1 Corollary M; t3.md Theorem L", uses=["LEM-READER", "LEM-LEAF", "LEM-CYCLE"],
  c3="proved-on-path")

# ------------------------------------------------------------------ proved theorems on classes
C(id="L599", st="LEAN", title="(OR) for C4-free pseudoforests (L_meta_599)",
  stmt="If G is a C4-free pseudoforest, every Monotone2 circuit has #OR >= |E| - 1.",
  scope=("C4-free pseudoforest", "any"), where="accepted Lean L_meta_599 (brilliant-hq/pequalnp-proofs); or.md 1", c3="proved-on-path",
  ev="The only sparsity use is regular_of_no_leaf; the circuit lemmas (release_exists, pay_core, no_module) are graph-free.")
C(id="AND-PF", st="LEAN", title="(AND) for C4-free pseudoforests",
  stmt="If G is a C4-free pseudoforest, every monotone fan-in-2 circuit has #AND >= tau(G).",
  scope=("C4-free pseudoforest", "any"), where="t9/t9.md 1-3; research/lean/PF_AND.lean (PEqualNP.Outside.PF_AND, no sorry); review9/",
  uses=["LEM-X1", "LEM-AL", "LEM-ANDCORE"], c3="proved-on-path")
C(id="THM-PF", st="LEAN", title="Theorem PF: MAIN for C4-free pseudoforests",
  stmt="MAIN holds for every C4-free pseudoforest (= AND-PF + L599).",
  scope=("C4-free pseudoforest", "any"), where="t9/t9.md 3; lean/PF_AND.lean + L_meta_599", fz="PF", uses=["AND-PF", "L599"],
  implies=["THM-F1", "THM-F2", "THM-P1"], c3="proved-on-path",
  ev="Supersedes the partial-sun SAT base cases of t4/t6 (C5{012}, C6{01}, C6{03}, C7{012}, C7{014}, C8{01}, C6{0123}; C8{03} closed).")
C(id="THM-F1", st="PROVED", title="MAIN for forests", stmt="MAIN for every forest.", scope=("forest", "any"),
  where="t2.md 1 Theorem F1", uses=["LEM-LEAF", "F-RTOT"], c3="proved-on-path")
C(id="THM-F2", st="PROVED", title="MAIN for trees+cycles (max degree <= 2)",
  stmt="MAIN for every C4-free G whose components are trees or cycles; in particular max degree <= 2.",
  scope=("components trees/cycles", "any"), where="t2.md 1 Theorem F2", uses=["LEM-CYCLE", "LEM-LEAF", "F-RTOT"], c3="proved-on-path")
C(id="THM-P1", st="MOOT", title="Full suns are not minimal counterexamples",
  stmt="No disjoint union of full suns and bare cycles is a minimal pseudoforest counterexample (Lemma R2 option x_P := 1).",
  scope=("pseudoforest", "minimum"), where="t4/t4.md 2", ev="PROVED; superseded by THM-PF.")
C(id="THM-S", st="PROVED", title="Theorem S (STAR-ALL bound)",
  stmt="Every STAR-ALL circuit for f_G (G C4-free) has size >= Phi(G); in fact #AND >= tau and #OR >= |E|-1. Contains Amano-Maruoka's single-level bound.",
  scope=("C4-free", "STAR-ALL"), where="girth5/girth5.md 2; core.md LIT-2", fz="thmS", c3="proved-on-path")
C(id="THM-S2", st="PROVED", title="Theorem S2 (N2 not needed)",
  stmt="Every circuit satisfying N1 and N3 at every AND gate has size >= Phi (G C4-free).",
  scope=("C4-free", "N1+N3"), where="nf/nf.md 1", fz="thmS2", uses=["LEM-L"], c3="proved-on-path",
  ev="A minimal counterexample must violate N1 or N3; used as the --viol constraint in petersen19/enc5.py.")
C(id="LEM-A", st="PROVED", title="Lemma A: clean circuits have #AND >= tau",
  stmt="If every AND gate is clean (N3), #AND >= #creators >= tau (creator centres form a vertex cover).",
  scope=("C4-free", "clean"), where="nf/nf.md 1", fz="lemmaA")
C(id="LEM-L", st="PROVED", title="Lemma L (empty links)", stmt="|Z| >= m0 - 1 - lnkA for any circuit.",
  scope=("any", "any"), where="nf/nf.md 1")
C(id="THM-F", st="PROVED", title="Theorem F: Lemma D with at most one hub",
  stmt="LEM-D holds when delta >= 2 and at most one vertex has degree >= 3; with THM-R: #OR >= |E|-1 for every C4-free graph with at most one vertex of degree >= 3.",
  scope=("C4-free, <= 1 vertex of degree >= 3", "reduced"), where="lemma-d/lemD.md 3", fz="thmF", uses=["LEM-L4L5", "THM-R"],
  ev="OR half only; the AND half is open on this class unless the graph is a pseudoforest.")
C(id="COR-A2", st="PROVED", title="Lemma D, case (a), special class",
  stmt="LEM-D holds via a degree-2 vertex when H (degree >= 3 vertices) is independent, no V2 vertex has N(v) in V2, and at most one has N(v) in H.",
  scope=("C4-free, delta = 2", "reduced"), where="lemma-d-case-a/lemDa.md 2", ev="Class not hereditary.")
C(id="THM-SL", st="PROVED", title="Corollary SL (AND-depth 1)",
  stmt="In a reduced circuit of AND-depth 1, A(c) is paid by syntactic eliminations at every star centre c.",
  scope=("C4-free", "AND-depth 1"), where="t8/t8.md 2", uses=["LEM-DV2"])
C(id="PROP-F", st="PROVED", title="Proposition F (2-slice subadditivity; formulas)",
  stmt="w(p) = |E_p| + |S_p| - 1 grows by <= 1 at OR gates and not at forest-rectangle AND gates; hence formulas with forest rectangles have #OR >= |E|-1, and clean formulas have size >= Phi.",
  scope=("C4-free", "formulas"), where="t10/t10.md 2", ev="Fan-out is the entire obstruction for circuits.")
C(id="THM-AB", st="PROVED", title="Theorems A, B and Lemmas 3-6 on star gates",
  stmt="For a minimal star g = x_a & OR_B: A(a) is good if F_a >= deg a, or F_a = 1 with a private OR tree (Thm A); or with a private tree and ATT (Thm B, minimum circuits).",
  scope=("any / C4-free", "reduced (A), minimum (B)"), where="estar/proof.md 3; star-case/star.md 1-3")
C(id="LEM-S", st="PROVED", title="Lemma S (one-sided minimal AND)",
  stmt="If h = OR_A & OR_B is a minimal AND gate with A\\B = {a}, then x_a := 0 removes an AND gate.",
  scope=("any", "reduced"), where="deg3/deg3.md 3")
C(id="LEM-X1", st="PROVED", title="Lemma X1", stmt="If f depends on x_v and f|x_v=1 != 1, then x_v := 1 removes an AND gate.",
  scope=("any", "any"), where="t9/t9.md 1")
C(id="LEM-AL", st="PROVED", title="Lemma AL (leaf, AND)", stmt="Leaf v at u: alpha(G) >= 1 + alpha(G-u-v) and tau(G-u-v) = tau(G)-1.",
  scope=("any", "any"), where="t9/t9.md 1", uses=["LEM-X1"])
C(id="LEM-ANDCORE", st="PROVED", title="Lemma AND-core",
  stmt="G C4-free, all non-isolated degrees >= 2, C dead-free: some v has an AND reader of x_v or |Ex(v)| >= 2 exits.",
  scope=("C4-free, delta >= 2", "dead-free"), where="t9/t9.md 2",
  ev="Holds for all C4-free graphs; the AND induction stalls only when the returned vertex has degree >= 3 and two exits (need deg v exits). This is the exact place where AND-C3 is open.")
C(id="LEM-READER", st="PROVED", title="Reader Lemma (first-order)",
  stmt="elim(x_v:=0) >= |D_v| + |dD_v| >= F_v + min(k_and,2); elim(x_v:=1) >= |R_v| + |dR_v| >= F_v + min(k_or,2).",
  scope=("any", "reduced"), where="t2/t2.md 1")
C(id="LEM-LEAF", st="PROVED", title="Leaf Lemma", stmt="At a leaf v with delta_v = 0 or deg u <= 2, A(v) or B(v) is good.",
  scope=("any non-star", "reduced"), where="t2/t2.md 1", uses=["LEM-READER"])
C(id="LEM-CYCLE", st="PROVED", title="Cycle Lemma", stmt="C4-free, min degree >= 2: some v has elim(x_v:=0) >= 3 or elim(x_v:=1) >= 4.",
  scope=("C4-free, delta >= 2", "reduced"), where="t2/t2.md 1", uses=["L599", "LEM-READER"])
C(id="LEM-N'", st="PROVED", title="Lemma N' and Theorem L (bad leaves)",
  stmt="Leaf v at u with an OR reader not reading x_u: elim(x_u:=0, x_v:=1) >= F_u + 2. In a min cex a bad leaf has the star or ORp shape (Theorem L).",
  scope=("any", "reduced / minimum"), where="t3/t3.md 1")
C(id="LEM-R2", st="PROVED", title="Lemma R2 (x_S := 1 counting)", stmt="elim(x_S:=1) >= |S| + r1 for S independent.",
  scope=("any", "any"), where="t4/t4.md 1")
C(id="LEM-PN", st="PROVED", title="Lemmas PN, AT, INS (partial suns)", stmt="Private-neighbour, AND-type and insertion structure lemmas.",
  scope=("any / pseudoforest min cex", "any / minimum"), where="t6/t6.md 1", ev="Moot for pseudoforests after THM-PF; PN and AT are graph-general.")
C(id="LEM-C2", st="PROVED", title="Lemma C2, C2', ST (configuration (2), set Reader Lemma with Top)",
  stmt="Structure of a minimal x_a & x_b gate with A, B bad at both ends; elim(x_X:=0) >= |D_X u dD_X u Top_X| - 1.",
  scope=("any", "reduced"), where="t5/t5.md 1")
C(id="LEM-DG", st="PROVED", title="Lemma DG (dead-gate identity)", stmt="LD(rho) = |Z u L| = F_rho + arcs_I + sum_{z in Z}(r(z)-1).",
  scope=("any", "reduced"), where="t8/t8.md 1")
C(id="LEM-DV2", st="PROVED", title="Theorem DV2 (A option at c)",
  stmt="LD_A(c) >= k_Z + k_L + |N_D(c)| - pen(c); A(c) is paid if pen(c) <= k_Z - delta_c and the carrier hypotheses hold.",
  scope=("C4-free", "reduced"), where="t8/t8.md 2", uses=["LEM-DG"])
C(id="LEM-P", st="PROVED", title="Lemma P / P2 (second-use lemma)",
  stmt="A node carrying two neighbours of c as singletons forces, on the first AND above it, an N1/N2/N3 violation or a re-creation gate.",
  scope=("C4-free", "any"), where="t10/t10.md 1")
C(id="LEM-L4L5", st="PROVED", title="Lemmas L1-L7 (charges)", stmt="Multi-vertex changed-domination, bottleneck property, dominated chains, L4/L5 (at most one single-charged vertex per minimal OR gate), L6/L7 (type R).",
  scope=("C4-free, delta >= 2", "reduced"), where="lemma-d/lemD.md 1-2")
C(id="LEM-LDA", st="PROVED", title="lemDa structure lemmas (P1-P4, A1, Theorem N)",
  stmt="Factorisation when every V2 vertex is single-charged; Theorem N builds all-V2-single-charged circuits when G[H] has an edge.",
  scope=("C4-free, delta = 2", "reduced"), where="lemma-d-case-a/lemDa.md 1-2")
C(id="LIT-LW42", st="PROVED", title="Lenz-Wegener Thm 4.2", stmt="C_AND(f_G) = 2 floor(n/3) for disjoint triangles.",
  scope=("disjoint triangles", "any"), where="literature.md addendum", ev="Special case of AND-PF.")

# ------------------------------------------------------------------ SAT base cases
C(id="SAT-N6", st="SAT", title="MAIN for all C4-free graphs on <= 6 vertices",
  stmt="No circuit of size Phi-1 exists for each of the 43 C4-free graphs without isolated vertices on <= 6 vertices.",
  scope=("n <= 6", "any"), where="argument.md 2; data/n6.txt (run1.py, CaDiCaL)", c3="base-case")
C(id="SAT-N7", st="SAT", title="MAIN for 46 of the 73 C4-free graphs on 7 vertices",
  stmt="UNSAT at Phi-1 for 46 graphs (<= 6 edges, or 7 edges with tau <= 3); 27 graphs timed out at 900 s.",
  scope=("n = 7", "any"), where="argument.md 2; data/s7.txt, data/g7s.txt", c3="base-case",
  ev="Of the 27 timeouts, the pseudoforests are now closed by THM-PF; see subcubic.md for the subcubic ones left open.")
C(id="SAT-PETSUB", st="SAT", title="Exact Phi for the non-pseudoforest induced subgraphs H7, H8a, H8b of Petersen",
  stmt="size(f_H) = Phi(H) for H7 (Phi 11), H8a (Phi 13, DRAT-checked) and H8b (Phi 12).",
  scope=("H7, H8a, H8b", "any"), where="petersen19/README.md 2, proven.json, logs/", c3="base-case", uses=["THM-PF", "THM-S2"])
C(id="SAT-H9", st="OPEN", title="MAIN for H9 = Petersen minus a vertex",
  stmt="size(f_H9) >= 16 = Phi.",
  scope=("H9 (n=9, |E|=12)", "any"), where="petersen19/logs/H9.log", c3="base-case",
  ev="UNSAT for every s <= 14 (enc5 with restriction hierarchy, unconditional); s = 15 running (kissat timeout 5400 s, re-run in progress).")
C(id="PET-EXACT", st="OPEN", title="Petersen: is size(f_P) = 20?",
  stmt="size(f_P) >= 20 = Phi(P).",
  scope=("Petersen", "any"), where="petersen19/README.md; petersen/sat19/README.md", c3="base-case",
  ev="UNSAT for s <= 15 without using H9 (P_noH9, unconditional); s = 16 running. Known upper bound 20, attained by STAR-ALL and by 13-OR non-STAR-ALL circuits.")

# ------------------------------------------------------------------ open statements / routes
C(id="AND-split", st="OPEN", title="(AND) #AND >= tau",
  stmt="Every circuit for f_G (G C4-free) has #AND >= tau(G).",
  scope=("C4-free", "any"), where="argument.md 2; nf.md 3; t9.md", fz="and_tau",
  ev="PROVED for pseudoforests (AND-PF) and clean circuits (LEM-A). 0 violations on the store. Alone it no longer implies MAIN (OR-split is false), but 'AND >= tau + (|E|-1-#OR)' type trades are what the Petersen 13-OR circuits show.",
  c3="")
C(id="AND-C3", st="OPEN", title="(AND) on max degree <= 3",
  stmt="AND-split restricted to C3.", scope=("C4-free, Delta <= 3", "any"), where="t9.md 3 (remark), deg3.md 6",
  ev="AND-core leaves exactly the case of a degree-3 vertex with two exits; R-AND with X = v or a pair survives all fuzzing (deg3.md 6). Not sufficient for MAIN-C3 because OR-C3 is false.",
  uses=["LEM-ANDCORE"], fz="and_tau")
C(id="T2", st="DATA", title="Lemma T2 (deg3.md): the surviving route for C3",
  stmt="G in C3 with an edge, not a star, C reduced: some v has tot(v) >= Phi(G)-Phi(G-v) with G-v not edgeless, or tot(N[v]) >= Phi(G)-Phi(G-N[v]) with G-N[v] not edgeless (tot = total functional eliminations under x_X := 0).",
  scope=("C4-free, Delta <= 3", "reduced"), where="deg3/deg3.md 7", fz="T2", uses=["F-RTOT"], implies=["MAIN-C3"],
  ev="0 violations on the store (225k circuits, also non-subcubic graphs), in deg3 fuzzing on 17 graphs (fewest good options: 1, net) and in seeded adversarial walks here (Petersen, Pet-v, n8, constrS7, 2tri+bridge, net, C5{012}; ~38k distinct circuits). Leaves need the N[v] option (P6). Only minimum circuits of a min cex (size Phi-1) are needed. Its structural strengthening T2-LR is now refuted.",
  c3="open-on-path")
C(id="T2F", st="DATA", title="T2F: some A, N or B option is good",
  stmt="G C4-free non-star, C reduced: some v has A(v), N(v) or B(v) good (B(v): x_v := 1, need Phi(G) - deg v - Phi(G-N[v])).",
  scope=("C4-free", "reduced"), where="t2/t2.md 0, 2", fz="T2F", uses=["F-RTOT"], implies=["MAIN"], c3="open-on-path",
  ev="Implied by T2 on C3 (weaker requirement). 0 violations on the store and on seeded adversarial walks (Petersen, Pet-v, n8, constrS7, 2tri+bridge, net, C5{012}).")
C(id="mANB", st="DATA", title="mANB: good option at a minimal-AND support vertex",
  stmt="Some v in the support of a minimal AND gate has a good A, N or B option.",
  scope=("C4-free", "reduced"), where="t2/t2.md 5", fz="mANB", implies=["T2F"], c3="open-on-path",
  ev="0 violations on the store and on t2 fuzzing (14 graphs; fewest good options 1: net, Petersen, sun5). Dropping N refutes it (E*+); requiring every minimal AND refutes it.")
C(id="T2-LR", st="REFUTED", title="T2-LR: structural payment (rule R + Top merge); also T2-LR(g5)",
  stmt="Some A/N/B option has LR(rho) = size - |ruleR(C|rho)| + (#Top survivors - 1) >= need(rho).",
  scope=("C4-free (and girth >= 5)", "reduced"), where="t7/t7.md 3; t10.md 0 (T2-LR(g5)); refuted here (ledger/witnesses_new.jsonl)",
  fz="T2LR", c3="dead-route",
  wit=["10=4|7 11=5|3 12=3|7 13=5|4 14=6|11 15=14&8 16=11&10 17=0|6 18=16&13 19=18|2 20=12&19 21=13&0 22=21|20 23=1|22 24=22|15 25=17&23 26=24|25 27=2&23 28=6|10 29=28&9 30=27|29 31=26|30"],
  ev="NEW (this ledger): refuted on Petersen at size 22 = Phi+2 (reduced; max LR - need = -1), found by falsify.py --fresh-from-store and re-checked with the original t2lib/lib7 code. T2F still holds on it (A(1), N(0), N(2), N(3), N(6), N(7) are good under functional reduction), so any payment proof must count functional (not only syntactic) eliminations. Before this, 0 violations on 225k store circuits and on t7/t10 LR fuzzing.")
C(id="E*opt", st="OPEN", title="Lemma E* for minimum circuits",
  stmt="E* (some minimal AND gate, v in its support, b with elim >= Phi(G)-Phi(G_b)) for minimum-size circuits only.",
  scope=("C4-free", "minimum"), where="estar/proof.md 2", implies=["MAIN"], c3="open-on-path",
  ev="Not refuted; any proof must use global minimality (E* and E*+ fail on non-minimum circuits).")
C(id="DV2-PHI", st="DATA", title="DV2-Phi (girth >= 5)",
  stmt="If no vertex of C is DV2-certified then size(C) >= Phi+1 (girth >= 5).",
  scope=("girth >= 5", "reduced"), where="t8.md 3b, t10.md 0, 4", implies=["MAIN"],
  ev="Every girth-5 circuit of size <= Phi tested has a certified vertex (7,053 + fuzzing on 16 graphs incl. Petersen). Vacuous at size <= Phi-1 if MAIN holds; needs a waste-charging proof.")
C(id="Z_k", st="OPEN", title="Claim Z_k (t3)",
  stmt="H C4-free, |W| = k >= 2 with no common neighbours in H: every circuit for f_H containing a node z with OR_W <= z <= OR_W v f_{H-W} has >= Phi(H)+k-1 gates.",
  scope=("C4-free", "any"), where="t3/t3.md 1.2(d)", uses=["MAIN"], ev="Implied by MAIN; a star-shape min cex violates Z_2. DATA: no violation (Z-form nodes appear only at size >= Phi(H)+1).")
C(id="NW-LEAF", st="DATA", title="Bad leaf: some N(w), w in N(u)-v, is good",
  stmt="At a locally-bad leaf v at u, some w in N(u)\\{v} has N(w) good.", scope=("C4-free", "reduced"), where="t3/t3.md 1.3",
  ev="17,463/17,463 locally-bad leaves (t3 locpool). Moot for pseudoforests; relevant for subcubic graphs with leaves.", c3="open-on-path")
C(id="NW-CONF2", st="DATA", title="Configuration (2): some N(w), w in N(a) u N(b) - {a,b}, is good",
  stmt="For a minimal x_a & x_b gate with F_a, F_b >= 2 and A, B bad at both ends, some w at distance 1 has N(w) good.",
  scope=("C4-free", "reduced"), where="t5/t5.md 2", ev="785/785 instances (Petersen, Pet-v, constrS7, ...).", c3="open-on-path")
C(id="RULE-S", st="DATA", title="Rule S (estar): every minimal star contains a good vertex",
  stmt="Every minimal AND gate x_a & OR_B (a not in B) has a good vertex in {a} u B (A or B option, rule R).",
  scope=("C4-free", "minimum"), where="estar/proof.md 4; star-case/star.md",
  ev="0 failures on minimum circuits n <= 7. LD-paid variants V4/V5 are refuted at Phi+2 (t10), so only the minimum-circuit form is alive.")
C(id="S2-SHARED", st="DATA", title="Shared star trees: every support vertex of a shared tree gate has (v,1) good",
  stmt="In sub-case S2 (F_a = 1, tree shared), every v in the support of a shared tree gate has B(v) good.",
  scope=("C4-free", "minimum"), where="star-case/star.md 4", ev="270/270 (net and extensions only).")
C(id="LDA-HUB", st="OPEN", title="lemDa (ii): a hub pays when all degree-2 vertices are single-charged",
  stmt="If every V2 vertex is single-charged then some hub h has ch(h) >= deg h.", scope=("C4-free, delta = 2", "reduced"),
  where="lemma-d-case-a/lemDa.md 3", ev="Holds in every construction; Lemma D (which it would serve) is refuted anyway.")

# ------------------------------------------------------------------ refuted
C(id="OR-split", st="REFUTED", title="(OR) #OR >= |E| - 1 for every C4-free G",
  stmt="Every circuit for f_G (G C4-free) has #OR >= |E|-1.", scope=("C4-free", "any"),
  where="petersen/README.md; deg3/deg3.md 5.1", fz="or_E1", c3="dead-route",
  wit=["8=0|2 9=1|2 10=0|3 11=1|3 12=4&8 13=5&9 14=6&10 15=8&9 16=10&15 17=7|16 18=11&17 19=12|13 20=19|14 21=20|18",
       "10=0|9 11=5|9 12=0|6 13=5|6 14=3|10 15=4&14 16=2|11 17=7&16 18=2|12 19=1&18 20=10&11 21=12&20 22=8|21 23=13&22 24=2|8 25=3&24 26=15|17 27=26|19 28=27|23 29=28|25"],
  ev="Smallest: the 8-vertex graph n8 (subcubic, delta = 2, girth 5, no cubic component), size 14 = Phi+1, #OR 8. Petersen: size 20 = Phi with #OR 13, #AND 7. Each saved OR costs an extra AND.",
  implies=[])
C(id="OR-C3", st="REFUTED", title="(OR) on max degree <= 3 (and on C3' without cubic components, and on girth >= 5)",
  stmt="OR-split restricted to C3, to C3' or to girth >= 5.", scope=("C4-free, Delta <= 3 / girth >= 5", "any"),
  where="deg3.md 5.1 (Petersen); petersen/README.md (n8)", fz="or_E1", c3="dead-route",
  wit=["8=0|2 9=1|2 10=0|3 11=1|3 12=4&8 13=5&9 14=6&10 15=8&9 16=10&15 17=7|16 18=11&17 19=12|13 20=19|14 21=20|18"],
  ev="deg3.md says Petersen is the smallest known (OR) counterexample; the n8 circuit of petersen/README.md is smaller, subcubic and girth 5. t10.md 4 still lists '(OR-g5) + (AND-g5)' as a route: it is dead (n8 and Petersen have girth 5).")
C(id="SPLIT-C3", st="REFUTED", title="The split route (OR)+(AND) on C3", stmt="Proving MAIN-C3 as OR-C3 plus AND-C3.",
  scope=("C4-free, Delta <= 3", "any"), where="deg3/deg3.md 5, 7", uses=["OR-C3"], c3="dead-route", ev="Dead because OR-C3 is false.")
C(id="LEM-D", st="REFUTED", title="Lemma D (ch version)",
  stmt="G C4-free, min degree >= 2, C reduced: some v has ch(v) >= deg v.", scope=("C4-free, delta >= 2", "reduced"),
  where="or-bound/or.md 2; refuted in deg3.md 5.2, petersen/README.md", fz="lemD_ch", c3="dead-route",
  ev="Smallest: constrS7 (n = 7) at size 14 = Phi+2 (ch <= sav, and sav fails). The Petersen gadget (petersen/README.md, size 24) also refutes it. Implied OR-split via THM-R, so OR-split's refutation already kills it.")
C(id="LEM-D-sav", st="REFUTED", title="sav-Lemma D / R-OR with single vertices",
  stmt="G C4-free, min degree >= 2, C reduced: some v has sav(v) >= need_OR(v).", scope=("C4-free, delta >= 2", "reduced"),
  where="deg3/deg3.md 5.2", fz="lemD_sav", c3="dead-route",
  wit=["7=1|5 8=0&7 9=2|8 10=5|9 11=7&10 12=6|11 13=9&12 14=10&6 15=3|14 16=4|13 17=0|1 18=17&16 19=12&15 20=19|18"])
C(id="DMIN", st="REFUTED", title="(Dmin): a minimum-degree vertex has sav >= deg",
  stmt="G C4-free, min degree >= 2: some minimum-degree vertex v has sav(v) >= deg v.", scope=("C4-free, delta >= 2", "reduced"),
  where="core/core.md 1 (listed as unrefuted)", fz="Dmin", c3="dead-route",
  ev="core.md lists it as the unrefuted candidate; it is refuted by the constrS7 circuit of deg3.md 5.2 (a weaker statement already fails there).")
C(id="T(a)", st="REFUTED", title="lemDa target T(a): some degree-2 vertex has ch >= 2",
  stmt="Case (a) of Lemma D (delta = 2, >= 2 hubs): some v in V2 has ch(v) >= 2.", scope=("C4-free, delta = 2", "reduced"),
  where="lemma-d-case-a/lemDa.md 1",
  wit=["7=6|1 8=2&7 9=5|6 10=3&9 11=0|1 12=4&11 13=1|5 14=0&13 15=5&6 16=8|10 17=16|12 18=17|14 19=18|15"],
  ev="Construction S on constrS7, size 13 = Phi+1. Also 'some min-degree vertex is ch-good' is false there.")
C(id="LEM-M'", st="REFUTED", title="Lemma M' / M0: a one-vertex restriction removes an AND gate",
  stmt="Every reduced circuit has v with sa(v) >= tau(G) - tau(G-v) (Lemma M': when every vertex lies in a minimum cover, some x_v := 0 removes an AND gate).",
  scope=("C4-free", "reduced"), where="or.md 3; refuted deg3.md 2.1", fz="Mprime", c3="dead-route",
  wit=["6=2|4 7=5|2 8=1|0 9=3|5 10=6&8 11=3|10 12=11&7 13=4|12 14=0|12 15=9&13 16=1|2 17=14&16 18=17|15"],
  ev="deg3.md's witness: two triangles + bridge, size 13. The store's smallest is on P6 (a tree, every vertex in a minimum cover) at size 11 = Phi+4.")
C(id="T2-A", st="REFUTED", title="One-vertex direct induction (A options only)",
  stmt="Non-star G: some v (G-v with an edge) has tot(v) >= Phi(G)-Phi(G-v).", scope=("C4-free", "reduced"),
  where="deg3.md 2.1; t2.md 2", fz="T2A", c3="dead-route",
  ev="Fails on 2tri+bridge (size 13), P6, C7; the store's smallest is the net at size 11 = Phi+3.")
C(id="ADJ-PAIR", st="REFUTED", title="Adjacent degree-2 pair lemma",
  stmt="deg u = deg v = 2, uv in E, G-{u,v} with an edge: sav({u,v}) >= 3.", scope=("C4-free", "reduced"), where="deg3.md 2.2",
  wit=["7=0&1 8=5|7 9=0&8 10=4|9 11=2|10 12=3&11 13=8&10 14=12|13 15=1|2 16=6&15 17=14|16"], ev="C7, size 11 = Phi+1, pair {4,5}.")
C(id="R-AND-vN", st="REFUTED", title="R-AND with X = v or N[v]",
  stmt="Some v has sa(v) >= need_AND(v), or sa(N[v]) >= need_AND(N[v]) with G-N[v] not edgeless.", scope=("C4-free", "reduced"),
  where="deg3.md 6; data/found.txt",
  wit=["6=2|1 7=5|0 8=7&6 9=3|8 10=9|6 11=4|2 12=0|8 13=8|1 14=0|11 15=13|12 16=10&14 17=16&15"], ev="net, size 12; also C6+2 pendants and C7.")
C(id="E*", st="REFUTED", title="Lemma E* (argument.md 4)",
  stmt="Some minimal AND gate OR_A & OR_B, v in A u B and b with rule-R elimination >= Phi(G) - Phi(G_b), for every circuit without constant or copy gates.",
  scope=("C4-free", "no constant/copy gates"), where="argument.md 4; refuted estar/proof.md 1", fz="Estar", c3="dead-route",
  wit=["6=1|3 7=2|5 8=6&7 9=4|8 10=0&9 11=3|5 12=4&10 13=9&11 14=12|13"], ev="net, size 9 = Phi+1.")
C(id="E*+", st="REFUTED", title="Lemma E*+ = mAB (functional reduction, A or B options at a minimal-AND support vertex)",
  stmt="Some v in the support of a minimal AND gate has a good A or B option (functional reduction R+).",
  scope=("C4-free", "reduced"), where="estar/proof.md 5; refuted t2.md 2.1", fz="mAB", c3="dead-route",
  wit=["6=1|0 7=2&3 8=5|7 9=4&8 10=0|9 11=1&10 12=9|11 13=2|12 14=8|4 15=12|3 16=14&15 17=13&6 18=16|17"],
  ev="2tri+bridge, size 13 = Phi+3 (only minimal AND is x2&x3); also constrS7 size 15.")
C(id="L6-FIXED", st="REFUTED", title="L6 with a vertex chosen from the graph",
  stmt="For a graph-determined vertex v (leaf, min degree, hub, ...) some b makes L6 hold on every optimal circuit.",
  scope=("C4-free", "minimum"), where="argument.md 3(b)", ev="Fails for C5 and the bowtie at size Phi (run6.py): every vertex fails on some optimal circuit.")
C(id="EVERY-MINAND", st="REFUTED", title="Every minimal AND gate contains a good vertex",
  stmt="For every minimal AND gate some v in its support satisfies L6 / has a good option.", scope=("C4-free", "minimum / reduced"),
  where="argument.md 3(d); t2.md 2",
  wit=["6=0|5 7=1|4 8=2&3 9=4|5 10=6&7 11=8|9 12=8|10 13=3|12 14=11&13"],
  ev="net: 4 of 489 optimal circuits (argument.md 3(d)); with A/N/B options the net Phi+1 circuit above (t2.md).")
C(id="SMALL-SIDE", st="REFUTED", title="'v on the smaller side' rule", stmt="Some v on the smaller side of a minimal AND gate satisfies L6.",
  scope=("C4-free", "reduced"), where="argument.md 3(c)", ev="K3 at size Phi+1: (x0|x1),(x0&x1),(x2&(x0|x1)),OR,(..)&(x0|x1).")
C(id="NF5", st="REFUTED", title="(NF5) every minimum circuit of a girth >= 5 graph is STAR-ALL",
  stmt="girth(G) >= 5 and size(C) <= Phi(G) imply C is STAR-ALL.", scope=("girth >= 5", "minimum"),
  where="girth5/girth5.md 5; refuted t2.md 4 (Petersen, size 20)", fz="NF5", c3="dead-route",
  wit=["10=6|0 11=0|9 12=6|5 13=11&12 14=9|5 15=13&14 16=3|11 17=4&16 18=3|7 19=12|3 20=19&8 21=14&7 22=1|15 23=22&10 24=23|17 25=18|1 26=2&25 27=20|26 28=27|21 29=24|28"],
  ev="NEW smallest: C5 with pendants at 0,1,2 (n = 8, a pseudoforest) at size 11 = Phi, from t3/locpool.jsonl. The data behind NF5 stopped at 7 vertices. Only the weak form NF-EQ survives.")
C(id="CLEAN-TF", st="REFUTED", title="Every minimum circuit of a triangle-free graph is clean",
  stmt="Triangle-free C4-free G: every minimum circuit has no junk pair.", scope=("triangle-free", "minimum"),
  where="star-case/star.md 0; t2.md 4", ev="Same witnesses as NF5 (the C5{012} size-Phi circuit carries a junk pair; Petersen size 20).", c3="dead-route")
C(id="J5", st="REFUTED", title="J5: size >= Phi + #junk ANDs on triangle-free graphs",
  stmt="Triangle-free C4-free G: size(C) >= Phi + j3 (j3 = AND gates with a junk pair).", scope=("triangle-free", "reduced"),
  where="t2/t2.md 4", fz="J5", c3="dead-route",
  wit=["9=1|7 10=6&9 11=3|9 12=11&2 13=5|6 14=13|3 15=0|10 16=8&14 17=5&9 18=17|4 19=1|5 20=6|7 21=18&20 22=21|12 23=19&15 24=23|16 25=24|22"],
  ev="t2.md: Pet-v size 17. Store's smallest: C5{012} at size Phi with j3 = 1.")
C(id="T2-LO", st="REFUTED", title="T2-LO: first-order eliminations pay some option",
  stmt="Some A/N/B option has |D_X| + |dD_X| (resp. |R_v| + |dR_v|) >= need.", scope=("C4-free", "reduced"), where="t2/t2.md 2",
  wit=["6=0|5 7=1|4 8=6&7 9=3|8 10=4|5 11=9&10 12=2|11 13=3|11 14=12&13"], ev="net, size 9 = Phi+1.", c3="dead-route")
C(id="T2-LT", st="REFUTED", title="T2-LT: first-order + Top merge",
  stmt="Some A/N/B option has |K u Cp u Top| - 1 >= need.", scope=("C4-free", "reduced"), where="t7/t7.md 2",
  wit=["10=1|5 11=10|4 12=0&11 13=3|7 14=1|13 15=2&14 16=8|1 17=16|9 18=6&17 19=8|4 20=3&19 21=4|7 22=9&21 23=7|8 24=5&23 25=18|20 26=25|12 27=26|24 28=15|22 29=28|27"],
  ev="Petersen, size 20 = Phi, a star (STAR-ALL) circuit: dead gates are needed. Also Pet-v size 17.", c3="dead-route")
C(id="T2-LD", st="REFUTED", title="T2-LD: constants, copies and dead gates pay some option",
  stmt="Some A/N/B option has LD(rho) = |K u Cp u Dead| >= need.", scope=("C4-free", "reduced"), where="t8/t8.md 3; t10.md 6", fz="T2LD",
  wit=["6=0|3 7=4|5 8=6&7 9=5|8 10=2|8 11=1|4 12=11&9 13=3|12 14=10&13 15=14|12"],
  ev="net, size 10 = Phi+2; Petersen size 24 (girth 5). The Top merge is needed (T2-LR survives).", c3="dead-route")
C(id="LOCALISE", st="REFUTED", title="Localisations of the good option (t2/t3/t10)",
  stmt="Each of: mA, mB, N-only, every vertex has a good option, every leaf / degree-2 vertex has one, the good option lies at v or u for a bad leaf, V1/V2/V4/V5 (t10), 'within distance 1 of a paid vertex'.",
  scope=("C4-free", "reduced"), where="t2.md 2 table; t3.md 1.3; t10.md 3",
  wit=["6=0|1 7=0|3 8=0|5 9=1|3 10=4&6 11=8&9 12=2|11 13=7&12 14=10&13",
       "8=4&3 9=8|0 10=4|5 11=7|3 12=11|1 13=2&12 14=9|6 15=1&14 16=10&9 17=15|16 18=13|17"],
  ev="First: [01,02,03,04,14,23,35] at size Phi, a vertex without good option. Second: C5{012} at size Phi, a locally-bad leaf (all of A(v),B(v),N(v),N'(v),A(u),B(u) bad). The good option can sit at distance 2-3.")
C(id="NaNb", st="REFUTED", title="Configuration (2): N(a) or N(b) is good",
  stmt="For a minimal x_a & x_b with F_a, F_b >= 2 and A, B bad at both ends, N(a) or N(b) is good.", scope=("C4-free", "reduced"),
  where="t5/t5.md 2",
  wit=["10=4|7 11=3|5 12=6|11 13=11&10 14=12&8 15=0|6 16=5|4 17=13&16 18=17|2 19=7|3 20=16&0 21=14|1 22=2&1 23=15&21 24=6|10 25=24&9 26=14|20 27=18&19 28=27|22 29=28|23 30=29|25 31=30|26"],
  ev="Petersen, size 22 = Phi+2.")
C(id="TOP-LB", st="REFUTED", title="Graph-term lower bound on |Top_X|", stmt="|Top_X \\ (K u Cp)| >= h(G,X) with h >= 2 for some option.",
  scope=("C4-free", "reduced"), where="t7/t7.md 1",
  wit=["8=3|7 9=6&1 10=1|8 11=2&10 12=5|1 13=0|9 14=13&12 15=11&14 16=3|13 17=4&16 18=17|15"], ev="C5{012}, size Phi.")
C(id="DV2-ALL", st="REFUTED", title="Every reduced circuit has a DV2-certified vertex",
  stmt="Some vertex c satisfies the DV2 certificate (pen(c) <= k_Z - delta_c, carrier hypotheses).", scope=("C4-free", "reduced"),
  where="t8/t8.md 3b", wit=["4=0|1 5=0|2 6=1|3 7=5&6 8=4&7", "5=0|2 6=0|3 7=2|4 8=6&7 9=1|8 10=5&9"],
  ev="P4 at Phi+1 (triangle-free); bull at Phi. The P6 example printed in t8.md 3b does not compute any f_G (dropped from the store).")
C(id="PENFREE", st="REFUTED", title="Pen-free DV2", stmt="LD_A(c) >= k_Z + k_L + |N_D(c)|.", scope=("girth >= 5", "reduced"),
  where="t10/t10.md 1", wit=["4=1|3 5=0&4 6=2&4 7=1&6 8=5|7"], ev="P4 at Phi+1, c = 0.")
C(id="SA-CENTRE", st="REFUTED", title="Every star centre of a STAR-ALL circuit has A(c) LD-paid",
  stmt="In STAR-ALL circuits every star centre c has LD_A(c) >= need_A(c).", scope=("C4-free", "STAR-ALL"), where="t8/t8.md 3",
  wit=["6=0|2 7=0|5 8=4&6 9=3|8 10=1|9 11=7&9 12=4|11 13=10&12"], ev="[03,04,14,24,34,35] at Phi+1; also C5{012}, n8 at Phi+3.")
C(id="KOR0", st="REFUTED", title="k_or(c) = 0 implies A(c) LD-paid", stmt="If x_c has no OR reader, LD_A(c) >= need_A(c).",
  scope=("C4-free", "reduced"), where="t8/t8.md 3", wit=["6=3&2 7=6|5 8=7|3 9=0|8 10=4&9 11=3|1 12=11&8 13=12&7 14=10|13"], ev="net, Phi+1, c = 4.")
C(id="NODE-POT", st="REFUTED", title="Per-node OR potential #OR(cone p) >= |E_p| + |S_p| - 1",
  stmt="Node-by-node induction for (OR) on girth >= 5.", scope=("girth >= 5", "any"), where="t10/t10.md 2",
  ev="Construction on the Heawood graph: p = OR(points) & OR(lines) has 12 ORs and E_p = E (needs 20). Not stored (p is not a circuit for f_G).")
C(id="EXCH", st="REFUTED", title="Local exchange towards STAR-ALL", stmt="Single-gate (plus distributive) edits reach a STAR-ALL circuit without size increase.",
  scope=("C4-free", "minimum / Phi+1"), where="t2/t2.md 3; t10/t10.md 3",
  wit=["5=0|2 6=0|3 7=2|4 8=6&7 9=1|8 10=5&9", "4=0|1 5=0|2 6=1|3 7=5&6 8=4&7"], ev="bull at size Phi; P4 at Phi+1 (needs a 3-gate template rewrite).")
C(id="NF-SPLIT", st="REFUTED", title="Separate inequalities of Theorem S beyond STAR-ALL",
  stmt="Z >= m-1; mc >= tau (centres cover); (B) B2 >= |E| - m0c with (C); variants B*.", scope=("C4-free", "minimum / reduced"),
  where="nf/nf.md 2; t10.md 4",
  wit=["6=0|5 7=1|4 8=4|5 9=2|8 10=6&7 11=8&10 12=3|11 13=9&12", "5=1|4 6=0&5 7=1|3 8=5&7 9=4&8 10=3&9 11=2|10 12=7&11 13=6|12"],
  ev="net minimum circuits (Z, mc); C5 at Phi+2 (B), girth 5.")
C(id="TRUNC", st="REFUTED", title="Degree-<=2 truncation is sound for (AND)",
  stmt="Circuits correct modulo monomials of degree >= 3 satisfy #AND >= tau.", scope=("C4-free", "truncated"), where="or-bound/or.md 3",
  wit=["6=3|5 7=0|6 8=1|3 9=2|5 10=4|6 11=8&9 12=4|11 13=7&12 14=10&13"], ev="net: gate 13 is already f_net on degree <= 2 with 2 ANDs < tau = 3.")
C(id="SLICE2", st="REFUTED", title="2-slice arguments suffice on graphs with triangles",
  stmt="Any argument using only inputs of weight <= 2 (S_p, E_p, Fact C, N1-N3, Theorem S charging) proves size >= Phi.", scope=("C4-free with triangles", "formulas"),
  where="form/formula.md 1", ev="net: a 2-separating formula with 8 leaves < Phi+1 = 9 exists. Any proof for triangle graphs must use inputs of weight >= 3. On girth >= 5 the 2-slice is tight on all data.")
C(id="EDGE-SET", st="REFUTED", title="lemD 4 abandoned variants",
  stmt="Edge-set version (|Q_uv| >= deg u + deg v - 1), high-set version (|Q_H| >= e(H)), every min-degree vertex ch-good, some degree->=3 vertex good, every minimal OR gate has a good vertex, sum ch/deg >= n, plain averaging sum ch >= 2|E|-n+1.",
  scope=("C4-free, delta >= 2", "reduced"), where="lemma-d/lemD.md 4; or-bound/or.md 2",
  wit=["5=0&1 6=2&3 7=2|3 8=0|7 9=1|8 10=4&9 11=5|6 12=10|11"], ev="bowtie (high set), triangle, two triangles, triangle+C5.")
C(id="PORT", st="REFUTED", title="All port holders of a minimum circuit lie in one minimum cover",
  stmt="(t9) port holders of a minimum circuit lie in a common minimum cover.", scope=("C5", "minimum"), where="t9/t9.md 4",
  wit=["5=0|2 6=0|3 7=2&3 8=1&5 9=4&6 10=7|9 11=8|10"], ev="C5 minimum circuit, ports at 3, 2, 1, 4.")
C(id="RHO-P", st="REFUTED", title="Partial suns: the all-pendant option pays", stmt="elim(rho_P) >= need(rho_P) and elim(U:=0, P:=1) >= need, from the local reader structure alone.",
  scope=("partial suns", "reduced"), where="t4/t4.md 4",
  wit=["8=3&4 9=3&2 10=0|9 11=7|2 12=10|4 13=12&5 14=1|9 15=6|14 16=11&14 17=15&10 18=16|13 19=17|8 20=19|18"], ev="C6{01}, Phi+2. Moot after THM-PF.")
