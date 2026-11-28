timeout 1300 python3 msat2.py '[[0,1],[2,3],[0,4],[2,4],[1,5],[2,5],[0,6],[3,6],[1,7],[3,7]]' 13 --timeout 1200 | grep RESULT >> e8b.log
timeout 1300 python3 msat2.py '[[0,1],[2,3],[0,4],[2,4],[1,5],[2,5],[0,6],[3,6],[1,7],[3,7]]' 13 --maxor 8 --timeout 1200 | grep RESULT >> e8b.log
timeout 1300 python3 msat2.py '[[0,1],[2,3],[0,4],[2,4],[1,5],[2,5],[0,6],[3,6],[1,7],[3,7]]' 13 --maxand 3 --timeout 1200 | grep RESULT >> e8b.log
