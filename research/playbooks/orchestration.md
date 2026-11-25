# Playbook: the orchestrator's own rules (self-improvement log)

## Briefing agents

- Name the playbooks to read first, the exact statement, the file locations, the deliverable, the
  verification required and a time budget.
- Give a CPU budget in slots (see `cpuslot.sh`) and tell the agent to kill only its own PIDs.
- Ask for falsify-first: test candidate lemmas on data before any proof effort.
- Ask the agent to append lessons to the relevant playbook when it finishes.

## Verification (never skip)

- Rebuild every Lean result myself and run `#print axioms`.
- Check every claimed circuit on all inputs.
- Accept UNSAT only from an encoding validated against a known positive instance.

## Resources

- 4 cores. The task that gates decisions (currently Petersen) gets 2 slots; other tasks get 1 slot
  each. Check `tools/cpustatus.sh` before spawning agents.
- Never let generated binaries or large data into git. Keep each committed file under 5 MB; keep
  bulk data gzipped or ignored.

## Lessons (orchestrator)

- 2026-11-25: The first gct-196 agent quit after 11 minutes. Briefs for hard items must say "do not
  stop at the first failed approach" and set an explicit budget.
- 2026-11-25: Recipes passed between agents (10524 to 10952) saved setup time. They are now written
  into playbooks instead of being retyped.
- 2026-11-25: I committed a 55 MB file by accident, so I now check sizes before every commit.
- 2026-11-25: Six heavy processes on 4 cores slowed everything. Hence the slot scheduler.
