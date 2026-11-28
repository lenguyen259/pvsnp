#!/bin/sh
# Show who holds the CPU slots and the heaviest processes.
D=${CPUSLOT_DIR:-/tmp/cpuslots}
for f in "$D"/slot*.who; do [ -f "$f" ] && echo "$(basename "$f" .who): $(cat "$f")"; done
ps -eo pid,etime,pcpu,args --sort=-pcpu | awk 'NR==1 || $3>20' | cut -c1-160 | head -12
