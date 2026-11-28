# L-meta-612: status summary

Claim: for every graph G with an edge and no 4-cycle, every monotone fan-in-two AND/OR circuit for
f_G has at least |E| + tau(G) - 1 gates.

## Status: open; not refuted
- Never violated in any test (hundreds of thousands of circuits, exact SAT on all C4-free graphs up to 6 vertices).
- Proving it in full answers Jukna's Problem 24 (ECCC TR05-021, 2005): apply it to the point-line incidence
  graph of PG(2,q), which is C4-free with Theta(n^{3/2}) edges (`core/core.md`).

## Proved
- **Full bound for every C4-free pseudoforest** (`t9/t9.md`, independently reviewed in `review9/`):
  #AND >= tau (new) plus #OR >= |E| - 1 (accepted Lean proof L_meta_599).
- Full bound for forests and for max degree <= 2 (`t2/t2.md`); clean monotone formulas (`t10/t10.md`).
- Upper bound |E| + tau - 1 (`argument.md`).
- Theorem S: the bound holds for every STAR-ALL circuit, for every C4-free G (`girth5/girth5.md`).
  It contains and strengthens the Amano-Maruoka single-level bound.
- Theorem S2: condition N2 can be dropped (`nf/nf.md`).
- Theorem A, Theorem B, Lemmas 3-6 on star gates (`estar/proof.md`, `star-case/star.md`).
- Theorem R and Theorem F: #OR >= |E| - 1 for C4-free graphs with at most one vertex of degree >= 3
  (`or-bound/or.md`, `lemma-d/lemD.md`).
- Lemma S on minimal AND gates (`deg3/deg3.md`).

## Refuted intermediate statements
- Lemma E* as first stated (net, size Phi+1) (`estar/proof.md`).
- The split #OR >= |E| - 1 (n=8 graph, and Petersen) (`petersen/README.md`, `deg3/deg3.md`).
- Lemma M' for the AND half (two triangles plus a bridge) (`deg3/deg3.md`).
- Lemma D and its savings version (`lemma-d-case-a/lemDa.md`, `deg3/deg3.md`, `petersen/README.md`).

## Only surviving route
Lemma T2 (`deg3/deg3.md`): an induction on the total number of eliminated gates, deleting v or N[v]. Holds on all data, unproved.
