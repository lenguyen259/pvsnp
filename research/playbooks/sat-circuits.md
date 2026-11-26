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
- 2026-11-26 (petersen19): the hierarchy is now proved up to H8a/H8b (DRAT); H9 <= 14 UNSAT (pysat,
  55 min at s=14); P >= 16 unconditional (s=15 UNSAT in 559 s). Restriction rows are cheap in enc5
  (4 binary clauses per gate) and the U-singleton family (`grest2.py`, A:=1 with N(A) partly free,
  bound L(H)+|U|) helps. Cube lessons on H9 s=15: cubes with an AND bottom gate on an early pair die in
  ~10 s; exact #AND split kills all k outside {4..7} at once; splitting further on lexbot bits or on the
  first gate leaves one or more children as hard as the parent (the hardness is in the upper circuit).
  Estimate a whole level from a 2-parent sample before committing; prefix splits look cheap but are not.
- drat-trim prints "\rs VERIFIED": strip \r before grepping (see petersen19/drat.sh).
- Other agents may call petersen19/kissat; count only your own PIDs (check the parent).
- 2026-11-26 (meta18434, RepSizeAtMost Fin 10 u!=v, 34 -> 33?): `research/meta18434/lns.py` (monotone, 100-row windowed LNS, copy of meta9745 lns with unary choice removed) runs ~40 windows/s; 2x30 min (75k windows, plateau at 34) found nothing. The local pequalnp-proofs clone working tree is stale (no Defs/Represents.lean): read defs with `git show origin/main:lean/PEqualNP/Defs/Represents.lean` and build in a copy checked out at origin/main. In this sandbox `sleep N` in run_in_background returns at once; wait with `timeout N tail -f log | grep -m1 ...`.
- 2026-11-26 (base7 G8t15..G8t26): of 12 triangle 8-vertex graphs, 5 closed (G8t15..18, G8t20; kissat 10-700 s at Phi-1, drat-trim 1-800 s, up to 500 MB proofs) and 7 hit the 1800 s kissat cap at s = Phi-1 or Phi-2 (G8t19, 21..26). Graphs with a closed G - v of Phi-1 are fast; Phi >= 14 or tau 5 with max tL <= 11 are not.
- 2026-11-26: A Bash run_in_background job is killed after its `timeout` (max 7200000 ms = 2 h), which also counts cpuslot queue wait; a whole batch.sh dies mid-graph. Launch lists of <= 3 slow graphs per background call and restart from the interrupted graph (rename its partial log first).
- 2026-11-26: Monitor greps on the log for "SAT" also match the expected "VALIDATION ... RESULT SAT" line (U circuit accepted); match "kissat: SAT" instead.
- 2026-11-26: `sleep N` in Bash is blocked; use `timeout 590 sh -c 'until [ -f FILE ]; do sleep 30; done'` as the wait.
- 2026-11-26 (meta18173, 3-colourability of 6-vertex graphs, <=65 gates?): the statement is the monotone DNF "not (15 K4 terms or 72 W5 terms)" with edge bit order lexicographic (01,02,..,05,12,..,45); K4-or-W5 claim brute-forced on all 2^15 (0 mismatches vs real 3-colouring). Plain greedy AND-pair extraction + Horner factoring (`meta18173/greedy2.py`) gives only 277 gates; naive structured counts (20 triangles x2, 15 K4 x2, 6 hub stars x4, 12 five-cycles per hub) already pass 110, so 65 needs a genuinely different decomposition, not DNF factoring. Do not start LNS from a greedy DNF circuit; it is ~4x too big. In greedy scripts keep signals = wire ids (a separate signal-id namespace caused a silent wire mix-up).
