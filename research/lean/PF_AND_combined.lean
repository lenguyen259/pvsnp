import PEqualNP.Outside.PF_AND
import PEqualNP.Outside.L_meta_599

open PEqualNP.CircuitLowerBounds PEqualNP.MetaComplexity in
theorem PFAndCheck.combined (n : ℕ) (G : SimpleGraph (Fin n)) (C : Circuit)
    (hs : ∀ S : Finset (Fin n), {e : Sym2 (Fin n) | e ∈ G.edgeSet ∧ ∀ v ∈ e, v ∈ S}.ncard ≤ S.card)
    (hf : ∀ (v : Fin n) (c : G.Walk v v), c.IsCycle → c.length ≠ 4) (hm : Monotone2 C)
    (h : ∀ x : Fin n → Bool, C.eval (List.ofFn x) = true ↔ ∃ u v : Fin n, G.Adj u v ∧ x u = true ∧ x v = true) :
    ∃ T : Finset (Fin n), (∀ u v : Fin n, G.Adj u v → u ∈ T ∨ v ∈ T) ∧
      G.edgeSet.ncard + T.card ≤ C.size + 1 := by
  classical
  let Aa := (Finset.range C.gates.length).filter (fun j => ∃ g, C.gates[j]? = some g ∧ g.op = .and)
  let Ao := (Finset.range C.gates.length).filter (fun j => ∃ g, C.gates[j]? = some g ∧ g.op = .or)
  have ca : ∀ j g, C.gates[j]? = some g → g.op = .and → j ∈ Aa := fun j g hg hop =>
    Finset.mem_filter.mpr ⟨Finset.mem_range.mpr (List.getElem?_eq_some_iff.mp hg).1, g, hg, hop⟩
  have co : ∀ j g, C.gates[j]? = some g → g.op = .or → j ∈ Ao := fun j g hg hop =>
    Finset.mem_filter.mpr ⟨Finset.mem_range.mpr (List.getElem?_eq_some_iff.mp hg).1, g, hg, hop⟩
  obtain ⟨T, hT, hTc⟩ := PEqualNP.Outside.PF_AND n G C Aa hs hf hm h ca
  have hE := PEqualNP.Outside.L_meta_599 n G C Ao hs hf hm h co
  have hdis : Disjoint Aa Ao := by
    rw [Finset.disjoint_left]
    intro j ha ho
    obtain ⟨_, g, hg, hop⟩ := Finset.mem_filter.mp ha
    obtain ⟨_, g', hg', hop'⟩ := Finset.mem_filter.mp ho
    obtain rfl := Option.some.inj (hg.symm.trans hg')
    rw [hop] at hop'
    cases hop'
  have hsub : Aa ∪ Ao ⊆ Finset.range C.gates.length :=
    Finset.union_subset (Finset.filter_subset _ _) (Finset.filter_subset _ _)
  have hcard := Finset.card_le_card hsub
  rw [Finset.card_union_of_disjoint hdis, Finset.card_range] at hcard
  exact ⟨T, hT, by unfold Circuit.size; omega⟩

