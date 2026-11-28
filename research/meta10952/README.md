# L-meta-10952 notes: GAP (not proved, no counterexample)

Statement: the edge function of the 9-vertex graph with edges 04 15 06 26 17 37 57 28 38 48 78
needs at least 15 AND/OR/NOT fan-in-2 gates (k = |E| + tau - 1 = 11 + 5 - 1).
Structure: triangle 1-5-7, triangle 3-7-8 (sharing 7), 5-cycle 8-4-0-6-2 (sharing 8).
C4-free; automorphisms swap 1<->5 and reflect the 5-cycle (4<->2, 0<->6).

## Result: no proof with the accepted checker (L_meta_9409 / L_meta_982 family)

* `gsearch.py`: exhaustive search over GTree certificates with exactly the `checkGTree`
  semantics (f0 cost 1, f1 cost 1, b2 cost 2, emp = |A|-1 with E empty, base needs A empty;
  base rows E0..E20 of L_meta_982, which hold every row of every accepted file with this
  checker). Best certifiable bound: **13** (e.g. f0 0, f0 4, b2 6, f0 2, base bowtie E2 = 8).
* `hyp.py`: give every graph with at most 8 vertices a hypothetical base row with lb = m + tau - 1.
  This is the largest lb any row can have, because m + tau - 1 is an upper bound for every graph.
  Best bound: **14**, via f0 3 then G-3 (8 vertices, 9 edges, would need lb 13).
  Hence, with GTree steps, 15 needs a base row for G itself (9 vertices, lb 15).
* The kernel base search cannot provide such rows. `verifyBase` checks `Nat.ble cap 11`, so a
  base row proves at most 12, in all 16 accepted copies. Even the 8-vertex row in the 14-tree
  (cap 12) is out of range. All 16 files have the same GTree constructors.
* Hand check: the only vertex whose x=0 restriction keeps tau = 5 at a loss of 2 edges is 3.
  But x3=1 leaves x7 OR x8 OR f(15, 04, 06, 26), which is far below 13. So the usual
  b2/f0 recursion stops at 14 = k-1, matching the desk note.

## SAT (bounded; kissat, one process at a time; about 31 min CPU in all)

`syn9.py s out.cnf [mono]` writes the exact-synthesis CNF and `dec9.py` decodes and checks a model
on all 512 inputs.
* monotone (AND/OR), 24 rows (minimal true and maximal false inputs, sound for monotone), s=15:
  SAT in under 1 min, and the decoded circuit is verified on all 512 inputs (validation).
* monotone, s=14: UNKNOWN after 20 min.
* full basis with NOT, 512 rows, s=15: UNKNOWN after 10 min, so even the known circuit was not
  found and the full-basis encoding is not validated at this size. s=14 was not run, since it is
  hopeless within budget.

So the truth is still unknown. The graph is C4-free, so the open L-meta-612 conjecture
(monotone >= m + tau - 1 for C4-free graphs) would predict that the statement is true.

## What would close it

A stronger checker: a base search with cap >= 14 on 9 inputs, or a step that keeps literals
(lb |A| + m + tau - 1 states). Or an UNSAT certificate for s=14 with NOT gates, which looks
infeasible with the current encoding.
