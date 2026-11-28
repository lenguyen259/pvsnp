for seed in 3 4 5 6 7 8 9 10 11 12; do for S in 24 28; do
 T0=1.0 timeout 240 python3 sa.py '[[0,1],[1,2],[2,3],[3,4],[4,0],[0,5],[1,6],[2,7],[3,8],[4,9],[5,7],[7,9],[9,6],[6,8],[8,5]]' or $S 20000000 $seed | grep -E "BEST" | tail -1 | sed "s/^/or S=$S seed=$seed /" >> sa_or.log
done; done
