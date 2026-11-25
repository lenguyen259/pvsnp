#!/bin/bash
# drat.sh file.cnf : kissat with DRAT proof, then drat-trim. Appends one line to drat.log.
K=/home/user/pvsnp/research/L-meta-612/petersen19
C=$1; P=/tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/$(basename ${C%.cnf}).drat
t0=$(date +%s)
r=$($K/kissat -q --no-binary $C $P | grep '^s ')
t1=$(date +%s)
if [ "$r" = "s UNSATISFIABLE" ]; then
  v=$(timeout 3000 $K/drat-trim $C $P -t 3000 2>&1 | tr -d "\r" | grep -E "^s (VERIFIED|NOT VERIFIED)|TIMEOUT" | head -1)
else v="-"; fi
echo "$C kissat: $r ($((t1-t0))s) ; drat-trim: $v ($(( $(date +%s)-t1 ))s)" >> drat.log
rm -f $P
