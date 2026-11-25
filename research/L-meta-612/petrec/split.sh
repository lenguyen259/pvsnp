#!/bin/bash
# split.sh CLASS SIZE TIMEOUT LOG
C=$1; S=$2; T=$3; LOG=$4
NO=$(python3 -c "from lib import *; print(len(pair_orbits(info($C)['E'])))")
for k in $(seq 0 $((NO-1))); do for op in '&' '|'; do
  if grep -q "case $k $op .*UNSAT" $LOG 2>/dev/null; then continue; fi
  ORB=$(python3 -c "from lib import *; import json; print(json.dumps([pair_orbits(info($C)['E']),$k,'$op'],separators=(',',':')))")
  python3 rec4.py $C --sizes $S --timeout $T --tag "case $k $op" --extra "--orb $ORB" >> $LOG 2>&1
done; done
echo DONE >> $LOG
