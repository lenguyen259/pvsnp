#!/bin/sh
# chain.sh NAME EDGES : finish s=13 for an 8-vertex graph: k>=6 cubes, then k=5 sub-cubes (ops of gates 8,9,10). Safe to re-run: finished cubes are skipped.
N=$1; E=$2
cd /home/user/pvsnp/research/L-meta-612/base7
ONLY='&6,|6,&7,|7,&8,|8,&9,|9,&10,|10,&11,|11,&12,|12,&13,|13'
sh ../../tools/cpuslot.sh python3 -u cubes7.py $N "$E" 13 --to 3000 --only "$ONLY" >> logs/${N}_chain.out 2>&1
sh ../../tools/cpuslot.sh python3 -u cubes7.py $N "$E" 13 --to 3000 --only '&5,|5' --splitops 8,9,10 >> logs/${N}_chain.out 2>&1
