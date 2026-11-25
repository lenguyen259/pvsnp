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
