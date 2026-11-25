# Environment and reproducibility

There are two kinds of reproducibility here.

1. **Results**: proofs, UNSAT claims and counterexamples. These are deterministic and can be
   re-checked by anyone with the tools below.
2. **The AI process**: LLM agents. A rerun will not produce the same output. What we provide is the
   complete trace: sanitized transcripts, prompts, model ids, scripts and logs. We also report
   success rates over repeated runs where we have them.

## Hardware

- Cloud container (Claude Code on the web): 4 cores, 15 GB RAM, Linux 6.18, no GPU.
- No model training or fine-tuning was used. All AI work is prompting of hosted models.

## AI

- Orchestrator: Claude Code (remote session).
- Subagents: Claude Opus. The exact model id per agent is in `transcripts/export/index.json` (field
  `model`, e.g. `claude-opus-5-5`), with its effort level (`medium` or `high`).
- One human contributor (GitHub handle `lenguyen259`) chose the tasks, approved actions and opened
  the upstream pull requests. Every human message is in the session transcript.

## Proof checking (Lean)

- Lean 4.36.0 (`leanprover/lean4:v4.36.0`, commit 611c117b).
- Lake project: `pequalnp-proofs`, upstream repository `open-goat/pequalnp-proofs` (formerly
  `brilliant-hq/pequalnp-proofs`). Builds used checkout `fcf3122c` (2026-11-23). Later files were
  checked against `origin/main` `e88806f1` where stated.
- Mathlib `fc4f59e577feb1a4956671bc04ac18aaaf8cd842`, Batteries `b4b25a38`, Aesop `66ff77cf`,
  Qq `ff055a2f`, Plausible `054b228c`.
- To re-check a proof file `F`:
  1. Copy `F` to `lean/PEqualNP/Outside/`.
  2. Run `lake build PEqualNP.Outside.<Module>`.
  3. In a scratch file, import the module and run `#print axioms <theorem>`. The expected output is
     `[propext, Classical.choice, Quot.sound]`.
  4. Check that the theorem statement is identical to the posted statement.

## SAT

- python-sat (pysat) 1.9.dev24, with the CaDiCaL and Glucose back ends.
- kissat 4.0.4, built from source.
- drat-trim, built from source; it checks kissat's DRAT proofs.
- UNSAT claims carry these labels:
  - **UNSAT**: solver verdict, with the encoding validated against known circuits so that it is not
    vacuous.
  - **DRAT**: kissat proof verified by drat-trim.
- Each folder's README lists the exact command line, encoding flags and runtime of every run. The
  CNF files are not stored (`.gitignore`) because they can be regenerated from the scripts.

## Python

- Python 3.13, numpy 2.5.3, sympy 1.14.0, networkx 3.7.

## Where things are

| What | Where |
|---|---|
| Research notes per problem | `research/L-meta-612/*/`, `research/gct196/`, `research/meta*/` |
| Lean proof files | `research/lean/` |
| Desk step log (one record per assigned step) | `research/desk-log.md`, `research/desk-log.json` |
| Who did what, when | `research/contributions.md` |
| Sanitized AI transcripts | `research/transcripts/export/` (one gzipped JSONL per session and per subagent, plus `index.json`) |
| Sanitizer | `research/transcripts/sanitize.py` |

## How the transcripts were sanitized

`sanitize.py` keeps the following:
- user and assistant text;
- tool calls (name and input);
- tool results, truncated to 4000 characters;
- timestamps and model ids.

It drops:
- system prompts, hook output, attachments, images and internal bookkeeping records;
- hidden reasoning blocks.

It also redacts private email addresses, private account identifiers and anything that looks like
a credential. The public contributor identity, the GitHub noreply address of `lenguyen259`, is kept.
