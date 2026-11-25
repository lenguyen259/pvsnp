#!/bin/bash
# split2.sh CLASS SIZE TIMEOUT LOG [rev]  -- lock-based, can run 2 copies
C=$1; S=$2; T=$3; LOG=$4; REV=$5
NO=$(python3 -c "from lib import *; print(len(pair_orbits(info($C)['E'])))")
CASES=""; for k in $(seq 0 $((NO-1))); do CASES="$CASES $k:a $k:o"; done
if [ -n "$REV" ]; then CASES=$(echo $CASES | tr ' ' '\n' | tac | tr '\n' ' '); fi
for cs in $CASES; do
  k=${cs%:*}; o=${cs#*:}; op='&'; [ $o = o ] && op='|'
  mkdir locks_${C}_${S}_${k}_$o 2>/dev/null || continue
  ORB=$(python3 -c "from lib import *; import json; print(json.dumps([pair_orbits(info($C)['E']),$k,'$op'],separators=(',',':')))")
  python3 rec4.py $C --sizes $S --timeout $T --tag "case $k $op" --extra "--orb $ORB" >> $LOG 2>&1
done
