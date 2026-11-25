#!/bin/bash
# drat.sh TAG s ENC5-ARGS... : write CNF, kissat with DRAT proof, check with drat-trim
cd /home/user/pvsnp/research/L-meta-612/petersen19
tag=$1; s=$2; shift 2
C=/tmp/claude-0/-home-user/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/$tag.cnf; P=${C%.cnf}.drat
python3 enc5.py $s "$@" --dimacs $C > /dev/null
r=$(./kissat -q --no-binary $C $P | grep '^s ')
if [ "$r" = "s UNSATISFIABLE" ]; then
  v=$(timeout 3000 ./drat-trim $C $P -t 3000 2>&1 | tr -d "\r" | grep -E "^s (VERIFIED|NOT VERIFIED)|TIMEOUT" | head -1)
else v="-"; fi
echo "$tag s=$s kissat: $r ; drat-trim: $v" >> logs/drat.log
rm -f $C $P
