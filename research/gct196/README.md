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

---

# Attempt 2 (2026-11-25, second agent)

Status: **still not proved.** No `L_gct_196.lean` was written to the clone. What follows is
mathematics (q-generic reformulations), new numerical evidence, and the remaining gap.

## A2.1 Reformulations that hold for every q (paper, short proofs)

**(i) Gradient criterion.** Write G_k(x) for the gradient of M_k at x, i.e. the 4 x q matrix with
entry (r, j) equal to M_{k-1}(x with row r and column j deleted). By Euler (<G_k(x), x> = k M_k(x))
and polarization: a subspace L is level iff G_k(x) ⊥ L (plain dot product) for all x in L and
k = 1..4. Here G_1 = J and G_2(x) = Q x = x - R(x)1^T - 1 C(x)^T (when S = 0). So, with
Γ(L) = span(J, G_2(L), G_3(L), G_4(L)) ⊆ L^⊥,

    dim L + dim Γ(L) <= pq,   and   dim Γ(L) >= 1 + dim L    (Q invertible, J ∉ Q L).

That is the isotropy bound 13. The bound 9 at 4 x 7 is **equivalent** to: no level L of dim 10
has dim Γ(L) <= 18, i.e. G_3, G_4 always add >= n - 2 dimensions beyond J + Q L.
Numerically, every maximal example below has dim Γ = 2n + 3 or 2n + 4 (19 or 20 for n = 8).
A "Cauchy–Davenport" inequality dim Γ(L) >= 2n - 1 would give 3n <= pq + ... , i.e. n <= 9.
(The p2/p3 Fermat–Kneser bound dim <= m/3 of the fleet's FermatFromKneser helper has exactly
this shape. On doubly centred matrices M_2 = p2/2 and M_3 = 2 p3/3 hold exactly. Off them,
M_3 is not a Hadamard cube: checked numerically, no rescaling of row/column effects works.)

**(ii) Formula for the cubic gradient.** If S(x) = 0 and M_2(x) = 0, then
G_3(x)_{rj} = 2x_rj^2 + R_r^2 + C_j^2 - 2x_rj(R_r + C_j) + R_r C_j + <R, x_{.j}> + <C, x_{r.}>
- sum_l x_rl^2 - sum_a x_aj^2. For doubly centred d this is 2 d∘d minus a row effect minus a
column effect. Polarized, for d, d' in D = L ∩ P (P = the doubly centred matrices) and s in L:
2<d∘d', s> = <C(d∘d'), C(s)> + <R(d∘d'), R(s)>. The Hessian of M_3 at d in D is
x ↦ 4 d∘x - 2 d∘(R_x 1^T + 1 C_x^T) + (row and column effects).

**(iii) Line-sum split** (the same as hint 1). dim L = dim λ(L) + dim D, where λ = (row sums,
column sums) maps into a 9-dimensional space and D = L ∩ P. Also D ⊥ L. **D = 0 gives dim <= 9 at
once** (only M_1 is used). Examples: hook λ = 8, D = 0; F_7 λ = 6, D = 2; N8 (below) λ = 5,
D = 3; G-type (7) λ = 4, D = 3. So D can be 3 in a maximal 8-dim space, and no simple inequality
of the form λ + c·D <= const with c >= 2 holds (N8 gives 5 + 6 = 11).

**(iv) Row-centred part.** On L_0 (zero row sums) the level conditions are Σμ_ab = 0,
Σμ_abc = 0 and 6μ_0123 = Ω, where μ_T = sum over j of prod_{r in T} t_rj and
Ω = μ01 μ23 + μ02 μ13 + μ03 μ12 (the hafnian of the row Gram matrix). So a subspace K ⊆ L_0
with Ω|K ≡ 0 is column-product level, and **L-gct-175 gives dim K <= q - 1**. The four-row
excess (F_q has dim L_0 = q + 1) comes entirely from Ω. Rado applied to L_0 with dim L_0 = q + e
gives affine e-dimensional families on which J + y has a zero in every column and Ω ≡ -6q.
That does not yield a contradiction.

**(v) Column and row deletion keep levelness** (all q): {t in L : columns U vanish} is level for
4 x (q - |U|), and {t : row r = 0} is level for 3 x q, because P(J+t) = (q-3) P_3(J'+t').
Hence for dim L = 10 at q = 7: every row image has rank >= 2, every pair of rows has rank >= 4,
every 2, 3, 4, 5 columns have rank >= 3, 4, 5, 7 (using f(5) = 7, f(4) = 6, f(3) = 5, f(2) = 3).
Single columns would need f(6) <= 8 (L-gct-195, open). A purely linear-algebra contradiction
(Rado plus Frobenius–König blocks plus Q-isotropy) is not available. Every FK block has at least
12 cells except a full row, and the full-row case is exactly lO.

## A2.2 Numerical evidence (scripts in `gct196/num/`)

* `lev.py`, `lm2.py`: fast evaluation of M_1..M_4 (Boolean-algebra product over columns) and
  an analytic Jacobian. Levenberg–Marquardt over a basis, with the conditions imposed as
  polynomial identities at about 1.3·C(n+3,4) random points of L. From random starts it finds
  level spaces of dim 3 at once but stalls for dim >= 4 even at 4 x 4. This confirms the earlier
  finding: random-start numerics say nothing about dim 9 or 10.
* `ext.py`: first-order extension space T1(L) = {s : D_s M_k(x) = 0 for all x in L, all k}.
  Every level L' ⊇ L lies in T1(L). Results at 4 x 7:
  - F_7 (rows 1-3 = x(1,w,w^2)(e1-e2) + y(1,w^2,w)(e3-e4), row 0 any sum-zero vector) and the hook
    (row 0 sum-zero, plus column 0 rows 1-3 sum-zero): both have dim 8 and dim T1 = 9. The extra
    direction is the constant-row matrix (3,-1,-1,-1)⊗1, which is not level (L-gct-202). So
    **both 8-dimensional families are inclusion-maximal.**
  - G-type at 4 x 7 (u e_0^T with Σu = 0, plus C^4 ⊗ (0,1,z,...,z^5), z = e^{2πi/6}): dim 7,
    level, T1 = 12. Searching inside T1 (12-dim ambient) found a **new 8-dim level space N8**,
    numerically exact (residual 5e-14) and inclusion-maximal (T1 = 8). It is spanned by
    {u e_0^T} (3 dims) and a 5-dim subspace of C^4⊗f_1 + C^4⊗f_2 + (one column-0/constant
    direction), with f_k = (0, z^{kj}). Its row ranks are (2,2,3,2), the row-sum image is 3-dim, the
column-sum image is 2-dim, λ = 5, D = 3, dim Γ = 20. It is a different family from the hook and
F_7, which both have a row of rank 6. The random walk `walk.py`, which takes 5-, 6- and 7-dim
subspaces of known spaces and searches inside their T1, found it again about ten times, up to
row permutation. It found nothing larger.
    The search for a 9-dim level space inside T1(G) did not finish its 12 LM seeds under the machine load. None was found; see `extG.log`.
  - C^4 ⊗ (7th roots) is level (dim 4, T1 = 15). The search inside it was not run.
* Shift-invariant ansatz (`inv_search.py`, `inv_enum.py`): L = ⊕ of subspaces of the eigenspaces of
  the cyclic column shift. These are Z_7 on all columns and Z_6 on columns 1-6. Only partly run: the
  machine was shared and overloaded (load about 8). The Z_7 run covered 20 of 596 canonical
  profiles for n = 9, with nothing found. Treat it as incomplete.
* 4 x 6 check (`g46.py`): G(4) (dim 7) and F_6 (dim 7) both have T1 = 8. The extra direction is
  again the non-level constant-row matrix, so both are inclusion-maximal. That fits L-gct-187
  being open.
* Doubly centred: dim 3 is found at once from random starts (generic). Dim 4 was not found
  (5 seeds). M_1..M_3 alone (no quartic) admit generic 8-dim solutions; 8 is also the generic
  expected dimension.

So far: **no 9- or 10-dimensional level space found**. Three different inclusion-maximal
8-dimensional families exist (hook, F_7, N8). This matches the fleet's record (best 8).

## A2.3 Exact low-order identities in centred coordinates (new, all p and q; checked numerically)

Write x with S(x) = 0 as x = d + a 1^T + 1 b^T, where Σa = Σb = 0 and d is doubly centred. Set
y = d + α a 1^T + β 1 b^T with α = (2-q)/2 and β = (2-p)/2. Then, with p_k the power sums of entries,

    M_2(x) = 1/2 [ p2(y) - (q^3/4) p2(a) - (p^3/4) p2(b) ]
    M_3(x) = 2/3 [ p3(y) + (q^3 (q-2)/8) p3(a) + (p^3 (p-2)/8) p3(b) ].

These hold as polynomial identities: random complex x, residual 1e-15. For level x,
G_3(x) = Θ(y∘y) + γ_1 (a∘a) 1^T + γ_2 1 (b∘b)^T + c J, where Θ(w) = 2w - R(w)1^T - 1C(w)^T,
γ_1 = (q-2) q^2/4 and γ_2 = (p-2) p^2/4. So up to order 3, a level space is a p2/p3-"Fermat-isotropic"
subspace of C^{pq} in the y-coordinates, corrected by terms that depend only on the 9 numbers (a, b).
On D = L ∩ P it is exactly Fermat-isotropic (D ⊥ D, D ⊥ D∘D), and also D ⊥ y(L) and
D ⊥ y(L)∘y(L). The Fermat–Kneser bound m/3 would give 28/3, i.e. 9, at 4 x 7, but only if the
corrections could be absorbed without new coordinates. Absorbing them needs at least two scaled
copies of a and of b (m = 50), so this route gives nothing as it stands. A "Kneser with a low-rank
correction" inequality of the form 3 dim L <= pq + 1 would suffice, but I have no proof of one.
M_4 is not of this form: on P, 24 M_4 = 36 p4 - 18 (R4 + C4) + 6 Gram + 3 p2^2 (L-gct-134).

**Conditional-expectation form of (M_2, M_3).** Let E_R and E_C be the τ-preserving projections of
the Hadamard algebra A = C^{p×q} onto row-constant and column-constant functions. Let
c_R = (q/(q-2))^2 and c_C = (p/(p-2))^2. Then for w, w', w'' in W = y(L) (y = φx as above):

    τ(w w')     = c_R τ(E_R w · E_R w')          + c_C τ(E_C w · E_C w'),
    τ(w w' w'') = c_R τ(E_R w · E_R w' · E_R w'') + c_C τ(E_C w · E_C w' · E_C w'').

The same constants appear in both lines. So ι(w) = (w, E_R w, E_C w) embeds W in the product
algebra A × C^p × C^q with the trace T = τ - c_R τ_R - c_C τ_C, and ι(W) is exactly
p2/p3-isotropic there ("Fermat"). Kneser for codes (the fleet's FermatFromKneser route) then gives
only 3n <= pq + p + q - 2 + (stabilizer). At 4 x 7 that is n <= 12, which is weaker than needed.
With no correction terms it would give 3n <= pq, i.e. n <= 9.

**Conjecture F (new, consistent with all data I know):** for p >= 3, every level space has
3 dim L <= pq. At 3 x q it gives q, the best known (L-gct-156 has q+1). At 4 x 4 it gives 5 and at
4 x 5 it gives 6, both equal to the best known (hooks). At 4 x 6 it gives 8 and at 4 x 7 it gives 9,
which is exactly L-gct-195 and L-gct-196. It fails at p = 2 (no cubic condition there). Random-start
LM found 3 x q level spaces of dim q but not q+1 for q = 3, 4, 5. That evidence is weak.

## A2.4 Remaining gap (precise)

No proof of dim L <= 9. All q-generic tools above give only 12 or 13 on their own:
isotropy 13, cubic Kneser 12, and the line-sum split 9 + dim(L ∩ P). The deletion and Rado tools
reduce to the open 4 x 6 case or to a 215-style case tree. The two cheapest closed sub-cases are
these. (a) L ∩ P = 0 gives dim <= 9 (rank–nullity). (b) Some row image of rank <= 1 gives
dim <= 1 + (3 x 7 bound 8) = 9; this needs L-gct-156 ported. Neither is written in Lean.
Concrete open targets that would finish the problem:
1. "Kneser with correction": dim(C1 + W + W∘W) >= 2n + 2 + (p+q-2) - (something <= 1) for the
   graph embedding ι. Equivalently, the correction coordinates cost nothing.
2. Or a structure theorem for D = L ∩ P that gives dim λ(L) <= 9 - dim D.
3. Or, as for 4 x 5, a full case analysis on the u_i and the pair ranks, generalised to Fin q.
