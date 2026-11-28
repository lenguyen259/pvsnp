# Playbook: "Table 2" rows (an edge function needs at least N AND/OR/NOT gates)

Statement shape: `∀ t, HasCircuitSize n f t → N ≤ t`, where f is the edge function of a small
graph and N = k = |E| + tau - 1 (the star-cover upper bound). The desk's own recursion usually
reaches k - 1.

## Recipe (worked for L-meta-10524 in about 8 minutes)

1. Copy an accepted file that uses `conj_of_gtree`. `L_meta_9409.lean` on origin/main is the
   template; 16 accepted files share the checker. Rename the namespace, and keep a line-2 comment
   saying where it was copied from.
2. GTree steps are `emp`, `base`, `f0 v`, `f1 v` and `b2 v`:
   - `f0 v`: fix x_v = 0, cost 1.
   - `b2 v`: two-branch at v, cost 2.
   - `base i π`: base row i under vertex map π.

   Base rows E0..E20 come from `L_meta_982` (at most 7 vertices, bound at most 12). `verifyBase`
   requires `Nat.ble cap 11`, so no base row certifies more than 12.
3. Search exhaustively for a tree with exactly the checker's semantics:
   `research/meta10952/gsearch.py`. With `hyp.py`, ask what is reachable if every graph on at most
   8 vertices had its best possible row.
4. The final theorem is `conj_of_gtree (req := N) rootTable rootTable_ok (f) [edges] (tree)
   (by decide +kernel) (by decide)`.
5. Build, run `#print axioms`, then check the exact statement with an `example`.

## Limits (when to release)

- If `gsearch.py` reaches at most N-1 and `hyp.py` shows that N needs a base row on 9 vertices or
  with a bound above 12, the accepted checker cannot do it. Release with `missing_lemma`. This
  happened for L-meta-10952.

## Lessons

- 2026-11-25: For theta(2,3,3) plus a pendant path, the missing base row was `lb15` (theta >= 11),
  reached via `b2` at the pendant vertex and then `f0` at its neighbour.
