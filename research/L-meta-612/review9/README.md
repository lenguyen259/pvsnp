# Independent review of t9 (pseudoforest AND bound)

Verdict of an independent adversarial review: correct, no gap in Lemma X1, Lemma AL, Lemma AND-core
and Theorem PF. Notes: Theorem PF should say explicitly that the circuit is reduced first (constants,
copies and dead gates removed; this never adds an AND gate). Step 2 already gives t_v in Q_a for every
neighbour a, so steps 3-5 shorten to: E(v) is the unique exit of both neighbours, entered at t_v,
which contradicts step 5.
Machine checks: SAT found no circuit with #AND <= tau - 1 on C3, P4, paw, P5, C3+P2, C5, bull, P6,
C6, net, C5+pendant, spider, 2C3, C7 (sizes up to the Lean OR bound plus slack); an independent
re-implementation confirmed every restriction step on 10,044 circuits; 30,000 random circuits.
