# L-gct-196 (4 x 7 level spaces, dim L <= 9): not proved

Status: **not proved.** No Lean proof of the full statement exists. Nothing was
submitted under `lean/PEqualNP/Outside/L_gct_196.lean`.

Statement (from the gct cache, `196.json`): L is a subspace of 4 x 7 complex
matrices. On L the entry sum vanishes, and so do the sums of all 2x2, 3x3 and 4x4
subpermanents. The claim is `finrank L <= 9 = p + q - 2`. The project lists this
case as open. The best spaces known have dimension 8.

Naming convention, for whoever proves it: the accepted files name the final
theorem `PEqualNP.Outside.L_gct_214` and `PEqualNP.Outside.L_gct_215`. They do not
use `...L_gct_215.L_gct_215`. Both declare it after
`end PEqualNP.Outside.L_gct_21x`, with `open PEqualNP.Outside.L_gct_21x in`. So the
196 theorem should be `theorem PEqualNP.Outside.L_gct_196 : <statement>`. The file
215 uses `set_option maxHeartbeats ... in` and `set_option maxRecDepth ... in`
before single lemmas.

## 1. How the accepted proofs work, and whether they carry over to q = 7

### L-gct-214 (4 x 4, bound 6, 1716 lines)

This proof works for square matrices only. Write C = L + CJ. It shows that
`perm(X + y) = perm(X)` for X in C and y in L. It then uses a Laplace expansion
along a row to get to the 3x3 minors. Lemmas F2 and F3 are invariance bounds:
dim <= 1 for 2x2 and dim <= 3 for 3x3. `step1`, `main_core` and `final` handle
the 4x4 step.

This induction gives the bounds n(n-1)/2, that is 1, 3, 6. These equal p + q - 2
only at n = 4. A rectangular 4 x 7 matrix expands into 3 x 6 minors, which are no
longer square. **The 214 argument does not carry over.**

### L-gct-215 (4 x 5, bound 7, 7559 lines)

The final theorem is
`Ac.aAm Ac.aEn Ac.aGj Ac.aCb Ac.vV Ac.aFy Ac.aGe`. It assumes a level subspace S
with dim S = 8 and splits into cases on

    u_i = dim (S ∩ {t : every row other than i is 0}),   with 0 <= u_i <= q-1 = 4.

| case | 215 name | proof | depends on q = 5? |
|---|---|---|---|
| some u_i = 4 = q-1 | `vJ` (`Av.aG7`, about 190 lines) | The row-i image is the whole sum-zero hyperplane, of dimension q-1. Each 3 x (q-1) minor of the other rows, with one column deleted, is then level. That makes each column sum zero. In the ω-coordinates (a, b) the Q2 condition reads (2a_j - A)(2b_j - B) = AB. Lemma `xO` gives dim of the rest <= 3, so the total is 4 + 3 = 7. | Partly. The arguments for `xO` and `vM` use dim > q-2. At q = 7 they only give dim of the rest <= 5, so the total is 6 + 5 = 11. That misses the target of 6 + 3. See section 3 for a sketch of the missing bound. |
| some u_i in {2, 3} | `MidCase` (`Ac.Af`, `M3`, `Ac.A4`, ..., about 2500 lines) | Case work on the row-i support U = (part of S supported on row i) mapped to row i. It uses explicit Finsets of `Fin 5` with fixed sizes, for example `A.card = 3` and `U = bJ A`. It also uses 3 x 5 slices `bI := Fin 3 × Fin 5` and explicit witness matrices. | **Yes, heavily.** At q = 7 the range is u_i in {2, ..., 5}, which has twice as many sub-cases. Every one needs new arguments. |
| some u_i = 1 | `mI` (`Ac.Ah`, about 530 lines) | Reduces to a 7-dimensional level space with two equal columns. | Yes. It uses explicit dimension counts. |
| two equal columns, dim 7 | `eI` (`Ac.Ad`, `Bd`, `Bf`, about 950 lines) | Shows `∑ u_i <= 3`, then reaches a contradiction. | Yes. |
| all u_i = 0, some pair projection has dim 7 | `HighPair` (`Ac.Ar`, ...) | Uses the extremal pair bound `lB`. | Yes. |
| all u_i = 0, every pair projection has dim <= 6 | `vK` | Dimension counting over the pairs, plus sub-cases. | Yes. |

Only the first section `Aa` of 215 is generic in q. It contains `cK`, `lO`, `vG`,
`aBr`, `cD` and `lB`, and these port to q = 7 by changing the constants.

At q = 7 the case tree must start from dim S = 10, not 8. u_i ranges over
0..6, and the pair bound becomes 2q - 3 = 11. So the top-level split has strictly
more cases than at q = 5, and almost every leaf of the q = 5 tree uses
5-specific computations. A port would mean re-deriving the mathematics of about
7000 lines of Lean, which has no paper version, for a larger q. That does not fit
a 4-hour budget.

## 2. What is proved in Lean for q = 7

The file `Partial196_q7.lean` sits next to this README. It ports section `Aa` of
215 to `Fin 4 × Fin 7`. It imports only Mathlib and `PEqualNP.Defs`. It builds
cleanly: it was copied into the clone as `PEqualNP/Outside/L_gct_196_partial.lean`,
built with `lake build`, and then removed.

- `cK`: aO M = ∑ over injections Fin 4 ↪ Fin 7 of ∏_r M(r, e r). It equals the
  4-fold column sum with the distinctness `if` that appears in the statement.
- `lO`: if aO(1+t) ≠ 0 on L, then for each row i there is a functional f with
  f 1 = 1 that kills row i of L. So no row image contains the all-ones vector.
- `cD`: a 2x2 cancelling pair of rows forces aO = 0.
- `lB`: for i ≠ j, dim (rows i and j of L) <= 2(q-1) - 1 = 11.
- `oD`: aO(1+t) = 840 + 120·cW + 20·pQ + 4·pR + yW.
  This identity links the statement to the "level" hypothesis aO(1+t) = 840.
  The coefficients are (7-k)!/3!. It is proved by brute-force `simp`/`ring`, like 215's `oD`, and builds in about 30 s.

The whole file builds in about 30 s. `#print axioms` on `lB` and on `oD`, run from a temporary file that was then deleted, shows only `propext`, `Classical.choice` and `Quot.sound`. The file has no `sorry`.

## 3. Mathematics on paper (partial, q-generic)

**(a) Isotropy bound.** Write Qy = y - (row sums) - (column sums) + (total), placed
entry by entry. Then 2 M_2(y) = <y, Qy>, and ∇²P(J) = (q-2)(q-3) Q. Polarising
P(J + s y + t) = P(J + s y) gives <t, Q y> = 0 for t in L and y in C = L + CJ.

The eigenvalues of Q are 1 (interaction part), 1-q (row effects), 1-p (column
effects) and (p-1)(q-1) (constants). None is zero, so Q is invertible. Hence
dim L + dim C <= pq, which gives **dim L <= floor((pq-1)/2) = 13** at 4 x 7.

This is the order-2 bound only. It is weaker than needed, though slightly better
than the "q+7 = 14" quoted in L-gct-183.

**(b) Moment form.** Let a_j be the columns of J + t, and set
m_B = ∑_j ∏_{r∈B} a_j(r). Then

    P(J+t) = ∑ over set partitions π of {0,1,2,3} of ∏_{B∈π} (-1)^{|B|-1} (|B|-1)! m_B,

and m_B(J+t) = ∑_{T⊆B} μ_T(t), where μ_T(t) = ∑_j ∏_{r∈T} t(r,j). So the level
condition depends only on the 15 column moments μ_T. This is the natural setting
for a q-generic argument. The 3-row bound q+1 (L-gct-156/157) comes from it via
row centring. At 4 rows, row-centred level spaces can exceed q-1: dimension
q+1 = 5 at 4 x 4 (L-gct-197/217). So the simple reduction dim L <= 3 + (q-1)
fails. L-gct-178 only gives dim <= q - 1 + r.

**(c) The case u_i = q-1, for general q (sketch).** Then dim L = (q-1) + dim R.
Here R is the projection of L to the other three rows. Every column of R sums to
zero, and R is written in ω-coordinates a, b ∈ C^q. The conditions are, for each j:

- (2a_j - A)(2b_j - B) = AB, where A = Σa and B = Σb;
- e3(a without coordinate j) + e3(b without coordinate j) = 0.

Three sub-cases:

- If AB is not identically 0 on R, then (A, B) is injective, so dim R <= 2. This
  is 215's argument and does not depend on q.
- If B ≡ 0 and b ≡ 0: summing over j gives (q-3)e3 = 0, and then
  a_j(a_j² - e1 a_j + e2) ≡ 0 for each j. The nonzero forms a_j take at most two
  values u, v with u + v = e1. Counting multiplicities forces dim R <= 2.
- If B ≡ 0 and S = {j : b_j ≠ 0} is nonempty: then a_j = A/2 on S, and similar
  identities hold. This sub-case was not finished.

So this case very likely gives dim L <= q - 1 + 3, which is 9 at q = 7. It is
still only one of the six top-level cases.

## 4. Numerical experiments (inconclusive)

Two methods were tried on the Grassmannian: LBFGS and Levenberg–Marquardt. The
residual was P(J + Bz) - P(J) at more random points z than there are monomials.
Both stalled in local minima at residual 1e-3 to 1e-2. This happened even for
4 x 4 with dim 4 and dim 5, where solutions are known to exist. Those solutions use
roots of unity and are not generic. So random-start numerics give **no evidence**
about whether dim 9 or 10 is reachable at 4 x 7, and none is claimed. A useful
search would need structured ansätze, such as root-of-unity circulant blocks.

## 5. The precise gap

The missing piece is a complete proof that a level 4 x 7 space cannot have
dimension 10. Concretely, following the 215 case tree with dim S = 10 and
u_i <= 6, these cases are missing:

1. u_i = 6: section 3(c), last sub-case.
2. u_i in {2, ..., 5}: no argument at all.
3. u_i = 1, including the "two equal columns" reduction at q = 7.
4. all u_i = 0: an analysis of the pair projections p(i,j) <= 11, in the cases
   p = 11 and p <= 10.

The alternative is a q-generic proof of dim L <= p + q - 2 at p = 4. That is the
open conjecture L-gct-086 restricted to four rows, and it would make the q = 4, 5
case analyses unnecessary.
