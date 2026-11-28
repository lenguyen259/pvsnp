#!/bin/sh
cd /home/user/pvsnp/research/meta9745
for s in 21 22 23 24; do
  side=left; [ $((s%2)) -eq 0 ] && side=right
  BUDGET=50000 MAXIN=10 MINK=6 python3 lns2.py $s ${1:-150} $side 0.6 9 0.05 > logs/p2_lns_$s.log 2>&1
  if ls found_* >/dev/null 2>&1; then exit 0; fi
done
