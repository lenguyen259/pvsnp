import Mathlib
import PEqualNP.Defs

namespace PEqualNP.Outside.L_gct_196_partial3


namespace Rado

open Submodule Module

variable {K : Type*} [Field K] {W : Type*} [AddCommGroup W] [Module K W] {ι : Type*}

/-- The union of the sets `A j` over `j ∈ s`. -/
def un (A : ι → Finset W) (s : Finset ι) : Set W := ⋃ j ∈ s, (A j : Set W)

lemma un_finite (A : ι → Finset W) (s : Finset ι) : (un A s).Finite :=
  s.finite_toSet.biUnion fun j _ => (A j).finite_toSet

lemma un_insert [DecidableEq ι] (A : ι → Finset W) (i : ι) (s : Finset ι) :
    un A (insert i s) = (A i : Set W) ∪ un A s := by
  simp only [un, Finset.set_biUnion_insert]

lemma un_union [DecidableEq ι] (A : ι → Finset W) (s t : Finset ι) :
    un A (s ∪ t) = un A s ∪ un A t := by
  simp only [un, Finset.set_biUnion_union]

lemma un_mono (A : ι → Finset W) {s t : Finset ι} (h : s ⊆ t) : un A s ⊆ un A t :=
  Set.biUnion_subset_biUnion_left (fun _ hx => h hx)

lemma un_update_of_not_mem [DecidableEq ι] (A : ι → Finset W) (i : ι) (B : Finset W)
    (s : Finset ι) (h : i ∉ s) : un (Function.update A i B) s = un A s := by
  unfold un
  refine Set.iUnion₂_congr fun j hj => ?_
  rw [Function.update_of_ne (by rintro rfl; exact h hj)]

lemma un_update_of_mem [DecidableEq ι] (A : ι → Finset W) (i : ι) (B : Finset W)
    (s : Finset ι) (h : i ∈ s) :
    un (Function.update A i B) s = (B : Set W) ∪ un A (s.erase i) := by
  conv_lhs => rw [← Finset.insert_erase h]
  rw [un_insert, un_update_of_not_mem _ _ _ _ (Finset.notMem_erase i s),
    Function.update_self]

/-- The rank condition: every index set `s` has at most as many indices as the dimension of
the span of its union. -/
def Good (K : Type*) [Field K] [Module K W] (A : ι → Finset W) : Prop :=
  ∀ s : Finset ι, s.card ≤ finrank K (span K (un A s))

lemma finrank_span_mono {X Y : Set W} (hY : Y.Finite) (h : X ⊆ Y) :
    finrank K (span K X) ≤ finrank K (span K Y) := by
  haveI := FiniteDimensional.span_of_finite K hY
  exact Submodule.finrank_mono (span_mono h)

/-- If removing `c` from `A i` breaks the rank condition, there is an index set `t` avoiding
`i` with `dim span ((A i).erase c ∪ un A t) ≤ |t|`. -/
lemma bad_erase [DecidableEq ι] [DecidableEq W] (A : ι → Finset W) (hA : Good K A) (i : ι)
    (c : W) (h : ¬ Good K (Function.update A i ((A i).erase c))) :
    ∃ t : Finset ι, i ∉ t ∧
      finrank K (span K ((((A i).erase c : Finset W) : Set W) ∪ un A t)) ≤ t.card := by
  simp only [Good, not_forall, not_le] at h
  obtain ⟨s, hs⟩ := h
  by_cases hi : i ∈ s
  · refine ⟨s.erase i, Finset.notMem_erase i s, ?_⟩
    rw [un_update_of_mem _ _ _ _ hi] at hs
    have := Finset.card_erase_add_one hi
    omega
  · rw [un_update_of_not_mem _ _ _ _ hi] at hs
    exact absurd (hA s) (not_le.mpr hs)

/-- The Rado / Mirsky reduction step: of two distinct elements of `A i`, one can be removed
keeping the rank condition. -/
lemma erase_good [DecidableEq ι] [DecidableEq W] (A : ι → Finset W) (hA : Good K A) (i : ι)
    {a b : W} (ha : a ∈ A i) (hb : b ∈ A i) (hab : a ≠ b) :
    Good K (Function.update A i ((A i).erase a)) ∨
      Good K (Function.update A i ((A i).erase b)) := by
  by_contra hcon
  rw [not_or] at hcon
  obtain ⟨t1, hi1, h1⟩ := bad_erase A hA i a hcon.1
  obtain ⟨t2, hi2, h2⟩ := bad_erase A hA i b hcon.2
  set X : Set W := (((A i).erase a : Finset W) : Set W) ∪ un A t1 with hX
  set Y : Set W := (((A i).erase b : Finset W) : Set W) ∪ un A t2 with hY
  have hXf : X.Finite := ((A i).erase a).finite_toSet.union (un_finite A t1)
  have hYf : Y.Finite := ((A i).erase b).finite_toSet.union (un_finite A t2)
  haveI : FiniteDimensional K (span K X) := FiniteDimensional.span_of_finite K hXf
  haveI : FiniteDimensional K (span K Y) := FiniteDimensional.span_of_finite K hYf
  have hmod := Submodule.finrank_sup_add_finrank_inf_eq (span K X) (span K Y)
  -- the union side
  have hU : un A (insert i (t1 ∪ t2)) ⊆ X ∪ Y := by
    rw [un_insert, un_union]
    intro x hx
    rcases hx with hx | hx | hx
    · by_cases hxa : x = a
      · subst hxa
        exact Or.inr (Or.inl (Finset.mem_coe.mpr (Finset.mem_erase.mpr ⟨hab, ha⟩)))
      · exact Or.inl (Or.inl (by simp [Finset.mem_erase, hxa, hx]))
    · exact Or.inl (Or.inr hx)
    · exact Or.inr (Or.inr hx)
  have hi12 : i ∉ t1 ∪ t2 := by simp [hi1, hi2]
  have hcardU := hA (insert i (t1 ∪ t2))
  rw [Finset.card_insert_of_notMem hi12] at hcardU
  have hsup : finrank K (span K (un A (insert i (t1 ∪ t2)))) ≤ finrank K ↥(span K X ⊔ span K Y) := by
    rw [← Submodule.span_union]
    exact finrank_span_mono (hXf.union hYf) hU
  -- the intersection side
  have hinf : finrank K (span K (un A (t1 ∩ t2))) ≤ finrank K ↥(span K X ⊓ span K Y) := by
    haveI : FiniteDimensional K ↥(span K X ⊓ span K Y) :=
      Submodule.finiteDimensional_inf_left _ _
    refine Submodule.finrank_mono (le_inf (span_mono ?_) (span_mono ?_))
    · exact (un_mono A Finset.inter_subset_left).trans Set.subset_union_right
    · exact (un_mono A Finset.inter_subset_right).trans Set.subset_union_right
  have hcardI := hA (t1 ∩ t2)
  have hc := Finset.card_union_add_card_inter t1 t2
  omega

/-- Rado's theorem, by induction on the total size of the sets. -/
theorem rado_aux [Fintype ι] [DecidableEq ι] [DecidableEq W] :
    ∀ n : ℕ, ∀ A : ι → Finset W, ∑ j, (A j).card = n → Good K A →
      ∃ f : ι → W, (∀ j, f j ∈ A j) ∧ LinearIndependent K f := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
  intro A hn hA
  by_cases hbig : ∃ i, 1 < (A i).card
  · obtain ⟨i, hi⟩ := hbig
    obtain ⟨a, ha, b, hb, hab⟩ := Finset.one_lt_card.mp hi
    have key : ∃ c ∈ A i, Good K (Function.update A i ((A i).erase c)) := by
      rcases erase_good A hA i ha hb hab with h | h
      · exact ⟨a, ha, h⟩
      · exact ⟨b, hb, h⟩
    obtain ⟨c, hc, hgood⟩ := key
    set A' := Function.update A i ((A i).erase c) with hA'
    have hlt : ∑ j, (A' j).card < n := by
      rw [← hn]
      refine Finset.sum_lt_sum (fun j _ => ?_) ⟨i, Finset.mem_univ _, ?_⟩
      · by_cases hj : j = i
        · subst hj; simp only [hA', Function.update_self]
          exact Finset.card_erase_le
        · simp only [hA', Function.update_of_ne hj, le_refl]
      · simp only [hA', Function.update_self]
        exact Finset.card_erase_lt_of_mem hc
    obtain ⟨f, hf, hli⟩ := ih _ hlt A' rfl hgood
    refine ⟨f, fun j => ?_, hli⟩
    have := hf j
    by_cases hj : j = i
    · subst hj; simp only [hA', Function.update_self] at this
      exact Finset.mem_of_mem_erase this
    · simpa only [hA', Function.update_of_ne hj] using this
  · push_neg at hbig
    have hone : ∀ j, ∃ v, A j = {v} := by
      intro j
      refine Finset.card_eq_one.mp (le_antisymm (hbig j) ?_)
      have h1 := hA {j}
      have hunj : un A {j} = (A j : Set W) := by simp [un]
      rw [hunj, Finset.card_singleton] at h1
      rw [Nat.one_le_iff_ne_zero] at h1 ⊢
      intro h0
      rw [Finset.card_eq_zero] at h0
      apply h1
      simp [h0]
    choose f hf using hone
    refine ⟨f, fun j => by simp [hf j], ?_⟩
    rw [linearIndependent_iff_card_le_finrank_span]
    have h := hA Finset.univ
    have hr : un A Finset.univ = Set.range f := by
      ext x; simp [un, hf, eq_comm]
    rw [hr, Finset.card_univ] at h
    exact h

end Rado

namespace TR
open Module
def StmtCentred : Prop :=
  ∀ (q : ℕ) (L : Submodule ℂ (Fin 3 × Fin q → ℂ)), 1 ≤ q → (∀ t ∈ L, (∀ i : Fin 3, ∑ j, t (i, j) = 0) ∧ (∑ j, ∑ l, if j = l then 0 else (t (0, j) * t (1, l) + t (0, j) * t (2, l) + t (1, j) * t (2, l))) = 0 ∧ (∑ j, ∑ l, ∑ m, if j = l ∨ j = m ∨ l = m then 0 else t (0, j) * t (1, l) * t (2, m)) = 0) → Module.finrank ℂ L + 1 ≤ q
def RadoStmt : Prop :=
  ∀ (K : Type) [Field K] (W : Type) [AddCommGroup W] [Module K W] (ι : Type) [Fintype ι] [DecidableEq ι] (A : ι → Finset W), (∀ U : Finset ι, U.card ≤ Module.finrank K (Submodule.span K (⋃ j ∈ U, (A j : Set W)))) → ∃ f : ι → W, (∀ j, f j ∈ A j) ∧ LinearIndependent K f

variable {κ : Type} [Fintype κ] [DecidableEq κ]

/-- First elementary symmetric function of column `j`. -/
def e1 (x : Fin 3 × κ → ℂ) (j : κ) : ℂ := x (0, j) + x (1, j) + x (2, j)

/-- Second elementary symmetric function of column `j`. -/
def e2 (x : Fin 3 × κ → ℂ) (j : κ) : ℂ := x (0, j) * x (1, j) + x (0, j) * x (2, j) + x (1, j) * x (2, j)

/-- Third elementary symmetric function of column `j`. -/
def e3 (x : Fin 3 × κ → ℂ) (j : κ) : ℂ := x (0, j) * x (1, j) * x (2, j)

/-- The hypothesis of the induction: every element of `V` is supported on the columns of `C`
and has the three column-symmetric sums zero. -/
def Good (V : Submodule ℂ (Fin 3 × κ → ℂ)) (C : Finset κ) : Prop :=
  ∀ x ∈ V, (∀ i, ∀ j ∉ C, x (i, j) = 0) ∧ ∑ j, e1 x j = 0 ∧ ∑ j, e2 x j = 0 ∧ ∑ j, e3 x j = 0

/-- The entry functional `x ↦ x (i, j)` on `V`. -/
def g (V : Submodule ℂ (Fin 3 × κ → ℂ)) (i : Fin 3) (j : κ) : Module.Dual ℂ V :=
  (LinearMap.proj (R := ℂ) (φ := fun _ : Fin 3 × κ => ℂ) (i, j)).comp V.subtype

theorem g_apply (V : Submodule ℂ (Fin 3 × κ → ℂ)) (i : Fin 3) (j : κ) (x : V) :
    g V i j x = (x : Fin 3 × κ → ℂ) (i, j) := rfl

/-- The entry functionals of the columns in `U`. -/
def S (V : Submodule ℂ (Fin 3 × κ → ℂ)) (U : Finset κ) : Set (Module.Dual ℂ V) :=
  {φ | ∃ i, ∃ j ∈ U, φ = g V i j}

theorem mem_coann_span_iff {V : Type} [AddCommGroup V] [Module ℂ V] (T : Set (Module.Dual ℂ V))
    (x : V) : x ∈ (Submodule.span ℂ T).dualCoannihilator ↔ ∀ φ ∈ T, φ x = 0 := by
  rw [Submodule.mem_dualCoannihilator]
  constructor
  · intro h φ hφ
    exact h φ (Submodule.subset_span hφ)
  · intro h φ hφ
    have hle : Submodule.span ℂ T ≤ LinearMap.ker (Module.Dual.eval ℂ V x) := by
      rw [Submodule.span_le]
      intro ψ hψ
      simp [h ψ hψ]
    have := hle hφ
    simpa using this

theorem mem_coann_S (V : Submodule ℂ (Fin 3 × κ → ℂ)) (U : Finset κ) (x : V) :
    x ∈ (Submodule.span ℂ (S V U)).dualCoannihilator ↔
      ∀ i, ∀ j ∈ U, (x : Fin 3 × κ → ℂ) (i, j) = 0 := by
  rw [mem_coann_span_iff]
  constructor
  · intro h i j hj
    exact h (g V i j) ⟨i, j, hj, rfl⟩
  · rintro h φ ⟨i, j, hj, rfl⟩
    simpa [g_apply] using h i j hj

theorem finrank_span_S (V : Submodule ℂ (Fin 3 × κ → ℂ)) (U : Finset κ) :
    finrank ℂ (Submodule.span ℂ (S V U)) =
      finrank ℂ V - finrank ℂ (Submodule.span ℂ (S V U)).dualCoannihilator := by
  have h1 := Subspace.finrank_add_finrank_dualCoannihilator_eq (Submodule.span ℂ (S V U))
  omega

/-- Per column: `(a + y0)(a + y1)(a + y2) = a + e1 + e2 + e3` for `a` the indicator of `C`. -/
theorem col_expand (C : Finset κ) (y : Fin 3 × κ → ℂ) (hy : ∀ i, ∀ j ∉ C, y (i, j) = 0)
    (j : κ) :
    ((if j ∈ C then 1 else 0) + y (0, j)) * ((if j ∈ C then 1 else 0) + y (1, j)) *
        ((if j ∈ C then 1 else 0) + y (2, j)) =
      (if j ∈ C then 1 else 0) + e1 y j + e2 y j + e3 y j := by
  by_cases hj : j ∈ C
  · simp only [hj, if_true, e1, e2, e3]; ring
  · simp [hj, e1, e2, e3, hy _ j hj]

theorem bound (hR : RadoStmt) : ∀ (n : ℕ) (C : Finset κ) (V : Submodule ℂ (Fin 3 × κ → ℂ)),
    C.card = n → C.Nonempty → Good V C → finrank ℂ V < n := by
  classical
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
  intro C V hCn hCne hV
  by_contra hcon
  push_neg at hcon
  -- Step 1: strict Hall
  have step1 : ∀ U : Finset κ, U ⊆ C → U.Nonempty →
      finrank ℂ (Submodule.span ℂ (S V U)).dualCoannihilator ≤ C.card - U.card := by
    intro U hUC hUne
    set Kc := (Submodule.span ℂ (S V U)).dualCoannihilator with hKc
    by_cases hUeq : U = C
    · have : Kc = ⊥ := by
        rw [eq_bot_iff]
        intro x hx
        rw [hKc, mem_coann_S] at hx
        rw [Submodule.mem_bot]
        apply Subtype.ext
        funext ⟨i, j⟩
        by_cases hj : j ∈ C
        · exact hx i j (hUeq ▸ hj)
        · exact (hV x.1 x.2).1 i j hj
      rw [this, finrank_bot]
      exact Nat.zero_le _
    · set K := Kc.map V.subtype with hK
      have hKr : finrank ℂ K = finrank ℂ Kc :=
        (LinearEquiv.finrank_eq (Submodule.equivMapOfInjective V.subtype V.injective_subtype Kc)).symm
      have hgood : Good K (C \ U) := by
        intro x hx
        obtain ⟨y, hy, rfl⟩ := Submodule.mem_map.mp hx
        rw [hKc, mem_coann_S] at hy
        obtain ⟨h0, h1, h2, h3⟩ := hV y.1 y.2
        refine ⟨?_, h1, h2, h3⟩
        intro i j hj
        rw [Finset.mem_sdiff, not_and_or, not_not] at hj
        rcases hj with hj | hj
        · exact h0 i j hj
        · exact hy i j hj
      have hlt : (C \ U).card < n := by
        rw [← hCn]
        exact Finset.card_lt_card (Finset.sdiff_ssubset hUC hUne)
      have hne : (C \ U).Nonempty := by
        rw [Finset.sdiff_nonempty]
        intro h
        exact hUeq (Finset.Subset.antisymm hUC h)
      have := ih _ hlt (C \ U) K rfl hne hgood
      rw [Finset.card_sdiff_of_subset hUC] at this
      omega
  -- Step 2: Rado
  let ι := {j // j ∈ C}
  let A : ι → Finset (Module.Dual ℂ V) := fun j => Finset.univ.image (fun i => g V i j.1)
  have hcond : ∀ U : Finset ι, U.card ≤ finrank ℂ
      (Submodule.span ℂ (⋃ j ∈ U, (A j : Set (Module.Dual ℂ V)))) := by
    intro U
    set U' : Finset κ := U.map (Function.Embedding.subtype _) with hU'
    have hset : (⋃ j ∈ U, (A j : Set (Module.Dual ℂ V))) = S V U' := by
      ext φ
      simp only [Set.mem_iUnion, Finset.coe_image, Finset.coe_univ, Set.image_univ,
        Set.mem_range, S, Set.mem_setOf_eq, hU', Finset.mem_map, Function.Embedding.coe_subtype,
        A]
      constructor
      · rintro ⟨j, hj, i, rfl⟩
        exact ⟨i, j.1, ⟨j, hj, rfl⟩, rfl⟩
      · rintro ⟨i, _, ⟨j, hj, rfl⟩, rfl⟩
        exact ⟨j, hj, i, rfl⟩
    rw [hset, finrank_span_S]
    have hcard : U'.card = U.card := Finset.card_map _
    have hsub : U' ⊆ C := by
      intro j hj
      rw [hU', Finset.mem_map] at hj
      obtain ⟨a, _, rfl⟩ := hj
      exact a.2
    have hUle : U'.card ≤ C.card := Finset.card_le_card hsub
    rcases U'.eq_empty_or_nonempty with he | hne
    · have : U.card = 0 := by rw [← hcard, he, Finset.card_empty]
      omega
    · have := step1 U' hsub hne
      omega
  obtain ⟨f, hfA, hfind⟩ := hR ℂ (Module.Dual ℂ V) ι A hcond
  have hσ : ∀ j : ι, ∃ i : Fin 3, g V i j.1 = f j := by
    intro j
    have := hfA j
    simpa [A] using this
  choose σ hσ using hσ
  -- the evaluation map at the chosen functionals is onto
  let Ψ : V →ₗ[ℂ] (ι → ℂ) := LinearMap.pi (fun j => f j)
  have hker : LinearMap.ker Ψ = (Submodule.span ℂ (Set.range f)).dualCoannihilator := by
    ext x
    rw [mem_coann_span_iff, LinearMap.mem_ker]
    constructor
    · rintro h φ ⟨j, rfl⟩
      exact congrFun h j
    · intro h
      funext j
      exact h (f j) ⟨j, rfl⟩
  have hspan : finrank ℂ (Submodule.span ℂ (Set.range f)) = Fintype.card ι :=
    finrank_span_eq_card hfind
  have h1 := Subspace.finrank_add_finrank_dualCoannihilator_eq (Submodule.span ℂ (Set.range f))
  have hrn := LinearMap.finrank_range_add_finrank_ker Ψ
  have hfun : finrank ℂ (ι → ℂ) = Fintype.card ι := Module.finrank_fintype_fun_eq_card ℂ
  have htop : LinearMap.range Ψ = ⊤ := by
    apply Submodule.eq_top_of_finrank_eq
    rw [hker] at hrn
    omega
  obtain ⟨y, hy⟩ : (fun _ => (-1 : ℂ)) ∈ LinearMap.range Ψ := htop ▸ Submodule.mem_top
  have hyσ : ∀ j : ι, (y : Fin 3 × κ → ℂ) (σ j, j.1) = -1 := by
    intro j
    have := congrFun hy j
    simp only [Ψ, LinearMap.pi_apply] at this
    rw [← hσ j] at this
    simpa [Ψ, g_apply] using this
  -- Step 3: the shifted point has a zero in every column
  obtain ⟨hy0, hy1, hy2, hy3⟩ := hV y.1 y.2
  have hzero : ∀ j : κ,
      ((if j ∈ C then 1 else 0) + (y : Fin 3 × κ → ℂ) (0, j)) *
          ((if j ∈ C then 1 else 0) + (y : Fin 3 × κ → ℂ) (1, j)) *
          ((if j ∈ C then 1 else 0) + (y : Fin 3 × κ → ℂ) (2, j)) = 0 := by
    intro j
    by_cases hj : j ∈ C
    · have h := hyσ ⟨j, hj⟩
      simp only [hj, if_true]
      generalize σ ⟨j, hj⟩ = s at h
      fin_cases s
      · simp only [Fin.zero_eta] at h; rw [h]; ring
      · simp only [Fin.mk_one] at h; rw [h]; ring
      · simp only [Fin.reduceFinMk] at h; rw [h]; ring
    · simp [hj, hy0 _ j hj]
  have hsum := Finset.sum_congr rfl (fun j (_ : j ∈ Finset.univ) => col_expand C y.1 hy0 j)
  simp only [hzero, Finset.sum_const_zero] at hsum
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib, Finset.sum_add_distrib, hy1, hy2, hy3,
    Finset.sum_boole] at hsum
  simp only [Finset.filter_mem_eq_inter, Finset.univ_inter, add_zero] at hsum
  have hc : (C.card : ℂ) ≠ 0 := by
    exact_mod_cast (Finset.card_pos.mpr hCne).ne'
  exact hc hsum.symm

/-- Step 0: a row-centred level element has the three column-symmetric sums zero. -/
theorem step0 {q : ℕ} (t : Fin 3 × Fin q → ℂ)
    (hrow : ∀ i : Fin 3, ∑ j, t (i, j) = 0)
    (h2 : (∑ j, ∑ l, if j = l then 0 else (t (0, j) * t (1, l) + t (0, j) * t (2, l) + t (1, j) * t (2, l))) = 0)
    (h3 : (∑ j, ∑ l, ∑ m, if j = l ∨ j = m ∨ l = m then 0 else t (0, j) * t (1, l) * t (2, m)) = 0) :
    ∑ j, e1 t j = 0 ∧ ∑ j, e2 t j = 0 ∧ ∑ j, e3 t j = 0 := by
  have r0 := hrow 0
  have r1 := hrow 1
  have r2 := hrow 2
  refine ⟨?_, ?_, ?_⟩
  · simp only [e1, Finset.sum_add_distrib, r0, r1, r2, add_zero]
  · have hsplit : ∀ j l : Fin q, (if j = l then 0 else (t (0, j) * t (1, l) + t (0, j) * t (2, l) + t (1, j) * t (2, l))) =
        (t (0, j) * t (1, l) + t (0, j) * t (2, l) + t (1, j) * t (2, l)) -
          (if j = l then (t (0, j) * t (1, l) + t (0, j) * t (2, l) + t (1, j) * t (2, l)) else 0) := by
      intro j l
      split_ifs <;> ring
    simp only [hsplit, Finset.sum_sub_distrib, Finset.sum_ite_eq, Finset.mem_univ, if_true] at h2
    have hfull : (∑ j, ∑ l, (t (0, j) * t (1, l) + t (0, j) * t (2, l) + t (1, j) * t (2, l))) = 0 := by
      simp only [Finset.sum_add_distrib, ← Finset.sum_mul_sum, r0, r1, zero_mul, add_zero]
    rw [hfull, zero_sub, neg_eq_zero] at h2
    simpa [e2] using h2
  · have hsplit : ∀ j l m : Fin q, (if j = l ∨ j = m ∨ l = m then 0 else t (0, j) * t (1, l) * t (2, m)) =
        t (0, j) * t (1, l) * t (2, m) - (if j = l then t (0, j) * t (1, l) * t (2, m) else 0)
          - (if j = m then t (0, j) * t (1, l) * t (2, m) else 0)
          - (if l = m then t (0, j) * t (1, l) * t (2, m) else 0)
          + 2 * (if j = l then (if l = m then t (0, j) * t (1, l) * t (2, m) else 0) else 0) := by
      intro j l m
      by_cases hjl : j = l <;> by_cases hjm : j = m <;> by_cases hlm : l = m <;>
        simp [hjl, hjm, hlm] <;> (try subst_vars) <;> (try simp_all) <;> ring
    simp only [hsplit, Finset.sum_add_distrib, Finset.sum_sub_distrib] at h3
    have a1 : (∑ j, ∑ l, ∑ m, t (0, j) * t (1, l) * t (2, m)) = 0 := by
      simp only [← Finset.mul_sum, ← Finset.sum_mul, r2, r1, r0, mul_zero, zero_mul,
        Finset.sum_const_zero]
    have a2 : (∑ j, ∑ l, ∑ m, if j = l then t (0, j) * t (1, l) * t (2, m) else 0) = 0 := by
      have : ∀ j l : Fin q, (∑ m, if j = l then t (0, j) * t (1, l) * t (2, m) else 0) =
          if j = l then t (0, j) * t (1, l) * ∑ m, t (2, m) else 0 := by
        intro j l; split_ifs <;> simp [Finset.mul_sum]
      simp only [this, r2, mul_zero, ite_self, Finset.sum_const_zero]
    have a3 : (∑ j, ∑ l, ∑ m, if j = m then t (0, j) * t (1, l) * t (2, m) else 0) = 0 := by
      simp only [Finset.sum_ite_eq, Finset.mem_univ, if_true]
      simp only [mul_right_comm _ _ (t (2, _)), ← Finset.mul_sum, r1, mul_zero,
        Finset.sum_const_zero]
    have a4 : (∑ j, ∑ l, ∑ m, if l = m then t (0, j) * t (1, l) * t (2, m) else 0) = 0 := by
      simp only [Finset.sum_ite_eq, Finset.mem_univ, if_true]
      simp only [mul_assoc, ← Finset.mul_sum, ← Finset.sum_mul, r0, zero_mul]
    have a5 : (∑ j, ∑ l, ∑ m, if j = l then (if l = m then t (0, j) * t (1, l) * t (2, m) else 0) else 0) =
        ∑ j, e3 t j := by
      have : ∀ j l : Fin q, (∑ m, if j = l then (if l = m then t (0, j) * t (1, l) * t (2, m) else 0) else 0) =
          if j = l then t (0, j) * t (1, l) * t (2, l) else 0 := by
        intro j l; split_ifs <;> simp [Finset.sum_ite_eq]
      simp only [this, Finset.sum_ite_eq, Finset.mem_univ, if_true, e3]
    have a6 : (∑ j, ∑ l, ∑ m, 2 * if j = l then (if l = m then t (0, j) * t (1, l) * t (2, m) else 0) else 0) =
        2 * ∑ j, e3 t j := by
      rw [← a5]; simp only [Finset.mul_sum]
    rw [a1, a2, a3, a4, a6] at h3
    have : (2 : ℂ) * ∑ j, e3 t j = 0 := by linear_combination h3
    simpa using this

theorem centred_of_rado : RadoStmt → StmtCentred := by
  intro hR q L hq hL
  have hgood : Good L (Finset.univ : Finset (Fin q)) := by
    intro x hx
    obtain ⟨hrow, h2, h3⟩ := hL x hx
    exact ⟨fun i j hj => absurd (Finset.mem_univ j) hj, step0 x hrow h2 h3⟩
  have hne : (Finset.univ : Finset (Fin q)).Nonempty :=
    Finset.univ_nonempty_iff.mpr ⟨⟨0, hq⟩⟩
  have := bound hR q Finset.univ L (by simp) hne hgood
  omega



theorem rado171 : RadoStmt := by
  intro K _ W _ _ ι _ _ A hA
  classical
  exact Rado.rado_aux _ A rfl hA

theorem centred : StmtCentred := centred_of_rado rado171

end TR


namespace Main
open Module Finset

abbrev M := Fin 4 × Fin 7 → ℂ

/-- The level conditions of the statement, for one matrix. -/
def Lev (t : M) : Prop :=
  (∑ i : Fin 4, ∑ j, t (i, j)) = 0 ∧ (∑ j, ∑ l, if j = l then 0 else ∑ a : Fin 4, ∑ b : Fin 4, if a < b then t (a, j) * t (b, l) else 0) = 0 ∧ (∑ j, ∑ l, ∑ m, if j = l ∨ j = m ∨ l = m then 0 else ∑ a : Fin 4, ∑ b : Fin 4, ∑ c : Fin 4, if a < b ∧ b < c then t (a, j) * t (b, l) * t (c, m) else 0) = 0 ∧ (∑ j, ∑ l, ∑ m, ∑ n, if j = l ∨ j = m ∨ j = n ∨ l = m ∨ l = n ∨ m = n then 0 else t (0, j) * t (1, l) * t (2, m) * t (3, n)) = 0

/-- Row sums. -/
def rs : M →ₗ[ℂ] (Fin 4 → ℂ) where
  toFun t i := ∑ j, t (i, j)
  map_add' a b := by ext i; simp [Finset.sum_add_distrib]
  map_smul' c a := by ext i; simp [Finset.mul_sum]

/-- Column sums. -/
def cs : M →ₗ[ℂ] (Fin 7 → ℂ) where
  toFun t j := ∑ i, t (i, j)
  map_add' a b := by ext j; simp [Finset.sum_add_distrib]
  map_smul' c a := by ext j; simp [Finset.mul_sum]

def s4 : (Fin 4 → ℂ) →ₗ[ℂ] ℂ where
  toFun a := ∑ i, a i
  map_add' a b := by simp [Finset.sum_add_distrib]
  map_smul' c a := by simp [Finset.mul_sum]

def s7 : (Fin 7 → ℂ) →ₗ[ℂ] ℂ where
  toFun a := ∑ i, a i
  map_add' a b := by simp [Finset.sum_add_distrib]
  map_smul' c a := by simp [Finset.mul_sum]

/-- The two totals of a pair (row sums, column sums). -/
def tot : ((Fin 4 → ℂ) × (Fin 7 → ℂ)) →ₗ[ℂ] ℂ × ℂ :=
  (s4.comp (LinearMap.fst ℂ _ _)).prod (s7.comp (LinearMap.snd ℂ _ _))

theorem finrank_ker_tot : finrank ℂ (LinearMap.ker tot) = 9 := by
  have h := LinearMap.finrank_range_add_finrank_ker tot
  have hr : LinearMap.range tot = ⊤ := by
    rw [LinearMap.range_eq_top]
    rintro ⟨x, y⟩
    refine ⟨(Pi.single 0 x, Pi.single 0 y), ?_⟩
    simp [tot, s4, s7]
  rw [hr, finrank_top] at h
  simp at h
  omega

/-- Line-sum split: if no nonzero member of `L` is doubly centred, `dim L ≤ 9`. -/
theorem partA (L : Submodule ℂ M) (hL : ∀ t ∈ L, Lev t)
    (hD : ∀ t ∈ L, rs t = 0 → cs t = 0 → t = 0) : finrank ℂ L ≤ 9 := by
  let f := (rs.prod cs).domRestrict L
  have hk : LinearMap.ker f = ⊥ := by
    rw [LinearMap.ker_eq_bot']
    intro x hx
    have h1 : rs x.1 = 0 := congrArg Prod.fst hx
    have h2 : cs x.1 = 0 := congrArg Prod.snd hx
    exact Subtype.ext (hD x.1 x.2 h1 h2)
  have h1 := LinearMap.finrank_range_add_finrank_ker f
  rw [hk, finrank_bot] at h1
  have h2 : LinearMap.range f ≤ LinearMap.ker tot := by
    rintro _ ⟨x, rfl⟩
    rw [LinearMap.mem_ker]
    have e := (hL x.1 x.2).1
    refine Prod.ext ?_ ?_
    · change ∑ i, ∑ j, x.1 (i, j) = 0
      exact e
    · change ∑ j, ∑ i, x.1 (i, j) = 0
      rw [Finset.sum_comm]
      exact e
  have h3 := Submodule.finrank_mono h2
  rw [finrank_ker_tot] at h3
  omega

/-- Line-sum split: `dim L ≤ 9 + dim D`, where `D` is the doubly centred part of `L`. -/
theorem splitA (L : Submodule ℂ M) (hL : ∀ t ∈ L, Lev t) :
    finrank ℂ L ≤ 9 + finrank ℂ (L ⊓ LinearMap.ker (rs.prod cs) : Submodule ℂ M) := by
  let f := (rs.prod cs).domRestrict L
  have h1 := LinearMap.finrank_range_add_finrank_ker f
  have h2 : LinearMap.range f ≤ LinearMap.ker tot := by
    rintro _ ⟨x, rfl⟩
    rw [LinearMap.mem_ker]
    have e := (hL x.1 x.2).1
    refine Prod.ext ?_ ?_
    · change ∑ i, ∑ j, x.1 (i, j) = 0
      exact e
    · change ∑ j, ∑ i, x.1 (i, j) = 0
      rw [Finset.sum_comm]
      exact e
  have h3 := Submodule.finrank_mono h2
  rw [finrank_ker_tot] at h3
  have h4 : (LinearMap.ker f).map L.subtype ≤ (L ⊓ LinearMap.ker (rs.prod cs) : Submodule ℂ M) := by
    rintro _ ⟨x, hx, rfl⟩
    exact ⟨x.2, hx⟩
  have h5 := Submodule.finrank_mono h4
  have h6 : finrank ℂ ((LinearMap.ker f).map L.subtype) = finrank ℂ (LinearMap.ker f) :=
    (LinearEquiv.finrank_eq
      (Submodule.equivMapOfInjective L.subtype L.injective_subtype (LinearMap.ker f))).symm
  omega

/-- Row `u`. -/
def rw4 (u : Fin 4) : M →ₗ[ℂ] (Fin 7 → ℂ) := LinearMap.funLeft ℂ ℂ fun j => (u, j)

/-- Row `u` together with the row sums. -/
def phi (u : Fin 4) : M →ₗ[ℂ] (Fin 7 → ℂ) × (Fin 4 → ℂ) := (rw4 u).prod rs

/-- The three rows other than `u`. -/
def restr (u : Fin 4) : M →ₗ[ℂ] (Fin 3 × Fin 7 → ℂ) :=
  LinearMap.funLeft ℂ ℂ fun p => (u.succAbove p.1, p.2)

theorem red2 (u : Fin 4) (t : M) (h0 : ∀ j, t (u, j) = 0) :
    (∑ j, ∑ l, if j = l then 0 else ∑ a : Fin 4, ∑ b : Fin 4, if a < b then t (a, j) * t (b, l) else 0) =
    ∑ j, ∑ l, if j = l then 0 else (restr u t (0, j) * restr u t (1, l) + restr u t (0, j) * restr u t (2, l) + restr u t (1, j) * restr u t (2, l)) := by
  refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun l _ => ?_
  split_ifs with h
  · rfl
  simp only [restr, LinearMap.funLeft_apply, Fin.sum_univ_four]
  obtain rfl | rfl | rfl | rfl : u = 0 ∨ u = 1 ∨ u = 2 ∨ u = 3 := by
    fin_cases u <;> simp
  all_goals simp (config := {decide := true}) [Fin.succAbove, h0]
  all_goals ring

theorem red3 (u : Fin 4) (t : M) (h0 : ∀ j, t (u, j) = 0) :
    (∑ j, ∑ l, ∑ m, if j = l ∨ j = m ∨ l = m then 0 else ∑ a : Fin 4, ∑ b : Fin 4, ∑ c : Fin 4, if a < b ∧ b < c then t (a, j) * t (b, l) * t (c, m) else 0) =
    ∑ j, ∑ l, ∑ m, if j = l ∨ j = m ∨ l = m then 0 else restr u t (0, j) * restr u t (1, l) * restr u t (2, m) := by
  refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun l _ => Finset.sum_congr rfl fun m _ => ?_
  split_ifs with h
  · rfl
  simp only [restr, LinearMap.funLeft_apply, Fin.sum_univ_four]
  obtain rfl | rfl | rfl | rfl : u = 0 ∨ u = 1 ∨ u = 2 ∨ u = 3 := by
    fin_cases u <;> simp
  all_goals simp (config := {decide := true}) [Fin.succAbove, h0]
  all_goals ring

/-- Three-row reduction: `dim L ≤ 6 + rank (row u, row sums)`. -/
theorem partB (L : Submodule ℂ M) (hL : ∀ t ∈ L, Lev t) (u : Fin 4) :
    finrank ℂ L ≤ 6 + finrank ℂ (L.map (phi u)) := by
  let f := (phi u).domRestrict L
  have h1 := LinearMap.finrank_range_add_finrank_ker f
  rw [LinearMap.range_domRestrict] at h1
  let N := LinearMap.ker f
  let g : N →ₗ[ℂ] (Fin 3 × Fin 7 → ℂ) := (restr u).comp (L.subtype.comp N.subtype)
  have hrow : ∀ x : N, ∀ j, x.1.1 (u, j) = 0 := by
    intro x j
    have hx0 : f x.1 = 0 := LinearMap.mem_ker.mp x.2
    exact congrFun (congrArg Prod.fst hx0) j
  have hrs : ∀ x : N, rs x.1.1 = 0 := by
    intro x
    have hx0 : f x.1 = 0 := LinearMap.mem_ker.mp x.2
    exact congrArg Prod.snd hx0
  have gker : LinearMap.ker g = ⊥ := by
    rw [LinearMap.ker_eq_bot']
    intro x hx
    apply Subtype.ext
    apply Subtype.ext
    funext p
    obtain ⟨i, j⟩ := p
    by_cases hi : i = u
    · subst hi
      exact hrow x j
    · obtain ⟨k, rfl⟩ := Fin.exists_succAbove_eq hi
      exact congrFun hx (k, j)
  have ginj : Function.Injective g := by
    rw [injective_iff_map_eq_zero]
    intro x hx
    have hm : x ∈ LinearMap.ker g := hx
    rw [gker] at hm
    exact (Submodule.mem_bot ℂ).mp hm
  have h2 := LinearMap.finrank_range_of_inj ginj
  have h3 := TR.centred 7 (LinearMap.range g) (by norm_num) (by
    rintro s ⟨x, rfl⟩
    obtain ⟨_, e2, e3, _⟩ := hL x.1.1 x.1.2
    refine ⟨fun i => ?_, ?_, ?_⟩
    · exact congrFun (hrs x) (u.succAbove i)
    · rw [red2 u _ (hrow x)] at e2
      exact e2
    · rw [red3 u _ (hrow x)] at e3
      exact e3)
  have hN : finrank ℂ N = finrank ℂ (LinearMap.ker f) := rfl
  omega

/-- The two proved cases. -/
theorem partAB (L : Submodule ℂ M) (hL : ∀ t ∈ L, Lev t)
    (h : (∀ t ∈ L, rs t = 0 → cs t = 0 → t = 0) ∨ ∃ u, finrank ℂ (L.map (phi u)) ≤ 3) :
    finrank ℂ L ≤ 9 := by
  rcases h with h | ⟨u, hu⟩
  · exact partA L hL h
  · have := partB L hL u
    omega


set_option maxRecDepth 100000 in
set_option maxHeartbeats 20000000 in
/-- The order-2 identity (L-gct-159 at 4 x 7, with the zero entry sum): on a level matrix the
sum of squared entries equals the sum of squared row sums plus squared column sums. -/
theorem sq_id (t : M) (h1 : (∑ i : Fin 4, ∑ j, t (i, j)) = 0)
    (h2 : (∑ j, ∑ l, if j = l then 0 else ∑ a : Fin 4, ∑ b : Fin 4, if a < b then t (a, j) * t (b, l) else 0) = 0) :
    ∑ i : Fin 4, ∑ j : Fin 7, t (i, j) ^ 2 = ∑ i, rs t i ^ 2 + ∑ j, cs t j ^ 2 := by
  simp only [rs, cs, LinearMap.coe_mk, AddHom.coe_mk]
  simp (config := {decide := true}) only [Fin.sum_univ_four, Fin.sum_univ_seven, ite_true, ite_false,
    add_zero, zero_add, Fin.isValue] at h1 h2 ⊢
  linear_combination (2 : ℂ) * h2 - (t (0, 0) + t (0, 1) + t (0, 2) + t (0, 3) + t (0, 4) + t (0, 5) + t (0, 6) +
    (t (1, 0) + t (1, 1) + t (1, 2) + t (1, 3) + t (1, 4) + t (1, 5) + t (1, 6)) +
    (t (2, 0) + t (2, 1) + t (2, 2) + t (2, 3) + t (2, 4) + t (2, 5) + t (2, 6)) +
    (t (3, 0) + t (3, 1) + t (3, 2) + t (3, 3) + t (3, 4) + t (3, 5) + t (3, 6))) * h1

/-- Gram identity: on a level space the entrywise dot product is the dot product of the line
sums. In particular a doubly centred member of `L` is orthogonal to all of `L`. -/
theorem gram (L : Submodule ℂ M) (hL : ∀ t ∈ L, Lev t) (t s : M) (ht : t ∈ L) (hs : s ∈ L) :
    ∑ i : Fin 4, ∑ j : Fin 7, t (i, j) * s (i, j) =
      ∑ i, rs t i * rs s i + ∑ j, cs t j * cs s j := by
  have a := sq_id t (hL t ht).1 (hL t ht).2.1
  have b := sq_id s (hL s hs).1 (hL s hs).2.1
  have c := sq_id (t + s) (hL _ (L.add_mem ht hs)).1 (hL _ (L.add_mem ht hs)).2.1
  simp only [map_add, Pi.add_apply, add_sq, Finset.sum_add_distrib] at c
  have c1 : ∑ x : Fin 4, ∑ y : Fin 7, 2 * t (x, y) * s (x, y) = 2 * ∑ x : Fin 4, ∑ y : Fin 7, t (x, y) * s (x, y) := by
    simp only [Finset.mul_sum, mul_assoc]
  have c2 : ∑ x : Fin 4, 2 * rs t x * rs s x = 2 * ∑ x : Fin 4, rs t x * rs s x := by
    simp only [Finset.mul_sum, mul_assoc]
  have c3 : ∑ x : Fin 7, 2 * cs t x * cs s x = 2 * ∑ x : Fin 7, cs t x * cs s x := by
    simp only [Finset.mul_sum, mul_assoc]
  rw [c1, c2, c3] at c
  linear_combination (c - a - b) / 2

theorem perp (L : Submodule ℂ M) (hL : ∀ t ∈ L, Lev t) (d s : M) (hd : d ∈ L) (hs : s ∈ L)
    (h1 : rs d = 0) (h2 : cs d = 0) : ∑ i : Fin 4, ∑ j : Fin 7, d (i, j) * s (i, j) = 0 := by
  rw [gram L hL d s hd hs, h1, h2]
  simp

end Main

end PEqualNP.Outside.L_gct_196_partial3
