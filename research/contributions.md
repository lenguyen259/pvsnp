# Who did what, and when

The work has three actors:
- **Human**: the contributor `lenguyen259`.
- **Orchestrator**: the Claude Code session that planned the work, briefed agents, verified results
  and ran git and the desk calls.
- **Agents**: Claude Opus subagents, at medium or high effort. Their full traces are in
  `transcripts/export/`; `index.json` maps each file to the agent's task description.

Dates are 2026-11 and times are UTC, approximate to within a commit. Labels:
- **PROVED**: hand proof, reviewed by an agent other than its author.
- **LEAN**: formal proof that builds and uses only the standard axioms.
- **DATA**: machine check only.

## Human decisions and interventions

These are the only human inputs; every one is in the session transcript.
- Chose the project (pequalnp.com) and the handle, and set the rules: commits under `lenguyen259`,
  research files in English, reports in Vietnamese.
- Picked L-meta-612 and asked for it to be researched "to the end".
- Picked the model and effort for agents (Opus medium; Opus high from 2026-11-25 11:0x).
- Approved force-pushes to the research branch (authorship rewrite; removing binaries).
- Opened the upstream pull request for L-meta-10524 from their GitHub account, because the session
  could not reach the upstream repository.
- Supplied two papers the session could not download: the Lenz–Wegener TCS 1991 paper in full, and
  Alon–Boppana.
- Chose, for L-gct-196: keep the step, make a third attempt, and ask for a second step in parallel.
- Chose to pursue L-meta-612 privately, gated on the Petersen result.

The human gave no mathematical ideas, lemmas or proof steps. All mathematics below came from agents
or the orchestrator.

## Mathematical results and who produced them

| When | Result | Status | Produced by | Checked by |
|---|---|---|---|---|
| 11-23 | E*, star-case analysis, Theorems A and B | PROVED / REFUTED parts | agents | orchestrator + agents |
| 11-23 | Theorem S (STAR-ALL), Theorem S2, Lemmas L and A | PROVED | agents | agents |
| 11-23 | Reduction of the OR half to Lemma D; Theorem F (≤ 1 vertex of degree ≥ 3) | PROVED | agents | agents |
| 11-24 | L-meta-612 implies Jukna's Problem 24 | PROVED (short) | agent | orchestrator |
| 11-24 | The (OR) split is false: Petersen 13-OR circuit; Lemma M' refuted | REFUTED (DATA) | agents (SAT) | decoded circuits verified on all inputs |
| 11-24 | T2–T8, T10: forests, max degree 2, suns, Lemma DG, clean formulas | PROVED / REFUTED | agents | agents |
| 11-24 | **Theorem PF**: #AND ≥ tau for C4-free pseudoforests, which with L_meta_599 gives the full bound | PROVED | agent (t9) | independent review agent (review9) |
| 11-25 06:xx | Lean files for L-meta-413, 418, 420, 421, 510 | LEAN | agents | orchestrator (rebuild + axioms) |
| 11-25 10:27 | **Theorem PF in Lean** (PF_AND.lean, 1157 lines) | LEAN | agent, about 17 min | orchestrator (rebuild + axioms) |
| 11-25 10:30 | Literature check: PF and Theorem F appear new; Lenz–Wegener Thm 4.2 covers disjoint triangles | DATA (reading) | agent + orchestrator | human supplied the paper |
| 11-25 11:00–12:25 | L-gct-196: partial Lean results, the N8 family, conjecture 3 dim L ≤ pq | LEAN (partial) / DATA | 3 agents | orchestrator |
| 11-25 12:03–12:16 | **L-meta-10524**: ≥ 14 gates over AND/OR/NOT | LEAN, submitted | agent, about 8 min | orchestrator (rebuild, axioms, exact statement) |
| 11-25 12:16–12:41 | L-meta-10952: checker limit analysis | DATA | agent | orchestrator |
| 11-25 → | Petersen size 19: H7, H8a, H8b bounds unconditional, H9 ≥ 15, P without H9 ≥ 16 | UNSAT, with DRAT for H8a | agent | drat-trim |

## Process facts useful for evaluation

- Triage of out-of-reach desk steps took under 1 minute each; there were 6 such steps.
- Several agents stopped early or failed:
  - The first L-gct-196 agent quit after 11 minutes.
  - One agent's `pkill` killed another agent's jobs.
  - A lease was lost on a worker restart.

  These are recorded in the transcripts and in the session summary.
- Every claimed proof was rebuilt by the orchestrator before it was reported or submitted.
  Every claimed counterexample circuit was checked on all inputs.
