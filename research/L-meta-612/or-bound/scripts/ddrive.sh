#!/bin/bash
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/orb
# $1 list file, $2 log, $3 X list, $4 timeout
for X in $3; do while read E; do timeout $4 python3 dsat.py "$E" $X >> $2 2>&1 || echo "TIMEOUT $E $X" >> $2; done < $1; done
echo DONE >> $2
