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
