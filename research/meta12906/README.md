# L-meta-12906: does NOT save a gate on a 6-input monotone function? (2026-11-25)

Step: `¬ ∀ s, HasCircuitSize 6 f s → ∃ C, Monotone2 C ∧ C.size ≤ s ∧ C computes f`, with f the
6-input function whose truth table is `4276813546 * 2^32 + 4276791976` (bit r = value on the input
with index r, x_i = bit i of r).

## The function

f is monotone, 43 ones. Maxterms: (x1∨x2∨x3∨x4∨x5), (x0∨x4∨x5), (x0∨x2∨x3), (x0∨x1∨x3), (x0∨x1∨x2), so

    f = (x1∨x2∨x3∨x4∨x5) ∧ (x0 ∨ (x4∨x5) ∧ Th2(x1,x2,x3)).

## Circuit model (lean/PEqualNP/Defs/CircuitLowerBounds.lean, MetaComplexity.lean, MetaComplexityLgpMono.lean)

Straight-line program; size = number of gates; inputs free. A gate reads a list of earlier wire
indices; an index that does not exist reads false (free). `HasCircuitSize`: ops AND/OR/NOT, at most
2 wires (NOT negates its first wire and is a gate; AND of no wire = true, OR of no wire = false, one
wire = copy; each costs a gate). `Monotone2`: the same without NOT. Output: any wire.

## Result

| basis | min size | evidence |
|---|---|---|
| monotone AND/OR (m) | 10 | SAT at 10 (validated on 64 rows); UNSAT at 8, 9 (`--strict`, seconds) |
| AND/OR/NOT (g) | 10 | SAT at 10 (validated); UNSAT at 9 (`--strict`, cadical 4 min; DRAT: kissat 230 s, drat-trim VERIFIED 420 s) |

Labels: m <= 10 and g <= 10 are DATA checked on all 64 rows; g >= 10 is DRAT for the normal-form CNF
`gen9_strict.cnf` (which contains monotone circuits, so it gives m >= 10 too) plus the standard
normal-form argument below, which is not machine-checked. The faithful encodings (no normal form)
at s = 9 are TIMEOUT (mono 280 s, general about 10 min), so they neither confirm nor contradict.
`gen9_strict.cnf` was written before a 9-clause vacuous addition to enc.py; its clause set is a
subset of what enc.py writes now, so the proof covers the current CNF as well.

**g = m = 10, so NOT saves nothing; the step's statement is FALSE** (its negation, L-meta-12905, is
true: every s with HasCircuitSize 6 f s has s >= 10, and the 10-gate monotone circuit serves).
Verdict: release with `statement_seems_false`. No Lean file written (nothing to prove).

10-gate monotone circuit (wires 0..5 = x0..x5, gates from 6):
6=x2∨x3, 7=x2∧x3, 8=x1∨6, 9=x1∧6, 10=x0∧8, 11=x0∨9, 12=x4∨10, 13=7∨11, 14=x5∨12, 15=13∧14.

## Files

- `enc.py s mono|gen [--strict] [--cnf file]`: exact synthesis on all 64 rows (pysat/cadical).
  Faithful mode: gate kinds AND(a,b), OR(a,b), NOT(a), TRUE; a <= b any earlier wire including the
  missing wire 0 (so copies and constants are present); output = last gate; every other gate read
  by a later gate (sound: a smaller circuit is padded with copies at the end).
  `--strict` adds the normal form of a minimum circuit of a non-constant function: no missing
  wire or constant, no copy (a < b), no NOT of NOT, and gates in colex order of (b, a) unless a gate
  reads its predecessor (Knuth/Kojevnikov ordering; the output is last in every topological order
  since every gate is an ancestor of it).
- `validate.py`: the general encodings find XOR (4 gates, uses NOT), NOT x0 (1), MUX (4) and
  refute one gate less. This caught a bug: the first faithful encoding forced NOT to read the
  missing wire (a <= b with b = 0), so early "UNSAT 7, 8 gen" lines were void and were deleted.
- `drat.sh`, `drat.log`: kissat 4.0.4 proof checked by drat-trim.
- `mono.log`, `gen_strict.log`, `faithful.log`: solver outputs.
