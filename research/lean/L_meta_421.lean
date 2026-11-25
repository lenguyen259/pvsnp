import Mathlib
import PEqualNP.Defs

open PEqualNP.CircuitLowerBounds

namespace PEqualNP.Outside.L_meta_421

private def m_adj (i j : Fin 6) : Bool :=
  decide ((i.val, j.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)] : List (ℕ × ℕ)) ∨
    (j.val, i.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)] : List (ℕ × ℕ)))

private def m_e (i : Fin 6) : Fin 6 → Bool := fun k => decide (k = i)

private def m_pair (i j : Fin 6) : Fin 6 → Bool := fun k => m_e i k || m_e j k

private def m_trip (i j k : Fin 6) : Fin 6 → Bool := fun t => m_pair i j t || m_e k t

private def m_hom (a : (Fin 6 → Bool) → Bool) : Prop :=
  ∀ x y : Fin 6 → Bool, a (fun i => x i || y i) = (a x || a y)

private theorem m_hom_pair {a : (Fin 6 → Bool) → Bool} (ha : m_hom a) (i j : Fin 6) :
    a (m_pair i j) = (a (m_e i) || a (m_e j)) := ha _ _

private theorem m_hom_trip {a : (Fin 6 → Bool) → Bool} (ha : m_hom a) (i j k : Fin 6) :
    a (m_trip i j k) = ((a (m_e i) || a (m_e j)) || a (m_e k)) :=
  (ha (m_pair i j) (m_e k)).trans (by rw [m_hom_pair ha])

set_option maxRecDepth 100000 in
private theorem m_cyc : ∀ i j : Fin 6,
    ((∃ u v : Fin 6, (u.val, v.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)] : List (ℕ × ℕ)) ∧
      m_pair i j u = true ∧ m_pair i j v = true) ↔ m_adj i j = true) := by decide

set_option maxRecDepth 100000 in
private theorem m_ind : ¬ ∃ u v : Fin 6,
    (u.val, v.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)] : List (ℕ × ℕ)) ∧
      m_trip 3 4 5 u = true ∧ m_trip 3 4 5 v = true := by decide

private theorem m_adj_self : ∀ i : Fin 6, m_adj i i = false := by decide

private theorem m_hz : ∀ p r : Bool, false = ((p || p) || r) → p = false := by decide
private theorem m_o1 : ∀ p q : Bool, false = (p || q) → p = false := by decide
private theorem m_o2 : ∀ p q : Bool, false = (p || q) → q = false := by decide
private theorem m_a2 : ∀ p q : Bool, true = (p && q) → q = true := by decide
private theorem m_al : ∀ p q : Bool, (p && q) = true → p = true := by decide
private theorem m_ar : ∀ p q : Bool, (p && q) = true → q = true := by decide
private theorem m_or3a : ∀ x y z : Bool, (x || y) = true → ((x || y) || z) = true := by decide
private theorem m_or3b : ∀ x y z : Bool, (x || z) = true → ((x || y) || z) = true := by decide
private theorem m_or3c : ∀ x y z : Bool, (y || z) = true → ((x || y) || z) = true := by decide
private theorem m_z3 : ∀ x y z : Bool, ((x || y) || z) = false →
    x = false ∧ y = false ∧ z = false := by decide
private theorem m_cov : ∀ x y : Bool, (x || y) = true → y = false → x = true := by decide
private theorem m_tr : ∀ A B U V : Bool, ((U || A && B) && V) = false → A = true → B = true →
    V = false := by decide
private theorem m_dg : ∀ x y P vx vy : Bool, false = (((x || y) || P) && (vx || vy)) →
    vx = true → P = false ∧ y = false := by decide
private theorem m_ed : ∀ x y P V : Bool, true = (((x || y) || P) && V) → x = false → y = false →
    P = true := by decide

private theorem m_nb : ∀ a1 a2 a3 a4 b1 b2 b3 b4 : Bool,
    ((a1 || a1) && (b1 || b1)) = false → ((a2 || a2) && (b2 || b2)) = false →
    ((a3 || a3) && (b3 || b3)) = false → ((a4 || a4) && (b4 || b4)) = false →
    ((a1 || a3) && (b1 || b3)) = false → ((a1 || a4) && (b1 || b4)) = false →
    ((a2 || a3) && (b2 || b3)) = false →
    (((a1 || a2) && (b1 || b2)) && ((a3 || a4) && (b3 || b4))) = false := by
  decide

private theorem m_nbf (a b : Fin 6 → Bool)
    (hn : ∀ i j, m_adj i j = false → ((a i || a j) && (b i || b j)) = false) (p q r s : Fin 6)
    (h1 : m_adj p r = false) (h2 : m_adj p s = false) (h3 : m_adj q r = false) :
    (((a p || a q) && (b p || b q)) && ((a r || a s) && (b r || b s))) = false :=
  m_nb _ _ _ _ _ _ _ _ (hn p p (m_adj_self p)) (hn q q (m_adj_self q)) (hn r r (m_adj_self r))
    (hn s s (m_adj_self s)) (hn p r h1) (hn p s h2) (hn q r h3)

private theorem m_f3 : ∀ p1 p2 p3 q1 q2 q3 : Bool,
    (p1 && p2) = false → (p2 && p3) = false → (p3 && p1) = false →
    (q1 && q2) = false → (q2 && q3) = false → (q3 && q1) = false →
    true = (p1 || q1) → true = (p2 || q2) → true = (p3 || q3) → False := by
  decide

private theorem m_pd : ∀ a1 a2 a3 a4 b1 b2 b3 b4 : Bool,
    ((a1 || a1) && (b1 || b1)) = false → ((a2 || a2) && (b2 || b2)) = false →
    ((a1 || a2) && (b1 || b2)) = true → ((a1 || a3) && (b1 || b3)) = true →
    ((a2 || a4) && (b2 || b4)) = true → ((a1 || a4) && (b1 || b4)) = false →
    ((a2 || a3) && (b2 || b3)) = false → ((a3 || a4) && (b3 || b4)) = true := by
  decide

private theorem m_tri3 : ∀ a0 a1 a2 b0 b1 b2 : Bool,
    ((a0 || a0) && (b0 || b0)) = false → ((a1 || a1) && (b1 || b1)) = false →
    ((a2 || a2) && (b2 || b2)) = false → ((a0 || a1) && (b0 || b1)) = true →
    ((a0 || a2) && (b0 || b2)) = true → ((a1 || a2) && (b1 || b2)) = true → False := by
  decide

private theorem m_k1 (h a b c d : Fin 6 → Bool)
    (H : ∀ i j, m_adj i j =
      ((h i || h j) || ((a i || a j) && (b i || b j) || (c i || c j) && (d i || d j)))) : False := by
  have h0 : ∀ i, h i = false := fun i => m_hz _ _ ((m_adj_self i).symm.trans (H i i))
  have H1 : ∀ i j, m_adj i j =
      ((a i || a j) && (b i || b j) || (c i || c j) && (d i || d j)) := fun i j => by
    rw [H i j, h0 i, h0 j]; rfl
  have hP : ∀ i j, m_adj i j = false → ((a i || a j) && (b i || b j)) = false :=
    fun i j hij => m_o1 _ _ (hij.symm.trans (H1 i j))
  have hQ : ∀ i j, m_adj i j = false → ((c i || c j) && (d i || d j)) = false :=
    fun i j hij => m_o2 _ _ (hij.symm.trans (H1 i j))
  have E : ∀ i j, m_adj i j = true →
      true = ((a i || a j) && (b i || b j) || (c i || c j) && (d i || d j)) :=
    fun i j hij => hij.symm.trans (H1 i j)
  exact m_f3 _ _ _ _ _ _
    (m_nbf a b hP 3 0 4 1 (by decide) (by decide) (by decide))
    (m_nbf a b hP 4 1 5 2 (by decide) (by decide) (by decide))
    (m_nbf a b hP 5 2 3 0 (by decide) (by decide) (by decide))
    (m_nbf c d hQ 3 0 4 1 (by decide) (by decide) (by decide))
    (m_nbf c d hQ 4 1 5 2 (by decide) (by decide) (by decide))
    (m_nbf c d hQ 5 2 3 0 (by decide) (by decide) (by decide))
    (E 3 0 (by decide)) (E 4 1 (by decide)) (E 5 2 (by decide))

private theorem m_pend (u a b v : Fin 6 → Bool)
    (H : ∀ i j, m_adj i j = (((u i || u j) || (a i || a j) && (b i || b j)) && (v i || v j)))
    (p q p' q' : Fin 6) (e1 : m_adj p q = true) (e2 : m_adj p p' = true) (e3 : m_adj q q' = true)
    (n1 : m_adj p q' = false) (n2 : m_adj q p' = false) (hp : v p = true) (hq : v q = true) :
    ((a p' || a q') && (b p' || b q')) = true := by
  obtain ⟨dp, up⟩ := m_dg _ _ _ _ _ ((m_adj_self p).symm.trans (H p p)) hp
  obtain ⟨dq, uq⟩ := m_dg _ _ _ _ _ ((m_adj_self q).symm.trans (H q q)) hq
  obtain ⟨np, uq'⟩ := m_dg _ _ _ _ _ (n1.symm.trans (H p q')) hp
  obtain ⟨nq, up'⟩ := m_dg _ _ _ _ _ (n2.symm.trans (H q p')) hq
  exact m_pd _ _ _ _ _ _ _ _ dp dq (m_ed _ _ _ _ (e1.symm.trans (H p q)) up uq)
    (m_ed _ _ _ _ (e2.symm.trans (H p p')) up up') (m_ed _ _ _ _ (e3.symm.trans (H q q')) uq uq')
    np nq

private theorem m_k2 (h u a b v : Fin 6 → Bool)
    (H : ∀ i j, m_adj i j =
      ((h i || h j) || ((u i || u j) || (a i || a j) && (b i || b j)) && (v i || v j)))
    (T : (((h 3 || h 4) || h 5) || (((u 3 || u 4) || u 5) || ((a 3 || a 4) || a 5) &&
      ((b 3 || b 4) || b 5)) && ((v 3 || v 4) || v 5)) = false) : False := by
  have h0 : ∀ i, h i = false := fun i => m_hz _ _ ((m_adj_self i).symm.trans (H i i))
  have H1 : ∀ i j, m_adj i j =
      (((u i || u j) || (a i || a j) && (b i || b j)) && (v i || v j)) := fun i j => by
    rw [H i j, h0 i, h0 j]; rfl
  have T1 : ((((u 3 || u 4) || u 5) || ((a 3 || a 4) || a 5) && ((b 3 || b 4) || b 5)) &&
      ((v 3 || v 4) || v 5)) = false := by
    rw [h0 3, h0 4, h0 5] at T; exact T
  have hv : ∀ i j, m_adj i j = true → (v i || v j) = true :=
    fun i j hij => m_a2 _ _ (hij.symm.trans (H1 i j))
  have V0 : ((v 3 || v 4) || v 5) = false := by
    have c01 := hv 0 1 (by decide)
    have c02 := hv 0 2 (by decide)
    have c12 := hv 1 2 (by decide)
    cases hv0 : v 0 <;> cases hv1 : v 1
    · rw [hv0, hv1] at c01; exact absurd c01 (by decide)
    · rw [hv0] at c02
      have hv2 : v 2 = true := c02
      have P := m_pend u a b v H1 1 2 4 5 (by decide) (by decide) (by decide) (by decide)
        (by decide) hv1 hv2
      exact m_tr _ _ _ _ T1 (m_or3c _ _ _ (m_al _ _ P)) (m_or3c _ _ _ (m_ar _ _ P))
    · rw [hv1] at c12
      have hv2 : v 2 = true := c12
      have P := m_pend u a b v H1 0 2 3 5 (by decide) (by decide) (by decide) (by decide)
        (by decide) hv0 hv2
      exact m_tr _ _ _ _ T1 (m_or3b _ _ _ (m_al _ _ P)) (m_or3b _ _ _ (m_ar _ _ P))
    · have P := m_pend u a b v H1 0 1 3 4 (by decide) (by decide) (by decide) (by decide)
        (by decide) hv0 hv1
      exact m_tr _ _ _ _ T1 (m_or3a _ _ _ (m_al _ _ P)) (m_or3a _ _ _ (m_ar _ _ P))
  obtain ⟨z3, z4, z5⟩ := m_z3 _ _ _ V0
  have w0 : v 0 = true := m_cov _ _ (hv 0 3 (by decide)) z3
  have w1 : v 1 = true := m_cov _ _ (hv 1 4 (by decide)) z4
  have w2 : v 2 = true := m_cov _ _ (hv 2 5 (by decide)) z5
  obtain ⟨d0, y0⟩ := m_dg _ _ _ _ _ ((m_adj_self 0).symm.trans (H1 0 0)) w0
  obtain ⟨d1, y1⟩ := m_dg _ _ _ _ _ ((m_adj_self 1).symm.trans (H1 1 1)) w1
  obtain ⟨d2, y2⟩ := m_dg _ _ _ _ _ ((m_adj_self 2).symm.trans (H1 2 2)) w2
  exact m_tri3 _ _ _ _ _ _ d0 d1 d2
    (m_ed _ _ _ _ ((show m_adj 0 1 = true by decide).symm.trans (H1 0 1)) y0 y1)
    (m_ed _ _ _ _ ((show m_adj 0 2 = true by decide).symm.trans (H1 0 2)) y0 y2)
    (m_ed _ _ _ _ ((show m_adj 1 2 = true by decide).symm.trans (H1 1 2)) y1 y2)

private theorem m_core (h a b u v : Fin 6 → Bool) (c1 c2 cu cv : Bool)
    (H : ∀ i j, m_adj i j = ((h i || h j) || (c1 && ((a i || a j) && (b i || b j)) ||
      c2 && (((u i || u j) || cu && ((a i || a j) && (b i || b j))) &&
        ((v i || v j) || cv && ((a i || a j) && (b i || b j)))))))
    (T : (((h 3 || h 4) || h 5) || (c1 && (((a 3 || a 4) || a 5) && ((b 3 || b 4) || b 5)) ||
      c2 && ((((u 3 || u 4) || u 5) || cu && (((a 3 || a 4) || a 5) && ((b 3 || b 4) || b 5))) &&
        (((v 3 || v 4) || v 5) || cv && (((a 3 || a 4) || a 5) && ((b 3 || b 4) || b 5)))))) = false) :
    False := by
  rcases c1 <;> rcases c2 <;> rcases cu <;> rcases cv <;>
  first
    | (refine m_k1 h (fun _ => false) (fun _ => false) (fun _ => false) (fun _ => false) ?_; intro i j; rw [H i j];
        cases (h i || h j) <;> cases ((a i || a j) && (b i || b j)) <;> cases (u i || u j) <;>
          cases (v i || v j) <;> rfl)
    | (refine m_k1 h a b (fun _ => false) (fun _ => false) ?_; intro i j; rw [H i j];
        cases (h i || h j) <;> cases ((a i || a j) && (b i || b j)) <;> cases (u i || u j) <;>
          cases (v i || v j) <;> rfl)
    | (refine m_k1 h (fun _ => false) (fun _ => false) u v ?_; intro i j; rw [H i j];
        cases (h i || h j) <;> cases ((a i || a j) && (b i || b j)) <;> cases (u i || u j) <;>
          cases (v i || v j) <;> rfl)
    | (refine m_k1 h a b u v ?_; intro i j; rw [H i j];
        cases (h i || h j) <;> cases ((a i || a j) && (b i || b j)) <;> cases (u i || u j) <;>
          cases (v i || v j) <;> rfl)
    | (refine m_k2 h u a b v ?_ ?_;
        (intro i j; rw [H i j];
          cases (h i || h j) <;> cases ((a i || a j) && (b i || b j)) <;> cases (u i || u j) <;>
            cases (v i || v j) <;> rfl);
        (refine Eq.trans ?_ T;
          cases ((h 3 || h 4) || h 5) <;> cases (((a 3 || a 4) || a 5) && ((b 3 || b 4) || b 5)) <;>
            cases ((u 3 || u 4) || u 5) <;> cases ((v 3 || v 4) || v 5) <;> rfl))
    | (refine m_k2 h v a b u ?_ ?_;
        (intro i j; rw [H i j];
          cases (h i || h j) <;> cases ((a i || a j) && (b i || b j)) <;> cases (u i || u j) <;>
            cases (v i || v j) <;> rfl);
        (refine Eq.trans ?_ T;
          cases ((h 3 || h 4) || h 5) <;> cases (((a 3 || a 4) || a 5) && ((b 3 || b 4) || b 5)) <;>
            cases ((u 3 || u 4) || u 5) <;> cases ((v 3 || v 4) || v 5) <;> rfl))

private def m_cl (G : List ((Fin 6 → Bool) → Bool)) (w : (Fin 6 → Bool) → Bool) : Prop :=
  ∃ h, m_hom h ∧ ∃ G' : List ((Fin 6 → Bool) → Bool),
    (∀ g ∈ G', g ∈ G) ∧ ∀ x, w x = (h x || G'.any (fun g => g x))

private def m_good : List ((Fin 6 → Bool) → Bool) → Prop
  | [] => True
  | g :: G => (∃ u v, m_cl G u ∧ m_cl G v ∧ ∀ x, g x = (u x && v x)) ∧ m_good G

private theorem m_hom_false : m_hom (fun _ => false) := fun _ _ => rfl

private theorem m_hom_true : m_hom (fun _ => true) := fun _ _ => rfl

private theorem m_cl_of_hom {G : List ((Fin 6 → Bool) → Bool)} {h : (Fin 6 → Bool) → Bool}
    (hh : m_hom h) : m_cl G h :=
  ⟨h, hh, [], by simp, by simp⟩

private theorem m_cl_congr {G : List ((Fin 6 → Bool) → Bool)} {u w : (Fin 6 → Bool) → Bool}
    (hu : m_cl G u) (e : ∀ x, w x = u x) : m_cl G w := by
  obtain ⟨h, hh, G', hs, he⟩ := hu
  exact ⟨h, hh, G', hs, fun x => by rw [e x, he x]⟩

private theorem m_cl_mono {G : List ((Fin 6 → Bool) → Bool)} {w : (Fin 6 → Bool) → Bool}
    (g : (Fin 6 → Bool) → Bool) (hw : m_cl G w) : m_cl (g :: G) w := by
  obtain ⟨h, hh, G', hs, he⟩ := hw
  exact ⟨h, hh, G', fun g' hg' => List.mem_cons_of_mem _ (hs g' hg'), he⟩

private theorem m_cl_or {G : List ((Fin 6 → Bool) → Bool)} {u v : (Fin 6 → Bool) → Bool}
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

private theorem m_cl_new (G : List ((Fin 6 → Bool) → Bool)) (g : (Fin 6 → Bool) → Bool) :
    m_cl (g :: G) g :=
  ⟨fun _ => false, m_hom_false, [g], by simp, by simp⟩

private theorem m_gate_or (G : List ((Fin 6 → Bool) → Bool)) (f : ℕ → (Fin 6 → Bool) → Bool)
    (hw : ∀ k, m_cl G (f k)) (ins : List ℕ) (hl : ins.length ≤ 2) :
    m_cl G (fun x => GateOp.eval GateOp.or (ins.map fun i => f i x)) := by
  rcases ins with _ | ⟨i, _ | ⟨j, _ | ⟨k, t⟩⟩⟩
  · exact m_cl_congr (m_cl_of_hom m_hom_false) (fun x => by simp [GateOp.eval])
  · exact m_cl_congr (hw i) (fun x => by simp [GateOp.eval])
  · exact m_cl_congr (m_cl_or (hw i) (hw j)) (fun x => by simp [GateOp.eval])
  · exact absurd hl (by simp only [List.length_cons]; omega)

private theorem m_gate_and (G : List ((Fin 6 → Bool) → Bool)) (f : ℕ → (Fin 6 → Bool) → Bool)
    (hw : ∀ k, m_cl G (f k)) (ins : List ℕ) (hl : ins.length ≤ 2) :
    ∃ u v, m_cl G u ∧ m_cl G v ∧
      ∀ x, GateOp.eval GateOp.and (ins.map fun i => f i x) = (u x && v x) := by
  rcases ins with _ | ⟨i, _ | ⟨j, _ | ⟨k, t⟩⟩⟩
  · exact ⟨fun _ => true, fun _ => true, m_cl_of_hom m_hom_true, m_cl_of_hom m_hom_true,
      fun x => by simp [GateOp.eval]⟩
  · exact ⟨f i, f i, hw i, hw i, fun x => by simp [GateOp.eval]⟩
  · exact ⟨f i, f j, hw i, hw j, fun x => by simp [GateOp.eval]⟩
  · exact absurd hl (by simp only [List.length_cons]; omega)

private def m_W (gs : List Gate) (x : Fin 6 → Bool) : List Bool :=
  gs.foldl (fun w g => w ++ [g.op.eval (g.inputs.map fun i => w.getD i false)]) (List.ofFn x)

private def m_wf (gs : List Gate) (k : ℕ) : (Fin 6 → Bool) → Bool :=
  fun x => (m_W gs x).getD k false

private theorem m_fold_len (gs : List Gate) : ∀ w0 : List Bool,
    (gs.foldl (fun w g => w ++ [g.op.eval (g.inputs.map fun i => w.getD i false)]) w0).length
      = w0.length + gs.length := by
  induction gs with
  | nil => intro w0; simp
  | cons g gs ih => intro w0; rw [List.foldl_cons, ih]; simp; omega

private theorem m_W_len (gs : List Gate) (x : Fin 6 → Bool) :
    (m_W gs x).length = 6 + gs.length := by
  unfold m_W
  rw [m_fold_len]
  simp

private theorem m_W_snoc (gs : List Gate) (g : Gate) (x : Fin 6 → Bool) :
    m_W (gs ++ [g]) x
      = m_W gs x ++ [g.op.eval (g.inputs.map fun i => (m_W gs x).getD i false)] := by
  simp [m_W, List.foldl_append]

private theorem m_wf_snoc (gs : List Gate) (g : Gate) (k : ℕ) :
    m_wf (gs ++ [g]) k = if k = 6 + gs.length then
      (fun x => g.op.eval (g.inputs.map fun i => m_wf gs i x)) else m_wf gs k := by
  funext x
  have hl := m_W_len gs x
  by_cases hk : k = 6 + gs.length
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
      have h3 : ¬ (k - (6 + gs.length) = 0) := by omega
      have h4 : ¬ k < (m_W gs x).length := by rw [hl]; exact h2
      simp [h3, hl, h2]

private theorem m_base (k : ℕ) : m_hom (m_wf [] k) := by
  intro x y
  unfold m_wf m_W
  simp only [List.foldl_nil, List.getD_eq_getElem?_getD, List.getElem?_ofFn]
  by_cases hk : k < 6
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
        by_cases hk : k = 6 + gs.length
        · rw [if_pos hk]; exact m_cl_new _ _
        · rw [if_neg hk]; exact m_cl_mono _ (hw k)
    · refine ⟨G, hG, ?_, ?_⟩
      · refine le_trans hlen (Finset.card_le_card ?_)
        intro j hj
        simp only [Finset.mem_filter, List.length_append, List.length_cons, List.length_nil] at hj ⊢
        exact ⟨hj.1, by omega⟩
      · intro k
        rw [m_wf_snoc, hop]
        by_cases hk : k = 6 + gs.length
        · rw [if_pos hk]; exact m_gate_or G (m_wf gs) hw g.inputs hl
        · rw [if_neg hk]; exact hw k

private theorem m_any2 (g1 g2 : (Fin 6 → Bool) → Bool) (G' : List ((Fin 6 → Bool) → Bool)) :
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

private theorem m_cl_nil {a : (Fin 6 → Bool) → Bool} (ha : m_cl [] a) : m_hom a := by
  obtain ⟨h, hh, G', hs, he⟩ := ha
  have hG : G' = [] := List.eq_nil_iff_forall_not_mem.mpr (fun g hg => by simpa using hs g hg)
  subst hG
  have he' : ∀ x, a x = h x := fun x => by simpa using he x
  intro x y
  rw [he', he', he']
  exact hh x y

private theorem m_cl_one {g1 u : (Fin 6 → Bool) → Bool} (hu : m_cl [g1] u) :
    ∃ h, m_hom h ∧ ∃ c : Bool, ∀ x, u x = (h x || (c && g1 x)) := by
  obtain ⟨h, hh, G', hs, he⟩ := hu
  obtain ⟨c1, c2, hc⟩ := m_any2 g1 g1 G' (fun g hg => by simpa using hs g hg)
  refine ⟨h, hh, c1 || c2, fun x => ?_⟩
  rw [he x, hc x]
  cases c1 <;> cases c2 <;> cases (g1 x) <;> cases (h x) <;> rfl

private theorem m_cl_two {g1 g2 w : (Fin 6 → Bool) → Bool} (hw : m_cl [g2, g1] w) :
    ∃ h, m_hom h ∧ ∃ c1 c2 : Bool, ∀ x, w x = (h x || (c1 && g1 x || c2 && g2 x)) := by
  obtain ⟨h, hh, G', hs, he⟩ := hw
  obtain ⟨c1, c2, hc⟩ := m_any2 g1 g2 G' (fun g hg => by simpa using hs g hg)
  exact ⟨h, hh, c1, c2, fun x => by rw [he x, hc x]⟩

private theorem m_pad {G : List ((Fin 6 → Bool) → Bool)} (hG : m_good G) :
    m_good ((fun _ => false) :: G) :=
  ⟨⟨fun _ => false, fun _ => false, m_cl_of_hom m_hom_false, m_cl_of_hom m_hom_false,
    fun _ => rfl⟩, hG⟩

private theorem m_two (g1 g2 w : (Fin 6 → Bool) → Bool) (hG : m_good [g2, g1])
    (hw : m_cl [g2, g1] w) (hcyc : ∀ i j, w (m_pair i j) = m_adj i j)
    (htrip : w (m_trip 3 4 5) = false) : False := by
  obtain ⟨⟨u, v, hu, hv, eg2⟩, ⟨a, b, ha, hb, eg1⟩, -⟩ := hG
  have ha' := m_cl_nil ha
  have hb' := m_cl_nil hb
  obtain ⟨hu', hhu, cu, eu⟩ := m_cl_one hu
  obtain ⟨hv', hhv, cv, ev⟩ := m_cl_one hv
  obtain ⟨h, hh, c1, c2, ew⟩ := m_cl_two hw
  refine m_core (fun i => h (m_e i)) (fun i => a (m_e i)) (fun i => b (m_e i))
    (fun i => hu' (m_e i)) (fun i => hv' (m_e i)) c1 c2 cu cv (fun i j => ?_) ?_
  · rw [← hcyc i j, ew, eg2, eu, ev, eg1, m_hom_pair hh, m_hom_pair ha', m_hom_pair hb',
      m_hom_pair hhu, m_hom_pair hhv]
  · rw [← htrip, ew, eg2, eu, ev, eg1, m_hom_trip hh, m_hom_trip ha', m_hom_trip hb',
      m_hom_trip hhu, m_hom_trip hhv]

private theorem m_final (G : List ((Fin 6 → Bool) → Bool)) (hG : m_good G)
    (hlen : G.length ≤ 2) (w : (Fin 6 → Bool) → Bool) (hw : m_cl G w)
    (hcyc : ∀ i j, w (m_pair i j) = m_adj i j) (htrip : w (m_trip 3 4 5) = false) : False := by
  rcases G with _ | ⟨g2, _ | ⟨g1, _ | ⟨g0, t⟩⟩⟩
  · exact m_two _ _ w (m_pad (m_pad hG)) (m_cl_mono _ (m_cl_mono _ hw)) hcyc htrip
  · exact m_two _ _ w (m_pad hG) (m_cl_mono _ hw) hcyc htrip
  · exact m_two _ _ w hG hw hcyc htrip
  · exact absurd hlen (by simp only [List.length_cons]; omega)

theorem main : ¬ ∃ C : PEqualNP.CircuitLowerBounds.Circuit, PEqualNP.MetaComplexity.Monotone2 C ∧ (∃ A : Finset ℕ, A.card ≤ 2 ∧ ∀ (j : ℕ) (g : PEqualNP.CircuitLowerBounds.Gate), C.gates[j]? = some g → g.op = PEqualNP.CircuitLowerBounds.GateOp.and → j ∈ A) ∧ ∀ x : Fin 6 → Bool, (C.eval (List.ofFn x) = true ↔ ∃ u v : Fin 6, (u.val, v.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)] : List (ℕ × ℕ)) ∧ x u = true ∧ x v = true) := by
  rintro ⟨C, hmono, ⟨A, hAc, hA⟩, hC⟩
  obtain ⟨G, hG, hlen, hw⟩ := m_inv A C.gates
    (fun g hg => ⟨by have h1 := (hmono g hg).1; simpa using h1, (hmono g hg).2⟩) hA
  have hlen2 : G.length ≤ 2 :=
    le_trans hlen (le_trans (Finset.card_le_card (Finset.filter_subset _ _)) hAc)
  refine m_final G hG hlen2 (m_wf C.gates C.output) (hw C.output) (fun i j => ?_) ?_
  · exact Bool.eq_iff_iff.mpr ((hC (m_pair i j)).trans (m_cyc i j))
  · exact Bool.eq_false_iff.mpr (fun ht => m_ind ((hC (m_trip 3 4 5)).mp ht))

end PEqualNP.Outside.L_meta_421

theorem PEqualNP.Outside.L_meta_421 : ¬ ∃ C : PEqualNP.CircuitLowerBounds.Circuit, PEqualNP.MetaComplexity.Monotone2 C ∧ (∃ A : Finset ℕ, A.card ≤ 2 ∧ ∀ (j : ℕ) (g : PEqualNP.CircuitLowerBounds.Gate), C.gates[j]? = some g → g.op = PEqualNP.CircuitLowerBounds.GateOp.and → j ∈ A) ∧ ∀ x : Fin 6 → Bool, (C.eval (List.ofFn x) = true ↔ ∃ u v : Fin 6, (u.val, v.val) ∈ ([(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)] : List (ℕ × ℕ)) ∧ x u = true ∧ x v = true) :=
  PEqualNP.Outside.L_meta_421.main
