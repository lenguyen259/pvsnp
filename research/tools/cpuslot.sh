#!/bin/sh
# Run a heavy command only when one of N CPU slots is free (default N=4).
# Usage: cpuslot.sh <command...>   (env CPUSLOTS=N, CPUSLOT_DIR=/tmp/cpuslots)
# Waits until a slot lock can be taken; the lock is held for the command's lifetime.
N=${CPUSLOTS:-4}
D=${CPUSLOT_DIR:-/tmp/cpuslots}
mkdir -p "$D"
while :; do
  i=0
  while [ $i -lt $N ]; do
    exec 9>"$D/slot$i"
    if flock -n 9; then
      echo "$$ $(date -u +%H:%M:%S) $*" > "$D/slot$i.who"
      "$@"; rc=$?
      rm -f "$D/slot$i.who"
      exit $rc
    fi
    exec 9>&-
    i=$((i+1))
  done
  sleep 20
done
