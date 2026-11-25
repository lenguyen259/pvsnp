# L-meta-10524 notes

Statement: the edge function of the graph on 9 vertices with edges
04 15 26 36 07 17 27 28 48 58 has no AND/OR/NOT fan-in-2 circuit with fewer than 14 gates
(k = |E| + tau - 1 = 10 + 5 - 1 = 14).

## Proof idea (gate elimination, one tree)

Structure of the graph: a theta graph between 7 and 8 with paths 7-2-8, 7-0-4-8, 7-1-5-8
(7 vertices, 8 edges), plus the pendant path 2-6-3.

* Two-branch step at the pendant vertex 3 (costs 2 gates in both branches):
  - x3 = 0: the graph minus edge 36;
  - x3 = 1: literal x6 plus the edges avoiding 3 and 6.
* In both branches fix x6 = 0 (costs 1 gate): what remains is exactly theta(2,3,3).
* theta(2,3,3) needs 11 gates: this is the base row E15 = [(0,1),(0,2),(0,3),(1,4),(2,5),(3,6),(4,5),(4,6)]
  proved (lemma lb15) in the accepted L_meta_9409.lean (from the checked L-meta-982).
* Total 2 + 1 + 11 = 14.

L_meta_9409 has exactly the same shape (pendant vertex attached to a theta(2,3,3), there at a
different position), so the Lean file is L_meta_9409.lean with the namespace renamed and the
final theorem replaced: GTree `.b2 3 (.f0 6 (.base 0 π)) (.f0 6 (.base 0 π))` with
π = [2,3,1,0,5,6,0,0,4] (7->0, 8->4, 2->1, 0->2, 4->5, 1->3, 5->6; 3,6 isolated).

No SAT counterexample search was needed: the bound is proved.

Side check (syn.py, SAT exact synthesis): theta(2,3,3) has an 11-gate circuit (upper bound matches).
