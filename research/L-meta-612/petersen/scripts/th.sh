for s in 12 13 14 15 16; do timeout 2500 python3 msat.py '[[0,1],[1,2],[2,3],[3,7],[0,4],[4,5],[5,7],[0,6],[6,7]]' $s --lemd --full --timeout 2400 | grep RESULT >> th_lemd.log; done
