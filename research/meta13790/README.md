# L-meta-13790: do NOT gates help for this monotone 6-input function? No (both minima are 7)

The desk step asks for a refutation: some size s at which an AND/OR/NOT circuit exists but no
monotone one does.

- f is the edge function of the bipartite graph with edges 03, 13, 23, 04, 24, 05, 15. It has
  47 true inputs and 7 minterms.
- The graph contains the 4-cycle 0-3-2-4.

## Results

The method is the same as in `../meta12906` (encoder `enc.py` with only the truth table changed,
normal-form `--strict` encoding, all 64 rows).

- **Monotone minimum m = 7**:
  - UNSAT at 6.
  - SAT at 7. The circuit, with wires 0..5 = x0..x5:
    `6=x0|x1, 7=x0|x2, 8=x3|x4, 9=x3|x5, 10=7&8, 11=6&9, out=10|11`.
  - The orchestrator re-checked the circuit on all 64 inputs.
  - It is a cover by two rectangles: (x0∨x2)(x3∨x4) ∨ (x0∨x1)(x3∨x5). This uses the C4.
- **General (AND/OR/NOT) minimum g = 7**:
  - UNSAT at 6. kissat with drat-trim gives `s VERIFIED` (`drat.log`).
  - SAT at 7, with the same circuit.
- Since g = m, NOT saves nothing. The positive twin L-meta-13789 holds, so the step's statement is
  false.
- Released with `statement_seems_false`.

## Caveat

The UNSAT result uses the normal-form encoding: no constants, no copies, no double NOT, colex
order. The reduction to that normal form is argued in `../meta12906/README.md`; it is not
machine-checked.
