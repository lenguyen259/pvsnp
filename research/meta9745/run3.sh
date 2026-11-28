#!/bin/sh
cd /home/user/pvsnp/research/meta9745
for s in 31 32; do
  side=left; [ $((s%2)) -eq 0 ] && side=right
  BUDGET=20000 MAXIN=9 MINK=5 python3 lns2.py $s ${1:-240} $side 0.6 8 0.05 > logs/p3_lns_$s.log 2>&1
  if ls found_* >/dev/null 2>&1; then exit 0; fi
done
