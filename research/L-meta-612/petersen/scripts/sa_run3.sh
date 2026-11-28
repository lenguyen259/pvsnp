for seed in 1 2 3 4 5 6; do for T in 0.3 0.7; do
 T0=$T timeout 200 python3 sa.py '[[0,1],[1,2],[2,3],[3,4],[4,0],[0,5],[1,6],[2,7],[3,8],[4,9],[5,7],[7,9],[9,6],[6,8],[8,5]]' or 26 20000000 $seed "$(cat gad.json)" | grep -E "BEST" | tail -1 | sed "s/^/orgad T=$T seed=$seed /" >> sa_or2.log
done; done
