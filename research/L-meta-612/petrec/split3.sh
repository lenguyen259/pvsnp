#!/bin/bash
# split3.sh CLASS SIZE TIMEOUT k op LOG [rev] : level-2 split of first-level case k op (lock-based)
C=$1; S=$2; T=$3; K=$4; OP=$5; LOG=$6; REV=$7
python3 mkcases.py $C $K "$OP" > cases_${C}_${S}_${K}.txt
if [ -n "$REV" ]; then tac cases_${C}_${S}_${K}.txt > /tmp/cc_$$; else cp cases_${C}_${S}_${K}.txt /tmp/cc_$$; fi
while IFS=$'\t' read nm js; do
  mkdir locks2_${C}_${S}_${K}_${nm} 2>/dev/null || continue
  python3 rec4.py $C --sizes $S --timeout $T --tag "case $K $OP $nm" --extra "--orbs $js" >> $LOG 2>&1
done < /tmp/cc_$$
