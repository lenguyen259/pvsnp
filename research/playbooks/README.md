# Playbooks: distilled experience for agents

Every agent brief names the playbooks the agent must read before it starts. Every agent that
finishes a task, including one that fails, appends what it learned to the relevant playbook under
"Lessons" (dated, one line each, concrete: file, command, pitfall). The orchestrator merges these
and prunes stale ones. This is how the workflow improves from one task to the next without
retraining a model.

| Playbook | Use when |
|---|---|
| `desk.md` | Taking, holding, submitting or releasing a pequalnp desk step |
| `gtree-lower-bound.md` | Desk "Table 2" rows: an edge function needs at least N AND/OR/NOT gates |
| `sat-circuits.md` | Exact synthesis or UNSAT of small circuits (Petersen, NOT savings) |
| `lean-submission.md` | Writing, building and checking a Lean file for the desk |
| `conjecture-evolution.md` | Generating and filtering candidate lemmas (falsify first) |
| `orchestration.md` | The orchestrator's own rules: briefs, CPU, verification, reporting |

## Rules every agent follows

- Use only CPU slots from `research/tools/cpuslot.sh`: 4 slots shared by all agents. Kill only your
  own process IDs, never with `pkill -f <pattern>`.
- Label every claim as PROVED, LEAN, UNSAT, DRAT, DATA, REFUTED or TIMEOUT. Never call a claim
  proved because of numerics or a timeout.
- Validate an encoding or test before trusting a negative result from it: it must accept a known
  positive instance.
- Write notes in English in the task folder. Do not commit; the orchestrator commits.
