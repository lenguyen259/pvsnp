#!/bin/bash
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t9
C5="0-1,1-2,2-3,3-4,0-4"; C6="0-1,1-2,2-3,3-4,4-5,0-5"
run(){ timeout $5 python3 scripts/andsat.py $1 $2 $3 /dev/null $5 2>&1 | grep -E "^G|CIRCUIT" || echo "G $1 s $2 amax $3 TIMEOUT(>$5s)"; }
run $C5 7 3 x 120
for s in 7 8 9 10; do run $C5 $s 2 x 240; done
for s in 8 9 10; do run $C6 $s 2 x 240; done
