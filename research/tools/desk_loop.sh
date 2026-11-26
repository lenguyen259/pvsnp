#!/bin/sh
# poll -> auto-handle two-lit steps -> repeat; stops (exit) when a step needs the orchestrator
cd /home/user/pvsnp/research/tools
while true; do
  python3 poll4.py || exit 1
  python3 auto_twolit.py; rc=$?
  [ $rc -eq 2 ] && exit 2
  [ $rc -eq 3 ] && exit 3
done
