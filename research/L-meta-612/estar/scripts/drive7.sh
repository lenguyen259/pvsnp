#!/bin/bash
# usage: drive7.sh nmin nmax X lim nostar tmo out
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/e612
python3 -c "
from lib import graphs; import json
for n,E in graphs($1,$2): print(json.dumps(E))" | while read E; do
  timeout $6 python3 t7.py "$E" $3 $4 $5 >> $7 2>&1 || echo "TIMEOUT/ERR $E" >> $7
done
