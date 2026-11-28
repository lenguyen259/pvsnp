#!/bin/bash
# Find monotone minimum m by descending from the star bound, then test general (NOT allowed) at m-1.
cd /home/user/pvsnp/research/meta14209
m=14
for s in 14 13 12 11 10; do
  r=$(timeout 2400 python3 -u enc.py $s mono --strict); echo "$(date -u +%H:%M) $r" | tee -a mono.log
  case "$r" in SAT*) m=$s;; UNSAT*) break;; *) echo "$(date -u +%H:%M) TIMEOUT mono $s" >> mono.log; break;; esac
done
s=$((m-1)); r=$(timeout 3600 python3 -u enc.py $s gen --strict); echo "$(date -u +%H:%M) m=$m test gen at $s: ${r:-TIMEOUT}" | tee -a gen.log
echo DONE >> gen.log
