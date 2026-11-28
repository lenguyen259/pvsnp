#!/bin/bash
# worker2.sh: job queue worker; at most 2 enc4 processes globally; TIMEOUT jobs are refined into child jobs
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/petrec
mine(){ n=0; for p in $(pgrep -f "python3 enc4.py"); do [ "$(readlink /proc/$p/cwd)" = "$PWD" ] && n=$((n+1)); done; echo $n; }
while true; do
  exec 9>slot.lock; flock 9
  while [ $(mine) -ge 2 ]; do sleep 10; done
  job=""
  while IFS=$'\t' read id C S T js; do
    [ -z "$id" ] && continue
    mkdir -p jl; mkdir jl/$id 2>/dev/null || continue
    job="$id"; break
  done < jobs.txt
  if [ -z "$job" ]; then flock -u 9; [ -f STOP ] && exit; sleep 60; continue; fi
  if [ "$js" = "-" ]; then
    python3 rec4.py $C --sizes $S --timeout $T --tag "job $id" > jl/$id/out 2>&1 &
  else
    python3 rec4.py $C --sizes $S --timeout $T --tag "job $id" --extra "--orbs $js" > jl/$id/out 2>&1 &
  fi
  P=$!; sleep 25; flock -u 9; wait $P
  cat jl/$id/out >> results.log
  if grep -q "RESULT TIMEOUT" jl/$id/out; then
    [ "$js" = "-" ] && js="[]"
    python3 refine.py $C "$js" | while IFS=$'\t' read nm cj; do printf "%s\t%s\t%s\t%s\t%s\n" "${id}_$nm" $C $S 300 "$cj" >> jobs.txt; done
  fi
  if grep -q "RESULT SAT" jl/$id/out; then echo "!!! SAT in $id" >> results.log; fi
done
