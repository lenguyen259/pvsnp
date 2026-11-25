#!/bin/bash
cd /tmp/claude-0/-home-user-pvsnp/0fc37754-ef86-508b-897b-e5f1fd591c14/scratchpad/petrec
JS=$(grep -P "^c1s14_4o\t" jobs.txt | cut -f5)


for v in "A2,N,B,B1,BB|" "A2,A3,N,B,B1,BB,B2,BB1,BBB|" "A2,N,B,B1,BB|--solver glucose4" "A2,N,B,B1,BB|--solver maplechrono"; do
  fam=${v%|*}; ex=${v#*|}
  python3 rec4.py 1 --sizes 14 --timeout 700 --fam $fam --tag "bench $v" --extra "--orbs $JS $ex" >> bench.log 2>&1
done
for v in "A2,N,B|--solver glucose4" "A2,N,B,B1,BB|--solver glucose3" "A2,N,B,B1,BB|--solver lingeling"; do
  fam=${v%|*}; ex=${v#*|}
  python3 rec4.py 1 --sizes 14 --timeout 700 --fam $fam --tag "bench $v" --extra "--orbs $JS $ex" >> bench.log 2>&1
done
JS2=$(grep -P "^c1s14_0o\t" jobs.txt | cut -f5)
python3 rec4.py 1 --sizes 14 --timeout 1800 --tag "bench 0o glucose4" --extra "--orbs $JS2 --solver glucose4" >> bench.log 2>&1
python3 rec4.py 1 --sizes 14 --timeout 1800 --fam A2,N,B --tag "bench 0o glucose4 A2NB" --extra "--orbs $JS2 --solver glucose4" >> bench.log 2>&1
python3 rec4.py 1 --sizes 14 --timeout 700 --fam A2,B --tag "bench A2B g4" --extra "--orbs $JS --solver glucose4" >> bench.log 2>&1
nohup ./worker2.sh >/dev/null 2>&1 &
