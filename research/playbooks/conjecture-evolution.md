# Playbook: evolving lemmas (falsify first, prove last)

The goal is to stop proving lemmas that are false or too weak. Candidate lemmas are evolved against
data, and only the survivors are proved.

## Loop (one generation)

1. **Generate.** Ask an LLM for 20-50 candidate lemmas toward the target. Write each one as a
   Python predicate over (graph, circuit), plus restrictions if needed, as in
   `research/L-meta-612/ledger/falsify.py`. Give each a one-line math statement and a note on which
   ledger claim it would imply.
2. **Falsify.** Run every candidate on the whole store (`ledger/circuits*.jsonl`, plus fresh
   random or enumerated circuits). Record the smallest counterexample for each candidate that
   dies.
3. **Score the survivors.**
   - Strength: does it imply the target, or close an open ledger node? How many open cases does it
     cover?
   - Tightness: on how many circuits is it tight?
   - Simplicity: how short is it?
4. **Mutate.** Feed the best survivors and the smallest counterexamples of the dead candidates back
   to the LLM. Ask for strengthenings, generalizations, alternative hypotheses and combinations.
5. **Promote.** A candidate that survives at least 3 generations and has high strength goes to a
   proof agent, then to two independent reviewers, then to a Lean skeleton.

## Bookkeeping

- Add every candidate to the ledger with its status: refuted (with its counterexample), surviving
  (with its generation count) or proved.
- Never re-propose a refuted statement unless the hypothesis has changed.

## Lessons

- (none yet; first run planned on L-meta-612 for max degree <= 3)
