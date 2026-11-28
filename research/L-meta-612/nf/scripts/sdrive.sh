#!/bin/bash
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/nf
for X in $3; do while read E; do timeout $4 python3 split.py "$E" $X $5 >> $2 2>&1 || echo "TIMEOUT $E $X" >> $2; done < $1; done
echo DONE >> $2
