#!/bin/bash
# worker.sh : repeatedly takes the first unlocked job from jobs.txt (lines: id<TAB>C<TAB>S<TAB>T<TAB>orbs-json-or-'-'), logs to results.log
while true; do
  got=0
  while IFS=$'\t' read id C S T js; do
    [ -z "$id" ] && continue
    mkdir -p jl; mkdir jl/$id 2>/dev/null || continue
    got=1
    if [ "$js" = "-" ]; then ex=""; else ex="--orbs $js"; fi
    if [ -z "$ex" ]; then python3 rec4.py $C --sizes $S --timeout $T --tag "job $id" >> results.log 2>&1
    else python3 rec4.py $C --sizes $S --timeout $T --tag "job $id" --extra "$ex" >> results.log 2>&1; fi
    break
  done < jobs.txt
  if [ $got = 0 ]; then [ -f STOP ] && exit; sleep 30; fi
done
