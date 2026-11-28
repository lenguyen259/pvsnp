#!/bin/bash
# collect results of orphaned job $1 (append + refine)
id=$1; out=jl/$id/out
line=$(grep -P "^$id\t" jobs.txt); C=$(echo "$line"|cut -f2); S=$(echo "$line"|cut -f3); T=$(echo "$line"|cut -f4); js=$(echo "$line"|cut -f5)
cat $out >> results.log
if grep -q "RESULT TIMEOUT" $out; then [ "$js" = "-" ] && js="[]"
 python3 refine.py $C "$js" | while IFS=$'\t' read nm cj; do printf "%s\t%s\t%s\t%s\t%s\n" "${id}_$nm" $C $S 900 "$cj" >> jobs.txt; done; fi
