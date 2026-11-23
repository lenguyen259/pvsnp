#!/bin/bash
# drive.sh nmin nmax lim tmo log
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/s_case
python3 -c "
import sys; sys.path.insert(0,'../e612')
from lib import graphs; import json
for n,E in graphs($1,$2): print(json.dumps(E))" | while read E; do
  timeout $4 python3 dump.py "$E" $3 >> $5 2>&1 || echo "TIMEOUT/ERR $E" >> $5
done
echo DONE >> $5
