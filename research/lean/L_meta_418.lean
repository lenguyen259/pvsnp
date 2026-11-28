import Mathlib
import PEqualNP.Defs

open PEqualNP.CircuitLowerBounds

namespace PEqualNP.Outside.L_meta_418

private def adj (i j : Fin 4) : Bool :=
  decide ((i.val, j.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3)] : List (ℕ × ℕ)) ∨ (j.val, i.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3)] : List (ℕ × ℕ)))

private def m_e (i : Fin 4) : Fin 4 → Bool := fun k => decide (k = i)

private def m_pair (i j : Fin 4) : Fin 4 → Bool := fun k => m_e i k || m_e j k

private def m_hom (a : (Fin 4 → Bool) → Bool) : Prop :=
  ∀ x y : Fin 4 → Bool, a (fun i => x i || y i) = (a x || a y)

private theorem m_hom_pair {a : (Fin 4 → Bool) → Bool} (ha : m_hom a) (i j : Fin 4) :
    a (m_pair i j) = (a (m_e i) || a (m_e j)) := ha _ _

set_option maxRecDepth 100000 in
private theorem tri : ∀ i j : Fin 4,
    ((∃ u v : Fin 4, (u.val, v.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3)] : List (ℕ × ℕ)) ∧
      m_pair i j u = true ∧ m_pair i j v = true) ↔ adj i j = true) := by decide

private theorem key : ∀ h0 h1 h2 a0 a1 a2 b0 b1 b2 c : Bool,
    false = ((h0 || h0) || c && ((a0 || a0) && (b0 || b0))) →
    false = ((h1 || h1) || c && ((a1 || a1) && (b1 || b1))) →
    false = ((h2 || h2) || c && ((a2 || a2) && (b2 || b2))) →
    true = ((h0 || h1) || c && ((a0 || a1) && (b0 || b1))) →
    true = ((h0 || h2) || c && ((a0 || a2) && (b0 || b2))) →
    true = ((h1 || h2) || c && ((a1 || a2) && (b1 || b2))) → False := by
  decide

private def m_cl (G : List ((Fin 4 → Bool) → Bool)) (w : (Fin 4 → Bool) → Bool) : Prop :=
  ∃ h, m_hom h ∧ ∃ G' : List ((Fin 4 → Bool) → Bool),
    (∀ g ∈ G', g ∈ G) ∧ ∀ x, w x = (h x || G'.any (fun g => g x))

private def m_good : List ((Fin 4 → Bool) → Bool) → Prop
  | [] => True
  | g :: G => (∃ u v, m_cl G u ∧ m_cl G v ∧ ∀ x, g x = (u x && v x)) ∧ m_good G

private theorem m_hom_false : m_hom (fun _ => false) := fun _ _ => rfl

private theorem m_hom_true : m_hom (fun _ => true) := fun _ _ => rfl

private theorem m_cl_of_hom {G : List ((Fin 4 → Bool) → Bool)} {h : (Fin 4 → Bool) → Bool}
    (hh : m_hom h) : m_cl G h :=
  ⟨h, hh, [], by simp, by simp⟩

private theorem m_cl_congr {G : List ((Fin 4 → Bool) → Bool)} {u w : (Fin 4 → Bool) → Bool}
    (hu : m_cl G u) (e : ∀ x, w x = u x) : m_cl G w := by
  obtain ⟨h, hh, G', hs, he⟩ := hu
  exact ⟨h, hh, G', hs, fun x => by rw [e x, he x]⟩

private theorem m_cl_mono {G : List ((Fin 4 → Bool) → Bool)} {w : (Fin 4 → Bool) → Bool}
    (g : (Fin 4 → Bool) → Bool) (hw : m_cl G w) : m_cl (g :: G) w := by
  obtain ⟨h, hh, G', hs, he⟩ := hw
  exact ⟨h, hh, G', fun g' hg' => List.mem_cons_of_mem _ (hs g' hg'), he⟩

private theorem m_cl_or {G : List ((Fin 4 → Bool) → Bool)} {u v : (Fin 4 → Bool) → Bool}
    (hu : m_cl G u) (hv : m_cl G v) : m_cl G (fun x => u x || v x) := by
  obtain ⟨h, hh, G1, hs, he⟩ := hu
  obtain ⟨k, hk, G2, hs2, he2⟩ := hv
  refine ⟨fun x => h x || k x, ?_, G1 ++ G2, ?_, ?_⟩
  · intro x y
    show (h _ || k _) = ((h x || k x) || (h y || k y))
    rw [hh x y, hk x y]
    cases h x <;> cases h y <;> cases k x <;> cases k y <;> rfl
  · intro g hg
    rcases List.mem_append.mp hg with h1 | h1
    · exact hs g h1
    · exact hs2 g h1
  · intro x
    show (u x || v x) = ((h x || k x) || (G1 ++ G2).any fun g => g x)
    rw [he x, he2 x, List.any_append]
    cases h x <;> cases k x <;> cases (G1.any fun g => g x) <;> cases (G2.any fun g => g x) <;> rfl

private theorem m_cl_new (G : List ((Fin 4 → Bool) → Bool)) (g : (Fin 4 → Bool) → Bool) :
    m_cl (g :: G) g :=
  ⟨fun _ => false, m_hom_false, [g], by simp, by simp⟩

private theorem m_gate_or (G : List ((Fin 4 → Bool) → Bool)) (f : ℕ → (Fin 4 → Bool) → Bool)
    (hw : ∀ k, m_cl G (f k)) (ins : List ℕ) (hl : ins.length ≤ 2) :
    m_cl G (fun x => GateOp.eval GateOp.or (ins.map fun i => f i x)) := by
  rcases ins with _ | ⟨i, _ | ⟨j, _ | ⟨k, t⟩⟩⟩
  · exact m_cl_congr (m_cl_of_hom m_hom_false) (fun x => by simp [GateOp.eval])
  · exact m_cl_congr (hw i) (fun x => by simp [GateOp.eval])
  · exact m_cl_congr (m_cl_or (hw i) (hw j)) (fun x => by simp [GateOp.eval])
  · exact absurd hl (by simp only [List.length_cons]; omega)

private theorem m_gate_and (G : List ((Fin 4 → Bool) → Bool)) (f : ℕ → (Fin 4 → Bool) → Bool)
    (hw : ∀ k, m_cl G (f k)) (ins : List ℕ) (hl : ins.length ≤ 2) :
    ∃ u v, m_cl G u ∧ m_cl G v ∧
      ∀ x, GateOp.eval GateOp.and (ins.map fun i => f i x) = (u x && v x) := by
  rcases ins with _ | ⟨i, _ | ⟨j, _ | ⟨k, t⟩⟩⟩
  · exact ⟨fun _ => true, fun _ => true, m_cl_of_hom m_hom_true, m_cl_of_hom m_hom_true,
      fun x => by simp [GateOp.eval]⟩
  · exact ⟨f i, f i, hw i, hw i, fun x => by simp [GateOp.eval]⟩
  · exact ⟨f i, f j, hw i, hw j, fun x => by simp [GateOp.eval]⟩
  · exact absurd hl (by simp only [List.length_cons]; omega)

private def m_W (gs : List Gate) (x : Fin 4 → Bool) : List Bool :=
  gs.foldl (fun w g => w ++ [g.op.eval (g.inputs.map fun i => w.getD i false)]) (List.ofFn x)

private def m_wf (gs : List Gate) (k : ℕ) : (Fin 4 → Bool) → Bool :=
  fun x => (m_W gs x).getD k false

private theorem m_fold_len (gs : List Gate) : ∀ w0 : List Bool,
    (gs.foldl (fun w g => w ++ [g.op.eval (g.inputs.map fun i => w.getD i false)]) w0).length
      = w0.length + gs.length := by
  induction gs with
  | nil => intro w0; simp
  | cons g gs ih => intro w0; rw [List.foldl_cons, ih]; simp; omega

private theorem m_W_len (gs : List Gate) (x : Fin 4 → Bool) :
    (m_W gs x).length = 4 + gs.length := by
  unfold m_W
  rw [m_fold_len]
  simp

private theorem m_W_snoc (gs : List Gate) (g : Gate) (x : Fin 4 → Bool) :
    m_W (gs ++ [g]) x
      = m_W gs x ++ [g.op.eval (g.inputs.map fun i => (m_W gs x).getD i false)] := by
  simp [m_W, List.foldl_append]

private theorem m_wf_snoc (gs : List Gate) (g : Gate) (k : ℕ) :
    m_wf (gs ++ [g]) k = if k = 4 + gs.length then
      (fun x => g.op.eval (g.inputs.map fun i => m_wf gs i x)) else m_wf gs k := by
  funext x
  have hl := m_W_len gs x
  by_cases hk : k = 4 + gs.length
  · rw [if_pos hk]
    show (m_W (gs ++ [g]) x).getD k false = g.op.eval (g.inputs.map fun i => (m_W gs x).getD i false)
    rw [m_W_snoc]
    simp [List.getD_eq_getElem?_getD, List.getElem?_append, hl, hk]
  · rw [if_neg hk]
    show (m_W (gs ++ [g]) x).getD k false = (m_W gs x).getD k false
    rw [m_W_snoc]
    simp only [List.getD_eq_getElem?_getD, List.getElem?_append, hl]
    split
    · rfl
    · rename_i h2
      have h3 : ¬ (k - (4 + gs.length) = 0) := by omega
      have h4 : ¬ k < (m_W gs x).length := by rw [hl]; exact h2
      simp [h3, hl, h2]

private theorem m_base (k : ℕ) : m_hom (m_wf [] k) := by
  intro x y
  unfold m_wf m_W
  simp only [List.foldl_nil, List.getD_eq_getElem?_getD, List.getElem?_ofFn]
  by_cases hk : k < 4
  · simp [hk]
  · simp [hk]

private theorem m_inv (A : Finset ℕ) (gs : List Gate)
    (hm : ∀ g ∈ gs, (g.op = GateOp.and ∨ g.op = GateOp.or) ∧ g.inputs.length ≤ 2)
    (hA : ∀ (j : ℕ) (g : Gate), gs[j]? = some g → g.op = GateOp.and → j ∈ A) :
    ∃ G, m_good G ∧ G.length ≤ (A.filter (fun j => j < gs.length)).card ∧
      ∀ k, m_cl G (m_wf gs k) := by
  induction gs using List.reverseRecOn with
  | nil => exact ⟨[], trivial, by simp, fun k => m_cl_of_hom (m_base k)⟩
  | append_singleton gs g ih =>
    obtain ⟨G, hG, hlen, hw⟩ := ih (fun g' hg' => hm g' (by simp [hg']))
      (fun j g' hj ho => hA j g' (by
        have hjl : j < gs.length := (List.getElem?_eq_some_iff.mp hj).1
        rw [List.getElem?_append_left hjl]; exact hj) ho)
    obtain ⟨hop, hl⟩ := hm g (by simp)
    rcases hop with hop | hop
    · obtain ⟨u, v, hu, hv, he⟩ := m_gate_and G (m_wf gs) hw g.inputs hl
      have hmem : gs.length ∈ A := hA gs.length g (by simp) hop
      refine ⟨(fun x => GateOp.eval GateOp.and (g.inputs.map fun i => m_wf gs i x)) :: G,
        ⟨⟨u, v, hu, hv, he⟩, hG⟩, ?_, ?_⟩
      · have hsub : insert gs.length (A.filter (fun j => j < gs.length))
            ⊆ A.filter (fun j => j < (gs ++ [g]).length) := by
          intro j hj
          simp only [Finset.mem_insert, Finset.mem_filter, List.length_append, List.length_cons,
            List.length_nil] at hj ⊢
          rcases hj with rfl | ⟨h1, h2⟩
          · exact ⟨hmem, by omega⟩
          · exact ⟨h1, by omega⟩
        have hc := Finset.card_le_card hsub
        rw [Finset.card_insert_of_notMem (by simp)] at hc
        simp only [List.length_cons]
        omega
      · intro k
        rw [m_wf_snoc, hop]
        by_cases hk : k = 4 + gs.length
        · rw [if_pos hk]; exact m_cl_new _ _
        · rw [if_neg hk]; exact m_cl_mono _ (hw k)
    · refine ⟨G, hG, ?_, ?_⟩
      · refine le_trans hlen (Finset.card_le_card ?_)
        intro j hj
        simp only [Finset.mem_filter, List.length_append, List.length_cons, List.length_nil] at hj ⊢
        exact ⟨hj.1, by omega⟩
      · intro k
        rw [m_wf_snoc, hop]
        by_cases hk : k = 4 + gs.length
        · rw [if_pos hk]; exact m_gate_or G (m_wf gs) hw g.inputs hl
        · rw [if_neg hk]; exact hw k

private theorem m_any2 (g1 g2 : (Fin 4 → Bool) → Bool) (G' : List ((Fin 4 → Bool) → Bool)) :
    (∀ g ∈ G', g = g2 ∨ g = g1) →
    ∃ c1 c2 : Bool, ∀ x, G'.any (fun g => g x) = (c1 && g1 x || c2 && g2 x) := by
  induction G' with
  | nil => intro _; exact ⟨false, false, fun x => rfl⟩
  | cons g G' ih =>
    intro hs
    obtain ⟨c1, c2, hc⟩ := ih (fun g' hg' => hs g' (List.mem_cons_of_mem _ hg'))
    rcases hs g (List.mem_cons_self) with hg | hg
    · refine ⟨c1, true, fun x => ?_⟩
      rw [List.any_cons, hc x, hg]
      cases c1 <;> cases c2 <;> cases (g2 x) <;> cases (g1 x) <;> rfl
    · refine ⟨true, c2, fun x => ?_⟩
      rw [List.any_cons, hc x, hg]
      cases c1 <;> cases c2 <;> cases (g2 x) <;> cases (g1 x) <;> rfl

private theorem m_cl_nil {a : (Fin 4 → Bool) → Bool} (ha : m_cl [] a) : m_hom a := by
  obtain ⟨h, hh, G', hs, he⟩ := ha
  have hG : G' = [] := List.eq_nil_iff_forall_not_mem.mpr (fun g hg => by simpa using hs g hg)
  subst hG
  have he' : ∀ x, a x = h x := fun x => by simpa using he x
  intro x y
  rw [he', he', he']
  exact hh x y

private theorem m_cl_one {g1 u : (Fin 4 → Bool) → Bool} (hu : m_cl [g1] u) :
    ∃ h, m_hom h ∧ ∃ c : Bool, ∀ x, u x = (h x || (c && g1 x)) := by
  obtain ⟨h, hh, G', hs, he⟩ := hu
  obtain ⟨c1, c2, hc⟩ := m_any2 g1 g1 G' (fun g hg => by simpa using hs g hg)
  refine ⟨h, hh, c1 || c2, fun x => ?_⟩
  rw [he x, hc x]
  cases c1 <;> cases c2 <;> cases (g1 x) <;> cases (h x) <;> rfl

private theorem m_pad {G : List ((Fin 4 → Bool) → Bool)} (hG : m_good G) :
    m_good ((fun _ => false) :: G) :=
  ⟨⟨fun _ => false, fun _ => false, m_cl_of_hom m_hom_false, m_cl_of_hom m_hom_false,
    fun _ => rfl⟩, hG⟩

private theorem one (g1 w : (Fin 4 → Bool) → Bool) (hG : m_good [g1])
    (hw : m_cl [g1] w) (hcyc : ∀ i j, w (m_pair i j) = adj i j) : False := by
  obtain ⟨⟨a, b, ha, hb, eg1⟩, -⟩ := hG
  have ha' := m_cl_nil ha
  have hb' := m_cl_nil hb
  obtain ⟨h, hh, c, ew⟩ := m_cl_one hw
  have H : ∀ i j, adj i j = ((h (m_e i) || h (m_e j)) ||
      c && ((a (m_e i) || a (m_e j)) && (b (m_e i) || b (m_e j)))) := by
    intro i j
    rw [← hcyc i j, ew, eg1, m_hom_pair hh, m_hom_pair ha', m_hom_pair hb']
  exact key _ _ _ _ _ _ _ _ _ _
    ((show adj 0 0 = false by decide).symm.trans (H 0 0))
    ((show adj 1 1 = false by decide).symm.trans (H 1 1))
    ((show adj 2 2 = false by decide).symm.trans (H 2 2))
    ((show adj 0 1 = true by decide).symm.trans (H 0 1))
    ((show adj 0 2 = true by decide).symm.trans (H 0 2))
    ((show adj 1 2 = true by decide).symm.trans (H 1 2))

private theorem final (G : List ((Fin 4 → Bool) → Bool)) (hG : m_good G)
    (hlen : G.length ≤ 1) (w : (Fin 4 → Bool) → Bool) (hw : m_cl G w)
    (hcyc : ∀ i j, w (m_pair i j) = adj i j) : False := by
  rcases G with _ | ⟨g1, _ | ⟨g0, t⟩⟩
  · exact one _ w (m_pad hG) (m_cl_mono _ hw) hcyc
  · exact one _ w hG hw hcyc
  · exact absurd hlen (by simp only [List.length_cons]; omega)

theorem main : ¬ ∃ C : PEqualNP.CircuitLowerBounds.Circuit, PEqualNP.MetaComplexity.Monotone2 C ∧ (∃ A : Finset ℕ, A.card ≤ 1 ∧ ∀ (j : ℕ) (g : PEqualNP.CircuitLowerBounds.Gate), C.gates[j]? = some g → g.op = PEqualNP.CircuitLowerBounds.GateOp.and → j ∈ A) ∧ ∀ x : Fin 4 → Bool, (C.eval (List.ofFn x) = true ↔ ∃ u v : Fin 4, (u.val, v.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3)] : List (ℕ × ℕ)) ∧ x u = true ∧ x v = true) := by
  rintro ⟨C, hmono, ⟨A, hAc, hA⟩, hC⟩
  obtain ⟨G, hG, hlen, hw⟩ := m_inv A C.gates
    (fun g hg => ⟨by have h1 := (hmono g hg).1; simpa using h1, (hmono g hg).2⟩) hA
  have hlen1 : G.length ≤ 1 :=
    le_trans hlen (le_trans (Finset.card_le_card (Finset.filter_subset _ _)) hAc)
  refine final G hG hlen1 (m_wf C.gates C.output) (hw C.output) (fun i j => ?_)
  exact Bool.eq_iff_iff.mpr ((hC (m_pair i j)).trans (tri i j))

end PEqualNP.Outside.L_meta_418

theorem PEqualNP.Outside.L_meta_418 : ¬ ∃ C : PEqualNP.CircuitLowerBounds.Circuit, PEqualNP.MetaComplexity.Monotone2 C ∧ (∃ A : Finset ℕ, A.card ≤ 1 ∧ ∀ (j : ℕ) (g : PEqualNP.CircuitLowerBounds.Gate), C.gates[j]? = some g → g.op = PEqualNP.CircuitLowerBounds.GateOp.and → j ∈ A) ∧ ∀ x : Fin 4 → Bool, (C.eval (List.ofFn x) = true ↔ ∃ u v : Fin 4, (u.val, v.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3)] : List (ℕ × ℕ)) ∧ x u = true ∧ x v = true) :=
  PEqualNP.Outside.L_meta_418.main
