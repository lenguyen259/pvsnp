# NF / weighted Theorem S: what extends, what breaks, the exact gap

Status: **NOT closed** (neither girth >= 5 nor all C4-free). Two partial theorems are PROVED, and
every Theorem-S-type local decomposition is shown by data to break. The gap is isolated as the
split statement (OR) + (AND) below.

Notation as in girth5.md: S_p = {u : p(e_u)=1}; for an AND gate h = h1&h2, S1, S2, R_h.
For all counts, dead gates (not reaching the output) and copy gates op(y,y) are deleted first.
Removing them never increases size and changes no surviving node's function.
* m = #AND. m0 = #AND gates with S = ∅. An AND gate is *nonempty* if S_h ≠ ∅, which is the same as violating N1.
* creator = the Fact-C gate of some edge (an AND gate accepting e purely, with neither input accepting e purely).
  mc = #creators. m0c = #creators with S = ∅. Here "first creator" is taken in circuit order.
* B2 = OR gates with both inputs S ≠ ∅ and |S| >= 2. Z = OR gates with an input S = ∅ (z0 = both, z1 = one).
* lnkA = number of (AND gate, input with S = ∅) incidences.
* Always (PROVED, trivial): size >= m + |B2| + |Z|, because the classes are disjoint.

## 1. Proved results

**Lemma L (empty links). PROVED, any monotone circuit for f_G, E ≠ ∅.** |Z| >= m0 - 1 - lnkA.
*Proof.* The empty nodes (S = ∅) are the AND gates with S = ∅ and the z0 OR gates. Inputs have
|S| = 1. The output is empty because f(e_u) = 0. Every non-output empty node has a reader, so
#(links from empty nodes) >= m0 + z0 - 1. Readers are OR gates (2 z0 + z1 links) or AND gates
(lnkA links). Hence 2z0 + z1 + lnkA >= m0 + z0 - 1. ∎

**Theorem S2 (N2 is not needed). PROVED, C4-free G, any circuit satisfying N1 and N3.**
size >= |E| + tau - 1.
*Proof.* By N1, every AND gate has S = ∅, so m0 = m.
* An AND gate with an empty input (a *killer*, k of them) has R_h = ∅. So lnkA <= 2k.
* Every other AND gate has disjoint nonempty S1, S2, and R_h = S1 x S2 ⊆ E by N3. So it is a star
  ({c} x L, L ⊆ N(c)), as in Lemma 1. Let m* be the number of stars, so m = m* + k.
* (a) By Fact C, every edge is created at a star as {centre, leaf}, so m* >= tau.
* (b) The proof of Theorem S (b) goes through verbatim, with H_c = the stars of centre c:
  - S-cones contain only inputs and OR gates, because AND gates are empty;
  - S_{p_h} = L_h ⊆ N(c), because S1 ∩ S2 = ∅;
  - so the C4 disjointness argument applies, and |B2| >= |E| - m*.
* (c) By Lemma L, |Z| >= m - 1 - lnkA >= m - 1 - 2k.
* Sum: size >= m + |E| - m* + m - 1 - 2k = |E| - 1 + m* >= |E| + tau - 1. ∎

**Lemma A (AND bound for clean circuits). PROVED, C4-free.** If C is clean (N3 at every AND,
with N1 and N2 arbitrary), then #AND >= mc >= tau.
*Proof.* Let e be an edge with Fact-C gate h. Then e ∈ R_h ⊆ E (Lemma 0), and R_h is complete
bipartite with both sides nonempty. C4-freeness forces one side to be a single vertex c_h ∈ e. So
the c_h form a vertex cover. ∎

**Corollary (PROVED).** For clean circuits, the claim follows from (OR) below; Lemma A gives the AND half.
For circuits satisfying N1 and N3, it is Theorem S2. So the only obstructions are:
* N1 violations, i.e. singletons carried through an AND (for the OR half), and
* junk pairs (for both halves).

## 2. What breaks (DATA; smallest instances)

Corpus: all minimum circuits in `../s_case/circs` and `../tf/circs` (C4-free graphs on <= 7
vertices, triangles included), plus new exhaustive or capped enumerations in `nf/circs`:
* size Phi+1 for all 17 graphs on <= 5 vertices (cap 4000);
* size Phi+1 for 26 graphs on 6 vertices, including net, bull and C6 (cap 3000);
* size Phi+2 for all 17 graphs on <= 5 vertices (cap 4000).

Total 125,935 circuits (16,001 of size Phi, 61,795 of size Phi+1, 48,139 of size Phi+2). 46,966 of them violate N1, N2 or N3; the 6-vertex Phi+1 sweep stopped after 21 of 26 graphs. Script: `t3.py`-`t8.py`.

| inequality | status |
|---|---|
| Theorem S (c): Z >= m-1 | fails on **minimum** net circuits (119), e.g. `6=0|5 7=1|4 8=4|5 9=2|8 10=6&7 11=8&10 12=3|11 13=9&12` |
| mc >= tau (centres cover) | fails on the same net minimum circuits (junk rectangle 10 = (0|5)&(1|4) creates the path 0-4-5-1, tau 2, killed junk 01) |
| (B) B2 >= E - m0c **with** (C) Z + m - m0c >= tau - 1 | both tight on every minimum circuit and every Phi+1 circuit. (B) **fails at size Phi+2 on C5 (girth 5)**: `5=1|4 6=0&5 7=1|3 8=5&7 9=4&8 10=3&9 11=2|10 12=7&11 13=6|12` (B2 = 2 < 3). 8 is a nonempty creator (S = {1}), 9 carries junk 14 and 10 kills it. The total still holds (size 10 = Phi+2). |
| B2 >= E - mc with Z + m - mc >= tau - 1 | B holds on all data; C fails on 242 minimum net circuits (N1-type, e.g. `6=1|3 7=2|5 8=3|5 9=0|8 10=4&9 11=6&8 12=7&11 13=10|12`) |
| B2 >= E - m0, and the "any creator" variant B* | B* fails on the same C5 Phi+2 circuits |

So **no split of Theorem S's three counts into separately valid inequalities survives**. Whether a
nonempty creator (N1 violation) saves an OR merge depends on the circuit:
* it saves none in the net minimum circuits;
* it saves one in the C5 Phi+2 circuit, where the merge 1|3 serves both the junk singleton and a real leaf set.

A weighted Theorem S must therefore charge OR gates globally, not class by class.

**What survives everywhere (DATA, 0 violations, tight on every minimum circuit):**
* (OR) B2 + Z >= |E| - 1, hence #OR >= |E| - 1.
* (AND) #AND >= tau; even #AND - #(ANDs with both inputs empty) >= tau.

SAT check (`split.py`, CaDiCaL): there is no circuit of size Phi with #OR <= |E| - 2, for all 26
C4-free graphs on 6 vertices, C6, net and bull included, except 3 graphs with 7 edges, which timed out at 200 s. Results are in `slog_or.txt`. The Phi+1 and Phi+2 SAT sweeps were not run, so near-minimum circuits are covered only by the enumeration above.

## 3. Exact remaining gap

(OR) and (AND) together give the claim (size = #AND + #OR). What is open:
* (OR) for every circuit, already open for clean circuits with N1 violations. The obstruction is
  that the C4 disjointness of S-cones (Theorem S (b)) fails once S_{p_h} contains junk singletons:
  a merge gate below p_h can be a leaf-merge for two centres only if its S meets K_h = S_h.
  So each sharing is caused by a nonempty creator. The C5 example shows such a creator can also
  *save* a merge.
* (AND) for circuits with junk pairs. Here a rectangle gate can cover tau(E_h) >= 2. In every
  example a killer AND above it pays the difference, but no injective charging is proved.
* Route 2 (rewriting to STAR-ALL) was not achieved. Note that for girth >= 5 the C5 example
  shows non-STAR-ALL circuits exist at size Phi+2. Data: every non-STAR-ALL circuit of a girth >= 5
  graph has size > Phi (girth5.md §4).

Files (all in this folder): `base.py`, `t1.py`-`t8.py` (tests), `dump.py`/`drive.sh` (enumeration),
`bsat.py` (SAT search for violations of B; superseded), `split.py`/`sdrive.sh` (split SAT check),
`circs/` (new dumps).
