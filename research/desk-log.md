# Desk log

One record per step the pequalnp desk assigned to `lenguyen259`. Times are UTC. A step is
**released** when we hand it back, with the reason sent to the desk. The machine-readable version
is `desk-log.json`.

Steps proved ahead of time but never assigned are not listed here: L-meta-413, 418, 420, 421 and
510 (Lean files in `research/lean/`).

| Gap | Assigned | Ended | Desk level | Outcome | Reason | AI effort |
|---|---|---|---|---|---|---|
| L-meta-624 | 2026-11-23T14:37Z | 2026-11-23T14:42Z |  | released | missing_lemma | orchestrator triage |
| L-meta-608 | 2026-11-23T14:42Z | 2026-11-23T15:01Z |  | released | missing_lemma | orchestrator + SAT agents |
| L-meta-612 | 2026-11-23T15:43Z | 2026-11-23 (lease lost on worker restart) | TRACTABLE (desk label) | lease lost; research continued without lease |  | ~30 Opus subagents over 2 days (proof, SAT, review, Lean) |
| L-meta-972 | 2026-11-23T19:1xZ | 2026-11-23T19:12Z |  | released | other | orchestrator triage |
| L-meta-5144 | 2026-11-24 | 2026-11-24T21:57Z |  | released | other | orchestrator triage |
| L-meta-2216 | 2026-11-25T08:40Z | 2026-11-25T08:41Z |  | released | other | orchestrator triage (<1 min) |
| L-meta-1482 | 2026-11-25T09:06Z | 2026-11-25T09:06Z |  | released | other | orchestrator triage (<1 min) |
| L-meta-2583 | 2026-11-25T09:46Z | 2026-11-25T09:46Z |  | released | other | orchestrator triage (<1 min) |
| L-gct-196 | 2026-11-25T10:46Z | 2026-11-25T12:19Z (withdrawn by desk) | TRACTABLE (desk label), plain statement says open case | withdrawn by desk while in work | withdrawn | 3 Opus agents (medium 11 min, high 48 min, high 27 min) |
| L-meta-10524 | 2026-11-25T12:03Z | 2026-11-25T12:16Z | solid, 30 points | proved; PR open-goat/pequalnp-proofs#14149 awaiting official check | submitted | 1 Opus agent (high), ~8 min; orchestrator re-verified build and axioms |
| L-meta-10952 | 2026-11-25T12:16Z | 2026-11-25T12:41Z | solid, 34 points | released | missing_lemma | 1 Opus agent (high), ~25 min |
| L-meta-10531 | 2026-11-25T12:41Z | 2026-11-25T~14:00Z (lease expired during usage-limit outage) | hard, 216 points | lease expired; not settled | expired | 1 Opus agent (high), SAT exact synthesis with CEGAR |
| L-meta-9745 | 2026-11-25T16:12Z | 2026-11-25T17:10Z | open, 793 points | released | other | 1 Opus agent (high), ~55 min, 1 CPU slot |
| L-meta-12906 | 2026-11-25T17:06Z | 2026-11-25T17:5xZ | solid, 30 points | released (statement false) | statement_seems_false | 1 Fable agent (medium), ~45 min, 1 CPU slot; orchestrator re-checked the 10-gate circuit |

## Notes

- **L-meta-624**: C4-free graphs: AND gates plus OR gates bound (circuit size). Released after triage; equivalent to the open L-meta-612 family.
- **L-meta-608**: girth >= 5 graphs: AND/OR circuits for the edge function need >= |E|+tau-1 gates. Open conjecture; partial analysis in research/L-meta-612/girth5.
- **L-meta-612**: C4-free graphs: every AND/OR circuit for f_G has >= |E|+tau-1 gates. Not solved. Results: Theorem PF (C4-free pseudoforests, Lean-formalized), Theorem F, STAR-ALL, many refutations; Petersen size-19 attack ongoing. See research/L-meta-612/STATUS.md.
- **L-meta-972**: projective plane of order 3: every AND/OR circuit has >= 64 gates. Instance of open L-meta-612 on a dense graph.
- **L-meta-5144**: (title not recorded). 
- **L-meta-2216**: refute search hypothesis: no <=61-gate circuit for projective-plane incidence (25 inputs). Stronger than the open L-meta-612 bound; judged out of reach.
- **L-meta-1482**: order-3 plane: no <=64-gate circuit with a double re-read. 64 = |E|+tau-1; L-meta-612 on a dense graph; desk notes plain SAT is insufficient.
- **L-meta-2583**: projective planes of order q: read-1 conversion without size increase. Desk: no proof expected in one piece; open part equals the hard part of L-meta-612.
- **L-gct-196**: level space of 4x7 complex matrices has dimension <= 9. Partial Lean (no sorry): expansion identity, row/two-row bounds, dim L <= 9 + dim D, cases D=0 and low row rank. New 8-dim family N8, conjecture 3 dim L <= pq. research/gct196/.
- **L-meta-10524**: 9-vertex graph (10 edges): edge function needs >= 14 AND/OR/NOT gates. Desk said its recursion reaches only k-1; agent found the missing base row (theta(2,3,3) >= 11 from accepted L-meta-982 via L-meta-9409). Tree: b2 3, f0 6, base.
- **L-meta-10952**: 9-vertex graph (11 edges): edge function needs >= 15 AND/OR/NOT gates. Exact search over the accepted gate-elimination checker: best certifiable bound 13 (14 with hypothetical rows); base rows capped at 12. SAT inconclusive. research/meta10952/.
- **L-meta-10531**: refute: exhibit a <=13-gate AND/OR/NOT circuit for a 9-vertex, 11-edge graph (tau 4, k 14). Agent stopped by the 5-hour usage limit before validating its NOT-basis encoding (could not yet rediscover the 14-gate circuit). research/meta10531/.
- **L-meta-9745**: exhibit a <=25-gate AND/OR/NOT circuit for a 14-vertex 20-edge graph (Heawood graph minus one edge; C4-free, tau 7, |E|+tau-1 = 26). A monotone 25-gate circuit would refute L-meta-612. Window LNS with exact don't-cares (3005 windows, up to 9 gates) never went below 26; SAT never chose NOT. Restriction + rectangle-gadget analysis explains why simple gadgets cannot save. research/meta9745/.
- **L-meta-12906**: refute: for a monotone 6-input function, NOT gates save at least one gate. Exact synthesis on all 64 rows: monotone minimum 10 (circuit verified), general AND/OR/NOT minimum also 10 (UNSAT at 9 in normal-form encoding, DRAT verified). So NOT saves nothing; the positive twin L-meta-12905 holds. research/meta12906/.

## Summary so far

- Assigned: 14. Proved and submitted: 1 (L-meta-10524, upstream PR #14149 awaiting the official check).
  Settled false with machine evidence and released: 1 (L-meta-12906). Withdrawn by the desk: 1.
  Lease lost or expired: 2. Other releases: 9 (7 were instances of the open L-meta-612 family or
  stronger; 2 hit a checker or lemma limit).
- Triage time for out-of-reach steps: under 1 minute each.
