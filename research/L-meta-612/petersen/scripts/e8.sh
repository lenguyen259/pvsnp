timeout 2500 python3 msat2.py '[[0,1],[2,3],[0,4],[2,4],[1,5],[2,5],[0,6],[3,6],[1,7],[3,7]]' 12 --timeout 2400 | grep RESULT >> e8.log
for s in 14 15 16; do timeout 1300 python3 msat2.py '[[0,1],[2,3],[0,4],[2,4],[1,5],[2,5],[0,6],[3,6],[1,7],[3,7]]' $s --maxor 7 --timeout 1200 | grep RESULT >> e8.log; done
