# Patterns of reduction files (R_<prog>_<n>_<k>.lean) on origin/main

Date: 2026-11-26. Source: `open-goat/pequalnp-proofs` origin/main (commit of 05:13 +0200), which
holds 1774 `R_meta_*.lean` files for 799 distinct steps (267 steps have 1 file, 153 have 2, 325
have 3, 46 have 4, 8 have 5 or more). Median file size 6.4 KB (min 0.9 KB, max 190 KB).
25 files were read (list at the end). Label: DATA (reading of merged files).

Caveat: "on main" means the file passed the checker and was merged. It does not show that the
reduction was credited; credit comes only when every hypothesis is later proved. Several merged
files are plain case splits, which join.txt says earn nothing.

## Shape shared by all files

- Imports, optional `--` comment lines, optional `open ...`, optional `set_option maxHeartbeats N in`,
  then one theorem. No namespace, no helper declarations; helper facts are `have` inside the proof.
- Hypotheses are written either as named binders `(name : ∀ ..., ...)` or as an implication chain
  `H1 → H2 → statement`. Both forms are on main.
- The conclusion is the desk statement pasted verbatim (machine variable names x1, x2, ...).
- Hypotheses use readable names (q, N, I, s, W) and may use `let` inside the type.
- Many files import `Mathlib` in addition to `PEqualNP.Defs` (e.g. R_meta_2794_2, R_meta_612_7),
  although the rule says "the step's imports only".
- Several k per step exist (k is free: 1, 2, 42, 556, 601, ...). Different agents posted
  different cuts of the same step; up to 5 or 7 files for one step are on main.

## Classes of split, from weakest to strongest

### A. Plain case split (no difficulty moved)
Two hypotheses are the statement with one extra assumption H and with not-H; the proof is
`by_cases`. Examples: R_meta_612_1 (graph acyclic or not), R_meta_2794_2 (output wire is an
input or a gate), R_meta_8811_1 (q even or odd). These are 1 to 3 KB. By join.txt they earn
nothing unless one side arrives proved.

### B. Case split where one side is closed in the file or by a known bound
The file proves one case itself and leaves the other. Examples: R_meta_2794_601 proves the case
q < 200 inline (a variable-counting bound s >= 2N - 1) and leaves q >= 200; R_meta_2130_42
(`bounded` for q <= 130, `larger` for q >= 131, with a pruning argument inside, 41 KB);
R_meta_2794_556 (the output may be taken to be the first wire equal to it; the copy and empty
cases and the pure-rectangle case are closed inline, leaving "strict union on top" and "exempt
intersection on top").

### C. Conjunction split of the conclusion (construction + properties)
For an existence statement: one hypothesis builds the object with the cheap properties, the others
prove each remaining property for any such object. Examples: R_meta_2796_1 and R_meta_2460_2
(`hBuild`, `hSound`, `hComplete` for a read-2 AND/OR circuit of size 2N). Glue is short.

### D. Elimination step + bound on the smaller instance (gate elimination)
For "function f needs k gates": hypothesis 1 says that fixing an input (or peeling the first
gate) removes d gates and leaves a circuit for a named cofactor f'; hypothesis 2 is the bound
k - d for f'. Examples: R_meta_2020_1 (`eliminate`, `cofactor`), R_meta_1670_1 (`peel`,
`distinguish`), R_meta_1670_3 (`delete`, `dropBound`, `fullBound`: three hypotheses, two of them
plain lower-bound statements that are separate desk steps). This is the pattern for the Petersen
"Table 2" family, and the one most likely to be credited: each child is a finite statement.

### E. Normal form + one hypothesis per normal-form case
Hypothesis 1: every circuit can be replaced by one no larger whose first gate has one of a short
list of shapes; hypotheses 2 to 4: the bound for each shape. Examples: R_meta_670_713
(`normalize`, `unary`, `both`, `either`), R_meta_670_419, R_meta_3216_74 (`normalize`, `lower`,
`residual`).

### F. Extract a combinatorial object + count it
Hypothesis 1: from the circuit, extract a combinatorial certificate whose cost is bounded by the
size (a biclique or rectangle cover, a block family, a family of certificates). Hypothesis 2: a
pure counting bound on such objects, with no circuit in it. The glue proves the link (for
instance that rectangles in a graph with no 4-cycle are stars). Examples: R_meta_612_2
(`extractBlocks`, `countStars`), R_meta_2794_1 (rectangle cover of cost <= 100 s + N, then
N k <= total cost), R_meta_2794_601 (`certificates` generic lemma, `freshPoint` plane lemma,
`coverBound` core), R_meta_3254_1 (`peel` a dense subgraph, then `coreBound`), R_meta_3489_317
(`geometry`, `bound`), R_meta_4305_25 (three counts added: 4 s + 96 s).
The counting hypothesis is usually provable; the extraction hypothesis carries the open part,
and it can be false if the cost constant is chosen carelessly.

### G. Split of the measure (count two resources separately)
Each hypothesis bounds one resource; the glue adds them. Examples: R_meta_612_7 (OR gates
>= |E| - 1, AND gates >= a vertex cover), R_meta_612_4 (`normalize`, `countGates`,
`coverResidual` with an inequality between named gate classes), R_meta_2794_42 (`axisCase`,
`mixedCase`, with a 27 KB charging argument inside the file).

## What the stronger files have in common

- At least one hypothesis is a self-contained statement that is plainly true and provable
  (a counting lemma, a geometry lemma, a finite bound), stated with no reference to the circuit.
- The glue proof does real work (50 to 500 lines), not only `by_cases` or `exact`.
- The hard hypothesis is stated in a new vocabulary (covers, certificates, charged gates) so that
  it is a different statement, not the original with one more assumption.
- Constants are kept loose so the hypotheses are not false (a false hypothesis is refused).

## Step L-meta-2794 (ours)

Five reductions are already on main: R_meta_2794_1 (class F), _2 (class A), _42 (class G),
_556 (class B), _601 (classes B and F). join.txt allows three live reductions per step.
A proved sibling exists: L_meta_9132 (same setting, conclusion 3 N <= s + 1).

## Files read

R_meta_2794_1, _2, _42, _556, _601; R_meta_2020_1; R_meta_1670_1, _3; R_meta_670_713, _419;
R_meta_612_1, _2, _4, _7; R_meta_2796_1; R_meta_3216_74; R_meta_3254_1; R_meta_4305_25;
R_meta_8811_1; R_meta_2130_42; R_meta_3489_317; R_meta_2460_2; and the proved siblings
L_meta_2792, L_meta_4303, L_meta_9132.
