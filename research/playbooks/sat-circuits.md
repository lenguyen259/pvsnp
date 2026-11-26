# Playbook: SAT for small circuits

## Monotone AND/OR circuits for edge functions

These work:
- `research/L-meta-612/petersen19/enc5.py`:
  - Encoding: gate selectors plus per-row values; the rows are edges and maximal independent sets.
  - Symmetry breaking: depth-canonical order (`--lexbot`).
  - Extra constraints: restriction constraints (`--rest`), Fact C (`--factc`) and Theorem S2
    (`--viol`, only for s < Phi).
- Validation: the encoding must accept the star-cover (U) circuit at s = Phi (`mku.py`, `ulb.py`).
  For Petersen it must also accept the 13-OR size-20 circuit.
- Restriction constraints are only as sound as the bounds they use. Build the hierarchy bottom-up:
  H7, then H8a and H8b, then H9, then the full graph. Record proved bounds in `proven.json`.
- kissat 4.0.4 (binary at `petersen19/kissat`) and drat-trim (`petersen19/drat-trim`) give DRAT
  certificates. Use them for any UNSAT claim we intend to publish.
- Costs grow steeply near Phi:
  - H9 at s = 14: 55 min.
  - H9 at s = 15: over 90 min (timeout).

  Near Phi, use cube-and-conquer. Estimate the total cost on a sample of cubes first.

## Circuits with NOT (general basis)

- A plain 512-row full-basis encoding could not rediscover a known 15-gate circuit in 10 minutes
  (L-meta-10952).
- Use CEGAR instead: start with a few rows (edges, maximal independent sets, a few random rows),
  add counterexample rows, and validate on the known k-gate circuit first
  (`research/meta10531/`).
- The desk has never seen a NOT saving on an edge function. Weigh effort against a low prior.

## Lessons

- 2026-11-25: Over-subscribing 4 cores (6 solvers) slowed every run. Use `cpuslot.sh`.
- 2026-11-24: An agent's `pkill -f enc4.py` killed another agent's runs. Kill your own PIDs only.
- 2026-11-25 (meta9745, Heawood minus edge, 26 -> 25?): window LNS with exact Boolean-relation
  don't-cares (`research/meta9745/lns.py`: force each window-output vector, evaluate the rest on all
  2^n inputs as big-int truth tables) is cheap and validated (27 -> 26 in 21 windows); 2764+241 windows
  found nothing below 26, and SAT never picked a NOT gate.
- 2026-11-25: Window encodings over all 2^|ins| patterns stall at >= 10 inputs (phase 2: ~0.1
  window/s). Cap window inputs at 8-9, set a conflict budget (`conf_budget` + `solve_limited`), or
  add rows by CEGAR.
- 2026-11-25: Pipe `| tail` on a long job loses all output when `timeout` kills it; write logs to files
  with `python3 -u` and flush.
- 2026-11-25: Launch long jobs with the Bash tool's run_in_background through `cpuslot.sh`; a
  `nohup ... &` launch and an extra unslotted python run were refused by the permission classifier.
- 2026-11-25 (meta12906, 6-input truth-table function, "NOT saves a gate?"): `research/meta12906/enc.py`
  does exact synthesis on all 64 rows in the project's model. Without a normal form the general
  basis at s = 9 ran over 8 min; with `--strict` (no constants/copies/NOT-NOT, colex gate order unless
  reading the previous gate) UNSAT 9 took 4 min, DRAT-checked in 7 min. Result g = m = 10, statement false.
- 2026-11-25: Validate a NOT-basis encoding on functions that need NOT (XOR = 4 gates, MUX = 4;
  `meta12906/validate.py`). An `a <= b` symmetry clause plus "NOT has b = missing wire" silently
  forced NOT to read only the false wire, so two UNSAT lines were void. Finding the target at the
  monotone size does not exercise NOT.
- 2026-11-26 (base7, subcubic base cases): `L-meta-612/base7/run7.py NAME EDGES` does the whole bottom-up
  step per graph (restriction family from proven bounds + missing-subgraph report, U-circuit validation,
  every m = 1..Phi-1 through kissat --no-binary + drat-trim, record in ledger/proven_subcubic.json).
  With the full hierarchy below them, all 8 open 7-vertex graphs closed (<= 15 min kissat each), the
  4 triangle-free 8-vertex ones in <= 9 min, and 8-vertex graphs with a subgraph G - v of Phi - 1 in seconds.
- 2026-11-26: drat-trim takes about 1.5x the kissat time; text proofs grow about 80 MB per kissat minute
  (1.1 GB for a 14 min run). Budget disk and time for both before launching.
- 2026-11-26: In shell until-loops, `grep -q "s=11"` also matches "clauses=110757". Match " s=11 ".
- 2026-11-26 (meta9246): "find k clauses, each RUP" as one SAT instance scales badly: 20 variables,
  k = 12 gives 1.1M clauses and no answer in 10 CPU-min; forcing 3 of 7 clauses did not help. Check
  `ps` CPU time, not wall time: cpuslot waits behind other agents' jobs.
