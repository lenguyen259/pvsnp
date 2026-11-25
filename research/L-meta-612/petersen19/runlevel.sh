#!/bin/bash
# runlevel.sh NAME EDGES MAXS TIMEOUT : run sizes 1..MAXS (stop at first non-UNSAT)
cd /home/user/pvsnp/research/L-meta-612/petersen19
nm=$1; E=$2; M=$3; TO=$4
for s in $(seq 1 $M); do
  r=$(timeout $((TO+300)) python3 enc5.py $s --graph "$E" --rest rest_$nm.json --factc --viol --solve --timeout $TO 2>&1 | grep -E "RESULT|VERIF|Error" | tr '\n' ' ')
  echo "$nm s=$s $r" >> logs/$nm.log
  echo "$r" | grep -q "RESULT UNSAT" || break
done
