# AI-for-mathematics pipelines: what we can use

Written 2026-11-25. Scope: what published AI-for-math pipelines do, what we can copy without training models
(prompting-only Opus agents + Python/pysat/kissat + Lean 4/Mathlib, 4 cores, 15 GB RAM, no GPU), and how
that applies to our open tasks:
**(a)** Petersen size 19 (`L-meta-612/petersen19/`, `petersen/sat19/README.md`);
**(b)** L-gct-196 (4x7 level space, dim <= 9);
**(c)** the general loop conjecture -> falsify -> hand proof -> review -> Lean (`L-meta-612/STATUS.md`, `t9/t9.md`).

Sections: §0 immediately actionable (a)/(b) · §1 comparison table · §2 per-system notes · §3 ranked
recommendations · §4 gap analysis · §5 proposed pipeline · §6 evaluation plan · §7 references.
"[ours]" marks my own reasoning or measurements, not a claim from a paper.

---

## 0. Immediately actionable for (a) and (b)

**Bottom line.** I found no published theorem that settles either task. For (b) no result bounds
linear spaces on the level set of the permanent by p+q-2. The closest literature is Chan–Ilten on Fano schemes
of permanents [R41], which covers a different variety. For (a) no exact monotone size of f_Petersen is
published. Both tasks are engineering-bound, and the techniques below are the ones with direct evidence.

### 0.1 Task (a): does Petersen have a monotone AND/OR fan-in-2 circuit with 19 gates?

What we have: `enc5.py` (selector encoding on the 30 critical rows: 15 edges and 15 maximal independent sets), a
size-20 circuit pool (`pool20.json`), restriction constraints (`rest_*.json`), LNS (`lns.py`) and cube
hooks (`--cube`, `--partial`, `--nand`). Size 17 is UNSAT only *conditionally* (146 s). Sizes 18 and 19 time out
after 2 h, monolithically. The prior strongly favours "no 19": L-meta-612 has never been violated in hundreds of
thousands of circuits. So spend about 80% of compute on the UNSAT side (§3, value of information).

| # | Action | Source | Why / expected effect | How, concretely |
|---|---|---|---|---|
| A1 | **Make the conditional result unconditional first.** Compute exact L(H) for every induced subgraph H of Petersen that the restriction constraints use: the open 7-vertex type and all 8- and 9-vertex types. | Lemma-library / reuse idea (Seed-Prover lemma pool [R12]; Heule's practice of proving small lemmas first [R30]); our README | Any final UNSAT claim for 18/19 needs these bounds anyway. Every proved bound also tightens the 18/19 encodings. These instances are much smaller: \|E\|<=12, sizes <=17. | Petersen is vertex-transitive and distance-transitive, so there are only a few induced subgraphs up to isomorphism: 1 class with 9 vertices, 2 with 8. Enumerate them with `networkx` canonical labels and run `runlevel.sh NAME EDGES MAXS TO` per class. Write the results into `proven.json` and `rest_*.json` with log paths. Replace the README's blanket assumption by citations of these entries. |
| A2 | **Cube-and-conquer with time estimation** for 18 first (calibration), then 19. | Heule et al. Cube-and-Conquer [R29]; Pythagorean triples: about 10^6 cubes, 800 cores, 2 days [R30]; Schur 5 / Keller used the same "estimate from sampled cubes" step [R31] | Turns a 2-h timeout into a measured cost: you learn whether 19 needs 10 CPU-h or 10^4. Easy cubes then run on all 4 cores. | Split on structural variables `enc5.py` already exposes: output op (`--outop`), (#AND, #OR) (`--nand/--nor`), and the op and children of the output gate and its two predecessors (`--partial`). Then go one level deeper with a lookahead proxy: pysat `Solver.propagate(assumptions)` counts implied literals; split on the variable that maximises propagation on both branches (march_cu's heuristic). Sample about 50 random cubes at 10 min each, fit the runtime distribution, and multiply by the number of cubes. Deepen the split until the median cube takes under 60 s. Run with `parallel -j4 kissat`. |
| A3 | **Stronger symmetry breaking under Aut(Petersen)** (order 120) on inputs, beyond `--symb`. | SAT Modulo Symmetries [R33]; BreakID static breaking [R34]; Haaswijk et al.: symmetry breaking and topology families dominate exact-synthesis runtime [R27] | Up to 120x less symmetric search. This is an upper bound: canonical gate order already removes the gate-permutation part. | (i) Static: emit lex-leader clauses for the 120 input permutations acting on the selector variables of the *first* gates. (ii) Dynamic, SMS-style: pysat 1.9 + `cadical195` here exposes IPASIR-UP (`connect_propagator`; checked in this environment). Write a propagator that, when the first k gates are assigned, checks whether some automorphism plus re-canonicalisation gives a lexicographically smaller prefix, and adds a blocking clause if so. |
| A4 | **Certificates for any UNSAT claim.** | DRAT/LRAT checking [R35, R36]; empty-hexagon and Keller proofs were checked with verified checkers, and the encoding itself was verified in Lean [R31, R32] | Without this, "UNSAT" is not accepted by reviewers. | Kissat writes DRAT (`kissat cube.cnf cube.drat`). Build `drat-trim` (one C file) and check each cube. Also check that the cube set is exhaustive: the CNF "not(any cube)" plus the structural constraints is UNSAT, which is trivial. Have an *independent* second encoder (`sat19/enc3.py` vs `enc5.py`) re-solve a random 5% of cubes. Lean's `bv_decide` contains a kernel-checked LRAT checker. It suits the small A1 lemmas, but not proofs of hundreds of GB. |
| A5 | **Topology-family split** as an alternative to A2: enumerate DAG "level profiles" (number of gates per depth, depth of output) and solve each family separately. | Haaswijk et al. (percy) [R27] | Embarrassingly parallel, and families are mostly tiny. Their paper reports that topology information both prunes and parallelises SAT exact synthesis. | Add `--profile d1,d2,...` to `enc5.py`: per-depth gate counts, via existing depth-canonical order variables. Enumerate profiles summing to 19, with depth bounded by the size-20 circuits' depth + 2. |
| A6 | **Counterexample side (≤20% budget): don't-care-aware windowed resynthesis** from the size-20 pool. | Kulikov–Pechenev–Slezkin SAT local improvement [R25]; eSLIM adds don't cares [R26]; AlphaEvolve-style diversification of starting points [R1] | `lns.py` keeps downward-closed gate sets. Windows with don't cares allow more changes: a window only has to match the input patterns that actually reach it on the 30 critical rows. | For each window of 4–7 gates (convex subgraph) of each circuit in `pool20.json`: (1) simulate the 30 rows to get the set of reachable window-input vectors; (2) ask SAT for a monotone window of size w-1 that agrees on those vectors; (3) splice it in and re-verify on all 2^10 inputs. Use `kissat`/`cadical195` with a 10 s timeout per window. |
| A7 | **Theory-side shortcut:** computer-assisted gate elimination. Prove "some restriction x_v:=0/1 or x_{N[v]}:=0 removes ≥k gates" by a SAT case analysis on the *local* neighbourhood of the first gates. | Golovnev–Kulikov–Smal–Tamaki, computer-generated gate-elimination case analysis [R28] | This is the same shape as our Lemma T2 route (`deg3/deg3.md`). A SAT-checked local case analysis could prove the Petersen bound without a 19-gate search. | Encode "first two gates touching x_v, plus their readers" as a partial circuit; enumerate cases with `--partial`, and for each case SAT-check that the restricted circuit computes f_{G-v} or f_{G-N[v]} with the claimed number of gates removed. |

Order: A1 → A2 calibrated on 18 (with A3 where cheap) → A4 on every UNSAT → A5 if A2's estimate is above
about 200 CPU-h. A6 runs at low priority alongside the others; A7 is a parallel thinking task for one agent.

### 0.2 Task (b): L-gct-196, a level space of 4x7 matrices has dim <= 9

**Reformulation [ours, checked].** The four conditions are exactly the coefficients of s^k in per(J + s·t), where
per is the rectangular permanent (a sum over injections rows→columns). Indeed
per(J+st) = Σ_k s^k · (q-k)!/(q-p)! · e_k(t), with e_k the sum of the k×k subpermanents. So L is level iff the
affine space J + L lies in the level set {per = per(J) = 840}. That is the right search phrase for the
literature (linear spaces in level sets of the permanent; Fano schemes [R41]). I found no published bound of
this form.

**Structural observation [ours, numerically checked].** e_2(t) = ½·tᵀ[(J_4−I)⊗(J_7−I)]t. On ℂ^{4×7} its
eigenvalues are 18 (×1, the all-ones direction), +1 (×18, the doubly centred matrices P), −3 (×6) and −6 (×3).
The 9 negative directions, N, are p+q−2 = 9. L ⊂ 1^⊥ is totally isotropic for e_2. Hence:
* over ℝ, dim L <= min(18, 9) = 9 using only e_1 and e_2. This is presumably the content of the accepted L-gct-158;
* over ℂ, e_1 and e_2 alone give only dim L <= ⌊27/2⌋ = 13. The cubic and quartic conditions have to remove 4
  more dimensions;
* the general inequality dim L <= dim π_N(L) + dim(L ∩ P) <= 9 + dim(L ∩ P) shows where the work is: level
  vectors that are *doubly centred*. In addition, L∩P is orthogonal, under the plain dot product, to π_P(L),
  because P ⊥ N for e_2. This matches the existing desk items on doubly- and row-centred bounds
  (L-gct-216/217, 199/200/201). **A plausible route:** prove a 4×q doubly-centred bound and a row-centred bound,
  then combine them through this decomposition. This is speculative; check it against how L_gct_215 splits its
  cases (`MidCase`/`HighPair`, row-projection ranks `u L m`, pair ranks `p L i j`).

| # | Action | Source | Why | How, concretely |
|---|---|---|---|---|
| B1 | **Refute first, numerically.** Search for 4×7 level spaces of dim 9 and 10 (and 4×6 of dim 8, L-gct-187). | Refute-before-prove: Wagner [R7]; Seed-Prover tries to "prove or disprove every conjecture" [R12]; Aletheia: verification is the bottleneck [R22] | A 10-dim space refutes L-gct-196 and saves all Lean work. If only dim 8 ever appears, you learn the extremal structure the proof has to handle. | Unknown basis B ∈ ℂ^{28×k}. The residuals are all polarisations: e_1(b_i); E_2(b_i,b_j); E_3(b_i,b_j,b_l); E_4(b_i,…,b_m) for multisets of indices (E_k = full polarisation of e_k). Run Levenberg–Marquardt (`scipy.optimize.least_squares` on real and imaginary parts) with a penalty keeping BᴴB = I, over thousands of random restarts on 4 cores. Record the rank and the invariants of each solution (dims of row projections, L∩P, π_N(L)). Exactify hits with PSLQ/LLL over ℚ(i, ω), as the 4x5 proof does. |
| B2 | **Do not copy-paste-port the 4x5 proof.** It contains 560 occurrences of `Fin 5`, 297 `fin_cases` and 312 `decide` [ours, grep], and 4x4→4x5 grew 1.7k→7.5k lines. Instead, **generalise to `Fin q`** and instantiate q=6 (L-gct-195) and q=7 (L-gct-196). | AlphaEvolve "generalizer mode": evaluate one program on many n so it must find the general pattern [R2]; Seed-Prover lemma pool [R12] | One proof for two open desk items. It avoids an estimated 20k+ line proof [ours, extrapolation]. | Step 1: an agent extracts the lemma DAG of `L_gct_215.lean` (682 lemmas) into a blueprint (`gct196/blueprint.md`) and tags each lemma q-generic, q-specific-but-symmetric (replace `fin_cases` by a WLOG via the permutation lemmas `nL`/`gI`/`pP`), or q-specific. Step 2: move the generic ones (`orth_bound`, `rank_nullity`, `finrank_sup_span`, `dE`, `vM`, the permutation-invariance lemmas, the e_2 identity of L-gct-159) into `LevelLib.lean`, parameterised by `q`. |
| B3 | **Statement-first skeleton with `sorry`**, then parallel per-lemma agents. | DeepSeek-Prover-V2 subgoals as `have … := by sorry` [R14]; Draft-Sketch-Prove [R17]; Hilbert recursive decomposition [R20]; Delta Prover reflective decomposition [R19] | Errors stay local. Lemmas compile independently, and several agents work at once. | Write the top-level theorem for general q with every case lemma stated and `sorry`-ed, and make it compile. One file per lemma (`import LevelLib`), so agents compile only their own file with `lake env lean`. Run at most 3 concurrent Lean processes: a Mathlib import takes about 3–4 GB of RAM. |
| B4 | **Error-driven repair, not resampling.** On failure, repair the failing block. After 2–3 failed repairs of the same lemma, re-decompose it rather than retry. | APOLLO: 25,600 → 362 samples at equal accuracy; o4-mini 7% → 46.7% [R18]. Seed-Prover: a problem needing Pass@8192 solved with about 64–256 refinement-equivalent samples [R12]. Delta Prover: re-decomposition solves IMO 2019 P1 where 1024 repair-only calls failed [R19] | Fewer wasted agent turns. | Agent protocol: (1) compile; (2) take the *first* error, its goal state and the local context; (3) close it with `sorry`, so the rest still checks (APOLLO's "Sorrifier"); (4) try an automation ladder on each sorry (`simp`, `ring`, `linear_combination`, `omega`, `grind`, `nlinarith`, `positivity`, `decide`); (5) only then call an LLM sub-agent on what remains. Log every failed tactic per goal in the ledger, so nobody tries it twice (COPRA keeps the same kind of failure memory [R23]). |
| B5 | **CAS certificates for the algebra steps.** | MathCheck SAT+CAS [R37]; Mathlib `polyrith` (needs network, unavailable here) | Steps like `alg_contra`, `pair_zero`, `dist_aux` and `vand` are ideal-membership facts. Their Lean proofs come for free once the coefficients are known. | Compute Gröbner-basis cofactors with `sympy` 1.14 (installed): `reduced(goal, hyps)` returns the quotients. Paste them as `linear_combination (exp := k) c₁ * h₁ + …`. Keep a small script `lean_tools/lincomb.py` that prints the Lean term. |
| B6 | **Reuse the accepted libraries.** Retrieve before proving. | LeanDojo/ReProver: premise retrieval [R15]; Hilbert: semantic theorem retriever [R20] | Many needed lemmas already exist in `pequalnp-proofs/lean/PEqualNP/Outside/L_gct_*.lean` (for example L-gct-202 constant row, L-gct-205 Lemma FK, L-gct-110/204 direct sums). | Use `rg -n "theorem\|lemma" ~/pequalnp-proofs/lean` with an index file of all statements (name + one-line type). Agents grep it before writing any new lemma. |

---

## 1. Comparison table

Training-free = can we reproduce the ingredient with prompting, search and solvers only?
Y = yes; P = partly (the idea yes, the trained model no); N = needs training.

| System (year) | Generator | Verifier / evaluator | Search & selection | How failures feed back | Decomposition | Scale reported | Training-free |
|---|---|---|---|---|---|---|---|
| FunSearch (2023) [R3] | Code LLM writes a short `priority()` function | Python evaluator (score of the construction) | Island-model evolution; best-shot prompt with 2 parent programs | Only via the scores of parents | None (one function, 10–20 lines) | Millions of samples; small LLM; evaluation <= 20 min per CPU [R1, Table 1] | **Y** (OpenEvolve, ShinkaEvolve [R5]) |
| AlphaEvolve (2025) [R1] | Gemini Flash + Pro ensemble, diff edits to whole files | User `evaluate()`, cascade of cheap→expensive tests; optional LLM-judged criteria | MAP-Elites + islands database; multiple metrics; meta-prompt evolution | Program outputs and scores rendered into the prompt | EVOLVE-BLOCKs; may evolve a *search algorithm*, not the object | Thousands of samples; evaluation up to about 100 compute-hours per candidate | **Y** |
| AlphaEvolve at scale, Tao et al. (2025) [R2] | Same | Same, plus a "generalizer mode" scoring over many n | Same | Expert hints in the prompt matter a lot (Nikodym: a hint changed q²−O(q log q) to q²−q^{3/2}) | Pipeline AlphaEvolve → Deep Think (proof) → AlphaProof (Lean) | 67 problems; setup a few hours per problem | **Y**, except the Lean step |
| Nagda–Raghavan–Thakurta (2025) [R4] | AlphaEvolve | Brute-force checker for the final result; **AlphaEvolve-evolved fast verifier (10,000×)** during search | Propose–test–refine | Smooth score for invalid structures | Human refactoring of the reduction so gadgets are finite | Gadgets up to 19 variables; MAX-4-CUT 0.987, TSP 111/110 | **Y** |
| Wagner RL (2021) [R7] | Small MLP policy (cross-entropy method) | Score function | Keep top x% and train | Gradient on elite sessions | None | Hours on a PC per conjecture | P (tiny training on CPU) |
| PatternBoost (2024) [R6] | Small transformer trained on the best constructions | Score | Alternate local search ↔ global model | Elite set re-trained | None | No-C4 n=33: 116.5M local searches to reach 96 edges | P (local search Y; transformer needs a GPU) |
| AlphaGeometry 1/2 (2024/25) [R8, R9] | LM proposes auxiliary constructions | Symbolic deduction engine (DD+AR) | Beam search | Engine closure | Construct → deduce | 100M synthetic theorems; 25/30 → 42/50 IMO geometry | P (the engine is Y) |
| AlphaProof (2024/25) [R10] | RL-trained Lean prover | Lean kernel | AlphaZero tree search; **test-time RL on problem variants** | RL on variants | Variant generation | IMO 2024 P1, P2, P6; up to days per problem | N (variant generation is P) |
| DeepSeek-Prover V1.5 / V2 (2024/25) [R13, R14] | V1.5: 7B prover + RMaxTS; V2: DeepSeek-V3 sketches, 7B fills | Lean | MCTS (V1.5); subgoal-wise sampling (V2) | Truncate-and-resume at the first error (V1.5) | **V2: `have … := by sorry` subgoals** | miniF2F 63.5% → 88.9%; PutnamBench 49 | P (decomposition Y) |
| Kimina-Prover (2025) [R16] | RL "think then Lean" model | Lean | Best-of-n | Later versions: error-fix | Informal reasoning first | 80.7% miniF2F at pass@8192 | N / P |
| Goedel-Prover V1/V2 (2025) [R11] | Expert-iterated prover; V2 adds verifier-guided self-correction | Lean | pass@k | **Self-correction from Lean errors** | Scaffolded data | V2-32B 88–90% miniF2F; 86 PutnamBench | P |
| Seed-Prover (2025) [R12] | RL lemma-style whole-proof model | Lean | Light (8–16×8–16 refinements), medium (inner/outer), heavy (5000 conjectures → lemma pool) | Compiler feedback + self-summary + proved and failed lemmas in the prompt | **Lemma-style + conjecture pool** | IMO 2025 5/6; PutnamBench 331/657; "days of thinking" per hard problem | P (whole control loop Y) |
| Delta Prover (2025) [R19] | **General LLM (Gemini 2.5 Pro), no fine-tuning** | Lean | Iterative repair + reflective re-decomposition | Unsolved subproblems trigger a new sketch | DSL for decomposition | 95.9% miniF2F with 16,384 calls | **Y** |
| Hilbert (2025) [R20] | Reasoner LLM + prover LLM + retriever | Lean | Recursive decomposition on failure | Error-driven | Recursive subgoals | PutnamBench 462/660 | **Y** (with a general model as prover) |
| APOLLO (2025) [R18] | Any LLM | Lean REPL | Low top-K per sub-lemma | **Syntax fix → sorrify failing blocks → auto tactics → recurse** | Automatic from errors | 25,600 → 362 samples at the same accuracy | **Y** |
| Draft-Sketch-Prove (2022) [R17] | LLM informal draft → formal sketch | Isabelle + Sledgehammer | Sampling | — | Sketch with holes | about 39% miniF2F | **Y** |
| LeanDojo / ReProver (2023) [R15] | Retrieval-augmented tactic model | Lean | Best-first | — | — | 98k Mathlib theorems; 1 GPU-week | P (retrieval is Y) |
| COPRA (2023) [R23] | GPT-4 in-context agent | Lean / Coq | Stack-based backtracking | **Remembers failed tactics per state**; retrieval | Step-level | Low cost per problem | **Y** |
| Lean Copilot (2024) [R24] | Tactic model inside Lean | Lean | `aesop` + LLM | — | — | About 74% of proof steps automated | P |
| LeanAgent (2024) [R40] | Lifelong-trained prover | Lean | Curriculum over repositories | Progressive training | — | `sorry` theorems across 23 repositories | N (curriculum ordering is P) |
| Aristotle, Harmonic (2025) [R21] | Lean search + informal lemma generator + geometry engine | Lean | Search | Lemma re-formalisation | **Informal proof → lemmas → formal** | IMO 2025 gold (formal); used on Erdős problems | P (available as a service; not here) |
| Gauss, Math Inc (2025) [R39] | Autoformalisation agent | Lean | — | — | Blueprint-driven | Strong PNT about 25k Lean lines in 3 weeks | P |
| AI co-scientist (2025) [R38] | Generation / Reflection / Ranking / Evolution / Meta-review agents | LLM review + tournament | Elo tournament | Reflection critiques | Hypothesis level | Biomedicine | **Y** |
| Aletheia, DeepMind (2026) [R22, R43] | Deep Think agent: generate–verify–revise | NL verifier, then humans | — | Revise from verifier | — | 700 Erdős problems → 200 candidates → 63 correct → **13 meaningful** | **Y** (pattern) |
| Heule SAT (2016–2024) [R30–R32] | Encoding + symmetry breaking + cube-and-conquer | CDCL + DRAT/LRAT + verified checker (encoding in Lean for the hexagon) | Lookahead cubes | Re-split hard cubes | Cubes | Pythagorean triples: 800 cores × 2 days, 200 TB proof | **Y** |
| MathCheck SAT+CAS [R37] | SAT solver | SAT + CAS callbacks (isomorphism, nonexistence certificates) | CDCL with programmatic learned clauses | CAS lemmas become clauses | — | Lam's problem, Kochen–Specker | **Y** (pysat IPASIR-UP) |
| Circuit SAT: KKY / Knuth / SLIM / eSLIM / percy [R25–R28, R42] | Exact-synthesis CNF | SAT | Windows (local improvement); topology families | Improved windows spliced back | Subcircuits | Seconds per window; reproduces old hand bounds | **Y** |
| Equational Theories Project, Tao et al. (2024–25) [R44] | Humans + ATPs (Vampire, Mace4, …) + LLMs | Lean | Crowd + automation | **Shared ledger of implications and counterexamples** | 22M implications | Complete, Lean-verified | **Y** (ledger pattern) |

## 2. Per-system notes: the parts that transfer

* **FunSearch / AlphaEvolve** [R3, R1]. The key design choices: (1) evolve a *program that builds* the object,
  or a *search algorithm*. The AlphaEvolve authors hypothesise that constructor programs suit symmetric
  objects and evolved search heuristics suit irregular ones (§2.1). (2) A cascade evaluator kills bad
  candidates cheaply. (3) A diverse database (MAP-Elites/islands); optimising several metrics helps even the
  single target metric. (4) Rich context: literature and rendered evaluation results. Ablations: removing
  evolution, prompt context, meta-prompting, full-file evolution or the strong LLM each degrades results
  significantly (Fig. 8). FunSearch needs fast evaluators (<= 20 min per CPU) and millions of samples.
  AlphaEvolve needs thousands, but with frontier models.
* **Tao et al.** [R2]. Problem setup takes "a few hours"; hints change outcomes dramatically. Failures are
  reported honestly: Heilbronn variants, Duchi's conjecture (no counterexample found), the Erdős–Szekeres
  convex k-gon bound (no improvement), and constructions later beaten by human-style methods.
  AlphaProof formalised only the simplest Deep Think proofs: it needed everything to be in Mathlib already.
* **Nagda et al.** [R4]. The closest to our setting (complexity theory, gadgets). The lessons:
  (i) evolve the *verifier*, guarded against cheating by a synthetic test set plus an LLM judge plus a
  brute-force recheck of the final object; (ii) a smooth score for invalid candidates; (iii) human
  refactoring of the proof so the search object is finite. Failure: Hadamard 668, and could not even
  reproduce 428.
* **PatternBoost / Wagner** [R6, R7]. Local search does most of the work. The learned global model only
  re-seeds it. Wagner keeps elites "indefinitely, until outperformed". Without a GPU, use the local-search half
  and let an LLM play the global role by writing seeds or generators (AlphaEvolve does exactly this).
* **Provers** [R12–R21]. They converge on one recipe: informal plan → lemma-style formal skeleton with
  `sorry` → independent lemma attempts → compiler-error-driven repair → re-decomposition when stuck → a
  lemma pool shared across attempts. Training mostly buys a cheaper fill-in model. Delta Prover [R19] and
  Hilbert [R20] show the control loop alone, with general models, reaches the state of the art on
  competition benchmarks. MiniCTX-v2 (81.8% for Seed-Prover [R12]) is the only listed result near
  research-repository context. CombiBench is only 30%: combinatorics with new definitions stays hard.
* **Heule** [R29–R32]. Every big success combines four things: a careful encoding (verified separately), symmetry breaking,
  cube-and-conquer with estimated cost, and a checkable proof (DRAT/LRAT plus a verified checker). For the
  empty hexagon, the encoding was itself proved correct in Lean [R32].
* **Circuit SAT** [R25–R28, R42]. Exact synthesis is feasible up to roughly 10–12 gates monolithically.
  Beyond that, people use windows (SLIM/eSLIM), topology families (percy) or problem-specific case analysis
  (gate elimination). Haaswijk et al. stress that exact-synthesis runtime is unpredictable and hard to
  parallelise without topology information.
* **Aletheia / Erdős** [R22]. The verifier passed 200 of 700. Of these, 137 were flawed and 50 of the 63 "correct"
  ones solved a misread statement. Rediscovery of known literature was frequent. Statement fidelity and
  novelty checks, not proof search, were the bottleneck.

## 3. What we can adopt now: ranked recommendations

Ranked by (expected benefit / cost) in our environment. Each entry gives: what · source · benefit · cost · how.

**R1. Claim ledger with negative results** — task (c), also (a) and (b).
Source: Equational Theories Project [R44]; Seed-Prover lemma/conjecture pool [R12]; AlphaEvolve program
database [R1]. Benefit: no re-proving or re-refuting. STATUS.md lists 4 refuted intermediate statements
(Lemma E*, OR split, Lemma M', Lemma D) whose counterexamples should be checked automatically against every
new lemma. Cost: about 1 h to set up. How: `research/ledger/claims.jsonl`, one line per claim:
`{id, informal, lean_stmt?, status: open|refuted|proved_informal|proved_lean|conditional, evidence_paths,
depends_on, refuted_by (instance), p_true, attempts:[{agent, approach, outcome, cost}]}`. Plus
`research/ledger/counterexamples/` holding the small objects themselves (graphs, circuits, matrices). Rule: a new
lemma is first run against every stored counterexample of its type.

**R2. Refute-first triage with cheap falsifiers** — (c), (b) via B1, (a) via A6.
Source: Wagner [R7]; Seed-Prover "prove or disprove every conjecture" [R12]; T9 (our own success: DATA checks
before the hand proof). Benefit: the refuted lemmas in STATUS.md were each found only after proof attempts
[ours, from the notes]. Cost: one falsifier script per domain, built once. How: before any hand proof, a
"red" agent gets 10% of the budget to find a counterexample with brute force, SAT or numerics. Proving starts
only after that pass.

**R3. Statement-first Lean + `sorry` skeleton + per-lemma files + repair loop** — (b), (c).
Source: [R14, R17, R18, R19, R20, R12]. Benefit: APOLLO reports 70× fewer samples at equal accuracy;
Seed-Prover reaches Pass@8192-level results with about 64–256 refinement samples. Our agents already repair
iteratively, so the realistic gain is in *structure*: locality, parallelism, no re-reading of a 7.5k-line file.
Cost: low. How: B3 and B4 above. Write the formal statement *before* the hand proof and have a second agent check
it against the intended meaning: 50 of Aletheia's 63 "correct" answers addressed a misread statement [R22].

**R4. SAT: cube-and-conquer + symmetry + certificates** — (a); any future exact-synthesis question.
Source: [R29–R36]. Benefit: makes cost predictable and parallel, and makes UNSAT claims checkable. Cost: 1–2
agent-days of engineering; CPU as estimated. How: A2–A5.

**R5. Lemma/encoding library reuse** — all tasks.
Source: Seed-Prover lemma pool [R12]; LeanDojo retrieval [R15]; our own rewrite history: `enc.py`,
`enc2.py`, `enc3.py`, `enc5.py`. Benefit: avoid rewriting. Cost: low. How: `research/lib/sat/circuit_synth.py`
(one encoder with plug-in constraints and a result cache keyed by a hash of (canonical graph, size, flags)).
Also `research/lean/LevelLib.lean` and a statement index (B6).

**R6. Adversarial reviewer agents with tools** — (c).
Source: AI co-scientist reflection and tournament [R38]; Aletheia verifier [R22]; Nagda's judge LLM *plus* test
suite [R4]. Benefit: catches gaps before Lean, as `review9/` did for T9. Cost: one agent per claim. How: the
reviewer prompt requires (i) a list of every step it could not verify, (ii) a counterexample attempt against
the falsifier suite for each lemma, and (iii) a statement-fidelity check. Two reviewers who have not seen each
other's reports; the claim is accepted only if both pass it.

**R7. AlphaEvolve-style loop for constructions** — (a) counterexample side, B1-style numeric searches, and
future "SEARCH" desk items (L-gct-179/181/185/187/190).
Source: [R1, R2, R4, R5]. Benefit: proven on extremal-combinatorics constructions; cheap evaluators exist
here. Cost: a small harness, about 200 lines. Subagent tokens are the main cost. How: `evolve/` with
`program_db.jsonl` (code, scores, outputs), parent sampling (best plus a random diverse member), a prompt with
2 parents plus rendered scores, a diff-style edit, and an evaluator with a timeout. Run 4 evaluators in
parallel. Give expert hints in the prompt; they matter a great deal [R2].

**R8. CAS-in-the-loop for algebra** — (b).
Source: MathCheck [R37]; Nagda MIP comparison [R4]. How: B5. For finite-field evidence (as for L-gct-182),
script the F_p computations once in `lib/cas/`.

**R9. Evolve the evaluator** (Nagda's 10,000× trick) — (a), (b).
Source [R4]. For SAT this means evolving *encodings or cube heuristics* scored by the solve time on known-answer
instances (Petersen sizes 15–18 and the induced subgraphs). Guard against cheating: every encoding must
reproduce known SAT and UNSAT answers, and must accept the stored size-20 circuits.

## 4. Gap analysis: weaknesses of the surveyed pipelines, with evidence

| Gap | Evidence | Consequence for us |
|---|---|---|
| **G1. The verifier is the bottleneck** (cost or soundness) | Nagda: exponential gadget verification; had to evolve the verifier, and 1 s per evaluation slowed the search [R4]. FunSearch needs evaluation <= 20 min [R1]. Aletheia: human verification was the arduous step [R22]. | Our SAT runs time out; our hand proofs need a separate review. Speeding up verification is the highest-leverage move. |
| **G2. Wasted samples / regenerate-from-scratch** | APOLLO: whole-proof pipelines use up to 25,600 samples; repair cuts this about 70× [R18]. Seed-Prover: refinement replaces Pass@8192 [R12]. | Agents that restart proofs instead of repairing waste turns. |
| **G3. No reuse of refuted hypotheses / no negative-result bookkeeping** | No surveyed prover stores refuted conjectures across problems. Seed-Prover keeps a per-problem pool only [R12]. The Equational Theories Project is the exception: an explicit ledger of implications and counterexamples [R44]. Tao et al. report failures only in prose [R2]. | Our refuted Lemma D and OR split were found by separate, unconnected efforts. |
| **G4. Weak decomposition of research-level problems** | Benchmarks are competition math. Seed-Prover: CombiBench 30%, with new definitions hard [R12]. AlphaProof formalised only proofs whose ingredients were already in Mathlib [R2]. APOLLO depends on the quality of the initial sketch [R18]. | (b) needs a human-quality blueprint before automation helps (B2). |
| **G5. Open-ended truth value (prove vs. refute both live)** | AlphaEvolve and PatternBoost only construct; provers only prove. Seed-Prover's "prove or disprove" is per-conjecture with no budget model [R12]. Aletheia: 50 of 63 "correct" answers were vacuous because of statement misreading [R22]. | We need explicit triage: (a) is exactly a "both live" question. |
| **G6. No cross-problem lemma transfer without training** | LeanAgent transfers by *training* [R40]. Retrieval (LeanDojo, Hilbert) covers Mathlib, not one's own fresh lemmas [R15, R20]. | Our accepted L_gct_* lemmas are not indexed for reuse. |
| **G7. Lean formalisation cost of long proofs** | Seed-Prover proofs exceed 1000 lines at "medium" [R12]. Gauss needed about 25k lines for Strong PNT [R39]. Our 4x4→4x5 growth was 1.7k→7.5k. | Generalising (parameterising by q) beats instance proofs. |
| **G8. SAT encodings are not reused or verified** | Heule verifies the encoding (Lean, empty hexagon) only as a final step [R32]. Haaswijk: runtime is unpredictable [R27]. | 4 encoder rewrites; conditional results whose assumptions are not tracked. |
| **G9. No calibrated stopping or triage** | No surveyed system reports a value-of-information rule. AlphaEvolve runs to its budget; Seed "heavy" runs for days [R1, R12]. Nagda report that some problems (Hadamard 668) never moved despite a fast verifier [R4]. | Our 2-h timeouts are arbitrary. A2's cube-time estimate gives a principled stop. |
| **G10. Novelty / literature checking** | Aletheia: 9 of 13 resolutions were already in the literature [R22]. Nagda cite results superseded quickly [R4]. | Check `literature.md` before claiming. |

## 5. Proposed pipeline: "Ledger–Triage–Repair" (LTR)

**Goal.** About 10× less agent-time per *closed desk item* in our setting. The honest version of that claim is
in §5.4.

### 5.1 Components (data structures)
1. **Claim ledger** (`research/ledger/claims.jsonl`, R1). It keeps the DAG of claims with status, p_true,
   evidence, conditional assumptions, and attempts with failure reasons. A plain-text index plus `rg` is enough
   at our scale; no embeddings are needed.
2. **Counterexample store** (`ledger/counterexamples/<type>/*.json`) with a `check_all(claim)` runner that
   tests every stored object of a matching type.
3. **Falsifier suite** (`lib/falsify/`): circuit verifier on the critical rows plus exhaustive small-n
   enumeration (graphs via networkx); level-space numerics (B1); F_p linear algebra.
4. **Encoding library** (`lib/sat/`): one parameterised circuit-synthesis encoder, cube generator, DRAT
   runner, and a result cache keyed by `sha256(canonical instance, size, flags)`.
5. **Lean library and index** (`research/lean/Lib/*.lean` + `lean_index.txt`): generic lemmas from accepted
   proofs, with one line per statement for grep.
6. **Job queue for CPU** (`flock`/GNU `parallel -j`): at most 3 Lean processes (RAM-bound), the rest for SAT
   and numerics. LLM subagents are not CPU-bound, so run 4–8 of them concurrently and queue their CPU jobs.

### 5.2 Control loop (per open claim C)
1. **Intake.** Write C informally *and* as a Lean statement. A fidelity agent checks that the Lean statement
   matches the intent (G5: Aletheia's misreads). Run `check_all(C)` against stored counterexamples.
2. **Triage.** Set p_true from evidence (data checks, analogy to proved cases). Value of information:
   VOI(C) = P(C decides its parent) × value(parent) / E[cost]. Pick the next claim by the highest VOI.
3. **Split the budget between the prove and refute branches.** Use Thompson-style allocation: refute
   share = max(0.1, 1 − p_true), prove share = max(0.1, p_true). Each failed falsification round of cost c
   raises p_true by a Bayesian update with a modest likelihood ratio, so the budget drifts toward proving as
   the claim survives. Each failed proof round lowers p_true only slightly.
4. **Refute branch.** Exhaustive small cases → SAT → AlphaEvolve-style construction search (R7). A hit becomes
   a counterexample-store entry, and every claim that depends on C is re-triaged.
5. **Prove branch.** Hand-proof sketch → lemma list in the ledger → Lean skeleton with `sorry` (statement-first)
   → parallel lemma agents with the repair ladder (B4) → re-decompose after 2–3 failed repairs (Delta) →
   proved lemmas go into the library. Lean starts at step 1, not at the end: a skeleton that compiles is the
   blueprint.
6. **Review.** Two independent adversarial reviewers (R6) with tool access. A claim is accepted when Lean
   checks it, or when both reviewers pass it and it is marked "informal".
7. **Propagation.** If a lemma is refuted, mark its dependants as conditional or broken. Re-run triage.
8. **Stopping.** Each attempt has a budget. Escalate to the coordinator when the re-decomposition count reaches 3, or when
   the SAT cost estimate exceeds the remaining budget. Write a ledger summary when escalating.

### 5.3 Agent specialisations
Prover (informal), Formaliser (Lean statements and skeletons), Repairer (one sorry at a time; small context),
Falsifier/Red (counterexample search, encodings), Reviewer ×2 (adversarial), Librarian (indexes lemmas and
counterexamples, deduplicates, checks literature). This mirrors the co-scientist roles [R38] and Seed-Prover
tiers [R12].

### 5.4 Where a 10× could come from, honestly

| Mechanism | Stage affected | Evidence | Our estimate |
|---|---|---|---|
| Repair instead of resample; per-lemma files; automation ladder | Lean formalisation | APOLLO 70× fewer samples; Seed 32–128× [R18, R12] | **2–4×** for us: agents already iterate, so the gain is mostly locality and parallelism. Speculative. |
| Parameterised proof (one proof for q=6 and q=7) | Lean (b) | 4x4→4x5 line growth of 4.4× [ours] | **About 2× per desk item**: two items from one proof, and no 20k-line instance proofs. |
| Refute-first + counterexample store | Discovery loop (c) | 4 refuted lemmas in STATUS.md, each found late [ours]; Seed's prove-or-disprove [R12] | **1.5–3×** on false-lemma-heavy routes; measurable. |
| Cube-and-conquer + symmetry + time estimates | SAT (a) | Heule-scale proofs [R30–R32]; percy [R27] | Unknown factor. It turns "timeout" into "N CPU-h". Calibrate on size 18. |
| Parallel subagents (4–8) gated by a CPU queue | All | AlphaEvolve's async pipeline [R1] | **2–3× wall-clock**, limited by 4 cores and 15 GB. |

The product of the midpoints is about 10–20× on Lean-heavy items. These stage factors are *not* independent,
and the evidence comes from competition benchmarks. Treat 10× as a hypothesis for §6 to test, not a result.

## 6. Evaluation plan

**Metrics** (per desk item):
1. wall-clock to verdict and agent-hours;
2. tokens per accepted result;
3. false-claim rate: claims marked PROVED that a reviewer or later work refutes;
4. Lean: repair iterations per lemma, lines, compile time;
5. SAT: CPU-hours to a *certified* verdict, and the fraction of cubes closed;
6. time to first counterexample on false claims.

**Benchmark (known answers, held out).** Replay about 12 closed items, with answer files hidden in a separate
worktree:
* Lean: L-gct-214 (4x4 ≤ 6), L-gct-216, L-gct-217, L-gct-202, L-gct-193, L_meta_599 / PF_AND (T9 AND half);
* refutations: the OR split (n=8 graph), Lemma D, Lemma M' (two triangles plus a bridge);
* SAT: Petersen conditional size-17 UNSAT (baseline 146 s), H8a/H8b restriction levels (`petersen19/logs/`),
  rediscovery of a size-20 circuit.

**Baseline.** The current workflow as recorded in `L-meta-612/` (logs, t2–t10 progression, `review9/`) and the
accepted Lean files: 1.7k and 7.5k lines for 4x4 and 4x5. Reconstruct agent-hours from session logs where
available, and otherwise re-run the baseline arm.

**Pilot (runnable here, about 2 days).** 4 items, chosen as 2 Lean (L-gct-216, L-gct-202), 1 refutation
(Lemma D), 1 SAT (size-17 conditional). Two arms: baseline vs LTR, same model, same caps (3 agent-hours and
8 CPU-hours per item), with randomised order. Success criterion for continuing: at least 3× median improvement
on metric 1 or 2, with no increase in metric 3. Claim 10× only after the full 12-item replay *and* one new
desk item (L-gct-195 or 196) closes faster than the baseline estimate. Report failures alongside successes,
following the Aletheia transparency figures [R22].

## 7. References

* [R1] Novikov et al., *AlphaEvolve: A coding agent for scientific and algorithmic discovery*, 2025. https://arxiv.org/abs/2506.13131
* [R2] Georgiev, Gómez-Serrano, Tao, Wagner, *Mathematical exploration and discovery at scale*, 2025. https://arxiv.org/abs/2511.02864
* [R3] Romera-Paredes et al., *Mathematical discoveries from program search with large language models* (FunSearch), Nature 625:468–475, 2024. https://www.nature.com/articles/s41586-023-06924-6
* [R4] Nagda, Raghavan, Thakurta, *Reinforced Generation of Combinatorial Structures: Hardness of Approximation*, 2025/26. https://arxiv.org/abs/2509.18057
* [R5] Open-source evolvers: OpenEvolve https://github.com/codelion/openevolve ; Lange, *ShinkaEvolve*, https://arxiv.org/abs/2509.19349
* [R6] Charton, Ellenberg, Wagner, Williamson, *PatternBoost*, 2024. https://arxiv.org/abs/2411.00566
* [R7] Wagner, *Constructions in combinatorics via neural networks*, 2021. https://arxiv.org/abs/2104.14516
* [R8] Trinh et al., *Solving olympiad geometry without human demonstrations* (AlphaGeometry), Nature 625:476–482, 2024. https://www.nature.com/articles/s41586-023-06747-5
* [R9] Chervonyi et al., *Gold-medalist performance … AlphaGeometry2*, 2025. https://arxiv.org/abs/2502.03544
* [R10] Hubert et al., *Olympiad-level formal mathematical reasoning with reinforcement learning* (AlphaProof), Nature, Nov 2025. https://www.nature.com/articles/s41586-025-09833-y ; blog https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/
* [R11] Lin et al., *Goedel-Prover*, https://arxiv.org/abs/2502.07640 ; *Goedel-Prover-V2*, https://arxiv.org/abs/2508.03613
* [R12] ByteDance Seed, *Seed-Prover: Deep and Broad Reasoning for Automated Theorem Proving*, 2025. https://arxiv.org/abs/2507.23726
* [R13] Xin et al., *DeepSeek-Prover-V1.5*, 2024. https://arxiv.org/abs/2408.08152
* [R14] Ren et al., *DeepSeek-Prover-V2*, 2025. https://arxiv.org/abs/2504.21801
* [R15] Yang et al., *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models*, NeurIPS 2023. https://arxiv.org/abs/2306.15626
* [R16] Wang et al., *Kimina-Prover Preview*, 2025. https://arxiv.org/abs/2504.11354
* [R17] Jiang et al., *Draft, Sketch, and Prove*, ICLR 2023. https://arxiv.org/abs/2210.12283
* [R18] Ospanov, Farnia, Yousefzadeh, *APOLLO: Automated LLM and Lean Collaboration*, NeurIPS 2025. https://arxiv.org/abs/2505.05758
* [R19] Zhou et al., *Solving Formal Math Problems by Decomposition and Iterative Reflection* (Delta Prover), 2025. https://arxiv.org/abs/2507.15225
* [R20] Varambally et al., *Hilbert: Recursively Building Formal Proofs with Informal Reasoning*, ICLR 2026. https://arxiv.org/abs/2509.22819
* [R21] Harmonic, *Aristotle: IMO-level Automated Theorem Proving*, 2025. https://arxiv.org/abs/2510.01346
* [R22] Feng et al., *Semi-Autonomous Mathematics Discovery with Gemini: A Case Study on the Erdős Problems*, 2026. https://arxiv.org/abs/2601.22401
* [R23] Thakur et al., *An In-Context Learning Agent for Formal Theorem-Proving* (COPRA), 2023. https://arxiv.org/abs/2310.04353
* [R24] Song, Yang, Anandkumar, *Lean Copilot*, 2024. https://arxiv.org/abs/2404.12534
* [R25] Kulikov, Pechenev, Slezkin, *SAT-based Circuit Local Improvement*, MFCS 2022. https://arxiv.org/abs/2102.12579 ; code https://github.com/alexanderskulikov/circuit_improvement
* [R26] Reichl, Slivovsky, Szeider, *eSLIM: Circuit Minimization with SAT Based Local Improvement*, SAT 2024. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2024.23 ; code https://github.com/fxreichl/eSLIM
* [R27] Haaswijk, Soeken, Mishchenko, De Micheli, *SAT-Based Exact Synthesis: Encodings, Topology Families, and Parallelism*, IEEE TCAD 39(4), 2020. https://infoscience.epfl.ch/record/271569 ; tool percy https://github.com/whaaswijk/percy
* [R28] Golovnev, Kulikov, Smal, Tamaki, *Gate elimination: circuit size lower bounds and #SAT upper bounds*, TCS 2018 (MFCS 2016). https://eccc.weizmann.ac.il/report/2016/022/
* [R29] Heule, Kullmann, Wieringa, Biere, *Cube and Conquer: Guiding CDCL SAT Solvers by Lookaheads*, HVC 2011.
* [R30] Heule, Kullmann, Marek, *Solving and Verifying the Boolean Pythagorean Triples problem via Cube-and-Conquer*, SAT 2016. https://arxiv.org/abs/1605.00723
* [R31] Brakensiek, Heule, Mackey, Narváez, *The Resolution of Keller's Conjecture*, IJCAR 2020. https://arxiv.org/abs/1910.03740 ; Heule & Scheucher, *Happy Ending: An Empty Hexagon in Every Set of 30 Points*, TACAS 2024. https://arxiv.org/abs/2403.00737
* [R32] Subercaseaux et al., *Formal Verification of the Empty Hexagon Number*, ITP 2024. https://arxiv.org/abs/2403.17370
* [R33] Kirchweger & Szeider, *SAT Modulo Symmetries for Graph Generation*, CP 2021. https://github.com/markirch/sat-modulo-symmetries
* [R34] Devriendt, Bogaerts, Bruynooghe, Denecker, *Improved Static Symmetry Breaking for SAT* (BreakID), SAT 2016.
* [R35] Wetzler, Heule, Hunt, *DRAT-trim*, SAT 2014. https://github.com/marijnheule/drat-trim
* [R36] Tan, Heule, Myreen, *cake_lpr: Verified Propagation Redundancy Checking in CakeML*, TACAS 2021.
* [R37] MathCheck (Bright, Ganesh, Kotsireas et al.): *A SAT-based Resolution of Lam's Problem*, AAAI 2021, https://arxiv.org/abs/2012.04715 ; Li, Bright, Ganesh, *A SAT Solver + Computer Algebra Attack on the Minimum Kochen–Specker Problem*, https://arxiv.org/abs/2306.13319
* [R38] Gottweis et al., *Towards an AI co-scientist*, 2025. https://arxiv.org/abs/2502.18864
* [R39] Math Inc, *Gauss* (Strong Prime Number Theorem formalisation), Sept 2025. https://www.math.inc/gauss
* [R40] Kumarappan et al., *LeanAgent: Lifelong Learning for Formal Theorem Proving*, 2024. https://arxiv.org/abs/2410.06209
* [R41] Chan & Ilten, *Fano schemes of determinants and permanents*, Algebra & Number Theory 9(3):629–679, 2015. https://arxiv.org/abs/1312.2577
* [R42] Kojevnikov, Kulikov, Yaroslavtsev, *Finding Efficient Circuits Using SAT-Solvers*, SAT 2009, LNCS 5584; Knuth, TAOCP Vol. 4A §7.1.2 and Vol. 4B §7.2.2.2.
* [R43] Feng et al., *Towards Autonomous Mathematics Research* (Aletheia), 2026. https://arxiv.org/abs/2602.10177
* [R44] Tao et al., Equational Theories Project. https://github.com/teorth/equational_theories ; https://terrytao.wordpress.com/2024/09/25/a-pilot-project-in-universal-algebra-to-explore-new-ways-to-collaborate-and-use-machine-assistance/
* Also relevant: Bubeck et al., *Early science acceleration experiments with GPT-5*, 2025, https://arxiv.org/abs/2511.16072 (case studies, including Erdős problems; for literature-identification pitfalls see [R22] §1.5).

Notes on verification of citations: I read [R1], [R2], [R4], [R6], [R7], [R12], [R18] and [R22] directly via alphaXiv in this session,
and checked [R10], [R19], [R20], [R25], [R26] and [R27] via search abstracts. Numbers for [R3], [R8], [R9], [R11], [R13]–[R17],
[R21], [R23], [R24], [R28]–[R41] and [R44] are from memory or secondary sources (the Seed-Prover comparison table and
Tao et al.'s introduction). Spot-check them before quoting them externally.
