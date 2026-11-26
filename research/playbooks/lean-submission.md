# Playbook: Lean files for the desk

## Environment

- Upstream clone (read-only): `/home/user/brilliant-hq/pequalnp-proofs`. Build from `lean/` with
  `PATH=$HOME/.elan/bin:$PATH lake build PEqualNP.Outside.<Module>`.
- Read accepted files with `git show origin/main:<path>` and search them with
  `git grep <pattern> origin/main`. Run `git fetch` first if the clone may be stale.
- Run at most one Lean build at a time; the machine has 15 GB RAM.

## Rules (CONTRIBUTING.md; a program checks them)

- One file, `lean/PEqualNP/Outside/L_<gap>.lean`.
- Import lines come first, with no comments before or among them. Only `Mathlib`, Mathlib modules
  and the listed project modules (usually `PEqualNP.Defs`) may be imported.
- The word import must not appear anywhere after the import lines, including comments.
- Helpers go inside `namespace PEqualNP.Outside.L_<gap>` and `end PEqualNP.Outside.L_<gap>`, both
  at column 0. The theorem comes last and carries its full name, `theorem PEqualNP.Outside.L_<gap>`.
- Not allowed, even inside comments: `sorry`, new axioms, `native_decide`, any `#` command, double
  quotes, `macro`, `syntax`, `notation`, `elab`, `attribute`, `initialize`.
- Options: only `set_option maxRecDepth|maxHeartbeats|synthInstance.maxSize|synthInstance.maxHeartbeats N in`
  placed directly above a declaration.
- The theorem must prove exactly the posted statement.

## Verification before reporting success

1. `lake build` succeeds.
2. In a temporary file, run `#print axioms` and type-check an `example` with the exact statement
   against the theorem. The axioms must be only `propext`, `Classical.choice`, `Quot.sound`. Delete
   the file afterwards.
3. Grep the file for the forbidden words.

## Workflow

- Write the statement first, as a skeleton with `sorry` for each lemma, and build often.
- When a build fails, repair the first error rather than regenerating the proof. After 2 or 3
  failed repairs, split the lemma.
- Compute polynomial certificates offline with sympy for `linear_combination` (`polyrith` needs the
  network).
- Copy accepted lemmas from origin/main rather than reproving them. Credit them in a `--` comment.

## Lessons

- 2026-11-25: L-gct-215 (4x5) is a 7559-line case tree specific to q = 5; it does not port to q = 7.
  For level-space items, look for a proof that works for every q, or release.
- 2026-11-26: IsRUPRun witnesses: accepted templates are L_meta_9250 (explicit UPForces chains, about
  130 lines per clause) and L_meta_9473/9477 (a `replay` function with `replay_sound`, much shorter).
  The list is newest first and the empty clause counts in the length.
- 2026-11-26: L-meta-13789/12905 (monotone 6-input, general size = monotone size). Template L_meta_12038 ships a
  certified frontier search whose data (L_,Y_,XS_,PD_,PM_,G_,T_cert,K_i) comes from an external generator that is not in
  any repo. I rewrote one (python, exact semantics of `next`/`via`/`hfind`/`stepOK`; BST ordered by lex list order;
  hints (tag,j) only for successors stored as a G-image). Scripts: /tmp/w13789/gen.py, mk3.py (may be lost; rewrite from
  the Lean defs). Pitfalls: (1) shell `$((a*2**32+b))` overflows to negative; compute the table with python, else Lean
  gets `-16843026` (Neg N error). (2) Pick the elimination: if one restriction x_p=b has a smaller circuit than min-1,
  one_gate_at cannot reach the bound; 13789 (min 7) needed NO elimination, direct cap 6 on 64 points = 4 states.
  12905 (min 10): one_gate_at p=4 b=false, cap 8 on 32 points, 1678 states. (3) Strong pD (all shifts d, maximal R) and
  pM (every false q, P = y) prune hard. (4) With >1000 states split K into chunks of ~60 with balanced all_app, else
  Lean was OOM-killed (137). Builds: 13789 5 min, 12905 8 min. Check validity: same search at cap = min size must FIND a circuit.
