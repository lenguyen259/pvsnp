#!/bin/bash
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/tf
while read E; do timeout 600 python3 tdump.py "$E" 1500 >> $2 2>&1 || echo "TIMEOUT/ERR $E" >> $2; done < $1
echo DONE >> $2
