#!/bin/bash
# auto.sh CLASS MONO_TO SPLIT_TO  : all sizes below phi
C=$1; MT=$2; ST=$3; LOG=auto$C.log
PHI=$(python3 -c "from lib import *; print(info($C)['phi'])")
for S in $(seq 1 $((PHI-1))); do
  python3 rec4.py $C --sizes $S --timeout $MT --tag mono >> $LOG 2>&1
  if tail -1 $LOG | grep -q -E "UNSAT"; then continue; fi
  if tail -1 $LOG | grep -q -E "RESULT SAT"; then echo "SATFOUND $S" >> $LOG; exit; fi
  ./split.sh $C $S $ST split${C}_$S.log
  if grep -q "RESULT SAT\|TIMEOUT" split${C}_$S.log; then echo "OPEN at $S" >> $LOG; exit; fi
  echo "SPLIT-UNSAT $S" >> $LOG
done
echo "PROVED $C $PHI" >> $LOG
