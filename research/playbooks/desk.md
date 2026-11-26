# Playbook: pequalnp desk steps

## Mechanics

- Ask for a step: `GET https://pequalnp.com/desk/next?handle=lenguyen259`. To get a second step
  while already holding one, add `&another=1`. Respect `retry_after_s` (usually 300).
- Never pick a step from the public file. Never open a pull request for a step we do not hold.
- Leases come in two kinds:
  - `meta` steps of level solid or hard: renew every 5 minutes (we use 4).
  - `gct` steps: renew every 10 minutes (we use 9).
  - Renew with `POST /desk/beat?lease=...`. HTTP 410, or "step was withdrawn", means stop work at
    once.
- Release with `POST /desk/release?lease=...&reason=...`. Reasons: submitted, hypothesis_too_weak,
  missing_lemma, statement_seems_false, does_not_elaborate, exhausted, out_of_time, other.
- Submit only after the human has opened the upstream pull request; the session cannot reach the
  upstream repository.
  1. Create a branch named after the gap in `/home/user/pequalnp-proofs` (the fork), based on
     upstream main.
  2. Add one file, in one commit, authored by lenguyen259 with the noreply address.
  3. Push to the fork and give the human the compare link.
  4. Once they confirm, release with `submitted`.
- The upstream repository is now `open-goat/pequalnp-proofs`. Its advisory CI expires unless a
  maintainer approves it; that is not a verdict.

## Triage (under 1 minute; decide before spending agent time)

- **Out of reach, release with `other`**: the step is equivalent to, or stronger than, an open
  problem. Signals: the desk text says "open case" or "no proof expected in one piece"; or the step
  is a lower bound of at least |E|+tau-1 on a dense C4-free graph (that is L-meta-612).
- **Tractable**: desk says TRACTABLE and smaller cases are accepted; or the step is a sibling of an
  accepted file (same checker, different instance); or it is a finite statement provable by kernel
  computation.
- Even when the desk says TRACTABLE, check the plain statement for "open".

## Lessons

- 2026-11-25: Three "TRACTABLE" desk items (gct-196) were in fact open cases. Agents spent about 90
  minutes; the desk then withdrew the step. Before investing, read the plain statement, and spend at
  most about 45 minutes before re-triage.
- 2026-11-25: A sibling of an accepted proof is the cheapest win. L-meta-10524 took 8 minutes by
  renaming accepted `L_meta_9409` and searching for a new elimination tree.
- 2026-11-25: The lease heartbeat loop lives at most 2 h as a background task and dies on a worker
  restart. Re-check the lease (`POST /desk/beat`) after any pause, and restart the loop.
- 2026-11-25: The release reason `exhausted` is only for sharded-search leases; the desk rejects it
  otherwise. For an ordinary step that we tried and failed, use `other`, or `missing_lemma` when
  the precise missing ingredient is known.
- 2026-11-25: Paired steps "for all s ..." (L-meta-12905) and its negation (L-meta-12906) on a
  6-input truth table: triage by exact synthesis first (about 15 min CPU, `research/meta12906/`).
  Here g = m = 10, so the negation was false; release it with `statement_seems_false` and quote m, g.
- 2026-11-25 (from join.txt and tools/pnp.sh on origin/main): "A counterexample is worth as much as a
  proof."
  - When a "False: ..." step turns out false, its positive twin is true. Prove the twin in Lean,
    then lease it with `GET /desk/next?handle=lenguyen259&gap=<twin id>&have=proof` (that is
    `pnp.sh next --proof-of`). This works even while someone else holds the twin. Then submit
    normally.
  - Kinds: prove (default) and refute (prove the negated twin listed in the gap's `refutation`
    field). Request a kind with `&kind=`.
  - The pull request body should be `Lease: <lease id>` (pnp.sh writes it).
  - Accepted "positive twin" proofs to copy: L_meta_12038 to L_meta_12056.
- 2026-11-25: L-meta-10524 is now `checked` on the public data, so our first accepted step is
  credited to lenguyen259.
- 2026-11-26 (L-meta-9246, RUP run for PHP(5,4) with <= 12 clauses, level open): 75 min, unresolved.
  A layered-UP SAT encoding (`research/meta9246/enc.py`) is validated on PHP(4,3) (min 5, UNSAT 4 in
  148 s) but kissat finds neither 12 nor 13 for PHP(5,4) in 10 CPU-min. "Their own run uses 13" was
  not available to us; without it, even the upper bound must be rediscovered. Re-triage such "open"
  items at 30 min.
- 2026-11-26: "False:" / "It is false that:" steps are the negated twins of "Table 2" steps. The
  fleet's own seat (`seat-intake-1`) checks the positive twin and marks the negation `refuted`
  within hours; by the time our Lean proof of L-meta-13789 / 12905 / 14208 was ready (about 8 hours
  after settling the negations by SAT), all three twins were already `checked` and the desk
  answered "That step is not open". So a settled negation is worth only its release reason
  (`statement_seems_false`), unless the Lean proof of the twin can be produced within minutes.
  Do not spend Lean-agent effort on twins of settled "False:" steps.
- 2026-11-26: Plain `next` returns `open`-level and `cut` steps at high rate (6 in a row, each
  released in under a minute). Ask with `&level=solid&kind=prove` to get tractable steps; use
  `poll3.sh` style polling. Levels: warmup, solid, hard, open.
- 2026-11-26: CHECKLIST of what the desk credits (from join.txt). Read `lease.terms.kind` and
  `reductions_open` before releasing any step.
  - kind prove: only a Lean proof file in a pull request. A search that finds nothing is not
    credited, whatever its quality; release honestly (`missing_lemma` if the missing smaller
    lemma is known, so that the desk posts it).
  - kind refute: only a Lean proof of the negated twin, that is, a counterexample file.
  - kind search: a range of a large search. A witness is sent as the Lean file. An empty range is
    reported with `release <step> exhausted <sha256 of the program>`. This is the one case where
    "found nothing" is reportable. The `exhausted` reason is invalid for other kinds.
  - kind value: find the least k; `pnp.sh value <step> <k>` writes the file.
  - kind cut, or any step with `reductions_open: true`: send one file
    `R_<prog>_<n>_<k>.lean` (a reduction into 2 to 4 smaller statements about the library). It
    is credited only when all the smaller statements are proved; a split that carries no part of
    the difficulty earns nothing. Then release the step as `reduced`.
  - We released 6987 and 4715 (kind cut) as `other`. A reduction was possible there; consider one
    next time before releasing, if a real split of the difficulty can be found in minutes.
- 2026-11-26 (L-meta-2794, kind cut): before writing a reduction, list existing R files for the step (`git ls-tree -r --name-only origin/main lean/PEqualNP/Outside | grep R_meta_<n>_`) and grep proved siblings by a distinctive fragment of the statement (`git grep -l '×ˢ Set.univ' origin/main`); 2794 already had 5 reductions and a proved linear sibling L_meta_9132. Classification of accepted splits: research/reductions/patterns.md. In 2794 the exempt set is decorative (take it to be all gates), so the step is the open monotone bound for a C4-free graph.
- 2026-11-26: `poll4.py` (in the scratchpad; copy it into research/tools/ if reused) auto-releases
  ONLY kind=cut steps and hands everything else to the orchestrator. The first version also released
  kind=prove at level hard/open and so threw away L-meta-17964 ("union of paths, folded circuits",
  435 points), which is in our PF/paths territory. Never auto-release prove steps. A step released
  as `other` is not offered again for an hour.
- 2026-11-26: RepSizeAtMost steps (rect, 3x5 / 5x5 masks): `research/meta20499/syn.py S MASK n m` is a 10-second exact synthesis on the 15/25 one-hot rows (validated on 20535: mask 7549 min 9). If SAT at the posted size, write the Lean file from accepted L_meta_20535 (upperC + decide +kernel). If UNSAT, the statement is false: release statement_seems_false; credit needs the refuting lower-bound file (live-set search template L_meta_5469 with an external generator) -- budget that before releasing.
- 2026-11-27 (human instruction): when a Lean file for a leased, creditable step is written, SUBMIT AT ONCE (branch in the fork, one commit, compare link to the human), without waiting for a local Lean build, because other groups can take the step. Keep only the instant static checks (forbidden words, file name, exact statement text, namespace/final theorem). Build locally in parallel AFTER pushing and tell the human at once if it fails.
