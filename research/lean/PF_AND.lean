import Mathlib
import PEqualNP.Defs

namespace PFAnd612
open SimpleGraph PEqualNP.CircuitLowerBounds PEqualNP.MetaComplexity
open scoped Classical

/-! Evaluation infrastructure -/

theorem ite_t {α : Sort*} {c : Prop} [Decidable c] (h : c) (a b : α) :
    (if c then a else b) = a := by simp [h]

theorem ite_f {α : Sort*} {c : Prop} [Decidable c] (h : ¬ c) (a b : α) :
    (if c then a else b) = b := by simp [h]

private def readGate (g : Gate) (w : ℕ → Bool) : Bool := g.op.eval (g.inputs.map w)
private def run (gs : List Gate) (input : List Bool) : List Bool :=
  gs.foldl (fun wires g => wires ++ [readGate g (fun j => wires.getD j false)]) input

private theorem run_append (gs : List Gate) (g : Gate) (s : List Bool) :
    run (gs ++ [g]) s = run gs s ++ [readGate g (fun j => (run gs s).getD j false)] := by
  simp [run,List.foldl_append]

private theorem run_len (gs : List Gate) (s : List Bool) :
    (run gs s).length=s.length+gs.length := by
  induction gs using List.reverseRecOn with
  | nil => simp [run]
  | append_singleton gs g ih => simp [run_append,ih,Nat.add_assoc]

private def val {n : ℕ} (gs : List Gate) (x : Fin n → Bool) (w : ℕ) : Bool :=
  (run gs (List.ofFn x)).getD w false

private theorem new_val {n : ℕ} (gs : List Gate) (g : Gate) (x : Fin n → Bool) :
    val (gs++[g]) x (n+gs.length) = readGate g (val gs x) := by
  have hl : (run gs (List.ofFn x)).length=n+gs.length := by simp [run_len]
  unfold val
  rw [run_append,←hl]
  simp

private theorem other_val {n : ℕ} (gs : List Gate) (g : Gate) (x : Fin n → Bool) {w : ℕ}
    (h : w ≠ n+gs.length) : val (gs++[g]) x w = val gs x w := by
  have hl : (run gs (List.ofFn x)).length=n+gs.length := by simp [run_len]
  unfold val
  rw [run_append]
  by_cases hw : w < (run gs (List.ofFn x)).length
  · exact List.getD_append _ _ _ _ hw
  · rw [List.getD_eq_default _ _ (by simp [hl]; omega),List.getD_eq_default _ _ (by omega)]

private theorem val_prefix {n : ℕ} (a b : List Gate) (x : Fin n → Bool) (w : ℕ)
    (hw : w<n+a.length) : val (a++b) x w=val a x w := by
  induction b using List.reverseRecOn with
  | nil => simp
  | append_singleton b g ih =>
    rw [←List.append_assoc,other_val _ _ _ (by simp; omega),ih]

/-- The value of wire `w` of `C` on input `x`. -/
def W {n : ℕ} (C : Circuit) (x : Fin n → Bool) (w : ℕ) : Bool :=
  (C.wires (List.ofFn x)).getD w false

/-- The value gate `k` reads from wire `i`: wires not yet built read `false`. -/
def rd {n : ℕ} (C : Circuit) (x : Fin n → Bool) (k i : ℕ) : Bool :=
  if i < n + k then W C x i else false

theorem W_eq_val {n : ℕ} (C : Circuit) (x : Fin n → Bool) (w : ℕ) :
    W C x w = val C.gates x w := rfl

theorem W_input {n : ℕ} (C : Circuit) (x : Fin n → Bool) {w : ℕ} (h : w < n) :
    W C x w = x ⟨w,h⟩ := by
  rw [W_eq_val]
  have key : ∀ gs : List Gate, val gs x w = x ⟨w,h⟩ := by
    intro gs
    induction gs using List.reverseRecOn with
    | nil =>
      unfold val run
      simp only [List.foldl_nil]
      rw [List.getD_eq_getElem _ _ (by simpa using h)]
      simp
    | append_singleton gs g ih =>
      rw [other_val _ _ _ (by omega), ih]
  exact key _

theorem W_dead {n : ℕ} (C : Circuit) (x : Fin n → Bool) {w : ℕ}
    (h : n + C.gates.length ≤ w) : W C x w = false := by
  rw [W_eq_val]
  unfold val
  exact List.getD_eq_default _ _ (by simp [run_len]; omega)

theorem W_gate {n : ℕ} (C : Circuit) (x : Fin n → Bool) {k : ℕ} {g : Gate}
    (hg : C.gates[k]? = some g) :
    W C x (n+k) = g.op.eval (g.inputs.map (rd C x k)) := by
  obtain ⟨hk, hgk⟩ := List.getElem?_eq_some_iff.mp hg
  have split : C.gates = (C.gates.take k ++ [g]) ++ C.gates.drop (k+1) := by
    rw [List.append_assoc]
    conv_lhs => rw [← List.take_append_drop k C.gates]
    congr 1
    rw [List.drop_eq_getElem_cons hk, hgk]
    rfl
  have hl : (C.gates.take k).length = k := by simp; omega
  rw [W_eq_val, split, val_prefix _ _ _ _ (by simp; omega)]
  have e := new_val (n:=n) (C.gates.take k) g x
  rw [hl] at e
  rw [e]
  unfold readGate
  congr 1
  apply List.map_congr_left
  intro i _
  unfold rd
  by_cases hi : i < n + k
  · simp only [hi, ↓reduceIte]
    rw [W_eq_val]
    have h1 := val_prefix (n:=n) (C.gates.take k ++ [g]) (C.gates.drop (k+1)) x i (by simp; omega)
    rw [← split] at h1
    rw [h1, val_prefix _ _ _ _ (by simp; omega)]
  · simp only [hi, ↓reduceIte]
    unfold val
    exact List.getD_eq_default _ _ (by simp [run_len]; omega)

theorem eval_eq_W {n : ℕ} (C : Circuit) (x : Fin n → Bool) :
    C.eval (List.ofFn x) = W C x C.output := rfl

/-! Monotonicity -/

theorem W_mono {n : ℕ} (C : Circuit) (hm : Monotone2 C) {x y : Fin n → Bool}
    (hxy : ∀ i, x i = true → y i = true) : ∀ w, W C x w = true → W C y w = true := by
  intro w
  induction w using Nat.strong_induction_on with
  | _ w ih =>
    intro hw
    by_cases h1 : w < n
    · rw [W_input _ _ h1] at hw ⊢
      exact hxy _ hw
    · obtain ⟨k, rfl⟩ : ∃ k, w = n + k := ⟨w - n, by omega⟩
      by_cases h2 : k < C.gates.length
      · have hg : C.gates[k]? = some C.gates[k] := List.getElem?_eq_getElem h2
        have hr : ∀ i, rd C x k i = true → rd C y k i = true := by
          intro i hi
          unfold rd at hi ⊢
          split_ifs at hi ⊢ with hlt
          exact ih i hlt hi
        rw [W_gate _ _ hg] at hw ⊢
        rcases (hm _ (List.getElem_mem h2)).1 with hop | hop
        · rw [Set.mem_singleton_iff.mp hop] at hw ⊢
          simp only [GateOp.eval, List.all_map, List.all_eq_true, Function.comp_apply,
            id_eq] at hw ⊢
          exact fun i hi => hr i (hw i hi)
        · rw [show C.gates[k].op = GateOp.or from hop] at hw ⊢
          simp only [GateOp.eval, List.any_map, List.any_eq_true, Function.comp_apply,
            id_eq] at hw ⊢
          obtain ⟨i, hi, hv⟩ := hw
          exact ⟨i, hi, hr i hv⟩
      · rw [W_dead _ _ (by omega)] at hw
        cases hw

/-! Restriction by a partial assignment, with constant propagation -/

/-- The input `x` with the coordinates fixed by `ρ` overwritten. -/
def fix {n : ℕ} (ρ : Fin n → Option Bool) (x : Fin n → Bool) : Fin n → Bool :=
  fun i => (ρ i).getD (x i)

/-- Wire `w` is constantly true under `ρ`. -/
def S1 {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) (w : ℕ) : Prop :=
  ∀ x, W C (fix ρ x) w = true

/-- Wire `w` is constantly false under `ρ`. -/
def S0 {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) (w : ℕ) : Prop :=
  ∀ x, W C (fix ρ x) w = false

/-- Gate `k` keeps its input `i` after propagation. -/
def keep {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) (k i : ℕ) : Prop :=
  i < n + k ∧ ¬ S0 C ρ i ∧ ¬ S1 C ρ i

/-- Gate `k` after propagation. -/
noncomputable def newGate {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) (k : ℕ) (g : Gate) :
    Gate :=
  if S0 C ρ (n+k) ∨ S1 C ρ (n+k) then ⟨.or, []⟩
  else ⟨if g.op = .and ∧ g.inputs.filter (fun i => decide (keep C ρ k i)) = g.inputs
      then .and else .or, g.inputs.filter (fun i => decide (keep C ρ k i))⟩

/-- The restricted circuit. -/
noncomputable def restricted {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) : Circuit :=
  ⟨C.gates.mapIdx (newGate C ρ), if S0 C ρ C.output then n + C.gates.length else C.output⟩

/-- An AND gate removed by the restriction. -/
def Killed {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) (j : ℕ) : Prop :=
  ∃ g, C.gates[j]? = some g ∧ g.op = .and ∧
    (S0 C ρ (n+j) ∨ S1 C ρ (n+j) ∨ ∃ i ∈ g.inputs, i < n+j ∧ S1 C ρ i)

theorem restricted_gate {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) (k : ℕ) (g' : Gate)
    (h : (restricted C ρ).gates[k]? = some g') :
    ∃ g, C.gates[k]? = some g ∧ g' = newGate C ρ k g := by
  change (C.gates.mapIdx (newGate C ρ))[k]? = some g' at h
  rw [List.getElem?_mapIdx] at h
  cases e : C.gates[k]? with
  | none => simp [e] at h
  | some g => exact ⟨g, rfl, by simpa [e] using h.symm⟩

theorem restricted_gate' {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) (k : ℕ) (g : Gate)
    (h : C.gates[k]? = some g) : (restricted C ρ).gates[k]? = some (newGate C ρ k g) := by
  change (C.gates.mapIdx (newGate C ρ))[k]? = _
  rw [List.getElem?_mapIdx, h]
  rfl

theorem restricted_len {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) :
    (restricted C ρ).gates.length = C.gates.length := by
  simp [restricted]

/-- Gate simplification: removed inputs carry the neutral value of the gate. -/
theorem gate_simplify (op : GateOp) (l : List ℕ) (P : ℕ → Prop) (r : ℕ → Bool)
    (hop : op = .and ∨ op = .or) (hlen : l.length ≤ 2)
    (removed : ∀ i ∈ l, ¬ P i → r i = decide (op = .and))
    (nonempty : op = .and → ∃ i ∈ l, P i) :
    GateOp.eval (if op = .and ∧ l.filter (fun i => decide (P i)) = l then .and else .or)
      ((l.filter (fun i => decide (P i))).map r) = op.eval (l.map r) := by
  rcases hop with rfl | rfl
  · by_cases hf : l.filter (fun i => decide (P i)) = l
    · simp only [hf, and_self, ↓reduceIte]
    · simp only [hf, and_false, ↓reduceIte, GateOp.eval]
      have hall : (l.map r).all id = ((l.filter (fun i => decide (P i))).map r).all id := by
        rw [Bool.eq_iff_iff]
        simp only [List.all_map, List.all_eq_true, Function.comp_apply, id_eq,
          List.mem_filter, decide_eq_true_eq]
        constructor
        · exact fun h i hi => h i hi.1
        · intro h i hi
          by_cases hp : P i
          · exact h i ⟨hi, hp⟩
          · simpa using removed i hi hp
      rw [hall]
      have hlt : (l.filter (fun i => decide (P i))).length < l.length := by
        apply lt_of_le_of_ne (List.length_filter_le _ _)
        intro he
        exact hf (List.filter_eq_self.mpr
          (List.length_filter_eq_length_iff.mp he))
      obtain ⟨i, hi, hp⟩ := nonempty rfl
      have hmem : i ∈ l.filter (fun i => decide (P i)) := List.mem_filter.mpr ⟨hi, by simpa using hp⟩
      generalize l.filter (fun i => decide (P i)) = m at hlt hmem
      rcases m with _ | ⟨a, _ | ⟨b, t⟩⟩
      · simp at hmem
      · simp
      · simp at hlt; omega
  · have hf : ¬ (GateOp.or = GateOp.and) := fun h => by cases h
    simp only [hf, false_and, ↓reduceIte, GateOp.eval]
    rw [Bool.eq_iff_iff]
    simp only [List.any_map, List.any_eq_true, Function.comp_apply, id_eq, List.mem_filter, decide_eq_true_eq]
    constructor
    · rintro ⟨i, ⟨hi, _⟩, hv⟩
      exact ⟨i, hi, hv⟩
    · rintro ⟨i, hi, hv⟩
      by_cases hp : P i
      · exact ⟨i, ⟨hi, hp⟩, hv⟩
      · have := removed i hi hp
        simp [hf] at this
        rw [this] at hv
        cases hv

theorem restricted_wire {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) (hm : Monotone2 C) :
    ∀ w, ¬ S0 C ρ w → ¬ S1 C ρ w → ∀ x, W (restricted C ρ) x w = W C (fix ρ x) w := by
  intro w
  induction w using Nat.strong_induction_on with
  | _ w ih =>
    intro h0 h1 x
    by_cases hn : w < n
    · rw [W_input _ _ hn, W_input _ _ hn]
      unfold fix
      cases e : ρ ⟨w, hn⟩ with
      | none => rfl
      | some b =>
        exfalso
        cases b
        · exact h0 (fun z => by rw [W_input _ _ hn]; simp [fix, e])
        · exact h1 (fun z => by rw [W_input _ _ hn]; simp [fix, e])
    · obtain ⟨k, rfl⟩ : ∃ k, w = n + k := ⟨w - n, by omega⟩
      by_cases hk : k < C.gates.length
      · have hg : C.gates[k]? = some C.gates[k] := List.getElem?_eq_getElem hk
        set g := C.gates[k]
        have hg' := restricted_gate' C ρ k g hg
        have hgood := hm g (List.getElem_mem hk)
        rw [W_gate _ _ hg', W_gate _ _ hg]
        have hng : newGate C ρ k g = ⟨if g.op = .and ∧ g.inputs.filter
            (fun i => decide (keep C ρ k i)) = g.inputs then .and else .or,
            g.inputs.filter (fun i => decide (keep C ρ k i))⟩ := by
          unfold newGate
          rw [ite_f (by tauto)]
        rw [hng]
        dsimp only
        have hmap : (g.inputs.filter (fun i => decide (keep C ρ k i))).map
            (rd (restricted C ρ) x k) = (g.inputs.filter (fun i => decide (keep C ρ k i))).map
            (rd C (fix ρ x) k) := by
          apply List.map_congr_left
          intro i hi
          obtain ⟨_, hk'⟩ := List.mem_filter.mp hi
          obtain ⟨hlt, hi0, hi1⟩ := of_decide_eq_true hk'
          unfold rd
          simp only [hlt, ↓reduceIte]
          exact ih i hlt hi0 hi1 x
        rw [hmap]
        have hop : g.op = .and ∨ g.op = .or := by
          rcases hgood.1 with h | h
          · exact Or.inl h
          · exact Or.inr h
        apply gate_simplify g.op g.inputs (keep C ρ k) _ hop hgood.2
        · intro i hi hnk
          unfold keep at hnk
          rcases hop with hop | hop
          · simp only [hop, decide_true]
            by_cases hlt : i < n + k
            · by_cases hi0 : S0 C ρ i
              · exfalso
                apply h0
                intro z
                rw [W_gate _ _ hg, hop]
                simp only [GateOp.eval, List.all_map, List.all_eq_false, Function.comp_apply,
                  id_eq, Bool.not_eq_true]
                exact ⟨i, hi, by simp [rd, hlt, hi0 z]⟩
              · have hi1 : S1 C ρ i := by tauto
                simp [rd, hlt, hi1 x]
            · exfalso
              apply h0
              intro z
              rw [W_gate _ _ hg, hop]
              simp only [GateOp.eval, List.all_map, List.all_eq_false, Function.comp_apply,
                id_eq, Bool.not_eq_true]
              exact ⟨i, hi, by simp [rd, hlt]⟩
          · have hne : ¬ (GateOp.or = GateOp.and) := fun h => by cases h
            simp only [hop, hne, decide_false]
            by_cases hlt : i < n + k
            · by_cases hi1 : S1 C ρ i
              · exfalso
                apply h1
                intro z
                rw [W_gate _ _ hg, hop]
                simp only [GateOp.eval, List.any_map, List.any_eq_true, Function.comp_apply,
                  id_eq]
                exact ⟨i, hi, by simp [rd, hlt, hi1 z]⟩
              · have hi0 : S0 C ρ i := by tauto
                simp [rd, hlt, hi0 x]
            · simp [rd, hlt]
        · intro hop
          by_contra hno
          push Not at hno
          apply h1
          intro z
          rw [W_gate _ _ hg, hop]
          simp only [GateOp.eval, List.all_map, List.all_eq_true, Function.comp_apply, id_eq]
          intro i hi
          have hnk := hno i hi
          unfold keep at hnk
          by_cases hlt : i < n + k
          · by_cases hi0 : S0 C ρ i
            · exfalso
              apply h0
              intro z'
              rw [W_gate _ _ hg, hop]
              simp only [GateOp.eval, List.all_map, List.all_eq_false, Function.comp_apply,
                id_eq, Bool.not_eq_true]
              exact ⟨i, hi, by simp [rd, hlt, hi0 z']⟩
            · have hi1 : S1 C ρ i := by tauto
              simp [rd, hlt, hi1 z]
          · exfalso
            apply h0
            intro z'
            rw [W_gate _ _ hg, hop]
            simp only [GateOp.eval, List.all_map, List.all_eq_false, Function.comp_apply,
              id_eq, Bool.not_eq_true]
            exact ⟨i, hi, by simp [rd, hlt]⟩
      · rw [W_dead _ _ (by rw [restricted_len]; omega), W_dead _ _ (by omega)]

theorem restrict {n : ℕ} (C : Circuit) (ρ : Fin n → Option Bool) (A S : Finset ℕ)
    (hm : Monotone2 C) (cover : ∀ j g, C.gates[j]? = some g → g.op = .and → j ∈ A)
    (killed : ∀ j ∈ S, Killed C ρ j) (notOne : ¬ S1 C ρ C.output) :
    ∃ (C' : Circuit) (B : Finset ℕ), Monotone2 C' ∧ B.card + S.card = A.card ∧
      (∀ x, C'.eval (List.ofFn x) = C.eval (List.ofFn (fix ρ x))) ∧
      ∀ j g, C'.gates[j]? = some g → g.op = .and → j ∈ B := by
  have sub : S ⊆ A := by
    intro j hj
    obtain ⟨g, hg, hop, _⟩ := killed j hj
    exact cover j g hg hop
  refine ⟨restricted C ρ, A \ S, ?_, Finset.card_sdiff_add_card_eq_card sub, ?_, ?_⟩
  · intro g' hg'
    obtain ⟨k, hk⟩ := List.mem_iff_getElem?.mp hg'
    obtain ⟨g, hg, rfl⟩ := restricted_gate C ρ k g' hk
    have hgood := hm g (List.mem_of_getElem? hg)
    unfold newGate
    split_ifs with h1 h2
    · simp
    · refine ⟨by simp, ?_⟩
      exact le_trans (List.length_filter_le _ _) hgood.2
    · refine ⟨by simp, ?_⟩
      exact le_trans (List.length_filter_le _ _) hgood.2
  · intro x
    rw [eval_eq_W, eval_eq_W]
    by_cases h0 : S0 C ρ C.output
    · have e : (restricted C ρ).output = n + C.gates.length := by simp [restricted, h0]
      rw [e, W_dead _ _ (by rw [restricted_len]), h0 x]
    · have e : (restricted C ρ).output = C.output := by simp [restricted, h0]
      rw [e]
      exact restricted_wire C ρ hm _ h0 notOne x
  · intro j g' hg' hop
    obtain ⟨g, hg, rfl⟩ := restricted_gate C ρ j g' hg'
    unfold newGate at hop
    by_cases h1 : S0 C ρ (n+j) ∨ S1 C ρ (n+j)
    · rw [ite_t h1] at hop
      cases hop
    rw [ite_f h1] at hop
    dsimp only at hop
    by_cases h2 : g.op = .and ∧ g.inputs.filter (fun i => decide (keep C ρ j i)) = g.inputs
    · refine Finset.mem_sdiff.mpr ⟨cover j g hg h2.1, ?_⟩
      intro hj
      obtain ⟨g2, hg2, _, hk⟩ := killed j hj
      obtain rfl : g2 = g := Option.some.inj (hg2.symm.trans hg)
      rcases hk with hk | hk | ⟨i, hi, hlt, hi1⟩
      · exact h1 (Or.inl hk)
      · exact h1 (Or.inr hk)
      · have hall := List.filter_eq_self.mp h2.2 i hi
        exact (of_decide_eq_true hall).2.2 hi1
    · rw [ite_f h2] at hop
      cases hop

/-! Isolation and forcing -/

theorem isolate {n : ℕ} (D : Circuit) (a : Fin n) (T : ℕ → Prop)
    (hin : ∀ w (_ : w < n), ¬ T w → w ≠ a.val)
    (hg : ∀ k g, D.gates[k]? = some g → ¬ T (n+k) → ∀ i ∈ g.inputs, i < n+k → ¬ T i) :
    ∀ w, ¬ T w → ∀ z b, W D (Function.update z a b) w = W D z w := by
  intro w
  induction w using Nat.strong_induction_on with
  | _ w ih =>
    intro hw z b
    by_cases hn : w < n
    · rw [W_input _ _ hn, W_input _ _ hn]
      exact Function.update_of_ne (fun e => hin w hn hw (congrArg Fin.val e)) _ _
    · obtain ⟨k, rfl⟩ : ∃ k, w = n + k := ⟨w - n, by omega⟩
      by_cases hk : k < D.gates.length
      · have hg' : D.gates[k]? = some D.gates[k] := List.getElem?_eq_getElem hk
        rw [W_gate _ _ hg', W_gate _ _ hg']
        congr 1
        apply List.map_congr_left
        intro i hi
        unfold rd
        by_cases hlt : i < n + k
        · simp only [hlt, ↓reduceIte]
          exact ih i hlt (hg k _ hg' hw i hi hlt) z b
        · simp only [hlt, ↓reduceIte]
      · rw [W_dead _ _ (by omega), W_dead _ _ (by omega)]

/-- The constant gate with value `e`. -/
def constGate (e : Bool) : Gate := if e then ⟨.and, []⟩ else ⟨.or, []⟩

theorem constGate_inputs (e : Bool) : (constGate e).inputs = [] := by
  cases e <;> rfl

theorem constGate_eval (e : Bool) (r : ℕ → Bool) :
    (constGate e).op.eval ((constGate e).inputs.map r) = e := by
  cases e <;> rfl

/-- `C` with gate `j` replaced by the constant `e`. -/
def force (C : Circuit) (j : ℕ) (e : Bool) : Circuit := ⟨C.gates.set j (constGate e), C.output⟩

theorem force_len (C : Circuit) (j : ℕ) (e : Bool) :
    (force C j e).gates.length = C.gates.length := by
  simp [force]

theorem force_gate_ne (C : Circuit) {j k : ℕ} (e : Bool) (h : k ≠ j) :
    (force C j e).gates[k]? = C.gates[k]? := by
  simp [force, Ne.symm h]

theorem force_gate_eq (C : Circuit) {j : ℕ} (e : Bool) (h : j < C.gates.length) :
    (force C j e).gates[j]? = some (constGate e) := by
  simp [force, h]

theorem force_agree {n : ℕ} (C : Circuit) (j : ℕ) (e : Bool) (x : Fin n → Bool)
    (hj : j < C.gates.length) :
    ∀ w, (w < n + j ∨ W C x (n+j) = e) → W (force C j e) x w = W C x w := by
  intro w
  induction w using Nat.strong_induction_on with
  | _ w ih =>
    intro hw
    by_cases hn : w < n
    · rw [W_input _ _ hn, W_input _ _ hn]
    · obtain ⟨k, rfl⟩ : ∃ k, w = n + k := ⟨w - n, by omega⟩
      by_cases hk : k < C.gates.length
      · by_cases hkj : k = j
        · subst hkj
          rcases hw with hw | hw
          · omega
          rw [W_gate _ _ (force_gate_eq C e hk), constGate_eval, hw]
        · have hg' : C.gates[k]? = some C.gates[k] := List.getElem?_eq_getElem hk
          have hf : (force C j e).gates[k]? = some C.gates[k] := (force_gate_ne C e hkj).trans hg'
          rw [W_gate _ _ hf, W_gate _ _ hg']
          congr 1
          apply List.map_congr_left
          intro i _
          unfold rd
          by_cases hlt : i < n + k
          · simp only [hlt, ↓reduceIte]
            apply ih i hlt
            rcases hw with hw | hw
            · left; omega
            · right; exact hw
          · simp only [hlt, ↓reduceIte]
      · rw [W_dead _ _ (by rw [force_len]; omega), W_dead _ _ (by omega)]

/-! Unit vectors, hits and exits -/

/-- The input with exactly coordinate `v` true. -/
def one {n : ℕ} (v : Fin n) : Fin n → Bool := fun i => decide (i = v)

/-- Gate `k` is an AND gate that becomes constant or a copy under `x_v := 1`. -/
def Hit {n : ℕ} (C : Circuit) (v : Fin n) (k : ℕ) : Prop :=
  ∃ g, C.gates[k]? = some g ∧ g.op = .and ∧
    (W C (one v) (n+k) = true ∨ ∃ i ∈ g.inputs, i < n+k ∧ W C (one v) i = true)

theorem one_self {n : ℕ} (v : Fin n) : one v v = true := by simp [one]

theorem W_one_self {n : ℕ} (C : Circuit) (v : Fin n) : W C (one v) v.val = true := by
  rw [W_input _ _ v.isLt]
  exact one_self v

theorem or_gate_true {n : ℕ} (C : Circuit) (x : Fin n → Bool) {k : ℕ} {g : Gate}
    (hg : C.gates[k]? = some g) (hop : g.op = .or) {i : ℕ} (hi : i ∈ g.inputs)
    (hlt : i < n + k) (hv : W C x i = true) : W C x (n+k) = true := by
  rw [W_gate _ _ hg, hop]
  simp only [GateOp.eval, List.any_map, List.any_eq_true, Function.comp_apply, id_eq]
  exact ⟨i, hi, by simp [rd, hlt, hv]⟩

theorem and_gate_true {n : ℕ} (C : Circuit) (x : Fin n → Bool) {k : ℕ} {g : Gate}
    (hg : C.gates[k]? = some g) (hop : g.op = .and) (h : W C x (n+k) = true) :
    ∀ i ∈ g.inputs, i < n + k ∧ W C x i = true := by
  rw [W_gate _ _ hg, hop] at h
  simp only [GateOp.eval, List.all_map, List.all_eq_true, Function.comp_apply, id_eq] at h
  intro i hi
  have := h i hi
  unfold rd at this
  by_cases hlt : i < n + k
  · simp only [hlt, ↓reduceIte] at this
    exact ⟨hlt, this⟩
  · simp [hlt] at this

theorem and_gate_false {n : ℕ} (C : Circuit) (x : Fin n → Bool) {k : ℕ} {g : Gate}
    (hg : C.gates[k]? = some g) (hop : g.op = .and) (h : W C x (n+k) = false) :
    ∃ i ∈ g.inputs, rd C x k i = false := by
  rw [W_gate _ _ hg, hop] at h
  simp only [GateOp.eval, List.all_map, List.all_eq_false, Function.comp_apply, id_eq,
    Bool.not_eq_true] at h
  exact h

theorem exit_exists {n : ℕ} (C : Circuit) (hm : Monotone2 C) (v : Fin n) (x : Fin n → Bool)
    (hx : W C (Function.update x v true) C.output ≠ W C x C.output)
    (hout : W C (one v) C.output = false) :
    ∃ k g, C.gates[k]? = some g ∧ g.op = .and ∧ W C (one v) (n+k) = false ∧
      ∃ i ∈ g.inputs, i < n+k ∧ W C (one v) i = true := by
  by_contra hno
  apply hx
  apply isolate C v (fun w => W C (one v) w = true)
  · intro w hw hT he
    subst he
    exact hT (W_one_self C v)
  · intro k g hg hT i hi hlt hTi
    rcases (hm g (List.mem_of_getElem? hg)).1 with hop | hop
    · exact hno ⟨k, g, hg, hop, by simpa using hT, i, hi, hlt, hTi⟩
    · exact hT (or_gate_true C _ hg hop hi hlt hTi)
  · simp [hout]

theorem iso_unique {n : ℕ} (C : Circuit) (hm : Monotone2 C) (a : Fin n) (E : ℕ)
    (uniq : ∀ k, Hit C a k → k = E) (e : Bool) :
    ∀ w, W C (one a) w ≠ true → ∀ z b,
      W (force C E e) (Function.update z a b) w = W (force C E e) z w := by
  apply isolate (force C E e) a (fun w => W C (one a) w = true)
  · intro w hw hT he
    subst he
    exact hT (W_one_self C a)
  · intro k g hg hT i hi hlt hTi
    by_cases hk : k = E
    · subst hk
      have hlen : k < C.gates.length := by
        have := (List.getElem?_eq_some_iff.mp hg).1
        rwa [force_len] at this
      rw [force_gate_eq C e hlen] at hg
      obtain rfl := Option.some.inj hg
      rw [constGate_inputs] at hi
      cases hi
    · rw [force_gate_ne C e hk] at hg
      rcases (hm g (List.mem_of_getElem? hg)).1 with hop | hop
      · exact hk (uniq k ⟨g, hg, hop, Or.inr ⟨i, hi, hlt, hTi⟩⟩)
      · exact hT (or_gate_true C _ hg hop hi hlt hTi)

/-! The edge function -/

/-- `C` computes the edge function of `G`. -/
def detects {n : ℕ} (G : SimpleGraph (Fin n)) (C : Circuit) : Prop :=
  ∀ x : Fin n → Bool, C.eval (List.ofFn x) = true ↔ ∃ u v, G.Adj u v ∧ x u = true ∧ x v = true

theorem single_false {n : ℕ} {G : SimpleGraph (Fin n)} {C : Circuit} (h : detects G C)
    (z : Fin n → Bool) (hz : ∀ i j, z i = true → z j = true → i = j) :
    W C z C.output = false := by
  rw [← eval_eq_W, Bool.eq_false_iff]
  intro ht
  obtain ⟨u, v, huv, hu, hv⟩ := (h z).mp ht
  exact huv.ne (hz u v hu hv)

theorem one_false {n : ℕ} {G : SimpleGraph (Fin n)} {C : Circuit} (h : detects G C)
    (v : Fin n) : W C (one v) C.output = false := by
  apply single_false h
  intro i j hi hj
  simp only [one, decide_eq_true_eq] at hi hj
  rw [hi, hj]

theorem pair_true {n : ℕ} {G : SimpleGraph (Fin n)} {C : Circuit} (h : detects G C)
    {a b : Fin n} (hab : G.Adj a b) (z : Fin n → Bool) (ha : z a = true) (hb : z b = true) :
    W C z C.output = true := by
  rw [← eval_eq_W]
  exact (h z).mpr ⟨a, b, hab, ha, hb⟩

theorem le_update {n : ℕ} (x : Fin n → Bool) (v : Fin n) :
    ∀ i, x i = true → Function.update x v true i = true := by
  intro i hi
  by_cases e : i = v
  · subst e; simp
  · rw [Function.update_of_ne e]; exact hi

theorem one_le {n : ℕ} (v : Fin n) (z : Fin n → Bool) (hz : z v = true) :
    ∀ i, one v i = true → z i = true := by
  intro i hi
  simp only [one, decide_eq_true_eq] at hi
  subst hi
  exact hz

/-! Step 2 of Lemma AND-core: the neighbours of `v` enter the exit of `v` -/

theorem stepB {n : ℕ} {G : SimpleGraph (Fin n)} {C : Circuit} (hm : Monotone2 C)
    (h : detects G C) {v a : Fin n} (hva : G.Adj v a) {E : ℕ} {g : Gate}
    (hg : C.gates[E]? = some g) (hop : g.op = .and) (hE : W C (one v) (n+E) = false)
    (uniq : ∀ k, Hit C v k → k = E) :
    W C (one a) (n+E) = false ∧
      ∃ t ∈ g.inputs, t < n+E ∧ W C (one v) t = false ∧ W C (one a) t = true := by
  have hlen : E < C.gates.length := (List.getElem?_eq_some_iff.mp hg).1
  let x0 := one a
  let x1 := Function.update (one a) v true
  have f0 : W C x0 C.output = false := one_false h a
  have f1 : W C x1 C.output = true := by
    apply pair_true h hva
    · simp [x1]
    · simp only [x1]
      rw [Function.update_of_ne hva.ne.symm]
      exact one_self a
  have hout : W C (one v) C.output ≠ true := by simp [one_false h v]
  have iso := fun e => iso_unique C hm v E uniq e
  have key : ∀ e x, W C x (n+E) = e →
      W C x C.output = W (force C E e) x C.output := fun e x hx =>
    (force_agree C E e x hlen C.output (Or.inr hx)).symm
  have c0 : W C x0 (n+E) = false := by
    rw [Bool.eq_false_iff]
    intro ht
    have ht1 : W C x1 (n+E) = true := W_mono C hm (le_update x0 v) _ ht
    have e0 := key true x0 ht
    have e1 := key true x1 ht1
    rw [iso true C.output hout x0 true] at e1
    rw [f0] at e0
    rw [f1, ← e0] at e1
    cases e1
  have c1 : W C x1 (n+E) = true := by
    by_contra hne
    have hne' : W C x1 (n+E) = false := by simpa using hne
    have e0 := key false x0 c0
    have e1 := key false x1 hne'
    rw [iso false C.output hout x0 true] at e1
    rw [f0] at e0
    rw [f1, ← e0] at e1
    cases e1
  refine ⟨c0, ?_⟩
  obtain ⟨t, ht, hrd⟩ := and_gate_false C (one v) hg hop hE
  obtain ⟨htlt, ht1⟩ := and_gate_true C x1 hg hop c1 t ht
  have htv : W C (one v) t = false := by simpa [rd, htlt] using hrd
  refine ⟨t, ht, htlt, htv, ?_⟩
  have a1 := force_agree C E false x0 hlen t (Or.inl htlt)
  have a2 := force_agree C E false x1 hlen t (Or.inl htlt)
  have i1 := iso false t (by simp [htv]) x0 true
  change W C x0 t = true
  rw [← a1, ← i1]
  change W (force C E false) x1 t = true
  rw [a2, ht1]

/-! Step 5 of Lemma AND-core: two vertices entering one exit on one side are twins -/

theorem and_two {n : ℕ} (C : Circuit) (z : Fin n → Bool) {E : ℕ} {g : Gate}
    (hg : C.gates[E]? = some g) (hop : g.op = .and) {p t : ℕ}
    (hin : ∀ i ∈ g.inputs, i = p ∨ i = t) (hp : p ∈ g.inputs) (hpE : p < n + E)
    (htE : t < n + E) (ht : W C z t = true) : W C z (n+E) = W C z p := by
  rw [W_gate _ _ hg, hop]
  simp only [GateOp.eval, List.all_map]
  rw [Bool.eq_iff_iff]
  simp only [List.all_eq_true, Function.comp_apply, id_eq]
  constructor
  · intro hall
    simpa [rd, hpE] using hall p hp
  · intro hpv i hi
    rcases hin i hi with rfl | rfl
    · simpa [rd, hpE] using hpv
    · simpa [rd, htE] using ht

theorem twin {n : ℕ} (C : Circuit) (hm : Monotone2 C) (a1 a2 : Fin n) {E : ℕ} {g : Gate}
    (hg : C.gates[E]? = some g) (hop : g.op = .and) {p t : ℕ}
    (hin : ∀ i ∈ g.inputs, i = p ∨ i = t) (hp : p ∈ g.inputs) (hpE : p < n + E)
    (htE : t < n + E) (ht1 : W C (one a1) t = true) (ht2 : W C (one a2) t = true)
    (hp1 : W C (one a1) p = false) (hp2 : W C (one a2) p = false)
    (u1 : ∀ k, Hit C a1 k → k = E) (u2 : ∀ k, Hit C a2 k → k = E)
    (ho1 : W C (one a1) C.output = false) (ho2 : W C (one a2) C.output = false)
    (y : Fin n → Bool) :
    W C (Function.update y a1 true) C.output = W C (Function.update y a2 true) C.output ∧
      W C (Function.update y a1 true) C.output =
        W C (Function.update (Function.update y a1 true) a2 true) C.output := by
  have hlen : E < C.gates.length := (List.getElem?_eq_some_iff.mp hg).1
  set e := W C y p
  set D := force C E e
  have iso1 := iso_unique C hm a1 E u1 e
  have iso2 := iso_unique C hm a2 E u2 e
  have pD : ∀ z, W D z p = W C z p := fun z => force_agree C E e z hlen p (Or.inl hpE)
  have np1 : W C (one a1) p ≠ true := by simp [hp1]
  have np2 : W C (one a2) p ≠ true := by simp [hp2]
  have no1 : W C (one a1) C.output ≠ true := by simp [ho1]
  have no2 : W C (one a2) C.output ≠ true := by simp [ho2]
  set y1 := Function.update y a1 true
  set y2 := Function.update y a2 true
  set y12 := Function.update y1 a2 true
  have pv1 : W C y1 p = e := by rw [← pD, iso1 p np1, pD]
  have pv2 : W C y2 p = e := by rw [← pD, iso2 p np2, pD]
  have pv12 : W C y12 p = e := by rw [← pD, iso2 p np2, iso1 p np1, pD]
  have tv : ∀ z : Fin n → Bool, (z a1 = true ∨ z a2 = true) → W C z t = true := by
    intro z hz
    rcases hz with hz | hz
    · exact W_mono C hm (one_le a1 z hz) t ht1
    · exact W_mono C hm (one_le a2 z hz) t ht2
  have Ev : ∀ z : Fin n → Bool, (z a1 = true ∨ z a2 = true) → W C z p = e →
      W C z C.output = W D z C.output := by
    intro z hz hpz
    have hE : W C z (n+E) = e := by
      rw [and_two C z hg hop hin hp hpE htE (tv z hz), hpz]
    exact (force_agree C E e z hlen C.output (Or.inr hE)).symm
  have hy1 : y1 a1 = true := by simp [y1]
  have hy2 : y2 a2 = true := by simp [y2]
  have hy12 : y12 a2 = true := by simp [y12]
  rw [Ev y1 (Or.inl hy1) pv1, Ev y2 (Or.inr hy2) pv2, Ev y12 (Or.inr hy12) pv12]
  simp only [y12, y1, y2]
  refine ⟨?_, ?_⟩
  · rw [iso1 C.output no1 y true, iso2 C.output no2 y true]
  · rw [iso2 C.output no2 (Function.update y a1 true) true]

/-! Graph facts -/

/-- Every vertex set `S` spans at most `|S|` edges (pseudoforest). -/
def sparse {n : ℕ} (G : SimpleGraph (Fin n)) : Prop :=
  ∀ S : Finset (Fin n), {e : Sym2 (Fin n) | e ∈ G.edgeSet ∧ ∀ v ∈ e, v ∈ S}.ncard ≤ S.card

/-- No cycle of length four. -/
def noFour {n : ℕ} (G : SimpleGraph (Fin n)) : Prop :=
  ∀ v (c : G.Walk v v), c.IsCycle → c.length ≠ 4

theorem sparse_subgraph {n : ℕ} {H G : SimpleGraph (Fin n)} (h : H ≤ G) (hG : sparse G) :
    sparse H := by
  intro S
  apply le_trans _ (hG S)
  refine Set.ncard_le_ncard ?_ (Set.toFinite _)
  intro e he
  exact ⟨SimpleGraph.edgeSet_mono h he.1, he.2⟩

theorem noFour_subgraph {n : ℕ} {H G : SimpleGraph (Fin n)} (h : H ≤ G) (hG : noFour G) :
    noFour H := by
  intro v c hc
  simpa only [Walk.length_mapLe] using hG v (c.mapLe h) (hc.mapLe h)

theorem count_eq {n : ℕ} (G : SimpleGraph (Fin n)) : G.edgeSet.ncard = G.edgeFinset.card := by
  exact Set.ncard_eq_toFinset_card' _

theorem support_count {n : ℕ} (G : SimpleGraph (Fin n)) (hs : sparse G) :
    G.edgeFinset.card ≤ G.support.toFinset.card := by
  rw [← count_eq]
  let S := G.support.toFinset
  apply le_trans _ (hs S)
  refine Set.ncard_le_ncard ?_ (Set.toFinite _)
  intro e he
  refine ⟨he, ?_⟩
  induction e using Sym2.inductionOn with
  | _ a b =>
    have hab : G.Adj a b := he
    intro v hv
    rcases Sym2.mem_iff.mp hv with rfl | rfl
    · exact Set.mem_toFinset.mpr (G.mem_support.mpr ⟨b, hab⟩)
    · exact Set.mem_toFinset.mpr (G.mem_support.mpr ⟨a, hab.symm⟩)

theorem regular_of_no_leaf {n : ℕ} (G : SimpleGraph (Fin n)) (hs : sparse G)
    (hl : ∀ v, G.degree v ≠ 1) (v : Fin n) (hv : v ∈ G.support) : G.degree v = 2 := by
  have hmin : ∀ i ∈ G.support.toFinset, 2 ≤ G.degree i := by
    intro i hi
    have hi' := (G.degree_pos_iff_mem_support i).mpr (Set.mem_toFinset.mp hi)
    have := hl i
    omega
  by_contra hn
  have hv' := Set.mem_toFinset.mpr hv
  have hd := hmin v hv'
  have hsum := Finset.sum_lt_sum hmin (⟨v,hv',by omega⟩ :
    ∃ i ∈ G.support.toFinset, 2 < G.degree i)
  have hmax := support_count G hs
  have hhand := G.sum_degrees_support_eq_twice_card_edges
  simp only [Finset.sum_const, smul_eq_mul] at hsum
  omega

theorem count_after_delete {n : ℕ} (G : SimpleGraph (Fin n)) (v : Fin n) :
    (G.deleteIncidenceSet v).edgeSet.ncard + G.degree v = G.edgeSet.ncard := by
  have h := G.card_edgeFinset_deleteIncidenceSet v
  have hle := G.degree_le_card_edgeFinset v
  simpa only [SimpleGraph.edgeFinset, Set.toFinset_card, ← Nat.card_eq_fintype_card,
    Nat.card_coe_set_eq] using (h ▸ Nat.sub_add_cancel hle :
      (G.deleteIncidenceSet v).edgeFinset.card + G.degree v = G.edgeFinset.card)

theorem two_neighbors {n : ℕ} {G : SimpleGraph (Fin n)} {v : Fin n} (hd : 2 ≤ G.degree v) :
    ∃ a b, a ≠ b ∧ G.Adj v a ∧ G.Adj v b := by
  have h : 1 < (G.neighborFinset v).card := by rw [G.card_neighborFinset_eq_degree]; omega
  obtain ⟨a,ha,b,hb,hab⟩ := Finset.one_lt_card.mp h
  exact ⟨a,b,hab,(G.mem_neighborFinset _ _).mp ha,(G.mem_neighborFinset _ _).mp hb⟩

theorem four_cycle {n : ℕ} {G : SimpleGraph (Fin n)} (hf : noFour G) {v a1 w a2 : Fin n}
    (h1 : G.Adj v a1) (h2 : G.Adj a1 w) (h3 : G.Adj w a2) (h4 : G.Adj a2 v)
    (d1 : v ≠ w) (d2 : a1 ≠ a2) : False := by
  have e1 := h1.ne
  have e2 := h2.ne
  have e3 := h3.ne
  have e4 := h4.ne
  let c : G.Walk v v := Walk.cons h1 (Walk.cons h2 (Walk.cons h3 (Walk.cons h4 Walk.nil)))
  apply hf v c _ rfl
  rw [Walk.cons_isCycle_iff, Walk.isPath_def]
  refine ⟨?_, ?_⟩
  · simp [e2, e3, e4, d2, e1.symm, d1.symm]
  · simp [e1, e2, d1, d2, e1.symm, e4.symm]

theorem list_two (l : List ℕ) (hl : l.length ≤ 2) {p t : ℕ} (hp : p ∈ l) (ht : t ∈ l)
    (hpt : p ≠ t) : ∀ i ∈ l, i = p ∨ i = t := by
  rcases l with _ | ⟨a, _ | ⟨b, _ | ⟨c, r⟩⟩⟩
  · simp at hp
  · simp at hp ht; omega
  · simp at hp ht ⊢; omega
  · simp at hl

theorem graph_twin {n : ℕ} {G : SimpleGraph (Fin n)} {C : Circuit} (h : detects G C)
    (hf : noFour G) {v a1 a2 : Fin n} (hva1 : G.Adj v a1) (hva2 : G.Adj v a2) (hne : a1 ≠ a2)
    (deg1 : 2 ≤ G.degree a1)
    (tw : ∀ y : Fin n → Bool,
      W C (Function.update y a1 true) C.output = W C (Function.update y a2 true) C.output ∧
      W C (Function.update y a1 true) C.output =
        W C (Function.update (Function.update y a1 true) a2 true) C.output) : False := by
  by_cases hadj : G.Adj a1 a2
  · have t := (tw (fun _ => false)).2
    rw [single_false h _ ?_, pair_true h hadj _ ?_ (by simp)] at t
    · cases t
    · rw [Function.update_of_ne hne]; simp
    · intro i j hi hj
      by_cases ei : i = a1
      · by_cases ej : j = a1
        · rw [ei, ej]
        · rw [Function.update_of_ne ej] at hj; cases hj
      · rw [Function.update_of_ne ei] at hi; cases hi
  · obtain ⟨b1, b2, hb, hb1, hb2⟩ := two_neighbors deg1
    obtain ⟨w, hw, hwv⟩ : ∃ w, G.Adj a1 w ∧ w ≠ v := by
      by_cases e : b1 = v
      · exact ⟨b2, hb2, fun e2 => hb (e.trans e2.symm)⟩
      · exact ⟨b1, hb1, e⟩
    have t := (tw (one w)).1
    rw [pair_true h hw _ (by simp) (by rw [Function.update_of_ne hw.ne.symm]; exact one_self w)]
      at t
    have t2 := t.symm
    rw [← eval_eq_W] at t2
    obtain ⟨u, u', huu, hu, hu'⟩ := (h _).mp t2
    have vals : ∀ i, Function.update (one w) a2 true i = true → i = a2 ∨ i = w := by
      intro i hi
      by_cases e : i = a2
      · exact Or.inl e
      · rw [Function.update_of_ne e] at hi
        simp only [one, decide_eq_true_eq] at hi
        exact Or.inr hi
    have hwa2 : G.Adj w a2 := by
      rcases vals u hu with rfl | rfl <;> rcases vals u' hu' with rfl | rfl
      · exact absurd rfl huu.ne
      · exact huu.symm
      · exact huu
      · exact absurd rfl huu.ne
    have hwa2' : w ≠ a2 := hwa2.ne
    exact four_cycle hf hva1 hw hwa2 hva2.symm hwv.symm hne

/-! Lemma AND-core -/

theorem core {n : ℕ} {G : SimpleGraph (Fin n)} {C : Circuit} (hm : Monotone2 C)
    (h : detects G C) (hf : noFour G) (deg : ∀ u ∈ G.support, 2 ≤ G.degree u)
    {v : Fin n} (hv : v ∈ G.support) :
    ∃ u ∈ G.support, ∃ j1 j2, j1 ≠ j2 ∧ Hit C u j1 ∧ Hit C u j2 := by
  by_contra hno
  have uniq : ∀ u ∈ G.support, ∀ E, Hit C u E → ∀ k, Hit C u k → k = E := by
    intro u hu E hE k hk
    by_contra hke
    exact hno ⟨u, hu, k, E, hke, hk, hE⟩
  obtain ⟨a1, a2, hne, hva1, hva2⟩ := two_neighbors (deg v hv)
  have hx : W C (Function.update (one a1) v true) C.output ≠ W C (one a1) C.output := by
    rw [one_false h a1, pair_true h hva1 _ (by simp)
      (by rw [Function.update_of_ne hva1.ne.symm]; exact one_self a1)]
    simp
  obtain ⟨E, g, hg, hop, hEv, p, hp, hpE, hpv⟩ := exit_exists C hm v _ hx (one_false h v)
  have uv := uniq v hv E ⟨g, hg, hop, Or.inr ⟨p, hp, hpE, hpv⟩⟩
  obtain ⟨hE1, t1, ht1, ht1E, ht1v, ht1a⟩ := stepB hm h hva1 hg hop hEv uv
  obtain ⟨hE2, t2, ht2, ht2E, ht2v, ht2a⟩ := stepB hm h hva2 hg hop hEv uv
  have hlen := (hm g (List.mem_of_getElem? hg)).2
  have hp1 : p ≠ t1 := by
    intro e; rw [e, ht1v] at hpv; cases hpv
  have hp2 : p ≠ t2 := by
    intro e; rw [e, ht2v] at hpv; cases hpv
  have hin := list_two g.inputs hlen hp ht1 hp1
  have ht12 : t2 = t1 := by
    rcases hin t2 ht2 with e | e
    · exact absurd e.symm hp2
    · exact e
  subst ht12
  have hs1 : a1 ∈ G.support := G.mem_support.mpr ⟨v, hva1.symm⟩
  have hs2 : a2 ∈ G.support := G.mem_support.mpr ⟨v, hva2.symm⟩
  have u1 := uniq a1 hs1 E ⟨g, hg, hop, Or.inr ⟨t2, ht1, ht1E, ht1a⟩⟩
  have u2 := uniq a2 hs2 E ⟨g, hg, hop, Or.inr ⟨t2, ht2, ht2E, ht2a⟩⟩
  have hp1' : W C (one a1) p = false := by
    rw [← and_two C (one a1) hg hop hin hp hpE ht1E ht1a, hE1]
  have hp2' : W C (one a2) p = false := by
    rw [← and_two C (one a2) hg hop hin hp hpE ht1E ht2a, hE2]
  have tw := twin C hm a1 a2 hg hop hin hp hpE ht1E ht1a ht2a hp1' hp2' u1 u2
    (one_false h a1) (one_false h a2)
  exact graph_twin h hf hva1 hva2 hne (deg a1 hs1) tw

/-! Theorem PF: the induction -/

theorem hit_killed {n : ℕ} (C : Circuit) (hm : Monotone2 C) (ρ : Fin n → Option Bool)
    (v : Fin n) (hρ : ρ v = some true) (k : ℕ) (hk : Hit C v k) : Killed C ρ k := by
  have up : ∀ w, W C (one v) w = true → S1 C ρ w := fun w hw x =>
    W_mono C hm (one_le v _ (by simp [fix, hρ])) w hw
  obtain ⟨g, hg, hop, hh⟩ := hk
  refine ⟨g, hg, hop, ?_⟩
  rcases hh with hh | ⟨i, hi, hlt, hv⟩
  · exact Or.inr (Or.inl (up _ hh))
  · exact Or.inr (Or.inr ⟨i, hi, hlt, up i hv⟩)

theorem not_one {n : ℕ} {G : SimpleGraph (Fin n)} {C : Circuit} (h : detects G C)
    (ρ : Fin n → Option Bool) (v : Fin n) (hρ : ∀ i, ρ i = some true → i = v) :
    ¬ S1 C ρ C.output := by
  intro hS
  have h1 := hS (fun _ => false)
  rw [single_false h] at h1
  · cases h1
  · have key : ∀ i, fix ρ (fun _ => false) i = true → i = v := by
      intro i hi
      apply hρ
      unfold fix at hi
      cases e : ρ i with
      | none => rw [e] at hi; cases hi
      | some b => rw [e] at hi; simp at hi; rw [hi]
    intro i j hi hj
    rw [key i hi, key j hj]

theorem main {n : ℕ} : ∀ (k : ℕ) (G : SimpleGraph (Fin n)) (C : Circuit) (A : Finset ℕ),
    G.edgeSet.ncard = k → sparse G → noFour G → Monotone2 C → detects G C →
    (∀ j g, C.gates[j]? = some g → g.op = .and → j ∈ A) →
    ∃ T : Finset (Fin n), (∀ u v, G.Adj u v → u ∈ T ∨ v ∈ T) ∧ T.card ≤ A.card := by
  intro k
  induction k using Nat.strong_induction_on with
  | _ k ih =>
  intro G C A hk hs hf hm h hc
  by_cases hedge : ∃ a b, G.Adj a b
  swap
  · push Not at hedge
    exact ⟨∅, fun u v huv => absurd huv (hedge u v), by simp⟩
  by_cases hleaf : ∃ v, G.degree v = 1
  · obtain ⟨v, hv⟩ := hleaf
    rw [← G.card_neighborFinset_eq_degree] at hv
    obtain ⟨u, hu⟩ := Finset.card_eq_one.mp hv
    have hvu : G.Adj v u := (G.mem_neighborFinset _ _).mp (by rw [hu]; simp)
    have nbr : ∀ b, G.Adj v b → b = u := by
      intro b hb
      have : b ∈ G.neighborFinset v := (G.mem_neighborFinset _ _).mpr hb
      rw [hu] at this
      simpa using this
    have hx : W C (Function.update (one u) v true) C.output ≠ W C (one u) C.output := by
      rw [one_false h u, pair_true h hvu _ (by simp)
        (by rw [Function.update_of_ne hvu.ne.symm]; exact one_self u)]
      simp
    obtain ⟨E, g, hg, hop, _, p, hp, hpE, hpv⟩ := exit_exists C hm v _ hx (one_false h v)
    let ρ : Fin n → Option Bool := fun i =>
      if i = v then some true else if i = u then some false else none
    have hρv : ρ v = some true := by simp [ρ]
    have hfix : ∀ x i, fix ρ x i = if i = v then true else if i = u then false else x i := by
      intro x i
      unfold fix
      by_cases e1 : i = v
      · simp [ρ, e1]
      · by_cases e2 : i = u
        · have huv : u ≠ v := hvu.ne.symm
          simp [ρ, e2, huv]
        · simp only [ρ, e1, e2, ↓reduceIte, Option.getD_none]
    have kill : ∀ j ∈ ({E} : Finset ℕ), Killed C ρ j := by
      intro j hj
      rw [Finset.mem_singleton.mp hj]
      exact hit_killed C hm ρ v hρv E ⟨g, hg, hop, Or.inr ⟨p, hp, hpE, hpv⟩⟩
    have no := not_one h ρ v (by
      intro i hi
      by_contra e1
      by_cases e2 : i = u
      · simp [ρ, e2] at hi
        exact hvu.ne hi.symm
      · simp [ρ, e1, e2] at hi)
    obtain ⟨C', B, hm', hcard, heval, hcov⟩ := restrict C ρ A {E} hm hc kill no
    let G' := G.deleteIncidenceSet u
    have hdet : detects G' C' := by
      intro x
      rw [heval x, h (fix ρ x)]
      constructor
      · rintro ⟨a, b, hab, ha, hb⟩
        rw [hfix] at ha hb
        have huv : u ≠ v := hvu.ne.symm
        have hau : a ≠ u := by intro e; rw [e] at ha; simp [huv] at ha
        have hbu : b ≠ u := by intro e; rw [e] at hb; simp [huv] at hb
        have hav : a ≠ v := by rintro rfl; exact hbu (nbr b hab)
        have hbv : b ≠ v := by rintro rfl; exact hau (nbr a hab.symm)
        refine ⟨a, b, G.deleteIncidenceSet_adj.mpr ⟨hab, hau, hbu⟩, ?_, ?_⟩
        · simpa [hav, hau] using ha
        · simpa [hbv, hbu] using hb
      · rintro ⟨a, b, hab, ha, hb⟩
        obtain ⟨hab, hau, hbu⟩ := G.deleteIncidenceSet_adj.mp hab
        refine ⟨a, b, hab, ?_, ?_⟩
        · rw [hfix]; by_cases e : a = v <;> simp [e, hau, ha]
        · rw [hfix]; by_cases e : b = v <;> simp [e, hbu, hb]
    have hcnt := count_after_delete G u
    have hdeg : 0 < G.degree u := (G.degree_pos_iff_exists_adj u).mpr ⟨v, hvu.symm⟩
    have hle : (G.deleteIncidenceSet u).edgeSet.ncard < k := by omega
    obtain ⟨T, hT, hTc⟩ := ih _ hle G' C' B rfl
      (sparse_subgraph (G.deleteIncidenceSet_le u) hs)
      (noFour_subgraph (G.deleteIncidenceSet_le u) hf) hm' hdet hcov
    refine ⟨insert u T, ?_, ?_⟩
    · intro a b hab
      by_cases ha : a = u
      · left; rw [ha]; exact Finset.mem_insert_self _ _
      by_cases hb : b = u
      · right; rw [hb]; exact Finset.mem_insert_self _ _
      rcases hT a b (G.deleteIncidenceSet_adj.mpr ⟨hab, ha, hb⟩) with h' | h'
      · exact Or.inl (Finset.mem_insert_of_mem h')
      · exact Or.inr (Finset.mem_insert_of_mem h')
    · have := Finset.card_insert_le u T
      rw [Finset.card_singleton] at hcard
      omega
  · push Not at hleaf
    have reg := regular_of_no_leaf G hs hleaf
    have deg : ∀ u ∈ G.support, 2 ≤ G.degree u := fun u hu => le_of_eq (reg u hu).symm
    obtain ⟨a0, b0, hab0⟩ := hedge
    obtain ⟨c, hcs, j1, j2, hj, hj1, hj2⟩ :=
      core hm h hf deg (G.mem_support.mpr ⟨b0, hab0⟩)
    obtain ⟨a1, a2, hne, hca1, hca2⟩ := two_neighbors (deg c hcs)
    have nbr : ∀ b, G.Adj c b → b = a1 ∨ b = a2 := by
      have hsub : ({a1, a2} : Finset (Fin n)) ⊆ G.neighborFinset c := by
        intro b hb
        rcases Finset.mem_insert.mp hb with rfl | hb
        · exact (G.mem_neighborFinset _ _).mpr hca1
        · rw [Finset.mem_singleton.mp hb]; exact (G.mem_neighborFinset _ _).mpr hca2
      have heq := Finset.eq_of_subset_of_card_le hsub (by
        rw [G.card_neighborFinset_eq_degree, reg c hcs, Finset.card_pair hne])
      intro b hb
      have : b ∈ G.neighborFinset c := (G.mem_neighborFinset _ _).mpr hb
      rw [← heq] at this
      simpa using this
    let ρ : Fin n → Option Bool := fun i =>
      if i = c then some true else if i = a1 ∨ i = a2 then some false else none
    have hρc : ρ c = some true := by simp [ρ]
    have hfix : ∀ x i, fix ρ x i =
        if i = c then true else if i = a1 ∨ i = a2 then false else x i := by
      intro x i
      unfold fix
      by_cases e1 : i = c
      · simp [ρ, e1]
      · by_cases e2 : i = a1 ∨ i = a2
        · simp only [ρ, e1, e2, ↓reduceIte, Option.getD_some]
        · simp only [ρ, e1, e2, ↓reduceIte, Option.getD_none]
    have kill : ∀ j ∈ ({j1, j2} : Finset ℕ), Killed C ρ j := by
      intro j hj'
      rcases Finset.mem_insert.mp hj' with rfl | hj'
      · exact hit_killed C hm ρ c hρc _ hj1
      · rw [Finset.mem_singleton.mp hj']; exact hit_killed C hm ρ c hρc _ hj2
    have no := not_one h ρ c (by
      intro i hi
      by_contra e1
      by_cases e2 : i = a1 ∨ i = a2
      · simp only [ρ, e1, e2, ↓reduceIte] at hi; cases hi
      · simp only [ρ, e1, e2, ↓reduceIte] at hi; cases hi)
    obtain ⟨C', B, hm', hcard, heval, hcov⟩ := restrict C ρ A {j1, j2} hm hc kill no
    let G' := (G.deleteIncidenceSet a1).deleteIncidenceSet a2
    have hc1 : c ≠ a1 := hca1.ne
    have hc2 : c ≠ a2 := hca2.ne
    have hdet : detects G' C' := by
      intro x
      rw [heval x, h (fix ρ x)]
      constructor
      · rintro ⟨a, b, hab, ha, hb⟩
        rw [hfix] at ha hb
        have ha1 : a ≠ a1 ∧ a ≠ a2 := by
          constructor <;> (rintro rfl; simp_all)
        have hb1 : b ≠ a1 ∧ b ≠ a2 := by
          constructor <;> (rintro rfl; simp_all)
        have hac : a ≠ c := by
          rintro rfl; rcases nbr b hab with e | e
          · exact hb1.1 e
          · exact hb1.2 e
        have hbc : b ≠ c := by
          rintro rfl; rcases nbr a hab.symm with e | e
          · exact ha1.1 e
          · exact ha1.2 e
        refine ⟨a, b, ?_, ?_, ?_⟩
        · rw [deleteIncidenceSet_adj, deleteIncidenceSet_adj]
          exact ⟨⟨hab, ha1.1, hb1.1⟩, ha1.2, hb1.2⟩
        · simpa [hac, ha1.1, ha1.2] using ha
        · simpa [hbc, hb1.1, hb1.2] using hb
      · rintro ⟨a, b, hab, ha, hb⟩
        rw [deleteIncidenceSet_adj, deleteIncidenceSet_adj] at hab
        obtain ⟨⟨hab, ha1, hb1⟩, ha2, hb2⟩ := hab
        refine ⟨a, b, hab, ?_, ?_⟩
        · rw [hfix]; by_cases e : a = c <;> simp [e, ha1, ha2, ha]
        · rw [hfix]; by_cases e : b = c <;> simp [e, hb1, hb2, hb]
    have hcnt := count_after_delete G a1
    have hdeg : 0 < G.degree a1 := (G.degree_pos_iff_exists_adj a1).mpr ⟨c, hca1.symm⟩
    have hsub : G'.edgeSet.ncard ≤ (G.deleteIncidenceSet a1).edgeSet.ncard :=
      Set.ncard_le_ncard (edgeSet_mono (deleteIncidenceSet_le _ a2)) (Set.toFinite _)
    have hle : G'.edgeSet.ncard < k := by omega
    have hG' : G' ≤ G := le_trans (deleteIncidenceSet_le _ a2) (deleteIncidenceSet_le _ a1)
    obtain ⟨T, hT, hTc⟩ := ih _ hle G' C' B rfl (sparse_subgraph hG' hs)
      (noFour_subgraph hG' hf) hm' hdet hcov
    refine ⟨insert a1 (insert a2 T), ?_, ?_⟩
    · intro a b hab
      by_cases ha : a = a1 ∨ a = a2
      · left; rcases ha with rfl | rfl <;> simp
      by_cases hb : b = a1 ∨ b = a2
      · right; rcases hb with rfl | rfl <;> simp
      push Not at ha hb
      have hab' : G'.Adj a b := by
        rw [deleteIncidenceSet_adj, deleteIncidenceSet_adj]
        exact ⟨⟨hab, ha.1, hb.1⟩, ha.2, hb.2⟩
      rcases hT a b hab' with h' | h'
      · left; simp [h']
      · right; simp [h']
    · have e1 := Finset.card_insert_le a1 (insert a2 T)
      have e2 := Finset.card_insert_le a2 T
      rw [Finset.card_pair hj] at hcard
      omega

end PFAnd612

/-- Theorem PF (AND half): in every monotone fan-in-2 circuit computing the edge function of a
C4-free pseudoforest `G`, the AND gates (any finite set `A` of gate indices containing every AND
gate) are at least as many as the vertices of some vertex cover of `G`. -/
theorem PEqualNP.Outside.PF_AND : ∀ (n : ℕ) (G : SimpleGraph (Fin n)) (C : PEqualNP.CircuitLowerBounds.Circuit) (A : Finset ℕ), (∀ S : Finset (Fin n), {e : Sym2 (Fin n) | e ∈ G.edgeSet ∧ ∀ v ∈ e, v ∈ S}.ncard ≤ S.card) → (∀ (v : Fin n) (c : G.Walk v v), c.IsCycle → c.length ≠ 4) → PEqualNP.MetaComplexity.Monotone2 C → (∀ x : Fin n → Bool, C.eval (List.ofFn x) = true ↔ ∃ u v : Fin n, G.Adj u v ∧ x u = true ∧ x v = true) → (∀ (j : ℕ) (g : PEqualNP.CircuitLowerBounds.Gate), C.gates[j]? = some g → g.op = PEqualNP.CircuitLowerBounds.GateOp.and → j ∈ A) → ∃ T : Finset (Fin n), (∀ u v : Fin n, G.Adj u v → u ∈ T ∨ v ∈ T) ∧ T.card ≤ A.card := by
  intro n G C A hs hf hm h hc
  exact PFAnd612.main _ G C A rfl hs hf hm h hc
