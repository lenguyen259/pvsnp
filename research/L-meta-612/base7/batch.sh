#!/bin/bash
# batch.sh LISTFILE [run7 extra args] : run run7.py on each "name<TAB>edges" line, sequentially (one solver at a time)
cd /home/user/pvsnp/research/L-meta-612/base7
lf=$1; shift
while IFS=$'\t' read -r nm E; do
  [ -z "$nm" ] && continue
  python3 run7.py "$nm" "$E" "$@"
done < "$lf"
