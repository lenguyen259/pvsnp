#!/bin/bash
# runlevel2.sh NAME EDGES RESTFILE SMIN SMAX TIMEOUT : sizes SMIN..SMAX, flags --factc --viol --lexbot (pysat CaDiCaL)
cd /home/user/pvsnp/research/L-meta-612/petersen19
nm=$1; E=$2; RF=$3; A=$4; M=$5; TO=$6
for s in $(seq $A $M); do
  r=$(timeout $((TO+300)) python3 enc5.py $s --graph "$E" --rest $RF --factc --viol --lexbot --solve --timeout $TO 2>&1 | grep -E "RESULT|VERIF|Error" | tr '\n' ' ')
  echo "$nm s=$s [$RF lexbot] $r" >> logs/$nm.log
  echo "$r" | grep -q "RESULT UNSAT" || break
done
