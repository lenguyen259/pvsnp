#!/bin/bash
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/petrec
mine(){ n=0; for p in $(pgrep -f "python3 enc4.py"); do [ "$(readlink /proc/$p/cwd)" = "$PWD" ] && n=$((n+1)); done; echo $n; }
while read nm js; do
  exec 9>slot.lock; flock 9
  while [ $(mine) -ge 2 ]; do sleep 10; done
  python3 rec4.py 0 --assume --sizes 18 --timeout 1800 --tag "PET18 $nm" --extra "--orbs $js" >> pet.log 2>&1 &
  P=$!; sleep 25; flock -u 9; wait $P
done < pcases.txt
