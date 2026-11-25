#!/bin/sh
# sequential LNS runs (one CPU slot); args: total budget per run in seconds
cd /home/user/pvsnp/research/meta9745
for s in 11 12 13 14 15 16 17 18; do
  side=left; [ $((s%2)) -eq 0 ] && side=right
  python3 lns.py $s ${1:-240} $side 0.6 7 0.05 > logs/lns_$s.log 2>&1
  if ls found_* >/dev/null 2>&1; then exit 0; fi
done
