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
