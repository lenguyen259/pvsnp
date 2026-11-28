for T in 0.5 1.0; do for mode in size or and; do for seed in 1 2; do
 T0=$T timeout 300 python3 sa.py '[[0,1],[1,2],[2,3],[3,4],[4,0],[0,5],[1,6],[2,7],[3,8],[4,9],[5,7],[7,9],[9,6],[6,8],[8,5]]' $mode 24 20000000 $seed | grep -E "BEST|final" | tail -1 | sed "s/^/$mode T=$T seed=$seed /" | cut -c1-400 >> sa_pet.log
done; done; done
