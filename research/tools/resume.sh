#!/bin/sh
# Restart the background work after a pause. Safe to run twice (skips jobs already running / logged).
R=/home/user/pvsnp/research
SC=/tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad
mkdir -p $SC /tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/cubes /tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/base7
pgrep -f "cubes.py jobs_H9_15g" >/dev/null || (cd $R/L-meta-612/petersen19 && setsid nohup sh ../../tools/cpuslot.sh python3 cubes.py jobs_H9_15g.txt logs/cubes_H9_15g.jsonl 2 7200 >/tmp/h9g.out 2>&1 &)
pgrep -f "cubes7.py G8t19" >/dev/null || (cd $R/L-meta-612/base7 && setsid nohup sh ../../tools/cpuslot.sh python3 -u cubes7.py G8t19 '[[0, 1], [0, 2], [0, 3], [1, 4], [2, 5], [3, 6], [4, 6], [4, 7], [5, 7], [6, 7]]' 12 >>logs/G8t19_c12.out 2>&1 &)
pgrep -f "poll4.py" >/dev/null || (cd $R/tools && setsid nohup python3 poll4.py >/tmp/poll4.out 2>&1 &)
sleep 3; ps -eo cmd | grep -E "cubes|poll4" | grep -v grep | cut -c1-80
