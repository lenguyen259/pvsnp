#!/bin/bash
# sequential (AND) SAT checks, one solver at a time
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/t9
T2="0-1,1-2,0-2,3-4,4-5,3-5"; C5="0-1,1-2,2-3,3-4,0-4"; C35="0-1,1-2,0-2,3-4,4-5,5-6,6-7,3-7"; C6="0-1,1-2,2-3,3-4,4-5,0-5"
run(){ timeout $(( $5 + 30 )) python3 scripts/andsat.py $1 $2 $3 /dev/null $5 2>&1 | grep -E "^G|CIRCUIT"; }
run $T2 9 4 x 300      # non-vacuity: Phi(2C3)=9 with 4 ANDs
for s in 9 10 11 12 13; do run $T2 $s 3 x 600; done
for s in 7 8 9 10 11; do run $C5 $s 2 x 600; done
for s in 8 9 10 11; do run $C6 $s 2 x 600; done
for s in 12 13; do run $C35 $s 4 x 900; done
