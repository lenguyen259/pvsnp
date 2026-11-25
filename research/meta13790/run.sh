#!/bin/bash
# min monotone size, then min general size (strict normal form), smallest SAT first
cd /home/user/pvsnp/research/meta13790
for s in 6 7 8 9 10 11 12; do timeout 1200 python3 -u enc.py $s mono --strict | tee -a mono.log; tail -1 mono.log | grep -q '^SAT' && break; done
for s in 6 7 8 9 10 11 12; do timeout 1800 python3 -u enc.py $s gen --strict | tee -a gen.log; tail -1 gen.log | grep -q '^SAT' && break; done
echo DONE >> gen.log
